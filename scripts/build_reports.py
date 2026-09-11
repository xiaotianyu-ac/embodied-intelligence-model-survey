#!/usr/bin/env python3
"""Build the bilingual survey PDFs from canonical Markdown and referenced SVGs.

Requires reportlab. svglib is optional: the bundled fallback reads the basic SVG
elements used by this repository's diagrams. Set SURVEY_CJK_FONT or --font when
Arial Unicode is unavailable. Source Markdown is never rewritten.
"""
from pathlib import Path
import argparse
import html
import os
import re
import textwrap
from urllib.parse import urljoin
import xml.etree.ElementTree as ET

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, LongTable, TableStyle, Preformatted, HRFlowable, Image
from reportlab.graphics.shapes import Drawing, Rect, Line, PolyLine, Polygon, String, Circle, Group
import reportlab.lib.textsplit as textsplit
import reportlab.platypus.paragraph as paragraph_module

ROOT = Path(__file__).resolve().parents[1]
PAGE = (595.28, 841.89)
DOCUMENT_NAME = 'survey-report.md'
for module in (textsplit, paragraph_module):
    module.ALL_CANNOT_START += '，：；！？）》】」』”’'

def resolve_font(explicit=None):
    candidates = [explicit, os.getenv('SURVEY_CJK_FONT'),
        '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
        '/Library/Fonts/Arial Unicode.ttf',
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc']
    for p in candidates:
        if p and Path(p).is_file():
            return str(p)
    raise SystemExit('Set SURVEY_CJK_FONT to a CJK TrueType font or pass --font PATH.')

def fonts(explicit=None):
    pdfmetrics.registerFont(TTFont('SurveyUnicode', resolve_font(explicit)))
    pdfmetrics.registerFontFamily('SurveyUnicode',normal='SurveyUnicode',bold='SurveyUnicode',italic='SurveyUnicode',boldItalic='SurveyUnicode')
    reg=Path('/System/Library/Fonts/Supplemental/Arial.ttf')
    bold=Path('/System/Library/Fonts/Supplemental/Arial Bold.ttf')
    if reg.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont('SurveyLatin',str(reg)))
        pdfmetrics.registerFont(TTFont('SurveyLatinBold',str(bold)))
        pdfmetrics.registerFontFamily('SurveyLatin',normal='SurveyLatin',bold='SurveyLatinBold',italic='SurveyLatin',boldItalic='SurveyLatinBold')
        return 'SurveyLatin'
    return 'SurveyUnicode'

def inline(raw):
    """A deliberately small Markdown inline subset, escaped before PDF markup."""
    s=html.escape(raw.replace('\u2011','-').replace('\u2013','-').replace('\u2014',' - '))
    s=re.sub(r'\[\^(\d+)\]',lambda m:f'<super><link href="#ref-{m[1]}" color="#315b7c">[{m[1]}]</link></super>',s)
    def mdlink(m):
        target=html.unescape(m[2])
        if not target.startswith(('https://','http://')):
            target=urljoin('https://github.com/xiaotianyu-ac/embodied-intelligence-model-survey/blob/main/records/artifacts/'+DOCUMENT_NAME,target)
        return f'<link href="{html.escape(target,quote=True)}" color="#315b7c">{m[1]}</link>'
    s=re.sub(r'\[([^\]]+)\]\(([^\s)]+)\)',mdlink,s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)',r'<i>\1</i>',s)
    s=re.sub(r'`([^`]+)`',r'<font color="#333333">\1</font>',s)
    return s

def num(x,default=0):
    return float(re.sub(r'(px|pt)$','',str(x))) if x is not None else default

def svg_color(value,default=None):
    if value=='none': return None
    if value is None: return default
    return colors.toColor(value)

def simple_svg(path):
    """Read rect/line/polyline/polygon/circle/text/group SVGs as real vectors.

    Fail explicitly on unsupported visible elements rather than silently dropping
    content. This is sufficient for the repository's portable, plain SVG figures.
    """
    root=ET.parse(path).getroot()
    view=[float(v) for v in root.attrib.get('viewBox','').split()]
    width=num(root.attrib.get('width'),view[2] if view else 800)
    height=num(root.attrib.get('height'),view[3] if view else 500)
    drawing=Drawing(width,height)
    def visit(el,parent,inherited):
        tag=el.tag.rsplit('}',1)[-1]
        if tag in ('title','desc','defs','metadata'): return
        style=dict(inherited)
        style.update(el.attrib)
        style.update(dict(x.split(':',1) for x in el.attrib.get('style','').split(';') if ':' in x))
        style={k.strip():v.strip() for k,v in style.items()}
        stroke=svg_color(style.get('stroke'))
        fill=svg_color(style.get('fill'),colors.black)
        sw=num(style.get('stroke-width'),1)
        dash=style.get('stroke-dasharray')
        opts=dict(strokeColor=stroke,fillColor=fill,strokeWidth=sw)
        if dash and dash!='none': opts['strokeDashArray']=[float(x) for x in re.split('[ ,]+',dash)]
        if tag in ('svg','g'):
            if 'transform' in el.attrib:
                raise ValueError(f'Unsupported SVG transform in {path}; use flat vector coordinates or install svglib.')
            for child in el: visit(child,parent,style)
            return
        if tag=='rect':
            parent.add(Rect(num(style.get('x')),height-num(style.get('y'))-num(style.get('height')),num(style.get('width')),num(style.get('height')),**opts))
        elif tag=='line':
            opts.pop('fillColor',None)
            parent.add(Line(num(style.get('x1')),height-num(style.get('y1')),num(style.get('x2')),height-num(style.get('y2')),**opts))
        elif tag in ('polyline','polygon'):
            points=[float(x) for x in re.split(r'[ ,]+',style['points'].strip())]
            points=[v if i%2==0 else height-v for i,v in enumerate(points)]
            parent.add((PolyLine if tag=='polyline' else Polygon)(points,**opts))
        elif tag=='circle':
            parent.add(Circle(num(style.get('cx')),height-num(style.get('cy')),num(style.get('r')),**opts))
        elif tag=='text':
            if len(el): raise ValueError(f'Unsupported nested SVG text in {path}; install svglib.')
            face='SurveyUnicode' if re.search(r'[\u3400-\u9fff]',el.text or '') else ('SurveyLatinBold' if style.get('font-weight') in ('bold','600','700') and 'SurveyLatinBold' in pdfmetrics.getRegisteredFontNames() else 'SurveyUnicode')
            parent.add(String(num(style.get('x')),height-num(style.get('y')),el.text or '',fontName=face,fontSize=num(style.get('font-size'),16),fillColor=fill,textAnchor=style.get('text-anchor','start')))
        else:
            raise ValueError(f'Unsupported SVG element {tag} in {path}; install svglib.')
    visit(root,drawing,{})
    return drawing

def figure(path,max_width,max_height=390):
    if not path.is_file(): raise FileNotFoundError(f'Referenced figure not found: {path}')
    if path.suffix.lower()=='.svg':
        try:
            from svglib.svglib import svg2rlg
        except ImportError:
            drawing=simple_svg(path)
        else:
            drawing=svg2rlg(str(path))
        scale=min(max_width/drawing.width,max_height/drawing.height,1)
        drawing.scale(scale,scale)
        drawing.width*=scale; drawing.height*=scale
        drawing.hAlign='CENTER'
        return drawing
    image=Image(str(path))
    scale=min(max_width/image.imageWidth,max_height/image.imageHeight,1)
    image.drawWidth=image.imageWidth*scale; image.drawHeight=image.imageHeight*scale
    return image

class SurveyDoc(SimpleDocTemplate):
    def afterFlowable(self,f):
        if isinstance(f,Paragraph) and f.style.name in ('H1','H2','H3'):
            level={'H1':0,'H2':1,'H3':2}[f.style.name]
            key='section-'+str(self.seq.nextf('section'))
            self.canv.bookmarkPage(key)
            # Keep PDF outlines legal when source skips a heading level.
            level=min(level,getattr(self,'previous_outline_level',-1)+1)
            self.canv.addOutlineEntry(f.getPlainText(),key,level,False)
            self.previous_outline_level=level

def make_styles(lang,latin):
    face='SurveyUnicode' if lang=='zh' else latin
    base=dict(fontName=face,textColor=colors.HexColor('#161616'),alignment=TA_LEFT,
              wordWrap='CJK' if lang=='zh' else 'LTR',allowWidows=0,allowOrphans=0)
    return {
      'body':ParagraphStyle('Body',fontSize=9.8 if lang=='zh' else 10.5,leading=16 if lang=='zh' else 14.7,spaceAfter=6,**base),
      'title':ParagraphStyle('Title',fontSize=21,leading=28,spaceAfter=18,**base),
      'h1':ParagraphStyle('H1',fontSize=14.5,leading=21,spaceBefore=16,spaceAfter=8,keepWithNext=True,**base),
      'h2':ParagraphStyle('H2',fontSize=11.6,leading=17.5,spaceBefore=12,spaceAfter=6,keepWithNext=True,**base),
      'h3':ParagraphStyle('H3',fontSize=10.6,leading=16,spaceBefore=10,spaceAfter=5,keepWithNext=True,**base),
      'cell':ParagraphStyle('Cell',fontSize=8 if lang=='zh' else 8.2,leading=11.7,rightIndent=1,spaceAfter=0,**base),
      'head':ParagraphStyle('Head',fontSize=8.2,leading=12,rightIndent=1,spaceAfter=0,**base),
      'ref':ParagraphStyle('Ref',fontSize=8.2,leading=11.7,spaceAfter=5,**base),
      'caption':ParagraphStyle('Caption',fontSize=8.4,leading=12,spaceBefore=4,spaceAfter=10,textColor=colors.HexColor('#4b4b4b'),**{k:v for k,v in base.items() if k!='textColor'}),
      'code':ParagraphStyle('Code',fontName='SurveyUnicode',fontSize=8.1,leading=11,spaceBefore=5,spaceAfter=9,leftIndent=8,rightIndent=8),
      'bullet':ParagraphStyle('Bullet',fontSize=9.8 if lang=='zh' else 10.5,leading=16 if lang=='zh' else 14.7,spaceAfter=5,leftIndent=11,firstLineIndent=-11,**base),
    }

def cells(line):
    return [x.strip().replace('\\|','|') for x in re.split(r'(?<!\\)\|',line.strip().strip('|'))]

def table(rows,width,styles):
    n=max(len(r) for r in rows)
    rows=[r+['']*(n-len(r)) for r in rows]
    # Human-readable comparison columns get width according to their content,
    # bounded so compact labels cannot consume an entire page column.
    weights=[]
    for c in range(n):
        mean=sum(min(len(re.sub(r'\[\^\d+\]','',r[c])),180) for r in rows)/len(rows)
        weights.append(max(16,min(55,mean**0.67*3)))
    if n>=4: weights[0]=min(weights[0],22)
    total=sum(weights)
    widths=[width*w/total for w in weights]
    if styles['cell'].wordWrap!='CJK':
        # Reserve room for ordinary English words so labels do not end with a
        # stranded final letter. Long technical identifiers may still wrap.
        minimum=[]
        for c in range(n):
            clean=' '.join(re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',r[c]) for r in rows)
            tokens=re.findall(r'[A-Za-z][A-Za-z0-9+./-]*',clean)
            longest=max((pdfmetrics.stringWidth(t.rstrip('.'),styles['cell'].fontName,styles['cell'].fontSize) for t in tokens),default=0)
            minimum.append(min(longest+12,95,width/n*.85))
        widths=[max(w,m) for w,m in zip(widths,minimum)]
        excess=sum(widths)-width
        spare=sum(w-m for w,m in zip(widths,minimum))
        if excess>0 and spare>0:
            widths=[w-excess*(w-m)/spare for w,m in zip(widths,minimum)]
    data=[[Paragraph(inline(v),styles['head' if ri==0 else 'cell']) for v in row] for ri,row in enumerate(rows)]
    tab=LongTable(data,colWidths=widths,repeatRows=1,hAlign='LEFT',splitByRow=1,splitInRow=1)
    tab.setStyle(TableStyle([
      ('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#eceff1')),
      ('LINEABOVE',(0,0),(-1,0),.65,colors.HexColor('#202020')),
      ('LINEBELOW',(0,0),(-1,0),.5,colors.HexColor('#777777')),
      ('LINEBELOW',(0,1),(-1,-1),.25,colors.HexColor('#d5d5d5')),
      ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),
      ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    return tab

def is_special(line):
    return not line or bool(re.match(r'^(#{1,6}\s|\||```|~~~|!\[|\[\^\d+\]:|[-*+]\s|\d+[.)]\s|>\s|---+$)',line))

def parse(source,doc,styles):
    lines=source.read_text(encoding='utf-8').splitlines(); story=[]; i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line: i+=1; continue
        if line.startswith(('```','~~~')):
            fence=line[:3]; block=[]; i+=1
            while i<len(lines) and not lines[i].strip().startswith(fence): block.append(lines[i]); i+=1
            # Source code and Mermaid remain explicit text unless supplied as an
            # image. Never substitute a fixed or unrelated diagram for a block.
            wrapped=[]
            for b in block:
                wrapped.extend(textwrap.wrap(b,90,replace_whitespace=False,drop_whitespace=False) or [''])
            story.append(Preformatted('\n'.join(wrapped),styles['code'])); i+=1; continue
        img=re.fullmatch(r'!\[([^\]]*)\]\(([^)]+)\)',line)
        if img:
            story.append(figure((source.parent/img[2]).resolve(),doc.width))
            if img[1]: story.append(Paragraph(inline(img[1]),styles['caption']))
            i+=1; continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                row=cells(lines[i])
                if not all(re.fullmatch(r'[:\- ]+',c) for c in row): rows.append(row)
                i+=1
            if rows: story.extend([table(rows,doc.width,styles),Spacer(1,9)])
            continue
        h=re.match(r'^(#{1,6})\s+(.+)',line)
        if h:
            level=len(h[1]); style=styles['title' if level==1 else 'h1' if level==2 else 'h2' if level==3 else 'h3']
            if level==1:
                plain=re.sub(r'[*`]','',h[2])
                available=doc.width-14
                needed=pdfmetrics.stringWidth(plain,style.fontName,style.fontSize)
                if needed>available:
                    style=ParagraphStyle('TitleFit',parent=style,fontSize=max(10,style.fontSize*available/needed*.985),leading=26)
            story.append(Paragraph(inline(h[2]),style)); i+=1; continue
        ref=re.match(r'^\[\^(\d+)\]:\s*(.*)',line)
        if ref:
            val=ref[2]
            while i+1<len(lines) and lines[i+1].startswith('    '):
                i+=1; val+=' '+lines[i].strip()
            story.append(Paragraph(f'<a name="ref-{ref[1]}"/>[{ref[1]}] '+inline(val),styles['ref'])); i+=1; continue
        if re.fullmatch(r'[-*_]{3,}',line):
            story.extend([Spacer(1,4),HRFlowable(width='100%',thickness=.4,color=colors.HexColor('#bbbbbb')),Spacer(1,7)]); i+=1; continue
        bullet=re.match(r'^([-*+]|\d+[.)])\s+(.+)',line)
        if bullet:
            label='•' if bullet[1] in '-*+' else bullet[1]
            story.append(Paragraph(inline(label+' '+bullet[2]),styles['bullet'])); i+=1; continue
        if line.startswith('> '):
            story.append(Paragraph(inline(line[2:]),styles['body'])); i+=1; continue
        chunk=[line]
        while i+1<len(lines) and not is_special(lines[i+1].strip()):
            i+=1; chunk.append(lines[i].strip())
        story.append(Paragraph(inline(' '.join(chunk)),styles['body'])); i+=1
    return story

def build(lang,latin):
    global DOCUMENT_NAME
    suffix='' if lang=='zh' else '-en'
    source=ROOT/f'records/artifacts/survey-report{suffix}.md'
    DOCUMENT_NAME=source.name
    output=ROOT/f'reports/embodied-intelligence-model-survey{suffix}.pdf'
    output.parent.mkdir(parents=True,exist_ok=True)
    first=next((l[2:].strip() for l in source.read_text().splitlines() if l.startswith('# ')),'Embodied Intelligence Model Survey')
    doc=SurveyDoc(str(output),pagesize=PAGE,rightMargin=46,leftMargin=46,topMargin=43,bottomMargin=43,
      title=first,author='Embodied Intelligence Model Survey',pageCompression=1)
    styles=make_styles(lang,latin)
    story=parse(source,doc,styles)
    def page(c,d):
        c.saveState();c.setFont('SurveyUnicode',7.4);c.setFillColor(colors.HexColor('#777777'))
        c.drawCentredString(PAGE[0]/2,23,str(d.page));c.restoreState()
    doc.build(story,onFirstPage=page,onLaterPages=page)
    print(output)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--font',help='CJK TrueType font path')
    p.add_argument('--language',choices=['zh','en','both'],default='both')
    args=p.parse_args();latin=fonts(args.font)
    for lang in (['zh','en'] if args.language=='both' else [args.language]):build(lang,latin)

if __name__=='__main__':main()
