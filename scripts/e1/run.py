from common import *
import argparse
BIN=Path(r'C:\YSYX_WORKSPACE\tools\oss-cad-suite-20261022\oss-cad-suite\bin')

def run_one(row,mutation=None):
    slug=row['slug'];name=slug if mutation is None else slug+'__fault_'+mutation['name'];out=ROOT/'temp/E1'/(name+'.vvp');dut=Path(row['dut']);tb=Path(row['testbench']);support=Path(row['support']);syntax_support=Path(row['syntax_support']);vec=Path(row['vectors'])
    if mutation:
        text=dut.read_text('utf8')
        if text.count(mutation['old'])!=1:raise ValueError('Mutation must match exactly once: '+name)
        dut=ROOT/'temp/E1'/(name+'.v');dut.write_text(text.replace(mutation['old'],mutation['new']),encoding='utf8')
    syntax=run('E1/'+name+'/syntax',[BIN/'iverilog.exe','-g2005','-Wall','-s','top_module','-tnull',dut,syntax_support],[dut,syntax_support],timeout=30)
    compiled=run('E1/'+name+'/compile',[BIN/'iverilog.exe','-g2012','-Wall','-s','tb','-o',out,dut,tb,support],[dut,tb,support,vec],timeout=30)
    if syntax['status']!='PASS' or compiled['status']!='PASS':return {**row,'status':'FAIL','syntax':syntax,'compile':compiled}
    sim=run('E1/'+name+'/simulate',[BIN/'vvp.exe',out],[dut,tb,support,vec,out],timeout=60,expected=1 if mutation else 0)
    text=(ROOT/'artifacts/E1'/name/'simulate/stdout.log').read_text('utf8',errors='replace');ok=sim['status']=='PASS' and ('MISMATCH' in text if mutation else f'PASS {slug} checks={row["cases"]}' in text)
    return {**row,'status':'PASS' if ok else 'FAIL','mutation':mutation,'syntax':syntax,'compile':compiled,'simulation':sim,'semantic_sentinel_pass':ok,'dut_sha256':sha(dut),'vectors_sha256':sha(vec),'testbench_sha256':sha(tb),'support_sha256':sha(support),'syntax_support_sha256':sha(syntax_support)}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('slugs',nargs='*');parser.add_argument('--all',action='store_true');parser.add_argument('--pending',action='store_true');parser.add_argument('--controls',action='store_true');args=parser.parse_args()
    allrows=json.loads((OUT/'jobs.json').read_text('utf8'))['records'];rows=allrows if args.all or args.pending else [x for x in allrows if x['slug'] in args.slugs]
    results_path=ROOT/'reports/E1_results.json';previous=json.loads(results_path.read_text('utf8')) if results_path.exists() else {'records':[]};results={x['slug']:x for x in previous['records']};fail=[]
    if args.pending:
        rows=[x for x in rows if x['slug'] not in results or results[x['slug']]['status']!='PASS' or any(results[x['slug']].get(k+'_sha256')!=sha(Path(x[k])) for k in ('dut','vectors','testbench','support','syntax_support'))]
    if not rows:print('E1_RUN no changed/pending built problems',flush=True)
    for row in rows:
        result=run_one(row);results[row['slug']]=result
        if result['status']!='PASS':fail.append(row['slug'])
        dump(results_path,{'status':'IN_PROGRESS','records':sorted(results.values(),key=lambda x:x['id']),'source_scope':112,'local_self_verification':True,'official_OJ_submission':False})
    if args.controls:
        row=next(x for x in allrows if x['slug']=='andgate');control=run_one(row,{'name':'and_replaced_by_or','old':'assign out = a & b;','new':'assign out = a | b;'});dump(ROOT/'reports/E1_preflight_control.json',control)
        if control['status']!='PASS':fail.append('mutation_control')
        else:
            p=ROOT/'reports/preflight_E1.json';data=json.loads(p.read_text('utf8'));data.update(status='PASS',control='reports/E1_preflight_control.json');dump(p,data)
    print('E1_RUN',len(rows),'failures',fail,flush=True);return 1 if fail else 0
if __name__=='__main__':sys.exit(main())
