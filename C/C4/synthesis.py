from pathlib import Path
import sys,argparse,gzip
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from resource_policy import POLICY_PATH, load_policy, generation_environment

def main():
    p=argparse.ArgumentParser();p.add_argument('--prepare-only',action='store_true');p.add_argument('--only',choices=['single','axi']);a=p.parse_args()
    d=ROOT/'C/C4';base=WORK/'c4/synthesis';base.mkdir(parents=True,exist_ok=True)
    ecc=Path('/home/USER/tools/e-stage/ecos-alpha9/squashfs-root/resources/binaries/ecc');suite=Path('/home/USER/tools/e-stage/oss-20260821/oss-cad-suite');pdk=Path('/home/USER/tools/icsprout55-e-stage')
    libs=[];lefs=[]
    for k in ('R','L'):
        folder=pdk/('IP/STD_cell/ics55_LLSC_H7C_V1p10C100/ics55_LLSC_H7C'+k)
        libs.append(folder/'liberty'/('ics55_LLSC_H7C'+k+'_typ_tt_1p2_25_nldm.lib'));lefs.append(folder/'lef'/('ics55_LLSC_H7C'+k+'_ecos.lef'))
    rows=[]
    for name,top,files in [('single','single_with_memories',[d/'rtl/rv32e_execute.sv',d/'synthesis/single_with_memories.sv']),('axi','c4_axi_core',sorted((d/'rtl').glob('*.sv')))]:
        project=base/name;(project/'rtl').mkdir(parents=True,exist_ok=True)
        source=project/'rtl/cpu.sv';source.write_text('\n'.join(p.read_text() for p in files))
        config=project/'ecc.toml';config.write_text('[design]\nname="c4_'+name+'"\ntop="'+top+'"\nrtl=["rtl/cpu.sv"]\nclock_port="clock"\nfrequency_mhz=100.0\n[pdk]\nname="ics55"\nroot="'+str(pdk)+'"\n[flow]\npreset="syn_sta"\nrun="baseline"\n[pdk.overrides]\nlibs='+json.dumps(list(map(str,libs)))+'\nlefs='+json.dumps(list(map(str,lefs)))+'\ndont_use=["*AO222*","*2BB2*","*AOI222*","*AOI33*","*OA222*","*OAI222*","*OAI33*","*NOR4*"]\n')
        row={'name':name,'top':top,'project':str(project),'config':str(config),'source':str(source),'source_sha256':sha(source),'source_files':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in files]};rows.append(row)
    dump(ROOT/'reports/C4_synthesis_inputs.json',{'status':'PREPARED_NOT_RUN','variants':rows,'libraries':[{'path':str(p),'sha256':sha(p)} for p in libs],'clock_mhz':100,'strategy':'DELAY 4','scope':'Baseline contains exactly two256x32 asynchronous-read flop memories plus CPU; AXI comparison contains CPU+adapters+arbiter, no DPI memory slave. Final SDC/structure/timing reports are authoritative.'})
    if a.prepare_only:print('C4_SYNTHESIS_PREPARED',flush=True);return
    guard=d/'synthesis/budget_exec.py'
    assert guard.is_file(), guard
    env={'PATH':str(suite/'bin')+':'+os.environ['PATH'],'CUDA_VISIBLE_DEVICES':'','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','YOSYS_SYNTH_STRATEGY':'DELAY 4'}
    accepted=[]
    for row in rows:
        if a.only and row['name']!=a.only:continue
        project=Path(row['project']);name=row['name'];target=project/'runs/baseline';budget=ROOT/'artifacts/C4/synthesis'/name/'budget.json'
        design='c4_'+name;net=target/'Synthesis_yosys/output'/(design+'_Synthesis.v.gz');metrics=target/'Synthesis_yosys/analysis/qor_metrics.json';qor=target/'Synthesis_yosys/feature/post_synthesis/qor_summary.json'
        run('C4/synthesis/'+name,['python3',guard,'--metric','pss','--report',budget,'--','taskset','-c','0,1',ecc,'run','--project',project,'--plain'],cwd=base,inputs=[POLICY_PATH,ROOT/'C/runtime/budget_exec.py',ROOT/'C/runtime/resource_policy.py',guard,Path(row['config']),Path(row['source']),ecc,*libs,*lefs],outputs=[net,metrics,qor],env=env,timeout=1800,resume=True)
        output=d/'synthesis'/name;output.mkdir(exist_ok=True)
        files=[Path(row['config']),Path(row['source']),net,metrics,qor,target/'origin'/(design+'.sdc'),target/'Synthesis_yosys/log/Synthesis.log',budget]
        files += list((target/'Synthesis_yosys/script').glob('*.tcl'))+list((target/'Synthesis_yosys/report').rglob('*.rpt'))
        saved=[]
        for i,p in enumerate(dict.fromkeys(files)):
            dest=output/(f'{i:02d}_'+p.name);shutil.copyfile(p,dest);saved.append({'path':str(dest.relative_to(ROOT)),'original':str(p),'sha256':sha(p)})
        result=json.loads(qor.read_text());assert result['design_statistics']['cella']>0 and result['summary']['setup']['frequency_mhz']>0
        accepted.append({**row,'status':'PASS_ECC_SYNTHESIS_STA','qor':result,'metrics':json.loads(metrics.read_text()),'files':saved,'netlist_sha256':sha(net)})
        dump(ROOT/'reports/C4_synthesis.json',{'status':'IN_PROGRESS_ADDITIONAL_IO_STA_PENDING','variants':accepted,'limits':'ECC clock constraint100MHz,TT library,ZeroWireload. Explicit external IO constraints and structural audit follow separately.'})
    print('C4_ECC_SYNTHESIS_FINISHED_IO_AUDIT_PENDING',flush=True)

if __name__=='__main__':main()
