from pathlib import Path
import sys,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--from-name');args_cli=parser.parse_args()
    subprocess.run(['python3',str(ROOT/'C/C5/prepare_am.py')],check=True)
    base=WORK/'c5/workbench';am=base/'abstract-machine';ref=WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so'
    build=next(r for r in json.loads((ROOT/'reports/C5_soc_build.json').read_text())['variants'] if r['reset_pc']==0x20000000 and not r.get('mutant',False) and not r.get('psram_qpi',False) and r.get('psram_bytes',4096)==4096 and not r.get('fast_flash',False) and not r.get('cycle_sim',False))
    exe=Path(build['executable']);assert sha(exe)==build['sha256'];rows=[]
    env={'AM_HOME':str(am),'NPC_HOME':str(base/'npc')}
    cases=[('hello-raw-empty','hello','raw',''),('hello-raw-short','hello','raw','abcdefgh'),
           ('hello-raw-long','hello','raw','0123456789abcdef'*3),('hello-divisor-only','hello','divisor','0123456789abcdef'*3),
           ('hello-polled-empty','hello','',''),('hello-polled-long','hello','','0123456789abcdef'*3)]
    cases += [('binary-'+str(n),'uart-check','',str(n)) for n in [1,8,16,64,257,512]]
    if args_cli.from_name:
        index=next(i for i,c in enumerate(cases) if c[0]==args_cli.from_name)
        prior=json.loads((ROOT/'reports/C5_uart.json').read_text())['runs']
        rows=[r for r in prior if r['name'] in {c[0] for c in cases[:index]}];assert len(rows)==index
        cases=cases[index:]
    for name,program,profile,args in cases:
        folder=base/program;folder.mkdir(exist_ok=True)
        if program=='uart-check':
            shutil.copyfile(ROOT/'C/C5/programs/uart-check.c',folder/'main.c')
            (folder/'Makefile').write_text('NAME = uart-check\nSRCS = main.c\ninclude $(AM_HOME)/Makefile\n')
        src=folder/('hello.c' if program=='hello' else 'main.c');arch='riscv32e-ysyxsoc'+('-'+profile if profile else '')
        image=folder/'build'/(program+'-'+arch+'.bin');elf=image.with_suffix('.elf');tag='C5/uart/'+name
        runtime=[*sorted((am/'am/src/riscv/ysyxsoc').glob('*')),am/'scripts/ysyxsoc-mrom.ld',am/'scripts/platform/ysyxsoc.mk',am/'scripts'/(arch+'.mk')]
        run(tag+'/build',['make','-j1','ARCH='+arch,'mainargs='+args,'insert-arg'],cwd=folder,env=env,inputs=[src,folder/'Makefile',*runtime],outputs=[image,elf],timeout=180)
        assert image.stat().st_size<=4096
        expected=("Hello, AbstractMachine!\nmainargs = '"+args+"'.\n").encode() if program=='hello' else bytes(i&255 for i in range(int(args)))
        out=ROOT/'artifacts'/tag;out.mkdir(parents=True,exist_ok=True);result=out/'simulation.json';trace=out/'events.log'
        pin_options=['--uart-bit-cycles','16'] if profile!='raw' else []
        stdout,stderr,_=run(tag+'/run',[exe,'--mrom',image,'--ref',ref,'--report',result,'--trace',trace,'--trace-limit','10000','--max-cycles','5000000',*pin_options],inputs=[exe,image,elf,ref],outputs=[result,trace],timeout=120)
        data=json.loads(result.read_text());assert data['result']=='GOOD_TRAP' and data['diff_enabled'] and data['diff_checked']+data['device_sync_checked']==data['instructions']
        uart=data['uart'];actual=bytes.fromhex(uart['hex']);assert not uart['capture_truncated']
        assert uart['attempted']==len(expected) and uart['accepted']==len(actual) and uart['accepted']+uart['dropped']==len(expected)
        if profile=='raw':assert uart['dropped']>0 and uart['maximum_fifo_occupancy']==16 and len(actual)<len(expected)
        elif profile=='':
            assert actual==expected and uart['dropped']==0 and uart['maximum_fifo_occupancy']==0
            assert data['uart_pin']['framing_errors']==0 and bytes.fromhex(data['uart_pin']['hex'])==expected
            # This Verilator's %c debug writer omits NUL. Actual serial bytes are
            # checked independently at the TX pin above, including NUL.
            assert (out/'run/stdout.log').read_bytes().startswith(expected.replace(b'\x00',b''))
        else:
            # Divider initialization changes transmission progress; capacity loss
            # remains a measured result, not a presumed fixed character count.
            assert uart['accepted']>0 and uart['dropped']>0 and data['uart_pin']['framing_errors']==0
            assert data['uart_pin']['frames']==uart['accepted'] and bytes.fromhex(data['uart_pin']['hex'])!=expected
        rows.append({'name':name,'status':'PASS_OBSERVATION' if profile else 'PASS_COMPLETE_OUTPUT','profile':profile,
                     'expected_hex':expected.hex(),'expected_bytes':len(expected),'simulation':data,'evidence':'artifacts/'+tag,
                     'source_sha256':sha(src),'image_sha256':sha(image),'elf_sha256':sha(elf)})
        dump(ROOT/'reports/C5_uart.json',{'status':'IN_PROGRESS','runs':rows})
    # Sampling at a deliberately wrong bit period must not reproduce the payload.
    bad_dir=ROOT/'artifacts/C5/uart/bad-sampling-period';bad_dir.mkdir(parents=True,exist_ok=True);bad_result=bad_dir/'simulation.json'
    run('C5/uart/bad-sampling-period',[exe,'--mrom',image,'--ref',ref,'--report',bad_result,'--uart-bit-cycles','8','--max-cycles','5000000'],inputs=[exe,image,ref],outputs=[bad_result],timeout=120)
    bad=json.loads(bad_result.read_text());assert bad['result']=='GOOD_TRAP' and (bad['uart_pin']['framing_errors']>0 or bytes.fromhex(bad['uart_pin']['hex'])!=expected)
    dump(ROOT/'reports/C5_uart.json',{'status':'PASS_UART_CAUSE_DIVISOR_AND_POLLED_OUTPUT','runs':rows,'wrong_sampling_period_control':bad,
         'overflow_detail':'The original tfifo RAM write-enable is raw push even when count==16; overflowing software can overwrite an unread FIFO entry. The accepted-byte debug log can therefore differ from actual TX payload in the unpolled divisor-only case. Polled cases require zero drops and exact independent TX-pin bytes.',
         'manual':{'path':'C/C5/perip/uart16550/doc/UART_spec.pdf','sha256':sha(ROOT/'C/C5/perip/uart16550/doc/UART_spec.pdf'),'PDF_pages':[8,12,14,15,17,18]},
         'scope':'Original hello with multiple argument lengths traverses real AXI4/APB/UART FIFO. Attempt/accept/drop counters observe original FIFO branches without changing functional assignments. Divisor written MSB then LSB,8N1 restored; actual register readback and TEMT drain tested. Polled output includes all256 byte values and multiple lengths, independently decoded from the real TX pin. A wrong sampling period is rejected. Verilator debug %c output omits NUL; serial data preserves it. NVBoard UI acceptance is separate and still pending.'})
    mark(['C5-M011','C5-M012','C5-M013','C5-M014'],'PASS',['reports/C5_uart.json'],'Actual original hello length experiments, FIFO saturation evidence, manual-based divisor/readback and complete polled output including binary bytes.')
    print('C5_UART_LOSS_EXPLAINED_AND_POLLED_OUTPUT_PASS',flush=True)


if __name__=='__main__':main()
