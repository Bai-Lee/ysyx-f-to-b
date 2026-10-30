"""Check prior F/E/D deliverables without invoking their obsolete stop-stage checks."""
from evidence import *
import re


def main():
    baseline=json.loads((ROOT/'reports/C_baseline.json').read_text('utf8'));manifest=json.loads((ROOT/'reports/D_delivery_manifest.json').read_text('utf8'))
    preserved=[]
    for row in manifest['entries']:
        path=Path(row['path']);parts=path.parts
        keep=parts[0] in ['F','E','D'] or (parts[0]=='reports' and re.match(r'^[FED](?:[0-9_]|$)',path.name)) or (parts[0]=='artifacts' and len(parts)>1 and re.fullmatch(r'[FED][0-9]?',parts[1]))
        if not keep:continue
        assert sha(ROOT/path)==row['sha256'],path;preserved.append(row)
    assert sha(ROOT/'reports/D_AUDIT.json')==baseline['D_audit_sha256']
    runtime=json.loads((ROOT/'reports/D_runtime_export.json').read_text('utf8'));assert sha(ROOT/runtime['archive'])==baseline['D_runtime_sha256']
    digest=sha(ROOT/'YSYX_D_DELIVERY.zip');assert digest==baseline['D_zip_sha256']
    assert (ROOT/'YSYX_D_DELIVERY.zip.sha256').read_text('ascii').split()[0]==digest
    dump(ROOT/'reports/C_history_preservation.json',{'status':'PASS','D_zip_sha256':digest,'D_audit_sha256':baseline['D_audit_sha256'],'D_runtime_sha256':baseline['D_runtime_sha256'],'prior_manifest_sha256':sha(ROOT/'reports/D_delivery_manifest.json'),'preserved_files':preserved,'scope':'PriorF/E/D source,chapterreports,frozenruntimesandrawstageevidence fromthepriorDmanifest are byte-identical. SharedREADME/config andnewCfiles evolve separately. Historical D/E verifiers are not run withobsolete stop-stage predicates.'})
    print('C_HISTORY_PRESERVED',len(preserved),'files',flush=True)


if __name__=='__main__':main()
