from pathlib import Path
import sys,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from support import select_build


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--build-only',action='store_true');parser.add_argument('--variant',default='30000000-cycle-psram4m-qpi');args=parser.parse_args()
    subprocess.run(['python3',str(ROOT/'C/C5/prepare_am.py')],check=True)
    base=WORK/'c5/workbench';am=base/'abstract-machine';rows=[]
    for name in ['positive','bad-restore']:
        app=base/('cte-'+name);app.mkdir(exist_ok=True)
        for filename in ['context-test.c','context-probe.S']:shutil.copyfile(ROOT/'C/C5/programs'/filename,app/filename)
        sources='context-test.c context-probe.S'
        if name=='bad-restore':
            trap=(ROOT/'C/C5/am/trap.S').read_text();assert trap.count('  RESTORE(5)')==1
            (app/'bad-trap.S').write_text(trap.replace('  RESTORE(5)','  li t0,0'));sources+=' bad-trap.S'
        (app/'Makefile').write_text('NAME = cte-'+name+'\nSRCS = '+sources+'\ninclude $(AM_HOME)/Makefile\n')
        arch='riscv32e-ysyxsoc-psram';image=app/'build'/('cte-'+name+'-'+arch+'.bin');elf=image.with_suffix('.elf');tag='C5/context/'+name
        inputs=[*sorted(app.glob('*.c')),*sorted(app.glob('*.S')),app/'Makefile',*sorted((am/'am/src/riscv/ysyxsoc').glob('*')),am/'scripts/ysyxsoc-code-psram.ld']
        run(tag+'/build',['make','-j1','ARCH='+arch,'insert-arg'],cwd=app,env={'AM_HOME':str(am)},inputs=inputs,outputs=[image,elf],timeout=180)
        if args.build_only:continue
        exe=Path(select_build(args.variant)['executable']);ref=WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so'
        directory=ROOT/'artifacts'/tag;result=directory/'simulation.json';budget=directory/'resources.json';trace=directory/'events.log'
        run(tag+'/run',['python3',ROOT/'C/runtime/budget_exec.py','--report',budget,'--',exe,'--flash',image,'--ref',ref,'--report',result,'--trace',trace,'--trace-limit','1000000','--max-cycles','200000000'],inputs=[exe,ref,image,elf],outputs=[result,budget,trace],expected=(0 if name=='positive' else 1,),timeout=240)
        data=json.loads(result.read_text());assert data['diff_enabled'] and data['diff_checked']+data['device_sync_checked']==data['instructions']
        uart=bytes.fromhex(data['uart']['hex']).decode('ascii');instructions=[line.split()[3] for line in trace.read_text().splitlines() if line.startswith('I ')]
        if name=='positive':assert data['result']=='GOOD_TRAP' and 'C5_CTE_PASS a=12 b=12' in uart and instructions.count('00000073')==instructions.count('30200073')==52
        else:assert data['result']=='BAD_TRAP' and data['a0']==95 and 'C5_CTE_PASS' not in uart
        rows.append({'name':name,'status':'PASS','result':data['result'],'cycles':data['cycles'],'instructions':data['instructions'],'diff_checked':data['diff_checked'],'ecalls':instructions.count('00000073'),'mrets':instructions.count('30200073'),'uart':uart,'image_sha256':sha(image),'elf_sha256':sha(elf),'evidence':'artifacts/'+tag})
    if not args.build_only:dump(ROOT/'reports/C5_context.json',{'status':'PASS','runs':rows,'scope':'Two distinct PSRAM stacks and arguments, all16 RV32E GPR slots across52 ECALL/MRET context transfers, stack locals, MIE nesting foundation. Corrupt t0 restore is rejected with explicit programcode95. An earlier s1-corruption attempt disrupted test control flow and was stopped without a correctness conclusion; its logs remain in attempts. No asynchronous interrupt delivery.'})
    print('C5_CONTEXT_BUILD_ONLY' if args.build_only else 'C5_CONTEXT_PASS',flush=True)


if __name__=='__main__':main()
