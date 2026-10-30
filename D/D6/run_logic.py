from pathlib import Path
import sys,re,itertools,collections
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
D=ROOT/'D/D6'; OUT=D/'results';OUT.mkdir(exist_ok=True)
SUITE=Path('/home/USER/tools/e-stage/oss-20260821/oss-cad-suite')
IV=Path('/home/USER/tools/e-stage/oss-20261022/oss-cad-suite/bin')
ENV={'PATH':str(SUITE/'bin')+':'+os.environ['PATH']}

def simulation(name,srcs,expected=(0,)):
    exe=WORK/'build'/('d6-'+name);exe.parent.mkdir(exist_ok=True)
    run('D6/logic/'+name+'/compile',[IV/'iverilog','-g2012','-s','tb','-o',exe,*srcs],inputs=srcs,outputs=[exe])
    return run('D6/logic/'+name+'/run',[IV/'vvp',exe],inputs=[exe],expected=expected)

def main():
    o,_,_=simulation('events',[D/'events.v']);assert 'EVENT_PASS' in o and 'MONITOR display_a=1' in o
    # Enumerate statement interleavings preserving each process's own ordering.
    def interleave(a,b):
        if not a:return [b]
        if not b:return [a]
        return [[a[0]]+x for x in interleave(a[1:],b)]+[[b[0]]+x for x in interleave(a,b[1:])]
    mixed=[]
    for seq in interleave(['a=0','a=1'],['b=a']):
        state={'a':0,'b':0}
        for s in seq:state[s[0]]=state['a'] if s=='b=a' else int(s[-1])
        mixed.append({'order':seq,'result':state})
    assert {x['result']['b'] for x in mixed}=={0,1}
    dump(OUT/'event_model.json',{'scope':'Independent finite interleaving model, initialized a=0. Actual simulator demonstrates one permitted schedule only.','interleavings':mixed,'blocking_swap_allowed':[[0,0],[1,1]],'nba_swap_required':[1,0]})
    # Copy the course's two-bit counter and example library directly, preserving originals.
    source=ARCHIVE/'docs/markdown/D/D6.md';text=source.read_text()
    blocks=re.findall(r'```(?:verilog|text)\n(.*?)```',text,re.S)
    counter=next(b for b in blocks if 'module counter' in b and 'input' in b)
    lib=next(b for b in blocks if 'library(demo)' in b)
    (D/'counter.v').write_text(counter);(D/'cell.lib').write_text(lib)
    stages=[('read','read_verilog '+str(D/'counter.v')+'; hierarchy -check -top counter'),('proc','proc'),('opt','opt'),('techmap','techmap; splitnets -ports; opt -full'),('dfflibmap','dfflibmap -liberty '+str(D/'cell.lib')+'; read_liberty -lib '+str(D/'cell.lib')),('abc','abc -liberty '+str(D/'cell.lib')+'; clean')]
    script='';outputs=[]
    for name,cmd in stages:
        prefix=OUT/name
        script+=cmd+'\nwrite_rtlil '+str(prefix)+'.il\nshow -format svg -prefix '+str(prefix)+' counter\n'
        if name!='read':script+='write_json '+str(prefix)+'.json\n'
        outputs.extend([Path(str(prefix)+'.il'),Path(str(prefix)+'.svg'),Path(str(prefix)+'.dot')])
    script+='rename counter counter_mapped\nwrite_verilog -noattr '+str(OUT/'mapped.v')+'\n'
    ys=D/'stages.ys';ys.write_text(script)
    run('D6/synthesis/stages',[SUITE/'bin/yosys','-s',ys],inputs=[ys,D/'counter.v',D/'cell.lib',source],outputs=outputs+[OUT/'mapped.v'],env=ENV)
    count={}
    for name,_ in stages[1:]:
        design=json.loads((OUT/(name+'.json')).read_text())['modules']['counter'];count[name]=dict(collections.Counter(c['type'] for c in design['cells'].values()))
    assert 'process ' in (OUT/'read.il').read_text() and 'process ' not in (OUT/'proc.il').read_text()
    assert count['abc']['DFF']==2 and all(not k.startswith('$') for k in count['abc'])
    cells=D/'cell_models.v';cells.write_text('''module BUF(input A,output Y);assign Y=A;endmodule
module NOT(input A,output Y);assign Y=~A;endmodule
module NAND(input A,B,output Y);assign Y=~(A&B);endmodule
module NOR(input A,B,output Y);assign Y=~(A|B);endmodule
module DFF(input C,D,output reg Q);always @(posedge C)Q<=D;endmodule
''')
    tb=D/'counter_tb.v';tb.write_text('''`timescale 1ns/1ps
module tb;
reg clk=0,rst=1,en=0;wire [1:0] refq,mapq;reg[1:0] expected;integer i;
counter original(clk,rst,en,refq);
counter_mapped mapped(.clk(clk),.rst(rst),.en(en),.\\count[0] (mapq[0]),.\\count[1] (mapq[1]));
initial begin
 expected=0;
 for(i=0;i<4096;i=i+1) begin
   clk=0;rst=(i%17==0);en=((i*13+3)%7<4);#1;
   if(rst)expected=0;else if(en)expected=expected+1;
   clk=1;#1;
   if(refq!==expected || mapq!==expected)$fatal(1,"COUNT_MISMATCH cycle=%d expected=%d ref=%d mapped=%d",i,expected,refq,mapq);
 end
 $display("COUNTER_PASS 4096 cycles");$finish;
end endmodule
''')
    o,_,_=simulation('mapped',[D/'counter.v',OUT/'mapped.v',cells,tb]);assert 'COUNTER_PASS' in o
    bad=OUT/'bad_cells.v';bad.write_text(cells.read_text().replace('Q<=D','Q<=~D'))
    o,_,_=simulation('mapped-mutant',[D/'counter.v',OUT/'mapped.v',bad,tb],(1,));assert 'COUNT_MISMATCH' in o
    # Concrete Annex B mismatches: omitted sensitivity, misordered temporary,
    # synthesis conditional, ignored delay, casex, casez and x don't-care.
    examples=D/'mismatch.v';examples.write_text('''`timescale 1ns/1ps
module tb;
reg a=0,b=0;reg incomplete,temporary,ywrong;wire ycorrect=a&b;
always @(a) incomplete=a&b;
always @(a or b) begin ywrong=temporary; temporary=a&b;end
reg [1:0] select;reg cx,cz;wire delayed;assign #2 delayed=a;
always @* casex(select) 2'b1?:cx=1;default:cx=0;endcase
always @* casez(select) 2'b1?:cz=1;default:cz=0;endcase
initial begin
 a=1;#3;b=1;#1;
 if(incomplete!==0 || ycorrect!==1 || ywrong!==0)$fatal(1,"missing expected mismatch");
 select=2'bx0;#1;if(cx!==1 || cz!==0)$fatal(1,"casex/casez X distinction");
 select=2'bz0;#1;if(cz!==1)$fatal(1,"casez Z wildcard");
 a=0;#1;if(delayed!==1)$fatal(1,"delay expected");#2;if(delayed!==0)$fatal(1,"settled delay");
 $display("MISMATCH_PASS sensitivity temporary casex casez delay");$finish;
end endmodule
''')
    o,_,_=simulation('mismatch',[examples]);assert 'MISMATCH_PASS' in o
    # Keep generated C++ for a genuine Verilator front-end trace to RTL.
    light=D/'light.v';light.write_text((WORK.parent/'e-stage/backend/light/rtl/light.v').read_text())
    vd=OUT/'verilator';vd.mkdir(exist_ok=True)
    run('D6/verilator/generated',[VERILATOR,'--cc','--top-module','light','--Mdir',vd,light],inputs=[light],outputs=[],env={'VERILATOR_ROOT':str(VROOT)})
    cpp=list(vd.glob('*.cpp'));assert cpp and any('trigger' in p.read_text().lower() for p in cpp)
    dump(ROOT/'reports/D6_logic.json',{'status':'PASS','source_sha256':sha(source),'stage_cells':count,'mapped_cycles':4096,'negative':'inverted DFF must fail first reset','mismatch_examples_stdout':o,'event_model_evidence':'artifacts/D6/logic','generated_cpp':[{'path':str(p),'sha256':sha(p)} for p in cpp],'evidence':['artifacts/D6/logic','artifacts/D6/synthesis','artifacts/D6/verilator','D/D6/results']})

if __name__=='__main__':main()
