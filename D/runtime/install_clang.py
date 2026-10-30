"""Fetch official Ubuntu packages and unpack a task-local compiler, without apt install."""
from common import *
import re

def main():
    downloads=Path('/workspace/downloads/ysyx_d_stage/clang');downloads.mkdir(parents=True,exist_ok=True)
    dest=Path('/home/USER/tools/d-stage/clang15');dest.mkdir(parents=True,exist_ok=True)
    rows=[]
    for name in ['clang-15','libclang-cpp15','libclang-common-15-dev']:
        o,_,_=run('D/dependencies/'+name+'/policy',['apt-cache','policy',name]);version=re.search(r'Candidate: (\S+)',o).group(1)
        meta,_,_=run('D/dependencies/'+name+'/metadata',['apt-cache','show',name+'='+version]);expected=re.search(r'^SHA256: (\w+)',meta,re.M).group(1)
        uri,_,_=run('D/dependencies/'+name+'/uri',['apt-get','--print-uris','download',name+'='+version]);assert 'ubuntu.com/ubuntu/' in uri
        run('D/dependencies/'+name+'/download',['apt-get','download',name+'='+version],cwd=downloads,timeout=300)
        files=list(downloads.glob(name+'_*.deb'));assert len(files)==1;deb=files[0];assert sha(deb)==expected
        run('D/dependencies/'+name+'/extract',['dpkg-deb','-x',deb,dest],inputs=[deb],timeout=90)
        rows.append({'package':name,'version':version,'file':str(deb),'sha256':expected,'official_apt_digest_match':True,'uri_record':'artifacts/D/dependencies/'+name+'/uri/stdout.log'})
    exe=dest/'usr/bin/clang-15';env={'LD_LIBRARY_PATH':str(dest/'usr/lib/x86_64-linux-gnu')}
    run('D/dependencies/clang_version',[exe,'--version'],env=env,inputs=[exe])
    c=WORK/'clang_check.c';c.write_text('int f(int x){return x+1;}\n')
    ll=WORK/'clang_check.ll';run('D/dependencies/clang_compile',[exe,'-S','-emit-llvm',c,'-o',ll],env=env,inputs=[c],outputs=[ll]);assert 'define' in ll.read_text()
    bad=WORK/'clang_bad.c';bad.write_text('int f(void){return missing_identifier;}\n')
    run('D/dependencies/clang_negative',[exe,'-fsyntax-only',bad],env=env,inputs=[bad],expected=(1,))
    dump(ROOT/'reports/D_clang.json',{'status':'PASS','packages':rows,'compiler':str(exe),'env':env,'system_installation':False,'evidence':'artifacts/D/dependencies','existing_libLLVM15_sha256':sha('/usr/lib/x86_64-linux-gnu/libLLVM-15.so.1')})

if __name__=='__main__':main()
