"""Deterministic source-regression tests for Build457 inbox identity isolation."""
import unittest
from apply_build457_inbox_identity import FIELD_OLD, ROW_OLD, transform

class TestInbox457(unittest.TestCase):
    def test_identity_bound_rows_and_no_self_fallback(self):
        source=("start\nclass _MesajPageState extends State<MesajPage> {\n"
               +FIELD_OLD+"\n"+ROW_OLD+"\n}\nclass ArsivSohbetlerPage\n")
        changed=transform(source)
        self.assertIn("ValueKey<String>('inbox-person-",changed)
        self.assertIn("u.data!.id!=other",changed)
        self.assertIn("if(other.isEmpty||other==ben)",changed)
        self.assertNotIn("orElse:()=>ben??''",changed)
        self.assertIn("_inbox457Profiles.putIfAbsent(uid",changed)
        self.assertEqual(transform(changed),changed)

    def test_unknown_legacy_renderer_is_not_modified(self):
        source=("class _MesajPageState extends State<MesajPage> {\n"
                +FIELD_OLD+"\n}\nclass ArsivSohbetlerPage\n")
        self.assertEqual(transform(source),source)

if __name__=="__main__":
    unittest.main()
