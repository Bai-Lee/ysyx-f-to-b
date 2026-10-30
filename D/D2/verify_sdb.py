from pathlib import Path
import sys,tarfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    n=BENCH/'nemu';exe=n/'build/riscv32-nemu-interpreter';p=ROOT/'D/D2';cases=p/'commands';cases.mkdir(exist_ok=True)
    texts={
      'steps':'help\np 1+2*3\np $pc\nx 5 0x80000000\nsi\np $pc\ninfo r\nsi 2\np $pc\nc\nq\n',
      'watch':'w $t0\ninfo w\nc\np $pc\nd 0\nw *0x80000010\nc\np $pc\nx 1 0x80000010\nd 0\ninfo w\nc\nq\n',
      'bad':'\nunknown\nsi -1\nsi 0\nsi abc\nsi 1000001\ninfo\ninfo z\np\np 1+\np $garbage\np *0\np 0&&*0\nx\nx -1 0\nx 2\nx 2 0xffffffff\nw\nd -1\nd 99\nd 0\np 42\nq\n',
      'pool':('w $pc\n'*33)+'info w\nd 31\nd 15\nd 0\nd 15\nw $t0\nw $t0\nw $t0\ninfo w\nq\n',
      'watch_error':'w 1/($t0-0x80000000)\nc\np $pc\nd 0\nq\n',
    }
    rows=[]
    for name,text in texts.items():
        f=cases/(name+'.txt');f.write_text(text)
        o,e,r=run('D2/sdb/'+name,[exe],cwd=n,env={'NEMU_HOME':str(n),'ASAN_OPTIONS':'detect_leaks=1:halt_on_error=1'},stdin_file=f,inputs=[exe,f,n/'tools/capstone/repo/libcapstone.so.5'],timeout=45)
        assert not any(x in e for x in ['ERROR: AddressSanitizer','LeakSanitizer: detected'])
        if name=='steps':assert 'EXPR_VALUE 7 0x00000007' in o and 'EXPR_VALUE 2147483652 0x80000004' in o and 'EXPR_VALUE 2147483660 0x8000000c' in o and 'HIT GOOD TRAP' in o
        if name=='watch':assert o.count('WATCH_HIT ')==2 and 'EXPR_VALUE 2147483652 0x80000004' in o and 'EXPR_VALUE 2147483656 0x80000008' in o and '0xdeadbe00' in o and 'WATCH_COUNT 0' in o and 'HIT GOOD TRAP' in o
        if name=='bad':assert o.count('COMMAND_ERROR')>=10 and o.count('EXPR_ERROR')>=4 and 'EXPR_VALUE 42' in o and 'EXPR_VALUE 0 0x00000000' in o
        if name=='pool':assert 'watchpoint pool exhausted' in o and o.count('WATCH_COUNT 32')==2 and 'WATCH_ERROR_NO_ID 15' in o
        if name=='watch_error':assert 'WATCH_ERROR 0 division by zero' in o and 'EXPR_VALUE 2147483652 0x80000004' in o
        rows.append({'name':name,'status':'PASS','log':'artifacts/D2/sdb/'+name,'commands_sha256':sha(f),'elapsed_seconds':r['elapsed_seconds']})
    original=ARCHIVE/'repos/NJU-ProjectN__nemu__ics2024'
    def counts(root):
        files=[x for x in root.rglob('*') if x.suffix in ('.c','.h') and not any(t in x.relative_to(root).parts for t in ('.git','build','repo','generated','config'))]
        return {'files':len(files),'lines':sum(len(x.read_text(errors='replace').splitlines()) for x in files),'nonblank_lines':sum(sum(bool(s.strip()) for s in x.read_text(errors='replace').splitlines()) for x in files)}
    before,after=counts(original),counts(n)
    dest=p/'snapshot';dest.mkdir(exist_ok=True);archive=dest/'nemu-pa1.tar.gz';members=[]
    files=[x for x in n.rglob('*') if x.is_file() and not x.is_symlink() and not any(t in x.relative_to(n).parts for t in ('.git','build','repo'))]
    files+=[exe,n/'tools/capstone/repo/libcapstone.so.5']
    with tarfile.open(archive,'w:gz') as tar:
        for f in sorted(set(files)):
            rel=str(f.relative_to(n));tar.add(f,arcname=rel,recursive=False);members.append({'path':rel,'sha256':sha(f),'bytes':f.stat().st_size})
    with tarfile.open(archive) as tar:
        for row in members:assert hashlib.sha256(tar.extractfile(row['path']).read()).hexdigest()==row['sha256']
    dump(dest/'manifest.json',{'status':'PASS','archive_sha256':sha(archive),'members':members})
    report={'status':'PASS','interactive_cases':rows,'expression_evidence':'reports/D2_expression.json','sanitizer':'Actual NEMU built with AddressSanitizer; all scripted command sessions clean including leak checks. Debugger core also tested with ASan+UBSan.','source_line_counts':{'original':before,'PA1':after,'delta_lines':after['lines']-before['lines'],'delta_nonblank':after['nonblank_lines']-before['nonblank_lines'],'scope':'all authored/framework .c/.h below NEMU, excluding .git/build/repo/generated/config; same exclusions on baseline'},'frozen_snapshot':'D/D2/snapshot/nemu-pa1.tar.gz','snapshot_sha256':sha(archive),'official_submission':'EXCLUDED_SCOPE','instruction_scope':'Original PA1 four-instruction scaffold; no RV32IM completion claim yet.'}
    dump(ROOT/'reports/D2_sdb.json',report);print('D2_SDB_PASS',flush=True)

if __name__=='__main__':main()
