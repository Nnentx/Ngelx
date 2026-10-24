from pathlib import Path
import hashlib,json,shutil,subprocess,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
class Build563(unittest.TestCase):
 def test_replay_and_preservation(self):
  manifest=json.loads((ROOT/'tools/build563_manifest.json').read_text())
  self.assertEqual(set(manifest),{'app/lib/main.dart'})
  with tempfile.TemporaryDirectory() as folder:
   temp=Path(folder);(temp/'tools').mkdir();(temp/'app/lib').mkdir(parents=True)
   for name in ['apply_build563_quality.py','build563_manifest.json','build563_quality.patch','build563_quality.dart']:shutil.copyfile(ROOT/'tools'/name,temp/'tools'/name)
   path=temp/'app/lib/main.dart';shutil.copyfile(ROOT/'app/lib/main.dart',path)
   def run(*args):return subprocess.run(args,cwd=temp,capture_output=True,text=True)
   if hashlib.sha256(path.read_bytes()).hexdigest()==manifest['app/lib/main.dart']['after']:
    p=run('git','apply','--reverse','tools/build563_quality.patch');self.assertEqual(p.returncode,0,p.stderr)
   before=path.read_text()
   for _ in range(2):
    p=run('python3','tools/apply_build563_quality.py');self.assertEqual(p.returncode,0,p.stderr)
   after=path.read_text()
   def section(s,a,b):return s[s.index(a):s.index(b,s.index(a))]
   for start,end in [('    Widget sekme(String ad,int sayi)','    Widget bildirimlerIcerigi()'),('  Future<void> _dogrulayipGonder561()', '  Future<void> yorumBegen'),('class YorumKarti','class KesfetPage')]:
    self.assertEqual(section(before,start,end),section(after,start,end))
   self.assertNotIn('KullaniciProfilPage',section(after,'    Widget bildirimlerIcerigi()','    Widget isteklerIcerigi()'))
   self.assertEqual(after.count('builder: (_) => Ngelx563CommentViewport(child:Yorumlar('),2)
   self.assertIn('stream: _yorumAkisi561',after)
   path.write_text(after+'\n// drift\n');self.assertNotEqual(run('python3','tools/apply_build563_quality.py').returncode,0)
if __name__=='__main__':unittest.main()
