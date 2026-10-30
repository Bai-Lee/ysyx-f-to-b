from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    d=ROOT/'D/D6';base=WORK/'backend';base.mkdir(exist_ok=True)
    ecc=Path('/home/USER/tools/e-stage/ecos-alpha9/squashfs-root/resources/binaries/ecc')
    suite=Path('/home/USER/tools/e-stage/oss-20260821/oss-cad-suite')
    pdk=Path('/home/USER/tools/icsprout55-e-stage')
    guard=d/'budget_exec.py'
    if not guard.exists():shutil.copyfile(ROOT/'E/runtime/budget_exec.py',guard)
    env={'PATH':str(suite/'bin')+':'+os.environ['PATH'],'CUDA_VISIBLE_DEVICES':'','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','YOSYS_SYNTH_STRATEGY':'DELAY 4'}
    rows=[]
    for label,corner in [('tt','typ_tt_1p2_25'),('ss','ss_rcworst_1p08_125'),('ff','ff_rcbest_1p32_m40')]:
        project=base/('light_'+label);project.mkdir(exist_ok=True);(project/'rtl').mkdir(exist_ok=True)
        rtl=project/'rtl/light.v';rtl.write_text((d/'light.v').read_text())
        libs=[];lefs=[]
        for k in ['R','L']:
            folder=pdk/('IP/STD_cell/ics55_LLSC_H7C_V1p10C100/ics55_LLSC_H7C'+k)
            libs.append(folder/'liberty'/('ics55_LLSC_H7C'+k+'_'+corner+'_nldm.lib'))
            lefs.append(folder/'lef'/('ics55_LLSC_H7C'+k+'_ecos.lef'))
        config=project/'ecc.toml';config.write_text('[design]\nname="light"\ntop="light"\nrtl=["rtl/light.v"]\nclock_port="clock"\nfrequency_mhz=100.0\n[pdk]\nname="ics55"\nroot="'+str(pdk)+'"\n[flow]\npreset="syn_sta"\nrun="baseline"\n[pdk.overrides]\nlibs='+json.dumps(list(map(str,libs)))+'\nlefs='+json.dumps(list(map(str,lefs)))+'\ndont_use=["*AO222*","*2BB2*","*AOI222*","*AOI33*","*OA222*","*OAI222*","*OAI33*","*NOR4*"]\n')
        target=project/'runs/baseline';budget=ROOT/'artifacts/D6/pvt'/label/'budget.json'
        outputs=[target/'Synthesis_yosys/output/light_Synthesis.v.gz',target/'Synthesis_yosys/analysis/qor_metrics.json',target/'Synthesis_yosys/report/post_synthesis/power.rpt']
        run('D6/pvt/'+label,['python3',guard,'--rss-mib','2800','--metric','pss','--report',budget,'--','taskset','-c','0,1',ecc,'run','--project',project,'--plain'],cwd=base,inputs=[config,rtl,ecc,*libs,*lefs],outputs=outputs,env=env,timeout=600,resume=True)
        out=d/'results/pvt'/label;out.mkdir(parents=True,exist_ok=True)
        qorfile=target/'Synthesis_yosys/feature/post_synthesis/qor_summary.json'
        files=[config,rtl,*outputs,qorfile,*list((target/'Synthesis_yosys/report').rglob('*.rpt')),*list((target/'Synthesis_yosys/script').glob('*.tcl')),target/'Synthesis_yosys/log/Synthesis.log',target/'origin/light.sdc',target/'home/flow.json',budget]
        saved=[]
        for i,p in enumerate(dict.fromkeys(files)):
            dest=out/(f'{i:02d}_'+p.name);shutil.copyfile(p,dest);saved.append({'original':str(p),'copy':str(dest),'sha256':sha(p)})
        metrics=json.loads(outputs[1].read_text())
        rows.append({'label':label,'corner':corner,'status':'PASS_SYNTHESIS_STA_ONLY','qor':json.loads(qorfile.read_text()),'metrics':metrics,'power_report':outputs[2].read_text(),'libraries':[{'path':str(p),'sha256':sha(p)} for p in libs],'netlist_sha256':sha(outputs[0]),'files':saved})
        dump(ROOT/'reports/D6_pvt.json',{'status':'IN_PROGRESS','constraint_mhz':100,'rows':rows})
    dump(ROOT/'reports/D6_pvt.json',{'status':'PASS_SYNTHESIS_STA_ONLY','constraint_mhz':100,'strategy':'DELAY 4','scope':'Same RTL, clock, LEF and strategy; each corner re-synthesized, so mapped cells may change. No routed parasitics; power is vectorless tool estimate. Not physical signoff or measured silicon.','rows':rows})

if __name__=='__main__':main()
