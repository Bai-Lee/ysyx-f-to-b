from pathlib import Path
import hashlib,json,difflib,re
ROOT=Path(__file__).resolve().parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    old=ROOT/'C/C4/models/nangate45/NangateOpenCellLibrary_typical.lib';new=ROOT/'B/models/nangate45/lib/Nangate45_typ.lib'
    a=old.read_bytes().splitlines(keepends=True);b=new.read_bytes().splitlines(keepends=True)
    changes=[x for x in difflib.SequenceMatcher(None,a,b).get_opcodes() if x[0]!='equal']
    assert len(changes)==1 and changes[0][0]=='delete',changes
    _,i,j,_,_=changes[0];removed=b''.join(a[i:j]);assert len(re.findall(rb'(?m)^\s*cell\s*\(',removed))==1 and b'cell (TAPCELL_X1)' in removed and re.search(rb'dont_use\s*:\s*true',removed)
    used=[]
    for p in sorted((ROOT/'B/B3/synthesis').glob('*/mapped.json')):
        modules=json.loads(p.read_text())['modules'];types={c['type'] for m in modules.values() for c in m.get('cells',{}).values()}
        assert 'TAPCELL_X1' not in types
        used.append({'mapped_json':str(p.relative_to(ROOT)),'sha256':sha(p),'cell_types':sorted(types)})
    report=ROOT/'reports/B_nangate_course_library.json';d=json.loads(report.read_text());d.update(status='PASS_ALL_USED_LIBRARY_CONTENT_IDENTICAL',only_difference='Prior OpenROAD file additionally contains one dont_use TAPCELL_X1 physical cell. No mapped design uses it. All other bytes, including timing tables, units, area, and conditions, are identical.',mapped_designs_checked=used)
    report.write_text(json.dumps(d,indent=2),encoding='utf8');print('B_COURSE_LIBRARY_CONTENT_MATCH',len(used))
if __name__=='__main__':main()
