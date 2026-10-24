from pathlib import Path
import hashlib,json,shutil,subprocess,tempfile,unittest
from build559_rules import patch_rules
ROOT=Path(__file__).resolve().parents[1]
class Quality559(unittest.TestCase):
 def test_rules_scoped_and_repeatable(self):
  raw=(ROOT/'firestore.rules').read_text();changed=patch_rules(raw)
  self.assertEqual(changed,patch_rules(changed))
  self.assertIn("allow delete: if false;",changed[changed.index('match /users/{uid}'):changed.index('match /videos/{videoId}')])
  self.assertIn("'displayNameChangedAt559', 'usernameChangedAt559'",changed)
 def test_reproduction_repeat_and_drift(self):
  manifest=json.loads((ROOT/'tools/build559_manifest.json').read_text())
  with tempfile.TemporaryDirectory() as folder:
   temp=Path(folder);(temp/'tools').mkdir();(temp/'app/lib').mkdir(parents=True)
   for name in ['apply_build559_quality.py','build559_rules.py','build559_manifest.json','build559_quality.patch','build559_quality.dart']:shutil.copyfile(ROOT/'tools'/name,temp/'tools'/name)
   shutil.copyfile(ROOT/'firestore.rules',temp/'firestore.rules')
   for path in manifest:shutil.copyfile(ROOT/path,temp/path)
   def run(*args):return subprocess.run(args,cwd=temp,capture_output=True,text=True)
   hashes=lambda:{p:hashlib.sha256((temp/p).read_bytes()).hexdigest() for p in manifest}
   if all(hashes()[p]==e['after'] for p,e in manifest.items()):
    result=run('git','apply','--reverse','tools/build559_quality.patch');self.assertEqual(result.returncode,0,result.stderr)
   self.assertTrue(all(hashes()[p]==e['before'] for p,e in manifest.items()))
   for _ in range(2):
    result=run('python3','tools/apply_build559_quality.py');self.assertEqual(result.returncode,0,result.stderr)
   self.assertTrue(all(hashes()[p]==e['after'] for p,e in manifest.items()))
   p=temp/'app/lib/main.dart';p.write_text(p.read_text()+'\n// drift\n');before=hashes()
   self.assertNotEqual(run('python3','tools/apply_build559_quality.py').returncode,0);self.assertEqual(hashes(),before)
if __name__=='__main__':unittest.main()
