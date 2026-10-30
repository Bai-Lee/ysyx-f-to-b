from evidence import *
from verify_C_delivery import c5_checks,load


def main():
    verified=c5_checks(False);spec=load(ROOT/'C/runtime/course_specs.json');results=load(ROOT/'reports/C_results.json')
    records=[row for row in results['records'] if row['id'].startswith('C5-')];expected=[row for row in spec['tasks'] if row['id'].startswith('C5-')]
    assert len(records)==len(expected)==62 and {row['id'] for row in records}=={row['id'] for row in expected}
    mapping={row['id']:row for row in records}
    for task in expected:
        if task['classification'] in ['PUBLIC_CORE_TASK','USER_ADAPTED']:assert mapping[task['id']]['status'].startswith('PASS')
    dump(ROOT/'reports/C5_AUDIT.json',{'status':'PASS_REQUIRED_ENGINEERING_WITH_DECLARED_LIMITS','stage_complete':True,'core_tasks':45,'adapted_tasks':2,'scope_records':62,'records':records,'verification':verified,
        'limits':['Finite functional/coverage testing, not arbitrary-input or unbounded formal proof.','RV32E machine-mode CSR/ECALL/MRET subset and cooperative RT-Thread; no asynchronous interrupt, U/S mode, protection or full privileged-ISA claim.','Ideal clocks and functional Flash/PSRAM/SDRAM/ChipLink models; no analog timing, retention, physical FPGA or new-chip signoff.','NVBoard input is controlled on an isolated Xvfb; key-repeat disabled and full Shell prompts awaited. Earlier input-overrun/readiness failures are retained.','NEMU checks every non-MMIO instruction in C5 long memory/application runs; MMIO is independently decoded and synchronized, not two independent device models.','ChipLink retains the original1GiB RTL memory capacity; only the required4KiB range is exercised.','SPI interrupt-completion variant remains optional and unimplemented.','CoreMark single iteration is functional/CRC acceptance, not a certified score; all MicroBench test workloads retain their validators.']})
    print('C5_COMPLETE_45_CORE_2_ADAPTED_62_RECORDS',flush=True)


if __name__=='__main__':main()
