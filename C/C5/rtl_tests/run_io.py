from pathlib import Path
import sys,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'runtime'))
from common import *
iverilog=Path('/home/USER/tools/e-stage/oss-20261022/oss-cad-suite/bin/iverilog');vvp=iverilog.parent/'vvp'
base=ROOT/'C/C5';out=WORK/'c5/io-units';out.mkdir(parents=True,exist_ok=True);rows=[]
parser=argparse.ArgumentParser();parser.add_argument('--peripheral',choices=['all','gpio','ps2','vga'],default='all');args=parser.parse_args()
cases=[('gpio','good',None,'GPIO_APB_PASS'),('gpio','bad-segment',("0:segments=8'hc0","0:segments=8'hc1"),'GPIO_SEGMENTS'),
       ('ps2','good',None,'PS2_APB_PASS'),('ps2','bad-parity',('&&(^frame[9:1])','&&1\'b1'),'PS2_FIFO_DATA'),
       ('vga','good',None,'VGA_FULL_FRAME_PASS'),('vga','bad-colors',('assign vga_r=pixel[23:16]','assign vga_r=pixel[15:8]'),'VGA_PIXEL_DATA')]
for peripheral,name,mutation,marker in cases:
    if args.peripheral!='all' and peripheral!=args.peripheral:continue
    implementation=base/'perip'/peripheral/(peripheral+'_top_apb.v');canonical=implementation
    if mutation:
        text=implementation.read_text();assert text.count(mutation[0])==1;implementation=out/(peripheral+'-'+name+'.v');implementation.write_text(text.replace(*mutation))
    sources=[implementation,base/'rtl_tests'/(peripheral+'_tb.sv')];image=out/(peripheral+'-'+name+'.vvp');tag='C5/io-units/'+peripheral+'-'+name
    run(tag+'/compile',[iverilog,'-g2012','-s',peripheral+'_tb','-o',image,*sources],inputs=sources,outputs=[image],timeout=60)
    text,err,record=run(tag+'/run',[vvp,image],inputs=[image],expected=(1 if mutation else 0,),timeout=90);assert marker in text+err
    rows.append({'peripheral':peripheral,'name':name,'status':'PASS','expected_exit':1 if mutation else 0,'stdout':text,'evidence':'artifacts/'+tag,'implementation_sha256':sha(implementation),'canonical_sha256':sha(canonical)})
report=ROOT/'reports/C5_io_units.json';prior=json.loads(report.read_text()).get('runs',[]) if report.exists() else []
keys={(r['peripheral'],r['name']) for r in rows};rows=[r for r in prior if (r['peripheral'],r['name']) not in keys]+rows
complete=len({(r['peripheral'],r['name']) for r in rows})==len(cases)
dump(report,{'status':'PASS' if complete else 'PASS_COMPLETED_SUBSET','runs':rows,'scope':'GPIO16 walking LEDs, byte masks,16hex patterns on8digits,65536 input patterns; PS2 all256bytes, oddparity/stop/timeout rejection, FIFOoverflow; VGA307200independent pattern pixels scored overone800x525pin frame, masks/bounds/warmreset. Segment/parity/color mutants rejected. This is not NVBoard GUI or CPU application acceptance and does not verify physical metastability/pixel-clock timing.'})
print('C5_IO_UNITS_PASS',flush=True)
