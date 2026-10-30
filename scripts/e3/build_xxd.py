"""LCT-04-X03: manually build a small official C tool with locked source blobs."""
from pathlib import Path
import sys,json,hashlib,shutil
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from evidence import *
from lct_early import lp

def main():
    source=ROOT.parents[1]/'downloads/ysyx_e3/xxd-source'
    meta_path=source/'provenance.json';meta=json.loads(meta_path.read_text('utf8'))
    build=ROOT/'artifacts/E3/xxd/build';build.mkdir(parents=True,exist_ok=True)
    for item in meta['files']:
        file=source/item['file'];data=file.read_bytes()
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==item['git_blob_sha']
        assert sha(file)==item['sha256'];shutil.copyfile(file,build/file.name)
    inputs=[build/'xxd.c',build/'Makefile',meta_path];runs=[]
    def linux(name,args,extra=()):
        q=run('E3/xxd/'+name,['wsl.exe','-d','YSYX-Linux','-u','ysyx','--exec',*map(str,args)],inputs+list(extra),timeout=45)
        assert q['status']=='PASS';runs.append(q)
        return (ROOT/'artifacts/E3/xxd'/name/'stdout.log').read_bytes(),(ROOT/'artifacts/E3/xxd'/name/'stderr.log').read_bytes()
    payload=ROOT/'artifacts/E3/xxd/payload.bin';payload.write_bytes(bytes(range(256))+b'YSYX\x00\xff')
    out,err=linux('existing_tool',['xxd','-p',lp(payload)],[payload]);assert b''.join(out.split()).decode()==payload.read_bytes().hex()
    linux('build',['make','-C',lp(build),'-j1','CC=gcc','CFLAGS=-O0 -g -Wall','xxd'])
    exe=build/'xxd'
    version,err=linux('version',[lp(exe),'-v'],[exe]);assert b'xxd' in version+err
    version_text=(version+err).decode('utf8',errors='replace').strip()
    dump_hex,err=linux('dump',[lp(exe),'-p',lp(payload)],[exe,payload]);assert b''.join(dump_hex.split()).decode()==payload.read_bytes().hex()
    hexfile=ROOT/'artifacts/E3/xxd/dump/stdout.log';restored=ROOT/'artifacts/E3/xxd/roundtrip.bin'
    linux('reverse',[lp(exe),'-r','-p',lp(hexfile),lp(restored)],[exe,hexfile])
    assert restored.read_bytes()==payload.read_bytes()
    result={'status':'PASS','task':'LCT-04-X03','source_provenance':meta,'version':version_text,'binary_sha256':sha(exe),'roundtrip_bytes':len(payload.read_bytes()),'roundtrip_sha256':sha(restored),'runs':runs,'scope':'Small single-source official xxd utility; compiled manually with native Linux make/gcc -j1. Does not substitute for the deferred full Valgrind source build.'}
    dump(ROOT/'reports/E3_xxd_build.json',result);print('E3_XXD_MANUAL_BUILD PASS',len(payload.read_bytes()),'byte roundtrip',flush=True)

if __name__=='__main__':main()
