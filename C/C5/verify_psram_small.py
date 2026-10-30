from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from support import select_build


def main():
    subprocess.run(['python3',str(ROOT/'C/C5/prepare_am.py')],check=True)
    base=WORK/'c5/workbench';am=base/'abstract-machine';app=base/'psram-small';app.mkdir(exist_ok=True)
    source=ROOT/'C/C5/programs/mem-test.c';shutil.copyfile(source,app/'main.c')
    (app/'Makefile').write_text('NAME = psram-small\nSRCS = main.c\nCFLAGS += -DMEMTEST_BASE=0x80000000u -DMEMTEST_BYTES=4096u\ninclude $(AM_HOME)/Makefile\n')
    image=app/'build/psram-small-riscv32e-ysyxsoc-flash.bin';elf=image.with_suffix('.elf')
    run('C5/psram-small/build',['make','-j1','ARCH=riscv32e-ysyxsoc-flash','insert-arg'],cwd=app,env={'AM_HOME':str(am),'NPC_HOME':str(base/'npc')},inputs=[source,app/'Makefile',*sorted((am/'am/src/riscv/ysyxsoc').glob('*'))],outputs=[image,elf],timeout=180)
    ref=WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so';rows=[]
    for mode in ['spi','qpi']:
        build=select_build('30000000-cycle'+('-qpi' if mode=='qpi' else ''));exe=Path(build['executable']);tag='C5/psram-small/'+mode
        directory=ROOT/'artifacts'/tag;directory.mkdir(parents=True,exist_ok=True);result=directory/'simulation.json'
        run(tag,[exe,'--flash',image,'--ref',ref,'--report',result,'--coverage-base','0x80000000','--coverage-size','4096','--max-cycles','200000000'],inputs=[exe,image,elf,ref],outputs=[result],timeout=600)
        data=json.loads(result.read_text());assert data['result']=='GOOD_TRAP' and data['diff_enabled'] and data['diff_checked']+data['device_sync_checked']==data['instructions']
        coverage=data['coverage'];assert coverage['unique_read_bytes']==coverage['unique_written_bytes']==4096
        assert coverage['read_ops_by_width']==coverage['write_ops_by_width']==[8192,4096,4096]
        commands=data['psram']['commands_spi_read_write_qpi_read_write']
        if mode=='spi':assert commands==[16384,16384,0,0] and data['psram']['qpi_entries']==0
        else:assert commands==[0,0,16384,16384] and data['psram']['qpi_entries']==1
        assert data['psram']['maximum_byte_address']==4095
        rows.append({'mode':mode,'status':'PASS','simulation':data,'image_sha256':sha(image),'elf_sha256':sha(elf),'evidence':'artifacts/'+tag})
        dump(ROOT/'reports/C5_psram_small.json',{'status':'IN_PROGRESS','runs':rows})
    a,b=[r['simulation'] for r in rows]
    assert a['gpr']==b['gpr'] and a['instructions']==b['instructions'] and b['cycles']<a['cycles']
    dump(ROOT/'reports/C5_psram_small.json',{'status':'PASS_ACTUAL_SPI_QPI_CPU_MEMORY','runs':rows,
         'cycles_saved_by_qpi':a['cycles']-b['cycles'],'scope':'Same unmodified program image on4KiB SPI and QPI hardware profiles. All8/16/32/64-bit address/inverse patterns cover4096bytes; all memory accesses checked against NEMU. Actual pin-model command/read/write counters verify the serial path and35h mode entry; QPI requires fewer cycles. Full4MiB remains separate.'})
    mark(['C5-M024','C5-M025'],'PASS',['reports/C5_psram_model.json','reports/C5_psram_controller.json','reports/C5_psram_small.json'],'Pin-level IS66 model and preserved/adapted Efabless SPI/QPI controllers, exhaustive4KiB CPU memory patterns, warm-reset/mask controls and fasterQPI using identical software.')
    print('C5_PSRAM_SPI_AND_QPI_CPU_PASS',flush=True)


if __name__=='__main__':main()
