from pathlib import Path

root = Path(__file__).resolve().parents[1]
main = (root / "app/lib/main.dart").read_text(encoding="utf-8")
editor = (root / "app/lib/create_music_editor.dart").read_text(encoding="utf-8")
story = (root / "app/lib/story_v66.dart").read_text(encoding="utf-8")
pubspec = (root / "app/pubspec.yaml").read_text(encoding="utf-8")

def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise SystemExit(f"V66 CHECK FAILED: {label}: missing {needle!r}")

def forbid(text: str, needle: str, label: str) -> None:
    if needle in text:
        raise SystemExit(f"V66 CHECK FAILED: {label}: forbidden {needle!r}")

if all(v not in pubspec for v in ("version: 1.0.66+285", "version: 1.0.67+286", "version: 1.0.68+287", "version: 1.0.69+288", "version: 1.0.70+289", "version: 1.0.71+290", "version: 1.0.72+291")):
    raise SystemExit("V66 CHECK FAILED: supported V66/V67 app version missing")

# Story: one ring per owner, multiple active stories in series, segmented progress,
# tap/hold navigation, exact timing and profile avatar entry.
for needle, label in [
    ("part 'story_v66.dart';", "story part"),
    ("NgelXHikayeSeriPage", "series viewer integration"),
    ("NgelXHikayeliAvatar", "profile story ring integration"),
    ("gruplar=<String,List<Map<String,dynamic>>>{}", "group stories by owner"),
]:
    require(main, needle, label)
for needle, label in [
    ("class NgelXHikayeSeriPage", "story series page"),
    ("LinearProgressIndicator", "segmented story progress"),
    ("onTapUp:", "tap next/previous"),
    ("onLongPressStart:", "hold pause"),
    ("onVerticalDragEnd:", "swipe dismiss"),
    ("Başladı:", "story start time"),
    ("Biter:", "story expiry time"),
    ("replyCount", "story replies"),
    ("reactionCount", "story reactions"),
]:
    require(story, needle, label)

# Profile: follow request changes immediately and can be cancelled; existing
# friendship is actionable and asks before removal.
for needle, label in [
    ("_yerelTakipIstekleri", "optimistic follow request state"),
    ("gidenSosyalIstekBelgesi", "pending social request lookup"),
    ("Takip isteği geri çekildi.", "follow request cancel"),
    ("_arkadasliktanCikar", "friend removal action"),
    ("Arkadaşlıktan çıkarılsın mı?", "friend removal confirmation"),
    ("Arkadaşlık kaldırıldı.", "friend removal completion"),
]:
    require(main, needle, label)

# Group member overflow menu must support live role changes and protect founder.
for needle, label in [
    ("Yöneticilikten çıkar", "demote admin"),
    ("Yönetici yap", "promote member"),
    ("Kurucu gruptan çıkarılamaz", "founder protection"),
]:
    require(main, needle, label)

# Create: crash-safe text editor, colors and transforms, larger photo canvas,
# real-time filters and trim seek.
for needle, label in [
    ("class NgelXMedyaYaziAyariSheet", "self-owned text editor controller"),
    ("Yazı rengi", "text colors"),
    ("class NgelXSuruklenebilirYaziKatmani", "draggable text layer"),
    ("onScaleUpdate:", "text drag/scale/rotate"),
    ("RangeSlider(", "video trim slider"),
    ("_trimSeek(", "trim live seek"),
]:
    require(editor, needle, label)
for needle, label in [
    ("height:390", "larger photo edit canvas"),
    ("_fotoOnizlemeFiltresi", "live photo filters"),
    ("overlayColor", "overlay color metadata"),
    ("overlayX", "overlay position metadata"),
    ("overlayRotation", "overlay rotation metadata"),
    ("NgelXMedyaYaziAyariSheet(", "crash-safe text editor wiring"),
]:
    require(main, needle, label)
forbid(main, "final c=TextEditingController(text:medyaYazisi);", "old externally-disposed media text dialog")

# Music picker should not depend on an indexed active==true query; filtering is
# client-side and a retry path exists.
require(editor, ".collection('music_catalog')", "music catalogue")
forbid(editor, ".where('active', isEqualTo: true)", "indexed music query")
require(editor, "Tekrar dene", "music retry")

print("V66 tested WORK regression checks passed.")
