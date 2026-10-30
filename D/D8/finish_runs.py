"""Serial final-candidate runs after the allocator change; no parallel heavy jobs."""
from pathlib import Path
import subprocess,sys
d=Path(__file__).parent
jobs=[(d/'run_apps.py',['--mode','test']),(d/'run_apps.py',['--mode','train']),
      (d.parent/'D5/run_portable.py',[]),(d/'extra_tests.py',[]),
      (d/'fceux_verify.py',[]),(d/'native_keyboard.py',[]),
      (d/'run_official.py',[]),(d/'verify_front.py',[]),(d/'verify_isa.py',[]),
      (d.parent/'D7/regression.py',[]),(d/'alu_study.py',[])]
for script,args in jobs:
    print('FINAL_CANDIDATE_NEXT',script.name,*args,flush=True)
    subprocess.run([sys.executable,str(script),*args],check=True)
print('D_FINAL_CANDIDATE_RUNS_PASS',flush=True)
