"""Regenerate the pinned real framework with Config.sdramUseAXI enabled."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from resource_policy import generation_environment

def main():
    origin=Path('/home/USER/c-stage/soc-generation/ysyxSoC');soc=WORK/'soc-generation/ysyxSoC'
    original_top=origin/'src/Top.scala';before=sha(original_top)
    if not soc.exists():
        soc.parent.mkdir(parents=True,exist_ok=True)
        shutil.copytree(origin,soc,symlinks=True,ignore=shutil.ignore_patterns('.git','build','__pycache__'))
    top=soc/'src/Top.scala';old=top.read_text()
    assert old.count('def sdramUseAXI: Boolean = false')+old.count('def sdramUseAXI: Boolean = true')==1
    top.write_text(old.replace('def sdramUseAXI: Boolean = false','def sdramUseAXI: Boolean = true'))
    toolchain=json.loads((ROOT/'reports/C5_toolchain.json').read_text());env=generation_environment(toolchain['environment'])
    for k in ['MILL_JVM_OPTS','JAVA_OPTS','JAVA_TOOL_OPTIONS']:
        if k in env:env[k]=env[k].replace('-XX:ActiveProcessorCount=2','-XX:ActiveProcessorCount=4')
    for row in toolchain['binaries']:assert sha(row['path'])==row['sha256']
    manifest=[{'path':str(p),'sha256':sha(p)} for p in sorted((soc/'src').rglob('*.scala'))]
    dest=ROOT/'B/soc/generation/axi';dest.mkdir(parents=True,exist_ok=True)
    dump(dest/'inputs.json',{'files':manifest,'C_top_sha256':before,'tools':'reports/C5_toolchain.json','scope':'Pinned already dev-init-completed framework copied; one Config switch. Reuses local compiled dependency caches and pinned tools.'})
    generated=soc/'build/ysyxSoCFull.v';budget=ROOT/'artifacts/B3/axi-generation/budget.json'
    run('B3/axi-generation',['python3',ROOT/'B/runtime/budget_exec.py','--report',budget,'--','make','-j4','verilog'],cwd=soc,env=env,inputs=[top,soc/'Makefile',soc/'build.sc',dest/'inputs.json'],outputs=[generated,budget],timeout=1800,resume=True)
    text=generated.read_text();assert 'sdram_top_axi ' in text and 'axi4_delayer ' in text and 'sdram_top_apb ' not in text
    assert sha(original_top)==before
    output=dest/'ysyxSoCFull.v';shutil.copyfile(generated,output);shutil.copyfile(top,dest/'Top.scala')
    dump(ROOT/'reports/B3_axi_generation.json',{'status':'PASS_ACTUAL_GENERATION','cwd':str(soc),'generated':str(output),'sha256':sha(output),'bytes':output.stat().st_size,'configuration':'sdramUseAXI=true,32-bit Edge32BitConfig,ChipLink=false','inputs':manifest,'C_top_preserved_sha256':before,'scope':'Actual make/Mill/Chisel/firtool generation completed. Peripheral behavior and integration are validated separately.'})
    print('B3_AXI_SOC_GENERATION_PASS',output.stat().st_size,flush=True)

if __name__=='__main__':main()
