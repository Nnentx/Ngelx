from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[1];app=root/'app'
if 'version: 1.0.359+589' in (app/'pubspec.yaml').read_text():
 print('Build589 already applied');sys.exit(0)
assert 'version: 1.0.358+588' in (app/'pubspec.yaml').read_text(),'Exact released Build588 source required'
patch=(root/'tools/build589_app.patch').read_bytes()
subprocess.run(['patch','--batch','--dry-run','-p1','-d',str(app)],input=patch,check=True)
subprocess.run(['patch','--batch','-p1','-d',str(app)],input=patch,check=True)
print('Build589: canonical PK scores, race-safe gift audio, testable circular room seats')
