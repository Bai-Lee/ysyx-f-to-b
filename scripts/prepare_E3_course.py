"""Freeze course exercise IDs and extract original fenced blocks without running them."""
from evidence import *
import re

def main():
    archive=ROOT.parents[1]/'YSYX_F_B_Archive';folder=ROOT/'E/E3';folder.mkdir(parents=True,exist_ok=True)
    matrix=json.loads((archive/'inventory/assignment_matrix.json').read_text('utf8'))['records']
    lct=json.loads((archive/'temp/assignment_review/lcthw_exercises.json').read_text('utf8'))
    ms=[r for r in matrix if r['id'].startswith('MS-')]
    chapters=[]
    for row in lct:
        if row['kind']!='base':continue
        source=archive/row['local_path'];assert sha(source)==row['sha256']
        original=folder/'lcthw/original'/f"ex{row['chapter']:02d}";original.mkdir(parents=True,exist_ok=True)
        text=source.read_text('utf8');blocks=[]
        for i,m in enumerate(re.finditer(r'^```([^\n]*)\n(.*?)^```\s*$',text,re.M|re.S)):
            lang=m[1].strip();suffix={'c':'.c','h':'.h','sh':'.sh','make':'.mk','makefile':'.mk'}.get(lang,'.txt');target=original/(f'block_{i:02d}'+suffix)
            target.write_text(m[2],encoding='utf8',newline='\n');blocks.append({'index':i,'language':lang,'source_line':text[:m.start()].count('\n')+1,'path':str(target),'sha256':sha(target),'first_line':m[2].splitlines()[0] if m[2].splitlines() else ''})
        chapters.append({'chapter':row['chapter'],'title':row['title'],'source':str(source),'source_sha256':row['sha256'],'source_url':row['source_url'],'blocks':blocks})
    assert len(chapters)==32 and len(lct)==180
    dump(folder/'course_specs.json',{'status':'FROZEN_NOT_IMPLEMENTATION_VERDICT','source_matrix_sha256':sha(archive/'inventory/assignment_matrix.json'),'lcthw_records':lct,'missing_semester_records':ms,'chapters':chapters,'warning':'Original example blocks can intentionally contain UB, formatting mistakes, dangerous system commands or shell output. Extraction does not authorize execution; explicit reviewed case scripts select inputs in isolated lab directories.'})
    print('E3_COURSE_FROZEN',len(ms),'MissingSemester items;',len(lct),'LCTHW items;32 chapters',flush=True)
    for c in chapters[:10]:print(c['chapter'],[(b['index'],b['language'],b['first_line'][:65]) for b in c['blocks']],flush=True)

if __name__=='__main__':main()
