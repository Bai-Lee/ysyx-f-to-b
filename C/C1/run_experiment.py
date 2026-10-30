"""Small authored ELF exercise for a background-only chapter; no AM edits."""
from pathlib import Path
import sys,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
recorded_run=run
def run(*args,**kwargs):
    # Reuse only identical command/input/output/log bytes; never call a reuse
    # a new execution. This also preserves the initial PDF-parser diagnosis.
    kwargs.setdefault('resume',True)
    return recorded_run(*args,**kwargs)

def main():
    d=ROOT/'C/C1';src=d/'src';out=d/'results';out.mkdir(exist_ok=True)
    source=ARCHIVE/'slides/markdown/2306/580e82b43f0b9820.md'
    tools=[]
    for name in ['gcc','ar','nm','readelf','objdump','riscv64-linux-gnu-gcc']:
        executable=Path(shutil.which(name));o,e,_=run('C1/tools/'+name,[executable,'--version'],inputs=[executable],cwd=out)
        tools.append({'name':name,'path':str(executable),'sha256':sha(executable),'version':(o+e).splitlines()[0]})
    dump(ROOT/'reports/C1_PREFLIGHT.json',{'status':'READY_FOR_BOUNDED_BACKGROUND_EXPERIMENT','core_tasks':0,'capabilities':['host C compilation','ELF and archive inspection','RV32E object generation only'],'tools':tools,'budget':'Sequential light compilation only, no project-wide builds or installations.','source':str(source),'source_sha256':sha(source),'limits':['Host ELF experiment is x86-64; RV32E object is inspected but not executed.','No whole-video or course-mastery claim.']})
    flags=['-std=c11','-O0','-g','-Wall','-Wextra','-Werror','-fno-pie','-fno-common']
    objects={}
    for name in ['main','producer','unused','duplicate']:
        obj=out/(name+'.o');objects[name]=obj
        run('C1/elf/compile-'+name,['gcc',*flags,'-c',src/(name+'.c'),'-o',obj],inputs=[src/(name+'.c'),src/'api.h'],outputs=[obj],cwd=out)
    archive=out/'liblesson.a';run('C1/elf/archive',['ar','rcs',archive,objects['producer'],objects['unused']],inputs=[objects['producer'],objects['unused']],outputs=[archive],cwd=out)
    o,_,_=run('C1/elf/object-inspection',['readelf','-h','-W','-S','-s','-r',objects['main']],inputs=[objects['main']],cwd=out)
    assert 'REL (Relocatable file)' in o and 'UND add_to_counter' in o and 'R_X86_64_PLT32' in o
    (out/'main-object.txt').write_text(o)
    elf=out/'linked.elf';mapfile=out/'linked.map'
    run('C1/elf/link',['gcc','-no-pie',objects['main'],archive,'-Wl,-Map='+str(mapfile),'-o',elf],inputs=[objects['main'],archive],outputs=[elf,mapfile],cwd=out)
    o,_,_=run('C1/elf/run',[elf],inputs=[elf],cwd=out);assert o=='ELF_LINK_PASS counter=15 zero=0\n'
    h,_,_=run('C1/elf/executable-inspection',['readelf','-h','-W','-S','-s','-l','-d',elf],inputs=[elf],cwd=out)
    assert 'EXEC (Executable file)' in h and 'INTERP' in h and 'Shared library: [libc.so.6]' in h
    assert '.shstrtab' in h and '.strtab' in h and '.symtab' in h and '.bss' in h
    assert re.search(r'LOCAL\s+DEFAULT\s+\d+\s+bias\b',h)
    assert re.search(r'GLOBAL\s+DEFAULT\s+\d+\s+counter\b',h)
    shndx=int(re.search(r'Section header string table index:\s*(\d+)',h)[1])
    assert re.search(r'\[\s*'+str(shndx)+r'\]\s+\.shstrtab\b',h)
    (out/'linked-elf.txt').write_text(h)
    symbols,_,_=run('C1/elf/nm',['nm','-n',elf],inputs=[elf],cwd=out)
    assert 'unused_archive_member' not in symbols and 'add_to_counter' in symbols and 'counter' in symbols
    (out/'linked-symbols.txt').write_text(symbols)
    _,e,bad_order=run('C1/elf/reject-library-order',['gcc','-no-pie',archive,objects['main'],'-o',out/'wrong-order.elf'],inputs=[archive,objects['main']],expected=(1,),cwd=out)
    assert 'undefined reference' in e and 'add_to_counter' in e
    _,e,duplicate=run('C1/elf/reject-duplicate-definition',['gcc','-no-pie',objects['main'],objects['duplicate'],archive,'-o',out/'duplicate.elf'],inputs=[objects['main'],objects['duplicate'],archive],expected=(1,),cwd=out)
    assert 'multiple definition' in e and 'counter' in e
    rv=out/'producer-rv32e.o'
    run('C1/elf/compile-rv32e',['riscv64-linux-gnu-gcc',*flags,'-march=rv32e','-mabi=ilp32e','-ffreestanding','-fno-pic','-c',src/'producer.c','-o',rv],inputs=[src/'producer.c',src/'api.h'],outputs=[rv],cwd=out)
    r,_,_=run('C1/elf/inspect-rv32e',['riscv64-linux-gnu-readelf','-h','-A','-r',rv],inputs=[rv],cwd=out)
    assert 'RVE' in r and 'rv32e' in r and 'R_RISCV_HI20' in r and 'R_RISCV_LO12' in r
    (out/'rv32e-relocations.txt').write_text(r)
    # Read a precise standards excerpt to avoid inheriting a misleading slide claim.
    pdf=ARCHIVE/'assets/offline/www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf'
    text,_,_=run('C1/standard/extract',['pdftotext','-layout',pdf,'-'],inputs=[pdf],cwd=out)
    pages=text.split('\f');selected=[]
    for i,page in enumerate(pages):
        normalized=' '.join(page.split())
        if ('6.9 External definitions' in normalized and 'If an identifier declared with external linkage' in normalized) or ('6.9.2 External object definitions' in normalized and 'tentative definition' in normalized):
            selected.append({'physical_page':i+1,'text':page})
    assert selected and any('exactly one external definition' in p['text'] for p in selected)
    (out/'n1570-excerpts.txt').write_text('\n\n'.join('PDF physical page '+str(p['physical_page'])+'\n'+p['text'] for p in selected))
    page=next(p['physical_page'] for p in selected if 'If an identifier declared with external linkage' in ' '.join(p['text'].split()))
    png=out/'n1570-external-definitions.png'
    run('C1/standard/render',['pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-scale-to','1600','-png',pdf,out/'n1570-external-definitions'],inputs=[pdf],outputs=[png],cwd=out)
    report={'status':'PASS_BOUNDED_BACKGROUND_EXPERIMENT','course_record':'C1-O001','core_tasks':0,'checks':{'unresolved_object_symbol_and_relocation':True,'archive_member_selected_on_demand':True,'correct_link_and_execution':True,'wrong_library_order_rejected':bad_order['exit_code']==1,'duplicate_definition_rejected':duplicate['exit_code']==1,'static_archive_with_dynamic_libc':True,'section_name_table_index':shndx,'RV32E_object_relocations':True},'sources':[{'path':str(source),'sha256':sha(source)},{'path':str(pdf),'sha256':sha(pdf)}],'standard_physical_pages':[p['physical_page'] for p in selected],'tools':tools,'evidence':['artifacts/C1/elf','artifacts/C1/standard','C/C1/results'],'limits':['Authored small example; not all slide examples replayed.','No static libc executable, dynamic-loader implementation or ELF certification claim.','RV32E object generated and inspected, not run here.']}
    dump(ROOT/'reports/C1_experiment.json',report)
    print('C1_BACKGROUND_EXPERIMENT_PASS',flush=True)

if __name__=='__main__':main()
