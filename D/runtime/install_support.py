from common import *
import re

def main():
    downloads=Path('/workspace/downloads/ysyx_d_stage/spike-support');downloads.mkdir(parents=True,exist_ok=True)
    dest=Path('/home/USER/tools/d-stage/support');dest.mkdir(parents=True,exist_ok=True);rows=[]
    for name in ['device-tree-compiler','libfdt1']:
        o,_,_=run('D/dependencies/'+name+'/policy',['apt-cache','policy',name]);version=re.search(r'Candidate: (\S+)',o).group(1)
        meta,_,_=run('D/dependencies/'+name+'/metadata',['apt-cache','show',name+'='+version]);expected=re.search(r'^SHA256: (\w+)',meta,re.M).group(1)
        uri,_,_=run('D/dependencies/'+name+'/uri',['apt-get','--print-uris','download',name+'='+version]);assert 'ubuntu.com/ubuntu/' in uri
        run('D/dependencies/'+name+'/download',['apt-get','download',name+'='+version],cwd=downloads,timeout=180)
        deb=next(downloads.glob(name+'_*.deb'));assert sha(deb)==expected
        run('D/dependencies/'+name+'/extract',['dpkg-deb','-x',deb,dest],inputs=[deb])
        rows.append({'package':name,'version':version,'sha256':expected,'archive':str(deb),'official_digest_match':True})
    env={'PATH':str(dest/'usr/bin')+':'+os.environ['PATH'],'LD_LIBRARY_PATH':str(dest/'usr/lib/x86_64-linux-gnu')}
    good=WORK/'device.dts';good.write_text('/dts-v1/; / { compatible="d-stage-control"; };\n')
    run('D/dependencies/dtc_positive',[dest/'usr/bin/dtc','-I','dts','-O','dtb','-o',WORK/'device.dtb',good],inputs=[good],outputs=[WORK/'device.dtb'],env=env)
    bad=WORK/'device_bad.dts';bad.write_text('/dts-v1/; / { syntax deliberately broken }\n')
    run('D/dependencies/dtc_negative',[dest/'usr/bin/dtc','-I','dts','-O','dtb','-o',WORK/'bad.dtb',bad],inputs=[bad],env=env,expected=(1,))
    dump(ROOT/'reports/D_spike_support.json',{'status':'PASS','packages':rows,'env':env,'system_installation':False})

if __name__=='__main__':main()
