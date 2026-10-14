"""Build457: nickname map keys are target UID in the *generated* app."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class NicknameSemantics457(unittest.TestCase):
    def test_generated_chat_uses_target_uid_consistently(self):
        content=(ROOT/'app/lib/main.dart').read_text()
        inbox=content.split("class _MesajPageState",1)[1].split(
            "class ArsivSohbetlerPage",1)[0]
        self.assertTrue(
            "takma=(takmalar[other]??'').toString().trim()" in inbox,
            "Inbox must read nickname by its TARGET UID")
        self.assertTrue(
            "'nicknames':{uid:" in content,
            "Generated nickname editor must store nickname by target UID")
        self.assertTrue(
            "takma=(nicks[widget.digerUid]??'').toString().trim()" in content,
            "Chat header should use the same target UID as inbox")

    def test_generator_keeps_target_uid_mapping(self):
        source=(ROOT/'tools/apply_build455.py').read_text()
        self.assertTrue(
            "takma=(takmalar[other]??'').toString().trim()" in source)

if __name__=="__main__":
    unittest.main()
