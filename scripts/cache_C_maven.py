"""Populate only failed fixed Maven artifacts through verified Windows TLS."""
from evidence import *
import re
from urllib.parse import urlparse

def main():
    log=(ROOT/'artifacts/C5/bootstrap/generate/stderr.log').read_text('utf8')
    urls=sorted(set(re.findall(r'https://repo\.maven\.apache\.org/maven2/[A-Za-z0-9_./-]+\.(?:jar|pom)',log)))
    assert urls,'No specific Maven artifact failures in the saved generation log'
    rows=[];base=ROOT.parents[1]/'downloads/ysyx_c_stage/maven'
    for url in urls:
        rel=urlparse(url).path.removeprefix('/maven2/');assert '..' not in Path(rel).parts
        target=base/rel;target.parent.mkdir(parents=True,exist_ok=True);checksum=target.with_name(target.name+'.sha1')
        tag='C5/bootstrap/maven-cache/'+rel.replace('/','__')
        fetch_url=url.replace('repo.maven.apache.org','repo1.maven.org')
        cached=False
        if target.exists() and checksum.exists():
            value=checksum.read_text().strip().split()[0]
            cached=bool(re.fullmatch('[0-9a-fA-F]{40}',value)) and hashlib.sha1(target.read_bytes()).hexdigest()==value.lower()
        if not cached:
            for endpoint,path in [(fetch_url,target),(fetch_url+'.sha1',checksum)]:
                record=run(tag+('/checksum' if path==checksum else '/artifact'),['curl.exe','--fail','--location','--retry','3','--retry-all-errors','--retry-delay','1','--connect-timeout','15','--max-time','30','--output',path,endpoint],timeout=135)
                assert record['status']=='PASS'
        expected=checksum.read_text().strip().split()[0];assert re.fullmatch('[0-9a-fA-F]{40}',expected)
        actual=hashlib.sha1(target.read_bytes()).hexdigest();assert actual==expected.lower(),url
        rows.append({'url':url,'fetched_from':fetch_url,'download':str(target),'sha256':sha(target),'official_sha1':expected.lower(),'official_digest_match':True,'relative':rel})
    # This only creates immutable-version cache files; no JVM/network settings.
    code='''import pathlib,json,sys,shutil,hashlib
base=pathlib.Path('/home/USER/tools/c-stage/cache/coursier/https/repo.maven.apache.org/maven2')
for r in json.loads(sys.argv[1]):
 p=pathlib.Path(r['download'].replace('\\\\','/'));s=str(p);p=pathlib.Path('/mnt/'+s[0].lower()+s[2:])
 q=base/r['relative'];q.parent.mkdir(parents=True,exist_ok=True)
 if q.exists():assert hashlib.sha256(q.read_bytes()).hexdigest()==r['sha256']
 else:shutil.copyfile(p,q)
 q.with_name('.'+q.name+'__sha1').write_text(r['official_sha1'])
 q.with_name('.'+q.name+'__sha1.computed').write_bytes(bytes.fromhex(r['official_sha1']))
 q.with_name('.'+q.name+'.checked').touch()
print('MAVEN_CACHE_INSTALLED',len(json.loads(sys.argv[1])))
'''
    staging=ROOT/'artifacts/C5/bootstrap/maven-cache/staging.json';dump(staging,rows)
    helper=ROOT/'C/C5/generation/install_maven_cache.py';helper.write_text(code.replace("json.loads(sys.argv[1])","json.loads(pathlib.Path(sys.argv[1]).read_text())").replace("r['download'].replace('\\\\','/')","r['download'].replace(chr(92),'/')"),encoding='utf8')
    def linux(path):s=str(path).replace(chr(92),'/');return '/mnt/'+s[0].lower()+s[2:]
    q=subprocess.run(['wsl.exe','-d','YSYX-Linux','-u','ysyx','--','python3',linux(helper),linux(staging)],capture_output=True,text=True,timeout=60);assert q.returncode==0,q.stderr
    dest=ROOT/'reports/C5_maven_cache.json';prior=json.loads(dest.read_text('utf8')).get('artifacts',[]) if dest.exists() else []
    merged={r['url']:r for r in prior+rows};dump(dest,{'status':'PASS_VERIFIED_CACHE','artifacts':list(merged.values()),'scope':'Only failed immutable Maven Central artifacts fetched through Windows curl with ordinary certificate/hostname verification, SHA-1 checked against the same official origin, local SHA-256 also recorded. No untrusted mirrors or disabled TLS verification.'})
    print(q.stdout.strip(),flush=True)

if __name__=='__main__':main()
