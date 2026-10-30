"""Compatibility entry point for the shared active C resource guard."""
from pathlib import Path
import runpy
import sys
runtime = Path(__file__).resolve().parents[2] / "runtime"
sys.path.insert(0, str(runtime))
if __name__ == "__main__":
    runpy.run_path(str(runtime / "budget_exec.py"), run_name="__main__")
