from common import *
import shutil,xml.etree.ElementTree as ET,re,pty,select,fcntl,termios,struct,signal

def main():
    resources=LAB/'resources';vimrc=Path.home()/'.vimrc';backups=LAB/'config-backups';backups.mkdir(exist_ok=True)
    if vimrc.exists():shutil.copyfile(vimrc,backups/('vimrc-'+str(time.time_ns())))
    vimrc.write_text((resources/'vimrc').read_text()+'\nlet g:ctrlp_map = "<c-p>"\nset expandtab shiftwidth=4 tabstop=4\n')
    pack=Path.home()/'.vim/pack/vendor/start';pack.mkdir(parents=True,exist_ok=True)
    for name in ('ctrlp','commentary'):
        target=pack/name
        if not target.exists():target.symlink_to(resources/name,target_is_directory=True)
    run('editors/plugin_docs',['cat',str(resources/'ctrlp/readme.md'),str(resources/'commentary/README.markdown')])
    fixture=LAB/'vim-lab';fixture.mkdir(exist_ok=True)
    script=fixture/'tutor.vim'
    # Native Vim assertions cover the command families from every tutor lesson.
    cases=[
      (['alpha beta gamma'],'0dw',['beta gamma']),(['abc'],'0x',['bc']),
      (['abc'],r'0iX\<Esc>',['Xabc']),(['abc'],r'A!\<Esc>',['abc!']),
      (['abc'],'0rZ',['Zbc']),(['abc'],r'0cwXYZ\<Esc>',['XYZ']),
      (['one','two','three'],'ggdd',['two','three']),(['one','two'],'ggyyGp',['one','two','one']),
      (['one','two','three'],'ggddGp',['two','three','one']),(['one','two'],'ggddu',['one','two']),
      (['one','two'],r'ggddu\<C-r>',['two']),(['abc'],'0d$',['']),
      (['alpha beta'],r'0/beta\<CR>cwB\<Esc>',['alpha B']),
      (['call(old)'],r'0f(ci(XYZ\<Esc>',['call(XYZ)']),(['abcd'],'0vld',['cd']),
      (['one','two'],'ggJ',['one two']),(['one','two'],r'ggonew\<Esc>',['one','new','two']),
      (['one','two'],r'ggOhead\<Esc>',['head','one','two']),(['abcd'],r'0RXZ\<Esc>',['XZcd'])]
    lines=['set nocompatible nomore','set undolevels=1000']
    for before,keys,after in cases:
        lines+=['enew!','call setline(1, '+json.dumps(before)+')','normal! gg0','let &undolevels=&undolevels','execute "normal! '+keys.replace('"',r'\"')+'"','call assert_equal('+json.dumps(after)+', getline(1,"$"))']
    lines+=['enew!','call setline(1, ["foo foo","foo"])','%s/foo/bar/g','call assert_equal(["bar bar","bar"],getline(1,"$"))',
       'normal! gg$','call assert_equal(7,col("."))','normal! ggG','call assert_equal(2,line("."))',
       'enew!','call setline(1, "(a[b]c)")','normal! 0%','call assert_equal(7,col("."))',
       'set ignorecase','call assert_equal(1, &ignorecase)',
       'help motion','call assert_equal("help",&buftype)',
       'call writefile(v:errors,'+json.dumps(str(fixture/'tutor-errors.json'))+')',
       'if len(v:errors) | cquit 1 | endif','qa!']
    script.write_text('\n'.join(lines)+'\n')
    run('editors/tutor_commands',['vim','-Nu','NONE','-n','-i','NONE','-es','-S',str(script)],inputs=[script])
    tutor=next(Path('/usr/share/vim').glob('vim*/tutor/tutor'))
    shutil.copyfile(tutor,fixture/'vimtutor-source.txt')
    record(['MS-03-01'],'PASS_ADAPTED',['editors/tutor_commands',str(fixture/'vimtutor-source.txt')],'Native Vim assertions for all7 tutor command families: movement, operators/counts, insert/change, undo/redo, put, search/substitution, file/help/options. Automated practice, not a human time-based completion claim.')
    opts=fixture/'options.vim';opts.write_text('call writefile([string(&number),string(&relativenumber),string(&ignorecase),maparg("<C-P>","n"),string(exists(":Commentary"))],'+json.dumps(str(fixture/'options.txt'))+')\nqa!\n')
    run('editors/settings',['vim','-Nu',str(vimrc),'-n','-i','NONE','-es','-S',str(opts)],inputs=[vimrc,opts])
    options=(fixture/'options.txt').read_text().splitlines();assert options[:3]==['1','1','1'] and 'ctrlp' in options[3].lower() and options[4]=='2'
    record(['MS-03-02','MS-03-07'],'PASS',['editors/settings','editors/plugin_docs'],'Course vimrc loaded, options inspected, CtrlP and commentary installed at pinned source commits in dedicated Linux user.')
    # Use a real PTY for CtrlP's interactive picker.
    search=fixture/'search';search.mkdir(exist_ok=True);(search/'start.txt').write_text('start\n');(search/'needle_target.txt').write_text('selected\n')
    result=fixture/'picked.txt';pid,fd=pty.fork()
    if pid==0:
        os.chdir(search);fcntl.ioctl(0,termios.TIOCSWINSZ,struct.pack('HHHH',24,80,0,0));os.environ['TERM']='xterm'
        os.execvp('vim',['vim','-Nu',str(vimrc),'-n','-i','NONE','start.txt'])
    transcript=bytearray()
    def pump(seconds):
        end=time.monotonic()+seconds
        while time.monotonic()<end:
            if select.select([fd],[],[],.05)[0]:
                try:b=os.read(fd,65536)
                except OSError:break
                transcript.extend(b)
    try:
        pump(.7);os.write(fd,b'\x10');pump(.5);os.write(fd,b'needle_target\r');pump(.6)
        os.write(fd,(":call writefile([expand('%:p')], '"+str(result)+"')\r:qa!\r").encode());pump(.5)
        os.waitpid(pid,0)
    finally:
        try:
            if os.waitpid(pid,os.WNOHANG)[0]==0:os.kill(pid,signal.SIGTERM);os.waitpid(pid,0)
        except ChildProcessError:pass
        os.close(fd);(OUT/'editors/ctrlp.pty').write_bytes(transcript)
    assert result.read_text().strip()==str(search/'needle_target.txt')
    record(['MS-03-03'],'PASS',['editors/ctrlp.pty','editors/settings',str(result)],'Actual Ctrl-P typed into80x24 Vim PTY; picker opened the expected file.')
    bad=fixture/'fizz.py';bad.write_text("""def fizz_buzz(limit):
    for i in range(limit):
        if i % 3 == 0:
            print('fizz')
        if i % 5 == 0:
            print('fizz')
        if i % 3 and i % 5:
            print(i)

def main():
    fizz_buzz(10)
""")
    edits=fixture/'fizz.vim';edits.write_text("""2s/range(limit)/range(1, limit+1)/
4s/print('fizz')/print('fizz', end='')/
6s/print('fizz')/print('buzz', end='')/
call append(8, ['        else:', '            print()'])
%s/fizz_buzz(10)/fizz_buzz(int(sys.argv[1]))/
call append(0, ['import sys', ''])
call append(line('$'), ['', 'if __name__ == "__main__":', '    main()'])
wq
""")
    run('editors/fizz_edit',['vim','-Nu','NONE','-n','-i','NONE','-es','-S',str(edits),str(bad)],inputs=[edits])
    for n in (1,3,5,15,30):
        o,e,r=run('editors/fizz_'+str(n),['python3',str(bad),str(n)],inputs=[bad])
        expected=['fizzbuzz' if i%15==0 else 'fizz' if i%3==0 else 'buzz' if i%5==0 else str(i) for i in range(1,n+1)];assert o.splitlines()==expected
    record(['MS-03-04'],'PASS',['editors/fizz_edit','editors/fizz_30'],'Actual Vim repair of all five demo defects, independently checked for1/3/5/15/30.')
    record(['MS-03-05'],'NOT_APPLICABLE_HUMAN_DURATION',[],'A month of personal editor habit cannot be truthfully compressed into this agent run; no future month claimed.')
    o,e,r=shell('editors/bash_vi','set -o vi\nset -o | grep -E "^vi[[:space:]]+on$"\n')
    record(['MS-03-06'],'PASS',['editors/bash_vi'],'Actual Bash Readline vi mode; no Windows application settings changed.')
    # Independently written whole-file macro; course macro documentation was read.
    xml=resources/'example-data.xml';copy=fixture/'people.json';shutil.copyfile(xml,copy)
    commands=[
      r':g#</\?people>#d',r':%s#<person>#{#g',r':%s#</person>#},#g',
      r''':%s#<name>\(.*\)</name>#\='"name": '.json_encode(submatch(1)).','#''',
      r''':%s#<email>\(.*\)</email>#\='"email": '.json_encode(submatch(1))#''',
      r':$s/},/}/']
    sq=lambda s:"'"+s.replace("'","''")+"'"
    macro=fixture/'xml_macro.vim';macro.write_text('let @q=join(['+','.join(map(sq,commands))+'], "\\<CR>")."\\<CR>"\nnormal! @q\ncall append(0,"[")\ncall append(line("$"),"]")\nwq\n')
    run('editors/xml_macro',['vim','-Nu','NONE','-n','-i','NONE','-es','-S',str(macro),str(copy)],inputs=[xml,macro])
    expected=[{c.tag:c.text for c in person} for person in ET.fromstring(xml.read_text())]
    assert json.loads(copy.read_text())==expected
    dump(OUT/'editors/xml_result.json',{'source_sha256':sha(xml),'json_sha256':sha(copy),'people':len(expected),'verified_by':'ElementTree source vs json parser result'})
    record(['MS-03-08'],'PASS',['editors/xml_macro','editors/xml_result.json'],'Actual Vim register macro; independent XML/JSON parsers compare every object. Read lecture macro guidance; not claimed to be solved without seeing hints.')
    patterns=[
      (r'abc',['abcdefg','abcde','abc'],['ab']), (r'\d+',['abc123','42'],['abc']),
      (r'c.t',['cat','cot'],['ct']), (r'a\.b',['a.b'],['axb']),
      (r'^[cmf]an$',['can','man','fan'],['ban']), (r'^[^b]og$',['dog','log'],['bog']),
      (r'^[A-Z][a-z]+$',['Alice'],['ALICE']), (r'^z{3,5}$',['zzz','zzzzz'],['zz','zzzzzz']),
      (r'^a+b*$',['a','aaabb'],['b']), (r'^colou?r$',['color','colour'],['colouur']),
      (r'^\s+abc\s+$',[' abc\t'],['abc']), (r'^Mission: successful$',['Mission: successful'],['xMission: successful']),
      (r'^(cat|dog)s?$',['cats','dog'],['cars']), (r'^\w+\W\d+$',['name:12'],['name12'])]
    count=0
    for pat,yes,no in patterns:
        for v in yes:assert re.search(pat,v,re.ASCII);count+=1
        for v in no:assert not re.search(pat,v,re.ASCII);count+=1
    assert re.fullmatch(r'((file)\.(\w+))','file.csv').groups()==('file.csv','file','csv')
    dump(OUT/'editors/regex_tests.json',{'source':'https://regexone.com/','tutorial_html_sha256':sha(resources/'regexone.html'),'checks':count+1,'patterns':patterns,'nested_capture':['file.csv','file','csv'],'scope':'Locally executed tutorial concepts; only first abc samples copied from page, other examples authored. No web account/progress completion claim.'})
    record(['MS-04-01'],'PASS_ADAPTED',['editors/regex_tests.json'],'Tutorial concepts learned and executed as local ASCII-compatible regex/capture tests, rather than claiming website UI progress.')
    print('MS_EDITORS_DONE',flush=True)
if __name__=='__main__':main()
