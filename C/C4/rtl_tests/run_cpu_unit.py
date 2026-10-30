from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'runtime'))
from common import *
def main():
    d=ROOT/'C/C4';out=WORK/'c4-rtl-unit';out.mkdir(exist_ok=True);results=d/'results';results.mkdir(exist_ok=True)
    tool=Path('/home/USER/tools/e-stage/oss-20261022/oss-cad-suite/bin/iverilog');vvp=tool.parent/'vvp';rows=[]
    sources=[d/'rtl/rv32e_execute.sv',d/'rtl/c4_simple_core.sv',d/'rtl_tests/simple_cpu_tb.sv']
    for stage,bad in [(1,0),(2,0),(2,1)]:
        name=f'stage{stage}'+('-mutant' if bad else '');image=out/(name+'.vvp');wave=results/(name+'.vcd')
        run('C4/rtl_unit/cpu/'+name+'/compile',[tool,'-g2012','-s','simple_cpu_tb','-Psimple_cpu_tb.STAGE='+str(stage),'-Psimple_cpu_tb.BAD='+str(bad),'-o',image,*sources],inputs=sources,outputs=[image])
        o,e,r=run('C4/rtl_unit/cpu/'+name+'/run',[vvp,image,'+vcd='+str(wave)],inputs=[image],outputs=[wave],expected=(1,) if bad else (0,),timeout=30)
        assert 'REGISTER_MISMATCH' in o if bad else f'SIMPLE_CPU_PASS stage={stage} cycles={12 if stage==1 else 14}' in o
        rows.append({'stage':stage,'mutant':bool(bad),'status':'PASS_REJECTED' if bad else 'PASS','stdout':o,'wave':str(wave.relative_to(ROOT)),'wave_sha256':sha(wave)})
    dump(ROOT/'reports/C4_cpu_cycles.json',{'status':'PASS_FOUR_STATE_AND_CYCLE_CONTRACT','rows':rows,'scope':'Independent ROM/constants, exact per-instruction 2-cycle stage1 and 2/3-cycle stage2, stable architectural state during waits, real wrong-ADDI RTL rejected. Zero-delay functional VCD, not SDF or silicon timing.'})
if __name__=='__main__':main()
