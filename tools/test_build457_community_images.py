import unittest
from apply_build457_community_images import OLD,transform

class CommunityImage457(unittest.TestCase):
    def test_placeholder_and_retry(self):
        source="header\n"+OLD+"\nfooter"
        changed=transform(source)
        self.assertIn("placeholder: SizedBox(",changed)
        self.assertIn("retryErrorBuilder: (context, error, retry)",changed)
        self.assertIn("onTap: retry",changed)
        self.assertEqual(transform(changed),changed)

    def test_refuse_unknown_image_api(self):
        with self.assertRaises(ValueError):
            transform("bad source")

if __name__=="__main__":
    unittest.main()
