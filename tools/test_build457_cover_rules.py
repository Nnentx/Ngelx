import unittest
from apply_build457_cover_rules import OLD,transform

class CoverRule457(unittest.TestCase):
    def test_adds_narrow_founder_cover_only_rule(self):
        sample='rules start\n'+OLD+'          || (someOtherCondition)\n'
        fixed=transform(sample)
        self.assertIn("hasOnly(['coverUrl','coverAlignment'])",fixed)
        self.assertEqual(fixed.count("founderId\n            && request.resource.data.diff"),1)
        self.assertEqual(transform(fixed),fixed)

    def test_fails_for_unexpected_rules(self):
        with self.assertRaises(ValueError):
            transform('not the expected community rules')

if __name__=='__main__':
    unittest.main()
