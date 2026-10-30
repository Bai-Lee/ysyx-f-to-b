from common import *
src=ROOT/'E/E4/csrc/case_unknown.sv';exe=OUT/'fourstate/case.vvp';exe.parent.mkdir(exist_ok=True)
run('fourstate/compile',['iverilog','-g2012','-Wall','-s','tb','-o',exe,src],inputs=[src])
o,e,r=run('fourstate/run',['vvp',exe],inputs=[exe]);assert 'PASS 4-state' in o
result(['NJU-02-03'],['artifacts/E4/fourstate'],'Actual Icarus four-state case/casez/casex observations; no reliance on two-state Verilator to claim X/Z behavior.')
