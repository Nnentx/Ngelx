"""Regression checks for Build461 device profile and black-video diagnostics.

Run after Build460 transform + Build461 patches.
"""
import unittest
from pathlib import Path
from apply_build461_cover_state import patch as cover_patch
from apply_build461_video_errors import patch as video_patch

class Build461RegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src=Path("app/lib/main.dart").read_text(encoding="utf-8")

    def test_mode_does_not_depend_on_missing_cover_photo(self):
        s=self.src
        self.assertIn("// Build461 owner mode not inferred from image URL",s)
        self.assertIn("profilGorunumu!='cover';",s)
        self.assertIn("ngelx461BaslangicProfilGorunumu(widget.ilkGorunum)",s)
        self.assertNotIn("_gorunum=widget.ilkGorunum=='coverless'||widget.ilkKapakUrl.isEmpty",s)
        self.assertNotIn("Kapaklı görünüm için önce bir kapak fotoğrafı ekle.",s)
        self.assertEqual(cover_patch(s),s)

    def test_actual_cover_spinner_replaced_in_editor_not_elsewhere(self):
        s=self.src
        a=s.index("class _NgelXOnayliProfilDuzenlePageState")
        b=s.index("\nclass ProfilPage extends StatefulWidget",a)
        editor=s[a:b]
        self.assertIn("child:cover.isNotEmpty?NgelXAgResmi(",editor)
        self.assertIn("Kapak açılamadı - tekrar dene",editor)
        self.assertIn("retryErrorBuilder:(ctx,error,retry)",editor)
        self.assertIn("onTap:retry",editor)
        self.assertNotIn("child:cover.isNotEmpty?Image(",editor)

    def test_profile_save_shows_permission_code_not_raw_user_data(self):
        s=self.src
        self.assertIn("e.code=='permission-denied'",s)
        self.assertIn("Profil izni reddedildi (permission-denied).",s)
        self.assertIn("if(changeUsername)",s)
        self.assertIn("'profileViewMode':_gorunum,",s)

    def test_video_error_classifier_and_retry(self):
        s=self.src
        self.assertIn("// Build461 video error report",s)
        self.assertIn("V461-404",s)
        self.assertIn("V461-FORMAT",s)
        self.assertIn("V461-AG",s)
        self.assertIn("kontrol.value.hasError",s)
        self.assertIn("identical(kontrol,hataliKontrol)",s)
        self.assertIn("V461-KARE",s)
        self.assertIn("Videoyu yeniden dene",s)
        self.assertIn("part 'community450.dart';",s)
        self.assertEqual(video_patch(s),s)

if __name__=="__main__":
    unittest.main()
