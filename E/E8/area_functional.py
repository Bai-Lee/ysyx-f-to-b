from pathlib import Path
import sys,resource
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
 resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024));resource.setrlimit(resource.RLIMIT_CPU,(180,190));exe=WORK/'build/E8/mapped_area/sim';rows=[]
 for item in json.loads((ROOT/'reports/E8_software.json').read_text())['programs']:
  image=Path(item['image']);assert sha(image)==item['sha256'];out=ROOT/'artifacts/E8/area_functional'/item['name']/'result.json'
  o,e,r=run('E8/area_functional/'+item['name'],[exe,'--image',image,'--report',out,'--max-cycles','50000000'],inputs=[exe,image],outputs=[out,Path(str(out)+'.uart.txt')],timeout=240);data=json.loads(out.read_text());assert data['result']=='GOOD_TRAP' and data['exit_writes']==1
  if item['name']=='microbench':assert 'MicroBench PASS' in o and data['cycles']==22129163
  rows.append({'program':item['name'],'result':data,'elapsed_seconds':r['elapsed_seconds'],'image_sha256':sha(image),'simulator_sha256':sha(exe)})
 dump(ROOT/'reports/E8_area_functional.json',{'status':'PASS','programs':rows,'scope':'AREA0mappednetlistalsocompletesfullhello/microbench inVerilator. FinalphysicalcandidateisBALANCEbaseline,whichadditionallypassedcompleteIcarus4stateandphysicalsignoff.'})
 print('AREA_MAPPED_FULL_FUNCTIONAL_PROGRAMS_PASS',flush=True)
if __name__=='__main__':main()
