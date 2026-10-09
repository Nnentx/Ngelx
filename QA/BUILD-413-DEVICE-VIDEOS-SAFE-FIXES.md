# NgelX Build 413 — 09.10.2026 cihaz videoları düzeltme paketi

## Onaylı Build 412'yi koruma sözleşmesi
Bu dal `work/build-412-profile-design-fixes` sürümünden ayrıldı. Ana dal, çalışan Android APK ve Firebase güvenlik kuralları değiştirilmedi. Kapaklı/kapaksız profil, gerçek avatar/kapak yükleme, dört sayaç, takip ve arkadaşlık isteklerinin mevcut callbacks, mesaj ve ortak grup geçişleri, profil video oynatıcısı ve gönderi grid'i korunur. Build395–412 kaynak testleri, emulator kuralları testi, Flutter analyze ve imzalı APK üretimi Build413 CI'da tekrar çalışır.

## Kodlanan ilk grup (Build 413)
1. Arkadaşlar listesinde doğrudan arkadaşlar için “Arkadaşın” etiketini kaybetme; ortak arkadaş sayısı varsa ayrıca göster.
2. Ziyaretçi takip/arkadaşlık düğmelerinin ilişki belgesi gelmeden yanlış “Takip et / Arkadaş ekle” göstermesini engelle.
3. Genel aramadaki ilk 60 kullanıcı sınırının yol açtığı kayıpları azalt: isim/kullanıcı adı için Firestore önek sorguları, arkadaşlar/takipleri dahil etme, sonucu UID ile tekilleştirme, hesap/sorgu bazlı önbellek ve 320 ms arama bekletmesi. Engelleme/görünürlük/gizlilik filtreleri aynı kalır.
4. Hikâye yanıtındaki `videos.replyCount/reactionCount` yetkisiz güncellemesi bütün batch'i bozuyordu. Bu istemci tarafı sayaç güncellemesi çıkarıldı. Özel sohbet erişimi ve mesaj izinleri doğrulanıp sohbet oluşturulduktan sonra mesaj ile sohbet özeti yazılır. Cloud backend ile güvenli hikâye sayaç güncellemesi ayrı iş olarak kalır.
5. “Eylül 2026’te katıldı” dilbilgisi hatası ay bağımsız “Eylül 2026 tarihinde katıldı” olur.
6. Android sürümü 1.0.188+413. Kaynak kodu dışında Firestore rules deploy **yok**.

## Cihazda onaylanması gerekenler
- Rojin -> Arkadaşlar -> Adem ve Dilek: “Arkadaşın”, varsa ayrıca “1 ortak arkadaş”.
- Rojin -> genel arama: “adem”, “ADEM”, “Adem” ve kullanıcı adı -> gizlilik izinleri uygunsa ilgili kişi görülmeli.
- Sultan/Adem/Rojin hesap değişimleri: takip/arkadaşlık durumları yüklenme tamamlandıktan sonra doğru olmalı.
- Hikâye yanıtı/emoji: daha önce sohbet varsa veya yeni mesaj izinliyse gidebilmeli; mesaj kısıtı varsa anlamlı açıklama çıkmalı.
- Kapaklı/kapaksız karşıdan görünüm, kaydetme, profil video, sayaç tıklama, gönderi geçişi ve Android alt navigasyon değişmemeli.

## Kalan işler (çalışıyor sayılmadı)
Gerçek cihazda düğme tıklama ve çift taraflı ilişki mutabakatı, bildirim teslimi, kırpma başlığı kesilmesi, dört eylem düğmesinin dokunma alanları, kapak önizleme akıcılığı, ziyaretçi yükleme süresi, avatar önbelleği, yeni kullanıcı arama sıralaması, hikâye süresi, tüm yazım ve sekme yerleşimi ayrıca takip edilecek.

**Durum:** Bunlar kodlanan düzeltmelerdir. CI sonucu ve gerçek cihaz testi başarılı olmadan “tamamlandı” olarak işaretlenmez.
