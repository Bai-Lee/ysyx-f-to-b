from pathlib import Path
import sys,resource
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
 resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024));resource.setrlimit(resource.RLIMIT_CPU,(40,40))
 exe=WORK/'build/E8/correct_2state/sim';rows=[]
 for item in json.loads((ROOT/'reports/E8_software.json').read_text())['programs']:
  image=Path(item['image']);assert sha(image)==item['sha256'];out=ROOT/'artifacts/E8/rtl_verilator'/item['name']/'result.json'
  o,e,r=run('E8/rtl_verilator/'+item['name'],[exe,'--image',image,'--report',out,'--max-cycles','50000000'],inputs=[exe,image],outputs=[out],timeout=50);d=json.loads(out.read_text());assert d['result']=='GOOD_TRAP' and d['exit_writes']==1
  assert ('MicroBench PASS' if item['name']=='microbench' else 'Hello, AbstractMachine!') in o
  rows.append({'name':item['name'],'result':d})
 dump(ROOT/'reports/E8_rtl_verilator.json',{'status':'PASS','programs':rows,'scope':'CPU RTL in final port-only test harness; full four-state and mapped netlist programs still separate.'})
 print('E8_RTL_VERILATOR_PROGRAMS_PASS',flush=True)
if __name__=='__main__':main()
