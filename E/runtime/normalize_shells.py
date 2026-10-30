from common import *
def main():
    changes=[]
    for p in BENCH.rglob('*'):
        if not p.is_file() or '.git' in p.parts or 'build' in p.parts:continue
        if p.suffix not in ['.sh',''] and p.name not in ['minirv-gcc','minirv-g++']:continue
        data=p.read_bytes()
        if not (p.suffix=='.sh' or data.startswith(b'#!')) or b'\0' in data or b'\r\n' not in data:continue
        before=sha(p);p.write_bytes(data.replace(b'\r\n',b'\n'))
        changes.append({'path':str(p),'before_sha256':before,'after_sha256':sha(p),'scope':'CRLF-to-LF only in extracted Linux working copy; original archive and original export preserved.'})
    dump(ROOT/'reports/E_shell_normalization.json',{'status':'PASS','changes':changes,'reason':'Windows Git export carried CRLF into executable shebangs, making /bin/bash\r unavailable in Linux.'})
    print('LINUX_SHELLS_NORMALIZED',len(changes),flush=True)
if __name__=='__main__':main()
