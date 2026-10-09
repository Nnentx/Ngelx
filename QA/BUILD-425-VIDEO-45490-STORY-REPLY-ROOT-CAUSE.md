# NgelX — 45490.mp4 gerçek hikâye yanıt hatası ve Build 425

**Tarih:** 2026-10-09. Kanıt: bu konuşmadaki `45490.mp4` (yaklaşık 34 saniye), `45492.jpg` özel sohbet ekran görüntüsü. 
**Gözlem:** 45490.mp4'nin yaklaşık 13–21. saniyelerinde açık hikâye serisinin altındaki mesaj alanına `tfff` gibi yanıt yazılıp gönderiliyor, ardından mavi Snackbar **“Hikâye yanıtı gönderilemedi.”** uyarısı görünüyor. 45492.jpg'deki özel sohbet ekranında yeni hikâye yanıtının göründüğü doğrulanamıyor.

## Kesin teknik bulgu
- Kullanıcının gerçek hikâye ekranı `NgelXHikayeSeriPage` (`app/lib/story_v66.dart`) bileşenidir.
- `story_v66.dart` içindeki `_yanitGonder()` eski kodu, `chats/{id}` yazısı, `chats/{id}/messages` mesajı **ve** `videos/{storyId}` dokümanındaki `replyCount` artışını **tek Firestore batch** ile gerçekleştiriyordu.
- Mevcut `firestore.rules` kullanıcıya başkasının video belgesindeki `replyCount` alanını güncelleme yetkisi tanımıyor; bu nedenle toplu işlem izin hatasıyla reddedilebilir ve mesaj hiç kaydedilmez. Güvenlik kuralını genişletmek gerekli değildir.
- **Önceki Build 422–424 çalışmaları başka bir ekran olan `main.dart/HikayeGosterPage` içindeki yanıt yöntemini düzeltmiş; fiilen kullanılan `story_v66.dart` yöntemi değişmeden kalmış.** Hatanın tekrarlamasının belirgin nedeni budur.
- Uyarı metni ile gerçek ekran kodu birebir eşleşir.

## Build 425 düzeltmesi
- Gerçek `story_v66.dart` içindeki yanıt yöntemi, Build 424'te hazırlanan gizlilik korumalı mesaj-öncelikli gönderim yöntemiyle değiştirilir.
- Yalnızca yetkili sohbete ve gerçek `videos/{storyId}.ownerId` sahibine; mevcut DM varsa **aynı DM'nin** `messages` koleksiyonuna doğrudan `story_reply` kaydedilir.
- Metin ve emoji yanıtlarında hikâye kimliği ve medya alanları korunur; sohbet önizlemesi/okunmamış sayacı sonradan güncellenir, hatası mesajı geri almaz.
- Önceden başarısızlığı tetikleyen hikâye `replyCount` batch güncellemesi kaldırılır; eksik yetkiyi gevşetmedik.
- Test betiği gerçek `story_v66.dart` dosyasını kaynak düzeyinde korur. Firebase emülatör testleri, Flutter analiz, Android sürüm 425 APK derlemesi ve imza kontrolü başarılı (GitHub run `37979592170`).
- **Gerçek cihazdan iki ayrı hesapla karşı DM teslimi hâlâ test edilmeli**; otomatik başarı, canlı teslim garantisi değildir.

**Başarı ölçütü:** Mevcut hikâyeye yanıt gönderen kullanıcı `Yanıtın gönderildi` bilgisini görür; hikâye sahibinin **mevcut** özel sohbetinde, hikâyeye bağlı yeni mesaj görünür; tekrarlı/duble DM üretilmez; mesaj ve tepki ayrı ayrı denenir.
