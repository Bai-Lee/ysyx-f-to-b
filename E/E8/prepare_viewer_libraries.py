from pathlib import Path
import sys,re,ctypes
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
 downloads=WORK/'viewer_downloads';downloads.mkdir(exist_ok=True);install=Path('/home/USER/tools/e-stage/gui-libs');install.mkdir(exist_ok=True)
 packages=['libxkbcommon-x11-0','libxcb-xkb1'];o,e,r=run('E8/viewer_dependencies/metadata',['apt-get','--print-uris','download',*packages],cwd=downloads)
 rows=[]
 for line in o.splitlines():
  match=re.fullmatch(r"'([^']+)' (\S+) (\d+) SHA512:([0-9a-f]+)",line)
  if match:
   url,name,size,digest=match.groups();assert url.startswith('http://archive.ubuntu.com/ubuntu/');rows.append({'url':url,'filename':name,'bytes':int(size),'official_sha512':digest})
 assert len(rows)==2
 run('E8/viewer_dependencies/download',['apt-get','download',*packages],cwd=downloads,timeout=180)
 final_download=Path('/workspace/downloads/ysyx_e_stage/gui');final_download.mkdir(exist_ok=True)
 for row in rows:
  file=downloads/row['filename'];assert file.stat().st_size==row['bytes'] and hashlib.sha512(file.read_bytes()).hexdigest()==row['official_sha512'];shutil.copyfile(file,final_download/file.name)
  run('E8/viewer_dependencies/extract_'+file.name,['dpkg-deb','--extract',file,install],inputs=[file]);row['local_sha256']=sha(file)
 run('E8/viewer_dependencies/link_check',['ldd',install/'usr/lib/x86_64-linux-gnu/libxkbcommon-x11.so.0'],env={'LD_LIBRARY_PATH':str(install/'usr/lib/x86_64-linux-gnu')},inputs=[install/'usr/lib/x86_64-linux-gnu/libxkbcommon-x11.so.0'])
 dump(ROOT/'reports/E8_viewer_dependencies.json',{'status':'PASS_PORTABLE_EXTRACTION','packages':rows,'root':str(install),'scope':'OfficialUbuntupackagebytesverifiedagainstAPTindexSHA512; unpackedunderprojecttools, notinstalledintothesystem. LD_LIBRARY_PATHappliestothisGUIprocessonly.'})
 print('VIEWER_XKB_DEPENDENCIES_VERIFIED_AND_UNPACKED',flush=True)
if __name__=='__main__':main()
