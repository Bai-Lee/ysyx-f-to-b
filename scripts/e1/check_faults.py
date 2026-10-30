"""Compile real mutated RTL and require a behavioral mismatch, not compile failure."""
from common import *
from run import run_one
from datetime import datetime,timezone

FAULTS=[
 ('andgate','or_instead_of_and','assign out = a & b;','assign out = a | b;'),
 ('fsm1','sync_instead_of_async','always @(posedge clk or posedge areset)','always @(posedge clk)'),
 ('dff8p','wrong_reset_value',"value<=8'h34", "value<=8'h00"),
 ('adder100i','carry_vector_off_by_one','assign cout=c[100:1];','assign cout=c[99:0];'),
 ('lemmings4','death_at_20', 'FLEFT:if(ground)next_state=(fall_count>20)?DEAD:LEFT;', 'FLEFT:if(ground)next_state=(fall_count>=20)?DEAD:LEFT;'),
 ('lemmings4','fall_counter_wrap','if(!ground && fall_count<21)','if(!ground)'),
 ('fsm_serialdata','resync_before_stop','end else state<=RECOVER;end','end else state<=IDLE;end'),
 ('fsm_serialdp','wrong_parity','if(odd)begin','if(!odd)begin'),
 ('fsm_ps2data','reversed_bytes','out_bytes<={first,second,in};','out_bytes<={in,second,first};'),
 ('conwaylife','wrong_wrapped_neighbor',"cells[((r+15)%16)*16+(c+15)%16]", "cells[((r+14)%16)*16+(c+15)%16]"),
 ('count_clock','pm_never_toggles','pm_value<=~pm_value;','pm_value<=pm_value;'),
 ('2013_q2bfsm','late_y_accepted','G:next_state=y?H:I;','G:next_state=y?H:G;'),
 ('fsm_onehot','ignores_second_active_state','assign next_state[1]=in&(state[0]|state[8]|state[9]);','assign next_state[1]=in&state[0];'),
 ('edgecapture','loses_previous_during_reset','previous<=in;if(reset)','if(!reset)previous<=in;if(reset)')]

def main():
    jobs={x['slug']:x for x in json.loads((OUT/'jobs.json').read_text('utf8'))['records']};results=[]
    for slug,name,old,new in FAULTS:
        result=run_one(jobs[slug],{'name':name,'old':old,'new':new})
        result['fault_rejected']=result['status']=='PASS' and result.get('semantic_sentinel_pass') is True
        results.append(result)
        dump(ROOT/'reports/E1_faults.json',{'status':'PASS' if len(results)==len(FAULTS) and all(r['fault_rejected'] for r in results) else 'IN_PROGRESS','records':results,'timestamp':datetime.now(timezone.utc).isoformat(),'meaning':'PASS means mutated RTL compiled and simulation exited1 with an explicit behavioral MISMATCH; failed compilation never counts as rejection.'})
    bad=[r['mutation']['name'] for r in results if not r['fault_rejected']]
    print('E1_FAULTS',len(results),'not_rejected',bad,flush=True);return int(bool(bad))

if __name__=='__main__':sys.exit(main())
