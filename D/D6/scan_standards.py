"""Read-only PDF extraction; originals stay in the frozen course archive."""
from pathlib import Path
import hashlib,json,re
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[2]
ARCHIVE=ROOT.parents[1]/'YSYX_F_B_Archive'
def main():
    out=ROOT/'temp/D6_pdf';out.mkdir(parents=True,exist_ok=True);rows=[]
    paths=[('verilog2005',ARCHIVE/'assets/offline/staff.ustc.edu.cn/~songch/download/IEEE.1364-2005.pdf'),('synthesis2002',ARCHIVE/'assets/offline/0x04.net/~mwk/vstd/ieee-1364.1-2002.pdf')]
    for name,p in paths:
        reader=PdfReader(p);pages=[];matches=[]
        for i,page in enumerate(reader.pages):
            text=page.extract_text() or '';pages.append(text)
            if name=='verilog2005':keys=['11. Scheduling semantics','11.4.1 Determinism','11.4.2 Nondeterminism','11.6.4 Nonblocking assignment']
            else:keys=['5. Modeling','5.1','Annex B','Simulation mismatches','Combinational logic']
            hits=[k for k in keys if k.lower() in text.lower()]
            if hits:matches.append({'physical_page':i+1,'hits':hits,'preview':text[:150]})
        (out/(name+'.pages.json')).write_text(json.dumps(pages,ensure_ascii=False),encoding='utf8')
        row={'name':name,'source':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'pages':len(pages),'matches':matches};rows.append(row)
        print(json.dumps(row,ensure_ascii=False),flush=True)
    (out/'index.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
if __name__=='__main__':main()
