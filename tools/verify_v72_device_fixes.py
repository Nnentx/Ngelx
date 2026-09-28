#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = (ROOT / "app/lib/main.dart").read_text(encoding="utf-8")
STORY = (ROOT / "app/lib/story_v66.dart").read_text(encoding="utf-8")
RULES = (ROOT / "firestore.rules").read_text(encoding="utf-8")
PUBSPEC = (ROOT / "app/pubspec.yaml").read_text(encoding="utf-8")
RULE_TEST = (ROOT / "tools/firestore_rules_test.mjs").read_text(encoding="utf-8")
SETTINGS = (ROOT / "app/lib/build258_settings.dart").read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"V72 cihaz düzeltmesi eksik: {message}")


require("version: 1.0.81+300" in PUBSPEC, "Build 300 sürüm zinciri")
require("defaultValue: '1.0.81'" in MAIN and "defaultValue: '300'" in MAIN,
        "uygulama içi sürüm varsayılanları")
require("ValueKey('ngelx_tab_${secili}_$dil')" in MAIN,
        "açık sekmelerin dil değişiminde yeniden oluşturulması")
require("valueListenable:uygulamaDili" in SETTINGS,
        "ayarlar ekranlarının dil değişimini canlı dinlemesi")
require("match /content_tools/{contentId}" in RULES and "allow read, write: if isMe(uid)" in RULES,
        "kullanıcıya özel çeviri/altyazı önbellek kuralı")
require("content_translation_cache_$icerikId" in MAIN and "content_caption_cache_$icerikId" in MAIN,
        "yerel çeviri ve altyazı önbelleği")
require("ngelxPaylasimVeAltKayitlariniSil" in MAIN,
        "gönderi alt kayıtlarını güvenli silme")
require("get(/databases/$(database)/documents/videos/$(videoId)).data.ownerId" in RULES,
        "içerik sahibinin alt kayıt silme yetkisi")
require("users/alice/content_tools/owned_post" in RULE_TEST and
        "videos/owned_post/comments/comment_bob/likes/bob" in RULE_TEST,
        "Firestore cihaz regresyon testleri")
require("ngelxRouteObserver" in MAIN and "didPushNext()=>_gorunmezkenDuraklat" in MAIN,
        "profil tanıtım videosu sayfa yaşam döngüsü")
require("playedColor:Color(0xFF22D3EE)" in MAIN and "allowScrubbing:true" in MAIN,
        "Akış video ilerleme ve sarma çizgisi")
require("playbackUrl" in STORY and "Hikâye medyası bulunamadı" in STORY,
        "hikâye medya alanı geri dönüşleri")
require("yaziyorBaslatZamanlayici" in MAIN,
        "özel mesaj yazıyor durumunun geciktirilmesi")
require("Takip, içerikleri Akışında gösterir" in MAIN,
        "takip/arkadaşlık/mesaj açıklaması")
require("NgelX Premium" in MAIN and "workspace_premium_rounded" in MAIN,
        "kompakt Premium geçişi")
require("mediaUrls':adaylar" in MAIN and "ceviriUret(setP,dil:sec)" in MAIN,
        "çeviri dili değişiminde üretim ve altyazı medya geri dönüşleri")

print("V72 cihaz testi düzeltmeleri doğrulandı.")
