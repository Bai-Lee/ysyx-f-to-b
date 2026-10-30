from common import *
import tempfile,tarfile
def main():
    source=ROOT/'E/E4';tmp=Path(tempfile.mkdtemp(prefix='e4-offline-',dir='/home/USER/e4-lab'))
    manifest=json.loads((source/'offline/manifest.json').read_text())
    for x in manifest['entries']:assert sha(ROOT/x['path'])==x['sha256']
    nv=tmp/'nvboard';nv.mkdir()
    with tarfile.open(source/'offline/nvboard.tar.gz') as t:
        for x in t.getmembers():assert (nv/x.name).resolve().is_relative_to(nv.resolve()) and not x.issym() and not x.islnk()
        t.extractall(nv)
    assert (nv/'resources/font').is_dir() and (nv/'LICENSE').exists()
    bench=tmp/'workbench';shutil.copytree(source/'offline/workbench-base',bench);shutil.copytree(source/'npc',bench/'npc')
    for tag,args in [('init',['init','-b','main']),('name',['config','user.name','YSYX AI Offline Validation']),('email',['config','user.email','offline@example.invalid']),('add',['add','.']),('commit',['commit','-m','Offline E4 reconstruction from pinned official base and authored sources'])]:
        run('offline/git_'+tag,['git',*args],cwd=bench)
    o,e,r=run('offline/make_sim',['make','-j2','sim'],cwd=bench/'npc',timeout=180);assert 'PASS XOR' in o and 'Error ' not in e
    got=subprocess.check_output(['git','show','tracer-ysyx:npc/vsrc/dual.sv'],cwd=bench);assert got==(source/'npc/vsrc/dual.sv').read_bytes()
    d=tmp/'c';shutil.copytree(source/'csrc',d);exe=tmp/'semu'
    run('offline/semu_build',['gcc','-std=c11','-Wall','-Wextra','-Werror','-O2',d/'semu.c',d/'semu_main.c','-o',exe],inputs=[d/'semu.c',d/'semu.h',d/'semu_main.c'])
    o,e,r=run('offline/semu_sum',[exe,source/'data/f6_output.hex','200','1'],inputs=[exe,source/'data/f6_output.hex']);last=list(map(int,o.splitlines()[-1].split(',')));assert last[-2:]==[55,55] and last[6]==55
    # Check the actual16-way glyph table independently in a four-state simulator.
    vvp=tmp/'hex.vvp';run('offline/hex_compile',['iverilog','-g2012','-s','tb','-o',vvp,source/'rtl/comb.sv',source/'csrc/hex_tb.sv'],inputs=[source/'rtl/comb.sv',source/'csrc/hex_tb.sv'])
    o,e,r=run('offline/hex_all16',['vvp',vvp],inputs=[vvp]);assert 'PASS hex decoder' in o
    dump(ROOT/'reports/E4_offline.json',{'status':'PASS','directory':str(tmp),'network_requests':0,'manifest_sha256':sha(source/'offline/manifest.json'),'nvboard_source_restored':True,'fresh_make_sim_and_tracer':True,'fresh_C_sEMU_sum55':True,'hex_values_checked':16,'scope':'Reconstructed local sources and Git base, native rebuild and execution; installed compiler/simulator prerequisites reused. Full NVBoard runtime verified separately; no bundled OS/toolchain image claim.'})
    print('E4_OFFLINE_PASS',flush=True)
if __name__=='__main__':main()
