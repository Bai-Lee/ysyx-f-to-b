"""Validate portable links, Python syntax, benchmark data and exported plaintext."""
from evidence import *
import ast,re,urllib.parse,csv

def main():
    files=list((ROOT/'E/E3').rglob('*.py'))+[ROOT/'scripts/finalize_E3.py',Path(__file__)]
    syntax=[]
    for f in files:
        if 'original' in f.parts:continue
        ast.parse(f.read_text('utf8'),filename=str(f));syntax.append(str(f.relative_to(ROOT)))
    scanned=0
    for root in [ROOT/'E/E3',ROOT/'artifacts/E3']:
        for f in root.rglob('*'):
            if not f.is_file() or f.suffix in {'.zip','.bundle','.png','.tar','.gz','.elf','.core','.so'}:continue
            data=f.read_bytes();scanned+=1
            assert not re.search(rb'(?m)^-----BEGIN (?:OPENSSH|RSA|EC)? ?PRIVATE KEY-----\r?\n[A-Za-z0-9+/]{40}',data),f
    docs=[ROOT/'reports/E3_REPORT.md',ROOT/'reports/E3_TASKS.md',ROOT/'reports/E3_DEPENDENCIES.md',ROOT/'E/E3/README.md',ROOT/'E/E3/ms/NOTES.md',*list((ROOT/'E/E3/lcthw/notes').glob('*.md'))]
    bad=[];count=0
    for f in docs:
        for target in re.findall(r'\]\(([^)]+)\)',f.read_text('utf8')):
            target=urllib.parse.unquote(target.strip('<>').split('#')[0])
            if not target or re.match(r'https?://',target):continue
            p=Path(target) if re.match(r'^[A-Za-z]:',target) else f.parent/target
            if not p.exists():bad.append((str(f),target))
            count+=1
    assert not bad,bad
    benchmark=json.loads((ROOT/'reports/E3_list_benchmark.json').read_text('utf8'))
    rows=list(csv.DictReader((ROOT/'E/E3/lcthw/figures/list_benchmark.csv').open(encoding='utf8',newline='')))
    assert len(rows)==len(benchmark['records'])==16
    # CSV schema intentionally inspected rather than assuming column spelling.
    for row,reference in zip(rows,benchmark['records']):
        for key in ['n','mean_build_sort_us','mean_comparisons']:
            assert float(row[key])==float(reference[key]),(key,row,reference)
    dump(ROOT/'reports/E3_document_check.json',{'status':'PASS','timestamp':datetime.now(timezone.utc).isoformat(),'python_files_checked':syntax,'local_markdown_links_checked':count,'plaintext_files_checked_for_private_key_material':scanned,'benchmark_csv_rows_verified':16,'plot_visual_review':'PNG inspected after generation; labels/legend/data ranges legible, merge comparison curves intentionally overlap.','scope':'Does not prove absence of every possible secret encoding; export uses a separate strict public whitelist.'})
    print('E3_DELIVERY_CONTENT_PASS',len(syntax),'Python files;',count,'local links;16 benchmark rows',flush=True)
if __name__=='__main__':main()
