"""Download explicit official C-stage source/specification supplements."""
from evidence import *
import urllib.request,urllib.error,traceback

def main():
    dest=ROOT.parents[1]/'downloads/ysyx_c_stage';dest.mkdir(parents=True,exist_ok=True)
    items=[
      {'name':'ysyxSoC-compatible-full','url':'https://codeload.github.com/OSCPU/ysyxSoC/tar.gz/bcdcbc3e8d97a11c07d3007e14f33c6147c02a8e','file':'sources/ysyxSoC-bcdcbc3e8d97a11c07d3007e14f33c6147c02a8e.tar.gz','commit':'bcdcbc3e8d97a11c07d3007e14f33c6147c02a8e','repository':'https://github.com/OSCPU/ysyxSoC','reason':'Official ysyx6 full-SoC source matches C5 topology; original archived 2607 snapshot is preserved separately.'},
      {'name':'AXI-IHI0022H','url':'https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/IHI0022H_amba_axi_protocol_spec.pdf','file':'specifications/IHI0022H_amba_axi_protocol_spec.pdf','revision':'Issue H, ID040120, 2020-03-31','reason':'Course-linked Issue K removed AXI4/AXI4-Lite; Issue H contains the required protocol.'}
    ]
    rows=[];attempts=[]
    for item in items:
        path=dest/item['file'];path.parent.mkdir(parents=True,exist_ok=True);start=time.monotonic()
        request=urllib.request.Request(item['url'],headers={'User-Agent':'A-Circuit-local-source-acquisition/1.0'})
        if not path.exists():
            part=path.with_name(path.name+'.partial')
            for retry in range(1,4):
                ad=ROOT/'artifacts/C/sources'/item['name']/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f');ad.mkdir(parents=True,exist_ok=True)
                begun=time.monotonic()
                try:
                    with urllib.request.urlopen(request,timeout=60) as response,part.open('wb') as output:
                        headers={k:response.headers.get(k) for k in ('Content-Type','Content-Length','Last-Modified','ETag')}
                        for block in iter(lambda:response.read(1048576),b''):output.write(block)
                    attempt={'status':'PASS','url':item['url'],'retry':retry,'elapsed_seconds':round(time.monotonic()-begun,3),'bytes':part.stat().st_size,'sha256':sha(part),'tls_verification':'Python default trust and hostname verification'}
                    dump(ad/'result.json',attempt);attempts.append(attempt);break
                except Exception as error:
                    (ad/'stderr.log').write_text(traceback.format_exc(),encoding='utf8')
                    attempt={'status':'FAIL','url':item['url'],'retry':retry,'elapsed_seconds':round(time.monotonic()-begun,3),'error':repr(error)}
                    dump(ad/'result.json',attempt);attempts.append(attempt)
                    if retry==3:
                        if path.suffix=='.pdf' and os.name=='nt':
                            args=['curl.exe','--fail','--location','--max-time','60','--output',str(part),item['url']]
                            q=subprocess.run(args,capture_output=True,timeout=70)
                            (ad/'curl.stdout.log').write_bytes(q.stdout);(ad/'curl.stderr.log').write_bytes(q.stderr)
                            fallback={'status':'PASS' if q.returncode==0 else 'FAIL','command':args,'exit_code':q.returncode,'tls_verification':'curl default Windows trust/hostname verification; no insecure flags'}
                            dump(ad/'curl.json',fallback);attempts.append(fallback)
                            if q.returncode==0:headers={'download_method':'Windows curl with default certificate verification'};break
                        raise
                    time.sleep(retry)
            first=part.open('rb').read(8)
            assert first.startswith(b'%PDF') if path.suffix=='.pdf' else first.startswith(b'\x1f\x8b'),(item['name'],first)
            part.replace(path)
        else:headers={'note':'Existing complete local download reused; final hash is recorded below.'}
        row={**item,'archive':str(path),'bytes':path.stat().st_size,'sha256':sha(path),'headers':headers,'elapsed_seconds':round(time.monotonic()-start,3),'provenance':'Official HTTPS source, fixed commit or document revision. Local SHA-256 recorded; no separate published digest claim.'};rows.append(row)
        evidence=ROOT/'artifacts/C/sources'/item['name']
        row['download_evidence']=[p.relative_to(ROOT).as_posix() for p in sorted(evidence.rglob('*.json'))] if evidence.exists() else []
        dump(ROOT/'reports/C_additional_sources.json',{'status':'IN_PROGRESS','items':rows})
        print('C_OFFICIAL_SOURCE_READY',item['name'],path.stat().st_size,flush=True)
    dump(ROOT/'reports/C_additional_sources.json',{'status':'PASS','items':rows,'download_attempts':attempts})

if __name__=='__main__':main()
