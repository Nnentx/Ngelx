"""Source regression gate for the bounded Build456 Firestore index fallback."""
import unittest
from apply_build456_feed_fallback import FEED_OLD, FEED_NEW, SORT_OLD, SORT_NEW, transform

class Build456FeedFallbackTest(unittest.TestCase):
    def test_bounded_fallback_and_ordering(self):
        source = "header\n" + FEED_OLD + "\nother\n" + SORT_OLD + "\nend"
        changed = transform(source)
        self.assertIn("error.code != 'failed-precondition'", changed)
        self.assertIn(".limit((postLimit * 3).clamp(20, 120).toInt())", changed)
        self.assertNotIn("yield* approved.snapshots()", changed)
        self.assertIn("return bTime.compareTo(aTime);", changed)
        self.assertEqual(transform(changed), changed)

    def test_refuses_unknown_source(self):
        with self.assertRaises(RuntimeError):
            transform("unrelated source")

if __name__ == '__main__':
    unittest.main()
