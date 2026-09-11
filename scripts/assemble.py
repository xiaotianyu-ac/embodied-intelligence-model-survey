#!/usr/bin/env python3
"""Rebuild the canonical bilingual survey and catalogs from checked research modules."""
import csv, json, re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
ROOT=Path(__file__).resolve().parents[1]
GROUPS=['vla','world','wholebody','synthesis']
ART=ROOT/'records/artifacts'

def read(group,name):return json.loads((ROOT/'records/research'/group/name).read_text())
def dump(path,value):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def plain(value):return '; '.join(map(str,value)) if isinstance(value,list) else str(value)
def slug(s):return re.sub(r'[^\w\- ]','',s.lower()).replace(' ','-')
def canonical(u):
 p=urlsplit(u);return urlunsplit((p.scheme.lower(),p.netloc.lower(),p.path.rstrip('/'),p.query,''))
def write_csv(path,rows,fields):
 with path.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fields,lineterminator='\n');w.writeheader()
  for row in rows:w.writerow({k:plain(row.get(k,'')) for k in fields})

def main():
 ART.mkdir(parents=True,exist_ok=True)
 sources=[];by_url={};aliases={}
 for group in GROUPS:
  for s in read(group,'sources.json'):
   u=canonical(s['url'])
   if u not in by_url:
    x=dict(s);x['id']=f'S{len(sources)+1:03d}';x['number']=len(sources)+1;x['aliases']=[];x['source_records']=[]
    sources.append(x);by_url[u]=x
   x=by_url[u];x['aliases'].append(s['id']);x['source_records'].append(dict(s,group=group));aliases[s['id']]=x['id']
 index={s['id']:s for s in sources}
 def ids(xs):return list(dict.fromkeys(aliases.get(x,x) for x in xs))
 def refs(xs):return ''.join(f"[^{index[x]['number']}]" for x in ids(xs))
 def convert(text):return re.sub(r'\[([VWHR]\d{3})\]',lambda m:refs([m[1]]),text)
 models=[];relations=[];products=read('wholebody','products.json')
 for group in GROUPS:
  for m in read(group,'models.json'):
   x=dict(m);x['research_group']=group;x['source_ids']=ids(x['source_ids']);models.append(x)
  for e in read(group,'relations.json'):
   x=dict(e);x['research_group']=group;x['source_ids']=ids(x['source_ids']);x['id']=f'E{len(relations)+1:03d}';relations.append(x)
 for p in products:p['source_ids']=ids(p['source_ids'])
 spec=read('synthesis','graph-node-aliases.json')
 node_map={m['id']:{'id':m['id'],'label':m['name'],'type':'catalog_card','family':m['family']} for m in models}
 for n in spec['nodes']:node_map[n['id']]=n
 node_alias={m['name']:m['id'] for m in models};node_alias.update(spec['aliases'])
 node_alias.update({k:k for k in node_map})
 for e in relations:
  original=dict(e);e['original_source']=e['source'];e['original_target']=e['target']
  for rule in spec['relation_endpoint_overrides']:
   if all(original.get(k)==v for k,v in rule['match'].items()):
    for endpoint in ('source','target'):
     if endpoint in rule:e[endpoint]=rule[endpoint]
    e['endpoint_note']=rule['reason']
  for endpoint in ('source','target'):
   assert e[endpoint] in node_alias,('Unresolved graph endpoint',e)
   e[endpoint]=node_alias[e[endpoint]]
  assert e['source']!=e['target'],('Ambiguous self-loop',e)
 dump(ART/'sources.json',sources);dump(ART/'source-aliases.json',aliases)
 dump(ART/'models.json',models);dump(ART/'model-relations.json',relations);dump(ART/'products.json',products)
 write_csv(ART/'model-matrix.csv',models,['id','name','year','family','inputs','architecture','action_representation','training','data','inference','contribution','limitations','openness','source_ids'])
 write_csv(ART/'model-relations.csv',relations,['id','source','target','relation_type','evidence_type','explanation','source_ids'])
 write_csv(ART/'product-matrix.csv',products,['organization','model_or_system','product_form','stage_as_of','evidence','limitations','source_ids'])
 dump(ART/'relationship-graph.json',{'legend':{'explicit':'A source explicitly documents the relationship; inspect relation_type, which need not mean weight inheritance.','analytical':'Comparison or proposed complementarity, not a claim of shared weights.'},'nodes':list(node_map.values()),'edges':[dict(e,source_node=e['source'],target_node=e['target']) for e in relations]})
 sections=['opening','vla','world','wholebody','supplement','closing']
 for lang,suffix in [('zh',''),('en','-en')]:
  chunks=[]
  for sec in sections:
   p=ROOT/'records/research'/('synthesis' if sec in ['opening','supplement','closing'] else sec)/(f'{sec}-{lang}.md' if sec in ['opening','supplement','closing'] else f'section-{lang}.md')
   chunks.append(convert(p.read_text()))
  text='\n\n'.join(chunks).strip()
  role_title='### 先确定模型在闭环中的位置' if lang=='zh' else '### Locate the model within the feedback loop'
  text=text.replace(role_title,role_title+'\n\n![Closed-loop model roles](../../figures/architecture.svg)\n')
  rel_title='## 模型关系的综合论述' if lang=='zh' else '## A synthesis of model relationships'
  text=text.replace(rel_title,rel_title+'\n\n![Training paths and framework reuse](../../figures/learning-paths.svg)\n\n![Model relationship map](../../figures/model-relations.svg)\n')
  headings=[]
  def number(m):
   label=f'{len(headings)+1}. {m[1]}';headings.append(label);return '## '+label
  text=re.sub(r'^## (.+)$',number,text,flags=re.M)
  nav=('**章节导航**' if lang=='zh' else '**Contents**')+'\n\n'+'\n'.join(f'- [{h}](#{slug(h)})' for h in headings)
  pos=text.find('\n');text=text[:pos]+ '\n\n'+nav+text[pos:]
  appendix='模型与方法卡索引' if lang=='zh' else 'Model and method card index'
  text+=f'\n\n## {len(headings)+1}. {appendix}\n\n'
  text+=('下表统计模型、版本、方法和组件卡，不等于独立基础模型数量。完整逐字段拆解见 [Model Atlas](model-atlas.md)。\n\n' if lang=='zh' else 'Entries include models, versions, methods, and components, not that many independent foundation models. Full field-by-field decompositions are in the [Model Atlas](model-atlas.md).\n\n')
  text+='| ID | Model / method | Year | Evidence |\n|---|---|---|---|\n'
  for m in models:text+=f"| {m['id']} | {m['name']} | {m['year']} | {refs(m['source_ids'])} |\n"
  text+=f"\n## {len(headings)+2}. "+('参考来源' if lang=='zh' else 'Sources')+'\n\n'
  text+=('以下按来源URL去重。日期为发布年份/日期或对应版本年份；动态页面按2026-09-11核验。别名、阅读范围和限制保存在sources.json。\n\n' if lang=='zh' else 'Sources are deduplicated by URL. Dates indicate publication or version dates; dynamic pages were checked on September 11, 2026. Source aliases, reading scope, and limitations are retained in sources.json.\n\n')
  for s in sources:text+=f"[^{s['number']}]: {s['authors_or_org']}. [{s['title']}]({s['url']}). {(s['date'] or 'n.d.; accessed 2026-09-11')}.\n\n"
  (ART/f'survey-report{suffix}.md').write_text(text)
 atlas='# Model Atlas / 模型与方法拆解\n\nThis structured atlas preserves each card\'s input, architecture, objective, data, execution, contribution, limitations, and available assets. Main analytical explanations are provided in both report editions. Entries include versions and methods.\n\n'
 fields=[('problem','Problem / 问题'),('family','Family / 分类'),('inputs','Inputs / 输入'),('architecture','Architecture / 架构'),('action_representation','Action representation / 动作表示'),('training','Training objective / 训练'),('data','Data / 数据'),('inference','Execution and feedback / 推理闭环'),('contribution','Contribution / 贡献'),('limitations','Limitations / 局限'),('openness','Available assets / 开放程度')]
 for m in models:
  atlas+=f"## {m['name']} ({m['year']})\n\nID: `{m['id']}`\n\n"
  for k,l in fields:
   if k in m:atlas+=f'**{l}:** {plain(m[k])}\n\n'
  atlas+='**Sources:** '+', '.join(f"[{s}]({index[s]['url']})" for s in m['source_ids'])+'\n\n'
 (ART/'model-atlas.md').write_text(atlas)
 rel='# Model relationships / 模型关系\n\nExplicit means the relationship is documented, not necessarily that weights are inherited. Analytical means a comparison or complementary design inference. Read each edge type and explanation. Component/version reference nodes supplement grouped catalog cards. GEN-1/1.5 and several named subcomponents are discussed in the reports and represented as context nodes, without separate full catalog cards.\n\n![Training paths](../../figures/learning-paths.svg)\n\n![Relationship map](../../figures/model-relations.svg)\n\n| From | To | Type | Evidence | Explanation | Sources |\n|---|---|---|---|---|---|\n'
 for e in relations:rel+='| '+' | '.join([node_map[e['source']]['label'],node_map[e['target']]['label'],e['relation_type'],e['evidence_type'],e['explanation'],', '.join(f"[{s}]({index[s]['url']})" for s in e['source_ids'])])+' |\n'
 (ART/'model-relations.md').write_text(rel)
 bib=[]
 for s in sources:
  clean=lambda x:str(x).replace('{','').replace('}','').replace('&',r'\&')
  bib.append('@misc{'+s['id']+',\n  title={'+clean(s['title'])+'},\n  author={{'+clean(s['authors_or_org'])+'}},\n  year={'+(re.search(r'\b(19|20)\d{2}\b',str(s['date']))[0] if s['date'] and re.match(r'^\d{4}',str(s['date'])) else 'n.d.')+'},\n  howpublished={\\url{'+s['url']+'}},\n  note={Accessed 2026-09-11}\n}')
 (ART/'references.bib').write_text('\n\n'.join(bib)+'\n')
 # Export the exact data/benchmark tables used by the reports, not a second hand-maintained inventory.
 zh=(ART/'survey-report.md').read_text()
 for start,name in [('数据或接口','data-matrix.csv'),('基准','benchmark-matrix.csv')]:
  lines=zh.splitlines();i=next(j for j,l in enumerate(lines) if l.startswith('| '+start+' |'));rows=[]
  while i<len(lines) and lines[i].startswith('|'):
   cells=[c.strip() for c in lines[i].strip('|').split('|')]
   if not all(re.fullmatch('[-: ]+',c) for c in cells):rows.append(cells)
   i+=1
  with (ART/name).open('w',newline='') as f:csv.writer(f,lineterminator='\n').writerows([[re.sub(r'\[\^(\d+)\]',lambda m: f'S{int(m[1]):03d}',c) for c in row] for row in rows])
 print(json.dumps({'sources':len(sources),'source_records':sum(len(s['aliases']) for s in sources),'model_method_cards':len(models),'relationships':len(relations),'products':len(products)},indent=2))

if __name__=='__main__':main()
