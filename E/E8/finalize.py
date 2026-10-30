from pathlib import Path,PurePosixPath
import sys,tarfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
 names=['E8_front_audit','E8_final_mapped','E8_area_functional','E8_icarus14_controls','E8_signoff_export','E8_gui','E8_visual_review','E8_physical_preflight'];data={n:json.loads((ROOT/'reports'/(n+'.json')).read_text()) for n in names};assert all(x['status'].startswith('PASS') for x in data.values())
 export=data['E8_signoff_export'];summary=export['summary'];assert len(summary['sta_matrix'])==13 and summary['checks']['home_checklist']['blocked']==0 and summary['checks']['home_checklist']['unavailable']==0
 archive=ROOT/export['archive'];assert sha(archive)==export['sha256'];manifest=json.loads((ROOT/'E/E8/signoff/manifest.json').read_text());initial=next(x for x in manifest['files'] if x['role']=='initial.verilog');synthesis=json.loads((ROOT/'reports/E7_synthesis.json').read_text());baseline=next(x for x in synthesis['variants'] if x['variant']=='baseline');assert initial['sha256']==baseline['netlist_sha256']
 matrix={c['qor_summary']:c for c in summary['sta_matrix']};corners=[];parameters=None
 with tarfile.open(archive,'r|gz') as stream:
  for member in stream:
   if not member.isfile():continue
   relative='/'.join(PurePosixPath(member.name).parts[1:])
   if relative in matrix:
    value=json.load(stream.extractfile(member));assert value['path_groups'];s=value['summary'];assert s['setup']['wns']>=0 and s['hold']['wns']>=0 and s['setup']['tns']==0 and s['hold']['tns']==0 and s['setup']['nvp']==0 and s['hold']['nvp']==0;corners.append({**matrix[relative],**s})
   if relative=='initial/parameters.json':parameters=json.load(stream.extractfile(member))
 assert len(corners)==13 and parameters['Frequency max [MHz]']==50
 spefs=[x for x in manifest['files'] if x['destination'].endswith(('.spef','.spef.gz'))];assert len(spefs)==9
 metrics={x['id']:x for x in summary['qor_metrics']['metrics']};assert metrics['drc_count']['value']==0
 physical=WORK/'physical/cpu_baseline';gates={}
 for name in ['drc','lvs','RCX','sta','Harden']:
  value=json.loads((physical/(name+'_ecc/analysis/qor_summary.json')).read_text());assert value['analysis_status']=='valid' and value['quality_status']=='pass'
  for gate in value['gates']:assert gate['state']=='pass';gates[gate['id']]=gate
 for row in data['E8_gui']['images']:assert sha(ROOT/row['path'])==row['sha256']
 flow=json.loads((physical/'home/flow.json').read_text());assert len(flow['steps'])==12 and all(x['state']=='Success' for x in flow['steps'])
 mark(['E8-M010'],'PASS',['reports/E8_signoff_export.json','reports/E8_gui.json','reports/E8_visual_review.json','E/E8/signoff/cpu-baseline-signoff.tar.gz','E/E8/signoff/layout.png','artifacts/E8/physical/cpu_baseline'],'ActualCPU12-stepphysicalflow,DRC0/LVS0,13cornerSTAsetup/holdclosedat50MHz,9validSPEFs;actualengineexport210membershashverified;realECOSdashboard/checklist/native2Dviewinspected. Onlyoptionalno-macrolocationwarning.')
 records={r['id']:r for r in json.loads((ROOT/'reports/E_remaining_results.json').read_text())['records'] if r['id'].startswith('E8-')};assert len(records)==16
 for i in range(1,11):assert records[f'E8-M{i:03}']['status'].startswith('PASS')
 audit={'status':'PASS','stage_complete':True,'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'core_tasks_passed':10,'core_tasks_total':10,'all_scope_items':16,'top_module':'ysyx_00000000','candidate':'BALANCE3baseline','constraint_frequency_mhz':50,'die_area_um2':metrics['die_area']['value'],'core_area_um2':metrics['core_area']['value'],'minimum_setup_wns_ns':min(x['setup']['wns'] for x in corners),'minimum_hold_wns_ns':min(x['hold']['wns'] for x in corners),'timing_corners':corners,'spef_files':len(spefs),'quality_gates':gates,'flow':flow,'signoff_archive':export['archive'],'signoff_sha256':export['sha256'],'verified_export_files':len(export['verified_files']),'gui':'PASS_NATIVE_2D_CPU_CANVAS','source_netlist_sha256':initial['sha256'],'limits':['LocalchecksunderlockedICsprout55libraries,SDC,andRCXparasitics;notmeasuredsilicon','50MHzconstraintclosed;GUI58MHzisareportedestimate,notaseparatelyrerun58MHzconstraint','Functionalnetlistprogramtestsareno-SDF;timingqualificationcomesfromseparateSTA','Optionalmaximum-utilizationsearch,Chisel-specificnotes,embeddedAIagent,and3Dviewnotselected']};dump(ROOT/'reports/E8_AUDIT.json',audit)
 p=ROOT/'config/task_status.json';state=json.loads(p.read_text());history=ROOT/'config/history'/str(time.time_ns());history.mkdir(parents=True);shutil.copyfile(p,history/p.name)
 for task in state['tasks']:
  if task['id'] in records:r=records[task['id']];task.update(status=r['status'],implementation_status=r['status'],evidence=r['evidence'],result_details=r['details'],updated=audit['timestamp'])
 state.update(current_stage='E9',stage_status='IN_PROGRESS',next_stage='Personal-scope exclusions and whole-E evidence/package audit');dump(p,state)
 lines=['# E8 验收报告','','10 项必做工程任务已完成本地验收。最终 CPU 在 **50 MHz 约束**下通过全流程及签核检查，DRC、LVS 均为 **0 违规**。','', '[完整签核包](../E/E8/signoff/cpu-baseline-signoff.tar.gz) · [版图](../E/E8/signoff/layout.png) · [ECOS 实际界面](../artifacts/E8/gui/dashboard_ready.png) · [原生二维查看器](../artifacts/E8/gui/native_micrometers.png) · [方法与限制](../E/E8/NOTES.md)','', '| 项目 | 结果 |','|---|---:|',f'| die 面积 | {audit["die_area_um2"]} µm² |',f'| core 面积 | {audit["core_area_um2"]} µm² |',f'| 最差 setup WNS | {audit["minimum_setup_wns_ns"]} ns |',f'| 最差 hold WNS | {audit["minimum_hold_wns_ns"]} ns |','| setup / hold TNS | 0 / 0 ns |','| 时序角 | 13 |','| SPEF 文件 | 9 |','| 签核包已核对文件 | 210 |','', '界面显示的 58 MHz 是工具报告的频率估计；本次实际闭合约束为 50 MHz。最终布线输入网表与已经通过功能仿真的 BALANCE 网表逐字节一致。','', '完整 microbench 在 Icarus 14 原始 UDP 标准单元模型中以 22,129,163 周期、GOOD_TRAP 结束；同样的程序和周期数也在 RTL 与 Verilator 网表环境中通过。AREA 网表另通过完整 Verilator hello/microbench，用于 E7 策略比较。','', '签核检查仅保留无宏单元时允许的 `config.macro_locations` 提示，未绕过任何阻塞项。ECOS 原生二维查看器使用工具提供的 CPU 绘制选项，实际查看了全部 20 个图层和 382,252 个绘图对象。','', '| 工艺库角 | 温度 | RC 角 | setup WNS/ns | hold WNS/ns |','|---|---:|---|---:|---:|']
 for c in corners:lines.append(f'| {c["lib_corner"]} | {c["temperature"]} | {c["rcx_corner"]} | {c["setup"]["wns"]} | {c["hold"]["wns"]} |')
 lines+=['','| ID | 状态 |','|---|---|']+[f'| {i} | {r["status"]} |' for i,r in sorted(records.items())]
 (ROOT/'reports/E8_REPORT.md').write_text('\n'.join(lines)+'\n');print('E8_ALL_REQUIRED_ENGINEERING_TASKS_COMPLETE',flush=True)
if __name__=='__main__':main()
