"""Serial E6 continuation; each child owns bounded, snapshotted evidence runs."""
from pathlib import Path
import sys,subprocess
p=Path(__file__).parent
for name in ['enable_devices.py','run_official_tests.py','diff_negative.py','synthesis.py','fceux_verify.py','performance.py']:
 print('E6_NEXT',name,flush=True)
 subprocess.run([sys.executable,str(p/name)],check=True)
