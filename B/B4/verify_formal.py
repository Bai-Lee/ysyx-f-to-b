from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    suite=Path('/home/USER/tools/e-stage/oss-20260821/oss-cad-suite');yosys=suite/'bin/yosys';harness=ROOT/'B/B4/formal/pipeline_miter.sv'
    sources=[ROOT/'B/soc/rtl/ysyx_00000000_pipe.sv',ROOT/'B/soc/rtl/ysyx_00000000_alu.sv',ROOT/'B/soc/rtl/ysyx_00000000_execute.sv',harness];rows=[]
    for label,forward,fault in [('interlock',0,0),('forward',1,0),('bad-raw',0,1)]:
        folder=ROOT/'artifacts/B4/formal'/label;folder.mkdir(parents=True,exist_ok=True);script=folder/'proof.ys';wave=folder/'counterexample.vcd';budget=folder/'budget.json'
        script.write_text('read_verilog -formal -sv -DSYNTHESIS '+' '.join(map(str,sources))+f'\nchparam -set FORWARD {forward} -set FAULT_RAW {fault} pipeline_miter\nprep -top pipeline_miter -flatten\nmemory_map\nopt\nasync2sync\ndffunmap\nopt_clean\nchformal -lower\nsat -seq 26 -set-assumes -prove-asserts -verify -show program_words -show cycle -show retirements -show fault -show gold_pc -show saved_gpr -show gold_gpr -show cpc -show ci -show cv -show halted -dump_vcd '+str(wave)+'\n')
        text,err,_=run('B4/formal/'+label+'/run',['python3',ROOT/'B/runtime/budget_exec.py','--rss-mib','3072','--report',budget,'--',yosys,'-s',script],inputs=[yosys,script,*sources],outputs=[budget,*([wave] if fault else [])],expected=(1 if fault else 0,),timeout=600)
        if fault:assert 'model found: FAIL!' in text and wave.is_file()
        else:assert 'no model found: SUCCESS!' in text
        rows.append({'name':label,'status':'PASS_COUNTEREXAMPLE_FOUND' if fault else 'PASS_BOUNDED_PROOF','forward':forward,'fault_raw':fault,'evidence':'artifacts/B4/formal/'+label,'counterexample_sha256':sha(wave) if fault else None})
    dump(ROOT/'reports/B4_formal.json',{'status':'PASS','runs':rows,'bound':26,'scope':'Three arbitrary legal RV32E ADDI/ADD/SUB/LUI instructions and EBREAK, all source/destination choices and immediate/data bits, one-cycle pipelined ROM, reset on the first abstract rising edge. GPR/PC/instruction-order equivalence to the previously validated sequential core and bounded completion are asserted. No loads/stores, branch programs, CSR exceptions, asynchronous events or full-ISA/unbounded proof is claimed.'});print('B4_BOUNDED_FORMAL_PASS')
if __name__=='__main__':main()
