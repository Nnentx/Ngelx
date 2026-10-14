import unittest
from apply_build457_live_recovery import HELPER, METHOD, FALLBACK_OLD, transform

class TestLive457(unittest.TestCase):
    def test_post_patch_fallback_is_finite(self):
        source=("class _CanliYayinPageState extends State<CanliYayinPage> {\n"
                +"late final _liveStream448 = 1;\n"
                +"  Widget _goruntuYokEkrani(){\n"+FALLBACK_OLD+"\n"
                +"  Widget build() {\n    final track = _goruntu();\n  }\n}")
        changed=transform(source)
        self.assertIn("valueListenable: _clock448",changed)
        self.assertIn("elapsedWithoutVideoSeconds: seconds - _lastVisibleVideoSecond",changed)
        self.assertIn("Yayına yeniden bağlan",changed)
        self.assertIn("Kamerayı yeniden başlat",changed)
        self.assertEqual(changed,transform(changed))

    def test_reject_unexpected_source(self):
        with self.assertRaises(ValueError):
            transform("class _CanliYayinPageState extends State<CanliYayinPage> {}")

if __name__=="__main__":
    unittest.main()
