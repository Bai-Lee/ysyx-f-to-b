from pathlib import Path
import sys,csv
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
    rt=ROOT/'E/runtime';p=ROOT/'E/E5';lib=WORK/'lib';lib.mkdir(exist_ok=True)
    obj=lib/'ref.o';emu=lib/'minirvEMU'
    run('E5/reference/compile',['gcc','-std=c11','-Wall','-Wextra','-Werror','-O2','-g',rt/'ref.c',rt/'emu_main.c','-o',emu],inputs=[rt/'ref.c',rt/'ref.h',rt/'emu_main.c'])
    run('E5/reference/object',['gcc','-std=c11','-Wall','-Wextra','-Werror','-O3','-g','-c',rt/'ref.c','-o',obj],inputs=[rt/'ref.c',rt/'ref.h'])
    sources=[p/'rtl'/n for n in ['minirv_decode.sv','minirv_regfile.sv','minirv_single.sv','npc_sim.sv']]
    executable=build('E5/npc','npc_sim',sources,[rt/'runner.cpp'],extra=[obj],flags=['--timescale','1ns/1ns','-CFLAGS','-O3 -g'],additional_inputs=[rt/'memory.hpp',rt/'ref.h'])
    rows=[]
    for c in json.loads((ROOT/'reports/E5_vectors.json').read_text())['cases']:
        image=Path(c['path']);assert sha(image)==c['sha256'];folder=ROOT/'artifacts/E5/cases'/c['name'];folder.mkdir(parents=True,exist_ok=True)
        # Keep actively-written traces on Linux ext4, then copy only verified bytes.
        native=WORK/'runs/E5'/c['name'];native.mkdir(parents=True,exist_ok=True)
        ct=native/'c.csv';dt=native/'rtl.csv';report=native/'result.json'
        o,e,cr=run('E5/cases/'+c['name']+'/C',[emu,image,'0',str(c['steps']),str(c['expect']),ct],inputs=[emu,image],expected=(c['error'],),timeout=90,outputs=[ct],env={'E5_TRACE_DEBUG':'1'})
        args=[executable,'--image',image,'--expect',str(c['expect']),'--trace',dt,'--report',report,'--max-cycles','100000']
        if c['steps']:args+=['--steps',str(c['steps'])]
        o,e,dr=run('E5/cases/'+c['name']+'/RTL',args,inputs=[executable,image],expected=(c['error'],),timeout=90,outputs=[dt,report])
        assert sha(ct)==cr['outputs'][0]['sha256'],'C trace changed after capture'
        result=json.loads(report.read_text());assert result['exit_code']==c['error']
        if not c['error']:
            expected=[list(map(lambda n:int(n,16),line.split(','))) for line in Path(c['trace']).read_text().splitlines()]
            for file in [ct,dt]:
                got=[list(map(lambda n:int(n,16),line.split(',')[1:])) for line in file.read_text().splitlines()]
                assert got==expected,(c['name'],file)
            assert result['gpr']==c['expected']['gpr'] and result['instructions']==c['expected']['instructions']
            assert result['load_commits']==c['expected']['loads'] and result['memory_writes']==c['expected']['stores']
            assert result['ebreak_calls']==(0 if c['steps'] else 1)
        for file in [ct,dt,report]:
            dest=folder/file.name
            if dest.exists():
                history=folder/'trace_history'/str(time.time_ns());history.mkdir(parents=True);shutil.copyfile(dest,history/dest.name)
            shutil.copyfile(file,dest);assert sha(file)==sha(dest)
        rows.append({'name':c['name'],'status':'EXPECTED_REJECTION' if c['error'] else 'PASS','result':result})
    dump(ROOT/'reports/E5_execution.json',{'status':'PASS','binary':str(executable),'binary_sha256':sha(executable),'cases':rows,'oracle':'Independent Python byte-memory model vs C11 emulator vs RTL; architectural and side-effect counts checked.'})
    mark(['E5-M005','E5-M006','E5-M007','E5-M009','E5-M010','E5-M011','E5-M012','E5-M013','E5-M014','E5-M016','E5-M017'],'PASS',['reports/E5_execution.json','reports/E5_vectors.json','artifacts/E5/cases'],'Actual C11 and Linux Verilator execution with independent Python traces. Exact8 core instructions,16GPR/x0, signed immediates, jalr alias/odd target, little-endian/partial writes, reserved/unaligned rejection and once-only ebreak callback including post-halt probes.')
    print('E5_EXECUTION_PASS',len(rows),flush=True)
if __name__=='__main__':main()
