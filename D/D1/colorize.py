"""Small C lexical highlighter for the course exercise, not a C preprocessor."""
import re,sys
from pathlib import Path
PATTERN=re.compile(r'(?P<comment>//[^\n]*|/\*[\s\S]*?\*/)|(?P<string>"(?:\\[\s\S]|[^"\\])*"|\'(?:\\[\s\S]|[^\'\\])*\')|(?P<identifier>[A-Za-z_]\w*)|(?P<number>\b(?:0[xX][0-9a-fA-F]+|[0-9]+)(?:[uUlL]*)\b)|(?P<other>[\s\S])')
KEYWORDS=set('auto break case char const continue default do double else enum extern float for goto if inline int long register restrict return short signed sizeof static struct switch typedef union unsigned void volatile while _Bool _Complex _Imaginary'.split())
COLORS={'comment':90,'string':32,'keyword':34,'identifier':36,'number':35}
def tokens(source):
    for match in PATTERN.finditer(source):
        text=match.group();kind=match.lastgroup
        if kind=='identifier' and text in KEYWORDS:kind='keyword'
        yield kind,text
def colorize(source):
    return ''.join(f'\x1b[{COLORS[k]}m{s}\x1b[0m' if k in COLORS else s for k,s in tokens(source))
if __name__=='__main__':sys.stdout.write(colorize(Path(sys.argv[1]).read_text()))
