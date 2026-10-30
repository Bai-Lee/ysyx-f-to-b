from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    scope=ROOT/'B/B5/address-checks';scope.mkdir(parents=True,exist_ok=True);suite=Path('/home/USER/tools/e-stage/oss-20260821/oss-cad-suite');yosys=suite/'bin/yosys';iv=suite/'bin/iverilog';vvp=suite/'bin/vvp';rows=[]
    for old in [True,False]:
        label='original' if old else 'explicit-mask';source=scope/(label+'.sv')
        expr="address&~32'(WORDS*4-1)" if old else "address&(32'hffffffff << (2+$clog2(WORDS)))"
        source.write_text("module address_control #(parameter integer WORDS=8)(input [31:0] address,input [3:0] beat,input cached,burst,output [31:0] y,output good); assign y=cached?(("+expr+")+(burst?32'b0:{26'b0,beat,2'b0})):address;wire [31:0] reference=cached?(((address>>(2+$clog2(WORDS)))<<(2+$clog2(WORDS)))+(burst?32'b0:{26'b0,beat,2'b0})):address;assign good=(y==reference);endmodule\n")
        tb=scope/(label+'-tb.sv');tb.write_text("module tb;reg [31:0] address=32'h30000000;wire [31:0] y;address_control dut(.address(address),.beat(4'b0),.cached(1'b1),.burst(1'b0),.y(y));initial begin #1;if(y!==32'h30000000)$fatal(1,\"RTL_ADDRESS_MISMATCH\");$display(\"RTL_ADDRESS_PASS %h\",y);$finish;end endmodule\n")
        exe=WORK/'b5'/('address-'+label+'.vvp');run('B5/address/'+label+'-compile',[iv,'-g2012','-s','tb','-o',exe,source,tb],inputs=[iv,source,tb],outputs=[exe])
        text,_,_=run('B5/address/'+label+'-rtl',[vvp,exe],inputs=[vvp,exe]);assert 'RTL_ADDRESS_PASS 30000000' in text
        script=scope/(label+'.ys');wave=ROOT/'artifacts/B5/address'/label/'counterexample.vcd';wave.parent.mkdir(parents=True,exist_ok=True)
        script.write_text('read_verilog -sv '+str(source)+'\nprep -top address_control\neval -set address 805306368 -set beat 0 -set cached 1 -set burst 0 -show y\nsat -prove good 1 -verify -show-inputs -show-outputs -dump_vcd '+str(wave)+'\n')
        text,err,record=run('B5/address/'+label,[yosys,'-s',script],inputs=[yosys,source,script],expected=(1 if old else 0,),outputs=[wave] if old else [])
        assert ('model found: FAIL!' in text) if old else ('no model found: SUCCESS!' in text)
        rows.append({'expression':label,'rtl':'PASS_EXPECTED_30000000','synthesis':'COUNTEREXAMPLE' if old else 'PASS_ALL_COMBINATIONAL_INPUTS','evidence':'artifacts/B5/address/'+label})
    dump(ROOT/'reports/B5_address_expression.json',{'status':'PASS_DISCREPANCY_ISOLATED_AND_FIXED','runs':rows,'scope':'The original unary-sized-cast expression is correct in the tested RTL simulator but is evaluated differently by the pinned Yosys frontend. Explicit32-bit shift mask agrees with an independent shift-based reference for all address/beat/cache/burst inputs at8words. No architectural behavior or checks were relaxed. Earlier cached netlists require regeneration and functional acceptance.'})
    report=ROOT/'reports/B_final_selection.json';d=json.loads(report.read_text());d['status']='INVALIDATED_PENDING_ADDRESS_FIX_REGRESSION';d['reason_for_invalidation']='B5 gate-level test and isolated address-expression counterexample; see reports/B5_address_expression.json';dump(report,d)
    print('B5_ADDRESS_EXPRESSION_FIXED')
if __name__=='__main__':main()
