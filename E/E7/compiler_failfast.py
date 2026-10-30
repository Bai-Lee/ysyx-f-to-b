from common7 import *
from software_soc import SOFT,environment
def main():
 am=SOFT/'abstract-machine';wrapper=am/'tools/minirv/minirv-common.sh';old=wrapper.read_text();save=ROOT/'E/E7/upstream/minirv-common.before-failfast.sh'
 if not save.exists():save.write_text(old)
 if 'set -euo pipefail' not in old:wrapper.write_text(old.replace('#!/bin/bash','#!/bin/bash\nset -euo pipefail',1))
 d=SOFT/'compiler_probe';d.mkdir(exist_ok=True);source=d/'bad.c';source.write_text('#error intentional_failfast_probe\n');output=d/'bad.o';assert not output.exists()
 compiler=am/'tools/minirv/minirv-gcc'
 o,e,r=run('E7/compiler_failfast/negative',[compiler,'-march=rv32e_zicsr','-mabi=ilp32e','-c','-o',output,source],cwd=d,env={**environment(),'PATH':str(am/'tools/minirv')+':'+os.environ['PATH']},inputs=[wrapper,source],expected=(1,));assert not output.exists() and 'intentional_failfast_probe' in e
 dump(ROOT/'reports/E7_compiler_failfast.json',{'status':'PASS_EXPECTED_REJECTION','wrapper':str(wrapper),'sha256':sha(wrapper),'reason':'Original wrapper continued after compiler errors and its finaldd could create a40byte bogusobject andreturn0. IsolatedSoCcopy nowusesfailfast; invalidC returnsnonzero andcreatesnoobject. E6/activeE7standaloneworkbench untouched.'})
 print('SOC_COMPILER_FAILFAST_PASS',flush=True)
if __name__=='__main__':main()
