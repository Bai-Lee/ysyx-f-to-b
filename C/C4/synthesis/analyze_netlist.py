"""Independent bounded STA of the unchanged mapped ECC netlist."""
from pathlib import Path
import sys,re,json,gzip,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'runtime'))
from common import *
from resource_policy import POLICY_PATH, load_policy, generation_environment

def main():
    p=argparse.ArgumentParser();p.add_argument('name',choices=['single','axi']);a=p.parse_args()
    root=WORK/'c4/synthesis'/a.name/'runs/baseline/Synthesis_yosys';inputs=json.loads((ROOT/'reports/C4_synthesis_inputs.json').read_text());variant=next(r for r in inputs['variants'] if r['name']==a.name)
    design='c4_'+a.name;net=root/'output'/(design+'_Synthesis.v.gz');assert net.exists()
    stat=json.loads((root/'feature/Synthesis_stat.json').read_text());module=stat['modules']['\\'+variant['top']]
    assert module['num_memories']==0 and module['num_processes']==0 and not any(k.startswith('$') for k in module['num_cells_by_type'])
    ff=sum(v for k,v in module['num_cells_by_type'].items() if k.startswith('DFF'))
    memcounts={}
    if a.name=='single':
        inventory=(root/'report/Synthesis_stat.json').read_text().splitlines()
        memcounts={kind:sum(line.startswith('single_with_memories/'+kind+'[') for line in inventory) for kind in ('imem','dmem')}
        assert memcounts=={'imem':8192,'dmem':8192} and ff>=16384,(ff,memcounts)
    tool=json.loads((ROOT/'reports/C4_opensta_toolchain.json').read_text());exe=Path(tool['binary']);assert sha(exe)==tool['sha256']
    out=ROOT/'C/C4/synthesis'/a.name;out.mkdir(exist_ok=True);flat=out/'mapped.v';flat.write_bytes(gzip.decompress(net.read_bytes()))
    sdc=out/'model.sdc';sdc.write_text('''create_clock -name clk -period 10.0 [get_ports clock]
set_clock_transition 0.1 [get_clocks clk]
set data_inputs {}
foreach p [all_inputs] {if {[get_full_name $p] ne "clock"} {lappend data_inputs $p}}
set_input_delay -clock clk -max 1.0 $data_inputs
set_input_delay -clock clk -min 0.1 $data_inputs
set_input_transition 0.1 $data_inputs
set_output_delay -clock clk -max 1.0 [all_outputs]
set_output_delay -clock clk -min 0.0 [all_outputs]
set_load 0.005 [all_outputs]
''')
    libraries=[Path(r['path']) for r in inputs['libraries']]
    script=out/'analysis.tcl';script.write_text('if {[catch {\n'+''.join('read_liberty {'+str(x)+'}\n' for x in libraries)+'read_verilog {'+str(flat)+'}\nlink_design '+variant['top']+'\nread_sdc {'+str(sdc)+'}\ncheck_setup -verbose\nputs "C4_SETUP_BEGIN"\nreport_checks -path_delay max -group_count 1 -endpoint_count 1 -digits 6\nreport_worst_slack -digits 6\nputs "C4_SETUP_END"\nputs "C4_HOLD_BEGIN"\nreport_checks -path_delay min -group_count 1 -endpoint_count 1 -digits 6\nputs "C4_HOLD_END"\nputs "C4_STA_COMPLETE"\n} message]} {puts stderr "C4_STA_ERROR $message"; exit 1}\nexit\n')
    guard=ROOT/'C/C4/synthesis/budget_exec.py';budget=ROOT/'artifacts/C4/opensta'/a.name/'budget.json'
    o,e,r=run('C4/opensta/'+a.name,['python3',guard,'--metric','pss','--report',budget,'--','taskset','-c','0,1',exe,'-exit',script],inputs=[POLICY_PATH,ROOT/'C/runtime/budget_exec.py',ROOT/'C/runtime/resource_policy.py',guard,exe,script,sdc,flat,*libraries],timeout=600)
    assert 'C4_STA_COMPLETE' in o and 'C4_STA_ERROR' not in o+e and 'Error:' not in o+e
    setup=float(re.search(r'worst slack\s+(-?[\d.]+)',o)[1]);holdtext=o.split('C4_HOLD_BEGIN',1)[1].split('C4_HOLD_END',1)[0]
    holds=[float(v) for v in re.findall(r'(-?[\d.]+)\s+slack\s+\((?:MET|VIOLATED)\)',holdtext)];assert holds
    hold=min(holds);period_est=10-setup;assert period_est>0
    (out/'analysis.txt').write_text(o+e)
    for file in [net,root/'output'/(design+'_Synthesis_sim.v.gz'),root/'feature/Synthesis_stat.json',root/'report/Synthesis_check.rpt',root/'log/Synthesis.log']:
        shutil.copyfile(file,out/file.name)
    row={'name':a.name,'status':'PASS_MAPPED_STRUCTURE_AND_STA','top':variant['top'],'rtl_sha256':variant['source_sha256'],'netlist_sha256':sha(net),'cell_area_um2':module['area'],'mapped_cells':module['num_cells'],'DFF_count':ff,'memory_DFF_origin_counts':memcounts,'clock_constraint_mhz':100,'setup_wns_ns':setup,'hold_min_slack_ns':hold,'setup_frequency_estimate_mhz':1000/period_est,'timing_met_at_100MHz':setup>=0 and hold>=0,'sdc_sha256':sha(sdc),'libraries':inputs['libraries'],'opensta_binary_sha256':sha(exe),'budget':json.loads(budget.read_text()),'evidence':'artifacts/C4/opensta/'+a.name,'scope':'Same unchanged ECC/Yosys mapped netlist; independent OpenSTA after ECC integrated STA exceeded PSS budget. Explicit IO model: input max1/min0.1ns, output max1/min0ns,100ps transitions,5fF load; no routed parasitics. Frequency is setup-based estimate under this model, not a newly qualified clock or silicon signoff.'}
    report=ROOT/'reports/C4_mapped_timing.json';prior=json.loads(report.read_text()).get('variants',[]) if report.exists() else []
    rows=[x for x in prior if x['name']!=a.name]+[row];dump(report,{'status':'PASS_SELECTED_VARIANTS','variants':rows})
    print('C4_MAPPED_STA_PASS',a.name,ff,module['area'],setup,hold,flush=True)
if __name__=='__main__':main()
