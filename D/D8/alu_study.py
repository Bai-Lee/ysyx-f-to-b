from pathlib import Path
import sys,collections
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    d=ROOT/'D/D8';out=d/'results/alu';out.mkdir(parents=True,exist_ok=True);suite=Path('/home/USER/tools/e-stage/oss-20260821/oss-cad-suite');yosys=suite/'bin/yosys';source=d/'alu_study.v';env={'PATH':str(suite/'bin')+':'+os.environ['PATH']};rows=[]
    for top in ['alu_naive','alu_shared']:
        coarse=out/(top+'-coarse.json');gates=out/(top+'-gates.json');ys=out/(top+'.ys')
        ys.write_text('read_verilog '+str(source)+'\nhierarchy -top '+top+'\nproc; opt\nwrite_json '+str(coarse)+'\nshow -format svg -prefix '+str(out/top)+' '+top+'\ntechmap; opt; abc -g simple; clean\nwrite_json '+str(gates)+'\n')
        run('D8/alu/'+top,[yosys,'-s',ys],inputs=[source,ys],outputs=[coarse,gates,out/(top+'.svg')],env=env)
        counts=lambda p:dict(collections.Counter(c['type'] for c in json.loads(p.read_text())['modules'][top]['cells'].values()))
        rows.append({'design':top,'coarse_cells':counts(coarse),'mapped_generic_cells':counts(gates)})
    proof=out/'equivalence.ys';proof.write_text('read_verilog '+str(source)+'\nproc; opt\nmiter -equiv -flatten alu_naive alu_shared miter\nhierarchy -top miter\nopt_clean\nsat -verify -prove trigger 0 -show-inputs -show-outputs miter\n')
    o,e,_=run('D8/alu/proof',[yosys,'-s',proof],inputs=[source,proof],env=env);assert 'SUCCESS' in o
    mutant=out/'mutant.v';mutant.write_text(source.read_text().replace("2:y={3'b0,!sum[4]}","2:y={3'b0,sum[4]}"));badproof=out/'mutant.ys';badproof.write_text(proof.read_text().replace(str(source),str(mutant)))
    o,e,_=run('D8/alu/mutant',[yosys,'-s',badproof],inputs=[mutant,badproof],expected=(1,),env=env);assert 'proof did fail' in o+e
    diagram=d/'architecture.dot';diagram.write_text('''digraph rv32e {
graph [rankdir=LR,bgcolor="white",fontname="DejaVu Sans",label="D8 RV32E single-cycle CPU | architectural state changes on rising edge",labelloc=t];
node [shape=box,style="rounded,filled",fillcolor="#edf3fa",fontname="DejaVu Sans",fontsize=12];
edge [fontname="DejaVu Sans",fontsize=10];
pc [label="PC register\nreset 0x80000000",fillcolor="#dbe8ff"];
fetch [label="Instruction port\n4-byte fetch"];
decode [label="Decode + immediates\nI/S/B/U/J\nencoding + x16..31 checks"];
rf [label="16 x 32-bit GPR\n2 read / 1 write\nx0 always zero",fillcolor="#dbe8ff"];
alu [label="ALU + comparison\nadd/sub/logic/shift/SLT"];
dm [label="Data port\nLB/LH/LW, SB/SH/SW\nRAM or checked MMIO"];
wb [label="Writeback MUX\nALU / load / PC+4"];
pcmux [label="Next-PC MUX\nPC+4 / branch / JAL / JALR"];
ctrl [label="Commit / halt / fault\nEBREAK reads a0\nno further side effects",fillcolor="#ffe5d8"];
host [label="C++ environment\nsdb + trace + NEMU shared REF",fillcolor="#e5f3e7"];
pc -> fetch -> decode;
decode -> rf [label="rs1, rs2"];
rf -> alu [label="a, b"];
decode -> alu [label="immediate + control",color="#3567b1"];
alu -> dm [label="address"];
rf -> dm [label="store data"];
dm -> wb [label="extended load data"];
alu -> wb [label="ALU result"];
pc -> wb [label="PC+4",constraint=false];
pc -> alu [label="PC for AUIPC/targets",constraint=false];
pc -> pcmux [label="PC+4",constraint=false];
wb -> rf [label="rd, write value @edge",constraint=false];
alu -> pcmux [label="compare/target"];
decode -> pcmux [label="branch/jump control",color="#3567b1"];
pcmux -> pc [label="next PC @edge",constraint=false];
decode -> ctrl [label="valid, EBREAK, fault",style=dashed,color="#3567b1"];
ctrl -> host [label="DPI commit + halt"];
dm -> host [label="one access per commit",style=dashed];
rf -> host [label="debug observation",style=dashed,constraint=false];
}
''')
    svg=d/'architecture.svg';png=d/'architecture.png'
    run('D8/architecture/svg',[suite/'bin/dot','-Tsvg',diagram,'-o',svg],inputs=[diagram,d/'rv32e_core.sv'],outputs=[svg])
    run('D8/architecture/png',[suite/'bin/dot','-Tpng',diagram,'-o',png],inputs=[diagram],outputs=[png])
    dump(ROOT/'reports/D8_alu.json',{'status':'PASS_FOUR_BIT_EQUIVALENCE','designs':rows,'proof':'All 2048 combinations of 4-bit a, 4-bit b and 3-bit op, via combinational SAT equivalence; wrong carry interpretation rejected.','scope':'Generic gate counts, not standard-cell area or nanosecond timing. This study does not replace the 32-bit CPU ISA tests.','evidence':'artifacts/D8/alu'})

if __name__=='__main__':main()
