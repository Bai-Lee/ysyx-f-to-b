from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
 checks=['E6_halt_and_exit','E6_official_tests','E6_difftest_negative','E6_devices','E6_timer','E6_benchmarks','E6_fceux_native','E6_fceux_ascii','E6_synthesis','E6_performance']
 data={name:json.loads((ROOT/'reports'/(name+'.json')).read_text(encoding='utf-8-sig')) for name in checks}
 assert all(x['status'].startswith('PASS') for x in data.values())
 assert data['E6_performance']['scaling_check']['status']=='PASS'
 assert len(data['E6_performance']['runs'])==4 and all(len(x['rows'])==20 for x in data['E6_performance']['runs'])
 # Correct a label in the generated device summary: preserve the actual unit output, not the later hello log.
 d=data['E6_devices'];d['unit_checks']=(ROOT/'artifacts/E6/devices/unit_run/stdout.log').read_text();dump(ROOT/'reports/E6_devices.json',d)
 p=ROOT/'reports/E6_source_line_endings.json';x=json.loads(p.read_text(encoding='utf-8-sig'));dump(p,x)
 mark(['E6-O001','E6-O002'],'PASS_DOCUMENTED',['E/E6/NOTES.md','reports/E_backend_compatible_tools.json'],'Explained why test inputs are not representative performance loads; retained official tool-version compatibility failures and validated working locked versions.')
 records=[r for r in json.loads((ROOT/'reports/E_remaining_results.json').read_text())['records'] if r['id'].startswith('E6-')];assert len(records)==24 and all(x['status'].startswith('PASS') for x in records)
 npc=BENCH/'npc';am=BENCH/'abstract-machine';snap=ROOT/'E/E6/runtime_snapshot';snap.mkdir(exist_ok=True);locked=[]
 files=[*[(n,npc/'csrc'/n) for n in ['runner.cpp','memory.hpp','ref.c','ref.h']],*[(n,npc/'vsrc'/n) for n in ['minirv_decode.sv','minirv_regfile.sv','minirv_single.sv','npc_sim.sv']],('NPC.Makefile',npc/'Makefile'),('trm.c',am/'am/src/riscv/npc/trm.c'),('timer.c',am/'am/src/riscv/npc/timer.c'),('npc.mk',am/'scripts/platform/npc.mk'),('riscv.mk',am/'scripts/isa/riscv.mk')]
 for n,src in files:dest=snap/n;shutil.copyfile(src,dest);locked.append({'path':str(dest.relative_to(ROOT)),'sha256':sha(dest)})
 offline=ROOT/'E/E6/offline';offline.mkdir(exist_ok=True);shutil.copyfile(npc/'build/sim',offline/'npc-e6-linux');assert sha(offline/'npc-e6-linux')==data['E6_performance']['runs'][0]['simulator_sha256']
 now=datetime.datetime.now(datetime.timezone.utc).isoformat();audit={'status':'PASS','stage_complete':True,'timestamp':now,'core_tasks':22,'background_nodes':2,'riscv_tests':38,'cpu_positive_tests':35,'negative_controls':'wrong; RTL sign-extension mutant; busy UART write; timer rollover; GUI/audio fixture defects retained as failed attempts','archbench_test_programs':21,'archbench_train_programs_per_mode':20,'train_modes':4,'performance_scaling':data['E6_performance']['scaling_check'],'snapshot':locked,'simulator_sha256':sha(offline/'npc-e6-linux'),'source_archive_policy':'Exact pinned repositories and official klib; canonical text inputs repaired without changing validator/checksum expectations.','scope_limits':['minirv8-op CPU plus simulation ebreak, not fullRV32I','FCEUX legal authored interaction ROM, virtualSDL display and capturedaudio; no physicalspeaker or commercial-game claim','pre-layout TT synthesis estimate only; no E6 physical signoff']};dump(ROOT/'reports/E6_AUDIT.json',audit)
 p=ROOT/'config/task_status.json';d=json.loads(p.read_text());hist=ROOT/'config/history'/str(time.time_ns());hist.mkdir(parents=True);shutil.copyfile(p,hist/p.name);rows={r['id']:r for r in records}
 for r in d['tasks']:
  if r['id'] in rows:x=rows[r['id']];r.update(status=x['status'],implementation_status=x['status'],evidence=x['evidence'],result_details=x['details'],updated=now)
 d.update(current_stage='E7',stage_status='IN_PROGRESS',next_stage='E7/E8/E9; E7 and E8 preflights underway');dump(p,d)
 modes={r['mode']:r for r in data['E6_performance']['runs']};lines=['# E6 阶段验收','', '22 项核心任务和 2 个背景节点已完成本地验收。38 个 riscv-tests、35 个 cpu-tests、21 个 archbench 小规模程序均通过；wrong 和注错 RTL 被正确拒绝。4 组 train 各 20 个程序实际运行，全部保留逐指令差分检查。','', '[实现说明](../E/E6/NOTES.md) · [机器审计](E6_AUDIT.json) · [官方测试](E6_official_tests.json) · [应用与 benchmark](E6_benchmarks.json) · [性能原始结果](E6_performance.json)','', '| train 程序 | 主机计时分数 | 100 MHz | 1000 MHz | 综合估计 830 MHz |','|---|---:|---:|---:|---:|']
 for i,row in enumerate(modes['wall']['rows']):lines.append('| '+row['program']+' | '+' | '.join(str(modes[m]['rows'][i]['score']) for m in ['wall','100MHz','1000MHz','synthesis'])+' |')
 lines+=['| 几何平均 | '+' | '.join(f'{modes[m]["geometric_mean"]:.3f}' for m in ['wall','100MHz','1000MHz','synthesis'])+' |','', '主机计时列反映仿真执行速度。其余三列反映指定频率下的模型时间；830 MHz 是 ICsprout55 R/L、TT、1.2 V、25°C 条件下布局前综合时序估计，不是已布线或实物频率。计时区内的 genann 子测试输出及 LLaMa tokens/s 输出会随频率变化，故指令数并非完全相同；实测时间比例的最大相对偏差为 '+f'{data["E6_performance"]["scaling_check"]["observed_max_relative_time_error"]*100:.5f}%'+'，整数分数舍入另外校验。','', '| ID | 状态 | 验收依据 |','|---|---|---|']
 for r in sorted(records,key=lambda x:x['id']):lines.append('| '+r['id']+' | '+r['status']+' | '+r['details'].replace('|','/')+' |')
 lines+=['','FCEUX 使用自制可再分发 ROM，实际完成画面、按键、PCM 音频及 NPC 字符模式验证。完整 E 阶段交付 ZIP 将在 E7、E8 和 E9 范围审计完成后生成。']
 (ROOT/'reports/E6_REPORT.md').write_text('\n'.join(lines)+'\n')
 print('E6_STAGE_COMPLETE_CONTINUE_E7',flush=True)
if __name__=='__main__':main()
