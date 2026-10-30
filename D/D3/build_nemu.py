from pathlib import Path
import sys,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def apply(rel):
    original=ARCHIVE/'repos/NJU-ProjectN__nemu__ics2024'/rel
    match=re.match(r'/\*.*?\*/\s*',original.read_text(),re.S)
    dest=BENCH/'nemu'/rel;dest.write_text((match.group(0) if match else '')+(ROOT/'D/nemu_overlay'/rel).read_text());return dest

def main():
    n=BENCH/'nemu';changed=[apply('src/isa/riscv32/inst.c'),apply('src/isa/riscv32/difftest/dut.c')]
    p=n/'src/memory/paddr.c';text=p.read_text()
    if 'D_STAGE_FULL_SPAN' not in text:
        text=text.replace('word_t ret = host_read(guest_to_host(addr), len);','word_t ret = 0; memcpy(&ret, guest_to_host(addr), (size_t)len);')
        text=text.replace('host_write(guest_to_host(addr), len, data);','memcpy(guest_to_host(addr), &data, (size_t)len);')
        text=text.replace('if (likely(in_pmem(addr)))', 'if (likely(in_pmem(addr) && (uint64_t)addr + len <= (uint64_t)CONFIG_MBASE + CONFIG_MSIZE))')
        text='/* D_STAGE_FULL_SPAN: little-endian host, defined unaligned byte copy; full access checked. */\n'+text;p.write_text(text)
    changed.append(p)
    # Upstream make dependencies do not invalidate every object when ASan/optimization
    # flags change. Keep object sets separated by the generated configuration digest.
    buildmk=n/'scripts/build.mk';text=buildmk.read_text()
    old='OBJ_DIR  = $(BUILD_DIR)/obj-$(NAME)$(SO)'
    new='OBJ_DIR  = $(BUILD_DIR)/obj-$(NAME)$(SO)-$(shell sha256sum $(NEMU_HOME)/include/generated/autoconf.h 2>/dev/null | cut -c1-12)'
    if old+'\n' in text:text=text.replace(old+'\n',new+'\n');buildmk.write_text(text)
    else:assert new in text
    changed.append(buildmk)
    disasm=n/'src/utils/disasm.c';text=disasm.read_text()
    old='  assert(count == 1);'
    if old in text:
        text=text.replace(old,'  if (count != 1) {\n    uint32_t raw = 0; memcpy(&raw, code, nbyte < 4 ? nbyte : 4);\n    snprintf(str, size, ".word 0x%08x", raw);\n    if (count) cs_free_dl(insn, count);\n    return;\n  }');disasm.write_text(text)
    changed.append(disasm)
    monitor=n/'src/monitor/monitor.c';text=monitor.read_text()
    anchor='  long size = ftell(fp);'
    if 'IMAGE_REJECT' not in text:
        assert anchor in text;text=text.replace(anchor,anchor+'\n  if (size <= 0 || (uint64_t)size > (uint64_t)CONFIG_MSIZE - CONFIG_PC_RESET_OFFSET) {\n    fprintf(stderr, "IMAGE_REJECT invalid size=%ld capacity=%u\\n", size, CONFIG_MSIZE - CONFIG_PC_RESET_OFFSET);\n    fclose(fp); exit(2);\n  }');monitor.write_text(text)
    changed.append(monitor)
    config=n/'configs/dstage_rv32im_defconfig';config.write_text('CONFIG_ISA_riscv=y\nCONFIG_ENGINE_INTERPRETER=y\nCONFIG_TARGET_NATIVE_ELF=y\nCONFIG_CC_O2=y\n# CONFIG_CC_DEBUG is not set\n# CONFIG_CC_ASAN is not set\nCONFIG_TRACE=y\nCONFIG_ITRACE=y\nCONFIG_DIFFTEST=y\nCONFIG_DIFFTEST_REF_SPIKE=y\nCONFIG_MBASE=0x80000000\nCONFIG_MSIZE=0x08000000\n# CONFIG_MEM_RANDOM is not set\n# CONFIG_DEVICE is not set\nCONFIG_WATCHPOINT=y\n')
    env={'NEMU_HOME':str(n),**json.loads((ROOT/'reports/D_spike_support.json').read_text())['env']}
    run('D3/nemu/configure',['make','-j1','dstage_rv32im_defconfig'],cwd=n,env=env,inputs=[config,n/'Kconfig'],outputs=[n/'.config',n/'include/generated/autoconf.h'])
    spike=n/'tools/spike-diff';repo=spike/'repo';build=spike/'build';build.mkdir(exist_ok=True)
    inc=['fesvr','riscv','disasm','customext','fdt','softfloat','spike_main','spike_dasm','build'];libs=['libspike_main.a','libriscv.a','libdisasm.a','libsoftfloat.a','libfesvr.a','libfdt.a'];so=build/'riscv32-spike-so'
    cmd=['g++','-std=c++17','-O2','-shared','-fPIC','-fvisibility=hidden','-I'+str(repo),*['-I'+str(repo/x) for x in inc],'-I'+str(n/'include'),spike/'difftest.cc',*[repo/'build'/x for x in libs],'-o',so]
    run('D3/spike/link',cmd,cwd=spike,env=env,inputs=[spike/'difftest.cc',n/'include/generated/autoconf.h',*[repo/'build'/x for x in libs]],outputs=[so],timeout=120)
    exe=n/'build/riscv32-nemu-interpreter'
    run('D3/nemu/build',['make','-j1'],cwd=n,env=env,inputs=[*changed,n/'.config'],outputs=[exe],timeout=300)
    o,_,_=run('D3/nemu/builtin',[exe,'-b','-d',so],cwd=n,env=env,inputs=[exe,so]);assert 'HIT GOOD TRAP' in o
    dump(ROOT/'reports/D3_build.json',{'status':'PASS_BUILTIN_ONLY','nemu':str(exe),'nemu_sha256':sha(exe),'spike':str(so),'spike_sha256':sha(so),'runtime_environment':env,'instructions':'RV32I integer operations and M; FENCE/FENCE.I sequential model; EBREAK host termination. Privileged CSR/trap machinery is deferred.','memory':'128 MiB at 0x80000000, little-endian. NEMU RAM permits defined unaligned memcpy; Spike configured to reject misaligned operations, so such tests require separate evidence.','evidence':['artifacts/D3/nemu','artifacts/D3/spike']})

if __name__=='__main__':main()
