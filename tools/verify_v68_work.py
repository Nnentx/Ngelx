from pathlib import Path

root = Path(__file__).resolve().parents[1]
editor = (root / "app/lib/create_music_editor.dart").read_text(encoding="utf-8")
pubspec = (root / "app/pubspec.yaml").read_text(encoding="utf-8")

def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise SystemExit(f"V68 CHECK FAILED: {label}: missing {needle!r}")

if all(v not in pubspec for v in ("version: 1.0.68+287", "version: 1.0.69+288", "version: 1.0.70+289", "version: 1.0.71+290", "version: 1.0.72+291", "version: 1.0.73+292", "version: 1.0.74+293")):
    raise SystemExit("V68 CHECK FAILED: supported V68/V69 app version missing")

for needle, label in [
    ("final bool secili;", "selectable text layer"),
    ("final VoidCallback? onSelect,onEdit;", "text layer selection callbacks"),
    ("onDoubleTap:widget.onEdit", "double-tap edit"),
    ("basFocal=d.focalPoint", "stable gesture start point"),
    ("final fark=d.focalPoint-basFocal", "drag from gesture origin"),
    ("yaziSecili=false", "video text selection state"),
    ("_yaziKatmaniniDuzenle", "direct text edit action"),
    ("_yaziOrtala", "center text action"),
    ("_yaziSifirla", "reset text transform action"),
    ("_yaziSil", "delete text action"),
    ("_yaziOlcekle", "scale text controls"),
    ("_yaziDondur", "rotate text control"),
    ("secili:yaziSecili", "selection visual wiring"),
    ("Yazıya dokun: seç", "gesture guidance"),
]:
    require(editor, needle, label)

print("V68 video text-layer gesture regression checks passed.")
