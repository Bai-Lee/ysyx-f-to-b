from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
    rt=ROOT/'E/runtime';p=ROOT/'E/E5';sources=[p/'rtl'/n for n in ['minirv_decode.sv','minirv_regfile.sv','minirv_single.sv','npc_sim.sv']];obj=WORK/'lib/ref.o';rows=[]
    m=WORK/'memory_api'
    run('E5/memory_api/compile',['g++','-std=c++17','-O2','-I'+str(rt),p/'memory_api.cpp','-o',m],inputs=[p/'memory_api.cpp',rt/'memory.hpp'])
    o,e,r=run('E5/memory_api/run',[m],inputs=[m]);assert 'PASS all16' in o
    cases=[('sign','FAULT_SIGN_EXT','negative_immediates',0),('zero','FAULT_X0','x0_overflow',0),('jalr','FAULT_JALR_LOW_BIT','jalr_alias_odd',30),('load','FAULT_LBU_SIGN','memory_endian',0),('mask','FAULT_SB_MASK','memory_endian',0),('ebreak','FAULT_BREAK_REPEAT','six_ebreak',30)]
    for name,macro,program,expect in cases:
        exe=build('E5/fault_'+name,'npc_sim',sources,[rt/'runner.cpp'],extra=[obj],flags=['--timescale','1ns/1ns','+define+'+macro,'-CFLAGS','-O3'],additional_inputs=[rt/'memory.hpp',rt/'ref.h'])
        image=p/'programs'/(program+'.bin');out=ROOT/'artifacts/E5'/('fault_'+name)/'result.json'
        o,e,r=run('E5/fault_'+name+'/run',[exe,'--image',image,'--expect',str(expect),'--report',out,'--max-cycles','100000'],inputs=[exe,image],expected=(1,3),outputs=[out]);assert any(x in e for x in ['DIFF','NPC_FAULT','MEMORY_ERROR','POST_HALT_SIDE_EFFECT']),e
        rows.append({'fault':macro,'result':json.loads(out.read_text()),'stderr':e[-1800:]})
    dump(ROOT/'reports/E5_mutations.json',{'status':'PASS','faults':rows,'memory_bus_masks_checked':16});print('E5_MUTATIONS_PASS',len(rows),flush=True)
if __name__=='__main__':main()
