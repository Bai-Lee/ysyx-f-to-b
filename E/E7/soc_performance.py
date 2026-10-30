"""Full blockchain train workload at the legal SoC PLL operating points."""
from common7 import *
from software_soc import SOFT,clock_config,environment
import re,resource
def main():
 resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024));resource.setrlimit(resource.RLIMIT_CPU,(18000,18010))
 synthesis=json.loads((ROOT/'reports/E7_synthesis.json').read_text());variants={v['variant']:v for v in synthesis['variants']};rows=[]
 exe=WORK/'build/E7/soc/sim';cwd=BENCH7/'archbench/bench/100.blockchain'
 jobs=[('baseline_k1','baseline',1),('baseline_kmax','baseline',variants['baseline']['max_pll_multiplier']),('area_kmax','area',variants['area']['max_pll_multiplier'])]
 for label,variant,k in jobs:
  assert k*25<=variants[variant]['frequency_mhz'] and (label=='baseline_k1' or (k+1)*25>variants[variant]['frequency_mhz'])
  tag='E7/soc_performance/'+label;dest=ROOT/'artifacts'/tag;checkpoint=dest/'accepted.json';hz=k*25000000;header=clock_config(hz)
  if checkpoint.exists():
   row=json.loads(checkpoint.read_text());assert row['simulator_sha256']==sha(exe) and row['config_sha256']==sha(header) and row['stdout_sha256']==sha(dest/'stdout.log');rows.append(row);print('SOC_PERFORMANCE_REUSE',label,flush=True);continue
  image=cwd/'build/blockchain-minirv-ysyxsoc.bin';result=Path(str(image)+'.npc.json');vcd=WORK/(label+'.vcd')
  args=['make','-j1','ARCH=minirv-ysyxsoc','mainargs=train','run','NPC_ARGS=--ratio '+str(k)+' --frequency '+str(hz)+' --max-cycles 200000000000 --trace '+str(vcd)+' --trace-cycles 10000']
  o,e,r=run(tag,args,cwd=cwd,env=environment(),inputs=[exe,header,cwd/'Makefile',cwd/'main.c',SOFT/'abstract-machine/am/src/riscv/npc/timer.c'],outputs=[image,image.with_suffix('.elf'),result,Path(str(result)+'.uart.txt'),Path(str(result)+'.serial.txt')],timeout=18000)
  data=json.loads(result.read_text());assert data['result']=='GOOD_TRAP' and data['serial_matches'] and data['serial_framing_errors']==0
  assert re.search(r'\[RESULT\].*PASS',o) and not re.search(r'\[RESULT\].*FAIL',o)
  score=int(re.search(r'^\s+(\d+) Marks$',o,re.M)[1]);minimum=int(re.search(r'\[RESULT\].*\((\d+) us\)',o)[1]);assert minimum>0
  from wave_check import clock_periods
  wave=clock_periods(vcd);assert abs(wave['cpu_to_soc_frequency_ratio']-k)<.001;shutil.copyfile(vcd,dest/'clocks.vcd');shutil.copyfile(result,dest/'result.json')
  row={'name':label,'variant':variant,'k':k,'cpu_frequency_hz':hz,'soc_frequency_hz':25000000,'synthesis_frequency_mhz':variants[variant]['frequency_mhz'],'min_time_us':minimum,'score':score,'simulation':data,'wave':wave,'simulator_sha256':sha(exe),'config_sha256':sha(header),'stdout_sha256':sha(dest/'stdout.log'),'image_sha256':sha(image),'evidence':str(dest.relative_to(ROOT))};dump(checkpoint,row);rows.append(row);dump(ROOT/'reports/E7_soc_performance.json',{'status':'IN_PROGRESS','records':rows})
 clock_config();base=rows[0]['min_time_us'];comparison=[{'name':r['name'],'speedup_vs_k1':base/r['min_time_us'],'cell_area_um2':variants[r['variant']]['cell_area_um2'],'modeled_cost_cny':variants[r['variant']]['modeled_fabrication_cost_cny']} for r in rows]
 dump(ROOT/'reports/E7_soc_performance.json',{'status':'PASS','records':rows,'comparison':comparison,'scope':'ThreeactualfulltrainSoCrunswithpercommitDiffTest, suppliedFlashloader/PSRAM/UARTandoriginalbenchmarkvalidators. AreaandbaselinehaveidenticalRTLfunctionalitybutdifferentmappedcellimplementation; theirlegalprelayoutPLLfrequenciesaredifferent. Thesearefunctionalmodeltimes, notpostroutefrequencymeasurements.'})
 mark(['E7-M024','E7-M026','E7-M027','E7-M029'],'PASS',['reports/E7_soc_performance.json','reports/E7_synthesis.json','reports/E7_area_units.json','artifacts/E7/soc_performance'],'Full100.blockchaintrainactualruns at25MHzk1,125MHzk5baseline and75MHzk3area;25MHzperipherals;counterfrequencyandVCDratioverified;min-times,marks,area/costretained.')
 print('SOC_BLOCKCHAIN_THREE_OPERATING_POINTS_PASS',flush=True)
if __name__=='__main__':main()
