#!/usr/bin/env python3
"""Check citations, bilingual coverage, graph integrity, links, and PDF text."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json, re, xml.etree.ElementTree as ET
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'records/artifacts'

def main():
    checks=[];errors=[]
    def check(ok,message):
        checks.append(message)
        if not ok:errors.append(message)
    def data(name):return json.loads((ART/name).read_text())
    sources=data('sources.json');models=data('models.json');relations=data('model-relations.json');graph=data('relationship-graph.json');products=data('products.json')
    ids={s['id'] for s in sources}
    check(len(ids)==len(sources),'Unique source IDs')
    check(len({m['id'] for m in models})==len(models),'Unique model/method card IDs')
    for s in sources:
        check(urlsplit(s['url']).scheme in {'http','https'},f'Source URL {s["id"]}')
        check(s['accessed']=='2026-09-11',f'Evidence access date {s["id"]}')
        if s.get('date') and re.fullmatch(r'\d{4}-\d{2}-\d{2}',str(s['date'])):check(s['date']<='2026-09-11',f'No future release {s["id"]}')
    fields=['inputs','architecture','action_representation','training','data','inference','contribution','limitations','openness','source_ids']
    for m in models:
        check(all(m.get(k) for k in fields),f'Complete decomposition {m["id"]}')
        check(set(m['source_ids'])<=ids,f'Card evidence {m["id"]}')
    for e in relations:
        check(e['evidence_type'] in {'explicit','analytical'},f'Relationship evidence type {e["id"]}')
        check(set(e['source_ids'])<=ids and bool(e['source_ids']),f'Relationship sources {e["id"]}')
    nodes={n['id'] for n in graph['nodes']}
    check(len(nodes)==len(graph['nodes']),'Unique graph node IDs')
    check(all(e['source_node'] in nodes and e['target_node'] in nodes for e in graph['edges']),'Every graph endpoint resolves')
    check(all(e['source_node']!=e['target_node'] for e in graph['edges']),'No graph self-loops from grouped cards')
    for p in products:check(bool(p.get('limitations')) and set(p['source_ids'])<=ids,'Product evidence '+p['organization'])
    report_refs=[];heading_counts=[];pdf_info={}
    for suffix in ('','-en'):
        text=(ART/f'survey-report{suffix}.md').read_text()
        definitions=re.findall(r'^\[\^(\d+)\]:',text,re.M)
        body=re.sub(r'^\[\^\d+\]:.*$','',text,flags=re.M)
        refs=re.findall(r'\[\^(\d+)\]',body);report_refs.append(refs)
        check(set(refs)<=set(definitions),f'All report citations resolve {suffix or "zh"}')
        check(len(definitions)==len(set(definitions))==len(sources),f'One definition per source {suffix or "zh"}')
        check(not re.search(r'\[[VWHR]\d{3}\]',text),f'No unresolved module citations {suffix or "zh"}')
        check(not re.search(r'\bNone\b|TODO|TBD|turn\d+(?:search|view)',text),f'No unresolved publication placeholders {suffix or "zh"}')
        headings=re.findall(r'^## ',text,re.M);heading_counts.append(len(headings))
        pdf=ROOT/'reports'/f'embodied-intelligence-model-survey{suffix}.pdf'
        reader=PdfReader(pdf);texts=[p.extract_text() or '' for p in reader.pages]
        check(len(texts)>10,f'Full-length PDF {suffix or "zh"}')
        check(all(len(t.strip())>40 for t in texts),f'No empty PDF pages {suffix or "zh"}')
        check(all('\ufffd' not in t for t in texts),f'No text replacement glyphs {suffix or "zh"}')
        for term in ['OpenVLA','Cosmos','SONIC','MolmoAct2','Xiaomi']:
            check(term in '\n'.join(texts),f'PDF contains {term} {suffix or "zh"}')
        pdf_info[suffix or 'zh']={'pages':len(texts),'bytes':pdf.stat().st_size,'citation_occurrences':len(refs),'headings':len(headings)}
    check(report_refs[0]==report_refs[1],'Identical bilingual citation sequence')
    check(heading_counts[0]==heading_counts[1],'Corresponding bilingual major sections')
    for p in ROOT.rglob('*.md'):
        text=p.read_text()
        for match in re.finditer(r'!?\[[^\]\n]+\]\(([^\s)]+)\)',text):
            target=match[1]
            if target.startswith(('http:','https:','mailto:','#')):continue
            clean=unquote(target.split('#')[0])
            check((p.parent/clean).exists(),f'Local link {p.relative_to(ROOT)} -> {clean}')
    for p in (ROOT/'figures').glob('*.svg'):
        ET.parse(p);check(True,'Valid SVG '+p.name)
    result={'status':'passed' if not errors else 'failed','evidence_cutoff':'2026-09-11','checks':len(checks),'sources':len(sources),'model_method_cards':len(models),'relationships':len(relations),'products':len(products),'pdfs':pdf_info,'errors':errors,'scope':'Artifact integrity and citation consistency; not experimental reproduction or proof of all source claims.'}
    out=ROOT/'records/runs/validation.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if errors:raise SystemExit(1)
if __name__=='__main__':main()
