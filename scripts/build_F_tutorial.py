from logisim_circuits import *
from evidence import *
def build():
    p=Project('tutorial_gui');e=ET.SubElement(p.root,'circuit',{'name':'tutorial_gui'});attr(e,'appearance','classic')
    for n,(x,y) in {'X':(100,100),'Y':(100,300)}.items():comp(e,'Wiring','Pin',x,y,label=n,type='input')
    comp(e,'Wiring','Pin',650,200,label='Z',type='output',facing='west')
    for x,y in [(250,100),(250,300)]:comp(e,'Gates','NOT Gate',x,y)
    for x,y in [(400,140),(400,260)]:comp(e,'Gates','AND Gate',x,y,inputs=2)
    comp(e,'Gates','OR Gate',550,200,inputs=2)
    wires=[(100,100,150,100),(150,100,220,100),(150,100,150,120),(150,120,350,120),(250,100,280,100),(280,100,280,240),(280,240,350,240),(100,300,170,300),(170,300,220,300),(170,300,170,280),(170,280,350,280),(250,300,300,300),(300,300,300,160),(300,160,350,160),(400,140,450,140),(450,140,450,180),(450,180,500,180),(400,260,470,260),(470,260,470,220),(470,220,500,220)]
    for x1,y1,x2,y2 in wires:ET.SubElement(e,'wire',{'from':point(x1,y1),'to':point(x2,y2)})
    # Leave the final output connection for an actual GUI wiring operation.
    p.write(ROOT/'F/circuits/tutorial_gui_unfinished.circ')
    ET.SubElement(e,'wire',{'from':'(550,200)','to':'(650,200)'})
    p.write(ROOT/'F/circuits/tutorial_reference_complete.circ')
    dump(ROOT/'config/execution_policy.json',{'current_scope':'Finish F1-F6 required technical tasks and selected F optional exercises; F7 placeholder ignored','stop_after':'F','next_model_requested_by_user':'GPT-6 Astra','advance_to_E':False,'source_instruction':'User explicitly requested notification at F completion and will change model before E.'})
if __name__=='__main__':build()
