"""Fail-closed and non-community-invariance tests for Firestore rule merge."""
import unittest
from merge_build457_community_rules import merge_hardened_community

BEFORE="""rules_version = '2';
service cloud.firestore {
match /databases/{database}/documents {
    function signedIn() { return true; }
    function communitySigned450() { return signedIn(); }
    match /communities450/{cid} {
      allow read: if true;
      match /posts/{pid} { allow read: if true; }
    }
    match /communityInvites450/{code} { allow read: if true; }
    match /chats/{chatId} { allow read: if true; allow update: if false; }
    match /users/{uid} { allow read: if true; }
}
}
"""
PROPOSED="""rules_version = '2';
service cloud.firestore {
match /databases/{database}/documents {
    function signedIn() { return true; }
    function community450(cid) { return true; }
    function community450PostView(cid, pid) { return community450(cid); }
    match /communities450/{cid} {
      allow read: if signedIn();
      match /posts/{pid} { allow read: if community450PostView(cid,pid); }
    }
    match /communityInvites450/{code} { allow read: if signedIn(); }
    match /chats/{chatId} { allow read, update: if true; }
}
}
"""
class RuleMergeSafetyTest(unittest.TestCase):
    def test_preserves_chat_privacy_and_users_exactly(self):
        merged=merge_hardened_community(BEFORE,PROPOSED)
        self.assertIn('allow update: if false;',merged)
        self.assertIn('match /users/{uid} { allow read: if true; }',merged)
        self.assertNotIn('allow read, update: if true;',merged)
        self.assertIn('community450PostView',merged)
        self.assertEqual(merged.count('match /communities450/{cid} {'),1)

    def test_requires_exact_and_known_rule_scopes(self):
        with self.assertRaises(ValueError):
            merge_hardened_community(BEFORE.replace('communitySigned450','missing'),PROPOSED)
        with self.assertRaises(ValueError):
            merge_hardened_community(BEFORE,PROPOSED.replace(
                'function community450(cid) { return true; }',''))
        with self.assertRaises(ValueError):
            merge_hardened_community(BEFORE.replace(
                '    match /communityInvites450/{code} { allow read: if true; }',''),PROPOSED)

if __name__=='__main__':
    unittest.main()
