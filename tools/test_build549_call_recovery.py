import os,unittest
from pathlib import Path
from apply_build549_call_recovery import main_source,incoming_source,pending_source,overlay_source
BASE=Path(os.environ.get('BUILD549_BASELINE','app/lib'))
class Recovery549(unittest.TestCase):
 def test_admission_rechecks_server_and_never_ends_a_group_on_decline(self):
  s=incoming_source((BASE/'build448_incoming_calls.dart').read_text());s=s[s.index('  Future<void> _action('):]
  self.assertIn('Source.server',s)
  self.assertIn('!eligible(current)',s)
  self.assertIn('FirebaseAuth.instance.currentUser?.uid!=me',s)
  reject=s[s.index("if(action=='reject'&&v['isGroup']==true)"):s.index("if(action=='answer')")]
  self.assertNotIn('tx.update',reject);self.assertNotIn('ref.set',reject)
  self.assertIn('_dismissed549.add(room)',reject)
  self.assertIn('ngelx542PrepareManualJoin(room,me)',s)
  self.assertIn('ngelx549CallNotice(error)',s)
 def test_pending_leave_is_retained_and_replay_stops_on_quota(self):
  s=pending_source((BASE/'build542_pending_leave.dart').read_text())
  self.assertIn('if(ngelx549Quota(error))break',s)
  self.assertIn('DateTime.now().isBefore(retryAfter)',s)
  self.assertIn("current['callRoomName']!=room",s)
  self.assertIn('ngelx517LeaveGroupCall',s)
  self.assertIn('ngelx549LastLeaveError=error;return false',s)
 def test_heartbeat_never_changes_status_or_participants(self):
  s=Path('tools/build549_call_recovery.dart').read_text()
  heartbeat=s[s.index('Future<void> ngelx549Heartbeat'):s.index('final Map<String,DateTime>')]
  self.assertEqual(heartbeat.count('tx.update'),1)
  self.assertIn("tx.update(ref,{'callHeartbeatAt':FieldValue.serverTimestamp()})",heartbeat)
  self.assertIn('FirebaseAuth.instance.currentUser?.uid!=uid',heartbeat)
  self.assertIn("v['callRoomName']!=name",heartbeat)
  self.assertIn("v['callParticipants']",heartbeat)
  self.assertIn('gate.enter(DateTime.now())',heartbeat)
  self.assertIn('gate.finish(DateTime.now(),quota:quota)',heartbeat)
 def test_both_surfaces_share_heartbeat_and_quota_does_not_auto_reconnect(self):
  s=main_source((BASE/'main.dart').read_text())
  self.assertIn('ngelx549Heartbeat(widget.aramaRef',s)
  self.assertIn('!ngelx549Quota(e)&&yenidenBaglanmaDenemesi<3',s)
  self.assertIn('if(!_callQuota549)TextButton(onPressed:openAppSettings',s)
  self.assertIn('ngelx549Heartbeat(detail.ref,name',overlay_source((BASE/'build445_inbox_model.dart').read_text()))
 def test_transform_idempotent(self):
  for file,fn in [('main.dart',main_source),('build448_incoming_calls.dart',incoming_source),('build542_pending_leave.dart',pending_source),('build445_inbox_model.dart',overlay_source)]:
   new=fn((BASE/file).read_text());self.assertEqual(fn(new),new)
if __name__=='__main__':unittest.main()
