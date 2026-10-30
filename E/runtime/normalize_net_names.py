"""Bijective lexical identifier normalization for the old ECC netlist reader.

Only escaped identifiers that cannot be plain identifiers are renamed. Comments,
strings, cell types and top ports using normal names remain unchanged. No gate,
pin connection, constraint or signoff criterion is removed.
"""
from pathlib import Path
import re,sys,gzip,json,hashlib
def main():
    p=Path(sys.argv[1]).resolve();root=Path('/home/USER/e-stage/backend').resolve();assert p.is_relative_to(root)
    original=gzip.decompress(p.read_bytes()).decode()
    regex=re.compile(r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\\[^\s]+|[A-Za-z_$][A-Za-z0-9_$]*',re.S)
    tokens=list(regex.finditer(original));existing={m[0] for m in tokens};mapping={}
    for m in tokens:
        t=m[0]
        if t.startswith('\\') and not re.fullmatch(r'[A-Za-z_$][A-Za-z0-9_$]*',t[1:]):
            name='e_net_'+hashlib.sha256(t.encode()).hexdigest()[:20]
            assert name not in existing;mapping[t]=name
    if not mapping:return
    assert len(set(mapping.values()))==len(mapping)
    changed=regex.sub(lambda m:mapping.get(m[0],m[0]),original)
    inverse={v:k for k,v in mapping.items()}
    assert regex.sub(lambda m:inverse.get(m[0],m[0]),changed)==original
    backup=p.parent.parent/'data'/('before_namefix_'+p.name);backup.write_bytes(p.read_bytes())
    with gzip.GzipFile(filename=str(p),mode='wb',mtime=0) as f:f.write(changed.encode())
    report={'status':'PASS_LEXICAL_BIJECTION','source':str(backup),'target':str(p),'original_sha256':hashlib.sha256(original.encode()).hexdigest(),'normalized_sha256':hashlib.sha256(changed.encode()).hexdigest(),'identifiers':mapping,'scope':'Escaped internal identifier spelling only; inverse transformation restores every original text byte.'}
    (p.parent.parent/'data/namefix.json').write_text(json.dumps(report,indent=2));print('IDENTIFIER_NORMALIZATION',len(mapping),flush=True)
if __name__=='__main__':main()
