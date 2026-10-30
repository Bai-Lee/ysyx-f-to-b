from common7 import *
import argparse,gzip,re
sys.path.insert(0,str(ROOT/'E/runtime'))
from backend_audit import pins,check_ports
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--prepare-only',action='store_true');args=parser.parse_args()
 lock=json.loads((ROOT/'reports/E_backend_compatible_tools.json').read_text());ecc=Path(lock['ecc']);suite=Path(lock['yosys_root']);proj=WORK/'backend/e7_minirv';(proj/'rtl').mkdir(parents=True,exist_ok=True)
 sources=[ROOT/'E/E5/rtl/minirv_decode.sv',ROOT/'E/E5/rtl/minirv_regfile.sv',ROOT/'E/E7/rtl/minirv_bus.sv',ROOT/'E/E7/rtl/ysyx_00000000.sv'];combined=proj/'rtl/cpu.v';combined.write_text('\n'.join(f.read_text() for f in sources))
 config=(WORK/'backend/light/ecc.toml').read_text().replace('name="light"','name="e7_minirv"').replace('top="light"','top="ysyx_00000000"').replace('rtl=["rtl/light.v"]','rtl=["rtl/cpu.v"]');(proj/'ecc.toml').write_text(config)
 env={'PATH':str(suite/'bin')+':'+os.environ['PATH'],'CUDA_VISIBLE_DEVICES':'','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'}
 run('E7/synthesis/check',[ecc,'check','--project',proj],env=env,inputs=[proj/'ecc.toml',combined])
 if args.prepare_only:print('E7_SYNTHESIS_READY_NOT_RUN',flush=True);return
 rows=[]
 for name,strategy in [('baseline','BALANCE 3'),('area','AREA 0')]:
  run('E7/synthesis/'+name,[ecc,'run','--project',proj,'--run-id',name,'--plain'],env={**env,'YOSYS_SYNTH_STRATEGY':strategy},inputs=[proj/'ecc.toml',combined,ecc],timeout=1200)
  root=proj/'runs'/name;qor=json.loads((root/'Synthesis_yosys/feature/post_synthesis/qor_summary.json').read_text());frequency=qor['summary']['setup']['frequency_mhz'];area=qor['design_statistics']['cella'];assert frequency>25 and area>0
  net=root/'Synthesis_yosys/output/e7_minirv_Synthesis.v.gz';text=gzip.decompress(net.read_bytes()).decode();count,errors=check_ports(text,pins(Path('/home/USER/tools/icsprout55-e-stage').glob('IP/STD_cell/ics55_LLSC_H7C_V1p10C100/*/lef/*_ecos.lef')));assert not errors
  assert not re.search(r'\bLAT\w*\s+[^;]+\(',text)
  dest=ROOT/'E/E7/synthesis'/name;dest.mkdir(parents=True,exist_ok=True)
  for f in [net,root/'Synthesis_yosys/output/e7_minirv_Synthesis_sim.v.gz',root/'Synthesis_yosys/feature/post_synthesis/qor_summary.json',root/'origin/e7_minirv.sdc',proj/'ecc.toml',combined]:shutil.copyfile(f,dest/f.name)
  row={'variant':name,'strategy':strategy,'frequency_mhz':frequency,'max_pll_multiplier':int(frequency//25),'cell_area_um2':area,'modeled_die_area_mm2':area/.6/1e6,'modeled_fabrication_cost_cny':area/.6/1e6*30000,'mapped_instances':count,'latches':0,'qor':qor,'constraint_frequency_mhz':100,'timing_constraint_met':qor['summary']['setup']['wns']>=0 and qor['summary']['hold']['wns']>=0,'netlist_sha256':sha(net),'rtl_sha256':sha(combined),'run':str(root)};rows.append(row);dump(ROOT/'reports/E7_synthesis.json',{'status':'IN_PROGRESS','variants':rows})
 dump(ROOT/'reports/E7_synthesis.json',{'status':'PASS_SYNTHESIS_ANALYSIS','variants':rows,'limits':'TT1.2V25C, pre-layout CPU only, no SoC or physical signoff. 60% utilization and CNY30000/mm2 are course hypothetical costing, not a quotation.'})
 mark(['E7-M028'],'PASS',['reports/E7_synthesis.json','E/E7/synthesis'],'Computed the course hypothetical die/cost model from actual synthesis area; CPU-only and missing other costs explicitly bounded.')
 print('E7_SYNTHESIS_BASELINE_AND_AREA_PASS',flush=True)
if __name__=='__main__':main()
