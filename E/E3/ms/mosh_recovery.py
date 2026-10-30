from common import *
import socket,threading,select,pty,fcntl,termios,struct,signal,re,resource

def main():
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    env=os.environ.copy();env.update(LC_ALL='C.UTF-8',LANG='C.UTF-8',SHELL='/bin/bash',TERM='xterm')
    command=['mosh-server','new','-i','127.0.0.1','-p','60011','-c','256','--','/bin/bash','--noprofile','--norc','-i']
    start=subprocess.run(command,env=env,capture_output=True,timeout=10);assert start.returncode==0
    match=re.search(rb'MOSH CONNECT (\d+) (\S+)',start.stdout);assert match
    key=match[2].decode();server_pid=int(re.search(rb'pid = (\d+)',start.stderr)[1])
    listen=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);listen.bind(('127.0.0.1',60012))
    upstream=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);upstream.bind(('127.0.0.1',0))
    state={'drop':False,'stop':False,'peer':None,'dropped':0,'forwarded':0}
    def proxy():
        while not state['stop']:
            for sock in select.select([listen,upstream],[],[],.05)[0]:
                data,peer=sock.recvfrom(65536)
                if sock is listen:state['peer']=peer
                if state['drop']:state['dropped']+=1;continue
                if sock is listen:upstream.sendto(data,('127.0.0.1',60011))
                elif state['peer']:listen.sendto(data,state['peer'])
                state['forwarded']+=1
    thread=threading.Thread(target=proxy,daemon=True);thread.start()
    pid,fd=pty.fork()
    if pid==0:
        fcntl.ioctl(0,termios.TIOCSWINSZ,struct.pack('HHHH',24,80,0,0))
        env['MOSH_KEY']=key;env['MOSH_PREDICTION_DISPLAY']='never'
        os.execvpe('mosh-client',['mosh-client','127.0.0.1','60012'],env)
    transcript=bytearray()
    def pump(seconds):
        end=time.monotonic()+seconds
        while time.monotonic()<end:
            if select.select([fd],[],[],.05)[0]:
                try:b=os.read(fd,65536)
                except OSError:return
                transcript.extend(b)
    def visible():
        return re.sub(rb'\x1b\[[0-?]*[ -/]*[@-~]',b'',bytes(transcript))
    def send_token(token):
        escaped=''.join('\\x'+format(b,'02x') for b in token.encode())
        os.write(fd,("printf '"+escaped+"\\n'\r").encode())
    try:
        pump(1);send_token('MOSH_BEFORE_OK')
        for _ in range(20):
            pump(.2)
            if b'MOSH_BEFORE_OK' in visible():break
        assert b'MOSH_BEFORE_OK' in visible()
        state['drop']=True;send_token('MOSH_RECOVER_OK');pump(3)
        assert b'MOSH_RECOVER_OK' not in visible() and state['dropped']>0
        state['drop']=False
        for _ in range(50):
            pump(.2)
            if b'MOSH_RECOVER_OK' in visible():break
        assert b'MOSH_RECOVER_OK' in visible()
        os.write(fd,b'exit\r');pump(.5)
        result={'status':'PASS_ADAPTED','server_command':command,'drop_seconds':3,'dropped_datagrams':state['dropped'],'forwarded_datagrams':state['forwarded'],'before_token_observed':True,'no_delivery_during_drop':True,'recovery_token_observed':True,'key_exported':False,'scope':'Real Mosh server/client through loopback UDP relay. Packet loss substituted for disabling a host/VM adapter; no Windows networking changes.'}
        dump(OUT/'terminal/mosh_result.json',result)
        record(['MS-05-17'],'PASS_ADAPTED',['terminal/mosh_result.json','terminal/mosh.pty'],'Actual Mosh session survived3s bidirectional UDP packet drop. Test tokens encoded in shell input prevent input echo from being mistaken for server output.')
    finally:
        try:
            if os.waitpid(pid,os.WNOHANG)[0]==0:os.kill(pid,signal.SIGTERM);os.waitpid(pid,0)
        except ChildProcessError:pass
        try:os.kill(server_pid,signal.SIGTERM)
        except ProcessLookupError:pass
        state['stop']=True;thread.join(timeout=1);listen.close();upstream.close();os.close(fd)
        (OUT/'terminal/mosh.pty').write_bytes(bytes(transcript).replace(key.encode(),b'[REDACTED]'))
    print('MOSH_REAL_PACKET_LOSS_RECOVERY_PASS',flush=True)
if __name__=='__main__':main()
