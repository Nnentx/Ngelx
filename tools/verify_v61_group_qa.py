#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
app = (ROOT / "app/lib/main.dart").read_text(encoding="utf-8")
quality = (ROOT / "app/lib/group_quality.dart").read_text(encoding="utf-8")
rules = (ROOT / "firestore.rules").read_text(encoding="utf-8")

checks = [
    ("Çıkış/çıkarılma arşivi", "ngelxRecordGroupArchive(" in app and "group_archives" in quality and "match /group_archives/{uid}/items/{chatId}" in rules),
    ("Çıkış sistem mesajı", "gruptan ayrıldı." in app and "member_left" in app),
    ("Çıkarma sistem mesajı", "adlı üyeyi gruptan çıkardı." in app and "member_removed" in app),
    ("Üye ekleme/onay isteği", "'Ekle',uyeler.length>=60?null:()=>uyeEkle" in app and "member_add" in app and "GrupKatilmaIstekleriPage" in app),
    ("Arama performans sınırı", "VideoParametersPresets.h360_169" in app and "maxFrameRate:20.0" in app and "_sonOdaCizimi" in app),
    ("Medya tepki konumu", "sadeMedya?-8:-3" in app),
    ("Mesaj teslim/görüldü", "ngelxMarkGroupMessagesSeen" in app and "deliveredTo" in quality and "seenBy" in quality and "onlyChanges(['deliveredTo', 'seenBy'])" in rules),
    ("Takma ad sistem mesajı", "nickname_changed" in app and "'newNickname':sonuc" in app),
    ("Foto/video yanıt önizleme", "replyToMediaUrl" in app and "NgelXReplyMediaPreview" in app and "replyToType" in app),
    ("Video oynatıcı kontrolleri", "Icons.replay_10_rounded" in app and "Icons.forward_10_rounded" in app and "VideoProgressIndicator" in app and "ignoring:oynuyor" in app),
    ("İlet ekranında adlar", "İletilebilecek başka sohbet yok." in quality and "p['displayName']" in quality and "p['photoUrl']" in quality),
    ("Mesaj sabitleme", "Mesajı sabitle" in app and "grupData['createdBy']" in app and "onlyChanges(['pinned', 'pinnedAt', 'pinnedBy'])" in rules),
    ("Grup arka planı ortak senkron", "backgroundVersion" in app and "tv['backgroundUrl']??''" in app and "backgroundChangedAt" in app),
]

failed = []
for name, ok in checks:
    print(("PASS" if ok else "FAIL") + " | " + name)
    if not ok:
        failed.append(name)

if failed:
    print("\nV61 grup QA doğrulaması BAŞARISIZ: " + ", ".join(failed))
    sys.exit(1)

print("\nV61 grup QA doğrulaması başarılı: %d/%d" % (len(checks), len(checks)))
