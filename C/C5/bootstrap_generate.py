"""Bounded actual make verilog, plus an injected Scala syntax-error control."""
from pathlib import Path
import sys,json,subprocess,shutil,os,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from resource_policy import POLICY_PATH, load_policy, generation_environment
SOC=WORK/'soc-generation/ysyxSoC';D=ROOT/'C/C5/generation'

def source_manifest():
    files=[SOC/'Makefile',SOC/'build.sc',SOC/'.mill-version',SOC/'patch/rocket-chip.patch']
    files += sorted((SOC/'src').rglob('*.scala'))
    files += sorted((SOC/'rocket-chip').rglob('*.sc'))
    files += sorted((SOC/'rocket-chip/src').rglob('*.scala'))
    for sub in ['cde','diplomacy','hardfloat']:
        files+=sorted((SOC/'rocket-chip/dependencies'/sub).rglob('*.scala'))
    return [{'path':str(p),'sha256':sha(p)} for p in dict.fromkeys(files)]

def main():
    D.mkdir(parents=True,exist_ok=True);tools=json.loads((ROOT/'reports/C5_toolchain.json').read_text());env=generation_environment(tools['environment'])
    for row in tools['binaries']:assert sha(row['path'])==row['sha256']
    command=['/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe','-NoProfile','-NonInteractive','-Command','(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory']
    free=int(subprocess.check_output(command,text=True).strip());assert free>=load_policy()['windows_start_available_mib']*1024,free
    guard=D/'budget_exec.py'
    assert guard.is_file(), guard
    before=source_manifest();dump(D/'inputs.json',{'files':before,'toolchain_sha256':sha(ROOT/'reports/C5_toolchain.json'),'source_lock_sha256':sha(ROOT/'reports/C5_source_lock.json'),'environment':env,'windows_free_kib':free,'windows_memory_command':command})
    output=SOC/'build/ysyxSoCFull.v';budget=ROOT/'artifacts/C5/bootstrap/generate/budget.json'
    cmd=['python3',guard,'--metric','pss','--report',budget,'--','taskset','-c','0,1','make','-j1','verilog']
    print('C5_ACTUAL_GENERATION_START',free,'KiB Windows free',flush=True)
    run('C5/bootstrap/generate',cmd,cwd=SOC,env=env,inputs=[POLICY_PATH,ROOT/'C/runtime/budget_exec.py',ROOT/'C/runtime/resource_policy.py',guard,D/'inputs.json',SOC/'Makefile',SOC/'build.sc',SOC/'.mill-version',SOC/'patch/rocket-chip.patch'],outputs=[output],timeout=1800)
    text=output.read_text();assert re.search(r'\bmodule\s+ysyxSoCFull\b',text) and re.search(r'\bmodule\s+ysyxSoCTop\b',text)
    modules=re.findall(r'^module\s+(\w+)',text,re.M);assert len(modules)>10
    assert source_manifest()==before
    out=D/'ysyxSoCFull.v';shutil.copyfile(output,out);goodsha=sha(output)
    # Force the real generator to reject invalid source, keeping good output unchanged.
    bad=D/'InjectedSyntaxError.scala';bad.write_text('package ysyx\nobject InjectedSyntaxError { val = }\n')
    injected=SOC/'src/InjectedSyntaxError.scala';assert not injected.exists();shutil.copyfile(bad,injected)
    try:
        negative_budget=ROOT/'artifacts/C5/bootstrap/generate-negative/budget.json'
        negative=['python3',guard,'--metric','pss','--report',negative_budget,'--','taskset','-c','0,1','make','-j1','verilog']
        stdout,stderr,record=run('C5/bootstrap/generate-negative',negative,cwd=SOC,env=env,inputs=[POLICY_PATH,ROOT/'C/runtime/budget_exec.py',ROOT/'C/runtime/resource_policy.py',guard,bad,SOC/'Makefile',SOC/'build.sc'],expected=(2,),timeout=600)
        combined=stdout+stderr;assert 'InjectedSyntaxError.scala' in combined and 'error' in combined.lower() and 'expected' in combined.lower()
    finally:
        assert injected.parent==SOC/'src';injected.unlink()
    assert source_manifest()==before and sha(output)==goodsha
    budget_result=json.loads(budget.read_text());assert budget_result['status']=='PASS'
    dump(ROOT/'reports/C5_generation.json',{'status':'PASS_ACTUAL_FRAMEWORK_GENERATION','source_lock':'reports/C5_source_lock.json','tools':'reports/C5_toolchain.json','command':['make','-j1','verilog'],'cwd':str(SOC),'environment':env,'generated':{'path':str(output),'copy':str(out),'bytes':output.stat().st_size,'sha256':goodsha,'module_count':len(modules),'modules':modules},'resource_budget':budget_result,'source_files':before,'negative_control':{'status':'PASS_REJECTED','injected_source':str(bad),'make_exit':record['exit_code'],'diagnostic':'Real Scala parser reports InjectedSyntaxError.scala and expected token error','source_restored':True,'good_output_preserved':True},'scope':'Actual pinned complete ysyx6 framework dev-init and Mill/Chisel/firtool generation. This does not qualify the future NPC integration, missing peripheral models or ChipLink behavior.'})
    print('C5_ACTUAL_GENERATION_PASS',len(modules),output.stat().st_size,flush=True)

if __name__=='__main__':main()
