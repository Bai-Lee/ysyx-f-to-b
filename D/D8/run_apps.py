from pathlib import Path
import sys,re,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--mode',choices=['test','train'],default='test');parser.add_argument('--only',nargs='+');option=parser.parse_args()
    d=ROOT/'D/D8';am=BENCH/'abstract-machine';kernels=BENCH/'am-kernels';suite=BENCH/'archbench';build=json.loads((ROOT/'reports/D8_build.json').read_text());exe=Path(build['executable']);ref=Path(build['reference'])
    if option.mode=='test':
        changes=[('benchmarks/dhrystone/dry.c','#define NUMBER_OF_RUNS\t\t500000','#define NUMBER_OF_RUNS\t\t2'),('benchmarks/coremark/include/core_portme.h','#define ITERATIONS 1000','#define ITERATIONS 2'),('benchmarks/dhrystone/dry.c','880900 / User_Time','880900 / (User_Time ? User_Time : 1)'),('benchmarks/coremark/src/core_main.c','2921400 / time_in_secs(total_time)','2921400 / (time_in_secs(total_time) ? time_in_secs(total_time) : 1)')]
        for rel,old,new in changes:
            target=kernels/rel;backup=d/'upstream'/rel;backup.parent.mkdir(parents=True,exist_ok=True)
            if not backup.exists():shutil.copyfile(target,backup)
            text=target.read_text();assert old in text or new in text;text=text.replace(old,new);target.write_text(text)
    plans=[]
    if option.mode=='test':
        for name in ['dhrystone','coremark','microbench']:
            for arch in ['native','riscv32e-npc']:plans.append(('benchmarks',name,kernels/'benchmarks'/name,arch))
    for cwd in sorted((suite/'bench').iterdir()):
        if not cwd.is_dir() or (option.mode=='train' and cwd.name=='000.hello'):continue
        for arch in (['native','riscv32e-npc'] if option.mode=='test' else ['riscv32e-npc']):plans.append(('archbench',cwd.name,cwd,arch))
    if option.only:
        plans=[p for p in plans if p[1] in option.only];assert plans,'requested program not found'
    summary=ROOT/'reports'/('D8_apps_'+option.mode+('_selected' if option.only else '')+'.json')
    rows=[]
    for group,name,cwd,arch in plans:
        tag=f'D8/apps/{option.mode}/{group}/{name}_{arch}';artifact=ROOT/'artifacts'/tag;checkpoint=artifact/'accepted.json'
        inputs=[cwd/'Makefile',*sorted(cwd.glob('**/*.c')),*sorted(cwd.glob('**/*.h'))]
        inputs=[p for p in inputs if 'build' not in p.relative_to(cwd).parts]
        inputs += [am/'Makefile',am/'scripts/isa/riscv.mk',am/'scripts/riscv32e-npc.mk',am/'scripts/platform/npc.mk',am/'am/src/riscv/npc/timer.c',*sorted((am/'klib/src').glob('*.c'))]
        if group=='archbench':inputs.extend([suite/'Makefile',suite/'libbench/bench.c'])
        if arch=='riscv32e-npc':inputs.extend([exe,ref])
        fingerprints=[{'path':str(p),'sha256':sha(p)} for p in dict.fromkeys(inputs)]
        if checkpoint.exists():
            prior=json.loads(checkpoint.read_text())
            if prior['inputs']==fingerprints and all(sha(Path(x['path']))==x['sha256'] for x in prior['saved']) and sha(artifact/'stdout.log')==prior['stdout_sha256']:
                rows.append(prior);print('APP_REUSE',option.mode,name,arch,flush=True);continue
            history=artifact/'accepted_history'/str(time.time_ns());history.mkdir(parents=True)
            shutil.copyfile(checkpoint,history/'accepted.json')
            for saved in prior['saved']:
                file=Path(saved['path']);assert file.parent==artifact and sha(file)==saved['sha256']
                shutil.copyfile(file,history/file.name)
        env={'BENCH_HOME':str(suite),'nproc':'1','SDL_VIDEODRIVER':'dummy','SDL_AUDIODRIVER':'dummy'}
        args=['make','-j1','ARCH='+arch,'run','mainargs='+option.mode]
        if arch=='riscv32e-npc':args.append('NPC_ARGS=--frequency 100000000 --uart-random --max-cycles 100000000000')
        o,e,record=run(tag,args,cwd=cwd,env=env,inputs=list(dict.fromkeys(inputs)),timeout=7200 if option.mode=='train' else 1200)
        if group=='archbench' and name!='000.hello':assert re.search(r'\[RESULT\].*PASS',o) and not re.search(r'\[RESULT\].*FAIL',o),(name,o[-3000:])
        if group=='benchmarks':assert 'PASS' in o and 'FAIL' not in o,(name,o[-3000:])
        if name=='202.llama2':assert 'Once' in o
        row={'mode':option.mode,'group':group,'name':name,'arch':arch,'status':'PASS','inputs':fingerprints,'elapsed_seconds':record['elapsed_seconds'],'evidence':tag,'stdout_sha256':sha(artifact/'stdout.log'),'saved':[]}
        if arch=='riscv32e-npc':
            result=next((cwd/'build').glob('*-riscv32e-npc.bin.npc.json'));r=json.loads(result.read_text());assert r['result']=='GOOD_TRAP' and r['ebreak_calls']==1 and r['diff_checked']+r['device_sync_checked']==r['instructions'];row['simulation']=r
            for file in [result,*list((cwd/'build').glob('*-riscv32e-npc.elf'))]:
                assert file.is_file()
                saved=artifact/file.name;shutil.copyfile(file,saved);row['saved'].append({'path':str(saved),'sha256':sha(saved)})
            image=next((cwd/'build').glob('*-riscv32e-npc.bin'));saved=artifact/image.name;shutil.copyfile(image,saved);row['saved'].append({'path':str(saved),'sha256':sha(saved)})
        else:
            native=next((cwd/'build').glob('*-native.elf'));saved=artifact/native.name;shutil.copyfile(native,saved);row['saved'].append({'path':str(saved),'sha256':sha(saved)})
        if option.mode=='train':
            row['score']=int(re.search(r'^\s+(\d+) Marks$',o,re.M)[1]);row['min_time_us']=int(re.search(r'\[RESULT\].*\((\d+) us\)',o)[1])
        dump(checkpoint,row);rows.append(row);dump(summary,{'status':'IN_PROGRESS','rows':rows})
    result={'status':'PASS_SELECTED' if option.only else 'PASS','selected':option.only,'mode':option.mode,'runs':len(rows),'rows':rows,'scope':'Earlier standalone E6 application workloads recompiled for RV32E; --only is a selected diagnostic run, not whole-suite acceptance. Native baselines in test mode. Dhrystone/CoreMark retain prior course-permitted two-iteration configuration; train archbench workloads and validators unchanged. 100MHz is an assumed model frequency, not a silicon qualification.'}
    if option.mode=='train':
        import math
        scores=[r['score'] for r in rows];result['arithmetic_mean']=sum(scores)/len(scores);result['geometric_mean']=math.exp(sum(math.log(v) for v in scores)/len(scores)) if min(scores)>0 else 0
    dump(summary,result);print('D8_APPS_PASS',option.mode,len(rows),flush=True)

if __name__=='__main__':main()
