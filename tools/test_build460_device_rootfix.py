"""Build460 regression after all prior transforms, no user-data mutations."""
import unittest
from pathlib import Path
from apply_build460_profile_save import patch as profile_patch
from apply_build460_image_status import patch as image_patch
from apply_build460_video_fallback import patch as video_patch

class Build460DeviceRegressionTests(unittest.TestCase):
    def test_legacy_turkish_username_does_not_block_profile_mode(self):
        s=Path("app/lib/main.dart").read_text(encoding="utf-8")
        a=s.index("  Future<void> _kaydet(String kapak)async{")
        b=s.index("  Future<void> _kapagiKaldir()async{",a)
        method=s[a:b]
        self.assertIn("// Build460 identity-preserving mode save",method)
        self.assertIn("final changeUsername=kullanici!=priorUsername;",method)
        self.assertIn("if(changeUsername){",method)
        self.assertIn("kayit['usernameLower']=kullanici.toLowerCase();",method)
        self.assertIn("'profileViewMode':_gorunum,",method)
        self.assertIn("SetOptions(merge:true)",method)
        self.assertNotIn("if(ad.length<2||!RegExp",method)
        self.assertEqual(profile_patch(s),s)

    def test_cover_error_has_finite_wait_and_safe_retry(self):
        s=Path("app/lib/main.dart").read_text(encoding="utf-8")
        self.assertIn("// Build460 bounded remote image",s)
        self.assertIn("_ngelxAgResmiBaytlari(key.url).timeout(const Duration(seconds:18))",s)
        self.assertIn("Kapak yüklenemedi - tekrar dene",s)
        self.assertIn("retryErrorBuilder:(ctx,error,retry)",s)
        self.assertEqual(image_patch(s),s)

    def test_video_retry_can_rotate_legacy_media_urls(self):
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

    def test_build458_and_459_integrations_preserved(self):
        s=Path("app/lib/main.dart").read_text(encoding="utf-8")
        live=Path("app/lib/live_broadcast_studio.dart").read_text(encoding="utf-8")
        self.assertIn("part 'community450.dart';",s)
        self.assertIn("Build458 feed retry",s)
        self.assertIn("Build458 bounded camera preview initialization",live)
        self.assertIn("ngelx459KapaksizGorunum",s)
        self.assertIn("NgelXOnayliProfilDuzenlePage",s)

if __name__=="__main__":unittest.main()
