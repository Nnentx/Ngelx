import unittest
from pathlib import Path
from apply_build545_account_handoff import transform

class AccountHandoff(unittest.TestCase):
    def test_handoff_releases_media_without_ending_private_or_group_call(self):
        source = Path('app/lib/main.dart').read_text()
        fixed = transform(source)
        self.assertEqual(transform(fixed), fixed)
        body = fixed.split('Future<void> ngelx544BeforeAccountChange()async{', 1)[1].split('\n}', 1)[0]
        self.assertIn('await ngelxArkaPlanAramayiTemizle(entry.key)', body)
        self.assertNotIn('ngelx445EndBackground', body)
        self.assertIn('await ngelx542RetryPendingLeaves()', body)
        self.assertIn('if(pending)throw StateError', body)
        # Explicit sign-out remains an intentional leave, unlike account handoff.
        self.assertIn('await ngelx445EndBackground(name)', fixed)
        for part in ['Ngelx543GlobalPip', '_toggleVoiceGroupVideo494', 'ngelx527ConfirmGroupRemoteTrack']:
            self.assertEqual(source.count(part), fixed.count(part))

if __name__ == '__main__': unittest.main()
