#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN_PATH=ROOT/"app/lib/main.dart"
PUB_PATH=ROOT/"app/pubspec.yaml"

def one(text,old,new,label):
    n=text.count(old)
    if n!=1:
        raise SystemExit(f"Build 298 patch failed: {label}: expected 1 match, got {n}")
    return text.replace(old,new,1)

main=MAIN_PATH.read_text(encoding="utf-8")
pub=PUB_PATH.read_text(encoding="utf-8")
if "version: 1.0.79+298" in pub:
    raise SystemExit("Build 298 already applied.")

# Grup fotoğrafını bytes yerine video ile aynı güvenilir XFile/stream yolundan yükle.
old_group="""      final bytes=await x.readAsBytes();
      final uzanti=x.name.contains('.')?x.name.split('.').last.toLowerCase():'jpg';
      final yol='groups/${widget.chatId}/${DateTime.now().millisecondsSinceEpoch}.$uzanti';
      final url=await ngelxMedyaYukleBytes(
        bytes:bytes,kind:'groups',ext:uzanti,legacyPath:yol,
        onProgress:(sent,total)=>_medyaIlerlemeGuncelle('Fotoğraf yükleniyor',sent,total),
      ).timeout(const Duration(seconds:60));"""
new_group="""      final uzanti=x.name.contains('.')?x.name.split('.').last.toLowerCase():'jpg';
      final yol='groups/${widget.chatId}/${DateTime.now().millisecondsSinceEpoch}.$uzanti';
      final url=await ngelxMedyaYukleDosya(
        dosya:x,kind:'groups',ext:uzanti,legacyPath:yol,
        onProgress:(sent,total)=>_medyaIlerlemeGuncelle('Fotoğraf yükleniyor',sent,total),
      ).timeout(const Duration(seconds:75));"""
main=one(main,old_group,new_group,"group photo file upload")

# Özel sohbet fotoğrafını da bytes yerine XFile/stream yolundan yükle.
old_private="""      final yol='chats/${widget.chatId}/${DateTime.now().millisecondsSinceEpoch}.jpg';
      final url=await ngelxMedyaYukleBytes(
        bytes: await x.readAsBytes(),
        kind: 'chats',
        ext: 'jpg',
        legacyPath: yol,
      ).timeout(const Duration(seconds:60));"""
new_private="""      final uzanti=x.name.contains('.')?x.name.split('.').last.toLowerCase():'jpg';
      final yol='chats/${widget.chatId}/${DateTime.now().millisecondsSinceEpoch}.$uzanti';
      final url=await ngelxMedyaYukleDosya(
        dosya:x,
        kind:'chats',
        ext:uzanti,
        legacyPath:yol,
      ).timeout(const Duration(seconds:75));"""
main=one(main,old_private,new_private,"private photo file upload")

# Sürüm.
main=one(main,"defaultValue: '1.0.78'","defaultValue: '1.0.79'","runtime version")
main=one(main,"defaultValue: '297'","defaultValue: '298'","runtime build")
MAIN_PATH.write_text(main,encoding="utf-8")

pub=one(pub,"version: 1.0.78+297","version: 1.0.79+298","pubspec version")
PUB_PATH.write_text(pub,encoding="utf-8")

# Birikimli doğrulama zinciri.
for path in [
    ROOT/"tools/verify_v64_app_quality.py",
    ROOT/"tools/verify_v65_media_traffic.py",
    ROOT/"tools/verify_v65_work.py",
    ROOT/"tools/verify_v66_work.py",
    ROOT/"tools/verify_v67_work.py",
    ROOT/"tools/verify_v68_work.py",
]:
    t=path.read_text(encoding="utf-8")
    if '"version: 1.0.79+298"' not in t:
        t=t.replace('"version: 1.0.78+297"))','"version: 1.0.78+297", "version: 1.0.79+298"))')
    path.write_text(t,encoding="utf-8")

for name in ["verify_v72_device_fixes.py","verify_v76_chat_media.py","verify_v77_social_relations.py","verify_v78_media_dialog.py"]:
    path=ROOT/"tools"/name
    t=path.read_text(encoding="utf-8")
    t=t.replace("version: 1.0.78+297","version: 1.0.79+298")
    t=t.replace("defaultValue: '1.0.78'","defaultValue: '1.0.79'")
    t=t.replace("defaultValue: '297'","defaultValue: '298'")
    t=t.replace("Build 297","Build 298")
    path.write_text(t,encoding="utf-8")

print("Build 298 photo upload patch prepared.")
