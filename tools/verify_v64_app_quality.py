from pathlib import Path

root = Path(__file__).resolve().parents[1]
main = (root / "app/lib/main.dart").read_text(encoding="utf-8")
settings = (root / "app/lib/build258_settings.dart").read_text(encoding="utf-8")
pubspec = (root / "app/pubspec.yaml").read_text(encoding="utf-8")

def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise SystemExit(f"V64 CHECK FAILED: {label}: missing {needle!r}")

def forbid(text: str, needle: str, label: str) -> None:
    if needle in text:
        raise SystemExit(f"V64 CHECK FAILED: {label}: forbidden {needle!r}")

if all(v not in pubspec for v in ("version: 1.0.64+283", "version: 1.0.65+284", "version: 1.0.66+285", "version: 1.0.67+286", "version: 1.0.68+287", "version: 1.0.69+288", "version: 1.0.70+289", "version: 1.0.71+290", "version: 1.0.72+291", "version: 1.0.73+292", "version: 1.0.74+293", "version: 1.0.75+294", "version: 1.0.76+295", "version: 1.0.77+296", "version: 1.0.78+297", "version: 1.0.79+298", "version: 1.0.80+299", "version: 1.0.81+300")):
    raise SystemExit("V64 CHECK FAILED: supported V64/V65/V66 app version missing")

# Main navigation / requested surfaces must remain wired.
for needle, label in [
    ("case 0: return const VideoAkisi(gorunur: true);", "Akis"),
    ("case 1: return const KesfetPage(gorunur: true);", "Kesfet"),
    ("case 2: return const YuklePage();", "Uret"),
    ("case 3: return const MesajPage();", "Sohbet"),
    ("case 4: return const ProfilPage();", "Ben"),
]:
    require(main, needle, label)

require(settings, "class AyarlarV258Page", "Ayarlar")
require(main, "NavigationDestination(icon: const Icon(Icons.explore_outlined)", "bottom navigation")
if "NavigationDestination(icon: const Icon(Icons.add_box_outlined" not in main and "label:t('create')" not in main:
    raise SystemExit("V64 CHECK FAILED: create navigation missing")

# Feed comments: bounded live window, O(n) reply lookup, no per-row like listener.
comments = main[main.index("class _YeniYorumlarState"):main.index("class KesfetPage")]
require(comments, "ref.limit(80).snapshots()", "comment live limit")
require(comments, "yanitHaritasi", "reply index")
require(comments, "keyboardDismissBehavior:ScrollViewKeyboardDismissBehavior.onDrag", "keyboard dismiss")
forbid(comments, "collection('likes').doc(aktifUid).snapshots()", "per-comment Firestore listener")
require(comments, "'reactions.$uid':'❤️'", "optimistic comment like snapshot")
require(main, "final oynuyordu=hazir&&kontrol.value.isPlaying;", "pause feed video under comments")
if main.count("isScrollControlled:true") < 2:
    raise SystemExit("V64 CHECK FAILED: comment sheets must be scroll controlled")

# Profile intro card must stay compact even for portrait videos.
intro = main[main.index("class ProfilTanitimVideoKarti"):main.index("class OrtakGruplarPage")]
require(intro, "height:150", "compact intro video")
require(intro, "width:double.infinity", "intro width")

# Social requests keep cached identity for quick labels, but correctness is
# verified from the server and pending-request reads are scoped to the pair.
social = main[main.index("Future<bool> sosyalIstekGonder"):main.index("Future<void> sosyalIstekIptalEt")]
require(social, "GetOptions(source:Source.cache)", "cached identity")
require(social, "GetOptions(source:Source.server)", "authoritative relationship check")
require(social, ".where('fromUid',isEqualTo:user.uid)", "pair request sender filter")
require(social, ".where('toUid',isEqualTo:hedefUid)", "pair request target filter")
require(social, ".limit(20)", "bounded pair request query")
require(social, "'clientCreatedAt':Timestamp.now()", "offline request timestamp")

# Remove obsolete placeholder / compatibility code from runtime.
for dead in [
    "class EskiYorumlar",
    "class VideoIlkKare",
    "class AyarlarPage extends StatelessWidget",
    "class ProfilBolumuPage",
    "class Istatistik extends StatelessWidget",
    "class BosEkran extends StatelessWidget",
]:
    forbid(main, dead, "dead runtime code")

# Explore should not restore the old Games category.
explore = main[main.index("class KesfetPage"):main.index("class CanliHazirlikPage")]
forbid(explore, "Oyunlar", "Explore games removal")

# Core real-data paths still exist; no demo/mock feed payloads.
require(main, "FirebaseFirestore.instance.collection('videos')", "real feed data")
for token in ["mockVideos", "demoVideos", "fakeVideos"]:
    forbid(main, token, "fake feed data")

print("V64 app quality/performance regression checks passed.")
