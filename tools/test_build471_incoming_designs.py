"""Build471: separate native group/private designs and no ringtone regression."""
import unittest
from pathlib import Path
from apply_build471_incoming_routing import service,main,dart
ACTIVITY=Path('app/android/app/src/main/kotlin/com/nnentx/ngelx_app/IncomingCallActivity470.kt')
SERVICE=Path('app/android/app/src/main/kotlin/com/nnentx/ngelx_app/IncomingCallService.kt')
MAIN=Path('app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt')
DART=Path('app/lib/build448_incoming_calls.dart')
POLICY=Path('cloudflare/call-push/src/policy.mjs')
class Build471DesignTests(unittest.TestCase):
 def test_group_and_private_have_separate_visuals(self):
  a=ACTIVITY.read_text(encoding='utf-8')
  for term in ('val group = intent.getBooleanExtra("callGroup471", false)',
    'if (group) "NgelX üzerinden arıyor..." else "Seni NgelX üzerinden arıyor..."',
    'if (group) 154 else 142', 'if (group) Color.rgb(194, 141, 254)',
    'if (group) Color.rgb(24, 16, 51)', 'CallBackdrop471(group)',
    'if (group) {', '"Grup sesli araması"', '"Özel sesli arama"',
    '"Grup görüntülü araması"', '"Özel görüntülü arama"',
    'actionButton("Reddet", true) { respond("reject") }',
    'actionButton("Cevapla", false) { respond("answer") }',
    'LinearLayout.LayoutParams(0, 1, 1f)', 'dp(52)', 
    'setShowWhenLocked(true)', 'setTurnScreenOn(true)',
    'IncomingCallService.isStillRinging470(room)',
    'IncomingCallService.cancel(this, room)',
    'putExtra("callChat448", chat)', 'putExtra("callRoom448", room)',
    'putExtra("callAction448", action)', 'Intent.FLAG_ACTIVITY_CLEAR_TOP'):
   self.assertIn(term,a)
  self.assertNotIn('FirebaseFirestore',a)
  self.assertNotIn('FirebaseAuth',a)
  self.assertNotIn('startService(',a)
 def test_native_ringtone_transport_and_user_settings_untouched(self):
  s=SERVICE.read_text(encoding='utf-8')
  self.assertEqual(service(s),s)
  for term in ('setFullScreenIntent(fullScreenCall, true)',
    'IncomingCallActivity470::class.java', 'putExtra("callGroup471", group || isGroupChat471(context, chat))',
    'd["group"] == "true"', 'currentRecipient470(context)', 'GROUP_PREFS471',
    'isStillRinging470(room: String)', 'timer.postDelayed(timeout, 60000)',
    'ring_blocked settings:', 'RingtoneManager.getRingtone',
    'AudioManager.RINGER_MODE_NORMAL', 'manager.currentInterruptionFilter',
    'manager.notify(room.hashCode(), notification)', 'ringing.remove(room)'):
   self.assertIn(term,s)
 def test_signed_user_local_call_kind_only(self):
  m=MAIN.read_text(encoding='utf-8')
  self.assertEqual(main(m),m)
  self.assertIn('"noteChatKind471" ->',m)
  self.assertIn('IncomingCallService.rememberChatKind471(this, chat, group)',m)
  self.assertIn('call.argument<Boolean>("group") == true); result.success(null)',m)
  d=DART.read_text(encoding='utf-8')
  self.assertEqual(dart(d),d)
  self.assertIn("channel.invokeMethod<void>('noteChatKind471'",d)
  self.assertIn("'group':value['isGroup']==true",d)
  self.assertIn("'group':group",d)
  self.assertIn('caller:',d)
  self.assertIn("_ringingChat469",d)
  self.assertIn("'setCallOwner470'",d)
 def test_server_push_only_server_derived_group(self):
  policy=POLICY.read_text(encoding='utf-8')
  self.assertIn('group:String(chat.isGroup===true)',policy)
  self.assertIn("Object.keys(v).every(k=>['chatId','roomName','offset'].includes(k))",policy)
if __name__=='__main__':unittest.main()
