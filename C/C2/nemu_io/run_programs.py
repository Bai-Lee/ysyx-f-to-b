"""C2 PA2 command-line programs with independent feature/performance binaries."""
from pathlib import Path
import sys,re,tarfile,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'runtime'))
from common import *

APPS=WORK/'c2-nemu-apps';D=ROOT/'C/C2/nemu_io';N=BENCH/'nemu';AM=BENCH/'abstract-machine'

def binaries():return {r['mode']:Path(r['executable']) for r in json.loads((ROOT/'reports/C2_nemu_build.json').read_text())['variants']}

def compile_app(name,cwd,arg='',extra=()):
    makefile=cwd/'Makefile';base=next(re.finditer(r'^NAME\s*[?:]?=\s*(\S+)',makefile.read_text(),re.M))[1]
    elf=cwd/'build'/(base+'-riscv32-nemu.elf');binary=elf.with_suffix('.bin')
    sources=sorted(p for p in cwd.rglob('*') if p.is_file() and p.suffix in ('.c','.cc','.h','.S') and 'build' not in p.relative_to(cwd).parts)
    inputs=[makefile,*sources,AM/'Makefile',AM/'scripts/platform/nemu.mk',*sorted((AM/'am/src/platform/nemu/ioe').glob('*.c')),*sorted((AM/'klib/src').glob('*.c'))]
    run('C2/pa2/build/'+name,['make','-j1','ARCH=riscv32-nemu','insert-arg','mainargs='+arg,*extra],cwd=cwd,inputs=inputs,outputs=[binary,elf],timeout=600,resume=True)
    return binary,elf

def execute(name,binary,elf,mode='feature',env=None,expected=(0,),timeout=600):
    exe=binaries()[mode];folder=ROOT/'artifacts/C2/pa2/programs'/name;folder.mkdir(parents=True,exist_ok=True);report=folder/'result.json'
    args=[exe,'-b','--report='+str(report),'--elf='+str(elf)]
    if mode=='feature':args.append('--diff='+str(N/'tools/spike-diff/build/riscv32-spike-so'))
    args.append(binary)
    o,e,r=run('C2/pa2/programs/'+name,args,cwd=N,inputs=[exe,binary,elf,N/'tools/spike-diff/build/riscv32-spike-so'] if mode=='feature' else [exe,binary,elf],outputs=[report],env={'SDL_VIDEODRIVER':'dummy',**(env or {})},expected=expected,timeout=timeout,resume=True)
    result=json.loads(report.read_text());assert result['result']==('GOOD_TRAP' if expected==(0,) else 'BAD_TRAP'),result
    assert result['diff_enabled']==(mode=='feature')
    if mode=='feature':assert result['diff_checked']+result['diff_skipped']==result['instructions']
    return {'name':name,'mode':mode,'status':'PASS','simulation':result,'wall_seconds':r['elapsed_seconds'],'executable_sha256':sha(exe),'image_sha256':sha(binary),'elf_sha256':sha(elf),'evidence':'artifacts/C2/pa2/programs/'+name},o+e

def normal():
    rows=[]
    for name,relative in [('hello','kernels/hello'),('alu','tests/alu-tests'),('klib','tests/klib-tests')]:
        binary,elf=compile_app(name,APPS/'am-kernels'/relative,'C2-NEMU' if name=='hello' else '')
        row,text=execute(name,binary,elf,timeout=900);rows.append(row)
        # alu-tests returns its accumulated exit_code and prints only failures.
        assert ('Hello, AbstractMachine!' if name=='hello' else 'KLIB_PORTABLE_PASS' if name=='klib' else 'HIT GOOD TRAP') in text
    # Source-preserving original wrong test must fail, including its own assertion.
    cwd=APPS/'am-kernels/tests/cpu-tests';image=cwd/'build/wrong-riscv32-nemu.bin';elf=image.with_suffix('.elf')
    run('C2/pa2/build/wrong',['make','-j1','ARCH=riscv32-nemu','ALL=wrong'],cwd=cwd,inputs=[cwd/'tests/wrong.c',cwd/'Makefile'],outputs=[image,elf],timeout=120)
    row,text=execute('wrong',image,elf,expected=(1,));rows.append(row);assert 'BAD TRAP' in text
    # Named dtrace, explicit cap and filtering on a genuine MMIO-output program.
    image,elf=compile_app('hello-dtrace',APPS/'am-kernels/kernels/hello','C2-DTRACE')
    trace=D/'results/serial.dtrace';trace.parent.mkdir(exist_ok=True)
    row,text=execute('dtrace',image,elf,env={'C_DTRACE_FILE':str(trace),'C_DTRACE_LIMIT':'8','C_DTRACE_FILTER':'serial'})
    lines=trace.read_text().splitlines();assert len(lines)==9 and lines[-1]=='DTRACE_LIMIT limit=8'
    assert all('map=serial' in line and 'op=W' in line and 'addr=a00003f8' in line for line in lines[:-1]);rows.append(row)
    excluded=D/'results/excluded.dtrace'
    row,text=execute('dtrace-excluded',image,elf,env={'C_DTRACE_FILE':str(excluded),'C_DTRACE_FILTER':'rtc'})
    assert excluded.read_bytes()==b'';rows.append(row)
    exe=binaries()['feature'];o,e,_=run('C2/pa2/programs/dtrace-invalid',[exe,'-b','--diff=none',image],cwd=N,inputs=[exe,image],env={'SDL_VIDEODRIVER':'dummy','C_DTRACE_LIMIT':'-1'},expected=(2,))
    assert 'DTRACE_CONFIG invalid limit' in e
    report=ROOT/'reports/C2_nemu_functional.json';dump(report,{'status':'PASS','programs':rows,'dtrace':{'path':str(trace),'sha256':sha(trace),'limit':8,'named_filter':'serial','excluded_serial_trace_empty':True,'negative_limit_rejected':True},'scope':'Actual C NEMU feature build, independent Spike comparison for ordinary instructions and explicit MMIO skip accounting; original wrong program rejected.'})
    print('C2_NEMU_COMMAND_PROGRAMS_PASS',flush=True)

def restore_original_benchmarks():
    lock=json.loads((ROOT/'reports/E_offline_sources.json').read_text());row=next(r for r in lock['repositories'] if r['name']=='NJU-ProjectN__am-kernels__ics2026')
    archive=ROOT/row['delivery_path'];assert sha(archive)==row['sha256']
    paths=['benchmarks/dhrystone/dry.c','benchmarks/coremark/src/core_main.c','benchmarks/coremark/include/core_portme.h'];records=[]
    with tarfile.open(archive) as t:
        for rel in paths:
            target=APPS/'am-kernels'/rel;backup=D/'upstream/performance'/rel;backup.parent.mkdir(parents=True,exist_ok=True)
            if not backup.exists():shutil.copyfile(target,backup)
            original=t.extractfile(rel).read();target.write_bytes(original)
            records.append({'path':str(target),'sha256':sha(target),'canonical_source_archive_sha256':row['sha256']})
    dump(D/'results/performance_sources.json',{'status':'PASS_CANONICAL_RESTORED','files':records,'scope':'C2 performance uses original official iteration counts, not D minimal demonstration iterations. Original validation logic restored byte-for-byte.'})

def benchmarks():
    (D/'results').mkdir(exist_ok=True);restore_original_benchmarks();rows=[]
    for name,arg in [('dhrystone',''),('coremark',''),('microbench','test'),('microbench','ref')]:
        tag=name+('-'+arg if arg else '');image,elf=compile_app(tag,APPS/'am-kernels/benchmarks'/name,arg)
        row,text=execute(tag,image,elf,mode='performance',timeout=1800)
        assert re.search(r'PASS|pass',text) and not re.search(r'FAIL|wrong',text)
        if name=='microbench':assert 'skipped' not in text.lower() and 'error' not in text.lower()
        row['score_lines']=[s for s in text.splitlines() if re.search(r'PASS|Marks|Score|score|BENCH',s)]
        rows.append(row);dump(ROOT/'reports/C2_nemu_benchmarks.json',{'status':'IN_PROGRESS','runs':rows})
    dump(ROOT/'reports/C2_nemu_benchmarks.json',{'status':'PASS','runs':rows,'configuration':'C2_nemu_build performance: actual TRACE/DIFFTEST/WATCHPOINT/CC_DEBUG off, separate binary; no GPU or keyboard, RTC+UART remain.','scope':'Official original Dhrystone/CoreMark inputs and iteration counts; MicroBench test then ref, all checks retained. Performance of this laptop/WSL/model only, not silicon PPA or an official CoreMark certification.'})
    print('C2_NEMU_BENCHMARKS_PASS',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--benchmarks',action='store_true');a=p.parse_args()
    benchmarks() if a.benchmarks else normal()
