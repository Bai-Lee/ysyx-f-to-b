from pathlib import Path
import sys,argparse,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from support import select_build


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--build-only',action='store_true');args=parser.parse_args()
    base=WORK/'c5/workbench';am=base/'abstract-machine';source=ROOT/'C/C5/programs/spi-shared.c';rows=[]
    for name,profile in [('flash','flash'),('sram','sram-code')]:
        app=base/('spi-shared-'+name);app.mkdir(exist_ok=True);shutil.copyfile(source,app/'main.c')
        (app/'Makefile').write_text('NAME = spi-shared-'+name+'\nSRCS = main.c\ninclude $(AM_HOME)/Makefile\n')
        arch='riscv32e-ysyxsoc-'+profile;image=app/'build'/('spi-shared-'+name+'-'+arch+'.bin');elf=image.with_suffix('.elf');tag='C5/spi-shared/'+name
        run(tag+'/build',['make','-j1','ARCH='+arch,'insert-arg'],cwd=app,env={'AM_HOME':str(am)},inputs=[source,app/'Makefile',*sorted((am/'am/src/riscv/ysyxsoc').glob('*'))],outputs=[image,elf],timeout=180)
        text,_,_=run(tag+'/symbols',['riscv64-linux-gnu-nm','-n',elf],inputs=[elf]);symbols={parts[2]:int(parts[0],16) for line in text.splitlines() if len(parts:=line.split())==3 and re.fullmatch('[0-9a-fA-F]+',parts[0])}
        function=next(value for key,value in symbols.items() if key.startswith('software_flash_read'))
        assert (0x30000000<=function<0x31000000) if name=='flash' else (0x0f000000<=function<0x0f001800)
        data=image.read_bytes();assert len(data)<0x80000;flash=app/'build/flash.bin';flash.write_bytes(data+b'\xff'*(0x80000-len(data))+bytes.fromhex('eeffc051'))
        if args.build_only:continue
        exe=Path(select_build('30000000-cycle-psram4m-qpi-sdram16x1-opt')['executable']);ref=WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so'
        folder=ROOT/'artifacts'/tag;result=folder/'simulation.json';trace=folder/'events.log';budget=folder/'resources.json'
        if result.exists():
            old=folder/'attempts'/str(time.time_ns());old.mkdir(parents=True);shutil.copyfile(result,old/result.name);assert sha(result)==sha(old/result.name);result.unlink()
        stdout,stderr,execution=run(tag+'/run',['python3',ROOT/'C/runtime/budget_exec.py','--report',budget,'--',exe,'--flash',flash,'--ref',ref,'--report',result,'--trace',trace,'--trace-limit','500000','--max-cycles','30000000'],inputs=[exe,ref,flash,elf],outputs=[result,trace,budget],expected=(1 if name=='flash' else 0,),timeout=120)
        events=trace.read_text();assert ' W 10001004 4 03080000' in events
        if name=='flash' and not result.exists():
            assert 'Unsupported command `00h`, only support `03h` read command' in stderr and 'Verilog $stop' in stdout
            assert re.search(r'^I \d+ 300[0-9a-f]{5} ',events,re.M) and re.search(r'^B \d+ 0 300[0-9a-f]{5} ',events,re.M)
            rows.append({'name':name,'status':'PASS','result':'FLASH_PROTOCOL_ASSERTION','model_command':'00h instead of03h','missing_host_simulation_report':'Expected: the Verilog model terminates beforehostreportfinalization; exactassertionandbus/PCtrace are checked.','instructions_traced':sum(line.startswith('I ') for line in events.splitlines()),'last_observed_cycle':max(int(line.split()[1]) for line in events.splitlines() if line),'function_address':function,'flash_image_sha256':sha(flash),'evidence':'artifacts/'+tag})
            continue
        actual=json.loads(result.read_text());uart=bytes.fromhex(actual['uart']['hex']).decode('ascii');match=re.search(r'C5_SHARED_SPI value=([0-9a-f]+) expected=51c0ffee',uart);assert match
        assert actual['diff_enabled'] and actual['diff_checked']+actual['device_sync_checked']==actual['instructions']
        if name=='flash':assert actual['result']=='BAD_TRAP' and actual['a0']==88 and int(match[1],16)!=0x51c0ffee
        else:assert actual['result']=='GOOD_TRAP' and int(match[1],16)==0x51c0ffee and actual['retired_by_region'][1]>0
        rows.append({'name':name,'status':'PASS','result':actual['result'],'exit_a0':actual['a0'],'observed_word':match[1],'function_address':function,'uart':uart,'cycles':actual['cycles'],'instructions':actual['instructions'],'flash_image_sha256':sha(flash),'evidence':'artifacts/'+tag})
    if not args.build_only:
        dump(ROOT/'reports/C5_spi_shared.json',{'status':'PASS_REPRODUCED_XIP_MANUAL_SPI_CONFLICT_AND_RELOCATION','runs':rows,'scope':'Same manualSPIregisterroutine withknownflashdata. Flashinstructionfetch reuses/reconfiguresSPI anddestroyssoftwaretransaction state: thelockedmodelexplicitlyasserts on00h ratherthan03h (ordata-mismatch88). Exactdiagnostic andbus/PCtrace are required; nohosttimeoutisaccepted. SRAMexecution succeeds. NEMUchecks eachretirednon-MMIOinstruction untilmodeltermination.'})
        mark(['C5-O007'],'PASS',['reports/C5_spi_shared.json'],'ActualFlash-executingmanualSPIread yieldswrongSPIcommand00h andanexplicitmodelassertion; relocatingcode/rodatatoSRAM succeeds. SharedSPIresourceconflict explained.')
    print('C5_SPI_SHARED_BUILT' if args.build_only else 'C5_SPI_SHARED_PASS',flush=True)


if __name__=='__main__':main()
