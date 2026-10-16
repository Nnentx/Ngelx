"""Regression checks for scoped Build467 generated UI (not device QA)."""
import unittest
from pathlib import Path
from apply_build467_chat_ui import transform as chat_transform
from apply_build467_ringtone import transform as ringtone_transform

MAIN=Path('app/lib/main.dart')
SERVICE=Path('app/android/app/src/main/kotlin/com/nnentx/ngelx_app/IncomingCallService.kt')

class Build467LayoutTests(unittest.TestCase):
    def test_generated_chat_patch_is_idempotent_and_targeted(self):
        source=MAIN.read_text(encoding='utf-8')
        self.assertEqual(chat_transform(source),source)
        self.assertIn('// Build467: common bounded photo',source)
        self.assertIn('maxHeight:math.min(390.0',source)
        self.assertIn('// Build467: reactions float outside text bubble',source)
        self.assertIn('child:_ozelMedyaTepkiBalonu(d.reference,sayilar,tepkiler.length)',source)
        self.assertTrue(
            'minimum:const EdgeInsets.only(bottom:7)' in source
            or ('// Build468: explicit Android nav-safe composer slot' in source
                and 'bottomNavigationBar:ColoredBox(' in source
                and 'SafeArea(top:false,bottom:false,child:Container(' in source)
        )
        self.assertEqual(source.count('if(!mounted||++ticks>3)'),2)
        self.assertIn('extendBodyBehindAppBar:true',source)
        # Preserve all user interaction handlers, including media and calls.
        for unchanged in ('onDoubleTap:()=>mesajTepkiDegistir(d,quickReaction)',
                          'medyaGonder(ImageSource.camera)',
                          'medyaGonder(ImageSource.gallery)',
                          'onPressed:sesKaydiDegistir',
                          'onPressed:emojiSec',
                          'onPressed:gonderiliyor?null:gonder',
                          '_aramaEkraniniKucult()async'):
            self.assertIn(unchanged,source)

    def test_notification_channel_changed_but_ringer_respects_user_settings(self):
        service=SERVICE.read_text(encoding='utf-8')
        self.assertEqual(ringtone_transform(service),service)
        self.assertIn('ngelx_incoming_calls467',service)
        for required in ('NotificationManager.IMPORTANCE_HIGH',
                         'AudioManager.RINGER_MODE_NORMAL',
                         'Notification.FLAG_INSISTENT','sound.play()',
                         'ringing.remove(room)'):
            self.assertIn(required,service)

if __name__=='__main__':
    unittest.main()
