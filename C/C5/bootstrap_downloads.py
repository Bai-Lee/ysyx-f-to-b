"""Official portable JDK/Mill/firtool inputs, with upstream digests when supplied."""
from pathlib import Path
import sys,urllib.request,hashlib,json,time,subprocess,traceback,re
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from evidence import ROOT,sha,dump,run
BASE=ROOT.parents[1]/'downloads/ysyx_c_stage/tooling'

def fetch(url,path):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():return path
    for i in range(3):
        folder=ROOT/'artifacts/C5/bootstrap/downloads'/path.name/str(time.time_ns());folder.mkdir(parents=True)
        start=time.monotonic();part=path.with_name(path.name+'.partial')
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'A-Circuit-local-source/1.0'}),timeout=60) as response,part.open('wb') as output:
                for b in iter(lambda:response.read(1048576),b''):output.write(b)
            part.replace(path);dump(folder/'result.json',{'status':'PASS','url':url,'bytes':path.stat().st_size,'sha256':sha(path),'elapsed_seconds':time.monotonic()-start});return path
        except Exception as error:
            (folder/'stderr.log').write_text(traceback.format_exc(),encoding='utf8');dump(folder/'result.json',{'status':'FAIL','url':url,'error':repr(error),'elapsed_seconds':time.monotonic()-start})
            if i==2:raise
            time.sleep(i+1)

def main():
    BASE.mkdir(parents=True,exist_ok=True);rows=[]
    for package in ['openjdk-17-jdk-headless','openjdk-17-jre-headless']:
        r=run('C5/bootstrap/apt/'+package,['wsl.exe','-d','YSYX-Linux','-u','ysyx','--','apt-cache','show',package]);assert r['status']=='PASS'
        text=(ROOT/'artifacts/C5/bootstrap/apt'/package/'stdout.log').read_text('utf8');block=text.split('\n\n')[0];fields=dict(line.split(': ',1) for line in block.splitlines() if ': ' in line)
        url='https://archive.ubuntu.com/ubuntu/'+fields['Filename'];path=fetch(url,BASE/Path(fields['Filename']).name)
        assert sha(path)==fields['SHA256']
        rows.append({'name':package,'version':fields['Version'],'url':url,'file':str(path),'sha256':sha(path),'official_digest_match':True,'digest_source':'existing official Ubuntu apt metadata retained in artifacts/C5/bootstrap/apt/'+package})
        print('PORTABLE_PACKAGE_DOWNLOADED',package,flush=True)
    release=fetch('https://api.github.com/repos/com-lihaoyi/mill/releases/tags/0.12.4',BASE/'mill-0.12.4-release.json');data=json.loads(release.read_text('utf8'))
    names=['0.12.4','0.12.4-assembly'];assets={x['name']:x for x in data['assets']}
    for name in names:
        asset=assets[name];path=fetch(asset['browser_download_url'],BASE/name);assert path.stat().st_size==asset['size']
        checksums=[x for x in data['assets'] if x['name'] in [name+'.sha256',name+'.sha256sum',name+'.sha512']]
        row={'name':'mill-'+name,'url':asset['browser_download_url'],'file':str(path),'sha256':sha(path),'official_digest_match':False,'provenance':'Official release asset; API size matched. No separately published checksum asset/API digest was supplied.'}
        if asset.get('digest'):
            algo,digest=asset['digest'].split(':',1);assert hashlib.new(algo,path.read_bytes()).hexdigest()==digest;row.update(official_digest_match=True,upstream_digest=asset['digest'])
        assert not checksums,'Unexpected checksum asset: implement verification rather than ignore'
        rows.append(row);print('MILL_ASSET_DOWNLOADED',name,flush=True)
    prefix='https://github.com/llvm/circt/releases/download/firtool-1.105.0/';name='firrtl-bin-linux-x64.tar.gz'
    checksum=fetch(prefix+name+'.sha256',BASE/(name+'.sha256'));path=fetch(prefix+name,BASE/name)
    expected=checksum.read_text().split()[0];assert re.fullmatch('[0-9a-fA-F]{64}',expected) and sha(path)==expected.lower()
    rows.append({'name':'firtool','version':'1.105.0','url':prefix+name,'file':str(path),'sha256':sha(path),'official_digest_match':True,'checksum_file':str(checksum),'checksum_sha256':sha(checksum)})
    dump(ROOT/'reports/C5_toolchain_downloads.json',{'status':'PASS_DOWNLOADS_ONLY','files':rows,'scope':'Portable task-local tools; no system/global install. Downloads alone do not qualify generation.'})
    print('C5_TOOL_DOWNLOADS_READY',flush=True)

if __name__=='__main__':main()
