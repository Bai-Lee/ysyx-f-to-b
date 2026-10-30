"""Select the measured area-compliant RTL, preserving faster rejected trials."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    origin=ROOT/'artifacts/B3/synthesis/b4-compact-cpu';record=json.loads((origin/'run.json').read_text());assert record['status']=='PASS'
    after={r['path']:r['sha256'] for r in record['inputs_after']};names={'ysyx_00000000_pipe.sv','ysyx_00000000_icache.sv'};rows=[]
    with zipfile.ZipFile(origin/'input_snapshot.zip') as z:
        for i,item in enumerate(record['inputs']):
            name=Path(item['path']).name
            if name not in names:continue
            assert after[item['path']]==item['sha256'];content=z.read(f'{i:03d}_{name}');assert hashlib.sha256(content).hexdigest()==item['sha256']
            target=ROOT/'B/soc/rtl'/name;before=sha(target);target.write_bytes(content);rows.append({'path':str(target.relative_to(ROOT)),'before_sha256':before,'selected_sha256':sha(target)})
    assert {Path(r['path']).name for r in rows}==names
    synthesis=next(r for r in json.loads((ROOT/'reports/B3_synthesis.json').read_text())['variants'] if r['name']=='b4-compact-cpu')
    assert synthesis['area_um2']<=25000 and synthesis['setup_frequency_estimate_mhz']>=350 and synthesis['max_transition_violations']==0 and synthesis['hold_slack_ns']>=0
    (ROOT/'reports/B_final_selection.json').write_text(json.dumps({'status':'SELECTED_PENDING_FINAL_REGRESSIONS','rtl':rows,'synthesis':synthesis,'soc_variant':'b4-final','standalone_variant':'pipeline-compact','model_frequency_mhz':350,'apb_ratio_q':896,'axi_ratio_q':896,'padding':24,'netlist':'B/B3/synthesis/b4-compact-cpu/mapped.v','reason':'Measured24918.082um2 with no transition violation meets the25000um2 limit. Faster address-path and reset experiments exceed it; their logs/netlists remain as rejected design-space points. No initial architectural state or assertions were weakened to meet the limit.'},indent=2),encoding='utf8')
    print('B_RELEASE_SELECTED',synthesis['area_um2'])
if __name__=='__main__':main()
