"""Cold/repeated application, pre-mutation drift protection and scoped rules delta."""
from pathlib import Path
import hashlib,json,shutil,subprocess,tempfile,unittest
from build558_rules import patch_rules
ROOT=Path(__file__).resolve().parents[1]
class Quality558(unittest.TestCase):
 def test_scoped_rules_change_preserves_sender_and_admin_gate(self):
  raw=(ROOT/'firestore.rules').read_text()
  changed=patch_rules(raw)
  self.assertEqual(changed,patch_rules(changed))
  start=raw.index('      match /messages/{messageId} {',raw.index('    match /chats/{chatId}'))
  end=raw.index('      match /joinRequests/',start)
  new_end=changed.index('      match /joinRequests/',start)
  self.assertEqual(raw[:start],changed[:start]);self.assertEqual(raw[end:],changed[new_end:])
  block=changed[start:new_end]
  self.assertIn('resource.data.senderId == request.auth.uid',block)
  self.assertIn("request.resource.data.get('albumItems558', []) == []",block)
  self.assertIn("request.resource.data.get('mediaUrls', []) == []",block)
  self.assertIn(".concat(resource.data.get('mediaUrls', []))",block)
 def test_real_patch_reproduction_repeat_and_drift(self):
  manifest=json.loads((ROOT/'tools/build558_manifest.json').read_text())
  with tempfile.TemporaryDirectory() as folder:
   temp=Path(folder);(temp/'tools').mkdir();(temp/'app/lib').mkdir(parents=True)
   for name in ['apply_build558_quality.py','build558_rules.py','build435_rules.py','build558_manifest.json','build558_quality.patch','build558_chat_quality.dart']:
    shutil.copyfile(ROOT/'tools'/name,temp/'tools'/name)
   shutil.copyfile(ROOT/'firestore.rules',temp/'firestore.rules')
   for path in manifest:shutil.copyfile(ROOT/path,temp/path)
   def run(*cmd):return subprocess.run(cmd,cwd=temp,capture_output=True,text=True)
   hashes=lambda:{path:hashlib.sha256((temp/path).read_bytes()).hexdigest() for path in manifest}
   if all(hashes()[p]==m['after'] for p,m in manifest.items()):
    result=run('git','apply','--reverse','tools/build558_quality.patch');self.assertEqual(result.returncode,0,result.stderr)
   self.assertTrue(all(hashes()[p]==m['before'] for p,m in manifest.items()))
   result=run('python3','tools/apply_build558_quality.py');self.assertEqual(result.returncode,0,result.stderr)
   self.assertTrue(all(hashes()[p]==m['after'] for p,m in manifest.items()))
   first=hashes();rules=(temp/'firestore.rules').read_text()
   result=run('python3','tools/apply_build558_quality.py');self.assertEqual(result.returncode,0,result.stderr)
   self.assertEqual(first,hashes());self.assertEqual(rules,(temp/'firestore.rules').read_text())
   drift=temp/'app/lib/main.dart';drift.write_text(drift.read_text()+'\n// unrelated source drift\n')
   before=hashes();result=run('python3','tools/apply_build558_quality.py')
   self.assertNotEqual(result.returncode,0);self.assertEqual(before,hashes())
   self.assertEqual(rules,(temp/'firestore.rules').read_text())
if __name__=='__main__':unittest.main()
