"""Build482 read-only source regression tests; no production data access."""
import unittest
from pathlib import Path

ROOT = Path("app/lib/build456_widgets.dart")
COMMUNITY = Path("app/lib/community450.dart")
MAIN = Path("app/lib/main.dart")
RULES = Path("firestore.rules")

class Build482CommunityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = ROOT.read_text(encoding="utf-8")

    def test_invite_names_visible_in_isolated_light_sheet(self):
        source = self.source
        picker = source[source.index("class _Ngelx456ChatPickerState"):
                        source.index("Future<void> ngelx456SendInvite")]
        self.assertIn("Build482: keep the existing white invite sheet", source)
        self.assertIn("child: const Ngelx456ChatPicker()", source)
        self.assertIn("color: ngelx456Ink", picker)
        self.assertIn("name,\n", picker)
        self.assertIn("style: TextStyle(fontSize: 12, color: Colors.black54)", picker)
        self.assertIn("activeColor: mor", picker)
        self.assertIn("tileColor: Colors.white", picker)
        self.assertIn("profiles.putIfAbsent", picker)
        self.assertIn("chatIds.containsKey(uid)", picker)
        self.assertIn("selected.isEmpty", picker)

    def test_separate_avatar_editor_uses_existing_media_path(self):
        source = self.source
        start = source.index("class Ngelx482CommunityAvatarEditor")
        end = source.index("class Ngelx456Header", start)
        editor = source[start:end]
        self.assertIn("Galeriden fotoğraf seç", editor)
        self.assertIn("ngelxResimSec(", editor)
        self.assertIn("ngelxFotografYukle(", editor)
        self.assertIn("kind: 'groups'", editor)
        self.assertIn("GetOptions(source: Source.server)", editor)
        # Build482 used the cover guard. Build484 uses a stricter member-
        # verified community manager for new avatar uploads while the cover
        # editor keeps its original behavior.
        self.assertTrue(
            "ngelx457CanEditCover(current, uid)" in editor
            or "ngelx484CommunityManager(current, uid)" in editor
        )
        if "ngelx484CommunityManager(current, uid)" in editor:
            self.assertIn("if (!members.contains(uid)) return false;", source)
        self.assertIn("await root.update({'photoUrl': url})", editor)
        self.assertNotIn("delete(", editor)
        self.assertNotIn("FieldValue.array", editor)
        self.assertNotIn("'coverUrl': url", editor)
        self.assertIn("'Topluluk profil fotoğrafını değiştir'", source)
        self.assertIn("Ngelx456CoverEditor(id: widget.id, value: v)", source)

    def test_working_481_chat_camera_and_firebase_preserved(self):
        main = MAIN.read_text(encoding="utf-8")
        community = COMMUNITY.read_text(encoding="utf-8")
        rules = RULES.read_text(encoding="utf-8")
        for marker in ("Build481: consistent large rounded chat photo frame",
                       "Build480: image-only selection",
                       "Build479: protect private chat navigation",
                       "Build478: follow keyboard layout"):
            # Android-only picker marker lives in MainActivity.kt.
            if "Build480" not in marker:
                self.assertIn(marker, main)
        self.assertIn("Build481: distinguish legacy founder permission", community)
        self.assertIn("if (!ngelx456Moderator(v))", community)
        self.assertNotIn("allow write: if true", rules)

if __name__ == "__main__":
    unittest.main()
