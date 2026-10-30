from pathlib import Path
import sys,zipfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *


def main():
    builds=json.loads((ROOT/'reports/C5_soc_build.json').read_text())['variants']
    profiles={cycle:next(r for r in builds if r['reset_pc']==0x20000000 and not r.get('mutant',False) and not r.get('fast_flash',False) and r.get('cycle_sim',False)==cycle) for cycle in [False,True]}
    fixtures=WORK/'c5/profile-fixtures';fixtures.mkdir(parents=True,exist_ok=True)
    ref=WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so';flash=WORK/'c5/images/pattern16m.bin'
    cases=[('ebreak','C5/boot/first-ebreak/compile','C5/boot/first-ebreak/extract',False),
           ('sram-patterns','C5/ram/mem-test/build','C5/ram/mem-test/build',False),
           ('boot-poison','C5/ram/boot-data/build','C5/ram/boot-data/build',False),
           ('uart512','C5/uart/binary-512/build','C5/uart/binary-512/build',True),
           ('spi-bitrev','C5/spi/bitrev/build','C5/spi/bitrev/build',False),
           ('serial-flash','C5/spi/serial-data/build','C5/spi/serial-data/build',False),
           ('xip-data','C5/spi/fast-data/build','C5/spi/fast-data/build',False)]
    rows=[]
    for name,_,source,pins in cases:
        with zipfile.ZipFile(ROOT/'artifacts'/source/'output_snapshot.zip') as z:
            member=next(n for n in z.namelist() if n.endswith('.bin'));image=fixtures/(name+'.bin');image.write_bytes(z.read(member))
        results=[]
        for cycle in [False,True]:
            b=profiles[cycle];exe=Path(b['executable']);assert sha(exe)==b['sha256'];tag='C5/cycle-profile/'+name+('-cycle' if cycle else '-timed')
            directory=ROOT/'artifacts'/tag;directory.mkdir(parents=True,exist_ok=True);report=directory/'simulation.json'
            options=['--uart-bit-cycles','16'] if pins else []
            run(tag,[exe,'--mrom',image,'--flash',flash,'--ref',ref,'--report',report,'--max-cycles','10000000',*options],inputs=[exe,image,flash,ref],outputs=[report],timeout=120)
            data=json.loads(report.read_text());assert data['result']=='GOOD_TRAP' and data['diff_enabled']
            results.append(data)
        timed,cycle=results
        for key in ['instructions','pc','next_pc','gpr','axi_channels','diff_checked','device_sync_checked','uart','uart_pin','retired_by_region']:
            assert timed[key]==cycle[key],(name,key,timed[key],cycle[key])
        for key in ['transfers','sampled_bits','incomplete_bits']:assert timed['spi'][key]==cycle['spi'][key]
        assert [(p['select'],p['bits'],p['tx_low64'],p['rx_low64']) for p in timed['spi']['packets']]==[(p['select'],p['bits'],p['tx_low64'],p['rx_low64']) for p in cycle['spi']['packets']]
        rows.append({'name':name,'status':'PASS_EQUIVALENT_OBSERVATIONS','timed':timed,'cycle':cycle,'wall_speed_ratio':timed['wall_seconds']/cycle['wall_seconds'],'image_sha256':sha(image)})
        dump(ROOT/'reports/C5_cycle_profile.json',{'status':'IN_PROGRESS','runs':rows})
    dump(ROOT/'reports/C5_cycle_profile.json',{'status':'PASS_FUNCTIONAL_CYCLE_PROFILE','runs':rows,
         'scope':'Same RTL and program bytes under timed simulation and cycle simulation that omits vendor #1 delays. Actual architecture, memory operations, UART TX-pin bytes and SPI sampled streams compared. This profile does not establish analog setup/hold timing; the timed baseline remains preserved.'})
    print('C5_FUNCTIONAL_CYCLE_PROFILE_ACCEPTED',flush=True)


if __name__=='__main__':main()
