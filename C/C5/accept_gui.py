from pathlib import Path
import sys,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
p=argparse.ArgumentParser();p.add_argument('case',choices=['gpio','keyboard','video','typing','fceux','rtthread','rtbench','rtguard']);p.add_argument('--note',required=True);args=p.parse_args()
path=ROOT/('reports/C5_gui_'+args.case+'.json');record=json.loads(path.read_text());assert record['status'] in ['PASS_PENDING_VISUAL_REVIEW','PASS']
for capture in record['screenshots']:assert sha(ROOT/capture['path'])==capture['sha256']
record['visual_review']={'reviewer':'Codex inspection of actual native-window captures','observed':args.note,'screenshots':record['screenshots']};record['status']='PASS'
dump(path,record);dump(ROOT/'artifacts/C5/gui'/args.case/'session/visual_review.json',record['visual_review'])
ids={'gpio':['C5-M036','C5-M037','C5-M038','C5-M039'],'keyboard':['C5-M040','C5-M042'],'video':['C5-M044'],'rtthread':['C5-M041','C5-M046']}.get(args.case,[])
if ids:mark(ids,'PASS',[str(path.relative_to(ROOT))],record['scope']+' Visual review: '+args.note)
if args.case in ['typing','fceux']:
    reports=[ROOT/('reports/C5_gui_'+case+'.json') for case in ['typing','fceux']]
    if all(report.exists() and json.loads(report.read_text())['status']=='PASS' for report in reports):
        mark(['C5-M045'],'PASS',[str(report.relative_to(ROOT)) for report in reports],'RealNVBoard typing-game hit andFCEUX CC0ROM controller changes through actualPS2/VGA pins; nativecaptures inspected and bothgames exit through their Escape paths.')
print('C5_GUI_VISUALLY_ACCEPTED',args.case,flush=True)
