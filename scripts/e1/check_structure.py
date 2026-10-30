"""Compile RTL to Yosys process netlists; inspect mandated hierarchy and clocks."""
from common import *
from run import BIN
from collections import Counter
from datetime import datetime,timezone

EXPECTED={
 'module':{'mod_a':1},'module_pos':{'mod_a':1},'module_name':{'mod_a':1},
 'module_shift':{'my_dff':3},'module_shift8':{'my_dff8':3},
 'module_add':{'add16':2},'module_fadd':{'add16':2},'module_cseladd':{'add16':3},'module_addsub':{'add16':2},
 'adder100i':{'bit_adder':100},'bcdadd100':{'bcd_fadd':100},
 'ece241_2014_q7b':{'bcdcount':3},'2014_q4b':{'MUXDFF':4},'fsm_serialdp':{'parity':1}}


def main():
    rows=json.loads((OUT/'jobs.json').read_text('utf8'))['records'];results=[];failed=[]
    for row in rows:
        slug=row['slug'];dut=Path(row['dut']);support=Path(row['syntax_support']);out=ROOT/'artifacts/E1/structure'/slug/'netlist.json';script=ROOT/'temp/E1'/(slug+'_structure.ys')
        script.write_text(f'read_verilog "{dut.as_posix()}" "{support.as_posix()}"\nhierarchy -check -top top_module\nproc\ncheck -assert\nstat\nwrite_json "{out.as_posix()}"\n',encoding='utf8')
        execution=run('E1/structure/'+slug,[BIN/'yosys.exe','-Q','-T','-s',script],[dut,support,script],timeout=60)
        record={'slug':slug,'id':row['id'],'status':execution['status'],'execution':execution}
        if execution['status']=='PASS':
            net=json.loads(out.read_text('utf8'));modules=net['modules'];top=modules['top_module'];types=Counter(c['type'] for c in top.get('cells',{}).values());checks=[]
            checks.append({'name':'no_latches','pass':not any('latch' in c['type'].lower() for m in modules.values() for c in m.get('cells',{}).values())})
            # Exact interface incl. non-zero array offsets and declaration direction.
            expected_ports={p['name']:(p['direction'],p['width'], min(map(int,re.findall(r'-?\d+',p['bounds']))) if p['bounds'] else 0) for p in row['interface']}
            actual_ports={k:(p['direction'],len(p['bits']),p.get('offset',0)) for k,p in top['ports'].items()}
            checks.append({'name':'source_port_directions_widths_offsets','pass':actual_ports==expected_ports})
            for kind,n in EXPECTED.get(slug,{}).items():checks.append({'name':f'{kind}_instances={n}','pass':types[kind]==n,'actual':types[kind]})
            if slug=='module_fadd':checks.append({'name':'provided_add16_contains_16_student_add1','pass':sum(c['type']=='add1' for c in modules['add16']['cells'].values())==16})
            if slug in ('module_shift','module_shift8','ece241_2014_q7b','2014_q4b'):
                clock=top['ports']['KEY']['bits'][:1] if slug=='2014_q4b' else top['ports']['clk']['bits']
                kinds=set(EXPECTED[slug]);connections=[c['connections'].get('clk') for c in top['cells'].values() if c['type'] in kinds]
                checks.append({'name':'all_instances_share_external_clock','pass':all(c==clock for c in connections)})
            if slug=='ece241_2014_q5b':checks.append({'name':'onehot_state_width_2','pass':len(top['netnames']['state']['bits'])==2})
            record.update(checks=checks,cell_types=dict(types),netlist_sha256=sha(out),netlist_path=str(out))
            if not all(c['pass'] for c in checks):record['status']='FAIL'
        if record['status']!='PASS':failed.append(slug)
        results.append(record)
        dump(ROOT/'reports/E1_structure.json',{'status':'PASS' if len(results)==112 and not failed else 'IN_PROGRESS','records':results,'timestamp':datetime.now(timezone.utc).isoformat(),'scope':'Synthesizable process netlists, no latch, exact public ports, mandatory helper instances and shared clocks. No standard-cell PPA or official OJ claim.'})
    print('E1_STRUCTURE',len(results),'failed',failed,flush=True)
    return 1 if failed else 0

if __name__=='__main__':sys.exit(main())
