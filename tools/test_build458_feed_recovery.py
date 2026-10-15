"""Build458 feed player regression checks after all generated patches."""
import unittest
from pathlib import Path
from apply_build458_feed_recovery import patch

class Build458FeedPlayerTests(unittest.TestCase):
    def test_no_infinite_feed_spinner_and_recovery(self):
        s=Path("app/lib/main.dart").read_text()
        a=s.index("class _VideoKartiState extends State<VideoKarti>")
        b=s.index("\nclass ",a+len("class _VideoKartiState"))
        frag=s[a:b]
        self.assertIn("// Build458 feed retry",frag)
        self.assertIn("await kontrol.initialize().timeout(const Duration(seconds:12))",frag)
        self.assertIn("VideoPlayerController.networkUrl(Uri.parse(widget.adres))",frag)
        self.assertIn("eski.removeListener(_kesimKontrol);",frag)
        self.assertIn("await eski.dispose().timeout",frag)
        self.assertIn("Videoyu yeniden dene",frag)
        self.assertIn("_videoyuTekrarDene()",frag)
        self.assertEqual(patch(s),s)

if __name__=="__main__":
    unittest.main()
