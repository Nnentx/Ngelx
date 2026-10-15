"""Build459 checks after all Build458 source transformations."""
import unittest
from pathlib import Path
from apply_build459_profile_modes import patch as profile_patch
from apply_build459_feed_watchdog import patch as feed_patch

class Build459PreservationTests(unittest.TestCase):
    def test_cover_mode_is_not_unconditionally_hidden(self):
        main=Path("app/lib/main.dart").read_text(encoding="utf-8")
        self.assertIn("ngelx459KapaksizGorunum(profilGorunumu,kapakUrl)",main)
        self.assertNotIn("if(true) // Build458 owner coverless rendering",main)
        self.assertIn("if(_gorunum=='cover') ...[",main)
        self.assertIn("Kapaklı görünüm",main)
        self.assertIn("Kapaksız sade görünüm",main)
        self.assertIn("Foto", main)
        self.assertIn("widget.onFoto", main)
        self.assertIn("widget.onKapak",main)
        self.assertIn("NgelXHikayeliAvatar",main)
        self.assertEqual(profile_patch(main),main)

    def test_all_build458_features_are_preserved(self):
        main=Path("app/lib/main.dart").read_text(encoding="utf-8")
        live=Path("app/lib/live_broadcast_studio.dart").read_text(encoding="utf-8")
        self.assertIn("part 'community450.dart';",main)
        self.assertIn("Build458 feed retry",main)
        self.assertIn("ngelx458VideoUrl",main)
        self.assertIn("Videoyu yeniden dene",main)
        self.assertIn("Build458 bounded camera preview initialization",live)
        self.assertIn("Kamera",live)

    def test_stalled_first_frame_finishes_with_user_retry(self):
        main=Path("app/lib/main.dart").read_text(encoding="utf-8")
        self.assertIn("// Build459 feed watchdog",main)
        self.assertIn("Timer(const Duration(seconds:12)",main)
        self.assertIn("_ngelx459FirstFrameTimer?.cancel();",main)
        self.assertIn("!identical(kontrol,player)",main)
        self.assertIn("Video görüntüsü yüklenemedi.",main)
        self.assertEqual(feed_patch(main),main)

if __name__=="__main__":
    unittest.main()
