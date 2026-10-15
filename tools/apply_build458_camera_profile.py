#!/usr/bin/env python3
"""Build458: bounded camera initialization and owner coverless layout.

Apply *after* the Build457 source transforms. No server changes, no record
migration, and no changes to saved cover/avatar URLs.
"""
from pathlib import Path

LIVE = Path("app/lib/live_broadcast_studio.dart")
MAIN = Path("app/lib/main.dart")

def once(s, old, new, label):
    n = s.count(old)
    if n != 1:
        raise ValueError(f"Build458 {label}: expected exactly 1 anchor, found {n}")
    return s.replace(old, new, 1)

def camera_patch(s):
    if "// Build458 bounded camera preview initialization" in s:
        return s
    s=once(s,"  Uint8List? kameraGecisKaresi;",
           "  Uint8List? kameraGecisKaresi;\n  // Build458 bounded camera preview initialization.\n  bool _onizlemeIslemde = false;",
           "camera guard")
    s=once(s,"  Future<void> _onizlemeyiBaslat() async {\n    if (!kamera || baglaniyor) return;",
           """  Future<CameraController> _onizlemeAygitiAc(CameraDescription acilacak) async {
    // Some Android cameras fail to initialize at 720p/1080p but work at 540p.
    // Every attempted controller is disposed on failure; no perpetual spinner.
    Object? sonHata;
    for(final preset in <ResolutionPreset>[_onizlemeKalitesi, ResolutionPreset.medium]){
      CameraController? denenen;
      try{
        denenen=CameraController(acilacak,preset,enableAudio:false,
          imageFormatGroup:ImageFormatGroup.jpeg);
        await denenen.initialize().timeout(const Duration(seconds:8));
        return denenen;
      }catch(e){
        sonHata=e;
        if(denenen!=null){try{await denenen.dispose().timeout(const Duration(seconds:3));}catch(_){}}
      }
    }
    throw StateError('Kamera başlatılamadı ($sonHata). Yeniden dene veya kamera iznini kontrol et.');
  }

  Future<void> _onizlemeyiBaslat() async {
    if (!kamera || baglaniyor || _onizlemeIslemde) return;
    _onizlemeIslemde = true;""", "retry/camera guard")
    s=once(s,"final izin = await Permission.camera.request();",
           "final izin = await Permission.camera.request().timeout(const Duration(seconds:8));",
           "camera permission timeout")
    s=once(s,"kameralar = await availableCameras();",
           "kameralar = await availableCameras().timeout(const Duration(seconds:8));",
           "camera enumeration timeout")
    s=once(s,"      final yeni = CameraController(kameralar[secilen], _onizlemeKalitesi, enableAudio: false, imageFormatGroup: ImageFormatGroup.jpeg);\n      await yeni.initialize();",
           "      final yeni = await _onizlemeAygitiAc(kameralar[secilen]);",
           "camera fallback")
    s=once(s,"      if (!mounted) { await yeni.dispose(); return; }\n      onizleme = yeni;",
           "      if (!mounted || !kamera || baglaniyor) { await yeni.dispose(); return; }\n      onizleme = yeni;",
           "late completion state")
    s=once(s,"""        kameraHatasi = e.toString().replaceFirst('Exception: ', '');
      });
    }
  }

  Future<void> _kamerayiAcKapat""",
       """        kameraHatasi = e.toString().replaceFirst('Exception: ', '');
      });
    } finally {
      _onizlemeIslemde = false;
    }
  }

  Future<void> _kamerayiAcKapat""",
       "finalize camera retry guard")
    return s

def owner_profile_patch(s):
    if "// Build458 owner coverless rendering" in s:
        return s
    start=s.index("class _ProfilPageState extends State<ProfilPage>")
    end=s.index("\nclass _ProfilEtkilesimRozeti", start)
    frag=s[start:end]
    old="if(profilGorunumu=='coverless'||kapakUrl.isEmpty)"
    if frag.count(old)!=1:
        raise ValueError("Build458: owner coverless condition unavailable")
    # Display-only fix: keep existing coverPhotoUrl in Firestore for the user;
    # no media migration, no cover upload, no accidental data deletion.
    frag=frag.replace(old,"if(true) // Build458 owner coverless rendering",1)
    return s[:start]+frag+s[end:]

def main():
    original_live=LIVE.read_text(encoding="utf-8")
    original_main=MAIN.read_text(encoding="utf-8")
    new_live=camera_patch(original_live)
    new_main=owner_profile_patch(original_main)
    # Only write after all anchors have been verified.
    LIVE.write_text(new_live,encoding="utf-8")
    MAIN.write_text(new_main,encoding="utf-8")
    print("Build458 bounded camera preview + owner coverless UI applied; media/user data untouched.")

if __name__=="__main__":
    main()
