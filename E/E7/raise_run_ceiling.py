"""Raise only an instruction-cycle watchdog, preserving binaries and checks."""
from common7 import *
def main():
 mf=BENCH7/'npc/Makefile';before=mf.read_text();after=before.replace(' $(NPC_ARGS)\n',' --max-cycles 100000000000 $(NPC_ARGS)\n')
 if '--max-cycles 100000000000' in before:after=before
 assert after.count('--max-cycles 100000000000')==2
 backup=ROOT/'E/E7/upstream/NPC_before_watchdog_change.Makefile'
 if not backup.exists():backup.write_text(before)
 temp=mf.with_suffix('.tmp');temp.write_text(after);os.replace(temp,mf)
 shutil.copyfile(mf,ROOT/'E/E7/runtime_patch/NPC.Makefile')
 dump(ROOT/'reports/E7_watchdog_budget.json',{'status':'UPDATED_LIMIT_ONLY','old_default_cycles':10000000000,'new_cycles':100000000000,'per_program_wall_timeout_seconds':7200,'reason':'E6 llama2 train executes about4.0billioninstructions; multicycleLSU can legitimately exceed10billioncycles. No workload, validator, RTL, simulator executable or DiffTest setting changes. Explicit laterNPC_ARGS can still select a lower limit.','before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':sha(mf)})
 print('CYCLE_CEILING_UPDATED_NO_BINARY_CHANGE',flush=True)
if __name__=='__main__':main()
