"""Source-only safety tests for post-Build456 community fixes."""
import unittest
from apply_build457_community_runtime_fixes import (
    community_fix,counts_fix,OLD_FOUNDER,NEW_FOUNDER,
    LOAD_START,LOAD_END,NEW_LOAD,LIVE_FIRST,SERVER_FIRST,
)

class CommunityRuntime457(unittest.TestCase):
    def test_legacy_founder_preserves_admin_lookup(self):
        result=community_fix(OLD_FOUNDER)
        self.assertIn("v['founderId'] == _communityUid450",result)
        self.assertIn("List<String>.from(v['admins']",result)
        self.assertEqual(community_fix(result),result)

    def test_comments_use_fresh_counts_over_stale_zero(self):
        existing=(
            LOAD_START+"\n"
            "    if (['likes','comments','shares','views'].every(widget.liveCounts.containsKey))\n"
            "      return widget.liveCounts.map((k, v) => MapEntry(k,(v as num).toInt()));\n"
            "    final keys = ['likes', 'comments', 'shares', 'views'];\n"
            "    final values = await Future.wait(keys.map((k) => widget.ref.collection(k).count().get()));\n"
            "    return {};\n"
            "  }\n"+LOAD_END+"\n"
            + LIVE_FIRST
        )
        result=counts_fix(existing)
        self.assertIn(NEW_LOAD,result)
        self.assertIn(SERVER_FIRST,result)
        self.assertNotIn(LIVE_FIRST,result)
        self.assertEqual(counts_fix(result),result)

    def test_drift_refused(self):
        with self.assertRaises(ValueError):
            community_fix('bool _communityAdmin450()=>true;')
        with self.assertRaises(ValueError):
            counts_fix(LOAD_START+LOAD_END)

if __name__=='__main__':
    unittest.main()
