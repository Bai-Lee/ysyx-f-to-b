"""E1 source/interface locking and four-state, vector-driven RTL verification."""
from pathlib import Path
import sys,json,re,itertools,random,hashlib
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from evidence import run,sha,dump
SPECS={x['slug']:x for x in json.loads((ROOT/'E/E1/specs.json').read_text('utf8'))['records']}
OUT=ROOT/'E/E1'

def ports(interface):
    clean=re.sub(r'//[^\n]*','',interface)
    m=re.search(r'module\s+top_module\s*\((.*?)\)\s*;(.*)',clean,re.S)
    if not m:raise ValueError('Unsupported module interface '+interface)
    result=[];direction=None;bounds='';width=1
    text=m[1] if re.search(r'\b(input|output)\b',m[1]) else ','.join(a+' '+b for a,b in re.findall(r'\b(input|output)\s+([^;]+);',m[2]))
    for part in text.split(','):
        part=part.strip();d=re.match(r'(input|output)\b',part)
        if d:direction=d[1];bounds='';width=1;part=part[d.end():].strip()
        part=re.sub(r'\b(wire|reg|logic|signed|unsigned)\b','',part).strip()
        b=re.match(r'\[\s*(-?\d+)\s*:\s*(-?\d+)\s*\]',part)
        if b:bounds=b[0];width=abs(int(b[1])-int(b[2]))+1;part=part[b.end():].strip()
        if not direction or not re.fullmatch(r'[A-Za-z_]\w*',part):raise ValueError((part,interface))
        result.append({'name':part,'direction':direction,'bounds':bounds,'width':width})
    return result

class Problem:
    def __init__(self,slug,body,procedural=(),submodules='',support='',compile_support=None,extra_inputs=None,checks='',explanation='',mask_reasons=None):
        self.spec=SPECS[slug];self.slug=slug;self.ports=ports(self.spec['interface']);self.ins=[p for p in self.ports if p['direction']=='input'];self.outs=[p for p in self.ports if p['direction']=='output'];self.extra=[{'name':n,'width':w,'bounds':f'[{w-1}:0]' if w>1 else '', 'direction':'extra'} for n,w in (extra_inputs or {}).items()];self.rows=[];self.checked={p['name']:0 for p in self.outs};self.mask_reasons=mask_reasons or {};self.support=support;self.compile_support=support if compile_support is None else compile_support;self.checks=checks;self.explanation=explanation
        decl=[]
        for p in self.ports:decl.append('  '+p['direction']+' '+('reg' if p['name'] in procedural else 'wire')+' '+(p['bounds']+' ' if p['bounds'] else '')+p['name'])
        self.rtl='// '+self.spec['id']+' '+self.spec['title']+'\n// Source: '+self.spec['source_url']+'\n// Independently authored implementation; exact external names and ranges preserved.\n`default_nettype none\nmodule top_module(\n'+',\n'.join(decl)+'\n);\n'+body.strip()+'\nendmodule\n'+submodules.strip()+'\n`default_nettype wire\n'
    def add(self,inputs,outputs):
        fields=[]
        for p in self.ins+self.extra:
            value=inputs[p['name']]
            if not isinstance(value,int) or not 0<=value<(1<<p['width']):raise ValueError((self.slug,p,value))
            fields.append(format(value,'x'))
        for p in self.outs:
            value=outputs[p['name']]
            if value is None:
                if p['name'] not in self.mask_reasons:raise ValueError('Undeclared dont-care '+self.slug+' '+p['name'])
                fields+=['0','0']
            else:
                if not isinstance(value,int) or not 0<=value<(1<<p['width']):raise ValueError((self.slug,p,value))
                fields += [format(value,'x'),format((1<<p['width'])-1,'x')];self.checked[p['name']]+=1
        self.rows.append(' '.join(fields))
    def comb(self,oracle,cases):
        for v in cases:self.add(v,oracle(v))
    def clocked(self,model,cycles,clock='clk',falling=False,clock_bit=None):
        for v0 in cycles:
            v=dict(v0)
            def setclk(level):
                if clock_bit is None:v[clock]=level
                else:v[clock]=(v.get(clock,0)&~(1<<clock_bit))|(level<<clock_bit)
            setclk(1 if falling else 0)
            model.asynchronous(v)
            self.add(v,model.output(v))
            setclk(0 if falling else 1)
            model.tick(v)
            self.add(v,model.output(v))
    def write(self):
        if not self.rows or any(n==0 for n in self.checked.values()):raise ValueError('No checked output '+self.slug)
        dut=OUT/'rtl'/(self.slug+'.v');vec=OUT/'vectors'/(self.slug+'.txt');tb=OUT/'tests'/(self.slug+'_tb.sv');lib=OUT/'tests'/(self.slug+'_support.v');lintlib=OUT/'tests'/(self.slug+'_syntax_support.v')
        dut.write_text(self.rtl,encoding='utf8');vec.write_text('\n'.join(self.rows)+'\n',encoding='ascii');lib.write_text(self.support,encoding='utf8');lintlib.write_text(self.compile_support,encoding='utf8')
        decl=[];variables=[]
        for p in self.ins+self.extra:decl.append(f'reg {p["bounds"]} v_{p["name"]};');variables.append('v_'+p['name'])
        for p in self.outs:
            decl.append(f'wire {p["bounds"]} got_{p["name"]};reg {p["bounds"]} exp_{p["name"]}, mask_{p["name"]};');variables += ['exp_'+p['name'],'mask_'+p['name']]
        # Values are scanned into temporary inputs. Data is applied before the
        # clock; a complete delta/NBA settle precedes every strict comparison.
        for p in self.ins+self.extra:decl.append(f'reg {p["bounds"]} scan_{p["name"]};')
        scanvars=['scan_'+p['name'] for p in self.ins+self.extra]+variables[len(self.ins+self.extra):]
        connections=','.join('.'+p['name']+'('+('v_' if p['direction']=='input' else 'got_')+p['name']+')' for p in self.ports)
        input_assign='\n'.join('v_'+p['name']+'=scan_'+p['name']+';' for p in sorted(self.ins+self.extra,key=lambda p:p['name'] in ('clk','KEY')))
        comparisons='\n'.join(f'if(((got_{p["name"]} ^ exp_{p["name"]}) & mask_{p["name"]}) !== {p["width"]}\'d0) begin $display("MISMATCH {self.slug} row=%0d port={p["name"]} got=%h expected=%h mask=%h",n,got_{p["name"]},exp_{p["name"]},mask_{p["name"]});$fatal(1,"behavior mismatch");end' for p in self.outs)
        fmt=' '.join(['%h']*len(scanvars))+'\\n'
        text='`timescale 1ns/1ps\nmodule tb;\n'+'\n'.join(decl)+f'\ninteger file,rc,n=0;top_module dut({connections});\ninitial begin\nfile=$fopen("{vec.as_posix()}","r");if(!file)$fatal(2,"vector file unavailable");\nwhile(!$feof(file))begin\nrc=$fscanf(file,"{fmt}",{",".join(scanvars)});\nif(rc!={len(scanvars)})$fatal(2,"vector parse failure");\n'+input_assign+'\n#1;\n'+comparisons+'\n'+self.checks+'\nn=n+1;end\n'+f'if(n!={len(self.rows)})$fatal(2,"wrong case count");\n$display("PASS {self.slug} checks=%0d",n);$fclose(file);$finish;end\nendmodule\n'
        tb.write_text(text,encoding='utf8')
        return {'id':self.spec['id'],'slug':self.slug,'title':self.spec['title'],'scope':self.spec['scope'],'source_path':self.spec['source_path'],'source_sha256':self.spec['source_sha256'],'dut':str(dut),'testbench':str(tb),'support':str(lib),'syntax_support':str(lintlib),'vectors':str(vec),'cases':len(self.rows),'outputs_checked':self.checked,'mask_reasons':self.mask_reasons,'explanation':self.explanation,'interface':self.ports,'status':'NOT_RUN'}

def exhaustive(widths):
    names=list(widths)
    for vals in itertools.product(*(range(1<<widths[n]) for n in names)):yield dict(zip(names,vals))

def random_cases(widths,count=400,seed=260701):
    rng=random.Random(seed);names=list(widths);yield {n:0 for n in names};yield {n:(1<<widths[n])-1 for n in names}
    for n in names:
        for bit in range(widths[n]):
            yield {k:(1<<bit if k==n else 0) for k in names}
            yield {k:(((1<<widths[n])-1)^(1<<bit) if k==n else 0) for k in names}
    for _ in range(count):yield {n:rng.getrandbits(widths[n]) for n in names}

class Model:
    def asynchronous(self,v):pass
    def tick(self,v):raise NotImplementedError
    def output(self,v):raise NotImplementedError

def write_jobs(problems):
    path=OUT/'jobs.json';old=json.loads(path.read_text('utf8')) if path.exists() else {'records':[]};existing={x['slug']:x for x in old['records']}
    for p in problems:existing[p.slug]=p.write()
    rows=sorted(existing.values(),key=lambda r:r['id']);dump(path,{'source_count':112,'records':rows});print('E1_BUILT',len(problems),'total',len(rows),'vectors',sum(len(p.rows) for p in problems),flush=True)
