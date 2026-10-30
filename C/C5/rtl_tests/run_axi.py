from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'runtime'))
from common import *


def main():
    folder=ROOT/'C/C5';subprocess.run(['python3',str(folder/'rtl_tests/make_axi_tb.py')],check=True)
    out=WORK/'c5/axi-unit';out.mkdir(parents=True,exist_ok=True)
    cpu=folder/'rtl/ysyx_00000000.v';test=folder/'rtl_tests/axi4_cpu_tb.sv'
    sources=[*sorted((folder/'rtl').glob('*.sv')),cpu,test]
    exe=out/'good/sim'
    def build(name,files):
        target=out/name;target.mkdir(exist_ok=True)
        run('C5/axi-unit/'+name+'/build',[VERILATOR,'--binary','--timing','--assert','-j','1','-Wno-fatal','-DSYNTHESIS=1','-DC5_CORE_DELAYS=7','--top-module','axi4_cpu_tb','--Mdir',target,'-o','sim',*files],inputs=files,outputs=[target/'sim'],timeout=180)
        return target/'sim'
    exe=build('good',sources);rows=[]
    for scenario in range(7):
        stdout,stderr,record=run('C5/axi-unit/scenario'+str(scenario),[exe,'+SCENARIO='+str(scenario)],inputs=[exe],timeout=10)
        marker='AXI4_CPU_PROTOCOL_REJECT_PASS' if scenario in [3,4,5] else 'AXI4_CPU_PROTOCOL_PASS';assert marker in stdout
        rows.append({'scenario':scenario,'status':'PASS','stdout':stdout,'evidence':record['name']})
    text=cpu.read_text();assert 'io_master_wlast=!w_done;' in text
    bad=out/'bad-wlast.v';bad.write_text(text.replace('io_master_wlast=!w_done;','io_master_wlast=0;'))
    exe=build('bad-wlast',[bad if p==cpu else p for p in sources])
    stdout,stderr,record=run('C5/axi-unit/bad-wlast',[exe,'+SCENARIO=0'],inputs=[exe],expected=(1,),timeout=10);assert 'W_FIELDS' in stdout+stderr
    rows.append({'mutation':'master WLAST stuck0','status':'PASS_REJECTED','evidence':record['name']})
    dump(ROOT/'reports/C5_axi_interface.json',{'status':'PASS_FULL_AXI4_INTERFACE_CONTROLS','runs':rows,
         'sources':[{'path':str(p),'sha256':sha(p)} for p in sources],
         'scope':'Finite timed CPU-only bus fixture: all unused slave outputs zero, byte addresses and AxSIZE/WSTRB, AW-first/W-first/simultaneous acceptance, held requests, randomized response readiness, reset with outstanding read; malformed RLAST/RID/BID rejected. Actual master WLAST mutation fails. Full SoC MROM/SRAM tests remain separate.'})
    mark(['C5-M003'],'PASS',['reports/C5_axi_interface.json','reports/C5_boot.json','reports/C5_diff.json'],'Exact public CPU interface, full AXI4 single-beat master, internal CLINT and real SoC path; malformed-response and wrong-master controls.')
    print('C5_AXI4_INTERFACE_PASS',flush=True)


if __name__=='__main__':main()
