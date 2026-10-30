from common7 import *
from software_soc import SOFT
import math,re
def main():
 names=['E7_standalone','E7_bus_tests','E7_bus_negative','E7_soc_tests','E7_soc_software','E7_soc_hello','E7_gpio_unit','E7_csr_tests','E7_gui','E7_visual_review','E7_timer','E7_synthesis','E7_soc_performance','E7_final_runtime','E7_batch_export'];data={n:json.loads((ROOT/'reports'/(n+'.json')).read_text()) for n in names};assert all(x['status'].startswith('PASS') for x in data.values()),[(n,d['status']) for n,d in data.items()]
 standalone=data['E7_standalone']['records'];assert len(standalone)==135 and all(r['simulation']['result']=='GOOD_TRAP' for r in standalone)
 for mode in ['ifu','lsu','valid']:
  scores=[r['score'] for r in standalone if r['mode']==mode and r['setting']=='train'];assert len(scores)==20;summary=json.loads((ROOT/'reports'/('E7_'+mode+'_performance.json')).read_text());assert abs(math.exp(sum(map(math.log,scores))/20)-summary['geometric_mean'])<1e-8
 for r in standalone:assert sha(ROOT/r['evidence']/'stdout.log')==r['stdout_sha256'] and sha(ROOT/r['evidence']/'result.json')==r['result_sha256']
 assert len(data['E7_soc_tests']['tests'])==73 and data['E7_soc_tests']['riscv_count']==38 and data['E7_soc_tests']['cpu_count']==35
 assert data['E7_gui']['screenshots']==data['E7_visual_review']['images']
 for f in data['E7_gui']['screenshots']:assert sha(ROOT/f['file'])==f['sha256']
 timer=data['E7_timer']['runs'][-1];assert all(.90<x<1.10 for x in timer['interval_seconds']) and [x['second'] for x in timer['displayed_time_samples']]==[1,2,3,4]
 performance=data['E7_soc_performance']['records'];assert [x['name'] for x in performance]==['baseline_k1','baseline_kmax','area_kmax']
 for r in performance:
  assert r['simulation']['result']=='GOOD_TRAP' and r['simulation']['serial_matches'] and r['k']*25<=r['synthesis_frequency_mhz'];assert sha(ROOT/r['evidence']/'stdout.log')==r['stdout_sha256']
 mark(['E7-O002'],'NOT_SELECTED_OPTIONAL',['E/E7/NOTES.md','reports/E7_standalone.json','reports/E7_soc_performance.json'],'The optional roughly10hour fullarchbenchSoCsweep is notselected. All21test/20trainprogramsrunineachstandalonevariant; requiredSoCblockchaintrainsrunatall3selectedoperatingpoints.')
 mark(['E7-O003'],'PASS_DOCUMENTED',['E/E7/NOTES.md','reports/E7_soc_performance.json'],'Measuredk1/kmaxandarearesults separateCPUfrequencyfrom25MHzperipheral/PSRAMlatency; integerMarksroundingandmin-timedifferencesreported, nofrequency-onlyperformanceclaim.')
 records={r['id']:r for r in json.loads((ROOT/'reports/E_remaining_results.json').read_text())['records'] if r['id'].startswith('E7-')};assert len(records)==35
 for i in range(1,31):assert records[f'E7-M{i:03}']['status'].startswith('PASS')
 # Failed early calibration attempts used the SoC AM's otherwise unused NPC
 # coefficient. Restore its normal default only after all SoC cases have ended.
 header=SOFT/'abstract-machine/am/src/riscv/npc/e7_config.h';text=header.read_text();updated=re.sub(r'#define NPC_CPU_HZ \d+u','#define NPC_CPU_HZ 100000000u',text);assert '#define SOC_CPU_HZ 25000000u' in updated
 if updated!=text:
  save=ROOT/'artifacts/E7/final_defaults/e7_config.before.h';save.parent.mkdir(parents=True,exist_ok=True);save.write_text(text);header.write_text(updated)
 snap=ROOT/'E/E7/runtime_snapshot';snap.mkdir(exist_ok=True);files=[]
 for prefix,base,names in [('npc',BENCH7/'npc',['Makefile','csrc/bus_runner.cpp','csrc/soc_runner.cpp','csrc/ref.c','csrc/ref.h','csrc/memory.hpp','vsrc/minirv_bus.sv','vsrc/ysyx_00000000.sv','vsrc/mygpio_top_apb.v']),('soc_am',SOFT/'abstract-machine',['am/src/riscv/npc/trm.c','am/src/riscv/npc/timer.c','am/src/riscv/npc/e7_config.h','tools/minirv/minirv-common.sh','scripts/minirv-ysyxsoc.mk','scripts/platform/npc.mk'])]:
  for n in names:
   source=base/n;target=snap/prefix/n;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target);files.append({'path':str(target.relative_to(ROOT)),'sha256':sha(target)})
 offline=ROOT/'E/E7/offline';offline.mkdir(exist_ok=True)
 for mode in ['ifu','lsu','valid','soc','soc_gui']:source=WORK/'build/E7'/mode/'sim';target=offline/('npc-'+mode+'-linux');shutil.copyfile(source,target);files.append({'path':str(target.relative_to(ROOT)),'sha256':sha(target)})
 now=datetime.datetime.now(datetime.timezone.utc).isoformat();audit={'status':'PASS','stage_complete':True,'timestamp':now,'core_tasks_passed':30,'core_tasks_total':30,'all_scope_items':35,'standalone_program_runs':135,'standalone_fceux_complete_frames_per_mode':2,'official_tests_per_bus_configuration':73,'bus_configurations':7,'soc_official_test_bodies':73,'soc_cold_boot_batch_count':1,'soc_negative_wrong_separate':True,'soc_performance_runs':3,'gui_visual_review':'PASS','timer_platform':'standalonevalidNPC','timer_intervals_seconds':timer['interval_seconds'],'snapshot':files,'limits':['Localqualificationonly;notofficialcourseadmission','SoCofficialtestsbatchedwithallocatedobjectsectionsunchanged;not73coldboots','Clockratiofunctionaltestsarenotanalogmetastabilityproof','Synthesisfrequency/costareprelayoutTTandcoursehypothetical;finalphysicalsignoffbelongsE8','RealSoCdateprintingwasabout1.7s/line;one-secondRTCdemonstrationusesoriginaltestonstandaloneNPC']};dump(ROOT/'reports/E7_AUDIT.json',audit)
 state=ROOT/'config/task_status.json';d=json.loads(state.read_text());backup=ROOT/'config/history'/str(time.time_ns());backup.mkdir(parents=True);shutil.copyfile(state,backup/state.name)
 for task in d['tasks']:
  if task['id'] in records:r=records[task['id']];task.update(status=r['status'],implementation_status=r['status'],evidence=r['evidence'],result_details=r['details'],updated=now)
 d.update(current_stage='E8',stage_status='IN_PROGRESS',next_stage='E8 physical signoff, E9 scope reconciliation and whole-E packaging');dump(state,d)
 lines=['# E7 验收报告','','30 项必做工程任务已完成本地验收；可选的完整 SoC archbench 长时扫描未选择。','', '[原理、方法和限制](../E/E7/NOTES.md) · [机器审计](E7_AUDIT.json) · [真实虚拟板截图](../artifacts/E7/gui/completed.png) · [73 项 SoC 测试](E7_SOC_TESTS.md)','', '| 结构 | hello 周期 | 提交指令 | IPC | 20 项 train 几何平均分（100 MHz） |','|---|---:|---:|---:|---:|']
 for mode in ['ifu','lsu','valid']:
  s=json.loads((ROOT/'reports'/('E7_'+mode+'_performance.json')).read_text());h=s['hello'];lines.append(f'| {mode} | {h["cycles"]} | {h["instructions"]} | {h["ipc"]:.6f} | {s["geometric_mean"]:.3f} |')
 lines+=['','每种结构还运行 21 项 archbench test、3 个内核 benchmark、hello 及两个完整 FCEUX 字符帧。7 组固定/随机延迟各通过 73 项官方测试，读数据翻转和重复写负对照均拒绝。','', '| SoC 场景 | CPU / 外设 MHz | k | train 最短时间（s） | Marks | 应用 IPC |','|---|---:|---:|---:|---:|---:|']
 for r in performance:lines.append(f'| {r["name"]} | {r["cpu_frequency_hz"]/1e6:g} / 25 | {r["k"]} | {r["min_time_us"]/1e6:.6f} | {r["score"]} | {r["simulation"]["application_ipc"]:.6f} |')
 lines+=['','这里的时间由 mcycle 与指定频率换算，软件校验、逐指令 DiffTest、实际 TX 解码和时钟波形同时检查。Marks 是粗粒度整数，比较小差异时应查看最短时间。','', 'BALANCE 综合报告 130 MHz、9915 µm²；AREA 为 89 MHz、9306 µm²。AREA 在原 100 MHz 约束下未闭合，采用 75 MHz 的合法整数倍用于本阶段比较。60% 利用率和 30000 元/mm² 的教学模型给出约 495.75 元、465.30 元，均不包含 SoC、封装和测试等成本。','', '原始 RTC 测试在独立 NPC 上的三个输出间隔为 '+', '.join(f'{x:.3f}s' for x in timer['interval_seconds'])+'。真实 SoC 的计数器也逐周期核对，但完整日期打印约需 1.7 秒；两种观察分别保存。','', '| ID | 状态 | 要求 |','|---|---|---|']
 tasks={x['id']:x for x in d['tasks']}
 for ident,r in sorted(records.items()):lines.append('| '+ident+' | '+r['status']+' | '+tasks[ident]['requirement'].replace('|','/').replace('\n',' ')+' |')
 (ROOT/'reports/E7_REPORT.md').write_text('\n'.join(lines)+'\n');print('E7_ALL_REQUIRED_ENGINEERING_TASKS_COMPLETE',flush=True)
if __name__=='__main__':main()
