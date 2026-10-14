"""Build457 regression for UID-isolated inbox rows."""
import unittest
from apply_build457_inbox_rows import LOOKUP,OTHER,BUILDER,transform

class InboxRows457(unittest.TestCase):
    def test_private_row_fail_closed(self):
        source=("class _MesajPageState extends State<MesajPage> {\n"
                "                  "+OTHER+"\n"
                "                  return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(\n"
                "                    "+LOOKUP+",\n"
                "                    "+BUILDER+"\n"
                "                      final p=u.data?.data()??{};\n"
                "                    });\n"
                "}\nclass ArsivSohbetlerPage\n")
        changed=transform(source)
        self.assertIn("if(other.isEmpty||other==ben||!members.contains(ben))",changed)
        self.assertIn("inbox-uid457-",changed)
        self.assertIn("if(u.data!.id!=other)",changed)
        self.assertIn("_profiles453.remove(other)",changed)
        self.assertEqual(transform(changed),changed)

    def test_unknown_generated_row_refused(self):
        with self.assertRaises(ValueError):
            transform("class _MesajPageState {} class ArsivSohbetlerPage")

if __name__=="__main__":
    unittest.main()
