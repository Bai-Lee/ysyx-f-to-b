from pathlib import Path
import sys,struct,zipfile,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *


def main():
    subprocess.run(['python3',str(ROOT/'C/C5/prepare_am.py')],check=True)
    base=WORK/'c5/workbench';am=base/'abstract-machine';images=WORK/'c5/images';fixtures=WORK/'c5/xip-fixtures';fixtures.mkdir(parents=True,exist_ok=True)
    ref=WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so';pattern=images/'pattern16m.bin'
    build=next(r for r in json.loads((ROOT/'reports/C5_soc_build.json').read_text())['variants'] if r['reset_pc']==0x20000000 and not r.get('mutant',False) and not r.get('psram_qpi',False) and r.get('psram_bytes',4096)==4096 and not r.get('fast_flash',False) and r.get('cycle_sim',False))
    exe=Path(build['executable']);assert sha(exe)==build['sha256'];env={'AM_HOME':str(am),'NPC_HOME':str(base/'npc')}
    compiler=Path(shutil.which('riscv64-linux-gnu-gcc'));objcopy=Path(shutil.which('riscv64-linux-gnu-objcopy'));payloads={}
    for name,entry in [('sram',0x0f000800),('flash',0x30010000)]:
        elf=fixtures/('char-'+name+'.elf');binary=elf.with_suffix('.bin');src=ROOT/'C/C5/programs/char-test.c'
        run('C5/xip/payload-'+name+'/compile',[compiler,'-march=rv32e','-mabi=ilp32e','-O2','-ffreestanding','-fno-pie','-nostdlib','-static','-DFINISH_TRAP',f'-Wl,--build-id=none,-Ttext=0x{entry:08x},-e,_start',src,'-o',elf],inputs=[compiler,src],outputs=[elf])
        run('C5/xip/payload-'+name+'/extract',[objcopy,'-O','binary','-j','.text',elf,binary],inputs=[objcopy,elf],outputs=[binary])
        data=binary.read_bytes();assert len(data)%4==0 and 0<len(data)<512
        flash=images/('payload-'+name+'.bin');shutil.copyfile(pattern,flash)
        with flash.open('r+b') as f:f.seek(0x10000);f.write(data)
        words=struct.unpack('<'+'I'*(len(data)//4),data)
        header=f'#define PAYLOAD_ENTRY 0x{entry:08x}u\n#define PAYLOAD_OFFSET 0x10000u\n#define PAYLOAD_WORDS {len(words)}\n#ifdef COPY_TO_SRAM\nstatic const uint32_t payload_words[]={{'+','.join(f'0x{x:08x}u' for x in words)+'};\n#endif\n'
        payloads[name]={'entry':entry,'bytes':len(data),'flash':flash,'header':header,'binary_sha256':sha(binary),'elf_sha256':sha(elf)}
    recovered={}
    for name in ['fast-data','bitrev','serial-data']:
        with zipfile.ZipFile(ROOT/'artifacts/C5/spi'/name/'build/output_snapshot.zip') as z:
            member=next(n for n in z.namelist() if n.endswith('.bin'));target=fixtures/(name+'.bin');target.write_bytes(z.read(member));recovered[name]=target
    def compile_app(name,source,defines=(),header=None):
        folder=base/('xip-'+name);folder.mkdir(exist_ok=True);src=ROOT/'C/C5/programs'/source
        shutil.copyfile(src,folder/'main.c');shutil.copyfile(ROOT/'C/C5/programs/spi_io.h',folder/'spi_io.h')
        if header:(folder/'payload.h').write_text(header)
        manifest=folder/'Makefile';manifest.write_text('NAME = xip-'+name+'\nSRCS = main.c\n'+('CFLAGS += '+' '.join('-D'+d for d in defines)+'\n' if defines else '')+'include $(AM_HOME)/Makefile\n')
        binary=folder/'build'/('xip-'+name+'-riscv32e-ysyxsoc.bin');elf=binary.with_suffix('.elf')
        run('C5/xip/'+name+'/build',['make','-j1','ARCH=riscv32e-ysyxsoc','insert-arg'],cwd=folder,env=env,
            inputs=[src,manifest,folder/'spi_io.h',*([folder/'payload.h'] if header else []),*sorted((am/'am/src/riscv/ysyxsoc').glob('*'))],outputs=[binary,elf],timeout=180)
        assert binary.stat().st_size<=4096
        return binary
    copy=compile_app('copy-sram','flash-loader.c',['COPY_TO_SRAM'],payloads['sram']['header'])
    corrupt_copy=compile_app('copy-corrupt','flash-loader.c',['COPY_TO_SRAM','CORRUPT_COPY'],payloads['sram']['header'])
    jump=compile_app('jump-flash','flash-loader.c',[],payloads['flash']['header'])
    write=compile_app('write-rejected','flash-write.c')
    unsupported=compile_app('unsupported-command','spi-unsupported.c')
    bad_flash=images/'corrupt-pattern.bin';shutil.copyfile(pattern,bad_flash)
    with bad_flash.open('r+b') as f:v=f.read(1);f.seek(0);f.write(bytes([v[0]^1]))
    cases=[('xip-data',recovered['fast-data'],pattern,0),('normal-bitrev-after-xip',recovered['bitrev'],pattern,0),
           ('normal-spi-after-xip',recovered['serial-data'],pattern,0),('copy-sram',copy,payloads['sram']['flash'],0),
           ('copy-corrupt',corrupt_copy,payloads['sram']['flash'],1),('jump-flash',jump,payloads['flash']['flash'],0),
           ('write-rejected',write,pattern,3),('corrupt-flash-detected',recovered['fast-data'],bad_flash,1),('unsupported-command',unsupported,pattern,1)]
    rows=[]
    for name,binary,flash,expected in cases:
        tag='C5/xip/'+name;out=ROOT/'artifacts'/tag;out.mkdir(parents=True,exist_ok=True);report=out/'simulation.json';trace=out/'events.log'
        options=[]
        if name in ['copy-sram','copy-corrupt','jump-flash']:options=['--coverage-base','0x0f000800','--coverage-size',str(payloads['sram']['bytes'])]
        stdout,stderr,_=run(tag+'/run',[exe,'--mrom',binary,'--flash',flash,'--ref',ref,'--report',report,'--trace',trace,'--trace-limit','10000','--max-cycles','10000000',*options],inputs=[exe,binary,flash,ref],outputs=[trace] if name=='unsupported-command' else [report,trace],expected=(expected,),timeout=180)
        if name=='unsupported-command':
            assert re.search(r'Unsupport(?:ed)? command.*9f',stdout+stderr,re.I)
            rows.append({'name':name,'status':'PASS_MODEL_SCOPE_REJECTION','evidence':'artifacts/'+tag,'scope':'The teaching flash model supports03h only;9Fh is not claimed invalid for a real W25Q128JV.'});continue
        data=json.loads(report.read_text());assert data['diff_enabled'] and data['diff_checked']+data['device_sync_checked']==data['instructions']
        if expected==0:assert data['result']=='GOOD_TRAP'
        elif name=='write-rejected':assert data['result']=='NPC_FAULT' and data['fault']==5 and data['spi']['transfers']==0 and data['flash_dpi_calls']==0
        else:assert data['result']=='BAD_TRAP' and data['a0']==(42 if name=='copy-corrupt' else 32)
        if name=='xip-data':assert data['spi']['transfers']==13 and data['flash_dpi_calls']==13
        if name=='normal-bitrev-after-xip':assert data['spi']['transfers']==256 and data['flash_dpi_calls']==0
        if name=='normal-spi-after-xip':assert data['spi']['transfers']==7 and data['flash_dpi_calls']==7
        if name=='copy-sram':
            assert data['retired_by_region'][1]>0 and data['retired_by_region'][2]==0 and data['uart']['hex']=='41'
            assert data['coverage']['unique_written_bytes']==payloads['sram']['bytes'] and data['coverage']['unique_read_bytes']==payloads['sram']['bytes']
        if name=='copy-corrupt':assert data['retired_by_region'][1]==0
        if name=='jump-flash':assert data['retired_by_region'][2]>0 and data['retired_by_region'][1]==0 and data['coverage']['unique_written_bytes']==0 and data['uart']['hex']=='41'
        assert data['spi']['incomplete_bits']==0
        rows.append({'name':name,'status':'PASS','simulation':data,'image_sha256':sha(binary),'flash_sha256':sha(flash),'evidence':'artifacts/'+tag})
        dump(ROOT/'reports/C5_xip.json',{'status':'IN_PROGRESS','runs':rows})
    dump(ROOT/'reports/C5_xip.json',{'status':'PASS_REAL_SPI_COPY_AND_XIP','runs':rows,
         'wrapper_sha256':sha(ROOT/'C/C5/perip/spi/rtl/spi_top_apb.v'),
         'scope':'Real SPI hardware FSM configures CTRL with GO clear, loads TX/divider/SS, starts, polls and byte-swaps RX. Normal SPI registers remain usable. CPU copies and verifies compiled payload into SRAM before actual SRAM execution; separate jump executes directly from flash with zero writes to the SRAM payload region. Flash writes return SLVERR; corrupt copy/image and unsupported model command controls retained. Low24-bit flash address decode preserves the original256MiB window alias; physical capacity16MiB.'})
    mark(['C5-M019','C5-M020','C5-M021'],'PASS',['reports/C5_xip.json'],'Actual serial loader, verified SRAM execution, real XIP FSM and direct flash execution; errors and corrupted data rejected.')
    print('C5_REAL_FLASH_XIP_AND_SRAM_LOAD_PASS',flush=True)


if __name__=='__main__':main()
