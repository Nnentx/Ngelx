from pathlib import Path
import hashlib,json,shutil,subprocess,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
class Inbox560(unittest.TestCase):
 def test_patch_repeat_drift_and_scope(self):
  manifest=json.loads((ROOT/'tools/build560_manifest.json').read_text())
  self.assertEqual(set(manifest),{'app/lib/main.dart','app/lib/build445_inbox_model.dart'})
  with tempfile.TemporaryDirectory() as folder:
   temp=Path(folder);(temp/'tools').mkdir();(temp/'app/lib').mkdir(parents=True)
   for name in ['apply_build560_inbox.py','build560_manifest.json','build560_inbox.patch','build560_inbox.dart']:shutil.copyfile(ROOT/'tools'/name,temp/'tools'/name)
   for path in manifest:shutil.copyfile(ROOT/path,temp/path)
   # Changes to external settings are rejected by exact fixture comparison.
   (temp/'firestore.rules').write_text('UNCHANGED RULES');(temp/'app/pubspec.yaml').write_text('UNCHANGED CONFIG')
   def run(*args):return subprocess.run(args,cwd=temp,capture_output=True,text=True)
   hashes=lambda:{p:hashlib.sha256((temp/p).read_bytes()).hexdigest() for p in manifest}
   if all(hashes()[p]==e['after'] for p,e in manifest.items()):
    result=run('git','apply','--reverse','tools/build560_inbox.patch');self.assertEqual(result.returncode,0,result.stderr)
   before={p:(temp/p).read_text() for p in manifest}
   self.assertTrue(all(hashes()[p]==e['before'] for p,e in manifest.items()))
   for _ in range(2):
    result=run('python3','tools/apply_build560_inbox.py');self.assertEqual(result.returncode,0,result.stderr)
   self.assertTrue(all(hashes()[p]==e['after'] for p,e in manifest.items()))
   after={p:(temp/p).read_text() for p in manifest}
   old=before['app/lib/main.dart'];new=after['app/lib/main.dart'].replace("part 'build560_inbox.dart';\n",'')
   start='class MesajPage extends StatefulWidget';end='class ArsivSohbetlerPage extends StatefulWidget'
   self.assertEqual(old[:old.index(start)],new[:new.index(start)])
   self.assertEqual(old[old.index(end):],new[new.index(end):])
   # Entire live list/filter/query implementation is unchanged.
   start='    Widget bildirimlerIcerigi()';end="    Widget govde=filtre=="
   self.assertEqual(old[old.index(start):old.index(end)],new[new.index(start):new.index(end)])
   start='class _MesajPageState';end='    Widget sekme(String ad,int sayi)'
   self.assertEqual(old[old.index(start):old.index(end)],new[new.index(start):new.index(end)])
   old=before['app/lib/build445_inbox_model.dart'];new=after['app/lib/build445_inbox_model.dart']
   start='Future<void> ngelx445ReturnCall';self.assertEqual(old[old.index(start):],new[new.index(start):])
   end='  @override Widget build(BuildContext context)=>StreamBuilder';self.assertEqual(old[:old.index(end)],new[:new.index(end)])
   self.assertNotIn('SizedBox(height:54,child:note',new)
   for feature in ['inboxNoteExpiresAt','_editNote(p)','_showNote(id,p,note)','_open(id,p)','Ngelx436PresenceAccess','story?mor:Colors.transparent']:self.assertIn(feature,new)
   self.assertEqual((temp/'firestore.rules').read_text(),'UNCHANGED RULES');self.assertEqual((temp/'app/pubspec.yaml').read_text(),'UNCHANGED CONFIG')
   p=temp/'app/lib/main.dart';p.write_text(p.read_text()+'\n// drift\n');before=hashes()
   self.assertNotEqual(run('python3','tools/apply_build560_inbox.py').returncode,0);self.assertEqual(hashes(),before)
if __name__=='__main__':unittest.main()
