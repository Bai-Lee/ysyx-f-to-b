from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
files=[ROOT/'reports'/name for name in ['E4_units.json','E4_gui.json','E4_visual_check.json','E4_REPORT.md','E4_TASKS.md','C5_io_units.json','C5_gpu_driver.json']]
for path in files:
    if path.suffix=='.json':assert json.loads(path.read_text())['status']==('PASS_NATIVE_LOGIC_AND_NEGATIVE' if path.name=='C5_gpu_driver.json' else 'PASS')
source=ARCHIVE/'references/markdown/8eb56251b0d9d092.md';assert '25MHz' in source.read_text() and '弹性碰撞' in source.read_text()
gui=json.loads((ROOT/'reports/E4_gui.json').read_text());visual=json.loads((ROOT/'reports/E4_visual_check.json').read_text())
screens=[];expected_names={'vga_static','vga_moving_1','vga_moving_2'}
for entry in gui['screens']:
    if entry['name'] in expected_names:
        path=ROOT/entry['path'];digest=sha(path)
        visual_entry=next(row for row in visual['results'] if row['name']==entry['name'])
        assert digest==visual_entry['image_sha256']
        screens.append({'name':entry['name'],'path':str(path.relative_to(ROOT)),'sha256':digest})
assert {screen['name'] for screen in screens}==expected_names
unit=next(row for row in json.loads((ROOT/'reports/E4_units.json').read_text())['runs'] if row['top']=='vga')
assert unit['run']['status']=='PASS' and 'static_frames=2 moving_frames=3' in unit['result']
dump(ROOT/'reports/C5_vga_prerequisite.json',{'status':'PASS_REUSED_E4_AND_CURRENT_C5','source':{'path':str(source),'sha256':sha(source)},'evidence':[{'path':str(path.relative_to(ROOT)),'sha256':sha(path)} for path in files],'historical_screens':screens,'timing':{'horizontal':[96,48,640,16],'vertical':[2,33,480,10],'pixel_clocks_per_frame':420000,'E4_ideal_pixel_clock_hz':25000000,'E4_ideal_refresh_hz':25000000/420000},'scope':'NJU08 prerequisite already completedinE4: staticimage/MIF andmovingbouncingimage plusindependentpixel checks. Historicalresultsare reused, not claimedrerun. C5 newlycheckscompleteRGBpinframes andsoftwareclipping. C5NVBoardtakesonesamplepersimclock, soits100MHzclockdoesnotassertphysical60Hzdisplaytiming orADV7123/FPGAboardacceptance.'})
mark(['C5-M043'],'PASS',['reports/C5_vga_prerequisite.json','reports/E4_units.json','reports/E4_gui.json','reports/E4_visual_check.json','reports/C5_io_units.json'],'ReusedcompletedNJU08 static/MIF/elastic-motion engineeringwithrecordedhashes; C5 timing/blanking explanation andnewwhole-framepin/driverchecks. No physicalFPGAclaim.')
print('C5_VGA_PREREQUISITE_REVIEW_PASS',flush=True)
