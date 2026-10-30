from pathlib import Path
import sys,re,struct
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *


def main():
    base=ROOT/'C/C5';out=WORK/'c5/programs';out.mkdir(parents=True,exist_ok=True)
    compiler=Path(shutil.which('riscv64-linux-gnu-gcc'));objcopy=Path(shutil.which('riscv64-linux-gnu-objcopy'));objdump=Path(shutil.which('riscv64-linux-gnu-objdump'))
    builds=json.loads((ROOT/'reports/C5_soc_build.json').read_text())['variants'];build=next(r for r in builds if r['reset_pc']==0x20000000 and not r.get('mutant',False) and not r.get('psram_qpi',False) and r.get('psram_bytes',4096)==4096 and not r.get('fast_flash',False) and not r.get('cycle_sim',False));exe=Path(build['executable']);assert sha(exe)==build['sha256']
    images={};rows=[]
    for name,source,flags in [('first-ebreak','first-ebreak.S',[]),('char-halt','char-test.c',['-DFINISH_TRAP']),('char-line','char-test.c',['-DINCLUDE_NEWLINE']),('char-only','char-test.c',[])]:
        elf=out/(name+'.elf');binary=out/(name+'.bin');src=base/'programs'/source
        run('C5/boot/'+name+'/compile',[compiler,'-march=rv32e','-mabi=ilp32e','-O2','-ffreestanding','-fno-pie','-fno-stack-protector','-nostdlib','-static','-Wl,--build-id=none,-Ttext=0x20000000,-e,_start',*flags,src,'-o',elf],inputs=[compiler,src],outputs=[elf])
        run('C5/boot/'+name+'/extract',[objcopy,'-O','binary','-j','.text',elf,binary],inputs=[objcopy,elf],outputs=[binary])
        disassembly,_,_=run('C5/boot/'+name+'/disassemble',[objdump,'-d',elf],inputs=[objdump,elf])
        assert '20000000 <_start>:' in disassembly and binary.stat().st_size<=4096
        images[name]={'binary':binary,'elf':elf,'binary_sha256':sha(binary),'elf_sha256':sha(elf)}
    assert images['first-ebreak']['binary'].read_bytes()==bytes.fromhex('73001000')
    bad=out/'illegal.bin';bad.write_bytes(struct.pack('<I',0xffffffff))
    for name,binary,expected in [('first-ebreak',images['first-ebreak']['binary'],0),('char-halt',images['char-halt']['binary'],0),('illegal',bad,3)]:
        d=ROOT/'artifacts/C5/boot'/name/'run';d.mkdir(parents=True,exist_ok=True);result=d/'simulation.json';trace=d/'events.log'
        stdout,stderr,_=run('C5/boot/'+name+'/run',[exe,'--mrom',binary,'--report',result,'--trace',trace,'--no-diff'],inputs=[exe,binary],outputs=[result,trace],expected=(expected,))
        data=json.loads(result.read_text());assert data['exit_code']==expected and not data['diff_enabled']
        if name=='first-ebreak':assert data['instructions']==1 and data['pc']==0x20000000 and data['axi_channels']==[1,1,0,0,0] and data['result']=='GOOD_TRAP'
        elif name=='char-halt':assert stdout=='A' and data['result']=='GOOD_TRAP' and data['axi_channels'][2:]==[1,1,1]
        else:assert data['result']=='NPC_FAULT' and data['fault']==1 and data['instructions']==0
        rows.append({'name':name,'status':'PASS','result':data,'evidence':'artifacts/C5/boot/'+name})
    for name,image,expected,buffered in [('line-buffered-newline','char-line','line',True),('line-buffered-without-newline','char-only','none',True),('unbuffered-without-newline','char-only','A',False)]:
        tag='C5/boot/stdout/'+name;directory=ROOT/'artifacts'/tag/'observation';probe=base/'sim/stdout_probe.py'
        command=['python3',probe,'--exe',exe,'--image',images[image]['binary'],'--expected',expected,'--output',directory]+(['--buffered'] if buffered else [])
        run(tag,command,inputs=[probe,exe,images[image]['binary']],outputs=[directory/'observation.json',directory/'child.stdout',directory/'child.stderr'],timeout=15)
        rows.append({'name':name,'status':'PASS','observation':json.loads((directory/'observation.json').read_text()),'evidence':'artifacts/'+tag})
    dump(ROOT/'reports/C5_boot.json',{'status':'PASS_FIRST_MROM_AND_UART_OUTPUT','runs':rows,'programs':{k:{key:str(v) for key,v in row.items()} for k,row in images.items()},
         'tool_fingerprints':[{'path':str(p),'sha256':sha(p)} for p in [compiler,objcopy,objdump]],
         'scope':'Actual generated full SoC path: CPU AXI4 to MROM and UART16550 APB/FIFO. Single first ebreak; compiled char-test; buffering positive/negative controls. DiffTest intentionally disabled only for these initial steps; NEMU MROM/SRAM support still pending. UART FIFO debug output is not physical TX pin acceptance.'})
    mark(['C5-M004','C5-M005','C5-M006'],'PASS',['reports/C5_boot.json'],'Actual first MROM instruction, compiled char-test and newline-free real UART FIFO output with buffering controls; initial scoped DiffTest disable declared.')
    print('C5_BOOT_FIRST_CHAR_BUFFERING_PASS',flush=True)


if __name__=='__main__':main()
