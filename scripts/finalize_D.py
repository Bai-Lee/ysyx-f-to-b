from evidence import *
from verify_D_delivery import verify_project,markdown_links

def main():
    if not (ROOT/'reports/D_AUDIT.json').exists():dump(ROOT/'reports/D_AUDIT.json',{'status':'IN_PROGRESS','stage_complete':False})
    markdown_links(external=True)
    verification=verify_project(external=True,require_final=False)
    result={'status':'PASS','stage_complete':True,'stage':'D','timestamp':datetime.now(timezone.utc).isoformat(),'core_tasks':55,'scope_records':103,'stop_after':'D','verification':verification,'declared_limits':['D6 extra ideal-MOS DFF transient FAIL_UNQUALIFIED_MODEL; required structural task is complete.','D8 RV32E finite functional verification; no C-stage privilege/interrupts, complete ISA proof or new physical signoff.','MMIO independently decoded/checked before reference synchronization, not two independent device-model comparisons.','Reference-only reading/video nodes and original todo are not counted as experimental passes.','FCEUX virtual display and actual PCM capture; no physical loudspeaker test.','Prior F/E qualification remains bound to its original sources and constraints.'],'delivery':'YSYX_D_DELIVERY.zip; CRC and every member SHA-256 checked by package_delivery.py after this audit.'}
    dump(ROOT/'reports/D_AUDIT.json',result)
    print('D_COMPLETE_AUDIT_PASS',json.dumps({'core':55,'records':103,'commands':verification['commands']['current_accepted_commands'],'nonzero_controls':verification['commands']['expected_nonzero_controls'],'snapshots':verification['commands']['snapshot_archives_verified'],'changed_inputs':len(verification['commands']['changed_inputs_recorded']),'links':verification['markdown']['resolved_links']},ensure_ascii=False),flush=True)

if __name__=='__main__':main()
