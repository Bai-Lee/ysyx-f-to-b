from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from support import select_build
name='30000000-cycle-psram4m-qpi-sdram16x1-opt';exe=Path(select_build(name)['executable']);ref=WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so'
baseline=next(r for r in json.loads((ROOT/'reports/C5_psram_sweep.json').read_text())['runs'] if r['bytes']==65536 and not r['corrupt'])
image=WORK/'c5/workbench/psram-sweep-65536/build/psram-sweep-65536-riscv32e-ysyxsoc-sram-code.bin'
assert sha(image)==baseline['image_sha256']
tag='C5/optimized/pilot';directory=ROOT/'artifacts'/tag;result=directory/'simulation.json';budget=directory/'resources.json'
run(tag+'/run',['python3',ROOT/'C/runtime/budget_exec.py','--report',budget,'--',exe,'--flash',image,'--ref',ref,'--report',result,'--coverage-base','0x80000000','--coverage-size','65536','--max-cycles','100000000'],inputs=[exe,image,ref],outputs=[result,budget],timeout=180)
data=json.loads(result.read_text());old=baseline['simulation'];fields=['result','exit_code','pc','next_pc','instruction','a0','fault','cycles','instructions','mrom_dpi_calls','flash_dpi_calls','memory_operations','diff_checked','device_sync_checked','axi_channels','gpr','coverage','uart','retired_by_region','psram']
for field in fields:assert data[field]==old[field],field
assert all(c['read_bytes']==c['write_bytes']==0 for c in data['sdram_chips'])
dump(ROOT/'reports/C5_optimized.json',{'status':'PASS_IDENTICAL_PSRAM_PILOT_OBSERVATIONS','variant':name,'image_sha256':sha(image),'baseline_evidence':baseline['evidence'],'evidence':'artifacts/'+tag,'equal_fields':fields,'old_wall_seconds':old['wall_seconds'],'new_wall_seconds':data['wall_seconds'],'wall_speed_ratio':old['wall_seconds']/data['wall_seconds'],'scope':'Same64KiB firmware, exact cycles/instructions/GPR/memory coverage/PSRAM/UART comparisons against retained earlier run. Explicit GNU C++OPT_FAST/OPT_SLOW/OPT_GLOBAL=-O3; includes newly implemented but unused SDRAM/GPIO/PS2/VGA. All per-instruction reference checks preserved. Full peripheral acceptance is separate.'})
print('C5_OPTIMIZED_PILOT_PASS',old['wall_seconds'],data['wall_seconds'],flush=True)
