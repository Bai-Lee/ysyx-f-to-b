from evidence import *
import re

def main():
    items=[];inputs=[ROOT/'E/E3/tool_probe/Makefile',ROOT/'E/E3/tool_probe/bad_memory.c',ROOT/'E/E2/linked_list.c']
    def linux(name,command,expected=0,timeout=45):
        q=run('E3/tools/'+name,['wsl.exe','-d','YSYX-Linux','-u','ysyx','--exec','bash','-lc',command],inputs,timeout=timeout,expected=expected)
        assert q['status']=='PASS',name;items.append(q)
        folder=ROOT/'artifacts/E3/tools'/name
        return (folder/'stdout.log').read_text('utf8',errors='replace'),(folder/'stderr.log').read_text('utf8',errors='replace')
    commands='''set -eu
mkdir -p /home/USER/e3-lab/tool-probe
cd /home/USER/e3-lab/tool-probe
make -j1 -f /workspace/projects/ysyx_f_to_b/E/E3/tool_probe/Makefile all
./good
'''
    out,err=linux('make_and_execute',commands)
    assert 'PASS E2 linked_list selftest operations=20000 live_nodes=0' in out
    out,err=linux('valgrind_positive','cd /home/USER/e3-lab/tool-probe\nvalgrind --error-exitcode=99 --leak-check=full --show-leak-kinds=all ./good',timeout=60)
    assert 'ERROR SUMMARY: 0 errors' in err and 'in use at exit: 0 bytes in 0 blocks' in err
    out,err=linux('valgrind_negative','cd /home/USER/e3-lab/tool-probe\nvalgrind --error-exitcode=99 --leak-check=full --show-leak-kinds=all ./bad_memory',expected=99)
    assert 'Invalid write of size 1' in err and re.search(r'definitely lost:\s+17 bytes in 1 blocks',err)
    command="cd /home/USER/e3-lab/tool-probe\ngdb --batch -q -ex 'set pagination off' -ex 'break list_insert' -ex run -ex 'print value' -ex 'print index' -ex bt -ex 'delete breakpoints' -ex continue ./good"
    out,err=linux('gdb',command)
    assert re.search(r'\$1\s*=\s*4\b',out) and re.search(r'\$2\s*=\s*18446744073709551615\b',out) and 'list_insert' in out and 'main' in out and 'exited normally' in out
    command='''set -eu
repo=/home/USER/e3-lab/git-tool-probe
if [ ! -d "$repo/.git" ]; then
    git init -b main "$repo"
    git -C "$repo" config user.name 'YSYX Local Tool Probe'
    git -C "$repo" config user.email 'ysyx-tool-probe@example.invalid'
    printf 'local tool probe\\n' > "$repo/probe.txt"
    git -C "$repo" add probe.txt
    git -C "$repo" commit -m 'Record isolated Linux Git tool probe'
fi
git -C "$repo" fsck --full
test -z "$(git -C "$repo" status --porcelain)"
git -C "$repo" show --format=fuller --stat HEAD
git -C "$repo" show HEAD:probe.txt
'''
    out,err=linux('git',command);assert 'local tool probe' in out and 'probe.txt' in out
    command='''set -eu
gcc --version
gdb --version
make --version
git --version
valgrind --version
sha256sum /usr/bin/x86_64-linux-gnu-gcc-11 /usr/bin/gdb /usr/bin/make /usr/bin/git /usr/bin/valgrind
uname -a
id
'''
    out,err=linux('versions',command)
    versions=out
    report={'status':'PASS','task':'E3-M001 tool capability portion','scope':'Real installed WSL2 Ubuntu Linux, dedicated local ysyx user; Make/GCC compilation, 20000-op C selftest, GDB real break/argument inspection, Valgrind positive/negative, local Git fsck/commit. No external publishing.','resource_budget':'User-authorized temporary1GB; one tiny compilation at a time; make-j1; no heavy builds.','runs':items,'versions_and_fingerprints':versions,'timestamp':datetime.now(timezone.utc).isoformat()}
    dump(ROOT/'reports/E3_toolchain.json',report);print('E3_TOOLS PASS real Linux positive/negative validation',flush=True)

if __name__=='__main__':main()
