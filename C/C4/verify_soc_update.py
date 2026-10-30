"""Requalify only the SoC variant affected by Xbar buffering and AM calibration."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
jobs = [('build_sim.py', '--modes', '6'),
        ('build_sim.py', '--modes', '6', '--mutant'),
        ('run_front.py', '--modes', '6'),
        ('regression.py', '--modes', '6'),
        ('verify_negative_sdb.py',),
        ('calibrate_clock.py',)]
for script, *args in jobs:
    subprocess.run([sys.executable, str(ROOT / script), *args], check=True)
print('C4_SOC_UPDATE_REQUALIFIED', flush=True)
