from common import *
import re,gzip
def pins(lefs):
 out={}
 for path in lefs:
  text=Path(path).read_text()
  for name,body in re.findall(r'^MACRO\s+(\S+)\s*\n(.*?)^END\s+\1\s*$',text,re.M|re.S):out[name]=set(re.findall(r'^\s*PIN\s+(\S+)',body,re.M))
 return out
def check_ports(text,cells):
 errors=[];count=0
 for kind,inst,body in re.findall(r'\b(\w+)\s+(\\\S+|\w+)\s*\((.*?)\);',text,re.S):
  if kind not in cells:continue
  count+=1
  for port in re.findall(r'\.(\w+)\s*\(',body):
   if port not in cells[kind]:errors.append({'cell':kind,'instance':inst,'bad_port':port})
 assert count>0
 return count,errors
def main():
 p=ROOT/'reports/E_backend_compatible_tools.json';r=json.loads(p.read_text());base=Path(r['project']);pdk=Path('/home/USER/tools/icsprout55-e-stage')
 lefs=list(pdk.glob('IP/STD_cell/ics55_LLSC_H7C_V1p10C100/*/lef/*_ecos.lef'));cellpins=pins(lefs)
 net=base/'Synthesis_yosys/output/light_Synthesis.v.gz';text=gzip.decompress(net.read_bytes()).decode();count,errors=check_ports(text,cellpins);assert not errors,errors
 qor=json.loads((base/'Synthesis_yosys/feature/post_synthesis/qor_summary.json').read_text());assert qor['summary']['setup']['frequency_mhz']>0 and qor['summary']['setup']['nvp']==0
 bad=re.sub(r'\.(\w+)\s*\(','.INTENTIONALLY_INVALID_PORT(',text,count=1);_,baderrors=check_ports(bad,cellpins);assert baderrors
 old=WORK/'backend/light/runs/baseline/Synthesis_yosys/output/light_Synthesis.v.gz';oldcnt,olderrors=check_ports(gzip.decompress(old.read_bytes()).decode(),cellpins);assert olderrors
 r.update(status='PASS_SYNTHESIS_STA_ONLY',mapped_instances=count,pin_errors=errors,negative_control_detected=baderrors,failed_newer_yosys_port_errors=olderrors,netlist_sha256=sha(net),qor=qor,scope='syn_sta positive run only. Overall ECC signoff checklist correctly remains blocked for unrequested physical steps; no route/DRC/LVS claim.')
 dump(p,r)
 dest=ROOT/'artifacts/E/backend/compatible_outputs';dest.mkdir(parents=True,exist_ok=True)
 for file in [net,base/'Synthesis_yosys/feature/post_synthesis/qor_summary.json',base/'Synthesis_yosys/report/Synthesis_check.rpt',base/'home/checklist.json']:shutil.copyfile(file,dest/file.name)
 print('BACKEND_SYNTHESIS_STA_AUDIT_PASS',count,flush=True)
if __name__=='__main__':main()
