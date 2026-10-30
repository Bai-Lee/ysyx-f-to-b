from common7 import *
from software_soc import SOFT,environment,clock_config
import re
def main():
 manifest=json.loads((ROOT/'reports/E7_batch_integrity.json').read_text());assert manifest['status']=='PASS_OBJECT_PRESERVATION_AND_FLAT_RUN';clock_config()
 rows=[];exe=WORK/'build/E7/soc/sim'
 for name in ['all','wrong']:
  cwd=SOFT/'batch'/name;image=cwd/'build'/('official-batch-'+name+'-minirv-ysyxsoc.bin');result=Path(str(image)+'.npc.json')
  o,e,r=run('E7/soc_batch/'+name,['make','-j1','ARCH=minirv-ysyxsoc','mainargs=test','run','NPC_ARGS=--ratio 1 --frequency 25000000 --max-cycles 10000000000'],cwd=cwd,env=environment(),inputs=[exe,cwd/'main.c',cwd/'batch_bridge.S',ROOT/'reports/E7_batch_integrity.json'],outputs=[image,result,Path(str(result)+'.serial.txt'),Path(str(result)+'.uart.txt')],expected=(2,) if name=='wrong' else (0,),timeout=3600)
  d=json.loads(result.read_text());assert d['serial_matches'] and d['serial_framing_errors']==0
  if name=='all':
   passed=re.findall(r'^\[CASE\] (\S+) PASS cycles=(\d+)$',o,re.M);wanted=[x['id'] for x in manifest['tests'] if x['id']!='cpu:wrong'];assert [x[0] for x in passed]==wanted and all(int(x[1])>0 for x in passed) and d['result']=='GOOD_TRAP' and 'BATCH_ALL_PASSED 73' in o
   rows=[{'id':n,'status':'PASS','cycles_including_bridge':int(c)} for n,c in passed]
  else:assert d['result']=='BAD_TRAP' and '[CASE] cpu:wrong FAIL code=1' in o
  dest=ROOT/'artifacts/E7/soc_batch'/name;shutil.copyfile(result,dest/'result.json');dump(dest/'summary.json',{'status':'PASS_EXPECTED_REJECTION' if name=='wrong' else 'PASS','simulation':d,'make_exit':r['exit_code'],'image_sha256':sha(image)})
  exported=ROOT/'E/E7/batch'/name
  for file in [image,image.with_suffix('.elf'),SOFT/'abstract-machine/am/src/riscv/npc/e7_config.h']:shutil.copyfile(file,exported/file.name)
 dump(ROOT/'reports/E7_soc_tests.json',{'status':'PASS','tests':rows,'riscv_count':38,'cpu_count':35,'negative':'Wrong-onlybatch producedBAD_TRAPandtop-levelmakenonzero','batching':'OnefullrealSoCbootexecutesall73originaltestbodies. Onlysymbolnamesandassemblyhaltdispatchareadapted; allallocatedobjectcode/dataunchanged, alltestconditionsretained. Not73separatecoldboots. Everyinstructionstillcomparedagainstindependentreference.'})
 lines=['# 73 项 SoC 测试结果','','批次从 Flash 通过原加载器启动，逐一执行 35 个 cpu-tests 和 38 个 riscv-tests。各测试目标代码及数据节逐字节保持，链接符号避免重名；汇编测试的 0/非零退出值通过保存现场的返回桥交给调度器。wrong 负对照在独立批次中使仿真和 make 失败。并非 73 次独立冷启动。','','| 测试 | 结果 | 周期（含调用桥） |','|---|---|---:|']
 lines += ['| '+r['id']+' | PASS | '+str(r['cycles_including_bridge'])+' |' for r in rows];(ROOT/'reports/E7_SOC_TESTS.md').write_text('\n'.join(lines)+'\n')
 mark(['E7-M013'],'PASS',['reports/E7_soc_tests.json','reports/E7_SOC_TESTS.md','reports/E7_batch_integrity.json','artifacts/E7/soc_batch'],'All35CPUand38ISAofficialtestbodiesactuallyranonrealSoC withpercommitDiffTest andper-casepass/cycleoutput; originalallocatedcode/data preserved; batchedoneboot, wrongbatchfailurepropagates.')
 print('ALL73_OFFICIAL_TESTS_ON_REAL_SOC_PASS',flush=True)
if __name__=='__main__':main()
