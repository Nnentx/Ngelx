# 45570.mp4 — 46 maddelik iş ve doğrulama listesi

Kaynak: Kullanıcının 51.28 saniyelik 45570.mp4 videosu. Videodaki maddeler aşağıdaki sırayla yazıldı. Kodda bir davranışın bulunması, cihaz testinden geçtiği anlamına gelmez.

Durumlar: **Kodlandı** = yeni düzeltme mevcut, CI/telefon doğrulaması gerekiyor. **Mevcut** = önceki kaynakta davranış mevcut, yeni cihaz testi gerekiyor. **Açık** = tamamlanmış sayılmıyor.

| No | İş | Durum / kanıt |
|---|---|---|
|1|Gelen Kutusu gri ekran / yükleme|Açık; gerçek cihazda tekrarlanmalı|
|2|Bildirimler listesinin görünmesi|Kodlandı: hata/yenileme durumu ve ortak stream|
|3|Bildirim sayacının 32'de kalması|Kodlandı: görünür satırların backend read güncellemesi|
|4|Tümü sayacının tutarlılığı|Kodlandı: mesaj istekleri ve bildirim uygunluğu ayrımı|
|5|Mesaj isteği sayısının tutarlılığı|Kodlandı: pending sohbetler ayrı sayılır; eski mükerrer sohbetler ayrıca incelenmeli|
|6|Mesaj isteği sayfasındaki boşluk|Açık: cihaz yerleşimi doğrulanmalı|
|7|Yinelenen takip isteği|Kodlandı: transaction içinde güncel pending kontrolü|
|8|Yinelenen arkadaşlık isteği|Kodlandı: aynı transaction kontrolü|
|9|Bildirim gönderen isimlerinin mor olması|Mevcut Inbox; Activity kalın isimleri de mor yapıldı|
|10|Sohbet işlemlerindeki gereksiz yükleme|Açık: performans ölçümü gerekiyor|
|11|Video hikâye yanıtı küçük önizlemesi|Kodlandı: video URL artık resim decoder'ına verilmez|
|12|Uzun video hikâye yükleme|Mevcut: 12 saniye initialization timeout / ön yükleme; cihaz testi gerekli|
|13|Başarısız videoda sonsuz yükleme|Mevcut: videoHata ve Tekrar dene; cihaz testi gerekli|
|14|Hikâye kartının doğru içeriği açması|Mevcut: storyId bağlantısı; iki hesap testi gerekli|
|15|Arşiv ilk açılış yüklemesi|Build429 kodlandı: yükleme / hata / yeniden dene|
|16|Süresi dolan hikâyelerin otomatik arşivlenmemesi|Build429 filtre kodlandı; kalıcı server temizliği açık|
|17|Silinen hikâyenin medya ve kayıt temizliği|Build429 + owner/r2-video yolu düzeltmesi; cihaz testi gerekli|
|18|Hikâye videolarının tekrar yüklemesini azaltma|Mevcut ön yükleme; ölçüm açık|
|19|Profil zilinin yalnız Bildirimler'e açılması|Kodlandı: iki gerçek profil düzeni de AktivitePage açar|
|20|Bildirim ekranında sohbet sekmeleri olmaması|Kodlandı: bağımsız AktivitePage|
|21|Profil zilinde kırmızı okunmamış sayaç|Kodlandı: ortak unread helper ile badge|
|22|Okunanların backend ve sayaçtan düşmesi|Kodlandı: read update, silinen kayıt yeniden yaratılmaz|
|23|Sıfır sayacın gizlenmesi|Kodlandı: count>0 şartı|
|24|Bildirim listesinin yükleme/hata durumu|Mevcut Activity; Inbox hata/yenileme eklendi|
|25|Profil içi arama performansı|Kodlandı: stream tuş vuruşlarında yeniden kurulmaz|
|26|Hikâye arşivi yükleme göstergesi/sorgusu|Build429 kodlandı; ölçüm açık|
|27|Canlı geçmişinde eski kayıtlara saklama kuralı|Açık|
|28|Arşivde silinmiş içeriklerin gizlenmesi|Build429 filtre kodlandı; arama da deleted/isDeleted filtreler|
|29|Yavaş profil geçişleri|Açık: ölçüm gerekir|
|30|Yeşil noktanın gerçek aktifliğe bağlı olması|Mevcut: heartbeat / 120 saniye sınırı|
|31|Son görülme|Mevcut; 16d/1s/2g formatı kodlandı|
|32|Son görülme süresinin güncellenmesi|Mevcut: 30 saniye timer / heartbeat; cihaz testi gerekli|
|33|Aktiflik gizliliği|Kodlandı: shared online helper showActivityStatus=false durumunu gizler|
|34|Kalıcı hikâye silme|Build429 kodlandı; telefon doğrulaması gerekli|
|35|Hikâye videosunun medya temizliği|Kodlandı: gerçek videos/uid R2 yolu desteklenir|
|36|Süresi dolan kaydedilmemiş hikâyenin temizlenmesi|Açık: güvenli sunucu bakım mekanizması gerekir|
|37|Kaydedilmemiş canlı yayın geçmişinin tutulmaması|Açık|
|38|Silinen canlı yayın kaydı ve medya temizliği|Açık|
|39|Silinen gönderi ve ilişkili medya|Kodlandı: güncel sahip + medya temizliği tamamlanmadan kayıt kaldırılmaz|
|40|Silinen fotoğraf dosyası|Kodlandı: gönderi helper'ında beklenen güvenli R2/Firebase silme|
|41|Silinen video dosyası|Kodlandı: aynı helper; hata kaybolmaz|
|42|Silinen yorum kaydı|Mevcut: gönderi alt kayıt temizliği; tek yorum davranışı doğrulanmalı|
|43|Silinen tepki kaydı|Mevcut: likes/yorum likes temizliği; tek tepki davranışı doğrulanmalı|
|44|Benden sil / herkesten sil ayrımı|Mevcut: message hidden/deletedForEveryone; medya retry eksik|
|45|Silinen içerik önbelleği|Kodlandı: medya cache eviction ve post invalidation; mesaj cache kontrolü açık|
|46|Sahipsiz medya güvenli temizliği|Açık: sunucu sahiplik/referans taraması gerekir|

## Koruma

Mesaj gönderme/alma, hikâye yanıtının DM'e gitmesi, kartın storyId'yi açması ve mevcut Firestore erişim kuralları korunur. Başka UID veya farklı Firebase bucket medyası silinmez. Kaydedilmiş/öne çıkarılmış içerikler otomatik silme kapsamına alınmadı.

## Doğrulama

Build395–429 kaynak oluşturma ve koruma zinciri yerel olarak geçti. Build430 kaynak kontratı geçti. Flutter davranış testleri, analiz ve APK için ayrı GitHub Actions workflow hazırlandı. Gerçek cihaz sonuçları henüz yok. **46/46 tamamlandı iddiası yok.**
