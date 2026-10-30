from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *


def main():
    subprocess.run(['python3',str(ROOT/'C/C5/prepare_am.py')],check=True)
    base=WORK/'c5/workbench';am=base/'abstract-machine';ref=WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so'
    images=WORK/'c5/images';images.mkdir(parents=True,exist_ok=True);flash=images/'pattern16m.bin'
    if not flash.exists():
        low=bytes((i^(i>>8)^0xa7)&255 for i in range(65536))
        with flash.open('wb') as stream:
            for high in range(256):stream.write(low.translate(bytes(i^high for i in range(256))))
    assert flash.stat().st_size==16*1024*1024
    builds=json.loads((ROOT/'reports/C5_soc_build.json').read_text())['variants']
    rows=[];env={'AM_HOME':str(am),'NPC_HOME':str(base/'npc')}
    cases=[('fast-data','flash-data.c',True,False),('bitrev','spi-bitrev.c',False,False),('serial-data','flash-data.c',False,True)]
    for name,filename,fast,serial in cases:
        build=next(r for r in builds if r['reset_pc']==0x20000000 and not r.get('mutant',False) and not r.get('psram_qpi',False) and r.get('psram_bytes',4096)==4096 and r.get('fast_flash',False)==fast and not r.get('cycle_sim',False))
        exe=Path(build['executable']);assert sha(exe)==build['sha256']
        app=base/('spi-'+name);app.mkdir(exist_ok=True);src=ROOT/'C/C5/programs'/filename;helper=ROOT/'C/C5/programs/spi_io.h'
        shutil.copyfile(src,app/'main.c');shutil.copyfile(helper,app/helper.name)
        (app/'Makefile').write_text('NAME = spi-'+name+'\nSRCS = main.c\n'+('CFLAGS += -DSERIAL_READ\n' if serial else '')+'include $(AM_HOME)/Makefile\n')
        image=app/'build'/('spi-'+name+'-riscv32e-ysyxsoc.bin');elf=image.with_suffix('.elf');tag='C5/spi/'+name
        run(tag+'/build',['make','-j1','ARCH=riscv32e-ysyxsoc','insert-arg'],cwd=app,env=env,inputs=[src,helper,app/'Makefile',*sorted((am/'am/src/riscv/ysyxsoc').glob('*'))],outputs=[image,elf],timeout=180)
        assert image.stat().st_size<=4096
        out=ROOT/'artifacts'/tag;out.mkdir(parents=True,exist_ok=True);report=out/'simulation.json';trace=out/'events.log'
        stdout,stderr,_=run(tag+'/run',[exe,'--mrom',image,'--flash',flash,'--ref',ref,'--report',report,'--trace',trace,'--trace-limit','10000','--max-cycles','10000000'],inputs=[exe,image,elf,flash,ref],outputs=[report,trace],timeout=180)
        data=json.loads(report.read_text());assert data['result']=='GOOD_TRAP' and data['diff_enabled'] and data['diff_checked']+data['device_sync_checked']==data['instructions']
        spi=data['spi'];assert spi['incomplete_bits']==0 and not spi['capture_truncated']
        if fast:assert data['flash_dpi_calls']>=13 and spi['transfers']==0
        elif name=='bitrev':
            assert spi['transfers']==256 and data['flash_dpi_calls']==0
            for value,packet in enumerate(spi['packets']):
                reverse=int(f'{value:08b}'[::-1],2)
                assert packet['select']==128 and packet['bits']==16 and packet['tx_low64']==value<<8 and packet['rx_low64']&255==reverse,packet
        else:
            addresses=[0,4,0x1fc,0x1000,0x12344,0x7ffffc,0xfffffc]
            assert spi['transfers']==7 and data['flash_dpi_calls']==7
            for address,packet in zip(addresses,spi['packets']):
                expected=int.from_bytes(bytes((i^(i>>8)^(i>>16)^0xa7)&255 for i in range(address,address+4)),'big')
                assert packet['select']==1 and packet['bits']==64 and packet['tx_low64']==(0x03000000|address)<<32 and packet['rx_low64']&0xffffffff==expected,packet
        rows.append({'name':name,'status':'PASS','fast_flash':fast,'simulation':data,'source_sha256':sha(src),'helper_sha256':sha(helper),
                     'image_sha256':sha(image),'elf_sha256':sha(elf),'flash_sha256':sha(flash),'evidence':'artifacts/'+tag})
        dump(ROOT/'reports/C5_spi.json',{'status':'IN_PROGRESS','runs':rows})
    dump(ROOT/'reports/C5_spi.json',{'status':'PASS_FAST_ARRAY_AND_REAL_SPI_CONTROLS','runs':rows,
         'scope':'FAST_FLASH is a separately built lookup-only prototype. Real SPI cases compile without FAST_FLASH, configure CTRL before GO, use Tx_NEG=1/Rx_NEG=0/MSB-first, divider0, automatic active-low SS. All256 bit reversals and seven real03h flash command/address/data streams verified at controller sample events and software results. Flash window256MiB vs physical array16MiB explicitly distinguished; only physical-capacity addresses tested.'})
    mark(['C5-M016','C5-M017','C5-M018'],'PASS',['reports/C5_spi.json'],'Actual separately scoped fast lookup, exhaustive bitrev over SPI slave7, and serial flash reads through slave0 with captured command/address/data bits.')
    print('C5_SPI_BITREV_AND_FLASH_PASS',flush=True)


if __name__=='__main__':main()
