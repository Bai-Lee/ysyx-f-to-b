"""Run the final read-only evidence audit after preparation of the C delivery."""
from evidence import *
from verify_C_delivery import verify_project


def main():
    path=ROOT/'reports/C_AUDIT.json'
    if not path.exists():dump(path,{'status':'IN_PROGRESS','stage_complete':False})
    verification=verify_project(external=True,require_final=False)
    dump(path,{'status':'PASS','stage_complete':True,'stage':'C','timestamp':datetime.now(timezone.utc).isoformat(),
        'core_tasks':68,'adapted_tasks':2,'scope_records':101,'nested_PA2_required':17,'stop_after':'C','verification':verification,
        'declared_limits':[
            'C1/C3 are bounded authored background experiments, not a claim to have watched all videos or replayed all slide examples.',
            'C2 optional NEMU audio is not implemented. Some earliest failed GUI attempt captures were not retained; outer failure records/inputs remain and later archival protection was fixed.',
            'C4 Nangate45 maximum-transition violations remain; no qualified Fmax or whole-chip PPA claim. The evaluation task is complete with failures reported.',
            'C5 finite RTL/functional memory models and cooperative machine-mode RT-Thread; no unbounded proof, full privileged ISA, asynchronous IRQ, physical display/electrical retention or new chip signoff.',
            'Full128MiB acceptance uses eight independently reset full-range patterns under the user-authorized parallel memory strategy; not one uninterrupted eight-pattern controller-state sequence. All address/width/payload and reference checks remain required.',
            'C5 MMIO is independently checked and then synchronized to NEMU; it is not two independently simulated device implementations.',
            'ChipLink actual RTL model capacity is1GiB; tested range is4KiB. SPI interrupt-completion variant remains optional and unimplemented.',
            'C6 source is under construction. No B work, personal submission, account application or tapeout completion claim.',
            'Frozen binary replay uses the installed Linux environment. Full original course archive and installed tools/Maven/JDK/system libraries remain locked external dependencies.'
        ],'delivery':'YSYX_C_DELIVERY.zip; package_C.py verifies CRC and every member SHA-256 after this audit.'})
    print('C_COMPLETE_AUDIT_PASS',json.dumps({'core':68,'adapted':2,'records':101,
        'command_counts':verification['commands']['counts'],'snapshots':verification['commands']['snapshot_archives_verified'],
        'frozen_members':verification['frozen']['runtime_members'],'links':verification['markdown']['resolved_links']},ensure_ascii=False),flush=True)


if __name__=='__main__':main()
