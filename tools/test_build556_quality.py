"""Exercise the real generated patch: cold apply, repeat apply and drift guard."""
from pathlib import Path
import hashlib,json,shutil,subprocess,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
class Quality556(unittest.TestCase):
 def test_real_patch_is_reproducible_and_rejects_unrelated_source_drift(self):
  manifest=json.loads((ROOT/'tools/build556_manifest.json').read_text())
  with tempfile.TemporaryDirectory() as folder:
   temp=Path(folder);(temp/'tools').mkdir();(temp/'app/lib').mkdir(parents=True)
   for name in ['apply_build556_quality.py','build556_manifest.json','build556_quality.patch','build556_quality.dart','build556_policy.dart']:
    shutil.copyfile(ROOT/'tools'/name,temp/'tools'/name)
   for path in manifest:shutil.copyfile(ROOT/path,temp/path)
   def run(*cmd):return subprocess.run(cmd,cwd=temp,capture_output=True,text=True)
   hashes=lambda:{path:hashlib.sha256((temp/path).read_bytes()).hexdigest() for path in manifest}
   # Starting from the applied generated source, reconstruct its exact baseline.
   if all(hashes()[p]==m['after'] for p,m in manifest.items()):
    result=run('git','apply','--reverse','tools/build556_quality.patch');self.assertEqual(result.returncode,0,result.stderr)
   self.assertTrue(all(hashes()[p]==m['before'] for p,m in manifest.items()))
   result=run('python3','tools/apply_build556_quality.py');self.assertEqual(result.returncode,0,result.stderr)
   self.assertTrue(all(hashes()[p]==m['after'] for p,m in manifest.items()))
   first=hashes();result=run('python3','tools/apply_build556_quality.py');self.assertEqual(result.returncode,0,result.stderr);self.assertEqual(first,hashes())
   drift=temp/'app/lib/main.dart';drift.write_text(drift.read_text()+'\n// unrelated change\n')
   before=hashes();result=run('python3','tools/apply_build556_quality.py');self.assertNotEqual(result.returncode,0);self.assertEqual(before,hashes())
if __name__=='__main__':unittest.main()
