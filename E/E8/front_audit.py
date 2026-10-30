from pathlib import Path
import sys,re,gzip,resource
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
 resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024));resource.setrlimit(resource.RLIMIT_CPU,(30,35))
 sources=[ROOT/'E/E5/rtl/minirv_decode.sv',ROOT/'E/E5/rtl/minirv_regfile.sv',ROOT/'E/E7/rtl/minirv_bus.sv',ROOT/'E/E7/rtl/ysyx_00000000.sv'];combined='\n'.join(f.read_text() for f in sources);gold=(ROOT/'E/E7/synthesis/baseline/cpu.v').read_text();assert combined==gold,'Synthesis input differs from current RTL'
 run('E8/final_front/lint',[VERILATOR,'--lint-only','--top-module','ysyx_00000000','-DSYNTHESIS','-Wall','-Wno-DECLFILENAME',*sources],inputs=sources)
 positive_edges=0
 for file in sources:
  text=file.read_text();text=re.sub(r'/\*.*?\*/|//[^\n]*','',text,flags=re.S)
  assert not re.search(r'\bnegedge\b',text),str(file)
  positive_edges+=len(re.findall(r'\bposedge\s+clock\b',text))
 net=(ROOT/'E/E8/netlists/baseline.v').read_text();assert not re.search(r'\bLAT\w*\s+\S+\s*\(',net)
 flops=re.findall(r'DFFQX0P5H7R\s+\S+\s*\((.*?)\);',net,re.S);assert len(flops)==611 and all(re.findall(r'\.CK\(([^)]+)\)',x)==['clock'] for x in flops)
 evidence=['E8_address_reset','E8_rtl_icarus','E8_rtl_verilator','E8_vpi_preflight','E8_two_state_control','E7_bus_tests','E7_bus_negative','E7_csr_tests','E7_gpio_unit']
 for name in evidence:assert json.loads((ROOT/'reports'/(name+'.json')).read_text())['status'].startswith('PASS'),name
 output={'status':'PASS','rtl_files':[{'path':str(f.relative_to(ROOT)),'sha256':sha(f)} for f in sources],'synthesis_rtl_matches_current':True,'combined_sha256':hashlib.sha256(combined.encode()).hexdigest(),'posedge_clock_blocks':positive_edges,'negedge_blocks':0,'mapped_latches':0,'mapped_DFFQX0P5H7R_instances':len(flops),'all_mapped_flop_clocks':'clock','strict_lint':'-Wall; onlyDECLFILENAMEexempted. No-Wno-fatal. unused_*signalsareexplicitnameddebugoutputsremovedfromphysicaltop.','evidence':evidence,'boundary':'Staticstructureplusactualreportedregressions; notformalallinputproof. FinalnetlistIcarus/fullphysicalcompletionauditedseparately.'};dump(ROOT/'reports/E8_front_audit.json',output)
 mark(['E8-M001','E8-M002','E8-M003','E8-M004','E8-M005','E8-M006','E8-M009'],'PASS',['reports/E8_front_audit.json','reports/E8_address_reset.json','reports/E8_rtl_icarus.json','reports/E8_two_state_control.json','artifacts/E8/final_front'],'CurrentRTLhashmatchesactualsynthesisinput; fulladdressboundarytests+clippingnegative;posedgeonly/611DFFsingleclock/noLAT;strictlintandcompleteRTLmicrobench4statepass;missingreset/Xargument/invalidexitnegativesretained. Laterchangeswerebuild/hostUIonly, notDUTRTL.')
 mark(['E8-O001','E8-O002','E8-O003','E8-O004'],'NOT_APPLICABLE',['E/E8/NOTES.md','reports/E8_front_audit.json'],'TheseareChisel-specificbackgroundnotes;thisprojectuseshandwrittenSystemVerilog. Equivalentgeneralrequirementsareactuallychecked.')
 mark(['E8-R001'],'PASS_DOCUMENTED',['reports/E_backend_assets.json','reports/E8_mapped_preflight.json','E/E8/NOTES.md'],'Lockedv1.10.100modelsincludeofficialVerilatorcompatibilitybranch;physical/functionalmodelhashesrecorded. FinalIcarususesoriginalUDPbranch.')
 mark(['E8-O005'],'NOT_SELECTED_OPTIONAL',['E/E8/NOTES.md'],'Optionalmaximumutilizationsearchnotselected;objectiveisonefullycheckedphysicalcandidate. Nooptimalityclaim.')
 print('CURRENT_RTL_STRUCTURE_AND_REGRESSION_AUDIT_PASS',flush=True)
if __name__=='__main__':main()
