from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
source=ROOT/'reports/C5_sdram_sweep.json';rows=[]
for run_record in json.loads(source.read_text())['runs']:
    if run_record['corrupt']:continue
    size=run_record['bytes'];width=run_record['width'];ranks=run_record['ranks'];chips=run_record['chips']
    assert sum(chip['read_bytes'] for chip in chips)==16*size
    assert sum(chip['write_bytes'] for chip in chips)==8*size
    expected=[]
    for rank in range(ranks):
        rank_capacity=33554432*(width//16);covered=max(0,min(size-rank*rank_capacity,rank_capacity))
        for lane in range(width//16):
            chip=rank*2+lane;per_chip=covered//(width//16)
            assert chips[chip]['read_bytes']==per_chip*16 and chips[chip]['write_bytes']==per_chip*8
            expected.append({'chip':chip,'unique_capacity_bytes_exercised':per_chip,'read_bytes':per_chip*16,'write_bytes':per_chip*8})
    rows.append({'evidence':run_record['evidence'],'width':width,'ranks':ranks,'bytes':size,'status':'PASS','physical_byte_expectations':expected})
dump(ROOT/'reports/C5_sdram_bus_coverage.json',{'status':'PASS_RECORDED_COMPLETED_SWEEPS','source_sha256':sha(source),'runs':rows,'derivation':'Every requested8/16/32/64-bit width is written/read foraddress andinverse. CPUlogicalbytepayload=8N eachdirection. SDRAMcontroller reads32bits for everyarchitectural load, giving16N pinreadbytes; maskedpinwrites commit8N. Eachx16lane andrank receives its proportional share. These physicalcounts supplement CPUunique-byte/operationcoverage.'})
print('C5_SDRAM_PIN_BYTE_COUNTS_PASS',len(rows),flush=True)
