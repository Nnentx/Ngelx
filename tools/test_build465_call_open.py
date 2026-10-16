"""Incoming-call title must open its authorized conversation, not a second dialog."""
from pathlib import Path
import unittest

CHAT=Path("app/lib/build454_widgets.dart")
ANDROID=Path("app/lib/build448_incoming_calls.dart")

class IncomingOpenTests(unittest.TestCase):
    def test_title_tap_routes_to_chat_without_sheet_or_auto_answer(self):
        text=CHAT.read_text(encoding="utf-8")
        block=text.split("Future<void> ngelx454OpenIncoming(",1)[1].split("Future<void> ngelx454RemoveHighlight(",1)[0]
        self.assertIn("ngelx445OpenCallChat",block)
        self.assertIn("'sourceId':chat",block)
        self.assertNotIn("showModalBottomSheet",block)
        self.assertNotIn("callParticipants",block)
        self.assertNotIn("action':'answer'",block)
        self.assertNotIn("action':'reject'",block)
    def test_original_acceptance_path_is_retained(self):
        text=ANDROID.read_text(encoding="utf-8")
        self.assertIn("if(action!='answer')return;",text)
        self.assertIn("'callParticipants':FieldValue.arrayUnion([me])",text)

if __name__=="__main__":unittest.main()
