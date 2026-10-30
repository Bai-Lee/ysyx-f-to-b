from pathlib import Path
import sys,json,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'runtime'))
from common import *
RTL=ROOT/'C/C4/rtl';TEST=ROOT/'C/C4/rtl_tests'
IVERILOG=Path('/home/USER/tools/e-stage/oss-20261022/oss-cad-suite/bin/iverilog')
VVP=IVERILOG.parent/'vvp';OUT=WORK/'c4-rtl-unit';OUT.mkdir(exist_ok=True)

def compile_run(name,top,sources,params=(),expected=0,marker=None):
    image=OUT/(name+'.vvp')
    run('C4/rtl_unit/'+name+'/compile',[IVERILOG,'-g2012','-s',top,*params,'-o',image,*sources],inputs=sources,outputs=[image],timeout=30)
    o,e,r=run('C4/rtl_unit/'+name+'/run',[VVP,image],inputs=[image],expected=(expected,),timeout=30)
    if marker:assert marker in o+e,(name,o,e)
    return {'name':name,'expected_exit':expected,'run':r,'stdout':o}

def main():
    sources=sorted(RTL.glob('*.sv'));image=OUT/'all-modules.vvp'
    run('C4/rtl_unit/syntax',[IVERILOG,'-g2012','-s','c4_axi_soc','-o',image,*sources],inputs=sources,outputs=[image],timeout=30)
    rows=[];device=[RTL/'axil_reg_frontend.sv',RTL/'axil_uart.sv',RTL/'axil_clint.sv',TEST/'uart_clint_tb.sv']
    rows.append(compile_run('devices','uart_clint_tb',device,marker='UART_CLINT_PASS'))
    rows.append(compile_run('uart-repeat-mutant','uart_clint_tb',device,['-Puart_clint_tb.BAD_UART=1'],1,'TX_DUPLICATE_OR_LOST'))
    rows.append(compile_run('clint-tear-mutant','uart_clint_tb',device,['-Puart_clint_tb.BAD_CLINT=1'],1,'CLINT_TORN_READ'))
    dump(ROOT/'reports/C4_rtl_units.json',{'status':'PASS_DEVICE_UNITS','rows':rows,'rtl_fingerprints':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in sources]})
    print('C4_DEVICE_UNITS_PASS',flush=True)

if __name__=='__main__':main()
