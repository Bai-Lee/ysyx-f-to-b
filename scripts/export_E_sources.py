from evidence import *
def main():
    arc=ROOT.parents[1]/'YSYX_F_B_Archive';dest=ROOT.parents[1]/'downloads/ysyx_e_stage/sources/canonical';dest.mkdir(parents=True,exist_ok=True)
    git='D:/Git/Git/cmd/git.exe';rows=[]
    names=['OSCPU__ysyx-workbench','NJU-ProjectN__abstract-machine__ics2026','NJU-ProjectN__am-kernels__ics2026','NJU-ProjectN__riscv-tests-am__master','NJU-ProjectN__fceux-am__ics2021','OSCPU__archbench__main','OSCPU__ysyxSoC__2607','openecos-projects__icsprout55-pdk__unconfirmed']
    for name in names:
        meta=json.loads((arc/'inventory/repo_metadata'/(name+'.json')).read_text('utf8'));repo=arc/'repos'/name
        head=subprocess.check_output([git,'-C',str(repo),'rev-parse','HEAD'],text=True).strip();assert head==meta['commit']
        archive=dest/(name+'.tar.gz')
        r=run('E/sources_canonical/'+name,[git,'-c','core.autocrlf=false','-C',repo,'archive','--format=tar.gz','-o',archive,'HEAD'],timeout=180);assert r['status']=='PASS'
        checked=[]
        for row in meta.get('submodules',[]):
            cols=row['line'].strip().split();want,path=cols[0],cols[1]
            got=subprocess.check_output([git,'-C',str(repo/path),'rev-parse','HEAD'],text=True).strip();assert want==got
            checked.append({'path':str(repo/path),'commit':got})
        rows.append({'name':name,'source':str(repo),'commit':head,'archive':str(archive),'sha256':sha(archive),'submodules_verified_in_original_archive':checked,'runtime_copy_scope':'Git top-level source snapshot; complete original source including listed submodules remains immutable in the archive. Supplied generated SoC RTL does not require regenerating Chisel.'})
    dump(ROOT/'reports/E_source_lock_canonical.json',{'status':'PASS','repositories':rows,'line_ending_policy':'Process-local core.autocrlf=false exports exact committed bytes. Initial CRLF archives and original E_source_lock.json remain unchanged for historical evidence.'});print('E_CANONICAL_SOURCES_EXPORTED',len(rows),flush=True)
if __name__=='__main__':main()
