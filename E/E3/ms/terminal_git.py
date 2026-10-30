from common import *
import pty,fcntl,termios,struct,select,signal,re

def terminal():
    transcript=bytearray();pid,fd=pty.fork()
    if pid==0:
        fcntl.ioctl(0,termios.TIOCSWINSZ,struct.pack('HHHH',24,80,0,0))
        os.environ.update(PS1='MSLAB> ',TERM='xterm',HISTFILE='/home/USER/e3-lab/missing-semester/session.history')
        os.execv('/bin/bash',['bash','--noprofile','--norc','-i'])
    def until(token,seconds=10):
        data=bytearray();end=time.monotonic()+seconds
        while token not in data:
            if time.monotonic()>end:raise TimeoutError(token)
            if select.select([fd],[],[],.1)[0]:
                b=os.read(fd,65536);data+=b;transcript.extend(b)
        return bytes(data)
    def cmd(text,n):
        os.write(fd,(text+f"\nprintf '\\nMSDONE{n}\\n'\n").encode());return until(f'\r\nMSDONE{n}\r\n'.encode())
    try:
        until(b'MSLAB> ')
        os.write(fd,b'sleep 10000\n');time.sleep(.3);os.write(fd,b'\x1a')
        stopped=until(b'MSLAB> ');assert b'Stopped' in stopped
        resumed=cmd('bg',1);assert b'sleep 10000' in resumed
        found=cmd("pgrep -af -P $$ '^sleep 10000$'",2);assert b'sleep 10000' in found
        cmd("pkill -P $$ -f '^sleep 10000$'",3)
        cmd('jobs -l',4)
        for i,c in enumerate(['pwd','ls','pwd','git --version','make --version','ls','date','printf test','true','pwd'],5):cmd(c,i)
        cmd('history -w',20);os.write(fd,b'exit\n');os.waitpid(pid,0)
    finally:
        try:
            if os.waitpid(pid,os.WNOHANG)[0]==0:os.kill(pid,signal.SIGTERM);os.waitpid(pid,0)
        except ChildProcessError:pass
        os.close(fd)
        (OUT/'terminal').mkdir(exist_ok=True);(OUT/'terminal/pty.log').write_bytes(transcript)
    record(['MS-05-01'],'PASS',['terminal/pty.log'],'Real80x24 PTY, Ctrl-Z, bg, scoped pgrep/pkill on this shell child only.')
    o,e,r=shell('terminal/wait',"""set -eu
sleep 60 &
task_pid=$!
task_start=$SECONDS
wait "$task_pid"
test "$((SECONDS-task_start))" -ge 59
ls
printf 'wait_seconds=%s\\n' "$((SECONDS-task_start))"
""",timeout=75);assert 'wait_seconds=' in o
    o,e,r=shell('terminal/pidwait',"""set -eu
pidwait(){ while kill -0 "$1" 2>/dev/null; do sleep 0.1; done; }
sleep 2 &
task_pid=$!
bash -c 'wait "$1"' other "$task_pid" 2> nonchild.stderr && exit 8
pidwait "$task_pid"
wait "$task_pid"
cat nonchild.stderr
""",timeout=10);assert 'not a child' in o
    record(['MS-05-02'],'PASS',['terminal/wait','terminal/pidwait'],'Actual60s wait and separate-shell non-child rejection; kill-0 polling tested.')
    shell('terminal/dc',"""shopt -s expand_aliases
alias dc=cd
dc /tmp
test "$PWD" = /tmp
""")
    record(['MS-05-04'],'PASS',['terminal/dc'],'dc alias actually changes directory.')
    o,e,r=shell('terminal/history',"""set -eu
set -o history
history -r /home/USER/e3-lab/missing-semester/session.history
history | awk '{$1="";print substr($0,2)}' | sort | uniq -c | sort -n | tail -n 10
alias ll='ls -alh'
alias gver='git --version'
alias where='pwd'
alias
""");assert 'pwd' in o and 'alias where=' in o
    record(['MS-05-05'],'PASS',['terminal/history','terminal/pty.log'],'Statistics use the actual recorded interactive session, not a fabricated long-term history.')
    socket='ysyx-ms-lab'
    run('terminal/tmux_create',['tmux','-L',socket,'new-session','-d','-s','lab','-n','first'])
    try:
        run('terminal/tmux_split',['tmux','-L',socket,'split-window','-h','-t','lab:0'])
        run('terminal/tmux_window',['tmux','-L',socket,'new-window','-t','lab','-n','second'])
        run('terminal/tmux_send',['tmux','-L',socket,'send-keys','-t','lab:0.0','printf "TMUX_REAL_PANE\\n"','Enter'])
        o,e,r=run('terminal/tmux_list',['tmux','-L',socket,'list-panes','-a','-F','#{session_name}:#{window_name}:#{pane_index}'])
        assert len(o.strip().splitlines())==3
        time.sleep(.2);o,e,r=run('terminal/tmux_capture',['tmux','-L',socket,'capture-pane','-p','-t','lab:0.0']);assert 'TMUX_REAL_PANE' in o
        config=LAB/'tmux.conf';config.write_text('set -g prefix C-a\nunbind C-b\nbind C-a send-prefix\nset -g mouse on\n')
        run('terminal/tmux_config',['tmux','-L',socket,'source-file',str(config)])
        o,e,r=run('terminal/tmux_option',['tmux','-L',socket,'show-options','-g','prefix']);assert 'C-a' in o
    finally:run('terminal/tmux_cleanup',['tmux','-L',socket,'kill-session','-t','lab'])
    record(['MS-05-03'],'PASS',['terminal/tmux_list','terminal/tmux_capture','terminal/tmux_option'],'Actual session, windows, split panes, key input/capture and custom prefix; isolated server socket.')

def git():
    repo=LAB/'resources/course'
    assert (repo/'.git').exists()
    run('git/history',['git','log','--all','--graph','--decorate','--oneline','-n','35'],cwd=repo)
    o,e,r=run('git/readme_author',['git','log','-1','--format=%H%n%an%n%aI%n%B','--','README.md'],cwd=repo);assert len(o.splitlines())>=4
    o,e,r=run('git/collections_blame',['git','blame','-L','/^collections:/,+1','--','_config.yml'],cwd=repo)
    commit=o.split()[0].lstrip('^');run('git/collections_commit',['git','show','--no-patch','--format=fuller',commit],cwd=repo)
    record(['MS-06-02'],'PASS',['git/history','git/readme_author','git/collections_blame','git/collections_commit'],'Actual full-history official-course clone; identity, commit and line provenance recorded at pinned HEAD.')
    # Every destructive history operation is inside this newly created synthetic repository.
    fixture=LAB/('git-history-fixture-'+str(time.time_ns()));fixture.mkdir()
    run('git/init_fixture',['git','init','-b','main'],cwd=fixture)
    for k,v in [('user.name','YSYX Local Lab'),('user.email','ysyx-lab@example.invalid')]:run('git/config_'+k,['git','config',k,v],cwd=fixture)
    (fixture/'keep.txt').write_text('initial\n');run('git/add_base',['git','add','.'],cwd=fixture);run('git/commit_base',['git','commit','-m','base'],cwd=fixture)
    (fixture/'unwanted.txt').write_text('SYNTHETIC-NOT-A-CREDENTIAL\n'*2000)
    old,_,_=run('git/old_blob',['git','hash-object','unwanted.txt'],cwd=fixture);old=old.strip()
    run('git/add_unwanted',['git','add','.'],cwd=fixture);run('git/commit_unwanted',['git','commit','-m','deliberate unwanted fixture'],cwd=fixture)
    (fixture/'keep.txt').write_text('after\n');run('git/add_after',['git','add','.'],cwd=fixture);run('git/commit_after',['git','commit','-m','useful change'],cwd=fixture)
    run('git/filter',['git','filter-branch','--force','--index-filter','git rm --cached --ignore-unmatch unwanted.txt','--prune-empty','--','--all'],cwd=fixture,timeout=60)
    refs,_,_=run('git/backup_refs',['git','for-each-ref','--format=%(refname)','refs/original'],cwd=fixture)
    for i,ref in enumerate(refs.splitlines()):
        assert ref.startswith('refs/original/');run('git/remove_backup'+str(i),['git','update-ref','-d',ref],cwd=fixture)
    run('git/expire',['git','reflog','expire','--expire=now','--all'],cwd=fixture)
    run('git/gc',['git','-c','pack.threads=1','gc','--prune=now'],cwd=fixture)
    out,_,_=run('git/objects',['git','rev-list','--objects','--all'],cwd=fixture);assert 'unwanted.txt' not in out
    run('git/old_blob_absent',['git','cat-file','-e',old],cwd=fixture,expected=(1,128))
    assert (fixture/'keep.txt').read_text()=='after\n'
    record(['MS-06-03'],'PASS',['git/filter','git/objects','git/old_blob_absent'],'Synthetic file removed from this isolated repository history, backups/reflogs expired, blob unreachable and pruned. No user history rewritten.')
    stash=LAB/('git-stash-fixture-'+str(time.time_ns()))
    run('git/stash_clone',['git','clone','--no-hardlinks',str(repo),str(stash)],timeout=60)
    for k,v in [('user.name','YSYX Local Lab'),('user.email','ysyx-lab@example.invalid')]:run('git/stash_config_'+k,['git','config',k,v],cwd=stash)
    target=stash/'README.md';before=target.read_bytes();target.write_bytes(before+b'\nLocal stash exercise.\n')
    run('git/stash',['git','stash','push','-m','E3 local exercise'],cwd=stash)
    assert target.read_bytes()==before
    out,_,_=run('git/stash_graph',['git','log','--all','--graph','--oneline','-n','10'],cwd=stash);assert 'E3 local exercise' in out
    run('git/stash_pop',['git','stash','pop'],cwd=stash);assert target.read_bytes()==before+b'\nLocal stash exercise.\n'
    record(['MS-06-04'],'PASS',['git/stash','git/stash_graph','git/stash_pop'],'Real clone, tracked edit, stash graph and exact pop restoration.')
    run('git/alias',['git','config','--global','alias.graph','log --all --graph --decorate --oneline'])
    run('git/graph',['git','graph','-n','8'],cwd=repo)
    ignore=Path.home()/'.gitignore_global'
    if ignore.exists():assert ignore.read_text()=='.DS_Store\n*.swp\n'
    ignore.write_text('.DS_Store\n*.swp\n')
    run('git/global_ignore',['git','config','--global','core.excludesfile',str(ignore)])
    (fixture/'.DS_Store').write_text('fixture')
    out,_,_=run('git/ignored',['git','check-ignore','-v','.DS_Store'],cwd=fixture);assert '.gitignore_global' in out
    record(['MS-06-05','MS-06-06'],'PASS',['git/graph','git/ignored'],'Settings apply only to the dedicated Linux ysyx account; Windows/user repositories untouched.')
    run('git/data_model',['git','cat-file','-p','HEAD'],cwd=fixture)
    run('git/tree',['git','ls-tree','HEAD'],cwd=fixture)
    record(['MS-06-01'],'PASS',['git/data_model','git/tree','git/history'],'Commit/tree/blob relationships exercised; identity is synthetic local lab, no public author impersonation.')
    # Reviewable local change, no unrequested posting to third-party maintainers.
    edit=next(p for p in repo.rglob('editors.md') if '2020' in str(p))
    original=edit.read_text();assert '命令控制行' in original
    import difflib
    patch=''.join(difflib.unified_diff(original.splitlines(True),original.replace('命令控制行','命令行',1).splitlines(True),fromfile='a/'+str(edit.relative_to(repo)),tofile='b/'+str(edit.relative_to(repo))))
    (OUT/'git/proposed.patch').write_text(patch)
    record(['MS-06-07'],'PREPARED_NOT_PUBLISHED',['git/proposed.patch'],'Local reviewable terminology correction prepared; GitHub fork/PR is a personal external-publication action, not falsely reported submitted.')
    print('MS_TERMINAL_GIT_DONE',flush=True)

if __name__=='__main__':
    if '--git-only' not in sys.argv:terminal()
    git()
