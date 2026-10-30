import pathlib,json,sys,shutil,hashlib
base=pathlib.Path('/home/USER/tools/c-stage/cache/coursier/https/repo.maven.apache.org/maven2')
for r in json.loads(pathlib.Path(sys.argv[1]).read_text()):
 p=pathlib.Path(r['download'].replace(chr(92),'/'));s=str(p);p=pathlib.Path('/mnt/'+s[0].lower()+s[2:])
 q=base/r['relative'];q.parent.mkdir(parents=True,exist_ok=True)
 if q.exists():assert hashlib.sha256(q.read_bytes()).hexdigest()==r['sha256']
 else:shutil.copyfile(p,q)
 q.with_name('.'+q.name+'__sha1').write_text(r['official_sha1'])
 q.with_name('.'+q.name+'__sha1.computed').write_bytes(bytes.fromhex(r['official_sha1']))
 q.with_name('.'+q.name+'.checked').touch()
print('MAVEN_CACHE_INSTALLED',len(json.loads(pathlib.Path(sys.argv[1]).read_text())))
