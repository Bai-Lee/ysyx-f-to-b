"""Buffered standard-cell mapping and explicit pre-layout timing models."""
from pathlib import Path
import sys,argparse,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--name',default='b3-uncached');parser.add_argument('--component',choices=['cpu','adder','regfile'],default='cpu');parser.add_argument('--mapping-target-ps',type=int,default=200)
    parser.add_argument('--cache-lines',type=int,default=0);parser.add_argument('--cache-words',type=int,default=1);parser.add_argument('--cache-ways',type=int,default=1);parser.add_argument('--cache-burst',action='store_true')
    parser.add_argument('--pipeline',action='store_true');parser.add_argument('--forward',action='store_true');parser.add_argument('--predict',action='store_true');parser.add_argument('--predict-jal',action='store_true');parser.add_argument('--stream-fetch',action='store_true');args=parser.parse_args()
    assert not(args.predict and args.predict_jal)
    assert 100<=args.mapping_target_ps<=10000
    suite=Path('/home/USER/tools/e-stage/oss-20260821/oss-cad-suite');yosys=suite/'bin/yosys'
    sta=Path(json.loads((ROOT/'reports/C4_opensta_toolchain.json').read_text())['binary'])
    lib=ROOT/'B/models/nangate45/lib/Nangate45_typ.lib';liblock=json.loads((ROOT/'reports/B_nangate_course_library.json').read_text())
    assert liblock['status']=='PASS_ALL_USED_LIBRARY_CONTENT_IDENTICAL'
    expected=next(x['sha256'] for x in liblock['files'] if x['path'].replace('\\','/').endswith('/lib/Nangate45_typ.lib'));assert sha(lib)==expected
    label=args.name+'-'+args.component;out=ROOT/'B/B3/synthesis'/label;out.mkdir(parents=True,exist_ok=True)
    if args.component=='cpu':top='ysyx_00000000';files=[*sorted((ROOT/'B/soc/rtl').glob('*.sv')),*sorted((ROOT/'B/soc/rtl').glob('*.v'))]
    else:top='b_adder32' if args.component=='adder' else 'b_regfile16';files=[ROOT/'B/B3/components.sv']
    constr=out/'abc.constr';constr.write_text('set_driving_cell BUF_X4\nset_load 5\n')
    script=out/'synthesis.ys';mapped=out/'mapped.v';structure=out/'mapped.json';statsfile=out/'stat.json'
    defines=f" -DC5_RESET_PC=32'h30000000 -DB_ICACHE_ENABLE={int(args.cache_lines>0)} -DB_ICACHE_LINES={args.cache_lines or 16} -DB_ICACHE_WORDS={args.cache_words} -DB_ICACHE_WAYS={args.cache_ways} -DB_ICACHE_BURST={int(args.cache_burst)} -DB_PIPELINE={int(args.pipeline)} -DB_FORWARD={int(args.forward)} -DB_PREDICT={2 if args.predict_jal else int(args.predict)} -DB_FETCH_PIPELINED={int(args.stream_fetch)} "
    script.write_text('read_liberty -lib '+str(lib)+'\nread_verilog -sv -DSYNTHESIS '+defines+' '.join(map(str,files))+'\nsynth -top '+top+' -flatten\ndfflibmap -liberty '+str(lib)+'\nabc -liberty '+str(lib)+' -constr '+str(constr)+' -D '+str(args.mapping_target_ps)+'\nclean -purge\ncheck -assert\ntee -o '+str(statsfile)+' stat -liberty '+str(lib)+' -json\nwrite_verilog -noattr -noexpr -simple-lhs '+str(mapped)+'\nwrite_json '+str(structure)+'\n')
    env={'PATH':str(suite/'bin')+':'+os.environ['PATH'],'OMP_NUM_THREADS':'1'};guard=ROOT/'B/runtime/budget_exec.py';budget=ROOT/'artifacts/B3/synthesis'/label/'budget.json'
    run('B3/synthesis/'+label,['python3',guard,'--report',budget,'--',yosys,'-s',script],inputs=[yosys,lib,script,constr,*files],outputs=[mapped,structure,statsfile,budget],env=env,timeout=1800,resume=True)
    stats=json.loads(statsfile.read_text())['modules']['\\'+top];module=json.loads(structure.read_text())['modules'][top]
    assert not module.get('memories')
    logic=[c for c in module['cells'].values() if c['type']!='$scopeinfo'];assert all(not c['type'].startswith('$') for c in logic)
    assert not any(c['type'].startswith(('DLH','DLL')) for c in logic)
    sdc=out/'model.sdc'
    sdc.write_text('create_clock -name clk -period 1 [get_ports clock]\nset_clock_transition 0.02 [get_clocks clk]\nset inputs {}\nforeach p [all_inputs] {if {[get_full_name $p] ne "clock"} {lappend inputs $p}}\nset_input_delay -clock clk -max 0.1 $inputs\nset_input_delay -clock clk -min 0.05 $inputs\nset_input_transition 0.02 $inputs\nset_output_delay -clock clk -max 0.1 [all_outputs]\nset_output_delay -clock clk -min 0 [all_outputs]\nset_load 5 [all_outputs]\n')
    analysis=out/'analysis.tcl'
    analysis.write_text('read_liberty {'+str(lib)+'}\nread_verilog {'+str(mapped)+'}\nlink_design '+top+'\nread_sdc {'+str(sdc)+'}\ncheck_setup -verbose\nreport_checks -path_delay max -group_count 3 -digits 6\nreport_worst_slack -digits 6\nputs "HOLD_BEGIN"\nreport_checks -path_delay min -group_count 1 -digits 6\nputs "TRANSITION_BEGIN"\nreport_check_types -max_transition -all_violators -no_line_splits -digits 6\nputs "B_STA_DONE"\nexit\n')
    text,err,_=run('B3/synthesis/'+label+'-sta',[sta,'-exit',analysis],inputs=[sta,lib,mapped,sdc,analysis],timeout=300)
    assert 'Error:' not in text+err and 'B_STA_DONE' in text
    setup=float(re.search(r'worst slack\s+(-?[\d.]+)',text)[1]);hold=float(re.search(r'(-?[\d.]+)\s+slack\s+\((?:MET|VIOLATED)\)',text.split('HOLD_BEGIN',1)[1])[1])
    transition=text.split('TRANSITION_BEGIN',1)[1].count('(VIOLATED)')
    row={'name':label,'status':'PASS_MAPPING_AND_TIMING_ANALYSIS','component':args.component,'top':top,'area_um2':stats['area'],'cells':stats['num_cells'],'flops':sum(c['type'].startswith('DFF') for c in logic),'latches':0,'target_period_ns':1,'mapping_target_ps':200,'setup_slack_ns':setup,'hold_slack_ns':hold,'max_transition_violations':transition,'max_capacitance_check':'NOT_RUN: installed OpenSTA does not support the requested reporting flag','setup_frequency_estimate_mhz':1000/(1-setup),'setup_hold_transition_model_only':hold>=0 and transition==0,'netlist':str(mapped),'netlist_sha256':sha(mapped),'sdc_sha256':sha(sdc),'library_sha256':sha(lib),'evidence':'artifacts/B3/synthesis/'+label,'scope':'Fixed Nangate45 typical cells, ABC buffer/upsize/dnsize, ideal clock, zero routed parasitics, explicit20ps input slew,50..100ps external input delay and5fF output load. Initial zero-minimum input-delay trial had an external hold violation and is preserved. This is synthesis-level model timing and cell area, not physical chip signoff or routed PPA.'}
    row['mapping_target_ps']=args.mapping_target_ps;row['configuration']=vars(args)
    report=ROOT/'reports/B3_synthesis.json';rows=json.loads(report.read_text())['variants'] if report.exists() else [];rows=[r for r in rows if r['name']!=label]+[row];dump(report,{'status':'PASS_COMPLETED_VARIANTS','variants':rows})
    print('B3_SYNTHESIS_RESULT',json.dumps(row),flush=True)

if __name__=='__main__':main()
