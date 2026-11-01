from pathlib import Path
import gzip,subprocess,shutil,sys
root=Path(__file__).resolve().parents[1]
app=root/'app'
if 'version: 1.0.358+588' in (app/'pubspec.yaml').read_text():
 print('Build588 already applied');sys.exit(0)
assert 'version: 1.0.357+587' in (app/'pubspec.yaml').read_text(),'Exact Build587 source required'
patch=gzip.decompress((root/'tools/build588_app.patch.gz').read_bytes())
subprocess.run(['patch','--batch','--dry-run','-p1','-d',str(app)],input=patch,check=True)
subprocess.run(['patch','--batch','-p1','-d',str(app)],input=patch,check=True)
shutil.copytree(root/'tools/assets/gifts588',app/'assets/gifts588',dirs_exist_ok=True)
print('Build588 applied to reviewed Build587')
