"""Build481 generated-source regressions; never touches production Firebase."""
import unittest
from pathlib import Path
from apply_build481_chat_community import (
    photo, community, PHOTO_MARK, COMMUNITY_MARK
)

class Build481Tests(unittest.TestCase):
    def test_generated_photo_and_reaction_are_stable(self):
        original=Path("app/lib/main.dart").read_text(encoding="utf-8")
        self.assertIn(PHOTO_MARK,original)
        self.assertEqual(photo(original),original)
        self.assertIn("maxWidth:frameWidth",original)
        self.assertIn("BorderRadius.circular(22)",original)
        self.assertIn("Ngelx453Photo(url:url)",original)
        self.assertIn("BoxFit.contain",Path("app/lib/build453_widgets.dart").read_text(encoding="utf-8"))
        self.assertIn("Positioned(right:5,bottom:0,",original)
        self.assertIn("// Build480",Path("app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt").read_text(encoding="utf-8"))

    def test_community_role_warnings_are_read_only(self):
        src=Path("app/lib/community450.dart").read_text(encoding="utf-8")
        self.assertIn(COMMUNITY_MARK,src)
        self.assertEqual(community(src),src)
        self.assertIn("legacyFounder481",src)
        self.assertIn("Üye veya yönetici yetkilerini otomatik değiştirmiyoruz",src)
        self.assertNotIn("FieldValue.arrayUnion([_communityUid450])",src[src.index(COMMUNITY_MARK):src.index("return ListView(",src.index(COMMUNITY_MARK))])
        self.assertIn("if (!_communityAdmin450(v))",src)
        self.assertIn("permission-denied",src)

    def test_existing_guardrails_unchanged(self):
        main=Path("app/lib/main.dart").read_text(encoding="utf-8")
        for marker in ("Build479: protect private chat navigation during gallery return",
                       "Build478: follow keyboard layout only when the user is at chat bottom",
                       "Build476: plain text timestamps belong below",
                       "Build465: one-tap camera and gallery"):
            self.assertIn(marker,main)
        rules=Path("firestore.rules").read_text(encoding="utf-8")
        self.assertIn("Build469: legacy verified founder limited-settings compatibility",rules)
        self.assertNotIn("allow write: if true",rules)

if __name__=="__main__":
    unittest.main()
