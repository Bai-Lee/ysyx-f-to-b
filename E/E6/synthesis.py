from pathlib import Path
import sys,re,gzip
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from backend_audit import pins,check_ports
def main():
 tools=json.loads((ROOT/'reports/E_backend_compatible_tools.json').read_text());ecc=Path(tools['ecc']);suite=Path(tools['yosys_root']);base=WORK/'backend';proj=base/'e6_minirv';proj.mkdir(exist_ok=True);(proj/'rtl').mkdir(exist_ok=True)
 sources=[]
 for n in ['minirv_decode.sv','minirv_regfile.sv','minirv_single.sv']:
  file=proj/'rtl'/n;shutil.copyfile(ROOT/'E/E5/rtl'/n,file);sources.append(file)
 combined=proj/'rtl/minirv.v';combined.write_text('\n'.join(p.read_text() for p in sources));sources.append(combined)
 config=(base/'light/ecc.toml').read_text().replace('name="light"','name="e6_minirv"').replace('top="light"','top="minirv_single"').replace('rtl=["rtl/light.v"]','rtl=["rtl/minirv.v"]');(proj/'ecc.toml').write_text(config)
 env={'PATH':str(suite/'bin')+':'+os.environ['PATH'],'CUDA_VISIBLE_DEVICES':'','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'}
 run('E6/synthesis/check',[ecc,'check','--project',proj],env=env,inputs=[proj/'ecc.toml',*sources])
 run('E6/synthesis/run',[ecc,'run','--project',proj,'--run-id','baseline','--plain'],env=env,inputs=[ecc,proj/'ecc.toml',*sources],timeout=1200)
 runroot=proj/'runs/baseline';qor=json.loads((runroot/'Synthesis_yosys/feature/post_synthesis/qor_summary.json').read_text());freq=qor['summary']['setup']['frequency_mhz'];assert freq>0
 net=runroot/'Synthesis_yosys/output/e6_minirv_Synthesis.v.gz';count,errs=check_ports(gzip.decompress(net.read_bytes()).decode(),pins(Path('/home/USER/tools/icsprout55-e-stage').glob('IP/STD_cell/ics55_LLSC_H7C_V1p10C100/*/lef/*_ecos.lef')));assert not errs
 dest=ROOT/'E/E6/synthesis';dest.mkdir(exist_ok=True)
 for f in [proj/'ecc.toml',runroot/'Synthesis_yosys/feature/post_synthesis/qor_summary.json',net,runroot/'Synthesis_yosys/output/e6_minirv_Synthesis_sim.v.gz',runroot/'origin/e6_minirv.sdc']:shutil.copyfile(f,dest/f.name)
 dump(ROOT/'reports/E6_synthesis.json',{'status':'PASS_SYNTHESIS_STA','frequency_mhz':freq,'frequency_hz':int(freq*1000000),'cell_area_um2':qor['design_statistics']['cella'],'qor':qor,'mapped_instances':count,'netlist_sha256':sha(net),'project':str(proj),'pdk':'ICsprout55 v1.10.100 R+L TT 1.2V 25C','yosys':tools['version'],'limitations':'Pre-layout library/SDC estimate for standalone CPU without memory; not routed timing, silicon measurement or signoff.'})
 mark(['E6-M021'],'PASS',['reports/E6_synthesis.json','E/E6/synthesis','artifacts/E6/synthesis'],'Real ECC synthesis and TT static timing, with compatible Yosys. Independent LEF pin-name checks pass; timing assumptions and no-layout scope explicit.')
 print('E6_SYNTHESIS_PASS',freq,flush=True)
if __name__=='__main__':main()
