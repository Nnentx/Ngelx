import os,sys,unittest
from pathlib import Path
from apply_build547_social_call_fixes import main_source,calls_source,incoming_source,activity_source

BASE=Path(os.environ.get('BUILD547_BASELINE','app'))
class FollowUps547(unittest.TestCase):
 def test_friend_source_does_not_depend_on_notification_history(self):
  old=(BASE/'lib/main.dart').read_text();new=main_source(old)
  start=new.index('class _KesfetPageState ');end=new.index('  Future<void> _yayinIzle',start)
  state=new[start:end]
  self.assertNotIn("collection('notifications')",state)
  self.assertIn("collection('friend_requests')",state)
  self.assertIn("collection('follow_requests')",state)
  self.assertNotIn('.limit(100)',state)
  self.assertIn("where('members',arrayContains:uid)",state)
  self.assertIn("if(d.data()['active']!=true)continue",state)
  self.assertIn('_arkadasIstekleri547?.cancel()',state)
  self.assertIn('_arkadasliklar547?.cancel()',state)
  action=new[new.index('  Future<void> _arkadaslikIstegiGonder'):new.index('  Future<void> _grupDurumuDegistir',start)]
  self.assertIn("records[1].data()?['friends']",action)
  self.assertIn("records[2].data()?['status']=='pending'",action)
  self.assertIn('if(pending&&!friends)gonderilenArkadaslikIstekleri.add',action)
  self.assertIn('finally{',action)
  self.assertIn('_gonderiliyor547.remove(hedefUid)',action)
  row=new[new.index('  Widget _kisiSatiri(String uid'):new.index('  Widget _toplulukSatiri',new.index('  Widget _kisiSatiri(String uid'))] if '  Widget _toplulukSatiri' in new else new[new.index('  Widget _kisiSatiri(String uid'):][:6000]
  self.assertIn("v['friends']",row)
  self.assertIn('hesapYukleniyor||_isteklerYukleniyor547||arkadas547||bekliyor547?null',row)
  self.assertEqual(main_source(new),new)
 def test_only_private_banner_removed(self):
  old=(BASE/'lib/main.dart').read_text();new=main_source(old)
  self.assertEqual(new.count('Sesli arama devam ediyor'),old.count('Sesli arama devam ediyor')-1)
  # Call setup, message delivery and global mini-window control are untouched.
  a=old.index("      if(ngelx440CallJoinable(veri,DateTime.now()))",old.index('class _SohbetPageState'))
  b=old.index('      Expanded(child:StreamBuilder<QuerySnapshot',a)
  strip=old[a:b]
  for guard in ['aramaBaslat(false)','aramaBaslat(true)','_mesajAkisi','ngelx446Calls','_media448']:
   self.assertEqual(new.count(guard),old.count(guard)-strip.count(guard))
 def test_native_auth_and_lifecycle_stay_guarded(self):
  root=BASE/'android/app/src/main/kotlin/com/nnentx/ngelx_app'
  old=(root/'IncomingCallActivity470.kt').read_text();new=incoming_source(old)
  for guard in ['respond("answer")','respond("reject")','IncomingCallService.cancel(this, room)','timer.postDelayed(check, 1000)','instanceFollowRedirects=false']:
   self.assertEqual(new.count(guard),old.count(guard))
  self.assertIn('photoExecutor547.execute',new)
  self.assertIn('frame.tag=="remote547"',new)
  self.assertIn('photoExecutor547.shutdownNow()',new)
  self.assertIn('currentUser?.uid!=uid',new)
  self.assertEqual(incoming_source(new),new)
  activity=(root/'MainActivity.kt').read_text()
  self.assertEqual(activity_source(activity).count('"noteChatKind471"'),activity.count('"noteChatKind471"'))
 def test_warmup_is_cache_only_and_account_scoped(self):
  old=(BASE/'lib/build448_incoming_calls.dart').read_text();new=calls_source(old)
  warm=new[new.index('  Future<void> _warmPhoto547'):new.index('  bool _registering453')]
  self.assertNotIn('Source.server',warm)
  self.assertNotIn('getSingleFile',warm)
  self.assertNotIn('downloadFile',warm)
  self.assertIn('Source.cache',warm)
  self.assertIn('currentUser?.uid!=uid',warm)
  self.assertEqual(calls_source(new),new)
  cache=Path('tools/build547_call_photo.kt').read_text()
  for guard in ['cacheDir.canonicalPath','age>24L*60*60*1000','file.length()>2097152','inSampleSize=sample','drop(79)']:
   self.assertIn(guard,cache)
if __name__=='__main__':unittest.main()
