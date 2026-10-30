from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    p=ROOT/'D/D2';runtime=ROOT/'D/runtime';build=WORK/'D2';build.mkdir(exist_ok=True);out=p/'results';out.mkdir(exist_ok=True)
    env={'ASAN_OPTIONS':'detect_leaks=1:halt_on_error=1','UBSAN_OPTIONS':'halt_on_error=1','TMPDIR':str(build)}
    flags=['gcc','-D_POSIX_C_SOURCE=200809L','-std=c11','-O1','-g','-Wall','-Wextra','-Werror','-I'+str(runtime)]
    exe=build/'debug_unit'
    run('D2/expr/build',[*flags,'-fsanitize=address,undefined','-fno-omit-frame-pointer',runtime/'debug_core.c',p/'debug_unit.c','-o',exe],inputs=[runtime/'debug_core.c',runtime/'debug_core.h',p/'debug_unit.c'],outputs=[exe])
    run('D2/expr/unit',[exe],inputs=[exe],env=env)
    gen=build/'gen-expr';run('D2/expr/generator_build',[*flags,p/'gen_expr.c','-o',gen],inputs=[p/'gen_expr.c'],outputs=[gen])
    text,_,row=run('D2/expr/generate_10000',[gen,'10000','0x2607d2'],inputs=[gen],env=env,timeout=300)
    vectors=out/'expressions.txt';vectors.write_text(text);assert len(text.splitlines())==10000
    o,_,_=run('D2/expr/differential_10000',[exe,vectors],inputs=[exe,vectors],env=env,timeout=120);assert 'RANDOM_EXPRESSIONS_PASS 10000' in o
    mutant=build/'mutant.c';mutant.write_text((runtime/'debug_core.c').read_text().replace("case '+':lhs+=rhs;break;","case '+':lhs-=rhs;break;"))
    bad=build/'bad_debug';run('D2/expr/mutant_build',[*flags,mutant,p/'debug_unit.c','-o',bad],inputs=[mutant,p/'debug_unit.c',runtime/'debug_core.h'],outputs=[bad])
    run('D2/expr/mutant_rejected',[bad],inputs=[bad],expected=(-6,))
    dump(ROOT/'reports/D2_expression.json',{'status':'PASS','random_expressions':10000,'seed':'0x2607d2','oracle':'Actual GCC C11 uint32_t computations, batched 128 per compilation','unit_checks':['precedence','associativity','parentheses','decimal and hexadecimal','uint32 wraparound','negative/unary operators','register and memory callbacks','short circuit','invalid syntax','zero division','literal overflow','token and recursion bounds','32-slot pool exhaustion','delete/recycle/invariants','change detection only once'],'sanitizers':['AddressSanitizer','UndefinedBehaviorSanitizer'],'negative_control':'wrong addition becomes subtraction; same assertions abort','vectors_sha256':sha(vectors),'evidence':'artifacts/D2/expr'})
    print('D2_EXPRESSION_PASS',flush=True)

if __name__=='__main__':main()
