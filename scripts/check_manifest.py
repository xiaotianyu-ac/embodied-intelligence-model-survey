#!/usr/bin/env python3
"""Read-only integrity check for the delivered repository snapshot."""
from pathlib import Path
import hashlib, json

ROOT=Path(__file__).resolve().parents[1]
def main():
    m=json.loads((ROOT/'records/runs/delivery-manifest.json').read_text())
    errors=[]
    for row in m['files']:
        p=ROOT/row['path']
        if not p.is_file():errors.append(row['path']+': missing');continue
        b=p.read_bytes()
        if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256'] or hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()!=row['git_blob_sha1']:errors.append(row['path']+': content mismatch')
    expected={x['path'] for x in m['files']}|{m['self_excluded']}
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and not any(x in {'.git','__pycache__','.venv','tmp'} for x in p.relative_to(ROOT).parts) and p.name!='.DS_Store'}
    if expected!=actual:errors.append('File set mismatch: '+str(expected^actual))
    if errors:raise SystemExit('\n'.join(errors))
    print(f'PASS: {len(m["files"])} file hashes; {len(actual)} total files.')
if __name__=='__main__':main()
