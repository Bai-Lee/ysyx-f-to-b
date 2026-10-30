"""C-only replay of the established UART/RTC/CC0-ROM device tests."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def prepare():
    d=ROOT/'C/C2';base=WORK/'c2-npc-apps';base.mkdir(exist_ok=True)
    for source,target in [(BENCH/'am-kernels/kernels/hello',base/'hello'),(BENCH/'am-kernels/tests/am-tests',base/'am-tests'),(BENCH/'fceux-am',base/'fceux-am')]:
        if not target.exists():shutil.copytree(source,target,symlinks=True,ignore=shutil.ignore_patterns('build','.git'))
    rom=d/'homebrew';rom.mkdir(exist_ok=True)
    for name in ('interaction.nes','symbols.json','provenance.json'):
        src=ROOT/'D/D8/homebrew'/name;dst=rom/name
        if src.exists():shutil.copyfile(src,dst)
    source=ROOT/'D/D8/fceux_verify.py';text=source.read_text()
    text=text.replace("ROOT/'D/D8/homebrew/", "ROOT/'C/C2/homebrew/")
    text=text.replace("ROOT/'artifacts/D8/", "ROOT/'artifacts/C2/")
    text=text.replace("ROOT/'reports/D8_fceux", "ROOT/'reports/C2_fceux")
    text=text.replace("'D8/fceux/", "'C2/fceux/")
    text=text.replace("BENCH/'fceux-am", "WORK/'c2-npc-apps/fceux-am")
    text=text.replace("Path(json.loads((ROOT/'reports/D8_reference.json').read_text())['shared_object'])", "WORK/'nemu-ref/build/riscv32-nemu-interpreter-so'")
    text=text.replace('# Derived from E/E6/fceux_verify.py for an isolated D-stage execution.', '# C replay derived from the accepted D FCEUX harness; actual source and byte hashes retained.')
    (d/'fceux_verify.py').write_text(text)
    shutil.copyfile(ROOT/'D/D8/timer_trm_only.c',d/'timer_trm_only.c')
    (d/'timer_menu.mk').write_text('NAME = amtest\nSRCS = $(shell find src/ -name "*.[cS]")\nSRCS += '+str(d/'timer_trm_only.c')+'\ninclude $(AM_HOME)/Makefile\n')
    dump(ROOT/'reports/C2_device_replay_sources.json',{'status':'PASS_SOURCE_SETUP','source_harness':str(source),'source_sha256':sha(source),'C_harness_sha256':sha(d/'fceux_verify.py'),'rom_sha256':sha(rom/'interaction.nes'),'scope':'Project-authored CC0 ROM and established driver probes are reused and executed anew in isolated C apps. No original D files edited.'})
    return base

def main():
    base=prepare();exe=BENCH/'npc/build/sim';ref=WORK/'nemu-ref/build/riscv32-nemu-interpreter-so';am=BENCH/'abstract-machine';d=ROOT/'C/C2'
    inputs=[exe,ref,am/'am/src/riscv/npc/trm.c',am/'am/src/riscv/npc/timer.c',am/'scripts/platform/npc.mk']
    cwd=base/'hello';report=cwd/'build/hello-riscv32e-npc.bin.npc.json'
    o,e,_=run('C2/npc/hello',['make','-j1','ARCH=riscv32e-npc','run','mainargs=C2-UART','NPC_ARGS=--uart-random'],cwd=cwd,inputs=[*inputs,cwd/'hello.c',cwd/'Makefile'],outputs=[report,cwd/'build/hello-riscv32e-npc.elf'],timeout=120)
    hello=json.loads(report.read_text());assert 'Hello, AbstractMachine!' in o and 'C2-UART' in o and hello['result']=='GOOD_TRAP' and hello['diff_checked']+hello['device_sync_checked']==hello['instructions']
    cwd=base/'am-tests';report=cwd/'build/amtest-riscv32e-npc.bin.npc.json';sources=sorted(p for p in (cwd/'src').rglob('*') if p.suffix in ('.c','.S'))
    command=['make','-j1','-f',d/'timer_menu.mk','ARCH=riscv32e-npc','run']
    o,e,_=run('C2/npc/timer',command+['mainargs=t',"NPC_ARGS=--wall-timer --until-output 'seconds).' --until-count 2"],cwd=cwd,inputs=[*inputs,d/'timer_menu.mk',d/'timer_trm_only.c',*sources],outputs=[report,cwd/'build/amtest-riscv32e-npc.elf'],timeout=120)
    timer=json.loads(report.read_text());assert timer['result']=='BOUNDED_OUTPUT_OBSERVATION' and all(f'{n} second' in o for n in (1,2,3))
    assert timer['diff_checked']+timer['device_sync_checked']==timer['instructions']
    o,e,_=run('C2/npc/cte_unavailable',command+['mainargs=i'],cwd=cwd,inputs=[*inputs,d/'timer_trm_only.c'],outputs=[report],expected=(2,),timeout=30)
    assert 'D_STAGE_NO_CTE' in o and json.loads(report.read_text())['result']=='BAD_TRAP'
    run('C2/fceux/suite',['python3',d/'fceux_verify.py'],inputs=[d/'fceux_verify.py',d/'homebrew/interaction.nes',exe,ref],timeout=1200)
    dump(ROOT/'reports/C2_npc_io.json',{'status':'PASS_BOUNDED_IO','hello':hello,'timer':timer,'timer_observed_seconds':[1,2,3],'unsupported_cte_negative':'BAD_TRAP and make=2; C2 TRM menu link support only, replaced by real traps later in C5.','fceux_native':'reports/C2_fceux_native.json','fceux_ascii':'reports/C2_fceux_ascii.json','scope':'C2 UART at0x10000000, existing readiness register, host-monotonic RTC model, real NEMU shared-REF comparisons on ordinary instructions. Native SDL audio/video/key and NPC two complete ASCII frames; no physical loudspeaker or infinite gameplay claim.'})
    print('C2_NPC_AND_FCEUX_PASS',flush=True)

if __name__=='__main__':main()
