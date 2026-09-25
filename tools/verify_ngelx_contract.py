#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app" / "lib" / "main.dart"
GROUP_QUALITY = ROOT / "app" / "lib" / "group_quality.dart"
WORKER = ROOT / "cloudflare" / "worker" / "src" / "index.js"
RULES = ROOT / "firestore.rules"
PUBSPEC = ROOT / "app" / "pubspec.yaml"

app = APP.read_text(encoding="utf-8")
group_quality = GROUP_QUALITY.read_text(encoding="utf-8")
worker = WORKER.read_text(encoding="utf-8")
rules = RULES.read_text(encoding="utf-8")
pubspec = PUBSPEC.read_text(encoding="utf-8")

errors = []

# The original NgelX logo implementation is a protected design asset.
# Individual screens may hide it by layout/visibility rules, but the shared
# Logo widget and original image assets must not be deleted or replaced.
for token in (
    "class Logo extends StatelessWidget",
    "'assets/ngelx_logo.png'",
    "'assets/ngelx_logo_horizontal.png'",
):
    if token not in app:
        errors.append("Eski NgelX logo tasarım kodu korunmalı: " + token)
for token in (
    "- assets/ngelx_logo.png",
    "- assets/ngelx_logo_horizontal.png",
):
    if token not in pubspec:
        errors.append("Eski NgelX logo asset kaydı korunmalı: " + token)

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

# Create/publishing flow must remain functional and must not regress into fake controls.
for token in (
    "class _YeniYuklePageState",
    "ngelxMedyaYukleDosya",
    "retrieveLostData()",
    "Fotoğraf en fazla 10 MB",
    "Video en fazla 50 MB",
    "Hikâye yayınlandı • 24 saat görünür.",
    "Bu içerik yeniden paylaşıma kapalı.",
    "'clientCreatedAt':Timestamp.now()",
    "'allowReshare':yenidenPaylasimaIzin",
):
    if token not in app:
        errors.append("Üret/yayınlama sözleşmesi eksik: " + token)

for forbidden in (
    "class EskiYuklePage",
    "Zamanla'))",
    "Otomatik altyazı'), value: otomatikAltyazi",
    "Ortak gönderi'), value: ortakGonderi",
    "aracı açıldı",
):
    if forbidden in app:
        errors.append("Üret ekranında eski/sahte kontrol kaldı: " + forbidden)

# Settings must show the real build version instead of a stale hard-coded UI label.
for token in (
    "NGELX_VERSION_NAME",
    "NGELX_BUILD_NUMBER",
    "v$ngelxVersionName • ${t(\"build\")} $ngelxBuildNumber",
):
    if token not in app:
        errors.append("Uygulama sürüm etiketi otomatik değil: " + token)
if "V42 • Geliştiriliyor" in app:
    errors.append("Eski sabit V42 sürüm etiketi kaldı.")

# Group creation must give the media service enough time to upload the selected avatar.
if "kind: 'groups'" in app and ").timeout(const Duration(seconds:75));" not in app:
    errors.append("Grup fotoğrafı yükleme zaman aşımı güvenli aralığa çıkarılmadı.")

# Authenticated account changes must rebuild account-scoped UI state.
for token in (
    "durum_${kullanici?.uid??'guest'}_$dil",
    "ana_${kullanici.uid}_$dil",
):
    if token not in app:
        errors.append("Hesap değişiminde UI state izolasyonu eksik: " + token)

# Guest/anonymous entry is intentionally removed. Legacy anonymous sessions must be signed out.
for forbidden in (
    "Misafir olarak keşfet",
    "Explore as guest",
    "Als Gast entdecken",
    "استكشف كضيف",
    "Войти как гость",
):
    if forbidden in app:
        errors.append("Kaldırılan misafir giriş metni/kodu geri gelmiş: " + forbidden)
for token in (
    "FirebaseAuth.instance.currentUser?.isAnonymous==true",
    "kullanici==null||kullanici.isAnonymous",
):
    if token not in app:
        errors.append("Eski anonim oturum temizliği eksik: " + token)

# Hidden-word editing uses a dedicated page to avoid modal/IME inherited-widget teardown crashes.
for token in (
    "class GizliKelimelerPage",
    "FocusManager.instance.primaryFocus?.unfocus()",
    "builder:(_)=>GizliKelimelerPage(",
):
    if token not in app:
        errors.append("Gizli kelime çökme koruması eksik: " + token)
if "class _GizliKelimeSheet" in app:
    errors.append("Gizli kelimelerde eski bottom-sheet yaşam döngüsü geri gelmiş.")

# Android media networking has native fallbacks for Worker presign and signed R2 PUT.
for token in (
    "_ngelxAndroidNativeGet",
    "_ngelxAndroidNativeR2Put",
    "android-native-httpurlconnection",
    "filePath:dosya.path",
):
    if token not in app:
        errors.append("Android medya ağ fallback sözleşmesi eksik: " + token)

# Primary screens must use the shared language system instead of fixed Turkish labels.
for token in (
    "t('settingsTitle')",
    "t('editProfile')",
    "t('searchExplore')",
    "t('createNew')",
    "t('publishOnNgelx')",
    "kitleEtiketi(e)",
):
    if token not in app:
        errors.append("Uygulama dili ana ekranlara bağlanmamış: " + token)
for forbidden in (
    "title:const Text('Ayarlar ve gizlilik')",
    "hintText: 'Kişi, grup veya içerik ara'",
    "const Text('Yeni içerik üret'",
):
    if forbidden in app:
        errors.append("Ana ekranda sabit Türkçe metin kaldı: " + forbidden)

# Social request cards must stay live and must not read deterministic request docs before create.
for token in (
    "StreamSubscription<DocumentSnapshot<Map<String,dynamic>>>? _hesapAboneligi",
    "StreamSubscription<QuerySnapshot<Map<String,dynamic>>>? _gidenIstekAboneligi",
    "sosyalIstekGonder(",
    "gidenSosyalIstekBekliyor(",
    "where('fromUid',isEqualTo:uid).limit(100).snapshots()",
    "color:Colors.black87,fontWeight:FontWeight.w900,fontSize:16",
):
    if token not in app:
        errors.append("Keşfet sosyal ilişki canlılık sözleşmesi eksik: " + token)
for forbidden in (
    "doc('friend_request_'+",
    "doc('follow_request_'+",
):
    if forbidden in app:
        errors.append("İstek gönderiminde permission-denied üreten eski deterministik belge okuması kaldı: " + forbidden)

# Explore must not suggest the signed-in account and must not fake online presence.
for token in (
    "d.id!=ben&&d.data()['deactivated']!=true",
    "v['isOnline']==true&&v['showActivityStatus']!=false",
):
    if token not in app:
        errors.append("Keşfet kişi kartı kapsam/aktiflik koruması eksik: " + token)

# Inbox filters keep stable internal codes while visible labels follow the selected app language.
for token in (
    "t('inbox')",
    "t('messageRequests')",
    "sohbetFiltreEtiketi(f)",
    "case 'Okunmamış': return t('unread')",
    "case 'Gruplar': return t('groups')",
):
    if token not in app:
        errors.append("Gelen Kutusu dil sözleşmesi eksik: " + token)
for forbidden in (
    "const Text('Gelen Kutusu'",
    "hintText:'Sohbetlerde ara'",
    "child:Text(f,maxLines:1)",
):
    if forbidden in app:
        errors.append("Gelen Kutusu ana görünümünde sabit dil metni kaldı: " + forbidden)

# Profile-to-chat entry must honor the target account's message permission.
for token in (
    "final mesajIzni=(v['messagePermission']",
    "mesajIzni=='friends'&&arkadaslar.contains(uid)",
    "mesajIzni=='following'&&hedefinTakipEttikleri.contains(me)",
    "t('messageNotAllowed')",
):
    if token not in app:
        errors.append("Profil mesaj gizliliği sözleşmesi eksik: " + token)

# New-chat picker must apply the same target message permission before creating a conversation.
for token in (
    "final izin=(v['messagePermission']",
    "izin=='friends'&&arkadaslar.contains(d.id)",
    "izin=='following'&&hedefinTakipEttikleri.contains(me)",
    "final kabulEdildi=cv['requestAccepted_$me']==true",
):
    if token not in app:
        errors.append("Yeni sohbet mesaj gizliliği sözleşmesi eksik: " + token)

# Firestore must enforce private-chat message privacy, not only the client UI.
for token in (
    "function privateChatCreateAllowed()",
    "messagePermission",
    "permission == 'friends'",
    "permission == 'following'",
    "privateChatCreateAllowed()",
):
    if token not in rules:
        errors.append("Firestore özel mesaj gizliliği eksik: " + token)

# Large private-chat files must stream from disk and private photos need a realistic upload window.
private_file_block = re.search(r"Future<void> dosyaGonder\(\)async\{(.*?)\n  \}", app, re.S)
if private_file_block:
    if "ngelxMedyaYukleDosya" not in private_file_block.group(1):
        errors.append("Özel sohbet dosyası streaming yüklemeyi kullanmıyor.")
    if "readAsBytes()" in private_file_block.group(1):
        errors.append("Özel sohbet dosyası hâlâ tamamını RAM'e alıyor.")
if "kind: 'chats'" in app and ").timeout(const Duration(seconds:60));" not in app:
    errors.append("Özel sohbet fotoğrafı yükleme zaman aşımı güvenli aralıkta değil.")

# Accepted private conversations remain reachable even if new-message privacy later becomes stricter.
for token in (
    "cv['requestAccepted_$me']==true||cv['requestAccepted_$uid']==true",
    "final kabulEdildi=cv['requestAccepted_$me']==true",
):
    if token not in app:
        errors.append("Kabul edilmiş sohbet erişimi gizlilikle uyumlu değil: " + token)

# Message-permission detail UI keeps stable permission codes while localizing visible labels.
for token in (
    "t('whoCanMessage')",
    "mesajIzinEtiketi(kod)",
    "mesajIzinAciklama(kod)",
    "for(final kod in const ['all','following','friends','none'])",
    "t('activityLoadFailed')",
    "t('noActivity')",
):
    if token not in app:
        errors.append("Mesaj izinleri/Aktivite dil sözleşmesi eksik: " + token)

# Main feed must show real content only and keep user filters/live behavior intact.
for token in (
    "class _VideoAkisiState",
    "_profilAboneligi",
    "'hiddenContent'",
    "'notInterestedIds'",
    "_goruntulemeKaydet",
    "FieldValue.increment(1)",
    ".orderBy('createdAt',descending:true)",
    ".limit(50)",
    "aciklama:(item['description']??'').toString()",
    "widget.aciklama.trim()",
    "paylasanProfiliAc",
):
    if token not in app:
        errors.append("Akış sözleşmesi eksik: " + token)

for forbidden in (
    "ornekVideolar",
    "flutter.github.io/assets-for-api-docs/assets/videos/bee.mp4",
    "media.w3.org/2010/05/sintel/trailer.mp4",
    "Anı yakala, kendi hikâyeni paylaş ✨",
    "class CanliEtkilesimOzet",
):
    if forbidden in app:
        errors.append("Akışta eski/sahte/gereksiz kod kaldı: " + forbidden)

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
    "_aramaFiltresineUyar",
    "_aramaSonucuAc",
    "Medyayı aç",
    "Videoyu aç",
    "Bağlantılar",
    "Dosyalar",
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

# Consolidated group hardening must stay intact.
for token in (
    "KURUCU • Yönetici",
    "formerMembers",
    "removedAt_",
    "quickEmoji':'👍'",
    "_gruptanCikarildiPaneli",
    "_mentionProfiliAc",
    "aktifAramadanAcildi",
    "_aramaEkraniniKucult",
    "kameraCevir",
    "görüntülü aramaya katıldı.",
    "sesli aramaya katıldı.",
    "Kuruculuğu devret",
    "Önce kuruculuğu devret",
    "Tepki eklenemedi. Tekrar dene.",
    "onDoubleTap:()=>grupKalpBirak(d)",
    "action:'member_added'",
    "Bu seçim gruptaki herkeste aynıdır.",
    "['👍','❤️','😘','🥰','😂','🔥','👏','🐥']",
    "'senderId':actor",
    "systemAction':'member_joined'",
    "systemAction':'call_join'",
    "systemAction':'call_leave'",
    "systemAction':'call_end'",
    "Önce kuruculuğu devret",
    "groupDeleted':true",
    "this.aktifAramadanAcildi=false",
    "canPop:bitisDurumu!=null",
    "Arama küçültülemedi. Arama devam ediyor.",
    "MediaQuery.viewInsetsOf(context).bottom",
    "_yerelVideo",
):
    if token not in app:
        errors.append("Konsolide grup düzeltmesi eksik: " + token)

for token in (
    "founderProtected()",
    "validFounderTransfer()",
    "validFormerHide()",
    "validFounderClose()",
    "formerChatMember()",
    "formerMembers",
    "removedAt_",
    "request.resource.data.get('systemAction', '') in [",
    "'member_added'",
    "'member_joined'",
    "'member_left'",
    "'call_join'",
    "'call_leave'",
    "'call_end'",
    "resource.data.get('formerMembers', []).removeAll([request.auth.uid])",
    "onlyChanges(['members', 'formerMembers', 'hiddenFor', 'updatedAt'])",
):
    if token not in rules:
        errors.append("Firestore grup koruması eksik: " + token)
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

# Private-chat voice recording must reset cleanly and use the polished recorder composer.
for token in (
    "sesKaydiniIptal",
    "_ozelSesKaydiSureYazisi",
    "_ozelSesKaydiSayaciniBaslat",
    "_ozelSesKaydiDurumunuTemizle",
    "_ozelSesliMesajiYukle",
    "Ses kaydı iptal edildi.",
    "tooltip:'Kaydı gönder'",
):
    if token not in app:
        errors.append("Özel sohbet ses kaydı sözleşmesi eksik: " + token)

# Build 251: private chat mirrors the group polish with a dedicated blue design,
# live last-active text, drafts, video sending, and group-only @herkes.
for token in (
    "const ngelxPrivateBlue = Color(0xFF146EF5)",
    "const ngelxPrivateBlueSoft = Color(0xFFEAF3FF)",
    "class NgelXPrivateCard",
    "class AktiflikDurumuYazisi",
    "AktiflikDurumuYazisi(uid:widget.digerUid)",
    "PrivateDraftStore.load(widget.chatId)",
    "Future<void> videoGonder(ImageSource kaynak)",
    "TamEkranVideoPage(url:",
    "Future<void> ozelMesajBilgisi",
    "_ozelSohbetGunEtiketi",
):
    if token not in app:
        errors.append("Özel sohbet mavi kalite sözleşmesi eksik: " + token)

for token in (
    "class PrivateDraftStore",
    "private_draft_",
):
    if token not in group_quality:
        errors.append("Özel sohbet taslak depolama sözleşmesi eksik: " + token)

private_start = app.find("class _SohbetPageState")
private_end = app.find("\nclass NgelXSesliMesaj", private_start)
private_chat = app[private_start:private_end if private_end > private_start else len(app)]
if "'uid':'all','username':'herkes'" in private_chat or "'username':'herkes'" in private_chat:
    errors.append("@herkes özel sohbette görünmemeli; yalnızca grup sohbetinde kullanılmalı.")
if "Bu sohbetteki herkesten bahset" not in app:
    errors.append("Grup sohbetinde @herkes komutu kaybolmuş.")

for token in (
    "style:TextStyle(color:Colors.black54,height:1.35)",
    "style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w900)",
):
    if token not in app:
        errors.append("Beyaz grup diyaloglarında okunabilir metin rengi koruması eksik: " + token)

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
if len(app) > 1_050_000:
    errors.append("main.dart beklenmedik şekilde büyüdü; tekrarlı kod eklenmiş olabilir.")

# Large group uploads must stream from disk instead of loading the whole file into RAM.
for token in (
    "grupVideoGonder",
    "grupDosyaGonder",
    "ngelxMedyaYukleDosya",
):
    if token not in app:
        errors.append("Grup medya streaming sözleşmesi eksik: " + token)
video_block = re.search(r"Future<void> grupVideoGonder\(\)async\{(.*?)\n  \}", app, re.S)
if video_block and "readAsBytes()" in video_block.group(1):
    errors.append("Grup videosu hâlâ tamamını RAM'e alıyor.")
file_block = re.search(r"Future<void> grupDosyaGonder\(\)async\{(.*?)\n  \}", app, re.S)
if file_block and "readAsBytes()" in file_block.group(1):
    errors.append("Grup dosyası hâlâ tamamını RAM'e alıyor.")

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


# Build 262: comment edit must not manually own/dispose a controller inside a
# transient dialog; that pattern caused a real _dependents.isEmpty framework
# assertion on Android. Keep the controller-free form-field lifecycle.
comment_card_start = app.find("class YorumKarti")
comment_card_end = app.find("\nclass EskiYorumlar", comment_card_start)
comment_card = app[comment_card_start:comment_card_end if comment_card_end > comment_card_start else len(app)]
comment_edit = re.search(r"else if \(secim == 'edit'\) \{(.*?)\n      \}", comment_card, re.S)
if not comment_edit:
    errors.append("Yorum düzenleme akışı bulunamadı.")
else:
    comment_edit_body = comment_edit.group(1)
    if "TextEditingController" in comment_edit_body or ".dispose()" in comment_edit_body:
        errors.append("Yorum düzenleme dialogu manuel controller/dispose kullanmamalı.")
    for token in ("TextFormField(", "initialValue:metin", "FocusScope.of(dialogContext).unfocus()"):
        if token not in comment_edit_body:
            errors.append("Yorum düzenleme yaşam döngüsü koruması eksik: " + token)

# Build 263: social request reliability + history/cancellation.
for token in (
    "Future<void> sosyalIstekIptalEt",
    "'status':'cancelled'",
    "class TakipIstegiGecmisiPage",
    "İstek geçmişi",
    "Takip ve arkadaşlık isteklerinin durumunu yönet",
    "zatenBekliyor",
    "zatenIliski",
):
    if token not in app:
        errors.append("Sosyal istek sözleşmesi eksik: " + token)
for token in (
    "resource.data.fromUid == request.auth.uid",
    "request.resource.data.get('status', '') == 'cancelled'",
    "affectedKeys().hasOnly(['status', 'read', 'cancelledAt'])",
):
    if token not in rules:
        errors.append("Sosyal istek Firestore iptal koruması eksik: " + token)

if errors:
    print("NgelX contract doğrulaması BAŞARISIZ:")
    for e in errors:
        print(" - " + e)
    sys.exit(1)

print("NgelX contract doğrulaması başarılı.")
print("App medya türleri:", ", ".join(sorted(app_kinds)))
print("Worker medya türleri:", ", ".join(sorted(worker_kinds)))
