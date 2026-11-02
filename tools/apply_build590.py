from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[1];app=root/'app'
if 'version: 1.0.360+590' in (app/'pubspec.yaml').read_text():
 print('Build590 already applied');sys.exit(0)
assert 'version: 1.0.359+589' in (app/'pubspec.yaml').read_text(),'Exact released Build589 source required'
patch=(root/'tools/build590_app.patch').read_bytes()
subprocess.run(['patch','--batch','--dry-run','-p1','-d',str(app)],input=patch,check=True)
subprocess.run(['patch','--batch','-p1','-d',str(app)],input=patch,check=True)
print('Build590: full reference-style audio room stage, comments and controls')
