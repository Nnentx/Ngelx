"""Build469 protection tests for generated chat and Android call fixes."""
import unittest
from pathlib import Path
from apply_build469_group_call_grid import transform as call_fix
from apply_build469_keyboard_inbox import transform as typing_fix
from apply_build469_ring_diagnostics import transform as ring_fix
from apply_build469_founder_rules_qa import transform as founder_fix
from apply_build469_foreground_ring import transform as incoming_fix
from apply_build469_live_mini_call import transform as mini_fix

MAIN=Path('app/lib/main.dart')
KOTLIN=Path('app/android/app/src/main/kotlin/com/nnentx/ngelx_app/IncomingCallService.kt')
RULES=Path('firestore.rules')
class Build469Tests(unittest.TestCase):
    def test_voice_and_video_call_grids(self):
        s=MAIN.read_text(encoding='utf-8')
        self.assertEqual(call_fix(s),s)
        self.assertIn('// Build469: every participant has one scoped actions menu',s)
        self.assertEqual(s.count('child:_ngelx469ParticipantMenu(p,yerel:yerel)'),2)  # video and voice tiles
        self.assertIn('Positioned(right:-10,top:-14,child:_ngelx469ParticipantMenu(p,yerel:yerel))',s)
        self.assertIn('p.isSpeaking&&mic446',s)
        self.assertIn("p.isSpeaking&&(yerel?mikrofon",s)
        self.assertIn('const Color(0xFF23DC7A)',s)
        self.assertIn("Text('Sesten at'",s)
        self.assertIn("enabled:canModerate",s)
        self.assertIn('ngelx446MuteMenu(context,widget.aramaRef,widget.roomName',s)
        self.assertIn('_ngelx465SetRemoteAudio(remote,locallyMuted)',s)
        self.assertIn('Ngelx446SpeakingRing(participant:p',s)
    def test_typing_is_local_and_cached_ids_preserved(self):
        s=MAIN.read_text(encoding='utf-8')
        self.assertEqual(typing_fix(s),s)
        for term in ["// Build469: do not split the entire draft on every keypress",
                     "deger.lastIndexOf(_wordBreak469)",
                     "_typingRef469",
                     "PrivateDraftStore.schedule(widget.chatId,deger)",
                     "onChanged:mesajDegisti",
                     "ngelx455ProfileName(p, fallback:'Kullanıcı')",
                     "title:Text('Kişi bilgisi yükleniyor…')",
                     "_ngelx465ProfileRetryTimers",
                     "_profiles453.putIfAbsent"]:
            self.assertIn(term,s)
    def test_native_ring_security_checks_are_unchanged(self):
        s=KOTLIN.read_text(encoding='utf-8')
        self.assertEqual(ring_fix(s),s)
        for t in ["push_ignored_auth_not_ready","incoming_call_delivered",
                  "ring_blocked settings","ringer_started","ringing.remove(room)",
                  "manager.notify(room.hashCode(), notification)",
                  "AudioManager.RINGER_MODE_NORMAL","currentInterruptionFilter"]:
            self.assertIn(t,s)
        self.assertNotIn('recipientUid=',s)
    def test_foreground_incoming_group_call_safe_cache(self):
        s=Path('app/lib/build448_incoming_calls.dart').read_text(encoding='utf-8')
        self.assertEqual(incoming_fix(s),s)
        for term in ('// Build469: verify empty snapshots before stopping a ringing call',
                     '_ringingChat469','Source.server','_verifyingMissing469',
                     "v['isGroup']==true&&v['callStatus']=='active'",
                     "if(_ringing==room)return",'ngelxCallSession444.busy'):
            self.assertIn(term,s)

    def test_mini_video_overlay_stays_in_screen(self):
        s=Path('app/lib/build445_inbox_model.dart').read_text(encoding='utf-8')
        self.assertEqual(mini_fix(s),s)
        for term in ('// Build469: Messenger-style live thumbnail in the EXISTING mini call',
                     'lk.VideoTrackRenderer(remote,fit:lk.VideoViewFit.cover)',
                     'final maxX=math.max(8.0,screen.width-152.0)',
                     'return Positioned(left:x,top:y,width:144',
                     'onTap:()=>ngelx445ReturnCall(name)',
                     'onEnd:()=>ngelx445EndBackground(name)'):
            self.assertIn(term,s)

    def test_founder_emulator_rules_cannot_delete_or_grant_roles(self):
        s=RULES.read_text(encoding='utf-8')
        self.assertEqual(founder_fix(s),s)
        part=s.split('// Build469: legacy verified founder limited-settings compatibility')[1].split('allow delete: if false;',1)[0]
        for t in ("resource.data.get('founderId','') == request.auth.uid",
                  "request.auth.uid in resource.data.get('members',[])",
                  "affectedKeys().hasOnly([","'visibility','joinApproval','postApproval','paused'"):
            self.assertIn(t,part)
        changed_fields=part.split("affectedKeys().hasOnly([",1)[1].split("])",1)[0]
        self.assertNotIn("'admins'",changed_fields)
        self.assertNotIn("'members'",changed_fields)
        self.assertNotIn("'founderId'",changed_fields)
if __name__=='__main__': unittest.main()
