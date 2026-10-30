"""Client for the official ECC Content-Length JSON-RPC transport used by ECOS.
Methods/fields are taken from the archived public runtime source, not guessed.
"""
from common import *
import select
class Rpc:
 def __init__(self,tag,env=None):
  self.dir=ROOT/'artifacts'/tag;self.dir.mkdir(parents=True,exist_ok=True);self.ident=0;self.buffer=b'';self.messages=[]
  if (self.dir/'protocol.json').exists():
   previous=self.dir/'attempts'/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f');previous.mkdir(parents=True)
   for file in self.dir.iterdir():
    if file.is_file():shutil.copyfile(file,previous/file.name)
  lock=json.loads((ROOT/'reports/E_backend_compatible_tools.json').read_text());self.ecc=Path(lock['ecc']);variables=os.environ.copy();variables.update(PATH=lock['yosys_root']+'/bin:'+variables['PATH'],OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',CUDA_VISIBLE_DEVICES='',SHELL='/bin/bash')
  if env:variables.update(env)
  self.err=(self.dir/'stderr.log').open('wb');self.p=subprocess.Popen([self.ecc,'rpc','serve','--stdio'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.err,env=variables,cwd=WORK)
  self.hello=self.call('rpc.hello',{'version':1});assert self.hello['version']==1
 def receive(self,timeout):
  end=time.monotonic()+timeout
  while True:
   if b'\r\n\r\n' in self.buffer:
    header,body=self.buffer.split(b'\r\n\r\n',1);fields=dict(line.split(b':',1) for line in header.split(b'\r\n'));length=int(fields[b'Content-Length'].strip())
    if len(body)>=length:self.buffer=body[length:];return json.loads(body[:length])
   left=end-time.monotonic()
   if left<=0:raise TimeoutError('ECC RPC response deadline')
   ready,_,_=select.select([self.p.stdout],[],[],left)
   if not ready:raise TimeoutError('ECC RPC response deadline')
   data=os.read(self.p.stdout.fileno(),65536)
   if not data:raise RuntimeError('ECC RPC process closed stdout')
   self.buffer+=data
 def call(self,method,params,timeout=60,allow_error=False):
  self.ident+=1;request={'jsonrpc':'2.0','id':self.ident,'method':method,'params':params};body=json.dumps(request,separators=(',',':')).encode();start=time.monotonic()
  self.p.stdin.write(b'Content-Length: '+str(len(body)).encode()+b'\r\n\r\n'+body);self.p.stdin.flush()
  self.messages.append({'direction':'request','timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'payload':request})
  while True:
   response=self.receive(timeout);self.messages.append({'direction':'response','payload':response,'elapsed_seconds':time.monotonic()-start});dump(self.dir/'protocol.json',self.messages)
   if response.get('id')==self.ident:
    if 'error' in response and not allow_error:raise RuntimeError(response['error'])
    return response if allow_error else response['result']
 def close(self):
  if self.p.poll() is None:
   try:self.call('rpc.shutdown',{},timeout=10)
   except Exception:self.p.terminate()
  self.p.stdin.close()
  try:rc=self.p.wait(timeout=10)
  except subprocess.TimeoutExpired:self.p.kill();rc=self.p.wait()
  self.err.close();dump(self.dir/'session.json',{'exit_code':rc,'ecc':str(self.ecc),'ecc_sha256':sha(self.ecc),'hello':self.hello,'protocol_sha256':sha(self.dir/'protocol.json'),'stderr_sha256':sha(self.dir/'stderr.log')})
 def __enter__(self):return self
 def __exit__(self,*_):self.close()
def preflight():
 with Rpc('E8/rpc/preflight') as rpc:
  assert 'workspace.inspect_signoff' in rpc.hello['capabilities']
  opened=rpc.call('workspace.open',{'directory':str(WORK/'backend/light/runs/yosys_august')});print('OPEN',json.dumps(opened),flush=True)
  review=rpc.call('workspace.inspect_signoff',{'workspaceId':opened['workspaceId']});assert review['status']=='blocked'
  assert any(r['severity']=='blocked' for r in review['risks'])
  dump(ROOT/'reports/E8_signoff_negative.json',{'status':'PASS_EXPECTED_BLOCK','review':review,'policy':'Synthesis-only workspace correctly fails actualECOS/ECC signoff inspection. Noexportrequested whileblocked; noqualitygateoverrides.'})
 print('ACTUAL_ECC_SIGNOFF_NEGATIVE_CHECK_PASS',flush=True)
if __name__=='__main__':preflight()
