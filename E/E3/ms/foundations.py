from common import *
import zipfile,re,collections,statistics,decimal,glob
def main():
    m=Path('/tmp/missing')
    if m.exists():assert (m/'.ysyx-lab').exists(),'Preserve unrelated /tmp/missing'
    m.mkdir(exist_ok=True);(m/'.ysyx-lab').touch()
    o,e,r=shell('shell/setup',"""set -eu
echo "$SHELL"
test "$SHELL" = /bin/bash
cd /tmp/missing
touch semester
printf '%s\n' '#!/bin/sh' 'curl --head --silent https://missing.csail.mit.edu' > semester
chmod 644 semester
ls -l semester
""");assert '/bin/bash' in o
    o,e,r=run('shell/no_execute',['/bin/bash','-c','./semester'],cwd=m,expected=(126,));assert 'Permission denied' in e
    for cmd in ('touch','chmod'):run('shell/man_'+cmd,['man','-P','cat',cmd])
    o,e,r=shell('shell/execute_header',"""set -eu
cd /tmp/missing
chmod u+x semester
./semester | tee headers.txt | tr -d '\\r' | grep -i '^last-modified:' > /home/USER/last-modified.txt
cat /home/USER/last-modified.txt
""",timeout=60);assert 'last-modified:' in o.lower()
    record([f'MS-01-{i:02}' for i in range(1,10)],'PASS',['shell/setup','shell/no_execute','shell/execute_header'],'Real Bash, permission rejection, executable shebang script and actual HTTP Last-Modified header.')
    sensors=[{'path':p,'value':Path(p).read_text().strip()} for p in glob.glob('/sys/class/power_supply/*/capacity')+glob.glob('/sys/class/thermal/thermal_zone*/temp')]
    dump(OUT/'shell/sysfs_probe.json',{'sensors':sensors,'platform':os.uname().release})
    record(['MS-01-10'],'PASS' if sensors else 'UNAVAILABLE_VM_HARDWARE',['shell/sysfs_probe.json'],'Actual sysfs probe; no physical reading invented.')
    tree=LAB/'find-fixture';tree.mkdir(exist_ok=True)
    names=['a.html','space name.html','line\nbreak.html','nested/-lead.html','ignore.txt']
    for i,name in enumerate(names):
        p=tree/name;p.parent.mkdir(exist_ok=True);p.write_text(name);os.utime(p,(100+i,100+i))
    (tree/'.hidden').write_text('hidden');(tree/'large.bin').write_bytes(b'x'*1150000)
    run('scripts/man_ls',['man','-P','cat','ls'])
    o,e,r=run('scripts/ls',['ls','-alth','--color=always',str(tree)]);assert '.hidden' in o and '\x1b[' in o and '1.1M' in o
    record(['MS-02-01'],'PASS',['scripts/ls','scripts/man_ls'],'Actual hidden file, colors, mtime order and human-readable size.')
    marco=LAB/'marco.sh';marco.write_text('marco(){ MARCO_DIR=$PWD; }\npolo(){ [[ -v MARCO_DIR ]] && cd -- "$MARCO_DIR"; }\n')
    o,e,r=shell('scripts/marco',f'''set -eu
source {shlex.quote(str(marco))}
mkdir -p "{LAB}/space directory"
cd "{LAB}/space directory"
marco
cd /
polo
test "$PWD" = "{LAB}/space directory"
printf '%s\\n' "$PWD"
''')
    record(['MS-02-02'],'PASS',['scripts/marco',str(marco)],'Returned to exact saved path including spaces.')
    rare=LAB/'rare.sh';rare.write_text('''#!/usr/bin/env bash
n=$(( RANDOM % 100 ))
if [[ n -eq 42 ]]; then
 echo "Something went wrong"
 >&2 echo "The error was using magic numbers"
 exit 1
fi
echo "Everything went according to plan"
''')
    o,e,r=shell('scripts/until_failure',f'''set -u
: > rare.stdout
: > rare.stderr
for ((attempt=1;attempt<=10000;attempt++)); do
 if bash {shlex.quote(str(rare))} >>rare.stdout 2>>rare.stderr; then :; else
  printf 'attempts=%d\\n' "$attempt"
  cat rare.stdout
  cat rare.stderr >&2
  exit 0
 fi
done
exit 2
''',timeout=60);assert 'Something went wrong' in o and 'The error was using magic numbers' in e
    record(['MS-02-03'],'PASS',['scripts/until_failure',str(rare)],'Original RANDOM script really failed; both streams and attempt count retained. Reaching the resource cap is not success.')
    target=LAB/'html-files.zip'
    if target.exists():target.unlink() # Only our generated archive, not input data.
    shell('scripts/html_zip',f'cd {shlex.quote(str(tree))}\nfind . -type f -name "*.html" -print0 | xargs -0 -r zip {shlex.quote(str(target))}\n')
    with zipfile.ZipFile(target) as z:assert sorted(z.namelist())==sorted(x for x in names if x.endswith('.html'));assert z.testzip() is None
    record(['MS-02-04'],'PASS',['scripts/html_zip',str(target)],'NUL-safe pipeline independently checked on spaces, newline and leading hyphen filenames.')
    shell('scripts/newest',f'find {shlex.quote(str(tree))} -type f -printf "%T@ %p\\\\0" | sort -z -nr')
    raw=(OUT/'scripts/newest/stdout.log').read_bytes().split(b'\0');actual=[x.split(b' ',1)[1].decode() for x in raw if x]
    expected=sorted((str(x) for x in tree.rglob('*') if x.is_file()),key=lambda s:(Path(s).stat().st_mtime,s),reverse=True);assert actual==expected
    record(['MS-02-05'],'PASS',['scripts/newest'],'NUL-delimited sorting checked against independent stat.')
    words=Path('/usr/share/dict/words')
    shell('data/words',r"""set -eu
tr '[:upper:]' '[:lower:]' < /usr/share/dict/words | grep 'a.*a.*a' | grep -v "'s$" > selected.words
wc -l selected.words
sed 's/.*\(..\)$/\1/' selected.words | sort | uniq -c | sort -k1,1nr -k2 > endings.txt
cat endings.txt
""")
    selected=[w.lower() for w in words.read_text().splitlines() if w.lower().count('a')>=3 and not w.lower().endswith("'s")]
    assert (LAB/'selected.words').read_text().splitlines()==selected
    counts=collections.Counter(w[-2:] for w in selected);expected=sorted(counts.items(),key=lambda x:(-x[1],x[0]))
    actual=[(line.split()[1],int(line.split()[0])) for line in (LAB/'endings.txt').read_text().splitlines()];assert actual==expected
    missing=sorted({a+b for a in 'abcdefghijklmnopqrstuvwxyz' for b in 'abcdefghijklmnopqrstuvwxyz'}-set(counts))
    dump(OUT/'data/words_analysis.json',{'word_list_sha256':sha(words),'matched':len(selected),'top3':expected[:3],'different_endings':len(counts),'missing_ascii_pairs':missing})
    record(['MS-04-02'],'PASS',['data/words','data/words_analysis.json'],'Actual dictionary, independent substring/count oracle, all absent ASCII pairs.')
    shell('data/truncation',"""set -eu
printf 'cat\\n' > truncation.txt
sed s/cat/dog/ truncation.txt > truncation.txt
test ! -s truncation.txt
printf 'cat\\n' > truncation.txt
sed -i s/cat/dog/ truncation.txt
test "$(cat truncation.txt)" = dog
man -P cat sed
""")
    record(['MS-04-03'],'PASS',['data/truncation'],'Actual shell redirection truncation and corrected sed -i, only within an isolated fixture.')
    o,e,r=run('data/journal_inventory',['journalctl','--list-boots'],expected=(0,1))
    dump(OUT/'data/boot_scope.json',{'stdout':o,'stderr':e,'pid1':Path('/proc/1/comm').read_text().strip(),'actual_boot_statistics':'UNAVAILABLE','reason':'New WSL with init; no qualifying systemd boot history.'})
    logs=[f'Startup finished in 250ms (kernel) + {n-.25}s (userspace) = {n}s.' for n in range(1,11)]
    extracted=[float(re.search(r'= ([0-9.]+)s',x)[1]) for x in logs];assert statistics.mean(extracted)==statistics.median(extracted)==5.5
    boots=[{'kernel ready','network ready','service A'},{'kernel ready','network ready','service B'},{'kernel ready','network ready','service A'}]
    differing=set.union(*boots)-set.intersection(*boots);assert differing=={'service A','service B'}
    dump(OUT/'data/boot_method_fixture.json',{'synthetic':True,'logs':logs,'mean':5.5,'median':5.5,'max':max(extracted),'noncommon_lines':sorted(differing)})
    record(['MS-04-04','MS-04-05'],'UNAVAILABLE_HISTORY_METHOD_TESTED',['data/journal_inventory','data/boot_scope.json','data/boot_method_fixture.json'],'Real history absent; fixture is labeled synthetic, never claimed as measured boots.')
    url='https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data';iris=LAB/'iris.data'
    run('data/iris_download',['curl','--fail','--location','--silent','--show-error','--max-time','45',url,'-o',str(iris)],timeout=50)
    rows=[x.split(',') for x in iris.read_text().splitlines() if x.strip()];assert len(rows)==150 and all(len(r)==5 for r in rows)
    o,e,r=shell('data/iris_minmax',"""awk -F, 'NF==5 {if(!n++||$1<min)min=$1;if(n==1||$1>max)max=$1} END{print min,max}' iris.data
""");assert list(map(decimal.Decimal,o.split()))==[min(decimal.Decimal(x[0]) for x in rows),max(decimal.Decimal(x[0]) for x in rows)]
    o,e,r=shell('data/iris_difference',"""awk -F, 'NF==5 {s+=$1-$2} END{printf "%.1f\\n",s}' iris.data
""");assert decimal.Decimal(o.strip())==sum(decimal.Decimal(x[0])-decimal.Decimal(x[1]) for x in rows)
    dump(OUT/'data/iris_source.json',{'url':url,'sha256':sha(iris),'rows':150,'columns':['sepal_length_cm','sepal_width_cm','petal_length_cm','petal_width_cm','class'],'citation':'Fisher,R.(1936). Iris. UCI. DOI10.24432/C56C76','license':'CC BY4.0'})
    record(['MS-04-06'],'PASS',['data/iris_download','data/iris_minmax','data/iris_difference','data/iris_source.json'],'Real curl download; awk results checked against Decimal on identical source bytes.')
    print('MS_FOUNDATIONS_DONE',flush=True)
if __name__=='__main__':main()
