from pathlib import Path
import subprocess,shutil
root=Path(__file__).resolve().parents[1];app=root/'app'
s=(app/'pubspec.yaml').read_text()
if 'version: 1.0.362+592' not in s:
 assert 'version: 1.0.361+591' in s,'Exact released Build591 required'
 patch=(root/'tools/build592_app.patch').read_bytes()
 subprocess.run(['patch','--batch','--dry-run','-p1','-d',str(app)],input=patch,check=True)
 subprocess.run(['patch','--batch','-p1','-d',str(app)],input=patch,check=True)
live_patch=(root/'tools/build592_live_moderation.patch').read_bytes()
live_patch_command=['patch','--batch','-p1','-d',str(app)]
if subprocess.run(live_patch_command+['--dry-run','--reverse','--forward'],input=live_patch,capture_output=True).returncode!=0:
 subprocess.run(live_patch_command+['--dry-run','--forward'],input=live_patch,check=True)
 subprocess.run(live_patch_command+['--forward'],input=live_patch,check=True)
shutil.copy2(root/'tools/assets/ludo592_gifts.png',app/'assets/ludo592_gifts.png')
shutil.copytree(root/'tools/assets/gifts592',app/'assets/gifts592',dirs_exist_ok=True)
print('Build592: shared four-seat invites, automatic full-table start, prompt pawn input and illustrated/sounding gifts')
