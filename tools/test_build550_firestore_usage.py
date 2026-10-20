import os
import unittest
from pathlib import Path
from apply_build550_firestore_usage import live_source, pk_source

ROOT = Path(os.environ.get('BUILD550_BASELINE', 'app/lib'))


class Usage550(unittest.TestCase):
    def test_periodic_live_heartbeat_has_no_reads_and_backs_off_on_quota(self):
        s = live_source((ROOT / 'live_broadcast_studio.dart').read_text())
        heartbeat = s[s.index('  Future<void> _heartbeatYaz()'):s.index('  lk.VideoTrack? _goruntu()')]
        self.assertNotIn('.get(', heartbeat)
        self.assertNotIn('.count()', heartbeat)
        self.assertIn('if(_totalsReady550)', heartbeat)
        self.assertIn('_heartbeatBusy550', heartbeat)
        self.assertIn('finally{_heartbeatBusy550=false;}', heartbeat)
        self.assertIn('Duration(minutes:2)', heartbeat)
        self.assertIn('Duration(seconds:6)', s)
        # Final reconciliation still includes the whole history once on exit.
        end = s[s.index('  Future<void> _bitir('):]
        self.assertIn("collection('comments').get()", end)
        self.assertIn('await _totalsSub550?.cancel()', end)

    def test_reactions_share_subscription_and_handle_removed_documents(self):
        s = live_source((ROOT / 'live_broadcast_studio.dart').read_text())
        self.assertEqual(s.count("collection('reactions').snapshots()"), 1)
        self.assertIn('DocumentChangeType.removed', s)
        self.assertIn('_reactionCounts453.remove(d.doc.id)', s)
        self.assertIn('_reactionTotal550.dispose()', s)
        self.assertIn('_totalsSub550?.cancel()', s)
        self.assertIn('!snapshot.metadata.isFromCache', s)

    def test_pk_idle_ticks_no_longer_reread_room_or_invitation_history(self):
        s = pk_source((ROOT / 'build541_audio_pk.dart').read_text())
        sync = s[s.index('  Future<void> _sync()'):s.index('  Future<void> _respond(')]
        self.assertNotIn('_ref.get(', sync)
        self.assertNotIn("arrayContains:_sessionUid).get", sync)
        self.assertIn('_invites550.where', sync)
        self.assertIn('tx.get(_ref)', sync)  # Admission remains authoritative.
        self.assertIn('_cancelWatches550()', s[s.index('@override void dispose()'):])
        self.assertIn('if(widget.ended)return;', s)
        self.assertIn('if(widget.ended&&!oldWidget.ended)', s)

    def test_generation_is_idempotent(self):
        for name, fn in [('live_broadcast_studio.dart', live_source), ('build541_audio_pk.dart', pk_source)]:
            with self.subTest(name=name):
                result = fn((ROOT / name).read_text())
                self.assertEqual(fn(result), result)


if __name__ == '__main__':
    unittest.main()
