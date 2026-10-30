from native import *
import shutil,csv
def main():
    d=SRC/'lists';(d/'lcthw').mkdir(parents=True,exist_ok=True)
    (d/'lcthw/list.h').write_text(block(32,1));(d/'lcthw/dbg.h').write_text(block(20,0))
    (d/'list.c').write_text(block(32,2));(d/'minunit.h').write_text(block(30,0));(d/'list_tests.c').write_text(block(32,3))
    shutil.copyfile(d/'lcthw/dbg.h',d/'dbg.h')
    base,_,_=build('list_original',files=[d/'list.c',d/'list_tests.c'],flags=['-I'+str(d)])
    o,e,r=execute('list_original',base,vg=True);assert 'ALL TESTS PASSED' in o and 'Tests run: 6' in o and 'ERROR SUMMARY: 0 errors' in e
    (d/'lcthw/list_algos.h').write_text(block(33,1));(d/'algos_original.c').write_text(block(33,2));(d/'algos_tests.c').write_text(block(33,0))
    _,o,e=build('list_inline_original',files=[d/'list.c',d/'algos_original.c',d/'algos_tests.c'],flags=['-I'+str(d)],expected=(1,));assert 'undefined reference' in e
    repaired=block(33,2).replace('inline ','static inline ')
    (d/'algos_linkable.c').write_text(repaired)
    old,_,_=build('list_merge_leak',files=[d/'list.c',d/'algos_linkable.c',d/'algos_tests.c'],flags=['-I'+str(d)])
    o,e,r=execute('list_merge_leak',old,vg=True,expected=(99,));assert 'ALL TESTS PASSED' in o and re.search(r'definitely lost:\s+[1-9]',e)
    # Always return a node-copy, including empty/singleton; preserve borrowed values.
    repaired=repaired.replace('        return list;','        List *copy=List_create(); if(!copy)return NULL;\n        if(list->first)List_push(copy,list->first->value); return copy;')
    repaired=repaired.replace('    return List_merge(sort_left, sort_right, cmp);','    List *result=List_merge(sort_left,sort_right,cmp);\n    List_destroy(sort_left);List_destroy(sort_right);return result;')
    (d/'algos.c').write_text(repaired)
    (d/'algos_tests.c').write_text(block(33,0).replace('List_create(words)','List_create()'))
    (d/'lcthw/extensions.h').write_text('''#include <lcthw/list.h>
#include <lcthw/list_algos.h>
List *List_copy_nodes(const List *);
int List_concat_transfer(List *,List *);
List *List_split_transfer(List *,int);
int List_insert_sorted(List *,void *,List_compare);
int List_bottom_up_sort(List *,List_compare);
''')
    fixed,_,_=build('list_algos_fixed',files=[d/'list.c',d/'algos.c',d/'algos_tests.c'],flags=['-I'+str(d)])
    o,e,r=execute('list_algos_fixed',fixed,vg=True);assert 'ALL TESTS PASSED' in o and 'ERROR SUMMARY: 0 errors' in e
    files=[d/'list.c',d/'algos.c',SRC/'list_extensions.c',SRC/'list_property.c']
    tested,_,_=build('list_properties',files=files,flags=['-I'+str(d)])
    o,e,r=execute('list_properties',tested,vg=True,timeout=60);assert 'PASS 3000' in o and 'ERROR SUMMARY: 0 errors' in e
    verdict(['LCT-32-BASE','LCT-32-X03'],'PASS',['list_original','list_properties'],'Original six tests plus3000 model-backed operations; node-copy/transfer-concat/split ownership is explicit; head/tail/prev/next/count checked in both directions.')
    verdict(['LCT-33-BASE','LCT-33-X05','LCT-33-X06'],'PASS_ADAPTED',['list_inline_original','list_merge_leak','list_algos_fixed','list_properties'],'Original inline linkage error reproduced; linkable original passes weak sortedness tests but leaks. Corrected copy-returning merge and iterative in-place bottom-up merge satisfy260 stable-sort cases including0/1 and duplicates. Sorted insertion preserves equal-key order.')
    benchmark=SRC/'list_benchmark.c';benchmark.write_text(benchmark.read_text().replace('#include <stdint.h>','#include <stdint.h>\n#include <inttypes.h>')) if '#include <inttypes.h>' not in benchmark.read_text() else None
    exe,_,_=build('list_benchmark',files=[d/'list.c',d/'algos.c',SRC/'list_extensions.c',benchmark],flags=['-I'+str(d),'-O2'])
    rows=[]
    for n in (32,128,512,2048):
        for method in range(4):
            o,e,r=execute(f'list_bench_{method}_{n}',exe,[str(method),str(n)],timeout=90)
            values=o.strip().split(',');assert len(values)==6
            row={'method':int(values[0]),'n':int(values[1]),'iterations':int(values[2]),'timed_seconds':float(values[3]),'mean_build_sort_us':float(values[4]),'mean_comparisons':float(values[5])}
            assert row['timed_seconds']>=3 and row['iterations']>0;rows.append(row)
            dump(PROJECT/'reports/E3_list_benchmark.json',{'status':'IN_PROGRESS','records':rows})
    run('list_man_time',['man','-P','cat','3','time'])
    dump(PROJECT/'reports/E3_list_benchmark.json',{'status':'PASS','records':rows,'seed_rule':'260733+n; identical input at each n for all methods','methods':['bubble','copying_merge','bottom_up_merge','sorted_insertion'],'timing_scope':'Wall time of constructing one sorted list, including required allocation/copy and discarded-input cleanup; output validation/final destruction outside timing. Each sample accumulates>=3seconds. One batch per point, no confidence intervals; WSL guest is not isolated.','compiler_flags':'GNU17 GCC11 -O2 -g; AMD64 WSL2,2GB/4vCPU; sequential benchmark'})
    verdict(['LCT-33-X01','LCT-33-X02'],'PASS',['list_man_time','reports/E3_list_benchmark.json'],'16 actual timed batches, four input lengths and four methods, at least3seconds each. No physical-chip performance inference.')
    print('LISTS_AND_BENCHMARK_DONE',flush=True)
if __name__=='__main__':main()
