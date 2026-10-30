"""Independent source reconstruction and portable tools; original trees untouched."""
from pathlib import Path
import sys,tarfile,os,shutil,json,subprocess,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import ROOT,WORK,sha,dump,run
from resource_policy import load_policy
TOOLS=Path('/home/USER/tools/c-stage');SOC=WORK/'soc-generation/ysyxSoC'

def local(s):
    s=str(s).replace('\\','/')
    return Path('/mnt/'+s[0].lower()+s[2:]) if len(s)>2 and s[1]==':' else Path(s)

def extract(path,dest,strip=False):
    dest=Path(dest);dest.mkdir(parents=True,exist_ok=True)
    with tarfile.open(path) as tar:
        for m in tar:
            name=Path(m.name)
            if strip:
                if len(name.parts)==1:continue
                name=Path(*name.parts[1:])
            assert not name.is_absolute() and '..' not in name.parts
            m.name=str(name);p=dest/name;assert p.resolve().is_relative_to(dest.resolve())
            if m.issym() or m.islnk():
                assert not Path(m.linkname).is_absolute()
                assert ((p.parent if m.issym() else dest)/m.linkname).resolve().is_relative_to(dest.resolve())
            tar.extract(m,dest)

def sources():
    lock=json.loads((ROOT/'reports/C5_source_lock.json').read_text());assert sha(local(lock['archive']))==lock['sha256']
    assert not (SOC/'.git').exists(),'Source bootstrap already exists; do not overwrite'
    extract(local(lock['archive']),SOC,True)
    run('C5/bootstrap/source/root-init',['git','init'],cwd=SOC)
    for key,value in [('user.name','Local C-stage source bootstrap'),('user.email','local-c-stage@invalid.example'),('core.autocrlf','false')]:run('C5/bootstrap/source/root-config-'+key,['git','config',key,value],cwd=SOC)
    run('C5/bootstrap/source/root-add',['git','add','--all'],cwd=SOC)
    rc=lock['submodules'][0];assert rc['path']=='rocket-chip'
    run('C5/bootstrap/source/root-gitlink',['git','update-index','--add','--cacheinfo','160000,'+rc['commit']+',rocket-chip'],cwd=SOC)
    tree=subprocess.check_output(['git','write-tree'],cwd=SOC,text=True).strip();assert tree==lock['tree'],(tree,lock['tree'])
    run('C5/bootstrap/source/root-commit',['git','-c','gc.auto=0','commit','-m','Local bootstrap of exact official tree '+lock['commit']],cwd=SOC)
    clones=[]
    for row in lock['submodules']:
        gd=local(row['gitdir']);assert not (gd/'objects/info/alternates').exists(),'Do not inherit external object alternates'
        cache=WORK/'soc-generation/git-cache'/(row['path'].replace('/','__')+'.git');cache.mkdir(parents=True,exist_ok=True)
        run('C5/bootstrap/source/init-'+row['path'].replace('/','__'),['git','init','--bare',cache])
        shutil.copytree(gd/'objects',cache/'objects',dirs_exist_ok=True)
        (cache/'refs/heads').mkdir(parents=True,exist_ok=True);(cache/'refs/heads/frozen').write_text(row['commit']+'\n');(cache/'HEAD').write_text('ref: refs/heads/frozen\n')
        if (gd/'shallow').exists():shutil.copyfile(gd/'shallow',cache/'shallow')
        dest=SOC/row['path']
        run('C5/bootstrap/source/clone-'+row['path'].replace('/','__'),['git','clone','--no-hardlinks',cache,dest],timeout=180)
        head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=dest,text=True).strip();assert head==row['commit']
        # Content comparison to canonical Git archive proves Windows CRLF state is not imported.
        with tarfile.open(local(row['archive'])) as tar:
            count=0
            for member in tar:
                if member.isfile():assert (dest/member.name).read_bytes()==tar.extractfile(member).read(),(row['path'],member.name);count+=1
        clones.append({'path':str(dest),'commit':head,'canonical_files_compared':count})
    before=sha(SOC/'rocket-chip/src/main/scala/amba/axi4/Bundles.scala')
    run('C5/bootstrap/source/dev-init',['make','-j1','dev-init'],cwd=SOC,inputs=[SOC/'Makefile',SOC/'patch/rocket-chip.patch'],timeout=180)
    diff=subprocess.check_output(['git','diff','--stat'],cwd=SOC/'rocket-chip',text=True)
    lock.update({'status':'PASS_SOURCE_DEV_INIT','runtime':str(SOC),'local_bootstrap_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=SOC,text=True).strip(),'verified_upstream_tree':tree,'bootstrap_git_note':'Top local commit is intentionally distinct; its tree exactly matches the official fixed commit tree. Recursive module HEADs are the actual upstream commits.','recursive_runtime':clones,'patch_sha256':sha(SOC/'patch/rocket-chip.patch'),'rocket_patch_diff_stat':diff,'AXI_bundles_before':before,'AXI_bundles_after':sha(SOC/'rocket-chip/src/main/scala/amba/axi4/Bundles.scala')})
    dump(ROOT/'reports/C5_source_lock.json',lock)
    print('C5_ACTUAL_DEV_INIT_PASS',flush=True)

def tools():
    lock=json.loads((ROOT/'reports/C5_toolchain_downloads.json').read_text());TOOLS.mkdir(parents=True,exist_ok=True);jdk=TOOLS/'jdk17'
    for row in lock['files']:
        path=local(row['file']);assert sha(path)==row['sha256']
        if row['name'].startswith('openjdk'):
            run('C5/bootstrap/tools/extract-'+row['name'],['dpkg-deb','-x',path,jdk],inputs=[path],timeout=120)
    links=[]
    for p in sorted(jdk.rglob('*')):
        if not p.is_symlink():continue
        target=os.readlink(p)
        if target.startswith('/etc/java-17-openjdk'):
            mapped=jdk/target.lstrip('/');assert mapped.exists(),(p,mapped)
            p.unlink();p.symlink_to(os.path.relpath(mapped,p.parent));links.append({'path':str(p),'original_target':target,'portable_target':os.readlink(p)})
    home=jdk/'usr/lib/jvm/java-17-openjdk-amd64';java=home/'bin/java';javac=home/'bin/javac'
    env={'JAVA_HOME':str(home),'PATH':str(home/'bin')+':'+os.environ['PATH']}
    run('C5/bootstrap/tools/java-version',[java,'-version'],env=env)
    fixture=ROOT/'C/C5/generation/tool-controls';fixture.mkdir(parents=True,exist_ok=True)
    positive=fixture/'Positive.java';positive.write_text('public class Positive { public static void main(String[] a) { if (7+9!=16) throw new AssertionError(); System.out.println("JAVA_CONTROL_PASS"); }}\n')
    negative=fixture/'Negative.java';negative.write_text('public class Negative { public static void main(String[] a) { missing_symbol(); }}\n')
    classes=WORK/'soc-generation/tool-controls';classes.mkdir(parents=True,exist_ok=True)
    run('C5/bootstrap/tools/javac-positive',[javac,'-d',classes,positive],inputs=[positive],env=env)
    out,_,_=run('C5/bootstrap/tools/java-positive',[java,'-cp',classes,'Positive'],env=env);assert 'JAVA_CONTROL_PASS' in out
    _,error,_=run('C5/bootstrap/tools/javac-negative',[javac,'-d',classes,negative],inputs=[negative],env=env,expected=(1,));assert 'cannot find symbol' in error
    trust=fixture/'TrustStore.java';trust.write_text('''import java.nio.file.*; import java.io.*; import java.security.*; import java.security.cert.*;
public class TrustStore { public static void main(String[] args) throws Exception {
KeyStore ks=KeyStore.getInstance("JKS"); char[] password="changeit".toCharArray(); ks.load(null,password); int i=0;
try(InputStream in=Files.newInputStream(Path.of(args[0]))) { for(java.security.cert.Certificate cert:CertificateFactory.getInstance("X.509").generateCertificates(in)) ks.setCertificateEntry("system-ca-"+(i++),cert); }
try(OutputStream out=Files.newOutputStream(Path.of(args[1]))) { ks.store(out,password); } System.out.println("TRUST_ROOTS "+i);
}}
''')
    certs=Path('/etc/ssl/certs/ca-certificates.crt');store=TOOLS/'system-ca.jks'
    run('C5/bootstrap/tools/portable-trust-store',[java,'-Xmx256m',trust,certs,store],env=env,inputs=[trust,certs],outputs=[store])
    cache=TOOLS/'cache';cache.mkdir(exist_ok=True)
    millrow=next(x for x in lock['files'] if x['name']=='mill-0.12.4-assembly');launcher=next(x for x in lock['files'] if x['name']=='mill-0.12.4')
    mill=TOOLS/'bin/mill';mill.parent.mkdir(exist_ok=True);shutil.copyfile(local(launcher['file']),mill);mill.chmod(0o755)
    assembly=cache/'mill/download/0.12.4';assembly.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(local(millrow['file']),assembly);assembly.chmod(0o755)
    fir=next(x for x in lock['files'] if x['name']=='firtool');extract(local(fir['file']),TOOLS/'firtool');firtool=TOOLS/'firtool/firtool-1.105.0/bin/firtool';assert firtool.is_file();firtool.chmod(0o755)
    patch=SOC/'patch/firtool'
    if patch.is_symlink():assert patch.resolve()==(TOOLS/'firtool').resolve()
    else:assert not patch.exists();patch.symlink_to(TOOLS/'firtool',target_is_directory=True)
    opts=f'-Xmx{load_policy()["jvm_heap_mib"]}m -XX:ActiveProcessorCount=2 -Djavax.net.ssl.trustStore={store} -Djavax.net.ssl.trustStorePassword=changeit'
    env.update(PATH=str(TOOLS/'bin')+':'+env['PATH'],XDG_CACHE_HOME=str(cache),COURSIER_CACHE=str(cache/'coursier'),COURSIER_REPOSITORIES='https://repo.maven.apache.org/maven2',MILL_JVM_OPTS=opts,JAVA_OPTS=opts,JAVA_TOOL_OPTIONS=opts)
    run('C5/bootstrap/tools/mill-version',[mill,'--version'],env=env,cwd=SOC,timeout=120)
    run('C5/bootstrap/tools/firtool-version',[firtool,'--version'],env=env)
    finish_tools(env,links)

def finish_tools(env=None,links=None):
    home=TOOLS/'jdk17/usr/lib/jvm/java-17-openjdk-amd64';java=home/'bin/java';javac=home/'bin/javac';mill=TOOLS/'bin/mill';assembly=TOOLS/'cache/mill/download/0.12.4';firtool=TOOLS/'firtool/firtool-1.105.0/bin/firtool';store=TOOLS/'system-ca.jks';certs=Path('/etc/ssl/certs/ca-certificates.crt')
    fixture=ROOT/'C/C5/generation/tool-controls';classes=WORK/'soc-generation/tool-controls'
    if env is None:
        opts=f'-Xmx{load_policy()["jvm_heap_mib"]}m -XX:ActiveProcessorCount=2 -Djavax.net.ssl.trustStore={store} -Djavax.net.ssl.trustStorePassword=changeit'
        env={'JAVA_HOME':str(home),'PATH':str(TOOLS/'bin')+':'+str(home/'bin')+':'+os.environ['PATH'],'XDG_CACHE_HOME':str(TOOLS/'cache'),'COURSIER_CACHE':str(TOOLS/'cache/coursier'),'COURSIER_REPOSITORIES':'https://repo.maven.apache.org/maven2','MILL_JVM_OPTS':opts,'JAVA_OPTS':opts,'JAVA_TOOL_OPTIONS':opts}
        links=[]
        for p in sorted(home.rglob('*')):
            if p.is_symlink() and p.resolve().is_relative_to(TOOLS/'jdk17/etc/java-17-openjdk'):
                links.append({'path':str(p),'original_target':'/'+p.resolve().relative_to(TOOLS/'jdk17').as_posix(),'portable_target':os.readlink(p)})
    for name in ['java-version','javac-positive','java-positive','javac-negative','portable-trust-store','mill-version','firtool-version']:
        assert json.loads((ROOT/'artifacts/C5/bootstrap/tools'/name/'run.json').read_text())['status']=='PASS',name
    good=fixture/'good.fir';good.write_text('FIRRTL version 4.0.0\ncircuit Control :\n  public module Control :\n    input a : UInt<1>\n    output y : UInt<1>\n    connect y, a\n')
    bad=fixture/'bad.fir';bad.write_text('not FIRRTL syntax\n');verilog=classes/'Control.sv'
    run('C5/bootstrap/tools/firtool-positive',[firtool,good,'-o',verilog],env=env,inputs=[good],outputs=[verilog]);assert 'module Control' in verilog.read_text()
    _,error,_=run('C5/bootstrap/tools/firtool-negative',[firtool,bad,'-o',classes/'bad.sv'],env=env,inputs=[bad],expected=(1,));assert 'error:' in error
    dump(ROOT/'reports/C5_toolchain.json',{'status':'PASS_TOOLS_NOT_SOC_GENERATION','environment':env,'binaries':[{'path':str(p),'sha256':sha(p)} for p in [java,javac,mill,assembly,firtool]],'portable_symlink_adjustments':links,'trust_store':{'path':str(store),'sha256':sha(store),'source':str(certs),'source_sha256':sha(certs),'scope':'Task-local JKS derived from existing OS trusted CA bundle; no system trust configuration changed.'},'downloads_report':'reports/C5_toolchain_downloads.json','generation_limits':{'jvm_heap_gib':load_policy()['jvm_heap_mib']/1024,'jvm_active_processors':2,'make_jobs':1,'system_available_memory_threshold_gib':load_policy()['windows_start_available_mib']/1024},'scope':'Portable extracted tools; actual Java/firtool positive and negative controls, Mill version launch. SoC generation still pending.'})
    print('C5_PORTABLE_TOOLS_PASS',flush=True)

if __name__=='__main__':
    if '--resume-controls' in sys.argv:finish_tools()
    else:
        if '--tools-only' not in sys.argv:sources()
        if '--sources-only' not in sys.argv:tools()
