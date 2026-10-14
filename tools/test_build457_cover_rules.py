import unittest
from apply_build457_cover_rules import OLD,transform

class CoverRule457(unittest.TestCase):
    def test_founder_legacy_exception_has_only_cover_fields(self):
        source='prefix\nmatch /communities450/{cid} {\n'+OLD+'\n'
        changed=transform(source)
        self.assertIn("request.auth.uid == resource.data.founderId",changed)
        self.assertIn("request.auth.uid in resource.data.members",changed)
        self.assertIn("hasOnly(['coverUrl','coverAlignment'])",changed)
        self.assertIn("coverAlignment',0) <= 1",changed)
        self.assertIn("request.resource.data.coverUrl.size() <= 2048",changed)
        self.assertEqual(transform(changed),changed)

    def test_fails_closed_for_unexpected_rules_source(self):
        with self.assertRaises(ValueError):
            transform("unexpected rules source")

if __name__=='__main__':
    unittest.main()
