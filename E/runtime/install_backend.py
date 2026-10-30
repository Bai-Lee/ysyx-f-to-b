from common import *
import tarfile
def native(s):return Path(s.replace('D:\\','/mnt/d/').replace('D:/','/mnt/d/').replace('\\','/'))
def extract(a,d):
    d.mkdir(parents=True,exist_ok=True)
    with tarfile.open(a) as t:
        for m in t.getmembers():
            assert (d/m.name).resolve().is_relative_to(d.resolve()),m.name
            if m.issym():assert (d/m.name).parent.joinpath(m.linkname).resolve().is_relative_to(d.resolve()),m.linkname
        t.extractall(d)
def main():
    info=json.loads((ROOT/'reports/E_backend_assets.json').read_text());assert info['status']=='PASS'
    base=Path('/home/USER/tools/e-stage');base.mkdir(exist_ok=True);rows=[]
    pdk=Path('/home/USER/tools/icsprout55-e-stage')
    for a in info['assets']:
        path=native(a['file']);assert sha(path)==a['sha256'];name=path.name
        if name.startswith('ecc-cli'):dest=base/'ecc-alpha10'
        elif name.startswith('oss-cad-suite'):dest=base/'oss-20261022'
        elif name.endswith('.AppImage'):
            dest=base/'ecos-alpha9';dest.mkdir(exist_ok=True);binary=dest/name
            if not binary.exists():shutil.copyfile(path,binary);binary.chmod(0o755)
            if not (dest/'squashfs-root').exists():run('E/backend/extract_ecos',[binary,'--appimage-extract'],cwd=dest,timeout=600,inputs=[binary])
            rows.append({'tool':'ecos','root':str(dest/'squashfs-root'),'archive_sha256':a['sha256']});continue
        elif '_liberty' in name or '_gds' in name:
            if name.startswith('ICsprout_55'):dest=pdk/'IP/IO'/name.split('_gds')[0]
            else:dest=pdk/'IP/STD_cell/ics55_LLSC_H7C_V1p10C100'/name.split('_liberty')[0].split('_gds')[0]
        else:raise ValueError(name)
        marker=dest/('.'+name+'.extracted.json')
        if marker.exists():assert json.loads(marker.read_text())['sha256']==a['sha256']
        else:
            extract(path,dest);dump(marker,{'sha256':a['sha256'],'source':str(path)})
        print('EXTRACTED',name,flush=True);rows.append({'asset':name,'root':str(dest),'archive_sha256':a['sha256']})
    dump(ROOT/'reports/E_backend_install.json',{'status':'EXTRACTED_REQUIRES_CAPABILITY_TEST','items':rows,'pdk_root':str(pdk),'scope':'Official course-pinned ECC/ECOS andPDK release1.10.100; no global PATH modification; no CUDA installation.'})
    print('BACKEND_EXTRACTED',flush=True)
if __name__=='__main__':main()
