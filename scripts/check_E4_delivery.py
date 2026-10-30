from evidence import *
import ast,re,urllib.parse
def main():
    files=list((ROOT/'E/E4').rglob('*.py'))+[ROOT/'scripts'/n for n in ['finalize_E4.py','check_E4_delivery.py','check_E4_visual.py','check_E4_structure.py']]
    for f in files:ast.parse(f.read_text('utf8'),filename=str(f))
    docs=[ROOT/'reports/E4_REPORT.md',ROOT/'reports/E4_TASKS.md',ROOT/'E/E4/README.md',ROOT/'E/E4/NOTES.md',ROOT/'E/E4/sources/README.md']
    bad=[];count=0
    for f in docs:
        for x in re.findall(r'\]\(([^)]+)\)',f.read_text('utf8')):
            target=urllib.parse.unquote(x.split('#')[0].strip('<>'))
            if not target or target.startswith(('https://','http://')):continue
            p=Path(target) if re.match(r'^[A-Za-z]:',target) else f.parent/target
            count+=1
            if not p.exists():bad.append((str(f),target))
    assert not bad,bad
    audit=json.loads((ROOT/'reports/E4_AUDIT.json').read_text('utf8'));assert audit['core_tasks_passed']==17 and not audit['missing_required_items']
    dump(ROOT/'reports/E4_document_check.json',{'status':'PASS','python_sources_parsed':len(files),'authored_document_local_links_verified':count,'scope':'Authored deliverables and source index; unchanged third-party raw Markdown retains original relative-link context in the full archive.'})
    print('E4_CONTENT_CHECK_PASS',len(files),'Python files;',count,'local links',flush=True)
if __name__=='__main__':main()
