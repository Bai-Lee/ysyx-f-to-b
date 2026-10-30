"""Complete documentation-based items and retain real manual lookups."""
from native import *

def main():
    for name in ('isalpha','isblank','isdigit'):
        o,e,r=run('manual/'+name,['man','-P','cat','3',name]);assert name in o
    notes=PROJECT/'E/E3/lcthw/notes/10-33.md'
    cards=PROJECT/'E/E3/lcthw/notes/21-flashcards.md'
    assert notes.exists() and cards.exists()
    verdict(['LCT-14-X04'],'PASS_DOCUMENTED',['E/E3/lcthw/notes/10-33.md'],'Compared primary GNU/Linux style documentation; distinguishes old K&R parameter definitions from brace style.')
    verdict(['LCT-32-X01','LCT-32-X02','LCT-33-X04'],'PASS_DOCUMENTED',['E/E3/lcthw/notes/10-33.md','list_properties'],'Explained singly/doubly linked list time/space/cache tradeoffs, required predecessor, ownership and sorting constraints; connected to actual invariant and model tests.')
    b=json.loads((PROJECT/'reports/E3_list_benchmark.json').read_text())
    assert b['status']=='PASS' and len(b['records'])==16 and all(x['timed_seconds']>=3 for x in b['records'])
    for ext in ['png','svg','csv']:assert (PROJECT/('E/E3/lcthw/figures/list_benchmark.'+ext)).exists()
    verdict(['LCT-33-X03'],'PASS',['reports/E3_list_benchmark.json','E/E3/lcthw/figures/list_benchmark.png','E/E3/lcthw/figures/list_benchmark.svg','E/E3/lcthw/figures/list_benchmark.csv'],'Measured fixed-seed random lists at four lengths; generated and visually inspected plot, explained asymptotics and allocation costs, no confidence interval or global optimum claim.')
    verdict(['LCT-21-X03'],'MATERIAL_PREPARED_HUMAN_DURATION',['E/E3/lcthw/notes/21-flashcards.md','types'],'Actual flashcards provided; no claim of elapsed daily human practice.')
    verdict(['LCT-31-X02'],'PASS_DOCUMENTED',['E/E3/lcthw/notes/10-33.md','debugger'],'Official VS Code C/C++ documentation comparison, CLI GDB executed; GUI not runtime-tested.')
    p=PROJECT/'reports/E3_LCT_continued.json';d=json.loads(p.read_text())
    for row in d['records']:
        row['evidence']=['ex29/library' if s=='ex29_library' else s for s in row['evidence']]
        if row['id']=='LCT-14-X03':row['evidence']+=['manual/isalpha','manual/isblank','manual/isdigit']
    dump(p,d)
    print('SUPPLEMENT_COMPLETE',flush=True)

if __name__=='__main__':main()
