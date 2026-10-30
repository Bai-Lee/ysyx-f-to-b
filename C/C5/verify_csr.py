from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *


def main():
    subprocess.run(['python3',str(ROOT/'C/C5/prepare_am.py')],check=True)
    base=WORK/'c5/workbench';am=base/'abstract-machine';ref=WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so'
    build=next(r for r in json.loads((ROOT/'reports/C5_soc_build.json').read_text())['variants'] if r['reset_pc']==0x30000000 and r.get('cycle_sim',False) and not r.get('mutant',False) and not r.get('psram_qpi',False) and r.get('psram_bytes',4096)==4096 and not r.get('fast_flash',False))
    exe=Path(build['executable']);assert sha(exe)==build['sha256'];rows=[]
    project=json.loads((ROOT/'C/C5/project_config.json').read_text());assert project['project_id']==int(project['project_id_hex'],16)==0x26070001
    for name,statement in [('positive',None),('readonly-write','csrw mvendorid,zero'),('unknown-csr','csrr a0,0x7ff')]:
        app=base/('csr-'+name);app.mkdir(exist_ok=True)
        if statement is None:
            shutil.copyfile(ROOT/'C/C5/programs/csr-test.c',app/'main.c');shutil.copyfile(ROOT/'C/C5/programs/csr-trap.S',app/'trap.S');srcs='main.c trap.S'
        else:
            (app/'main.c').write_text('#include <am.h>\nint main(const char *args){(void)args;__asm__ volatile("'+statement+'":::"a0","memory");return 0;}\n');srcs='main.c'
        (app/'Makefile').write_text('NAME = csr-'+name+'\nSRCS = '+srcs+'\ninclude $(AM_HOME)/Makefile\n')
        arch='riscv32e-ysyxsoc-flash-id';image=app/'build'/('csr-'+name+'-'+arch+'.bin');elf=image.with_suffix('.elf');tag='C5/csr/'+name
        inputs=[app/'main.c',app/'Makefile',*([app/'trap.S'] if statement is None else []),*sorted((am/'am/src/riscv/ysyxsoc').glob('*')),ROOT/'C/C5/project_config.json']
        run(tag+'/build',['make','-j1','ARCH='+arch,'insert-arg'],cwd=app,env={'AM_HOME':str(am),'NPC_HOME':str(base/'npc')},inputs=inputs,outputs=[image,elf],timeout=180)
        out=ROOT/'artifacts'/tag;out.mkdir(parents=True,exist_ok=True);report=out/'simulation.json';trace=out/'events.log'
        stdout,stderr,_=run(tag+'/run',[exe,'--flash',image,'--ref',ref,'--report',report,'--trace',trace,'--trace-limit','250000','--max-cycles','20000000'],inputs=[exe,image,elf,ref],outputs=[report,trace],expected=(0 if statement is None else 3,),timeout=180)
        data=json.loads(report.read_text());assert data['diff_enabled'] and data['diff_checked']+data['device_sync_checked']==data['instructions']
        uart=bytes.fromhex(data['uart']['hex']).decode('ascii');assert uart.startswith('C5 ID vendor=79737978 project=26070001\n')
        if statement is None:
            assert data['result']=='GOOD_TRAP' and 'CSR/TRAP PASS project=26070001' in uart
            instructions=[line.split()[3] for line in trace.read_text().splitlines() if line.startswith('I ')]
            assert instructions.count('00000073')==4 and instructions.count('30200073')==4
        else:assert data['result']=='NPC_FAULT' and data['fault']==1
        rows.append({'name':name,'status':'PASS','simulation':data,'uart':uart,'evidence':'artifacts/'+tag,'image_sha256':sha(image),'elf_sha256':sha(elf)})
    dump(ROOT/'reports/C5_csr.json',{'status':'PASS_PROJECT_ID_CSR_AND_SYNCHRONOUS_TRAPS','runs':rows,'project':project,
         'scope':'Educational machine-mode subset: six CSR operations, read-only IDs, MIE/MPIE and fixed MPP=M, mtvec direct/vectored base for synchronous ECALL, mepc alignment, mcause11, MRET. Immediate31 and rd/rs1 collision tested; read-only/unknown accesses fail. No U/S mode, asynchronous timer interrupt or full privileged-ISA claim. Minimum C5 RT-Thread prerequisite, not completion of B stage.'})
    mark(['C5-M023'],'PASS',['reports/C5_csr.json','C/C5/project_config.json'],'Actual project-only IDs read and printed before main; CSR operations and real ECALL/MRET prerequisites verified against independent NEMU and program checks.')
    print('C5_CSR_IDS_AND_TRAP_PREREQUISITE_PASS',flush=True)


if __name__=='__main__':main()
