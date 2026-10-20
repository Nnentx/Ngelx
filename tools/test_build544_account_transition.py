import unittest
from pathlib import Path
from apply_build544_call_cleanup import main, behavior, pending, transform

class CleanupRegression(unittest.TestCase):
    def test_generated_auth_transition_is_serialized_before_token_change(self):
        source=Path('app/lib/main.dart').read_text()
        result=transform(source,main)
        self.assertEqual(result,transform(result,main))
        auth=result[result.index('Future<UserCredential> ngelx439EmailSignIn'):]
        self.assertLess(auth.index('await ngelx544BeforeAccountChange()'),auth.index('return FirebaseAuth.instance.signInWithEmailAndPassword'))
        for name in ['_toggleVoiceGroupVideo494','ngelx527ConfirmGroupRemoteTrack','Ngelx543GlobalPip','ngelx543DeleteCommunity']:
            self.assertEqual(source.count(name),result.count(name))
        self.assertIn("if(pending)throw StateError",result)
        self.assertIn("&&sameCall&&ngelx440CallJoinable(callData,DateTime.now())",result)

    def test_leave_waits_for_commit_but_keeps_offline_retry(self):
        source=Path('app/lib/build542_pending_leave.dart').read_text()
        result=transform(source,pending)
        self.assertEqual(result,transform(result,pending))
        self.assertLess(result.index('await prefs.setString(key'),result.index('await _ngelx542AttemptLeave(key,prefs).timeout'))
        self.assertIn("if(current==null||current['callRoomName']!=room",result)
        self.assertIn("FirebaseAuth.instance.currentUser?.uid!=uid",result)

    def test_shared_join_policy_keeps_ended_and_freshness_guards(self):
        source=Path('app/lib/build440_behavior.dart').read_text()
        result=transform(source,behavior)
        self.assertEqual(result,transform(result,behavior))
        for line in source.splitlines():
            self.assertIn(line,result)
        self.assertIn('participants is List&&participants.isEmpty',result)

if __name__=='__main__':unittest.main()
