"""Derive a separate replay from the accepted E6 native GUI test, preserving E."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
d=ROOT/'D/D8';source=ROOT/'E/E6/fceux_verify.py'
text=source.read_text().replace('E6','D8').replace('minirv-npc','riscv32e-npc')
text=text.replace("mark(['D8-M001']","mark(['D8-NATIVE_FCEUX']").replace("mark(['D8-M017']","mark(['D8-NPC_FCEUX']")
text=text.replace("ROOT/'D8/D8/", "ROOT/'D/D8/")
# E/E6 became E/D8 under a simple stage-name replacement; fix only those paths.
text=text.replace("ROOT/'E/D8/", "ROOT/'D/D8/")
text=text.replace(" d=ROOT/'artifacts/D8/fceux/native_session';d.mkdir(parents=True,exist_ok=True)"," d=ROOT/'artifacts/D8/fceux/native_session';d.mkdir(parents=True,exist_ok=True)\n if (d/'run.json').exists():\n  history=d/'attempts'/str(time.time_ns());history.mkdir(parents=True)\n  for file in list(d.iterdir()):\n   if file.is_file():shutil.copyfile(file,history/file.name)")
text=text.replace("SDL_RENDER_DRIVER='software',SHELL='/bin/bash')","SDL_RENDER_DRIVER='software',SHELL='/bin/bash',mainargs='interaction')")
text='\n'.join(line for line in text.splitlines() if not line.lstrip().startswith('mark('))+'\n'
text=text.replace('Actual minirv NPC','Actual RV32E NPC')
text=text.replace("inputs=[config,rom],timeout=600)","inputs=[config,rom],outputs=[fceux/'build/fceux-native.elf'],timeout=600)")
text=text.replace("inputs=[config,rom],timeout=1800)","inputs=[config,rom,BENCH/'npc/build/sim',Path(json.loads((ROOT/'reports/D8_reference.json').read_text())['shared_object'])],outputs=[fceux/'build/fceux-riscv32e-npc.bin',fceux/'build/fceux-riscv32e-npc.elf',fceux/'build/fceux-riscv32e-npc.bin.npc.json'],timeout=1800)")
dest=d/'fceux_verify.py';dest.write_text('# Derived from E/E6/fceux_verify.py for an isolated D-stage execution.\n'+text)
rom=d/'homebrew';rom.mkdir(exist_ok=True)
for name in ['interaction.nes','symbols.json','make_homebrew.py']:
    original=ROOT/('E/E6/'+name if name.endswith('.py') else 'E/E6/homebrew/'+name)
    shutil.copyfile(original,(d if name.endswith('.py') else rom)/name)
dump(d/'homebrew/provenance.json',{'rom_source':'E/E6/homebrew/interaction.nes','rom_sha256':sha(rom/'interaction.nes'),'script_source':str(source),'script_source_sha256':sha(source),'purpose':'Existing original project-authored ROM and actual SDL/X11 callback test, rerun in the D-stage workbench. No E files are modified.'})
