from native import *
import struct,ctypes,random,shlex
def main():
    lab=common.LAB/'database';lab.mkdir(exist_ok=True)
    original,_,_=build('ex17_original',block(17))
    db=lab/'original.db'
    for tag,args in [('create',['c']),('set',['s','1','Alice','alice@example.invalid']),('get',['g','1']),('list',['l']),('delete',['d','1'])]:
        o,e,r=execute('ex17_'+tag,original,[str(db),*args],vg=True);assert 'ERROR SUMMARY: 0 errors' in e
        if tag in ('get','list'):assert o=='1 Alice alice@example.invalid\n'
    class Address(ctypes.Structure):_fields_=[('id',ctypes.c_int),('set',ctypes.c_int),('name',ctypes.c_char*512),('email',ctypes.c_char*512)]
    assert db.stat().st_size==ctypes.sizeof(Address)*100==103200
    execute('ex17_long_set',original,[str(db),'s','2','x'*600,'mail'])
    o,_,_=execute('ex17_long_get',original,[str(db),'g','2']);assert 'x'*512+'mail mail' in o
    fixed=block(17).replace('if(!res) die("Name copy failed");','addr->name[MAX_DATA-1]=0;\n    if(!res) die("Name copy failed");').replace('if(!res) die("Email copy failed");','addr->email[MAX_DATA-1]=0;\n    if(!res) die("Email copy failed");')
    classic,_,_=build('ex17_terminated',fixed)
    execute('ex17_classic_create',classic,[str(lab/'fixed.db'),'c'])
    execute('ex17_classic_set',classic,[str(lab/'fixed.db'),'s','0','x'*600,'mail'])
    o,e,r=execute('ex17_classic_get',classic,[str(lab/'fixed.db'),'g','0'],vg=True);assert o=='0 '+'x'*511+' mail\n' and 'ERROR SUMMARY: 0 errors' in e
    invalid,_,_=build('ex17_negative_id',block(17),flags=['-fsanitize=address,undefined','-fno-sanitize-recover=all'])
    o,e,r=execute('ex17_negative_id',invalid,[str(db),'g','-1'],expected=(1,-11));assert 'out of bounds' in e or 'AddressSanitizer' in e
    short=lab/'short.db';short.write_bytes(db.read_bytes()[:27])
    o,e,r=execute('ex17_corrupt_short',original,[str(short),'l'],expected=(1,));assert 'Failed to load' in o+e
    verdict(['LCT-17-BASE','LCT-17-BREAK'],'PASS',['ex17_create','ex17_get','ex17_long_get','ex17_classic_get','ex17_negative_id','ex17_corrupt_short'],'Original CRUD/size verified; long strncpy fields reproduce concatenation defect; copied correction terminates; negative IDs and corrupted file tested. Allocation limit has a separate bounded probe.')
    source=SRC/'database.c';exe,_,_=build('database',files=[source],strict=True)
    def command(tag,args,expected=(0,),vg=False):return execute('database_'+tag,exe,args,expected,vg)
    for width,rows in [(1,1),(8,3),(32,8),(513,2)]:
        file=lab/f'db-{width}-{rows}.bin'
        command(f'create_{width}',[str(file),'c',str(width),str(rows)])
        assert file.stat().st_size==32+rows*(5+3*width)
        command(f'set_{width}',[str(file),'s','0','Alice','a@example.invalid','City','27'])
        o,e,r=command(f'get_{width}',[str(file),'g','0'],vg=True)
        assert o=='0\t'+'\t'.join(x[:width-1] for x in ['Alice','a@example.invalid','City'])+'\t27\n' and 'ERROR SUMMARY: 0 errors' in e
        data=file.read_bytes();magic,w,n,h=struct.unpack('<8sQQQ',data[:32]);assert (magic,w,n)==(b'YSYXDB01',width,rows)
        calc=14695981039346656037
        for b in data[32:]:calc=((calc^b)*1099511628211)&((1<<64)-1)
        assert h==calc
    file=lab/'model.bin';command('model_create',[str(file),'c','24','12']);ref={};rng=random.Random(260717)
    for step in range(36):
        i=rng.randrange(12)
        if i in ref:command('model_del'+str(step),[str(file),'d',str(i)]);del ref[i]
        else:
            values=[f'person{i}',f'e{i}@example.invalid',f'city{i%3}',str(20+i)]
            command('model_set'+str(step),[str(file),'s',str(i),*values]);ref[i]=values
        o,_,_=command('model_list'+str(step),[str(file),'l'])
        assert o==''.join(str(k)+'\t'+'\t'.join(v)+'\n' for k,v in sorted(ref.items()))
    for field,column,query in [('city',2,'city1'),('name',0,'person'),('email',1,'@example'),('age',3,'23')]:
        o,_,_=command('find_'+field,[str(file),'f',field,query])
        expect=''.join(str(k)+'\t'+'\t'.join(v)+'\n' for k,v in sorted(ref.items()) if (v[column]==query if field=='age' else query in v[column]))
        assert o==expect
    for i,args in enumerate([['g','-1'],['g','12'],['g','no'],['f','bad','x'],['?'],['s','0','x','e','c','4294967296']]):
        o,e,r=command('reject'+str(i),[str(file),*args],expected=(1,),vg=True);assert 'ERROR SUMMARY: 0 errors' in e and 'in use at exit: 0 bytes' in e
    damaged=lab/'damaged.bin';blob=bytearray(file.read_bytes());blob[-2]^=1;damaged.write_bytes(blob)
    o,e,r=command('checksum',[str(damaged),'l'],expected=(1,),vg=True);assert 'checksum mismatch' in e and 'in use at exit: 0 bytes' in e
    # Refactor the copied implementation into a genuinely global-context API.
    text=source.read_text();text=text.replace('static void cleanup', 'static Connection global_db={0};static Connection *c=&global_db;\nstatic void cleanup',1)
    for name in ['cleanup','save']:
        text=text.replace(name+'(Connection *c)',name+'(void)').replace(name+'(c)',name+'()')
    for name in ['fail','number','dimensions','row','load','show']:
        text=text.replace(name+'(Connection *c,',name+'(').replace(name+'(c,',name+'(')
    text=text.replace('allocate(Connection *c)','allocate(void)').replace('allocate(c)','allocate()')
    text=text.replace('    Connection local={0};Connection *c=&local;','')
    global_exe,_,_=build('database_global',text,strict=True)
    g=lab/'global.bin';execute('database_global_create',global_exe,[str(g),'c','16','4'])
    execute('database_global_set',global_exe,[str(g),'s','2','Bob','b@x','Town','31'])
    o,e,r=execute('database_global_get',global_exe,[str(g),'g','2'],vg=True);assert o=='2\tBob\tb@x\tTown\t31\n' and 'ERROR SUMMARY: 0 errors' in e
    # Resource-limited size search, never described as the machine's global maximum.
    lo,hi=0,500000;probes=[]
    while hi-lo>1:
        n=(lo+hi)//2
        o,e,r=shell('database_alloc_'+str(n),f'ulimit -v 65536\nexec {shlex.quote(str(exe))} unused p 64 {n}\n',expected=(0,1),timeout=40)
        probes.append({'rows':n,'bytes':197*n,'exit_code':r['exit_code']})
        if r['exit_code']==0:lo=n
        else:assert 'allocation failed' in e;hi=n
    dump(common.OUT/'database_size_probe.json',{'RLIMIT_AS_kib':65536,'max_data':64,'largest_observed_rows':lo,'first_rejected_rows':hi,'scope':'Per-process64MiB virtual-address limit on this build; not hardware/global maximum.','probes':probes})
    verdict([f'LCT-17-X{i:02}' for i in range(1,8)],'PASS',['database_model_list35','database_checksum','database_global_get','database_size_probe.json'],'Parameterized persistent format and searchable city/age, checked cleanup on failures, independent dict/binary-layout/checksum oracle, automation, and global-context refactor. Original struct1032 bytes; portable new file32+rows*(5+3*width), without native padding.')
    print('DATABASE_EXERCISE_DONE',flush=True)
if __name__=='__main__':main()
