from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
 review=json.loads((ROOT/'reports/E8_visual_review.json').read_text());assert review['status']=='PASS'
 for row in review['images']:assert sha(ROOT/row['path'])==row['sha256'],row['path']
 gui=ROOT/'artifacts/E8/gui';native=json.loads((gui/'native-viewer.json').read_text());assert native['environment']['ECOS_GPU_CANVAS']=='0' and '--mode' in native['command'] and 'view' in native['command']
 assert json.loads((gui/'session-end.json').read_text())['exit_code']==0
 assert json.loads((ROOT/'reports/E8_signoff_export.json').read_text())['status']=='PASS'
 dump(ROOT/'reports/E8_gui.json',{'status':'PASS','review':'reports/E8_visual_review.json','images':review['images'],'native_viewer':native,'geometry_manifest_sha256':sha(WORK/'physical/cpu_baseline/filler_ecc/output/geometry/geometry.manifest'),'interaction_log':'artifacts/E8/gui/interactions.json','application_version':'ECOS Studio0.1.0-alpha.9','scope':'RealECOSdashboard/checklistandnative2Dread-onlyview;CPUcanvasflagisprovidedbytheupstreamsource. OptionalembeddedAIagentand3Dviewnotselected. NoLogisimcomputeruse.'})
 print('ACTUAL_ECOS_GUI_AND_NATIVE_2D_VISUAL_ACCEPTANCE_PASS',flush=True)
if __name__=='__main__':main()
