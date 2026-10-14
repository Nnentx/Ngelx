"""Build457 regression: a chat nickname belongs to the viewer who saved it."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / 'app/lib/main.dart'
APPLY455 = ROOT / 'tools/apply_build455.py'

class TestNicknameScope457(unittest.TestCase):
    def test_inbox_reads_nickname_key_saved_by_this_user(self):
        text = MAIN.read_text()
        section = text.split("class _MesajPageState",1)[1].split(
            "class ArsivSohbetlerPage",1)[0]
        self.assertIn(
            "takma=(ben==null?'':(takmalar[ben]??'').toString()).trim()",
            section,
            "The inbox must read the nickname stored under the viewer UID.")
        self.assertNotIn("takma=(takmalar[other]??'').toString().trim()",section)
        self.assertIn("'nicknames.$me':",text,
            "The nickname editor must still write under the viewer UID.")

    def test_legacy_build455_must_not_reintroduce_bug(self):
        source=APPLY455.read_text()
        self.assertNotIn("takma=(takmalar[other]??'').toString().trim()",source)
        self.assertIn("viewer-scoped reader",source)

if __name__ == '__main__':
    unittest.main()
