from pathlib import Path
import hashlib,json,shutil,subprocess,tempfile,unittest,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
class Build564(unittest.TestCase):
 def test_replay_scoped_native_permissions_and_source_preservation(self):
  tools=ROOT/'tools';manifest=json.loads((tools/'build564_manifest.json').read_text())
  with tempfile.TemporaryDirectory() as folder:
   temp=Path(folder);(temp/'tools').mkdir()
   for name in ['apply_build564_update.py','build564_manifest.json','build564_update.patch','build564_update.dart','Ngelx564Updater.kt','update_paths564.xml']:shutil.copyfile(tools/name,temp/'tools'/name)
   for path in manifest:
    target=temp/path;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/path,target)
   def run(*args):return subprocess.run(args,cwd=temp,text=True,capture_output=True)
   if all(hashlib.sha256((temp/p).read_bytes()).hexdigest()==v['after'] for p,v in manifest.items()):
    result=run('git','apply','--reverse','tools/build564_update.patch');self.assertEqual(result.returncode,0,result.stderr)
   before={p:(temp/p).read_bytes() for p in manifest}
   for _ in range(2):
    result=run('python3','tools/apply_build564_update.py');self.assertEqual(result.returncode,0,result.stderr)
   main=(temp/'app/lib/main.dart').read_text();old=before['app/lib/main.dart'].decode()
   def section(s,a,b):return s[s.index(a):s.index(b,s.index(a))]
   self.assertEqual(section(old,'class _IcerikBaglantiPageState','class UygulamaDurumKapisi'),section(main,'class _IcerikBaglantiPageState','class UygulamaDurumKapisi'))
   self.assertEqual(section(old,'class Yorumlar','class KesfetPage'),section(main,'class Yorumlar','class KesfetPage'))
   self.assertEqual(section(old,'    Widget bildirimlerIcerigi()','    Widget isteklerIcerigi()'),section(main,'    Widget bildirimlerIcerigi()','    Widget isteklerIcerigi()'))
   ns='{http://schemas.android.com/apk/res/android}'
   xml=ET.parse(temp/'app/android/app/src/main/AndroidManifest.xml')
   provider=next(p for p in xml.findall('.//provider') if p.get(ns+'authorities')=='${applicationId}.updates564')
   self.assertEqual(provider.get(ns+'exported'),'false');self.assertEqual(provider.get(ns+'grantUriPermissions'),'true')
   paths=ET.parse(tools/'update_paths564.xml').getroot();self.assertEqual([(x.tag,x.get('path')) for x in paths],[('cache-path','ngelx_updates/')])
   native=(tools/'Ngelx564Updater.kt').read_text()
   for check in ['file.parentFile == directory.canonicalFile','file.length() == size','apk.packageName == activity.packageName','code(apk) > code(current)','signatures(apk) == expected','ACTION_MANAGE_UNKNOWN_APP_SOURCES','FLAG_GRANT_READ_URI_PERMISSION']:self.assertIn(check,native)
   path=temp/'app/lib/main.dart';path.write_text(main+'\n// drift');self.assertNotEqual(run('python3','tools/apply_build564_update.py').returncode,0)
if __name__=='__main__':unittest.main()
