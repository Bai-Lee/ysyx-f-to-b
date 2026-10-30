"""E2 allowed competence branch: native C execution, independent FFI oracle, CE."""
from evidence import *
import argparse,ctypes,random,shutil,platform
SOURCE=ROOT/'E/E2/linked_list.c'
GCC=Path(r'D:\msys64\ucrt64\bin\gcc.exe')


def ffi_check(library):
    lib=ctypes.CDLL(str(library));ptr=ctypes.c_void_p;sz=ctypes.c_size_t;ip=ctypes.POINTER(ctypes.c_int)
    signatures={'list_create':([],ptr),'list_destroy':([ptr],None),'list_size':([ptr],sz),'list_insert':([ptr,sz,ctypes.c_int],ctypes.c_int),'list_erase':([ptr,sz,ip],ctypes.c_int),'list_get':([ptr,sz,ip],ctypes.c_int),'list_reverse':([ptr],None),'list_sort':([ptr],None),'list_clear':([ptr],None),'list_snapshot':([ptr,ip,sz],sz),'list_validate':([ptr],ctypes.c_int),'list_live_nodes':([],sz),'list_limit_allocations':([ctypes.c_long],None)}
    for name,(args,result) in signatures.items():fn=getattr(lib,name);fn.argtypes=args;fn.restype=result
    lists=[lib.list_create(),lib.list_create()];assert all(lists);refs=[[],[]];operations=0;rng=random.Random(260702)
    def check():
        for handle,ref in zip(lists,refs):
            assert lib.list_validate(handle)==1, 'topology/length/tail invariant'
            assert lib.list_size(handle)==len(ref), 'size differs'
            assert lib.list_snapshot(handle,None,0)==len(ref), 'zero-capacity snapshot'
            for cap in (len(ref),len(ref)//2):
                buf=(ctypes.c_int*(cap+2))(*([1234567]*(cap+2)))
                assert lib.list_snapshot(handle,buf,cap)==len(ref)
                assert list(buf[:cap])==ref[:cap], 'sequence differs'
                assert buf[cap]==buf[cap+1]==1234567,'snapshot overrun'
            if ref:
                for index in (0,len(ref)//2,len(ref)-1):
                    value=ctypes.c_int(314159);assert lib.list_get(handle,index,ctypes.byref(value))==1 and value.value==ref[index]
            for index in (len(ref),2**(8*ctypes.sizeof(sz))-1):
                value=ctypes.c_int(314159);assert lib.list_get(handle,index,ctypes.byref(value))==0 and value.value==314159
        assert lib.list_live_nodes()==sum(map(len,refs)), 'allocation balance differs'
    def insert(which,index,value,fail=False):
        nonlocal operations
        handle=lists[which];ref=refs[which]
        lib.list_limit_allocations(0 if fail else -1)
        success=lib.list_insert(handle,index,value);assert success==int(index<=len(ref) and not fail),'insert return'
        if success:ref.insert(index,value)
        lib.list_limit_allocations(-1);operations+=1;check()
    check()
    for value in [-(2**31),2**31-1,0,0,-1,1]+list(range(511,-1,-1)):insert(0,len(refs[0]),value)
    lib.list_sort(lists[0]);refs[0].sort();operations+=1;check()
    lib.list_reverse(lists[0]);refs[0].reverse();operations+=1;check()
    for i in (0,len(refs[0])//2,len(refs[0])):insert(0,i,999,True)
    insert(1,0,42);insert(1,2**(8*ctypes.sizeof(sz))-1,8)
    for step in range(12000):
        which=rng.randrange(2);handle=lists[which];ref=refs[which];op=rng.randrange(8)
        index=rng.randrange(len(ref)+2);value=rng.choice([-(2**31),2**31-1,rng.randint(-9999,9999)])
        if len(ref)>256:op=5
        if op in (0,1,6):insert(which,index,value,op==6);continue
        if op==2:
            out=ctypes.c_int(314159);got=lib.list_erase(handle,index,ctypes.byref(out));assert got==int(index<len(ref))
            if got:assert out.value==ref.pop(index)
            else:assert out.value==314159
        elif op==3:lib.list_reverse(handle);ref.reverse()
        elif op==4:lib.list_sort(handle);ref.sort()
        elif op==5:lib.list_clear(handle);ref.clear()
        else:
            out=ctypes.c_int(314159);got=lib.list_get(handle,index,ctypes.byref(out));assert got==int(index<len(ref))
            assert out.value==(ref[index] if got else 314159)
        operations+=1;check()
    for handle in lists:lib.list_destroy(handle)
    lib.list_destroy(None);assert lib.list_live_nodes()==0
    print('PASS E2 FFI operations='+str(operations)+' live_nodes=0 seed=260702',flush=True)


def main(online):
    folder=ROOT/'E/E2';temp=ROOT/'temp/E2';temp.mkdir(parents=True,exist_ok=True)
    previous_path=ROOT/'reports/E2_results.json'
    previous=json.loads(previous_path.read_text('utf8')) if previous_path.exists() else {}
    env=os.environ.copy();env['PATH']=str(GCC.parent)+';'+env.get('PATH','');env['PYTHONIOENCODING']='utf-8'
    prior=json.loads((ROOT/'reports/F4_results.json').read_text('utf8'))
    assert sha(GCC)==prior['toolchain']['sha256'],'GCC changed since prior actual F4 acceptance'
    source_course=ROOT.parents[1]/'YSYX_F_B_Archive/docs/raw_html/E/E2.html'
    preflight={'status':'PASS','task':'E2 official independent-linked-list competence branch','course_source':str(source_course),'course_source_sha256':sha(source_course),'compiler':{'path':str(GCC),'sha256':sha(GCC),'version':subprocess.run([str(GCC),'--version'],capture_output=True,env=env).stdout.decode('utf8').splitlines()[0]},'reused_prior_positive_negative_evidence':'reports/F4_results.json; executable fingerprint unchanged','resource_budget':{'parallel_jobs':1,'compile_timeout_seconds':60,'execute_timeout_seconds':30,'heavy_jobs':0},'scope':'Native C17, recursion/pointers/list; public CE execution. No Linux host installation.'}
    dump(ROOT/'reports/preflight_E2.json',preflight)
    flags=['-std=c17','-Wall','-Wextra','-Wpedantic','-Werror'];runs=[]
    for opt in ('O0','O2'):
        exe=temp/('linked_list_'+opt+'.exe')
        c=run('E2/'+opt+'/compile',[GCC,*flags,'-'+opt,'-g',SOURCE,'-o',exe],[SOURCE],env=env,timeout=60);assert c['status']=='PASS';runs.append(c)
        r=run('E2/'+opt+'/execute',[exe],[SOURCE,exe],env=env,timeout=30);assert r['status']=='PASS';runs.append(r)
        assert (ROOT/'artifacts/E2'/opt/'execute/stdout.log').read_text('utf8').strip()=='PASS E2 linked_list selftest operations=20000 live_nodes=0'
    library=temp/'linked_list.dll'
    c=run('E2/ffi/compile',[GCC,*flags,'-O2','-g','-DLIST_LIBRARY','-shared',SOURCE,'-o',library],[SOURCE],env=env,timeout=60);assert c['status']=='PASS';runs.append(c)
    r=run('E2/ffi/execute',[sys.executable,Path(__file__).resolve(),'--ffi',library],[SOURCE,Path(__file__).resolve(),library],env=env,timeout=30);assert r['status']=='PASS';runs.append(r)
    assert 'PASS E2 FFI operations=12525 live_nodes=0 seed=260702' in (ROOT/'artifacts/E2/ffi/execute/stdout.log').read_text('utf8')
    controls=[]
    for name,old,new in [('broken_reverse_tail','list->tail = list->head;\n    while (node)','list->tail = NULL;\n    while (node)'),('descending_sort','if (left->value <= right->value)','if (left->value >= right->value)'),('allocation_failure_changes_size','if (!node) return 0;','if (!node) { ++list->length; return 0; }')]:
        text=SOURCE.read_text('utf8');assert text.count(old)==1;mut=temp/(name+'.c');mut.write_text(text.replace(old,new),encoding='utf8');dll=temp/(name+'.dll')
        c=run('E2/faults/'+name+'/compile',[GCC,*flags,'-O2','-DLIST_LIBRARY','-shared',mut,'-o',dll],[SOURCE,mut],env=env,timeout=60);assert c['status']=='PASS'
        r=run('E2/faults/'+name+'/execute',[sys.executable,Path(__file__).resolve(),'--ffi',dll],[SOURCE,mut,Path(__file__).resolve(),dll],env=env,expected=1,timeout=30)
        err=(ROOT/'artifacts/E2/faults'/name/'execute/stderr.log').read_text('utf8');assert r['status']=='PASS' and 'AssertionError' in err
        controls.append({'name':name,'status':'PASS','compile':c,'execute':r})
    result={'status':'NATIVE_PASS_ONLINE_PENDING','branch':'official independent linked-list competence alternative','source':str(SOURCE),'source_sha256':sha(SOURCE),'native_runs':runs,'controls':controls,'official_exercise_count_completed':0,'individual_CEX_rows_not_marked_pass':True,'compiler':preflight['compiler'],'platform':platform.platform()}
    dump(ROOT/'reports/E2_results.json',result)
    if online:
        import requests
        from urllib3.util.retry import Retry
        session=requests.Session();session.mount('https://',requests.adapters.HTTPAdapter(max_retries=Retry(total=2,backoff_factor=1,status_forcelist=[429,500,502,503,504],allowed_methods=['POST'])))
        target=ROOT/'artifacts/E2/compiler_explorer';target.mkdir(parents=True,exist_ok=True)
        online_results=[]
        for name,extra in [('normal',''),('asan_ubsan',' -fsanitize=address,undefined -fno-omit-frame-pointer')]:
            body={'source':SOURCE.read_text('utf8'),'lang':'c','options':{'userArguments':'-std=c17 -O1 -g -Wall -Wextra -Werror'+extra,'compilerOptions':{'executorRequest':True},'filters':{'execute':True}}}
            url='https://godbolt.org/api/compiler/cg151/compile';dump(target/(name+'_request.json'),body)
            response=session.post(url,json=body,headers={'Accept':'application/json'},timeout=(15,75));response.raise_for_status();data=response.json();dump(target/(name+'_response.json'),data)
            out='\n'.join(x['text'] for x in data.get('stdout',[]));err='\n'.join(x['text'] for x in data.get('stderr',[]))
            assert data.get('code')==0 and data.get('didExecute') and not data.get('truncated') and out.strip()=='PASS E2 linked_list selftest operations=20000 live_nodes=0',(name,out,err)
            assert not any(x in err for x in ('ERROR: AddressSanitizer','runtime error:','LeakSanitizer'))
            online_results.append({'name':name,'status':'PASS','url':url,'compiler':'cg151','compiler_arguments':body['options']['userArguments'],'http_status':response.status_code,'didExecute':True,'exit_code':data['code'],'stdout':out,'stderr':err,'request':str(target/(name+'_request.json')),'request_sha256':sha(target/(name+'_request.json')),'response':str(target/(name+'_response.json')),'response_sha256':sha(target/(name+'_response.json'))})
            print('E2_ONLINE',name,'PASS',flush=True)
        result.update(status='PASS_ALTERNATIVE',online=online_results)
    elif previous.get('source_sha256')==sha(SOURCE) and len(previous.get('online',[]))==2:
        for item in previous['online']:
            assert item['status']=='PASS' and sha(item['request'])==item['request_sha256'] and sha(item['response'])==item['response_sha256']
        result.update(status='PASS_ALTERNATIVE',online=previous['online'],online_evidence_reused=True)
    dump(ROOT/'reports/E2_results.json',result);print('E2_RESULT',result['status'],flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--ffi',type=Path);parser.add_argument('--online',action='store_true');args=parser.parse_args()
    if args.ffi:ffi_check(args.ffi)
    else:main(args.online)
