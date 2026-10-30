from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *


def main():
    base=WORK/'c5/workbench';base.mkdir(parents=True,exist_ok=True);am=base/'abstract-machine';source=ROOT/'C/C5/am'
    if not am.exists():shutil.copytree(BENCH/'abstract-machine',am,ignore=shutil.ignore_patterns('.git','build','__pycache__'))
    mapping={'riscv32e-ysyxsoc.mk':'scripts/riscv32e-ysyxsoc.mk','ysyxsoc.mk':'scripts/platform/ysyxsoc.mk',
             'ysyxsoc-mrom.ld':'scripts/ysyxsoc-mrom.ld','ysyxsoc-initial.ld':'scripts/ysyxsoc-initial.ld',
             'start.S':'am/src/riscv/ysyxsoc/start.S','trm.c':'am/src/riscv/ysyxsoc/trm.c','ioe.c':'am/src/riscv/ysyxsoc/ioe.c','lshrdi3.S':'am/src/riscv/ysyxsoc/lshrdi3.S',
             'cte.c':'am/src/riscv/ysyxsoc/cte.c','trap.S':'am/src/riscv/ysyxsoc/trap.S','riscv.h':'am/include/arch/riscv.h','ps2.h':'am/src/riscv/ysyxsoc/ps2.h'}
    for filename,relative in mapping.items():
        target=am/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source/filename,target)
    (am/'scripts/ysyxsoc-flash.ld').write_text((source/'ysyxsoc-mrom.ld').read_text().replace('mrom','flash').replace('0x20000000','0x30000000').replace('LENGTH = 4K','LENGTH = 16M').replace('MROM image exceeds4KiB','Flash image exceeds16MiB'))
    shutil.copyfile(source/'ysyxsoc-psram-data.ld',am/'scripts/ysyxsoc-psram-data.ld')
    template=(source/'ysyxsoc-relocate.ld.in').read_text()
    for target in ['sram','psram']:
        text=template.replace('@TARGET@',target).replace('@HEAP_START@','ORIGIN(psram)' if target=='sram' else 'ALIGN(__bss_end,16)').replace('@TARGET_LIMIT@','ORIGIN(sram)+LENGTH(sram)-2048' if target=='sram' else 'ORIGIN(psram)+LENGTH(psram)').replace('@HEAP_END@','ORIGIN(psram)+LENGTH(psram)').replace('@SDRAM_MB@','32')
        (am/'scripts'/('ysyxsoc-code-'+target+'.ld')).write_text(text)
    for capacity in [32,64,128]:
        text=template.replace('@TARGET@','sdram').replace('@HEAP_START@','ALIGN(__bss_end,16)').replace('@TARGET_LIMIT@','ORIGIN(sdram)+LENGTH(sdram)').replace('@HEAP_END@','ORIGIN(sdram)+LENGTH(sdram)').replace('@SDRAM_MB@',str(capacity))
        (am/'scripts'/('ysyxsoc-code-sdram'+str(capacity)+'.ld')).write_text(text)
    profiles={'initial':{'SOC_BOOT_DATA':0,'SOC_UART_MODE':0},'raw':{'SOC_UART_MODE':0},'divisor':{'SOC_UART_MODE':1},
              'poison':{'SOC_POISON_SRAM':1},'broken-data':{'SOC_POISON_SRAM':1,'SOC_SKIP_DATA':1},'broken-bss':{'SOC_POISON_SRAM':1,'SOC_SKIP_BSS':1},'flash':{'SOC_FLASH_BOOT':1},'flash-id':{'SOC_FLASH_BOOT':1,'SOC_PRINT_ID':1},
              'flash-psram':{'SOC_PSRAM_DATA':1},'psram':{'SOC_RELOCATE_TEXT':1},'sram-code':{'SOC_RELOCATE_TEXT':1,'SOC_CODE_SRAM':1},
              'psram-ssbl':{'SOC_RELOCATE_TEXT':1,'SOC_TWO_STAGE':1}}
    for capacity in [32,64,128]:profiles['sdram'+str(capacity)]={'SOC_RELOCATE_TEXT':1,'SOC_TWO_STAGE':1,'SOC_CODE_SDRAM':1,'SOC_SDRAM_MB':capacity}
    for name,values in profiles.items():
        (am/'scripts'/('riscv32e-ysyxsoc-'+name+'.mk')).write_text(''.join(k+' := '+str(v)+'\n' for k,v in values.items())+'include $(AM_HOME)/scripts/riscv32e-ysyxsoc.mk\n')
    for name,origin in [('cpu-tests',BENCH/'am-kernels/tests/cpu-tests'),('hello',BENCH/'am-kernels/kernels/hello')]:
        if not (base/name).exists():shutil.copytree(origin,base/name,ignore=shutil.ignore_patterns('build','.git','.result','Makefile.*'))
    shutil.copyfile(BENCH/'Makefile',base/'Makefile')
    npc=base/'npc';npc.mkdir(exist_ok=True)
    (npc/'Makefile').write_text('SIM := '+str(WORK/'c5/build/20000000/sim')+'\nREF := '+str(WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so')+'\nNPC_ARGS ?=\nsim:\n\t$(SIM) --mrom "$(IMAGE)" --ref $(REF) --report "$(IMAGE).npc.json" --max-cycles 1000000000 $(NPC_ARGS)\ninclude ../Makefile\n.PHONY: sim\n')
    if not (base/'.git').exists():
        run('C5/am/git-init',['git','init'],cwd=base)
        run('C5/am/git-name',['git','config','user.name','Local C5 engineering'],cwd=base)
        run('C5/am/git-email',['git','config','user.email','local-c5@invalid.example'],cwd=base)
        (base/'.gitignore').write_text('**/build/\n**/*.o\n.result\n')
        run('C5/am/git-add',['git','add','.'],cwd=base)
        run('C5/am/git-base',['git','-c','gc.auto=0','commit','-m','Record C5 AM source baseline'],cwd=base)
    dump(ROOT/'reports/C5_am_setup.json',{'status':'PREPARED_NOT_RUNTIME_ACCEPTED','workbench':str(base),
         'files':[{'path':str(source/k),'destination':str(am/v),'sha256':sha(source/k)} for k,v in mapping.items()],
         'profiles':profiles,'scope':'MROM4KiB/SRAM8KiB; stack2KiB reserved; initial no-copy demonstration and final .data/.bss bootloader. Explicit poisoned-SRAM omission controls. UART raw/divisor/poll profiles; unimplemented peripherals report absent.'})
    print('C5_PRIVATE_AM_PREPARED',flush=True)


if __name__=='__main__':main()
