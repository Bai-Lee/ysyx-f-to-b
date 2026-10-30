from evidence import *
import requests
from urllib3.util.retry import Retry
import re,csv

def main():
    folder=ROOT/'F/programs';gcc=Path(r'D:\msys64\ucrt64\bin\gcc.exe');gdb=gcc.with_name('gdb.exe');objdump=gcc.with_name('objdump.exe');env=os.environ.copy();env['PATH']=str(gcc.parent)+';'+env.get('PATH','')
    examples={'z3':('#include <stdio.h>\nint main(void) {\n  int x=1;\n  int y=2;\n  int z=x+y;\n  printf("z = %d\\n",z);\n  return 0;\n}\n','z = 3\n'),'z42':('#include <stdio.h>\nint main(void) { int x=17, y=25; int z=x+y; printf("z = %d\\n",z); return 0; }\n','z = 42\n'),'sum10_c':('#include <stdio.h>\nint main(void) {\n  int i=0, sum=0;\n  while(i!=10) { i=i+1; sum=sum+i; }\n  printf("sum = %d\\n",sum);\n  return 0;\n}\n','sum = 55\n')}
    result={'native':{},'online':{},'source_scope':'F4 C execution and source/assembly correspondence only; not E coursework'}
    for name,(code,expected) in examples.items():
        src=folder/(name+'.c');src.write_text(code,encoding='utf8');exe=ROOT/'temp'/(name+'.exe')
        c=run('F4/'+name+'_compile',[gcc,'-std=c17','-Wall','-Wextra','-Werror','-g','-O0',src,'-o',exe],[src],env=env,timeout=40)
        r=run('F4/'+name+'_execute',[exe],[src,exe],env=env,timeout=10)
        actual=(ROOT/'artifacts/F4'/(name+'_execute')/'stdout.log').read_text('utf8').replace('\r\n','\n')
        if actual!=expected:raise ValueError((name,actual,expected))
        asm=ROOT/'F/analysis'/(name+'_native.s')
        s=run('F4/'+name+'_assembly',[gcc,'-std=c17','-O0','-g','-fverbose-asm','-S',src,'-o',asm],[src],env=env,timeout=40)
        result['native'][name]={'status':'PASS' if all(q['status']=='PASS' for q in (c,r,s)) else 'FAIL','expected_stdout':expected,'source_sha256':sha(src),'assembly':str(asm),'assembly_sha256':sha(asm)}
    bad=folder/'negative_invalid_c.txt';bad.write_text('int main(void) { return missing_name; }\n',encoding='ascii');q=run('F4/negative_compiler',[gcc,'-x','c','-std=c17','-Wall','-Werror',bad,'-o',ROOT/'temp/negative_c.exe'],[bad],env=env,expected=1,timeout=30);result['negative_compile']=q
    if gdb.exists():
        src=folder/'z3.c';q=run('F4/gdb_source_state',[gdb,'--batch','-q','-ex','set pagination off','-ex','break z3.c:6','-ex','run','-ex','print x','-ex','print y','-ex','print z','-ex','continue',ROOT/'temp/z3.exe'],[src,ROOT/'temp/z3.exe'],env=env,timeout=30)
        text=(ROOT/'artifacts/F4/gdb_source_state/stdout.log').read_text('utf8',errors='replace')
        if not all(re.search(r'\$'+str(i)+r'\s*=\s*'+str(v)+r'\b',text) for i,v in enumerate((1,2,3),1)):raise ValueError('GDB did not confirm x/y/z')
        result['gdb']=q
    session=requests.Session();session.mount('https://',requests.adapters.HTTPAdapter(max_retries=Retry(total=3,backoff_factor=.4,status_forcelist=[429,500,502,503,504],allowed_methods=['GET','POST'])))
    online=ROOT/'artifacts/F4/compiler_explorer';online.mkdir(parents=True,exist_ok=True)
    for name in ('z3','z42','sum10_c'):
        code=examples[name][0];body={'source':code,'lang':'c','options':{'userArguments':'-O0 -g -std=c17','compilerOptions':{'executorRequest':True},'filters':{'execute':True}}}
        url='https://godbolt.org/api/compiler/cg151/compile';response=session.post(url,json=body,headers={'Accept':'application/json'},timeout=(15,75));response.raise_for_status();data=response.json();dump(online/(name+'_request.json'),body);dump(online/(name+'_response.json'),data)
        output='\n'.join(x['text'] for x in data.get('stdout',[]))+'\n'
        if data.get('code')!=0 or not data.get('didExecute') or data.get('truncated') or output!=examples[name][1]:raise ValueError('Online execution failed: '+name)
        result['online'][name]={'status':'PASS','url':url,'compiler':'cg151','didExecute':True,'stdout':output,'request_sha256':sha(online/(name+'_request.json')),'response_sha256':sha(online/(name+'_response.json')),'http_status':response.status_code}
        print('F4_ONLINE',name,repr(output),flush=True)
    body={'source':examples['z3'][0],'lang':'c','options':{'userArguments':'-O0 -g -std=c17','compilerOptions':{'executorRequest':False},'filters':{'execute':False,'intel':True,'labels':True,'directives':False,'commentOnly':False}}}
    response=session.post('https://godbolt.org/api/compiler/cg151/compile',json=body,headers={'Accept':'application/json'},timeout=(15,75));response.raise_for_status();data=response.json();dump(online/'assembly_request.json',body);dump(online/'assembly_response.json',data)
    if data.get('code')!=0 or data.get('truncated') or not data.get('asm'):raise ValueError('Online assembly missing')
    annotated=[x for x in data['asm'] if x.get('source') and x['source'].get('line')]
    if len(annotated)<3:raise ValueError('Compiler Explorer source mapping absent')
    md=['# F4：C 与汇编的对应','', 'Compiler Explorer 的真实 gcc 15.1 API 编译结果。用 API 的 source.line 对应代替网页颜色高亮；不是从手写汇编伪造映射。原始请求/响应在 artifacts/F4/compiler_explorer。','', '| C行号 | 汇编 |','|---|---|']
    md += [f'| {x["source"]["line"]} | `{x["text"].replace("|","\\|")}` |' for x in annotated]
    md += ['', '同一源程序也用已安装的 MinGW GCC 本地编译和执行。宿主 Windows x86-64 与线上 Linux x86-64 的 ABI/启动代码不同，因此不要求两份汇编逐字相同。均实测得到 z=3；修改例为42，求和为55。','', '把 x/y/z 的赋值与相应源行的栈槽写入、读出和加法指令对照；printf 对应调用及参数准备；return 对应返回值与函数退栈。这里不要求先掌握每一条 x86 指令，也不声称编译器经过形式化验证。']
    (ROOT/'F/analysis/c_to_assembly.md').write_text('\n'.join(md)+'\n',encoding='utf8')
    result['source_assembly']={'status':'PASS','mapped_instructions':len(annotated),'raw_response_sha256':sha(online/'assembly_response.json')}
    # Relate real RTL commit states to the dedicated sum circuit's iteration states.
    path=ROOT/'artifacts/F/rtl_f5_sum10/commits.csv';rows=list(csv.DictReader(path.open(encoding='utf8')));boundary=[]
    for row in rows:
        if row['reset']=='1':continue
        pc=int(row['new_pc'],16);i=int(row['r1'],16);s=int(row['r2'],16)
        if pc in (4,7):
            if s!=i*(i+1)//2:raise ValueError('State-machine boundary invariant')
            boundary.append({'cycle':int(row['cycle']),'pc':pc,'i':i,'sum':s})
    dump(ROOT/'F/analysis/sum_state_boundaries.json',boundary)
    result['state_boundary_invariant']={'status':'PASS','rows':len(boundary),'scope':'At loop boundary PC4 or terminal PC7, sum=i(i+1)/2. The two add instructions create an intermediate state not identical to a dedicated-sum clock.'}
    result['toolchain']={'gcc':str(gcc),'sha256':sha(gcc),'gdb':str(gdb) if gdb.exists() else None,'compiler_explorer':'gcc 15.1 cg151'}
    result['status']='PASS' if all(v['status']=='PASS' for v in result['native'].values()) and q['status']=='PASS' else 'FAIL';dump(ROOT/'reports/F4_results.json',result);print('F4_RESULT',result['status'],flush=True)
    return 0 if result['status']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
