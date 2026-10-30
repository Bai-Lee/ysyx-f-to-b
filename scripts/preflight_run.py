from evidence import *
def main():
    cfg=json.loads((ROOT/'config/toolchain.json').read_text('utf8'));jar=cfg['logisim']['jar'];classes=ROOT/'temp/java-classes';classes.mkdir(parents=True,exist_ok=True)
    java=cfg['java']['executable'];javac=str(Path(java).with_name('javac.exe'))
    sources=list((ROOT/'scripts/java').glob('*.java'))
    result=run('preflight/javac',[javac,'-encoding','UTF-8','-cp',jar,'-d',classes,*sources],sources)
    if result['status']!='PASS':return 1
    prefix=[java,'-Xmx512m','-Djava.awt.headless=true','-Duser.language=en','-Duser.country=US','-Dfile.encoding=UTF-8','-Djava.util.prefs.PreferencesFactory=LocalPrefsFactory','-cp',str(classes)+';'+jar,'CircuitRunner']
    circ=ROOT/'F/circuits/preflight.circ';good=ROOT/'F/vectors/preflight_good.txt';bad=ROOT/'F/vectors/preflight_bad.txt'
    q=run('preflight/logisim_positive',prefix+[circ,'control_and',good],[circ,good],timeout=45)
    n=run('preflight/logisim_negative',prefix+[circ,'control_and',bad],[circ,bad],timeout=45,expected=1)
    if q['status']!='PASS' or n['status']!='PASS':return 1
    if 'TOTAL vectors=4 failures=0' not in (ROOT/'artifacts/preflight/logisim_positive/stdout.log').read_text('utf8'):raise ValueError('Positive output malformed')
    if 'TOTAL vectors=4 failures=1' not in (ROOT/'artifacts/preflight/logisim_negative/stdout.log').read_text('utf8'):raise ValueError('Negative control did not reject exactly one incorrect expected value')
    data=json.loads((ROOT/'reports/preflight_F.json').read_text('utf8'));data.update(status='PASS',controls=[q,n],limits_note='Digital Logisim control only; no physical timing or analog metastability claim');dump(ROOT/'reports/preflight_F.json',data)
    return 0
if __name__=='__main__':sys.exit(main())
