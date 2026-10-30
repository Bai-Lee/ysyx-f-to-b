"""Compare installed simulators/model branches without changing the benchmark or checks."""
from pathlib import Path
import sys,resource
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
 resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024));resource.setrlimit(resource.RLIMIT_CPU,(60,65))
 p=ROOT/'E/E8';dest=WORK/'build/E8/profile';dest.mkdir(parents=True,exist_ok=True)
 cpp=dest/'vpi_memory.cpp';cpp.write_text((p/'vpi_memory.cpp').read_text().replace('#include "memory_model.hpp"','#include "profile_memory.hpp"').replace('GateMemory','ProfileMemory').replace('memory->load(image);','memory->open_profile(report+".progress.tsv");memory->load(image);'))
 models=[Path('/home/USER/tools/icsprout55-e-stage/IP/STD_cell/ics55_LLSC_H7C_V1p10C100/ics55_LLSC_H7C'+v+'/verilog/ics55_LLSC_H7C'+v+'.v') for v in ['R','L']]
 rows=[]
 for version in ['11','14']:
  root=Path('/usr/bin') if version=='11' else Path('/home/USER/tools/e-stage/oss-20261022/oss-cad-suite/bin')
  wd=dest/version;wd.mkdir(exist_ok=True)
  run('E8/profile/'+version+'/vpi_build',[root/'iverilog-vpi','--name=vpi_memory','-O3','-I'+str(p),'-I'+str(ROOT/'E/runtime'),cpp],cwd=wd,inputs=[cpp,p/'profile_memory.hpp',p/'memory_model.hpp',ROOT/'E/runtime/memory.hpp'],timeout=90)
  for model in ['udp','behavioral']:
   vvp=wd/(model+'.vvp');flags=[] if model=='udp' else ['-D__VERILATOR__']
   run('E8/profile/'+version+'/'+model+'/compile',[root/'iverilog','-g2012','-Dfunctional',*flags,'-s','iverilog_top','-o',vvp,p/'netlists/baseline.v',*models,p/'gate_system.sv',p/'iverilog_top.sv'],inputs=[p/'netlists/baseline.v',*models,p/'gate_system.sv',p/'iverilog_top.sv'],timeout=90)
   item=json.loads((ROOT/'reports/E8_software.json').read_text())['programs'][0];image=Path(item['image']);assert item['name']=='hello'
   out=ROOT/'artifacts/E8/profile'/version/model/'hello/result.json'
   _,_,r=run('E8/profile/'+version+'/'+model+'/hello',[root/'vvp','-M'+str(wd),'-mvpi_memory',vvp,'+image='+str(image),'+report='+str(out),'+max_cycles=100000'],inputs=[root/'vvp',vvp,wd/'vpi_memory.vpi',image],outputs=[out,Path(str(out)+'.progress.tsv')],timeout=90)
   d=json.loads(out.read_text());assert d['result']=='GOOD_TRAP'
   rows.append({'version':version,'model':model,'result':d,'elapsed_seconds':r['elapsed_seconds'],'vvp':str(vvp),'plugin':str(wd/'vpi_memory.vpi')});dump(ROOT/'reports/E8_profile.json',{'status':'IN_PROGRESS','rows':rows})
 dump(ROOT/'reports/E8_profile.json',{'status':'PASS_PROFILE_ONLY','rows':rows,'scope':'AllvariantsuseunchangedofficialPDKsource. SelectingbehavioralFFbranchforfour-statequalificationrequiresseparateequivalenceevidenceundermappeddesignclock/resetassumptions.'})
if __name__=='__main__':main()
