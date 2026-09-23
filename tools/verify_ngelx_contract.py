#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app" / "lib" / "main.dart"
GROUP_QUALITY = ROOT / "app" / "lib" / "group_quality.dart"
WORKER = ROOT / "cloudflare" / "worker" / "src" / "index.js"
RULES = ROOT / "firestore.rules"

app = APP.read_text(encoding="utf-8")
group_quality = GROUP_QUALITY.read_text(encoding="utf-8")
worker = WORKER.read_text(encoding="utf-8")
rules = RULES.read_text(encoding="utf-8")

errors = []

# Every media kind sent by the Flutter app must be accepted by the R2 worker.
app_kinds = set(re.findall(r"kind\s*:\s*['\"]([^'\"]+)['\"]", app))
allowed_block = re.search(r"const ALLOWED_KINDS = new Set\(\[(.*?)\]\);", worker, re.S)
if not allowed_block:
    errors.append("R2 worker ALLOWED_KINDS bulunamadı.")
    worker_kinds = set()
else:
    worker_kinds = set(re.findall(r"['\"]([^'\"]+)['\"]", allowed_block.group(1)))
missing = sorted(app_kinds - worker_kinds)
if missing:
    errors.append("R2 worker eksik medya türleri: " + ", ".join(missing))

# New uploads must use the NgelX R2 media service only.
for forbidden in (
    "package:supabase_flutter/supabase_flutter.dart",
    "supa.Supabase.initialize(",
    "supa.Supabase.instance.client.storage",
):
    if forbidden in app:
        errors.append("Eski Supabase çalışma zamanı kodu kaldı: " + forbidden)

# The main profile avatar must directly open the photo editor.
profile_class = app.find("class _ProfilPageState")
if profile_class < 0:
    errors.append("Profil sayfası bulunamadı.")
else:
    profile_tail = app[profile_class:]
    if "onTap: fotografYukle" not in profile_tail:
        errors.append("Profil fotoğrafına dokunma fotografYukle akışına bağlı değil.")
    if "await user.updatePhotoURL(url)" not in profile_tail:
        errors.append("Profil fotoğrafı Firebase Auth photoURL ile senkronize edilmiyor.")
    if "CachedNetworkImage.evictFromCache(eski)" not in profile_tail:
        errors.append("Eski profil fotoğrafı önbellekten temizlenmiyor.")

# Contract tokens for the group experience. These guard accidental regressions.
required_group_tokens = [
    "class _GrupSohbetPageState",
    "grupAramasiBaslat",
    "grupVideoGonder",
    "grupDosyaGonder",
    "grupSesKaydiDegistir",
    "grupKonumGonder",
    "grupKalpBirak",
    "mentionOnerileri",
    "SabitlenenGrupMesajlariPage",
    "GrupMedyaPage",
    "GrupKatilmaIstekleriPage",
    "onlyAdminsCanPost",
    "onlyAdminsCanAddMembers",
    "onlyAdminsCanEditGroup",
    "onlyAdminsCanPin",
    "onlyAdminsCanMentionAll",
    "deletedForEveryone",
    "GroupDraftStore",
    "GroupOfflineQueue",
    "fetchGroupLinkPreview",
    "showGroupStickerPicker",
    "showGroupForwardSheet",
    "showGroupMessageInfo",
    "lastDeliveredAt_",
    "RoomReconnectingEvent",
    "_cevapsizSayaciniBaslat",
    "NgelXMedyaGaleriPage",
    "_grupSesliMesajiYukle",
    "_acilisOkunmamis",
    "Cevapsız görüntülü grup araması",
    "Tekrar Ara",
    "newMembersSeeHistory",
    "joinApproval",
    "lastReadAt_",
    "typing_",
    "mutedFor",
    "groupPhotoUrl",
    "GrupTakmaAdlarPage",
    "GrupOzellestirPage",
    "GrupAyarlarPage",
    "Sohbet üyelerini gör",
    "Davetler ve istekler",
    "Sohbet bilgileri",
    "Sohbet balonu aç",
    "Okundu bilgisi",
    "Yazma göstergesi",
    "Bir üyeyi engelle",
    "Şikayet et",
    "Sohbetten ayrıl",
    "Gruptan ayrılmak istiyor musun?",
    "Kaydı iptal et",
    "Kaydı gönder",
    "oynatici.positionStream",
    "Kişiler",
    "@herkes",
    "@sessiz",
    "Mesaj seçenekleri",
    "Daha fazla tepki",
    "reactionMore",
    "grupTepkiDetayi",
    "Bu mesaja tepki veren kişiler",
    "Kimler mesaj gönderebilir?",
    "Kimler kişi ekleyebilir?",
    "Kimler grup bilgisini düzenleyebilir?",
    "Kimler mesaj sabitleyebilir?",
    "Kimler @herkes kullanabilir?",
    "grupIzinSec",
    "grupAramasinaKisiDavetEt",
    "Grup aramasına davet et",
    "Davet gönderildi",
    "gorulenIds",
    "kişi gördü",
    "grupYanitiHazirla",
    "onHorizontalDragEnd",
    "kişi yazıyor",
    "•••",
    "Sesli mesaj",
    "Arama cevaplanmadı",
    "Kimse aramaya katılmadı. İstersen tekrar arayabilirsin.",
    "Sohbete dön",
    "bitisDurumu",
    "biriKabulEtti",
    "kimseKatilMadi",
    "Bağlantıyı kopyala",
    "linkUrl",
    "Sohbeti sil",
]
for token in required_group_tokens:
    if token not in app:
        errors.append("Grup özelliği sözleşmesi eksik: " + token)

# Group helper file contracts cover delivery/read details and offline resilience.
for token in (
    "showGroupMessageInfo",
    "deliveredOnlyIds",
    "Kim gördü, kime teslim edildi",
    "lastDeliveredAt_",
    "lastReadAt_",
    "GroupOfflineQueue",
):
    if token not in group_quality:
        errors.append("Grup kalite yardımcısı eksik: " + token)

# Polls are intentionally removed from NgelX group chat.
if "'type':'poll'" in app or '"type":"poll"' in app:
    errors.append("Anket özelliği kaldırıldığı halde uygulamada poll oluşturma kodu bulundu.")
if "request.resource.data.get('type', 'text') != 'poll'" not in rules:
    errors.append("Firestore anket mesajlarını engellemiyor.")

# Guard against accidental duplicate/replayed Dart blocks. This caught a real
# regression while the group polish work was being consolidated.
for token in (
    "class GrupSohbetPage",
    "class _GrupSohbetPageState",
    "class NgelXAramaPage",
    "class GrupBilgiPage",
    "class GrupMedyaPage",
    "class SohbetPage",
):
    count = app.count(token)
    if count != 1:
        errors.append(f"Tekrarlı/eksik Dart sınıfı: {token} ({count} adet)")
if len(app) > 1_000_000:
    errors.append("main.dart beklenmedik şekilde büyüdü; tekrarlı kod eklenmiş olabilir.")

# App/worker size contract for group videos and attachments.
if "80*1024*1024" in app and "videos: 80 * 1024 * 1024" not in worker:
    errors.append("Grup video boyutu app/worker arasında uyuşmuyor.")
if "30*1024*1024" in app and "'chat-files': 30 * 1024 * 1024" not in worker:
    errors.append("Grup dosya boyutu app/worker arasında uyuşmuyor.")

if "heic: 'image/heic'" not in worker or "heif: 'image/heif'" not in worker:
    errors.append("R2 worker HEIC/HEIF fotoğraf türlerini desteklemiyor.")

# Secure group invitation/join contract.
for token in (
    "match /joinRequests/{requestUid}",
    "match /group_invites/{code}",
    "validSelfJoin(chatId)",
    "validInvite(code, chatId)",
    "validMemberAddition()",
    "validMemberGroupEdit()",
    "onlyAdminsCanAddMembers",
    "onlyAdminsCanEditGroup",
    "onlyAdminsCanPin",
):
    if token not in rules:
        errors.append("Firestore grup davet kuralı eksik: " + token)

if ".collection('chats').where('inviteCode'" in app:
    errors.append("Uygulama hâlâ üye olmayan kullanıcı için yasak chats inviteCode sorgusunu kullanıyor.")
if ".collection('group_invites').doc(invite)" not in app:
    errors.append("Güvenli doğrudan grup davet belgesi akışı bulunamadı.")
if "status':onayGerekli?'pending':'autojoin'" not in app:
    errors.append("Grup davet onay/autojoin ayrımı bulunamadı.")

if errors:
    print("NgelX contract doğrulaması BAŞARISIZ:")
    for e in errors:
        print(" - " + e)
    sys.exit(1)

print("NgelX contract doğrulaması başarılı.")
print("App medya türleri:", ", ".join(sorted(app_kinds)))
print("Worker medya türleri:", ", ".join(sorted(worker_kinds)))
