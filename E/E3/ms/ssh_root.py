from pathlib import Path
import os,sys,signal,subprocess
assert os.geteuid()==0
base=Path('/home/USER/e3-lab/missing-semester/ssh')
pidfile=base/'sshd.pid';config=base/'sshd_config'
if sys.argv[1]=='freshuser':
    if subprocess.run(['id','ysyx-dotcheck'],capture_output=True).returncode:subprocess.run(['useradd','-m','-s','/bin/bash','ysyx-dotcheck'],check=True)
elif sys.argv[1]=='start':
    Path('/run/sshd').mkdir(exist_ok=True)
    assert 'ListenAddress 127.0.0.1' in config.read_text() and 'Port 22222' in config.read_text()
    subprocess.run(['/usr/sbin/sshd','-t','-f',str(config)],check=True)
    subprocess.run(['/usr/sbin/sshd','-f',str(config),'-E',str(base/'sshd.log')],check=True)
elif sys.argv[1] in ('stop','reload'):
    if pidfile.exists():
        pid=int(pidfile.read_text());cmd=Path(f'/proc/{pid}/cmdline')
        if cmd.exists():
            assert str(config).encode() in cmd.read_bytes()
            os.kill(pid,signal.SIGTERM if sys.argv[1]=='stop' else signal.SIGHUP)
elif sys.argv[1]=='check':
    subprocess.run(['/usr/sbin/sshd','-T','-f',str(config),'-C','user=ysyx,host=vm,addr=127.0.0.1'],check=True)
