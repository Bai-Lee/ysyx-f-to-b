"""LCT-04-BASE: actual native source configure/build/install, private prefix."""
from pathlib import Path
import sys,json,shlex
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from evidence import *

def main():
    lock=ROOT/'reports/E3_valgrind_source_layout.json'
    meta=json.loads(lock.read_text('utf8'))
    for f in meta['manifest_hashes_matched']:assert sha(f['path'])==f['sha256']
    assert sha(meta['dsc'])==meta['dsc_sha256']
    source='/home/USER/e3-lab/valgrind-3.18.1-source'
    prefix='/home/USER/tools/valgrind-3.18.1-source'
    result={'status':'IN_PROGRESS','source':source,'prefix':prefix,'source_lock':str(lock),'make_jobs':2,'architecture':'amd64 only, matching the actual target host','runs':[]}
    def execute(name,script,expected=0,timeout=120):
        r=run('E3/valgrind_build/'+name,['wsl.exe','-d','YSYX-Linux','-u','ysyx','--exec','bash','-lc',script],[lock,Path(__file__).resolve(),ROOT/'config/E3_resume.json'],timeout=timeout,expected=expected)
        result['runs'].append(r);dump(ROOT/'reports/E3_valgrind_build.json',result)
        if r['status']!='PASS':result['status']=r['status'];dump(ROOT/'reports/E3_valgrind_build.json',result);raise RuntimeError(name)
        folder=ROOT/'artifacts/E3/valgrind_build'/name
        return (folder/'stdout.log').read_text('utf8',errors='replace'),(folder/'stderr.log').read_text('utf8',errors='replace')
    execute('extract',f'''set -eu
test "$(awk '/MemTotal/ {{print $2}}' /proc/meminfo)" -ge 1800000
if [ ! -d {source} ]; then
    dpkg-source -x /workspace/downloads/ysyx_e3/valgrind-source/valgrind_3.18.1-1ubuntu2.dsc {source}
fi
test -f {source}/configure
''',timeout=120)
    execute('configure',f'cd {source}\n./configure --prefix={prefix} --enable-only64bit',timeout=300)
    execute('make',f'cd {source}\nmake -j2',timeout=1800)
    execute('install',f'cd {source}\nmake -j1 install',timeout=300)
    out,err=execute('positive',f'{prefix}/bin/valgrind --version\n{prefix}/bin/valgrind --error-exitcode=99 --leak-check=full --show-leak-kinds=all /home/USER/e3-lab/tool-probe/good',timeout=60)
    assert 'valgrind-3.18.1' in out and 'PASS E2 linked_list' in out
    assert 'ERROR SUMMARY: 0 errors' in err and 'in use at exit: 0 bytes in 0 blocks' in err
    out,err=execute('negative',f'{prefix}/bin/valgrind --error-exitcode=99 --leak-check=full /home/USER/e3-lab/tool-probe/bad_memory',expected=99,timeout=60)
    assert 'Invalid write of size 1' in err and 'definitely lost: 17 bytes' in err
    out,err=execute('fingerprints',f'sha256sum {prefix}/bin/valgrind {prefix}/libexec/valgrind/memcheck-amd64-linux\n{prefix}/bin/valgrind --version')
    result.update(status='PASS',fingerprints=out,timestamp=datetime.now(timezone.utc).isoformat(),scope='Actual configure/make/install from Ubuntu-authenticated source; private user prefix. This build covers AMD64 host programs, not every supported architecture.')
    dump(ROOT/'reports/E3_valgrind_build.json',result);print('VALGRIND_SOURCE_BUILD_AND_CONTROLS PASS',flush=True)

if __name__=='__main__':main()
