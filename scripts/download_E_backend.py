"""Download exact official release assets; bounded streaming, retries and digests."""
from evidence import *
import requests,time
DEST=ROOT.parents[1]/'downloads/ysyx_e_stage'
def main():
    selections=[('0_v0.1.0-alpha.10.json',lambda n:n=='ecc-cli-linux-x86_64.tar.gz'),('4_v1.10.100.json',lambda n:n.endswith('.tar.bz2')),('3_2026-10-22.json',lambda n:n=='oss-cad-suite-linux-x64-20261022.tgz'),('1_v0.1.0-alpha.9.json',lambda n:n.endswith('x86_64.AppImage'))]
    rows=[]
    for meta,choose in selections:
        release=json.loads((DEST/'releases'/meta).read_text('utf8'))
        for a in release['assets']:
            if not choose(a['name']):continue
            folder=DEST/release['tag_name'];folder.mkdir(exist_ok=True);p=folder/a['name'];want=a['digest'].split(':',1)[1]
            if not (p.exists() and p.stat().st_size==a['size'] and sha(p)==want):
                assert not p.exists(),'Preserve mismatched existing asset: '+str(p)
                part=p.with_name(p.name+'.part');attempts=[]
                for attempt in range(1,5):
                    try:
                        offset=part.stat().st_size if part.exists() else 0
                        headers={'User-Agent':'YSYX-offline-engineering/1','Range':f'bytes={offset}-'} if offset else {'User-Agent':'YSYX-offline-engineering/1'}
                        with requests.get(a['browser_download_url'],headers=headers,stream=True,timeout=(30,90)) as response:
                            response.raise_for_status();append=response.status_code==206 and offset>0
                            if append:assert response.headers.get('Content-Range','').startswith(f'bytes {offset}-')
                            done=offset if append else 0;last=time.monotonic()
                            with part.open('ab' if append else 'wb') as output:
                                for chunk in response.iter_content(1024*1024):
                                    if chunk:output.write(chunk);done+=len(chunk)
                                    if time.monotonic()-last>20:print(a['name'],done,'/',a['size'],flush=True);last=time.monotonic()
                        assert part.stat().st_size==a['size'] and sha(part)==want
                        part.replace(p);break
                    except Exception as e:
                        attempts.append({'attempt':attempt,'error':str(e),'time':datetime.now(timezone.utc).isoformat()});print('DOWNLOAD_RETRY',a['name'],str(e)[:200],flush=True)
                        dump(ROOT/'reports/E_backend_download_attempts.json',{'current':a['name'],'attempts':attempts})
                        if attempt==4:raise
                        time.sleep(2*attempt)
            rows.append({'file':str(p),'url':a['browser_download_url'],'release':release['tag_name'],'bytes':a['size'],'sha256':sha(p),'published_digest_match':True})
            dump(ROOT/'reports/E_backend_assets.json',{'status':'IN_PROGRESS','assets':rows});print('ASSET_VERIFIED',a['name'],flush=True)
    dump(ROOT/'reports/E_backend_assets.json',{'status':'PASS','assets':rows});print('BACKEND_ASSETS_READY',flush=True)
if __name__=='__main__':main()
