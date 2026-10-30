from pathlib import Path
import sys,tarfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
 src=Path('/workspace/downloads/ysyx_e_stage/sources');old=src/'OSCPU__archbench__main.tar.gz';new=src/'OSCPU__archbench__main.canonical.tar.gz';root=BENCH/'archbench';rows=[]
 with tarfile.open(old) as a,tarfile.open(new) as b:
  for m in b.getmembers():
   if not m.isfile():continue
   original=a.extractfile(m.name).read();canonical=b.extractfile(m).read()
   if original==canonical:continue
   target=root/m.name
   assert original.replace(b'\r\n',b'\n')==canonical,('unexpected source drift',m.name)
   current=target.read_bytes()
   if current==original:
    target.write_bytes(canonical);action='restored_canonical_git_bytes'
   elif current==canonical:action='already_canonical'
   else:
    # Keep the documented am.filelist selection and other intentional working edits; do not overwrite user/work changes.
    action='preserved_working_edit';assert m.name.endswith('am.filelist') or m.name.endswith('.sh'),m.name
   rows.append({'file':m.name,'export_sha256':hashlib.sha256(original).hexdigest(),'canonical_sha256':hashlib.sha256(canonical).hexdigest(),'action':action})
 dump(ROOT/'reports/E6_source_line_endings.json',{'status':'REPAIRED_RETEST_REQUIRED','cause':'Windows Git archive inherited core.autocrlf=true and exported CRLF, including benchmark input/test-hello.txt. Re-export with process-local -c core.autocrlf=false restores exact committed bytes. Original immutable archives retained; no checksum expectations changed.','original_archive_sha256':sha(old),'canonical_archive_sha256':sha(new),'files':rows})
 print('CANONICAL_SOURCE_RESTORED',len(rows),flush=True)
if __name__=='__main__':main()
