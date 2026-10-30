"""Install the exact course klib after materializing its make prerequisites.

On a new working copy, merely touching the archive is insufficient: missing .o
prerequisites cause make to compile TODO stubs and replace its members. Compile
those dependency objects first, then replace the entire archive with official
bytes. No TODO implementation is executed or accepted as a library solution.
"""
from common import *
import tarfile,argparse
def install(am,arch,tag):
 am=Path(am);source=ARCHIVE/'assets/offline/ysyx.oscc.cc/slides/resources/archive/klib-minirv-npc.tar.bz2'
 run(tag+'/bootstrap_dependencies',['make','-j1','ARCH='+arch,'archive'],cwd=am/'klib',env={'AM_HOME':str(am)},inputs=[am/'klib/Makefile'],timeout=180)
 with tarfile.open(source) as t:data=t.extractfile('klib-minirv-npc.a').read()
 output=am/'klib/build'/('klib-'+arch+'.a');before=sha(output) if output.exists() else None;output.write_bytes(data);output.touch()
 expected=hashlib.sha256(data).hexdigest();assert sha(output)==expected
 dump(ROOT/'artifacts'/tag/'installed.json',{'status':'PASS_BYTE_IDENTICAL','source':str(source),'source_sha256':sha(source),'archive':str(output),'archive_sha256':expected,'previous_sha256':before,'reason':'Missing object prerequisites must exist before touching/installing the supplied archive; no stubs are executed.'})
 return output
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--am',required=True);parser.add_argument('--arch',required=True);parser.add_argument('--tag',required=True);a=parser.parse_args();install(a.am,a.arch,a.tag)
