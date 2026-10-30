"""Rebuild selected completed work from packaged local sources in a fresh directory.

No HTTP request, remote Git fetch, package install, or system setting change.
Installed Linux compiler/debugging tools remain explicit prerequisites.
"""
from pathlib import Path
import sys,json,shutil,subprocess,tempfile,tarfile,os,pwd,platform,datetime,re
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'E/E3/ms'))
from common import run,sha,dump,PROJECT

def main():
    work=Path(tempfile.mkdtemp(prefix='offline-check-',dir='/home/USER/e3-lab'))
    offline=PROJECT/'E/E3/offline';manifest=json.loads((offline/'manifest.json').read_text())
    for row in manifest['files']:assert sha(PROJECT/row['path'])==row['sha256']
    for row in manifest['repos']:assert sha(PROJECT/row['archive'])==row['sha256']
    course=work/'course';bundle=offline/'resources/course.bundle'
    run('offline/course_clone',['git','clone',str(bundle),str(course)],inputs=[bundle],timeout=60)
    o,e,r=run('offline/course_commit',['git','-C',str(course),'rev-parse','HEAD'])
    assert o.strip()==next(x for x in manifest['repos'] if x['name']=='course')['commit']
    run('offline/course_fsck',['git','-C',str(course),'fsck','--full'],timeout=60)
    for name in ['ctrlp','commentary']:
        with tarfile.open(offline/'resources'/(name+'.tar.gz')) as t:
            dest=work/name;dest.mkdir()
            for member in t.getmembers():
                assert (dest/member.name).resolve().is_relative_to(dest.resolve()) and not member.issym() and not member.islnk()
            t.extractall(dest)
        assert any(dest.iterdir())
    dot=work/'dotfiles';run('offline/dotfiles_clone',['git','clone',str(offline/'ms/dotfiles.bundle'),str(dot)])
    home=work/'fresh-home';home.mkdir()
    for n in (1,2):run('offline/dotfiles_install_'+str(n),['bash',str(dot/'install.sh'),str(home)])
    o,e,r=run('offline/dotfiles_use',['env','HOME='+str(home),'bash','--noprofile','--norc','-c','source "$HOME/.bash_extra"; alias dc; test -L "$HOME/.gitconfig"'])
    assert "alias dc='cd'" in o
    source=PROJECT/'E/E3/lcthw/solutions/continued'
    shutil.copytree(source/'c_skeleton',work/'skeleton')
    o,e,r=run('offline/skeleton_build',['make','-j2','all'],cwd=work/'skeleton');assert 'PASS' in o
    dbsource=work/'database.c';shutil.copyfile(source/'database.c',dbsource);db=work/'database'
    run('offline/database_build',['gcc','-std=gnu17','-Wall','-O2','-g',str(dbsource),'-o',str(db)],inputs=[dbsource])
    file=work/'sample.db'
    for tag,args in [('create',['c','32','4']),('set',['s','2','Ada','ada@example.invalid','Offline','36'])]:
        run('offline/database_'+tag,[str(db),str(file),*args],inputs=[db])
    o,e,r=run('offline/database_get',['valgrind','--error-exitcode=99','--leak-check=full',str(db),str(file),'g','2'],inputs=[db,file])
    assert o=='2\tAda\tada@example.invalid\tOffline\t36\n' and 'ERROR SUMMARY: 0 errors' in e
    assert len(file.read_bytes())==32+4*(5+3*32)
    bad=work/'corrupt.db';data=bytearray(file.read_bytes());data[-1]^=1;bad.write_bytes(data)
    o,e,r=run('offline/database_reject_corruption',[str(db),str(bad),'g','2'],expected=(1,),inputs=[db,bad]);assert 'checksum mismatch' in e
    # Fresh linkage ensures tests do not accidentally reuse a stale executable.
    shutil.copytree(source/'lists',work/'lists')
    for name in ['list_extensions.c','list_property.c']:shutil.copyfile(source/name,work/name)
    cpp=[work/'lists/list.c',work/'lists/algos.c',work/'list_extensions.c',work/'list_property.c'];exe=work/'list_check'
    run('offline/lists_build',['gcc','-std=gnu17','-Wall','-O0','-g','-I'+str(work/'lists'),*map(str,cpp),'-o',str(exe)],inputs=cpp)
    o,e,r=run('offline/lists_check',['valgrind','--error-exitcode=99','--leak-check=full',str(exe)],inputs=[exe],timeout=60)
    assert 'PASS 3000' in o and 'ERROR SUMMARY: 0 errors' in e
    tools={}
    for name in ['gcc','make','gdb','git','valgrind','vim','tmux','mosh-client','sshd','curl','python3','xxd']:
        p=shutil.which(name) or ('/usr/sbin/sshd' if name=='sshd' else None)
        assert p and Path(p).is_file(),name
        tools[name]={'path':p,'resolved':str(Path(p).resolve()),'sha256':sha(p)}
    custom=Path('/home/USER/tools/valgrind-3.18.1-source/bin/valgrind')
    tools['source_built_valgrind']={'path':str(custom),'sha256':sha(custom)}
    o,e,r=run('offline/private_valgrind_version',[str(custom),'--version'],inputs=[custom]);assert 'valgrind-3.18.1' in o
    packages=['gcc','make','gdb','git','valgrind','vim','tmux','mosh','openssh-server','curl','python3','zip','unzip','wamerican','man-db','manpages-dev']
    o,e,r=run('offline/package_versions',['dpkg-query','-W','-f=${Package}\t${Version}\t${Architecture}\n',*packages])
    versions=[dict(zip(['package','version','architecture'],line.split('\t'))) for line in o.splitlines()]
    mem={line.split(':')[0]:int(line.split()[1]) for line in Path('/proc/meminfo').read_text().splitlines()}
    w=Path('/home/USER/ysyx-workbench')
    commit=subprocess.check_output(['git','-C',str(w),'rev-parse','HEAD'],text=True).strip()
    assert commit=='a839def3f3b046f730537ea420d3075e725d27ce'
    assert not subprocess.check_output(['git','-C',str(w),'status','--porcelain'],text=True)
    assert os.cpu_count()==4 and 1800000<mem['MemTotal']<=2097152 and mem['SwapTotal']==2097152
    listeners=subprocess.check_output(['ss','-H','-ltnu'],text=True)
    assert not re.search(r':(?:22222|8888|9999)\s',listeners),listeners
    env={'user':pwd.getpwuid(os.getuid()).pw_name,'uid':os.getuid(),'kernel':platform.release(),'processors':os.cpu_count(),'mem_total_kib':mem['MemTotal'],'swap_total_kib':mem['SwapTotal'],'workbench_commit':commit,'workbench_dirty':False,'lab_ssh_and_http_ports_closed':True}
    result={'status':'PASS','timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fresh_directory':str(work),'network_requests':0,'scope':'Local bundle clone/fsck, plugin source extraction, dotfiles idempotence, fresh Make/C builds, DB positive/corruption controls, linked-list model/Valgrind checks. Installed tools are prerequisites; this is not a full OS image.','environment':env,'tools':tools,'packages':versions,'offline_manifest_sha256':sha(offline/'manifest.json')}
    dump(PROJECT/'reports/E3_offline_verification.json',result)
    print('OFFLINE_VERIFICATION_PASS',flush=True)

if __name__=='__main__':main()
