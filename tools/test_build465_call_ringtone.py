"""Build465 call notification regression checks (no device or Firebase access)."""
from pathlib import Path
import unittest
from apply_build465_ringtone_channel import transform as ringtone_transform

ANDROID = Path("app/android/app/src/main")
SERVICE = ANDROID / "kotlin/com/nnentx/ngelx_app/IncomingCallService.kt"
MANIFEST = ANDROID / "AndroidManifest.xml"

class CallRingtoneTests(unittest.TestCase):
    def test_android13_notification_permission_exists(self):
        xml=MANIFEST.read_text(encoding="utf-8")
        self.assertIn('android.permission.POST_NOTIFICATIONS',xml)
        self.assertEqual(xml.count('android.permission.POST_NOTIFICATIONS'),1)
    def test_incoming_call_has_distinct_high_priority_ringing_channel(self):
        kotlin=SERVICE.read_text(encoding="utf-8")
        generated=ringtone_transform(kotlin)
        self.assertIn('ngelx_incoming_calls465',generated)
        self.assertEqual(generated,ringtone_transform(generated))
        self.assertIn('NotificationManager.IMPORTANCE_HIGH',kotlin)
        self.assertIn('setSound(ringtone',kotlin)
        self.assertIn('AudioAttributes.USAGE_NOTIFICATION_RINGTONE',kotlin)
        self.assertIn('Notification.FLAG_INSISTENT',kotlin)
        self.assertIn('setContentIntent(action("open"))',kotlin)
        self.assertIn('action("answer")',kotlin)
        self.assertIn('action("reject")',kotlin)
    def test_notification_title_does_not_join_call(self):
        dart=Path("app/lib/build448_incoming_calls.dart").read_text(encoding="utf-8")
        navigation=dart.split("if(action=='open'){",1)[1].split("if(action!='answer')",1)[0]
        self.assertIn('ngelx445OpenCallChat',navigation)
        self.assertNotIn("callParticipants",navigation)

if __name__=="__main__":
    unittest.main()
