from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
d=ROOT/'D/D6/results';dot=Path('/home/USER/tools/e-stage/oss-20260821/oss-cad-suite/bin/dot')
for p in [*d.glob('*.dot'),*(d/'pdk').glob('*.dot')]:
    out=p.with_suffix('.png')
    run('D6/visual/'+p.stem,[dot,'-Tpng','-Gdpi=85',p,'-o',out],inputs=[p],outputs=[out])
