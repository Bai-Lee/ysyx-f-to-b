from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from ecc_rpc import Rpc
def main():
 jobs=[('light_preflight','light',WORK/'backend/light/runs/yosys_august/Synthesis_yosys/output/light_Synthesis.v.gz',100,.3),('cpu_area','ysyx_00000000',ROOT/'E/E7/synthesis/area/e7_minirv_Synthesis.v.gz',50,.3),('cpu_baseline','ysyx_00000000',ROOT/'E/E7/synthesis/baseline/e7_minirv_Synthesis.v.gz',50,.3)];rows=[]
 with Rpc('E8/rpc/prepare_physical') as rpc:
  for name,top,net,hz,util in jobs:
   directory=WORK/'physical'/name
   if directory.exists():opened=rpc.call('workspace.open',{'directory':str(directory)})
   else:
    opened=rpc.call('workspace.create',{'directory':str(directory),'pdk':'ics55','pdkRoot':'/home/USER/tools/icsprout55-e-stage','originVerilog':str(net),'parameters':{'Design':name,'Top module':top,'Clock':'clock','Frequency max [MHz]':hz,'Core':{'Utilitization':util,'Margin':[2,2],'Aspect ratio':1},'Target density':.2,'STA max paths':1000},'flowConfig':{'start_step':'Floorplan','end_step':'Harden'}},timeout=90)
   rows.append({'name':name,'directory':str(directory),'netlist':str(net),'netlist_sha256':sha(net),'target_frequency_mhz':hz,'core_utilization':util,'status':'CONFIGURED_NOT_RUN','workspace':opened})
 dump(ROOT/'reports/E8_physical_workspaces.json',{'status':'CONFIGURED_NOT_RUN','workspaces':rows,'policy':'SameofficialECOS/ECCbackendworkspace API; startsfromalreadyverifiedmappednetlist. Noqualitygateoverrides. MainCPUphysicalflowwillrunafterbackendpreflight; targets/utilizationmayberevisedbasedonrealSTA/DRC/LVS results withseparatehistory.'})
 print('PHYSICAL_WORKSPACES_CREATED_NOT_RUN',flush=True)
if __name__=='__main__':main()
