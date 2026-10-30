"""Keep byte-preservation evidence and both object sets available offline."""
from common7 import *
from software_soc import SOFT
import tarfile
def main():
 manifest=json.loads((ROOT/'reports/E7_batch_integrity.json').read_text());files=[]
 for row in manifest['tests']:
  name=row['id'].replace(':','_')+'.o'
  for key,prefix in [('original_object','original'),('namespaced_object','namespaced')]:
   path=Path(row[key]);expected=row['original_sha256' if prefix=='original' else 'namespaced_sha256'];assert sha(path)==expected;files.append((path,prefix+'/'+name))
 for name in ['all','wrong']:
  for f in sorted((SOFT/'batch'/name).glob('*')):
   if f.is_file():files.append((f,'dispatch/'+name+'/'+f.name))
 files += [(ROOT/'reports/E7_batch_integrity.json','integrity.json'),(ROOT/'E/E7/batch_bridge.S','batch_bridge.S')]
 target=ROOT/'E/E7/batch/objects-and-dispatch.tar.gz'
 assert len({n for _,n in files})==len(files)
 with tarfile.open(target,'w:gz',compresslevel=6) as archive:
  for path,name in files:archive.add(path,arcname=name,recursive=False)
 with tarfile.open(target) as archive:
  for path,name in files:
   stream=archive.extractfile(name);assert stream is not None;h=hashlib.sha256()
   for chunk in iter(lambda:stream.read(1024*1024),b''):h.update(chunk)
   assert h.hexdigest()==sha(path),name
 dump(ROOT/'reports/E7_batch_export.json',{'status':'PASS','archive':str(target.relative_to(ROOT)),'sha256':sha(target),'members':[{'path':n,'source':str(p),'sha256':sha(p)} for p,n in files],'scope':'BothunchangedoriginalandnamespacedELFobjects, exactsymbolmappings/sectiondigests, anddispatchsource. Archiveverifiedmember-by-memberwithoutoverwritinglivefiles.'})
 print('BATCH_OBJECTS_OFFLINE_ARCHIVE_PASS',len(files),flush=True)
if __name__=='__main__':main()
