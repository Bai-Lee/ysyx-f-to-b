from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

REPORT_CODE=r'''
void monitor_write_report(void) {
  if (!result_file) return;
  extern uint64_t g_nr_guest_inst, g_diff_checked, g_diff_skipped;
  extern bool g_diff_enabled;
  FILE *f = fopen(result_file, "w");
  Assert(f, "cannot create result report");
  const char *result = nemu_state.state == NEMU_END ? (nemu_state.halt_ret == 0 ? "GOOD_TRAP" : "BAD_TRAP") : nemu_state.state == NEMU_ABORT ? "ABORT" : nemu_state.state == NEMU_QUIT ? "QUIT" : "STOP";
  fprintf(f, "{\"result\":\"%s\",\"pc\":%u,\"halt_pc\":%u,\"halt_ret\":%u,\"instructions\":%" PRIu64 ",\"diff_enabled\":%s,\"diff_checked\":%" PRIu64 ",\"diff_skipped\":%" PRIu64 ",\"gpr\":[", result, cpu.pc, nemu_state.halt_pc, nemu_state.halt_ret, g_nr_guest_inst, g_diff_enabled ? "true" : "false", g_diff_checked, g_diff_skipped);
  for (int i = 0; i < 32; i++) fprintf(f, "%s%u", i ? "," : "", cpu.gpr[i]);
  fputs("]}\n", f);
  assert(fclose(f) == 0);
}
'''
def main():
    n=BENCH/'nemu';am=BENCH/'abstract-machine';changed=[]
    p=n/'src/cpu/difftest/dut.c';text=p.read_text()
    if 'g_diff_checked' not in text:
        text=text.replace('#ifdef CONFIG_DIFFTEST','uint64_t g_diff_checked = 0, g_diff_skipped = 0;\nbool g_diff_enabled = false;\n\n#ifdef CONFIG_DIFFTEST',1)
        text=text.replace('  assert(ref_so_file != NULL);','  assert(ref_so_file != NULL);\n  if (strcmp(ref_so_file, "none") == 0) { puts("DIFFTEST_DISABLED_EXPLICITLY"); return; }\n  g_diff_enabled = true;')
        text=text.replace('static void checkregs(CPU_state *ref, vaddr_t pc) {','static void checkregs(CPU_state *ref, vaddr_t pc) {\n  g_diff_checked++;')
        text=text.replace('void difftest_step(vaddr_t pc, vaddr_t npc) {','void difftest_step(vaddr_t pc, vaddr_t npc) {\n  if (!g_diff_enabled) return;')
        text=text.replace('  if (is_skip_ref) {','  if (is_skip_ref) {\n    g_diff_skipped++;');p.write_text(text)
    changed.append(p)
    p=n/'src/monitor/monitor.c';text=p.read_text()
    if 'monitor_write_report' not in text:
        text=text.replace('static char *log_file = NULL;','static char *log_file = NULL;\nstatic char *result_file = NULL;')
        text=text.replace('    {"batch"','    {"report", required_argument, NULL, \'r\'},\n    {"batch"')
        text=text.replace('"-bhl:d:p:"','"-bhl:d:p:r:"')
        text=text.replace("      case 'b':", "      case 'r': result_file = optarg; break;\n      case 'b':")
        text=text.replace('static long load_img() {',REPORT_CODE+'\nstatic long load_img() {',1);p.write_text(text)
    changed.append(p)
    p=n/'src/nemu-main.c';text=p.read_text()
    if 'monitor_write_report' not in text:text=text.replace('  return is_exit_status_bad();','  extern void monitor_write_report(void);\n  monitor_write_report();\n  return is_exit_status_bad();');p.write_text(text)
    changed.append(p)
    p=am/'scripts/platform/nemu.mk';text=p.read_text();text=text.replace('$(shell dirname $(IMAGE).elf)/nemu-log.txt','$(IMAGE).nemu.log')
    text=text.replace('run ARGS="$(NEMUFLAGS)"','run ARGS="-b --report=$(IMAGE).nemu.json $(NEMUFLAGS)"');p.write_text(text);changed.append(p)
    env=json.loads((ROOT/'reports/D5_setup.json').read_text())['environment'];exe=n/'build/riscv32-nemu-interpreter'
    run('D5/nemu/report_build',['make','-j1'],cwd=n,env=env,inputs=changed,outputs=[exe],timeout=300)
    ref=n/'tools/spike-diff/build/riscv32-spike-so';out=WORK/'D5/builtin-report.json'
    _,_,_=run('D5/nemu/report_smoke',[exe,'-b','-d',ref,'--report',out],cwd=n,env=env,inputs=[exe,ref],outputs=[out]);d=json.loads(out.read_text());assert d['result']=='GOOD_TRAP' and d['diff_enabled'] and d['diff_checked']+d['diff_skipped']==d['instructions']==4
    dump(ROOT/'reports/D5_report_support.json',{'status':'PASS','report_example':d,'executable':str(exe),'sha256':sha(exe),'spike':str(ref),'spike_sha256':sha(ref),'environment':env,'explicit_no_diff':'-d none is available for separately labelled EEI cases; normal AM runs always supply Spike.'})

if __name__=='__main__':main()
