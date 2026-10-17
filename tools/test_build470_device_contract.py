"""Build470: preserve call security and messaging while providing native incoming UX."""
from pathlib import Path
import unittest
from apply_build470_native_incoming import patch_manifest,patch_service,patch_main
from apply_build470_chat_performance import patch_main as patch_chat,patch_incoming
ROOT=Path('app')
SERVICE=ROOT/'android/app/src/main/kotlin/com/nnentx/ngelx_app/IncomingCallService.kt'
MANIFEST=ROOT/'android/app/src/main/AndroidManifest.xml'
NATIVE=ROOT/'android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt'
ACTIVITY=ROOT/'android/app/src/main/kotlin/com/nnentx/ngelx_app/IncomingCallActivity470.kt'
INCOMING=ROOT/'lib/build448_incoming_calls.dart'
MAIN=ROOT/'lib/main.dart'
class Build470CallAndPerformanceTests(unittest.TestCase):
    def test_native_fullscreen_is_declared_and_valid(self):
        s=MANIFEST.read_text()
        self.assertEqual(patch_manifest(s),s)
        self.assertIn('android.permission.USE_FULL_SCREEN_INTENT',s)
        self.assertIn('android.permission.POST_NOTIFICATIONS',s)
        self.assertIn('android:name=".IncomingCallActivity470"',s)
        self.assertIn('android:exported="false"',s)
        self.assertIn('com.google.firebase.MESSAGING_EVENT',s)
        activity=ACTIVITY.read_text()
        for guard in ('setShowWhenLocked(true)','setTurnScreenOn(true)',
          'IncomingCallService.cancel(this, room)','"Reddet"','"Cevapla"',
          'IncomingCallService.isStillRinging470(room)',
          'Intent.FLAG_ACTIVITY_CLEAR_TOP','"callChat448"','"callRoom448"'):
            self.assertIn(guard,activity)
        self.assertNotIn('FirebaseFirestore',activity)
    def test_native_push_owner_and_notification_are_protected(self):
        s=SERVICE.read_text()
        self.assertEqual(patch_service(s),s)
        for guard in ('// Build470: Android platform incoming call UI and owner fallback',
          'val signedIn = currentRecipient470(this)', 
          'FirebaseAuth.getInstance().currentUser?.uid',
          'age > 72L*60L*60L*1000L',
          'IncomingCallActivity470::class.java',
          '.setFullScreenIntent(fullScreenCall, true)',
          '.setContentIntent(fullScreenCall)',
          'Notification.CATEGORY_CALL',
          'NotificationManager.IMPORTANCE_HIGH',
          'ringing.remove(room)','manager.currentInterruptionFilter',
          'RingtoneManager.getRingtone'):
             self.assertIn(guard,s)
        self.assertNotIn('Log.i("NgelxIncoming", "recipientUid',s)
        m=NATIVE.read_text()
        self.assertEqual(patch_main(m),m)
        self.assertIn('"setCallOwner470"',m)
        self.assertIn('IncomingCallService.rememberOwner470(this, owner)',m)
        self.assertIn('"pendingAction"',m)
    def test_private_keyboard_no_immediate_firestore_work(self):
        s=MAIN.read_text()
        self.assertEqual(patch_chat(s),s)
        part=s.split('class _SohbetPageState',1)[1].split('class NgelXSesliMesaj',1)[0]
        keypath=part.split('  void mesajDegisti(String deger){',1)[1].split('  void _ngelx470ProcessComposer',1)[0]
        self.assertIn('PrivateDraftStore.schedule(widget.chatId,deger)',keypath)
        self.assertIn('_ngelx465StopOpeningBottom()',keypath)
        self.assertIn('Duration(milliseconds:120)',keypath)
        self.assertNotIn('FirebaseFirestore',keypath)
        self.assertIn('_ngelx470ComposerTick?.cancel()',part)
        self.assertIn('onChanged:mesajDegisti',part)
    def test_inbox_last_real_profile_while_reconnecting(self):
        s=MAIN.read_text()
        part=s.split('class _MesajPageState',1)[1].split('class ArsivSohbetlerPage',1)[0]
        for guard in ("_ngelx470VerifiedProfiles", "final profileKey470='$ben|$other';",
         "final verified470=_ngelx470VerifiedProfiles[profileKey470];",
         "if(!u.hasData&&verified470==null)",
         "_profiles453.putIfAbsent(other",
         "title:Text('Kişi bilgisi yükleniyor…')",
         "if(u.hasData&&u.data!.id!=other)"):
            self.assertIn(guard,part)
        self.assertNotIn('Map<String,dynamic> cachedGlobal470',part)
    def test_auth_account_switch_updates_cold_call_owner(self):
        s=INCOMING.read_text()
        self.assertEqual(patch_incoming(s),s)
        self.assertIn("channel.invokeMethod<void>('setCallOwner470',{'uid':user?.uid})",s)
        self.assertIn("channel.invokeMethod<void>('cancelAll454')",s)
        self.assertIn('_account455=user?.uid',s)
if __name__=='__main__':
    unittest.main()
