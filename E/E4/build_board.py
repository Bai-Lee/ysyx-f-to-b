from common import *
def main():
    root=ROOT/'E/E4';run('board/library',['make','-f',NVBOARD/'scripts/nvboard.mk','-j2','nvboard-archive'],cwd=WORK,timeout=180)
    run('board/official_build',['make','-j2','VERILATOR='+str(VERILATOR)],cwd=NVBOARD/'example',timeout=240)
    pin=WORK/'auto_bind.cpp';run('board/pin_bind',['python3',NVBOARD/'scripts/auto_pin_bind.py',root/'constr/lab_board.nxdc',pin],inputs=[root/'constr/lab_board.nxdc',NVBOARD/'scripts/auto_pin_bind.py'])
    src=[root/'rtl'/n for n in ['comb.sv','sequential.sv','keyboard.sv','vga.sv','scpu.sv','cpu_top.sv','program_rom.sv','lab_board.sv']]
    sdl=subprocess.check_output(['sdl2-config','--cflags'],text=True).strip()
    archive=NVBOARD/'build/nvboard.a'
    flags=['-Wno-DECLFILENAME','--timescale','1ns/1ns','-CFLAGS',sdl+' -I'+str(NVBOARD/'usr/include'),'-LDFLAGS',str(archive)+' -lSDL2_image -lSDL2_ttf -lSDL2']
    exe=build('lab_board',src,root/'csrc/board_main.cpp','lab_board',trace=False,extra=[pin,WORK/'semu.o'],flags=flags,additional_inputs=[archive,root/'csrc/semu.h'])
    bench=Path('/home/USER/ysyx-workbench')
    staged=subprocess.check_output(['git','diff','--cached','--name-only'],cwd=bench,text=True).splitlines()
    assert all(s=='.gitignore' or s.startswith('npc/') for s in staged)
    if staged:run('framework/restore_owned_index',['git','read-tree','HEAD'],cwd=bench)
    o,e,r=run('framework/make_sim',['make','-j2','sim'],cwd=bench/'npc',timeout=240)
    assert 'Error ' not in e and 'cannot ' not in e,e
    o,e,r=run('framework/tracer_log',['git','log','-1','--format=fuller','tracer-ysyx'],cwd=Path('/home/USER/ysyx-workbench'))
    assert 'sim RTL' in o and 'AI_AUTONOMOUS_ENGINEERING_TEST' in o
    traced=subprocess.check_output(['git','show','tracer-ysyx:npc/vsrc/dual.sv'],cwd=bench)
    assert traced==(bench/'npc/vsrc/dual.sv').read_bytes()
    run('framework/traced_files',['git','ls-tree','-r','--name-only','tracer-ysyx','npc'],cwd=bench)
    dump(ROOT/'reports/E4_board_build.json',{'status':'PASS','exe':str(exe),'sha256':sha(exe),'nvboard_commit':'b5f49b68a85f4a1a185086cbd6532fff3ecda454','official_example':str(NVBOARD/'example/build/top'),'gui_status':'NOT_RUN'})
    result(['E4-M006','E4-R003'],['artifacts/E4/framework/make_sim','artifacts/E4/framework/tracer_log','E/E4/npc/Makefile'],'Real one-command make sim and preserved exact git_commit call; tracer commit exists and explicitly identifies AI engineering work without fabricated student identity.')
    print('BOARD_BUILD_PASS',flush=True)
if __name__=='__main__':main()
