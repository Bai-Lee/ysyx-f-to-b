from pathlib import Path
import sys,struct,re,random
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
_logged_run=run
def run(tag,args,**kwargs):
    kwargs.setdefault('cwd',BENCH/'nemu')
    return _logged_run(tag,args,**kwargs)

def main():
    d=ROOT/'D/D7';out=d/'results';out.mkdir(exist_ok=True)
    conf=json.loads((ROOT/'reports/D7_build.json').read_text());exe=Path(conf['nemu']);ref=Path(conf['spike']);env=conf['environment'];n=BENCH/'nemu'
    cc='riscv64-linux-gnu-gcc';objcopy='riscv64-linux-gnu-objcopy';ld=d/'baremetal.ld'
    ld.write_text('OUTPUT_ARCH(riscv)\nENTRY(_start)\nSECTIONS { . = 0x80000000; .text : { KEEP(*(.text.start)) *(.text*) } .rodata : { *(.rodata*) } . = ALIGN(4); .data : { *(.data*) } .bss : { *(.bss*) *(COMMON) } /DISCARD/ : { *(.note*) *(.comment*) } }\n')
    elf=out/'trace.elf';binary=out/'trace.bin';source=d/'trace_test.S'
    run('D7/trace/assemble',[cc,'-march=rv32im','-mabi=ilp32','-nostdlib','-nostartfiles','-static','-Wl,--build-id=none','-T',ld,source,'-o',elf],inputs=[source,ld],outputs=[elf])
    run('D7/trace/objcopy',[objcopy,'-O','binary',elf,binary],inputs=[elf],outputs=[binary])
    trace=out/'normal.trace';report=out/'normal.json'
    traceenv={**env,'D_TRACE_FILE':str(trace),'D_TRACE_MODES':'imf','D_TRACE_LIMIT':'1000'}
    o,e,_=run('D7/trace/normal',[exe,'-b','-d',ref,'--elf',elf,'--report',report,binary],inputs=[exe,ref,elf,binary],outputs=[trace,report],env=traceenv)
    result=json.loads(report.read_text());assert result['result']=='GOOD_TRAP' and result['diff_checked']==result['instructions']-1 and result['diff_skipped']==1
    lines=trace.read_text().splitlines();assert len([l for l in lines if l.startswith('I ')])==result['instructions']
    assert sum(l.startswith('M ') for l in lines)==4
    assert any('call outer@' in l and 'depth=0' in l for l in lines)
    assert any('call leaf@' in l and 'depth=1' in l for l in lines)
    assert any('tail outer -> tail@' in l for l in lines)
    assert any('depth=0 ret tail ' in l for l in lines)
    assert any('W addr=0x80020000 size=4 value=0x0000002a' in l for l in lines)
    assert any('R addr=0x80020000 size=4 value=0x0000002a' in l for l in lines)
    limited=out/'limited.trace'
    run('D7/trace/limited',[exe,'-b','-d',ref,'--elf',elf,binary],inputs=[exe,ref,elf,binary],outputs=[limited],env={**traceenv,'D_TRACE_FILE':str(limited),'D_TRACE_LIMIT':'5'})
    assert len(limited.read_text().splitlines())==6 and limited.read_text().splitlines()[-1]=='TRACE_LIMIT limit=5'
    off=out/'disabled.trace';assert not off.exists()
    run('D7/trace/disabled',[exe,'-b','-d',ref,binary],inputs=[exe,ref,binary],env={**traceenv,'D_TRACE_FILE':str(off),'D_TRACE_MODES':''});assert not off.exists()
    bad=out/'illegal.bin';bad.write_bytes(struct.pack('<I',0x00000013)*40+struct.pack('<I',0xffffffff))
    o,e,_=run('D7/trace/iring',[exe,'-b','-d','none',bad],inputs=[exe,bad],env=env,expected=(1,))
    rings=[l for l in e.splitlines() if re.match(r'(--> |    )0x',l)]
    assert len(rings)==16 and '0x800000a0: ffffffff' in rings[-1] and rings[-1].startswith('-->')
    badmem=out/'badmem.bin';badmem.write_bytes(struct.pack('<III',0xf00002b7,0x0002a303,0x00100073))
    o,e,_=run('D7/trace/iring-memory',[exe,'-b','-d','none',badmem],inputs=[exe,badmem],env=env,expected=(-6,134))
    assert 'out of bound' in o+e or 'can not find map' in o+e
    assert 'IRINGBUF' in e and '0x80000004' in e
    stripped=out/'stripped.elf'
    run('D7/trace/strip',['riscv64-linux-gnu-strip','-s','-o',stripped,elf],inputs=[elf],outputs=[stripped])
    strippedtrace=out/'stripped.trace'
    o,e,_=run('D7/trace/stripped',[exe,'-b','-d',ref,'--elf',stripped,binary],inputs=[exe,ref,stripped,binary],outputs=[strippedtrace],env={**traceenv,'D_TRACE_FILE':str(strippedtrace)})
    assert 'symbols=0' in o and 'call ?@' in strippedtrace.read_text()
    # Independently build the ELF parser with host sanitizers, then test damaged
    # bounds and deterministic random headers without using readelf as parser.
    probe=WORK/'build/trace-probe';core=ROOT/'D/runtime/trace_core.c';header=ROOT/'D/runtime/trace_core.h'
    run('D7/elf/build',['gcc','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-g','-fno-pie','-no-pie','-I'+str(header.parent),core,d/'trace_probe.c','-o',probe],inputs=[core,header,d/'trace_probe.c'],outputs=[probe])
    run('D7/elf/valid',[probe,elf],inputs=[probe,elf],env={'ASAN_OPTIONS':'detect_leaks=1'})
    edge=bytearray(elf.read_bytes());shoff=struct.unpack_from('<I',edge,32)[0];shnum=struct.unpack_from('<H',edge,48)[0];edge_name=None
    for k in range(shnum):
        h=struct.unpack_from('<10I',edge,shoff+k*40)
        if h[1]!=2:continue
        strings=struct.unpack_from('<10I',edge,shoff+h[6]*40)
        for offset in range(h[4],h[4]+h[5],16):
            name,value,size,info,other,index=struct.unpack_from('<IIIBBH',edge,offset)
            if info&15==2 and index!=0:
                begin=strings[4]+name;edge_name=bytes(edge[begin:edge.index(0,begin)]).decode();struct.pack_into('<II',edge,offset+4,0xfffffff0,16);break
        if edge_name:break
    assert edge_name
    edge_elf=out/'edge-range.elf';edge_elf.write_bytes(edge)
    o,e,_=run('D7/elf/edge-range',[probe,edge_elf,'edge'],inputs=[probe,edge_elf],env={'ASAN_OPTIONS':'detect_leaks=1'});assert 'call '+edge_name+'@0xfffffff4' in o
    blob=elf.read_bytes();cases={'short':b'\x7fELF','magic':b'NOPE'+blob[4:],'class64':blob[:4]+b'\x02'+blob[5:],'bigendian':blob[:5]+b'\x02'+blob[6:],'section_oob':blob[:32]+struct.pack('<I',0xfffffff0)+blob[36:]}
    rng=random.Random(0x2607d7)
    for i in range(50):cases['random_'+str(i)]=rng.randbytes(rng.randint(0,200))
    for name,data in cases.items():
        p=out/(name+'.elf');p.write_bytes(data)
        o,e,_=run('D7/elf/'+name,[probe,p],inputs=[probe,p],expected=(2,),env={'ASAN_OPTIONS':'detect_leaks=1'});assert 'ELF_REJECT' in e and 'AddressSanitizer' not in e
    # Actual NEMU addi mutant in a separate build directory; restore the live
    # source byte-for-byte before executing either test binary.
    inst=n/'src/isa/riscv32/inst.c';original=inst.read_bytes();text=original.decode();old='case 0:value=a+ii;break;';assert text.count(old)==1
    mutant=d/'results/inst-addi-mutant.c';mutant.write_text(text.replace(old,'case 0:value=a+ii+1;break;'))
    mutantdir=WORK/'build/nemu-addi-mutant';badexe=mutantdir/'riscv32-nemu-interpreter'
    try:
        inst.write_bytes(mutant.read_bytes())
        run('D7/diff/mutant-build',['make','-j1','BUILD_DIR='+str(mutantdir)],cwd=n,inputs=[mutant,inst,n/'.config',core],outputs=[badexe],env=env,timeout=300)
    finally:inst.write_bytes(original)
    badreport=out/'mutant.json'
    o,e,_=run('D7/diff/mutant',[badexe,'-b','-d',ref,'--report',badreport,binary],inputs=[badexe,ref,binary],outputs=[badreport],env=env,expected=(1,))
    assert 'DIFF_MISMATCH' in o+e
    r=json.loads(badreport.read_text());assert r['result']=='ABORT' and r['halt_pc']==0x80000004 and r['diff_checked']==2
    # Native strip experiment demonstrates executable vs relocatable contracts.
    hello=out/'hello.c';hello.write_text('#include <stdio.h>\nint main(void){puts("STRIP_OK");return 0;}\n')
    host=WORK/'build/d7-hello';obj=WORK/'build/d7-hello.o';strippedobj=WORK/'build/d7-hello-stripped.o'
    run('D7/strip/native-build',['gcc',hello,'-o',host],inputs=[hello],outputs=[host])
    run('D7/strip/native-strip',['strip','-s',host],inputs=[host],outputs=[host])
    o,_,_=run('D7/strip/native-run',[host],inputs=[host]);assert 'STRIP_OK' in o
    run('D7/strip/object-build',['gcc','-c',hello,'-o',obj],inputs=[hello],outputs=[obj])
    run('D7/strip/object-strip',['strip','-s','-o',strippedobj,obj],inputs=[obj],outputs=[strippedobj])
    o,e,_=run('D7/strip/object-link',['gcc',strippedobj,'-o',WORK/'build/d7-stripped-link'],inputs=[strippedobj],expected=(1,));assert 'undefined reference' in e
    dump(ROOT/'reports/D7_trace.json',{'status':'PASS','normal_report':result,'normal_trace':str(trace),'malformed_elf_cases':len(cases),'parser_sanitizers':'ASAN+UBSAN','ring_capacity':16,'trace_limit_checked':5,'modes_disabled_checked':True,'addi_mutant':r,'source_restored_sha256':sha(inst),'scope':'Instruction/data/function tracing, ELF32 RISC-V parsing, tail-call accounting, bounded output, ring on illegal instruction and bad memory. Spike comparisons cover PC and 32 GPR, not all RAM; only EBREAK and known device instructions skip.'})

if __name__=='__main__':main()
