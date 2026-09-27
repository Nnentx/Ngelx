from pathlib import Path

root = Path(__file__).resolve().parents[1]
editor = (root / "app/lib/create_music_editor.dart").read_text(encoding="utf-8")
rules = (root / "firestore.rules").read_text(encoding="utf-8")
deploy = (root / ".github/workflows/v67-firestore-rules-deploy.yml").read_text(encoding="utf-8")
pubspec = (root / "app/pubspec.yaml").read_text(encoding="utf-8")

def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise SystemExit(f"V67 CHECK FAILED: {label}: missing {needle!r}")

require(pubspec, "version: 1.0.67+286", "V67 app version")
require(editor, "SingleChildScrollView(", "keyboard-safe text editor scroll")
require(editor, "ScrollViewKeyboardDismissBehavior.onDrag", "keyboard dismiss behavior")
require(editor, "18+klavye", "keyboard inset padding")
require(editor, "backgroundColor: Colors.white", "white music picker")
require(editor, "_katalogHataMetni(snap.error)", "music catalogue error classification")
require(editor, "Müzik kataloğu sunucu izni bekliyor", "permission-denied message")
require(rules, "match /music_catalog/{trackId}", "music catalogue firestore rule")
require(rules, "allow read: if true;", "public licensed catalogue read")
require(rules, "allow write: if false;", "catalogue client write protection")
require(deploy, "firebase deploy --only firestore:rules", "production firestore rules deploy")
require(deploy, "ngelx-44eed", "firebase project")

print("V67 device-fix regression checks passed.")
