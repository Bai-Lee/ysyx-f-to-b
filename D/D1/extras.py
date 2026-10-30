from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
import re

def main():
    p=ROOT/'D/D1';out=p/'results';src=p/'src'
    limits=src/'limits.c';limits.write_text('#include <limits.h>\n#include <stdio.h>\nint main(void){printf("CHAR_BIT=%d INT_MIN=%d INT_MAX=%d UINT_MAX=%u LLONG_MAX=%lld\\n",CHAR_BIT,INT_MIN,INT_MAX,UINT_MAX,LLONG_MAX);return 0;}\n')
    exe=WORK/'D1/limits';run('D1/extras/limits_build',['gcc','-Wall','-Wextra','-Werror',limits,'-o',exe],inputs=[limits],outputs=[exe])
    text,_,_=run('D1/extras/limits',[exe],inputs=[exe]);assert 'CHAR_BIT=8' in text and 'INT_MAX=2147483647' in text
    source=src/'visibility.c';source.write_text('int public_add(int x){return x+3;}\nstatic int local_add(int x){return x+3;}\nint caller(int x){return public_add(x)+local_add(x);}\n')
    obj=out/'visibility.o';run('D1/extras/visibility_build',['gcc','-O2','-c',source,'-o',obj],inputs=[source],outputs=[obj])
    syms,_,_=run('D1/extras/visibility_symbols',['nm',obj],inputs=[obj]);assert 'public_add' in syms and 'local_add' not in syms
    fixture=src/'color.c';fixture.write_text('/* int keyword inside comment */\nint value=42; // return value\nconst char *s="int // string \\\"quote\\\"";\n')
    colored,_,_=run('D1/extras/colorizer',['python3',p/'colorize.py',fixture],inputs=[p/'colorize.py',fixture]);assert re.sub(r'\x1b\[[0-9;]*m','',colored)==fixture.read_text()
    assert '\x1b[90m/* int keyword inside comment */' in colored and '\x1b[34mint\x1b[0m' in colored and '\x1b[36mvalue\x1b[0m' in colored and '\x1b[32m"int // string' in colored
    dump(ROOT/'reports/D1_background.json',{'status':'PASS_BACKGROUND_REVIEW','limits_output':text.strip(),'visibility_symbols':syms.strip(),'highlighter':'Comments, strings, identifiers, keywords and numbers receive distinct ANSI colors; stripping ANSI restores the exact fixture bytes. A small lexical exercise, not a complete C lexer or editor.','evidence':['artifacts/D1/extras','artifacts/D1/clang_tokens','D/D1/NOTES.md'],'scope':'Small implementations, observations and source-based answers; no claim of a complete syntax-highlighting editor or complete compiler implementation.'})
    mark([f'D1-O{i:03d}' for i in range(1,9)]+[f'D1-R{i:03d}' for i in range(1,4)],'PASS_BACKGROUND_REVIEW',['reports/D1_background.json','D/D1/NOTES.md'],'Review tied to real token/AST/lint, integer-limit and symbol-visibility evidence; source errors identified explicitly.')

if __name__=='__main__':main()
