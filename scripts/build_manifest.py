#!/usr/bin/env python3
"""Freeze a complete file index and content hashes after report validation."""
from pathlib import Path
import hashlib, json

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'records/runs/delivery-manifest.json'

def files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file() and not any(x in {'.git','__pycache__','.venv','tmp'} for x in p.relative_to(ROOT).parts) and p.name!='.DS_Store')

def main():
    index=ROOT/'CONTENTS.md'
    paths=sorted({p.relative_to(ROOT).as_posix() for p in files()}|{'CONTENTS.md','records/runs/delivery-manifest.json'})
    text='# Complete file index / 完整资料目录\n\n'+f'This snapshot contains **{len(paths)} files**. Both reports, PDFs, model and relationship catalogs, source modules, evidence records, diagrams, and build scripts are included. The integrity manifest excludes itself from hashing.\n\n'
    text+='\n'.join(f'- [{p}]({p})' for p in paths)+'\n'
    index.write_text(text)
    records=[]
    for p in files():
        if p==MANIFEST:continue
        b=p.read_bytes()
        records.append({'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob_sha1':hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()})
    value={'evidence_cutoff':'2026-09-11','total_files':len(records)+1,'self_excluded':'records/runs/delivery-manifest.json','files':records}
    MANIFEST.parent.mkdir(parents=True,exist_ok=True)
    MANIFEST.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    print(f'Manifest: {len(records)} hashed files; {len(records)+1} total.')

if __name__=='__main__':main()
