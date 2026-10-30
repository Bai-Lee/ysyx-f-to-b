from common import *
from resource_policy import windows_available_bytes,linux_memory,load_policy

def main():
    tools=[VERILATOR,Path('/usr/bin/gcc'),Path('/usr/bin/riscv64-linux-gnu-gcc'),Path('/usr/bin/make')]
    samples={'windows_available_bytes':windows_available_bytes(),'linux':linux_memory()}
    versions=[]
    for executable in tools:
        assert executable.is_file(),executable
        out,_,_=run('B/preflight/'+executable.name,[executable,'--version'],inputs=[executable])
        versions.append({'path':str(executable),'sha256':sha(executable),'version':out.splitlines()[0]})
    dump(ROOT/'reports/B_PREFLIGHT.json',{'status':'READY_FOR_B1_SCOPED_RUNS','timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'capabilities':['NEMU C interpreter','RV32 cross compiler','Verilator with C++ runner','pinned original SoC RTL','Icarus and synthesis/STA to be checked at B3/B5 use'],'inputs':['B/runtime/course_specs.json','reports/B_baseline.json','reports/B_runtime_setup.json'],'tools':versions,'memory':samples,'limits':load_policy(),'validation':'B1 positive/negative CSR, context and RT-Thread tests; every NPC retirement compared against independent NEMU, cycles clocked independently without copying DUT CSR values. Standalone NEMU also checked against qualified Spike where applicable.','scope':'Machine mode, synchronous ECALL only, no asynchronous interrupts/U/S/VM or official examination; project ID is not a student identity. B2 source has no programming assignment. B3/B4/B5 remain pending.'})
    print('B_PREFLIGHT_PASS')

if __name__=='__main__':main()
