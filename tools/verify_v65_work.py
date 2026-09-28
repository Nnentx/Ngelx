from pathlib import Path

root = Path(__file__).resolve().parents[1]
main = (root / "app/lib/main.dart").read_text(encoding="utf-8")
editor = (root / "app/lib/create_music_editor.dart").read_text(encoding="utf-8")
rules = (root / "firestore.rules").read_text(encoding="utf-8")

def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise SystemExit(f"V65 CHECK FAILED: {label}: missing {needle!r}")

def forbid(text: str, needle: str, label: str) -> None:
    if needle in text:
        raise SystemExit(f"V65 CHECK FAILED: {label}: forbidden {needle!r}")

pubspec = (root / "app/pubspec.yaml").read_text(encoding="utf-8")
if all(v not in pubspec for v in ("version: 1.0.65+284", "version: 1.0.66+285", "version: 1.0.67+286", "version: 1.0.68+287", "version: 1.0.69+288", "version: 1.0.70+289", "version: 1.0.71+290", "version: 1.0.72+291", "version: 1.0.73+292", "version: 1.0.74+293", "version: 1.0.75+294", "version: 1.0.76+295", "version: 1.0.77+296", "version: 1.0.78+297", "version: 1.0.79+298")):
    raise SystemExit("V65 CHECK FAILED: supported V65/V66 app version missing")

# New Create/editor surfaces are wired into the app.
require(main, "part 'create_music_editor.dart';", "editor part")
require(editor, "class NgelXMuzikSecPage", "music picker")
require(editor, "Müziklerde ara", "music search")
for tab in ["Senin için", "Popüler", "Kaydedilenler"]:
    require(editor, tab, f"music tab {tab}")
for license_guard in ["royaltyFree", "licensed", "licenseStatus", "permissioned", "public-domain"]:
    require(editor, license_guard, f"music license guard {license_guard}")
require(rules, "match /music_catalog/{trackId}", "music catalogue rules")
require(rules, "allow write: if false;", "catalogue client write protection")

# Create flow: media editing, text overlay, trim and licensed music metadata.
for needle, label in [
    ("String medyaYazisi='';", "media overlay state"),
    ("videoBaslangicMs=0,videoBitisMs=0", "video trim state"),
    ("Map<String,dynamic>? secilenMuzik", "selected music state"),
    ("Future<void> _videoDuzenle()", "video editor action"),
    ("Future<void> _medyaYazisiDuzenle()", "media text action"),
    ("Future<void> _muzikSec()", "music selection action"),
    ("'overlayText':medyaYazisi", "publish overlay"),
    ("'videoTrimStartMs':tur=='video'?videoBaslangicMs:0", "publish trim start"),
    ("'videoTrimEndMs':tur=='video'?videoBitisMs:0", "publish trim end"),
    ("'audioUrl':(yayinMuzik?['audioUrl']??'').toString()", "publish music url"),
    ("'musicLicense':(yayinMuzik?['licenseStatus']??'').toString()", "publish license metadata"),
]:
    require(main, needle, label)

require(editor, "class NgelXVideoDuzenlemePage", "video edit page")
require(editor, "RangeSlider(", "video trim UI")
require(editor, "Video üzerine yazı", "video overlay text UI")

# Feed must keep multi-photo and new media metadata.
require(main, "'mediaUrls':List<String>.from(veri['mediaUrls']??const[])", "multi-photo feed mapping")
require(main, "audioUrl:(item['audioUrl']??'').toString()", "video music feed mapping")
require(main, "trimStartMs:(item['videoTrimStartMs'] as num?)?.toInt()??0", "video trim feed mapping")
require(main, "widget.overlayText.trim().isNotEmpty", "video overlay render")
require(main, "musicTitle", "music title render")

# Regression: angry/laugh reactions must not light the heart control.
require(main, "final benimTepkim=aktifUid==null?'':(tepkiler[aktifUid]??'').toString();", "comment reaction identity")
require(main, "final kalpSecili=benimTepkim=='❤️';", "heart-only selected state")
forbid(main, "final secili=aktifUid!=null&&tepkiler.containsKey(aktifUid);", "old comment reaction heart bug")

# Premium must be visible next to profile names without replacing verified state.
require(main, "Text('PREMIUM'", "premium profile badge")
require(main, "workspace_premium_rounded", "premium badge icon")
require(main, "veri['premiumActive'] == true ||", "premium compatibility")

# Low-level upload protocol errors must not be shown directly in story/create UI.
require(main, "String ngelxMedyaHataMetni(Object e)", "friendly media error mapper")
require(main, "Hikâye yüklenemedi: '+ngelxMedyaHataMetni(e)", "story friendly error")
forbid(main, "Hikâye yüklenemedi: '+e.toString()", "raw story exception")

print("V65 consolidated WORK regression checks passed.")
