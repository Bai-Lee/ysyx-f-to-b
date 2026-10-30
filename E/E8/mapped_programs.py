"""Full mapped-netlist functional tests; bounded512MiB,1800CPU seconds/case."""
from pathlib import Path
import sys,resource
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
 resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024));resource.setrlimit(resource.RLIMIT_CPU,(1800,1810))
 p=ROOT/'E/E8';work=WORK/'build/E8/vpi';rows=[]
 assert json.loads((ROOT/'reports/E8_mapped_preflight.json').read_text())['status']=='PASS_SMALL_NETLIST_CONTROLS'
 for variant in ['baseline','area']:
  for engine in ['verilator','iverilog']:
   executable=WORK/'build/E8'/('mapped_'+variant)/'sim' if engine=='verilator' else work/('netlist_'+variant+'.vvp')
   for item in json.loads((ROOT/'reports/E8_software.json').read_text())['programs']:
    tag='E8/mapped_programs/'+variant+'/'+engine+'/'+item['name'];dest=ROOT/'artifacts'/tag;dest.mkdir(parents=True,exist_ok=True);checkpoint=dest/'accepted.json';image=Path(item['image']);assert sha(image)==item['sha256']
    if checkpoint.exists():
     row=json.loads(checkpoint.read_text());assert row['executable_sha256']==sha(executable) and row['image_sha256']==sha(image) and row['stdout_sha256']==sha(dest/'stdout.log');rows.append(row);print('MAPPED_REUSE',variant,engine,item['name'],flush=True);continue
    out=dest/'result.json';cmd=[executable,'--image',image,'--report',out,'--max-cycles','50000000'] if engine=='verilator' else ['vvp','-M'+str(work),'-mvpi_memory',executable,'+image='+str(image),'+report='+str(out),'+max_cycles=50000000']
    o,e,r=run(tag,cmd,inputs=[executable,image,work/'vpi_memory.vpi'] if engine=='iverilog' else [executable,image],outputs=[out,Path(str(out)+'.uart.txt')],timeout=2700)
    d=json.loads(out.read_text());assert d['result']=='GOOD_TRAP' and d['exit_writes']==1
    assert ('MicroBench PASS' if item['name']=='microbench' else 'Hello, AbstractMachine!') in o
    row={'variant':variant,'engine':engine,'program':item['name'],'status':'PASS','result':d,'executable_sha256':sha(executable),'image_sha256':sha(image),'stdout_sha256':sha(dest/'stdout.log'),'elapsed_seconds':r['elapsed_seconds'],'evidence':str(dest.relative_to(ROOT))};dump(checkpoint,row);rows.append(row);dump(ROOT/'reports/E8_mapped_programs.json',{'status':'IN_PROGRESS','records':rows})
 dump(ROOT/'reports/E8_mapped_programs.json',{'status':'PASS','records':rows,'scope':'Both actual synthesisnetlists with officialICsprout55cellmodels; Verilator2state andIcarus4state, completeupstreamhello/microbenchtestvalidators. Functional no-SDFsimulations, notphysicaltimingproof.'})
 mark(['E8-M006','E8-M007'],'PASS',['reports/E8_mapped_programs.json','reports/E8_mapped_preflight.json','artifacts/E8/mapped_programs'],'Bothbaselineandareamappednetlists actuallyrancompletehello/microbench underVerilatorandIcarus; positive/negativeexit controls andX-awareVPI retained.')
 print('ALL_MAPPED_NETLIST_PROGRAMS_PASS',flush=True)
if __name__=='__main__':main()
