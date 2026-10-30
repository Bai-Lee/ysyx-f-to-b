from common import *
import tarfile
def main():
    dest=ROOT/'E/E4/offline';dest.mkdir(exist_ok=True);sources=[]
    run('export/nvboard',['git','archive','--format=tar.gz','-o',str(dest/'nvboard.tar.gz'),'HEAD'],cwd=NVBOARD)
    for name in ['overview.rst','install.rst','example_cc.rst','simulating.rst','warnings.rst']:
        p=VROOT/'docs/guide'/name;assert p.exists();to=dest/'verilator-guide'/name;to.parent.mkdir(exist_ok=True);shutil.copyfile(p,to);sources.append({'original':str(p),'path':str(to.relative_to(ROOT)),'sha256':sha(to)})
    for p in VROOT.glob('LICENSE*'):
        if p.is_file():shutil.copyfile(p,dest/'verilator-guide'/p.name)
    bench=Path('/home/USER/ysyx-workbench');base=dest/'workbench-base';base.mkdir(exist_ok=True)
    for name in ['Makefile','AGENTS.md','init.sh','.gitignore']:
        (base/name).write_bytes(subprocess.check_output(['git','show','a839def3f3b046f730537ea420d3075e725d27ce:'+name],cwd=bench))
    packages=['gcc','g++','make','git','iverilog','gtkwave','libsdl2-dev','libsdl2-image-dev','libsdl2-ttf-dev','liblz4-dev','xvfb','xauth','xdotool','scrot']
    o,e,r=run('tools/packages',['dpkg-query','-W','-f=${Package}\t${Version}\t${Architecture}\n',*packages])
    tools={}
    for name,p in [('verilator',VERILATOR),('verilator_bin',VROOT/'bin/verilator_bin'),*[(n,Path(shutil.which(n))) for n in ['g++','gcc','git','make','iverilog','vvp','gtkwave','fst2vcd','Xvfb','xdotool','scrot']]]:
        tools[name]={'path':str(p),'sha256':sha(p)}
    dump(ROOT/'reports/E4_tools.json',{'status':'PASS','tools':tools,'packages':[dict(zip(['package','version','architecture'],s.split('\t'))) for s in o.splitlines()],'verilator_source_commit':'983a06a16f2aea1cf4bda3a45099c8bad24d112c','verilator_version':'5.052 2026-09-05','nvboard_source_commit':'b5f49b68a85f4a1a185086cbd6532fff3ecda454','nvboard_history':'Upstream archived snapshot is shallow. Imported object bundle plus exact original shallow boundary; fsck verified. No full-history claim.','originality':'Local AI engineering experiment, not student independent-authorship certification.'})
    entries=[{'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size} for p in dest.rglob('*') if p.is_file() and p.name!='manifest.json']
    dump(dest/'manifest.json',{'status':'PASS','entries':entries,'verilator_docs':sources,'nvboard_commit':'b5f49b68a85f4a1a185086cbd6532fff3ecda454','tools_packaged':False,'scope':'Public NVBoard source/resources/license, selected Verilator source-version manuals, unchanged workbench base. Installed tools and full original course archive remain external prerequisites.'})
    print('E4_PUBLIC_EXPORT_PASS',len(entries),flush=True)
if __name__=='__main__':main()
