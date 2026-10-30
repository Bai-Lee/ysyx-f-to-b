"""Create the C5 implementation copies from accepted C4 and pinned SoC inputs."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *


def main():
    target=ROOT/'C/C5'; source=WORK/'soc-generation/ysyxSoC'; rows=[]
    for folder in ['rtl','sim','programs','results']:(target/folder).mkdir(exist_ok=True)
    for p in sorted((source/'perip').rglob('*')):
        if p.is_file() and '.git' not in p.parts:
            copy=target/'perip'/p.relative_to(source/'perip')
            copy.parent.mkdir(parents=True,exist_ok=True)
            if not copy.exists():shutil.copyfile(p,copy)
            if not (ROOT/'reports/C5_integration_setup.json').exists():assert sha(copy)==sha(p),copy
            rows.append({'source':str(p),'destination':str(copy),'source_sha256':sha(p)})
    for old,new in [('rv32e_execute','ysyx_00000000_execute'),('c4_simple_core','ysyx_00000000_core')]:
        original=ROOT/'C/C4/rtl'/(old+'.sv');dest=target/'rtl'/(new+'.sv')
        if not dest.exists():
            text=original.read_text().replace('rv32e_execute','ysyx_00000000_execute').replace('c4_simple_core','ysyx_00000000_core')
            if old=='c4_simple_core':
                text=text.replace('output logic d_req_valid,','output wire [2:0] d_req_size,output logic d_req_valid,')
                text=text.replace('  assign debug_state=state;','  assign debug_state=state;\n  assign d_req_size=logical_size==1?3\'d0:logical_size==2?3\'d1:3\'d2;')
                text=text.replace("d_req_addr={logical_addr[31:2],2'b00}", 'd_req_addr=logical_addr')
            dest.write_text(text)
        rows.append({'source':str(original),'destination':str(dest),'source_sha256':sha(original)})
    generated=target/'generation/ysyxSoCFull.v'
    lock=json.loads((ROOT/'reports/C5_generation.json').read_text())
    assert sha(generated)==lock['generated']['sha256']
    dump(ROOT/'reports/C5_integration_setup.json',{'status':'PREPARED_NOT_INTEGRATION_PASS','inputs':rows,
         'generated_soc':str(generated),'generated_sha256':sha(generated),
         'scope':'Independent C5-prefixed CPU copies retain logical byte address and AXI size; C4 and pristine SoC generation inputs untouched. Peripheral stubs remain unimplemented until their own tasks.'})
    print('C5_INTEGRATION_INPUTS_PREPARED',len(rows),flush=True)


if __name__=='__main__':main()
