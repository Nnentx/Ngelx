"""Build458 offline camera/profil guards, without touching real user data."""
import unittest
from pathlib import Path
from apply_build458_camera_profile import camera_patch, owner_profile_patch

class Build458DeviceRegression(unittest.TestCase):
    def test_bounded_camera_retry_and_cleanup(self):
        source = Path("app/lib/live_broadcast_studio.dart").read_text()
        self.assertIn("// Build458 bounded camera preview initialization", source)
        self.assertIn("await denenen.initialize().timeout(const Duration(seconds:8))", source)
        self.assertIn("await denenen.dispose().timeout(const Duration(seconds:3))", source)
        self.assertIn("kameralar = await availableCameras().timeout", source)
        self.assertIn("return;", source)
        self.assertIn("_onizlemeIslemde = false;", source)
        self.assertEqual(camera_patch(source), source)

    def test_owner_profile_coverless_without_deleting_cover(self):
        source=Path("app/lib/main.dart").read_text()
        start=source.index("class _ProfilPageState extends State<ProfilPage>")
        end=source.index("\nclass _ProfilEtkilesimRozeti",start)
        owner=source[start:end]
        self.assertIn("if(true) // Build458 owner coverless rendering",owner)
        self.assertIn("_onayliKapaksizBaslik()",owner)
        self.assertIn("NgelXHikayeliAvatar(",owner)
        self.assertIn("fotoUrl:fotoUrl",owner)
        self.assertIn("fotografYukle",owner)
        self.assertEqual(owner_profile_patch(source),source)

if __name__=="__main__":
    unittest.main()
