from common import *
import shutil,socket

def setup():
    b=LAB/'ssh';b.mkdir(exist_ok=True);os.chmod(b,0o700)
    user_ssh=Path.home()/'.ssh';user_ssh.mkdir(mode=0o700,exist_ok=True)
    if (user_ssh/'authorized_keys').exists():assert (user_ssh/'.ysyx-lab').exists(),'Preserve unrelated authorized_keys'
    (user_ssh/'.ysyx-lab').touch()
    for name in ('bootstrap','client'):
        key=b/name
        if not key.exists():run('ssh/keygen_'+name,['ssh-keygen','-o','-a','100','-t','ed25519','-N','','-C','ephemeral-local-ysyx-lab','-f',str(key)])
        os.chmod(key,0o600)
    authorized=user_ssh/'authorized_keys';authorized.write_text((b/'bootstrap.pub').read_text());os.chmod(authorized,0o600)
    server=f'''Port 22222
ListenAddress 127.0.0.1
HostKey /etc/ssh/ssh_host_ed25519_key
PidFile {b}/sshd.pid
AuthorizedKeysFile .ssh/authorized_keys
AllowUsers ysyx
PubkeyAuthentication yes
PasswordAuthentication yes
PermitRootLogin prohibit-password
UsePAM yes
PrintMotd no
'''
    (b/'sshd_config').write_text(server)
    print('SSH_FIXTURE_READY_PRIVATE_KEYS_NOT_EXPORTED',flush=True)

def test():
    b=LAB/'ssh';known=b/'known_hosts'
    o,e,r=run('ssh/scan',['ssh-keyscan','-p','22222','-t','ed25519','127.0.0.1'])
    pub=Path('/etc/ssh/ssh_host_ed25519_key.pub').read_text().split()
    assert o.split()[1:3]==pub[:2];known.write_text(o)
    opts=['-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(known),'-o','IdentitiesOnly=yes','-p','22222']
    run('ssh/copy_id',['ssh-copy-id','-f','-i',str(b/'client.pub'),'-o','IdentityFile='+str(b/'bootstrap'),*opts,'ysyx@127.0.0.1'],timeout=30)
    conf=Path.home()/'.ssh/config';conf.parent.mkdir(mode=0o700,exist_ok=True)
    if conf.exists():shutil.copyfile(conf,b/('config.backup-'+str(time.time_ns())))
    conf.write_text(f'''Host vm
    HostName 127.0.0.1
    Port 22222
    User ysyx
    IdentityFile {b}/client
    IdentitiesOnly yes
    UserKnownHostsFile {known}
    StrictHostKeyChecking yes
    LocalForward 127.0.0.1:9999 127.0.0.1:8888
''');os.chmod(conf,0o600)
    o,e,r=run('ssh/key_login',['ssh','-F',str(conf),'vm','id -un']);assert o.strip()=='ysyx'
    web=b/'web';web.mkdir(exist_ok=True);(web/'probe.txt').write_text('YSYX_SSH_TUNNEL_OK\n')
    serverlog=(b/'http.log').open('wb');http=subprocess.Popen(['python3','-m','http.server','8888','--bind','127.0.0.1','--directory',str(web)],stdout=serverlog,stderr=serverlog)
    ctl=b/'control.sock'
    try:
        run('ssh/tunnel_start',['ssh','-F',str(conf),'-M','-S',str(ctl),'-o','ExitOnForwardFailure=yes','-fN','vm'])
        time.sleep(.2);o,e,r=run('ssh/tunnel_get',['curl','--fail','--silent','--max-time','5','http://127.0.0.1:9999/probe.txt']);assert o=='YSYX_SSH_TUNNEL_OK\n'
        run('ssh/tunnel_check',['ssh','-F',str(conf),'-S',str(ctl),'-O','check','vm'])
    finally:
        run('ssh/tunnel_stop',['ssh','-F',str(conf),'-S',str(ctl),'-O','exit','vm'])
        http.terminate();http.wait(timeout=5);serverlog.close()
    record([f'MS-05-{i:02}' for i in range(12,16)]+['MS-05-18'],'PASS_ADAPTED',['ssh/key_login','ssh/copy_id','ssh/tunnel_get','ssh/tunnel_check'],'Real ephemeral-key SSH and TCP forwarding on isolated loopback server in this VM, not an external account. -N executes no remote command; -f backgrounds after authentication. Private keys stay outside exported project.')
    script=b/'harden.vim';script.write_text('%s/^PasswordAuthentication yes$/PasswordAuthentication no/\n%s/^PermitRootLogin prohibit-password$/PermitRootLogin no/\nwq\n')
    run('ssh/harden_vim',['vim','-Nu','NONE','-n','-i','NONE','-es','-S',str(script),str(b/'sshd_config')],inputs=[script])
    print('SSH_NEEDS_RELOAD_THEN_CHECK',flush=True)

def after():
    conf=Path.home()/'.ssh/config'
    o,e,r=run('ssh/after_hardening',['ssh','-F',str(conf),'vm','id -un']);assert o.strip()=='ysyx'
    o,e,r=run('ssh/no_password',['ssh','-F',str(conf),'-o','PreferredAuthentications=password','-o','BatchMode=yes','vm','true'],expected=(255,));assert 'Permission denied' in e
    record(['MS-05-16'],'PASS_ADAPTED',['ssh/harden_vim','ssh/after_hardening','ssh/no_password','ssh/effective_settings.txt'],'Actual Vim edit and server reload; effective PasswordAuthentication=no and PermitRootLogin=no, public-key login remains working. Isolated server config rather than global sshd service.')

def dotfiles():
    repo=LAB/'dotfiles';repo.mkdir(exist_ok=True)
    extra=repo/'bash_extra';extra.write_text("alias dc='cd'\nalias ll='ls -alh'\nPS1='[ysyx-lab] \\w $ '\n")
    bashrc=Path.home()/'.bashrc';text=bashrc.read_text()
    if '# YSYX dotfiles' not in text:text+='\n# YSYX dotfiles\nsource ~/.bash_extra\n'
    backing=LAB/'dotfile-backups';backing.mkdir(exist_ok=True)
    names=['.bashrc','.profile','.bash_logout','.vimrc','.gitconfig','.gitignore_global']
    for name in names:
        src=Path.home()/name
        if src.exists() and not src.is_symlink():shutil.copyfile(src,backing/(name+'.'+str(time.time_ns())))
        content=text if name=='.bashrc' else src.read_text()
        (repo/name[1:]).write_text(content)
    installer=repo/'install.sh';installer.write_text('''#!/bin/bash
set -euo pipefail
repo_dir=$(cd -- "$(dirname -- "$0")" && pwd)
target_dir=$1
test -d "$target_dir"
for name in bashrc profile bash_logout vimrc gitconfig gitignore_global bash_extra; do
 target="$target_dir/.$name"
 if [ -e "$target" ] || [ -L "$target" ]; then
  if [ "$(readlink -f "$target")" != "$repo_dir/$name" ]; then
   backup_dir="$target_dir/.dotfile-backups/$(date +%Y%m%dT%H%M%S%N)"
   mkdir -p "$backup_dir"
   mv -- "$target" "$backup_dir/.$name"
   ln -s "$repo_dir/$name" "$target"
  fi
 else
  ln -s "$repo_dir/$name" "$target"
 fi
done
''')
    for name in names:
        target=Path.home()/name
        if not target.is_symlink():
            assert target.parent==Path.home();target.unlink() # Backed up above; these are this task's dedicated Linux-user configs.
    run('dotfiles/install',['bash',str(installer),str(Path.home())],inputs=[installer])
    o,e,r=run('dotfiles/use',['bash','-ic','dc /tmp; test "$PWD" = /tmp; alias dc; printf "%s\\n" "$PS1"']);assert 'ysyx-lab' in o
    if not (repo/'.git').exists():
        run('dotfiles/init',['git','init','-b','main'],cwd=repo)
        run('dotfiles/name',['git','config','user.name','YSYX Local Lab'],cwd=repo)
        run('dotfiles/email',['git','config','user.email','ysyx-lab@example.invalid'],cwd=repo)
        run('dotfiles/add',['git','add','.'],cwd=repo);run('dotfiles/commit',['git','commit','-m','Version isolated Linux course configuration'],cwd=repo)
    run('dotfiles/fsck',['git','fsck','--full'],cwd=repo)
    record(['MS-05-06','MS-05-07','MS-05-08','MS-05-10'],'PASS',['dotfiles/install','dotfiles/use','dotfiles/fsck'],'Dedicated Linux lab-account plain-text settings backed up, versioned and symlinked; private SSH keys and Windows settings excluded.')
    record(['MS-05-11'],'NOT_PUBLISHED_PERSONAL_ACTION',['dotfiles/fsck'],'Local dotfiles repository prepared; no unrequested publication to the user GitHub account.')
    print('DOTFILES_READY',flush=True)

if __name__=='__main__':globals()[sys.argv[1]]()
