import unittest
from pathlib import Path
from apply_build546_live_guest import studio,main
class GuestContinuity(unittest.TestCase):
 def test_source_preserves_host_and_call_paths(self):
  old=Path('app/lib/live_broadcast_studio.dart').read_text();new=studio(old)
  self.assertEqual(studio(new),new)
  for name in ['_guestRail488','_hostGuestAction489','_guestControl453','_bitir','_heartbeatYaz','_guestAudioPolicySub489']:
   self.assertEqual(old.count(name),new.count(name),name)
  a=new.index('final reusable=');b=new.index('if(!reusable)',a);c=new.index('await widget.oda.disconnect()',b)
  self.assertLess(a,b);self.assertLess(b,c)
  self.assertIn('GetOptions(source:Source.server)',new)
  self.assertIn('await Future.wait([',new)
  self.assertIn('if(!current546()||!_guestWanted448)',new)
  self.assertIn('revision546!=_guestRevision546',new)
  self.assertIn('if(changed&&muted)_guestMicWanted546=false;',new)
  self.assertIn('microphone:_guestMicWanted546&&!state.muted',new)
  self.assertIn('await _guestSync448(accepted)',new)
  self.assertIn('_guestRetry546?.cancel();\n    _guestSub448?.cancel();',new)
 def test_main_change_is_import_only(self):
  old=Path('app/lib/main.dart').read_text();new=main(old)
  self.assertEqual(main(new),new)
  self.assertIn('await ngelxArkaPlanAramayiTemizle(entry.key)',new)
  self.assertEqual(old.count('Ngelx543GlobalPip'),new.count('Ngelx543GlobalPip'))
if __name__=='__main__':unittest.main()
