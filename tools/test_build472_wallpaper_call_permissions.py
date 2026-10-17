"""Build472: caller ownership, wallpaper stability, native CTA offset,
and genuine community auth denial are regression-checked.
"""
import unittest
from pathlib import Path
from apply_build472_wallpaper_callclose import transform as chat_fix
from apply_build472_call_buttons_community import patch_activity,patch_community
MAIN=Path('app/lib/main.dart')
COMMUNITY=Path('app/lib/community450.dart')
ACTIVITY=Path('app/android/app/src/main/kotlin/com/nnentx/ngelx_app/IncomingCallActivity470.kt')
class Build472Tests(unittest.TestCase):
 def test_selected_photo_cached_but_retained(self):
  s=MAIN.read_text(encoding='utf-8')
  self.assertEqual(chat_fix(s),s)
  start=s.index('class _SohbetPageState');end=s.index('class NgelXSesliMesaj',start)
  part=s[start:end]
  for term in ('// Build472: memoize the private wallpaper decoration',
    '_wallpaperDecoration472', '_wallpaperKey472', 
    'image:ResizeImage(NgelXAgImageProvider(url),width:720)',
    'return Container(decoration:_ngelx472Wallpaper(arkaPlan,arkaPlanUrl,arkaPlanOpaklik)',
    "veri['backgroundUrl']", 'onChanged:mesajDegisti',
    '_ngelx470ComposerTick','_ngelx465StopOpeningBottom()',
    'bottomNavigationBar:ColoredBox('):
    self.assertIn(term,part)
  self.assertNotIn('width:900),fit:BoxFit.cover,opacity:arkaPlanOpaklik',part)
 def test_call_close_changes_owned_history_only(self):
  s=MAIN.read_text(encoding='utf-8')
  self.assertIn("if(mesajId.isNotEmpty && data['callStartedBy']==me){",s)
  self.assertEqual(s.count("Arama kapandı. Sunucu kaydı güncellenemedi; yeniden dene."),2) # source + translations
  self.assertIn("'callStatus':finalDurum",s)
  self.assertIn("await widget.aramaRef.set({",s)
  self.assertIn("call_end_",s)
 def test_two_visuals_and_voice_controls_retained(self):
  s=ACTIVITY.read_text(encoding='utf-8')
  self.assertEqual(patch_activity(s),s)
  for t in ('Build472: move call actions safely above',
    'LinearLayout.LayoutParams(1, dp(42))',
    'val group = intent.getBooleanExtra("callGroup471", false)',
    'actionButton("Reddet", true) { respond("reject") }',
    'actionButton("Cevapla", false) { respond("answer") }',
    'IncomingCallService.cancel(this, room)'):
   self.assertIn(t,s)
 def test_founder_denial_is_not_hidden(self):
  s=COMMUNITY.read_text(encoding='utf-8')
  self.assertEqual(patch_community(s),s)
  for t in ('// Build472: show a permission-denied backend response truthfully',
    "e.code=='permission-denied'", 'Firestore','kurucu','Firebase kuralları'):
    self.assertIn(t,s)
if __name__=='__main__':unittest.main()
