from evidence import *
import urllib.request, re

def main():
    dest=ROOT.parents[1]/'downloads/ysyx_d_stage/sources';dest.mkdir(parents=True,exist_ok=True)
    previous=ROOT/'reports/D_additional_sources.json'
    rows=json.loads(previous.read_text('utf8'))['repositories'] if previous.exists() else []
    for name,repo,ref in [('capstone','capstone-engine/capstone','refs/tags/5.0.6'),('spike','NJU-ProjectN/riscv-isa-sim','HEAD')]:
        found=next((x for x in rows if x['name']==name),None)
        if found and Path(found['archive']).is_file() and sha(found['archive'])==found['sha256']:
            print(name,'verified existing locked archive',flush=True);continue
        url=f'https://github.com/{repo}.git'
        api=f'https://api.github.com/repos/{repo}/commits/'+('5.0.6' if name=='capstone' else 'HEAD')
        req=urllib.request.Request(api,headers={'User-Agent':'A-Circuit-local-course-toolchain','Accept':'application/vnd.github+json'})
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req,timeout=90) as response:meta=json.load(response)
                break
            except Exception as err:
                dump(dest/f'{name}-metadata-attempt-{attempt}.json',{'url':api,'error':str(err),'timestamp':datetime.now(timezone.utc).isoformat()})
                if attempt==2:raise
                time.sleep(1+attempt)
        dump(dest/(name+'-commit.json'),meta)
        commit=meta['sha'];assert re.fullmatch('[0-9a-f]{40}',commit)
        source=f'https://codeload.github.com/{repo}/tar.gz/{commit}';archive=dest/f'{name}-{commit}.tar.gz'
        request=urllib.request.Request(source,headers={'User-Agent':'A-Circuit-local-course-toolchain'})
        start=time.monotonic()
        with urllib.request.urlopen(request,timeout=120) as response,archive.open('wb') as out:
            import shutil;shutil.copyfileobj(response,out)
        row={'name':name,'repository':url,'ref':ref,'commit':commit,'download_url':source,'archive':str(archive),'bytes':archive.stat().st_size,'sha256':sha(archive),'elapsed_seconds':time.monotonic()-start,'provenance':'Official project HTTPS source archive at resolved commit; local SHA-256 is recorded. No separate published upstream digest was available.'};rows.append(row);print(name,commit,archive.stat().st_size,flush=True)
        dump(ROOT/'reports/D_additional_sources.json',{'status':'IN_PROGRESS','repositories':rows})
    dump(ROOT/'reports/D_additional_sources.json',{'status':'PASS','repositories':rows})

if __name__=='__main__':main()
