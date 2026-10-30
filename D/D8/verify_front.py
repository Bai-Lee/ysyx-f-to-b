from pathlib import Path
import sys,struct,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    d=ROOT/'D/D8';out=d/'results';out.mkdir(exist_ok=True)
    config=json.loads((ROOT/'reports/D8_build.json').read_text());exe=Path(config['executable']);ref=Path(config['reference']);npc=BENCH/'npc';am=BENCH/'abstract-machine'
    env={'NEMU_HOME':str(BENCH/'nemu'),'YSYX_HOME':str(BENCH)}
    source=ROOT/'D/D7/trace_test.S';ld=ROOT/'D/D7/baremetal.ld';elf=out/'trace-rv32e.elf';binary=out/'trace-rv32e.bin'
    run('D8/front/compile',['riscv64-linux-gnu-gcc','-march=rv32e','-mabi=ilp32e','-nostdlib','-nostartfiles','-static','-Wl,--build-id=none','-T',ld,source,'-o',elf],inputs=[source,ld],outputs=[elf])
    run('D8/front/objcopy',['riscv64-linux-gnu-objcopy','-O','binary',elf,binary],inputs=[elf],outputs=[binary])
    o,_,_=run('D8/front/attributes',['riscv64-linux-gnu-readelf','-A',elf],inputs=[elf]);assert 'rv32e' in o and '_m2p' not in o
    trace=out/'normal.trace';report=out/'normal.json'
    args=[exe,'--image',binary,'--ref',ref,'--elf',elf,'--report',report]
    _,_,_=run('D8/front/trace',[*args,'--trace',trace,'--trace-modes','imf'],inputs=[exe,ref,elf,binary],outputs=[trace,report])
    result=json.loads(report.read_text());assert result['result']=='GOOD_TRAP' and result['ebreak_calls']==1 and result['instructions']==result['diff_checked'] and result['device_sync_checked']==0
    assert result['gpr'][0]==0 and result['gpr'][7]==43
    lines=trace.read_text().splitlines();assert sum(l.startswith('I ') for l in lines)==result['instructions']
    assert sum(l.startswith('M ') for l in lines)==4 and any('call outer@' in l for l in lines) and any('tail outer -> tail@' in l for l in lines)
    limited=out/'limited.trace'
    run('D8/front/trace-limit',[*args,'--trace',limited,'--trace-modes','imf','--trace-limit','3'],inputs=[exe,ref,elf,binary],outputs=[limited])
    assert len(limited.read_text().splitlines())==4 and limited.read_text().endswith('TRACE_LIMIT limit=3\n')
    scripts={
      'steps':'si\ninfo r\np $sp\nx 2 0x80000000\nsi 1\np $t0\nq\n',
      'watch':'w $t0\nw *0x80020000\nc\ninfo r\nc\nc\ninfo w\nd 0\nd 1\nc\nq\n',
      'bad':'si 0\nsi -1\nsi 1000001\np 1/0\np $x16\nx 1 0\nx 257 0x80000000\nw *0\nd 31\ninfo z\nblah\nsi\nq\n'
    }
    sdb=[]
    for name,text in scripts.items():
        commands=out/(name+'.commands');commands.write_text(text);r=out/(name+'.json')
        o,e,_=run('D8/sdb/'+name,[exe,'--interactive','--image',binary,'--ref',ref,'--report',r],inputs=[exe,ref,binary,commands],outputs=[r],stdin_file=commands)
        sdb.append({'name':name,'result':json.loads(r.read_text())})
        if name=='steps':assert 'PC 0x80000004' in o and 'EXPR_VALUE 2147549184' in o and 'EXPR_VALUE 5 ' in o
        if name=='watch':assert o.count('WATCH_HIT')==3 and 'PC 0x80000008' in o and 'WATCH_DELETED 0' in o and 'WATCH_DELETED 1' in o and json.loads(r.read_text())['result']=='GOOD_TRAP'
        if name=='bad':assert o.count('COMMAND_ERROR')>=6 and o.count('EXPR_ERROR')>=2 and 'MEMORY_ERROR outside RAM' in o
    cases=[('reserved',[0xffffffff],1),('x16_destination',[0x00100813],2),('x16_source',[0x00080513],2),('multiply',[0x02b50533],1),('misaligned_jump',[0x0020006f],3),('unaligned_half',[0x800002b7,0x00129303],4),('unaligned_word',[0x800002b7,0x0022a303],4)]
    rejects=[]
    for name,words,fault in cases:
        path=out/(name+'.bin');path.write_bytes(struct.pack('<'+'I'*len(words),*words));r=out/(name+'.json')
        o,e,_=run('D8/front/reject-'+name,[exe,'--image',path,'--ref',ref,'--report',r],inputs=[exe,ref,path],outputs=[r],expected=(3,));assert 'NPC_FAULT' in e and f'code={fault}' in e
        rejects.append({'name':name,'fault_code':fault,'result':json.loads(r.read_text())})
    # Build the actual RTL addi mutant through a separate Verilator build tree.
    mutantdir=WORK/'build/npc-addi-mutant';badexe=mutantdir/'sim'
    run('D8/diff/mutant-build',['make','-j1','BUILD='+str(mutantdir),'FAULT_ADDI=1'],cwd=npc,inputs=[npc/'Makefile',npc/'vsrc/rv32e_core.sv',npc/'vsrc/npc_sim.sv',npc/'csrc/runner.cpp'],outputs=[badexe],timeout=300)
    r=out/'mutant.json';o,e,_=run('D8/diff/mutant',[badexe,'--image',binary,'--ref',ref,'--report',r],inputs=[badexe,ref,binary],outputs=[r],expected=(1,))
    mutant=json.loads(r.read_text());assert mutant['result']=='DIFF_FAIL' and mutant['instructions']==2 and 'pc=80000004' in e and 'DIFF_MISMATCH' in e
    # AM run must use the just-compiled RV32E ELF and propagate failures.
    cwd=BENCH/'am-kernels/tests/cpu-tests';amruns=[]
    for name,rc in [('dummy',0),('wrong',2)]:
        r=cwd/'build'/(name+'-riscv32e-npc.bin.npc.json');elf=cwd/'build'/(name+'-riscv32e-npc.elf')
        o,e,record=run('D8/am/'+name,['make','-j1','ARCH=riscv32e-npc','ALL='+name,'run'],cwd=cwd,env=env,inputs=[cwd/'tests'/(name+'.c'),cwd/'Makefile',am/'scripts/riscv32e-npc.mk',am/'scripts/platform/npc.mk',am/'am/src/riscv/npc/trm.c',exe,ref],outputs=[r,elf],expected=(rc,),timeout=180)
        status=json.loads(r.read_text());assert status['result']==('GOOD_TRAP' if rc==0 else 'BAD_TRAP') and status['ebreak_calls']==1
        amruns.append({'name':name,'make_exit':record['exit_code'],'simulation':status})
        o,_,_=run('D8/am/'+name+'-attributes',['riscv64-linux-gnu-readelf','-A',elf],inputs=[elf]);assert 'rv32e' in o and '_m2p' not in o
    dump(ROOT/'reports/D8_front.json',{'status':'PASS_BOUNDED_CHECKS','normal':result,'sdb':sdb,'negative_encodings':rejects,'rtl_addi_mutant':mutant,'am':amruns,'scope':'Full RV32E base operations implemented; finite boundary/front tests only. No M, C, privilege or silicon timing claim.'})

if __name__=='__main__':main()
