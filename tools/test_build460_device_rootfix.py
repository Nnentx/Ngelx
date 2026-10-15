"""Build460 regression after 459 build transformations.

Tests guard the targeted fixes and prevent deleting/changing user data paths.
"""
import unittest
from pathlib import Path
from apply_build460_profile_save import patch as profile_patch
from apply_build460_image_status import patch as image_patch
from apply_build460_video_fallback import patch as video_patch

class Build460DeviceRegressionTests(unittest.TestCase):
    def test_profile_appearance_saves_without_rewriting_identity(self):
        s=Path("app/lib/main.dart").read_text(encoding="utf-8")
        self.assertIn("// Build460 save only fields actually edited",s)
        self.assertIn("if(ad!=priorAd)kayit['displayName']=ad;",s)
        self.assertIn("if(kullanici!=priorUsername)kayit['username']=kullanici;",s)
        self.assertIn("'profileViewMode':_gorunum,",s)
        self.assertIn("SetOptions(merge:true)",s)
        self.assertEqual(profile_patch(s),s)

    def test_cover_error_has_finite_wait_and_retry(self):
        s=Path("app/lib/main.dart").read_text(encoding="utf-8")
        self.assertIn("// Build460 bounded remote image",s)
        self.assertIn("_ngelxAgResmiBaytlari(key.url).timeout(const Duration(seconds:18))",s)
        self.assertIn("Kapak yüklenemedi - tekrar dene",s)
        self.assertIn("retryErrorBuilder:(ctx,error,retry)",s)
        self.assertEqual(image_patch(s),s)

    def test_video_retry_uses_alternative_saved_media_and_host(self):
        s=Path("app/lib/main.dart").read_text(encoding="utf-8")
        self.assertIn("// Build460 video fallback URLs",s)
        self.assertIn("final String alternatifAdres;",s)
        self.assertIn("ngelxMedyaUrlAdaylari(normalized)",s)
        self.assertIn("_ngelx460KaynakIndex=(_ngelx460KaynakIndex+1)%candidates.length;",s)
        self.assertIn("alternatifAdres:(v['mediaUrl']??'').toString()",s)
        self.assertIn("alternatifAdres:(item['mediaUrl']??'').toString()",s)
        self.assertIn("if(!ilerledi){",s)
        self.assertIn("Video görüntüsü yüklenemedi.",s)
        self.assertEqual(video_patch(s),s)

    def test_unchanged_features_are_still_in_code(self):
        s=Path("app/lib/main.dart").read_text(encoding="utf-8")
        live=Path("app/lib/live_broadcast_studio.dart").read_text(encoding="utf-8")
        self.assertIn("part 'community450.dart';",s)
        self.assertIn("Build458 feed retry",s)
        self.assertIn("Build458 bounded camera preview initialization",live)
        self.assertIn("ngelx459KapaksizGorunum",s)
        self.assertIn("NgelXOnayliProfilDuzenlePage",s)

if __name__=="__main__":unittest.main()
