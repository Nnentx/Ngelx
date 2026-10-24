from pathlib import Path
import hashlib,json,shutil,subprocess,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
class Build561(unittest.TestCase):
 def test_replay_drift_permission_and_layout_preservation(self):
  tools=ROOT/'tools';manifest=json.loads((tools/'build561_manifest.json').read_text())
  self.assertEqual(set(manifest),{'app/lib/main.dart'})
  with tempfile.TemporaryDirectory() as folder:
   temp=Path(folder);(temp/'tools').mkdir();(temp/'app/lib').mkdir(parents=True)
   for name in ['apply_build561_quality.py','build561_manifest.json','build561_quality.patch','build561_quality.dart']:shutil.copyfile(tools/name,temp/'tools'/name)
   path=temp/'app/lib/main.dart';shutil.copyfile(ROOT/'app/lib/main.dart',path)
   digest=lambda:hashlib.sha256(path.read_bytes()).hexdigest()
   def run(*args):return subprocess.run(args,cwd=temp,capture_output=True,text=True)
   if digest()==manifest['app/lib/main.dart']['after']:
    p=run('git','apply','--reverse','tools/build561_quality.patch');self.assertEqual(p.returncode,0,p.stderr)
   self.assertEqual(digest(),manifest['app/lib/main.dart']['before'])
   before=path.read_text()
   (temp/'firestore.rules').write_text('unchanged');(temp/'app/pubspec.yaml').write_text('unchanged')
   for _ in range(2):
    p=run('python3','tools/apply_build561_quality.py');self.assertEqual(p.returncode,0,p.stderr)
   after=path.read_text()
   self.assertEqual(digest(),manifest['app/lib/main.dart']['after'])
   def section(s,a,b):return s[s.index(a):s.index(b,s.index(a))]
   # Inbox header, filters, counts and layout remain byte-for-byte Build560.
   self.assertEqual(section(before,'    Widget sekme(String ad,int sayi)','    Widget bildirimlerIcerigi()'),section(after,'    Widget sekme(String ad,int sayi)','    Widget bildirimlerIcerigi()'))
   self.assertEqual(section(before,'            Ngelx560InboxHeader(','            // Build542:'),section(after,'            Ngelx560InboxHeader(','            // Build542:'))
   # Authorization and Firestore write payloads are not relaxed for speed.
   self.assertEqual(section(before,"    String icerikSahibi='';",'    setState(()=>gonderiliyor=true);'),section(after,"    String icerikSahibi='';",'    if(!mounted)return;\n    final yanitId='))
   self.assertEqual(section(before,'      final yorumRef=ref.doc(),videoRef=','    }on TimeoutException{\n      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text(\'Yorum gönderimi'),section(after,'      final yorumRef=ref.doc(),videoRef=','    }on TimeoutException{\n      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text(\'Yorum gönderimi'))
   comment=section(after,'class _YeniYorumlarState','class NgelXYorumYazici')
   self.assertEqual(comment.count('ref.limit(80).snapshots()'),1)
   self.assertIn('stream: _yorumAkisi561',comment)
   self.assertLess(comment.index('setState(()=>gonderiliyor=true)'),comment.index('await _dogrulayipGonder561()'))
   self.assertEqual((temp/'firestore.rules').read_text(),'unchanged');self.assertEqual((temp/'app/pubspec.yaml').read_text(),'unchanged')
   path.write_text(after+'\n// drift\n');p=run('python3','tools/apply_build561_quality.py');self.assertNotEqual(p.returncode,0)
if __name__=='__main__':unittest.main()
