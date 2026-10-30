from common7 import *
import resource
def main():
 resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024));resource.setrlimit(resource.RLIMIT_CPU,(40,40))
 exe=WORK/'build/E7/soc/sim';image=BENCH7/'ysyxSoC/ready-to-run/minirv/hello-minirv-ysyxsoc.bin';result=ROOT/'artifacts/E7/loader_pilot/result.json'
 o,e,r=run('E7/loader_pilot',[exe,'--image',image,'--report',result,'--max-cycles','10000000','--until-output',"mainargs = 'Hello, One Student One Chip!'.\n",'--require-loop'],inputs=[exe,image],outputs=[result],expected=(0,124),timeout=45)
 d=json.loads(result.read_text());dump(ROOT/'reports/E7_loader_pilot.json',{'status':'PASS_BOUNDED_HELLO' if d['result']=='BOUNDED_OUTPUT_OBSERVATION' else 'RESOURCE_LIMIT_PILOT_ONLY','simulation':d,'note':'10M-cycle bounded pilot. A CYCLE_LIMIT result measures throughput/progress only and does not accept the official loader/hello task.'})
 print('LOADER_PILOT_RESULT',d['result'],d['cycles'],d['wall_seconds'],flush=True)
if __name__=='__main__':main()
