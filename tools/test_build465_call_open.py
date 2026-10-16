"""Incoming-call title taps must navigate, never answer a call implicitly."""
from pathlib import Path
import unittest

SOURCE=Path("app/lib/build448_incoming_calls.dart")

class IncomingOpenTests(unittest.TestCase):
    def test_title_tap_opens_chat_without_auto_answer(self):
        text=SOURCE.read_text(encoding="utf-8")
        start=text.index("if(action=='open')")
        end=text.index("if(action!='answer')return;",start)
        block=text[start:end]
        self.assertIn("ngelx445OpenCallChat",block)
        self.assertIn("'sourceId':chat",block)
        self.assertIn("return;",block)
        self.assertNotIn("callParticipants",block)
        self.assertNotIn("callStatus':'active",block)
        self.assertLess(text.index("if(action=='open')"),text.index("if(action!='answer')return;"))

if __name__=="__main__":unittest.main()
