"""Exact build identities for C5's independently recorded hardware profiles."""
from pathlib import Path
import json,hashlib
ROOT=Path('/workspace/projects/ysyx_f_to_b')
def variant_name(row):
    if 'variant' in row:return row['variant']
    return f"{row['reset_pc']:08x}"+('-fast' if row.get('fast_flash',False) else '')+('-cycle' if row.get('cycle_sim',False) else '')+('-psram4m' if row.get('psram_bytes',4096)==4194304 else '')+('-qpi' if row.get('psram_qpi',False) else '')+('-mutant' if row.get('mutant',False) else '')+(f"-sdram{row['sdram_width']}x{row.get('sdram_ranks',1)}" if row.get('sdram_width',0) else '')+('-opt' if row.get('optimized',False) else '')+('-gui' if row.get('nvboard',False) else '')+('-ps2log' if row.get('ps2_observe',False) else '')+('-chiplink' if row.get('chiplink',False) else '')+('-bad-read' if row.get('chiplink_corrupt',False) else '')
def select_build(name):
    rows=json.loads((ROOT/'reports/B_soc_soc_build.json').read_text())['variants']
    matches=[r for r in rows if variant_name(r)==name];assert len(matches)==1,(name,[variant_name(r) for r in rows])
    row=matches[0];assert hashlib.sha256(Path(row['executable']).read_bytes()).hexdigest()==row['sha256']
    return row
