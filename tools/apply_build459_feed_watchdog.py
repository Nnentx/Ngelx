#!/usr/bin/env python3
"""Build459: bounded playback first-frame stall with retry; keep Build458 player.

No URL logging, content mutation, backend deployment, user record or R2 changes.
Run AFTER tools/apply_build458_feed_recovery.py.
"""
from pathlib import Path
MAIN=Path("app/lib/main.dart")

def one(s,old,new,label):
    count=s.count(old)
    if count!=1:
        raise ValueError(f"Build459 {label}: expected 1 anchor, found {count}")
    return s.replace(old,new,1)

def patch(s):
    if "// Build459 feed watchdog" in s:
        return s
    a=s.index("class _VideoKartiState extends State<VideoKarti>")
    b=s.index("\nclass ",a+len("class _VideoKartiState"))
    frag=s[a:b]

    frag=one(frag,"  String? medyaHatasi;",
        "  String? medyaHatasi;\n  // Build459 feed watchdog; catches a playable URL that never paints frames.\n  Timer? _ngelx459FirstFrameTimer;",
        "first frame timer")

    marker="  Future<void> _videoyuTekrarDene() async {"
    helper="""  void _ngelx459IzlemeBaslat() {
    _ngelx459FirstFrameTimer?.cancel();
    if(!mounted||!widget.aktif||!_rotaGorunur||duraklatildi||!hazir)return;
    final player=kontrol;
    final ilkKonum=player.value.position;
    _ngelx459FirstFrameTimer=Timer(const Duration(seconds:12),(){
      if(!mounted||!widget.aktif||!_rotaGorunur||duraklatildi||
          !hazir||!identical(kontrol,player))return;
      final durum=player.value;
      final ilerledi=durum.position>ilkKonum+const Duration(milliseconds:300);
      if(!ilerledi && (durum.isBuffering||!durum.isPlaying||durum.hasError)){
        setState(()=>medyaHatasi='Video görüntüsü yüklenemedi.');
        unawaited(player.pause());
      }
    });
  }

"""
    frag=one(frag,marker,helper+marker,"watchdog placement")

    frag=one(frag,marker+"\n    if(hazirlaniyor || !mounted)return;",
             marker+"\n    if(hazirlaniyor || !mounted)return;\n    _ngelx459FirstFrameTimer?.cancel();",
             "retry cancels watchdog")

    frag=one(frag,"        _otomatikKaydirmaZamanla();\n      }\n    }catch(e){",
             "        _otomatikKaydirmaZamanla();\n        _ngelx459IzlemeBaslat();\n      }\n    }catch(e){",
             "start watchdog after video initialized")

    frag=one(frag,"  void _oynatmalariDuraklat(){\n    _otomatikKaydirmaIptal();",
             "  void _oynatmalariDuraklat(){\n    _ngelx459FirstFrameTimer?.cancel();\n    _otomatikKaydirmaIptal();",
             "pause cleanup")

    frag=one(frag,"  void dispose() {\n    _otomatikKaydirmaIptal();",
             "  void dispose() {\n    _ngelx459FirstFrameTimer?.cancel();\n    _otomatikKaydirmaIptal();",
             "dispose cleanup")

    # When a post returns into view, re-arm only if still at the beginning.
    frag=one(frag,"  void _oynatmalariBaslat(){\n    if(!hazir||!widget.aktif||!_rotaGorunur||duraklatildi)return;",
             "  void _oynatmalariBaslat(){\n    if(!hazir||!widget.aktif||!_rotaGorunur||duraklatildi)return;\n    if(kontrol.value.position<const Duration(milliseconds:300))_ngelx459IzlemeBaslat();",
             "resume first-frame watchdog")

    return s[:a]+frag+s[b:]

def main():
    before=MAIN.read_text(encoding="utf-8")
    after=patch(before)
    if after!=before:MAIN.write_text(after,encoding="utf-8")
    print("Build459: playback stall detection after 12 seconds; safe retry retained.")

if __name__=="__main__":
    main()
