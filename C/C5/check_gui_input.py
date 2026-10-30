from pathlib import Path
import sys,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from gui_verify import Session,disable_private_repeat,target
from support import select_build
VARIANT='30000000-cycle-psram4m-qpi-sdram32x2-opt-gui-ps2log'


def child():
    job=target('gpio');exe=Path(select_build(VARIANT)['executable']);folder=ROOT/'artifacts/C5/gui-input-control/session';report=folder/'simulation.json';budget=folder/'resources.json'
    command=['python3',ROOT/'C/runtime/budget_exec.py','--report',budget,'--',exe,'--gui','--flash',job['image'],'--ref',WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so','--report',report,'--max-cycles','100000000']
    s=Session(exe,'',folder,title='^NVBoard',command=command,cwd=WORK/'c5',env_extra={'NVBOARD_HOME':str(WORK/'c5/nvboard')})
    try:
        control=disable_private_repeat(s.env)
        s.key('keydown','j');time.sleep(2);s.key('keyup','j');time.sleep(.4)
        session=s.finish();data=json.loads(report.read_text());codes=[code for _,code in data['pins']['ps2_scans']]
        assert codes==[0x3b,0xf0,0x3b],codes
        assert data['ps2_queue']=={'accepted':3,'dropped':0,'invalid':0,'popped':0,'maximum_occupancy':3},data['ps2_queue']
        dump(ROOT/'reports/C5_gui_input_control.json',{'status':'PASS','control':control,'session':session,'pin_scan_codes':codes,'ps2_queue':data['ps2_queue'],'evidence':'artifacts/C5/gui-input-control','scope':'ActualNVBoard,2secondheldJ, exactonePS2makeandonebreak, noFIFOloss. NativeXvfbkeyboardrepeatquerieddisabledafterSDLinitialization; no userdisplaysettingchanged.'})
        print('C5_GUI_SINGLE_MAKE_BREAK_PASS',flush=True)
    finally:
        if s.proc.poll() is None:s.cleanup()
        if not s.out.closed:s.out.close()
        if not s.err.closed:s.err.close()


if __name__=='__main__':
    if '--child' in sys.argv:child()
    else:run('C5/gui-input-control/launch',['xvfb-run','-a','-s','-screen 0 1600x1200x24 -nolisten tcp -r','env','C_PRIVATE_XVFB=1','python3',Path(__file__),'--child'],inputs=[Path(__file__),ROOT/'C/C5/gui_verify.py'],outputs=[ROOT/'reports/C5_gui_input_control.json'],timeout=120)
