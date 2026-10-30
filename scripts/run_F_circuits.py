from evidence import *
def main():
    cfg=json.loads((ROOT/'config/toolchain.json').read_text('utf8'));j=cfg['java']['executable'];jar=cfg['logisim']['jar'];classes=ROOT/'temp/java-classes';sources=list((ROOT/'scripts/java').glob('*.java'));cp=str(classes)+';'+jar
    q=run('F/compile_driver',[str(Path(j).with_name('javac.exe')),'-encoding','UTF-8','-cp',cp,'-d',classes,*sources],sources,timeout=40)
    if q['status']!='PASS':return 1
    data=json.loads((ROOT/'config/F_circuit_jobs.json').read_text('utf8'));jobs=data['jobs']
    batch='--batch' in sys.argv
    if len(sys.argv)>1 and not batch:jobs=[x for x in jobs if x['circuit'] in sys.argv[1:]]
    prefix=[j,'-Xmx512m','-Djava.awt.headless=true','-Dfile.encoding=UTF-8','-Duser.language=en','-Djava.util.prefs.PreferencesFactory=LocalPrefsFactory','-cp',cp,'CircuitRunner',data['circuit_file']]
    results=[]
    if batch:
        args=[part for job in jobs for part in (job['circuit'],job['vectors'])]
        q=run('F/fundamentals_final_batch',prefix+args,[Path(data['circuit_file'])]+[Path(job['vectors']) for job in jobs],timeout=180)
        text=(ROOT/'artifacts/F/fundamentals_final_batch/stdout.log').read_text('utf8')
        for job in jobs:
            ok=q['status']=='PASS' and f'RESULT {job["circuit"]} vectors={job["rows"]} failures=0' in text
            results.append({**job,'result':{**q,'status':'PASS' if ok else 'FAIL'}})
        dump(ROOT/'reports/F_circuit_results.json',{'status':'PASS' if all(x['result']['status']=='PASS' for x in results) else 'FAIL','jobs':results,'mode':'one-process native Logisim, immutable raw-byte loading, all input pre/post hashes checked','scope':'Actual native gate/display/sequence simulation only; no physical timing/analog metastability claim'})
        print('F_CIRCUIT_RESULT_BATCH',len(results),'jobs',sum(j['rows'] for j in jobs),'vectors; failures',[x['circuit'] for x in results if x['result']['status']!='PASS'],flush=True)
        return 0 if all(x['result']['status']=='PASS' for x in results) else 1
    for job in jobs:
        q=run('F/circuit_'+job['circuit'],prefix+[job['circuit'],job['vectors']],[Path(data['circuit_file']),Path(job['vectors'])],timeout=180)
        text=(ROOT/'artifacts/F'/('circuit_'+job['circuit'])/'stdout.log').read_text('utf8')
        expected=f'TOTAL vectors={job["rows"]} failures=0'
        if q['status']=='PASS' and expected not in text:q['status']='FAIL';q['reason']='Simulator output missing exact case count'
        results.append({**job,'result':q})
    dump(ROOT/'reports/F_circuit_results.json',{'status':'PASS' if results and all(x['result']['status']=='PASS' for x in results) else 'FAIL','jobs':results,'scope':'Actual Logisim 4.0.0 simulation; DUT circuits independently authored; arithmetic/truth-table reference values from integer formulas; no timing/physical-signoff claim'})
    print('F_CIRCUIT_RESULT',len(results),'jobs',sum(x['rows'] for x in results),'vectors; failures',[x['circuit'] for x in results if x['result']['status']!='PASS'],flush=True)
    return 0 if all(x['result']['status']=='PASS' for x in results) else 1
if __name__=='__main__':sys.exit(main())
