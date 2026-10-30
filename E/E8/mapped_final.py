"""Complete final baseline netlist in four states, with unchanged PDK UDP models."""
from pathlib import Path
import sys,resource
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
 resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024));resource.setrlimit(resource.RLIMIT_CPU,(14400,14410))
 p=ROOT/'E/E8';wd=WORK/'build/E8/profile/14';exe=Path('/home/USER/tools/e-stage/oss-20261022/oss-cad-suite/bin/vvp');vvp=wd/'udp.vvp';rows=[]
 prior=json.loads((ROOT/'reports/E8_mapped_programs.json').read_text())
 assert [(r['program'],r['status']) for r in prior['records'] if r['variant']=='baseline' and r['engine']=='verilator']==[('hello','PASS'),('microbench','PASS')]
 tests=[('correct',p/'examples/correct.bin',0),('bad_exit',p/'examples/bad_exit.bin',1)]+[(x['name'],Path(x['image']),0) for x in json.loads((ROOT/'reports/E8_software.json').read_text())['programs']]
 for name,image,expected in tests:
  tag='E8/final_mapped/icarus14/'+name;d=ROOT/'artifacts'/tag;checkpoint=d/'accepted.json'
  if checkpoint.exists():
   row=json.loads(checkpoint.read_text());assert row['image_sha256']==sha(image) and row['vvp_sha256']==sha(vvp) and row['stdout_sha256']==sha(d/'stdout.log');rows.append(row);continue
  out=d/'result.json'
  o,e,r=run(tag,[exe,'-M'+str(wd),'-mvpi_memory',vvp,'+image='+str(image),'+report='+str(out),'+max_cycles=50000000'],inputs=[exe,vvp,wd/'vpi_memory.vpi',image],outputs=[out,Path(str(out)+'.uart.txt'),Path(str(out)+'.progress.tsv')],expected=(expected,),timeout=18000)
  data=json.loads(out.read_text());assert data['exit_writes']==1 and data['exit_code']==expected
  if name=='microbench':assert 'MicroBench PASS' in o
  row={'name':name,'status':'PASS_EXPECTED_REJECTION' if expected else 'PASS','result':data,'elapsed_seconds':r['elapsed_seconds'],'image_sha256':sha(image),'vvp_sha256':sha(vvp),'stdout_sha256':sha(d/'stdout.log'),'evidence':str(d.relative_to(ROOT))};dump(checkpoint,row);rows.append(row);dump(ROOT/'reports/E8_final_mapped.json',{'status':'IN_PROGRESS','rows':rows})
 dump(ROOT/'reports/E8_final_mapped.json',{'status':'PASS','candidate':'baseline','rows':rows,'verilator_evidence':[r for r in prior['records'] if r['variant']=='baseline' and r['engine']=='verilator'],'scope':'Finalbaselinecandidate: fullhelloandmicrobench inVerilatorandIcarus14. IcarususesofficialoriginalUDPstandardcellmodelswithfunctionaldefineonly; noforcedinitialization, noXcoercion, noSDFtimingclaim. EarlierIcarus11CPUlimitpreservedasseparateRESOURCE_LIMIT.'})
 mark(['E8-M007','E8-M008'],'PASS',['reports/E8_final_mapped.json','reports/E8_mapped_preflight.json','artifacts/E8/final_mapped'],'Finalbaselineactualmappednetlist completeshelloandfullmicrobench inboth2stateand4statesimulators, originalPDKUDPmodelsretainedforIcarus; invalidexitnegativefails.')
 print('FINAL_BASELINE_NETLIST_FULL_PROGRAMS_BOTH_SIMULATORS_PASS',flush=True)
if __name__=='__main__':main()
