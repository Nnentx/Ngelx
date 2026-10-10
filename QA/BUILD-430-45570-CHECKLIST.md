# 45570.mp4 — 46 maddelik iş ve doğrulama listesi

Kaynak: Kullanıcının 51.28 saniyelik 45570.mp4 videosu. Videodaki maddeler aşağıdaki sırayla yazıldı. Kodda bir davranışın bulunması, cihaz testinden geçtiği anlamına gelmez.

Durumlar: **Kodlandı** = yeni düzeltme mevcut; CI geçti, telefon doğrulaması gerekiyor. **Mevcut** = önceki kaynakta davranış mevcut, yeni cihaz testi gerekiyor. **Açık** = tamamlanmış sayılmıyor.

| No | İş | Durum / kanıt |
|---|---|---|
|1|Gelen Kutusu gri ekran / yükleme|Build432 kodlandı: geç açılan sekmelere snapshot replay, 15 saniye ilk sonuç sınırı ve retry. Cihaz testi açık|
|2|Bildirimler listesinin görünmesi|Build431 metin/tarih ve koleksiyon doğrulaması + Build432 replay düzeltmesi. 45651 cihaz regresyonu sonrası yeni test gerekli|
|3|Bildirim sayacının 32'de kalması|Kodlandı: görünür satırların backend read güncellemesi|
|4|Tümü sayacının tutarlılığı|Kodlandı: mesaj istekleri ve bildirim uygunluğu ayrımı|
|5|Mesaj isteği sayısının tutarlılığı|Kodlandı: pending sohbetler ayrı sayılır; eski mükerrer sohbetler ayrıca incelenmeli|
|6|Mesaj isteği sayfasındaki boşluk|Build432 kodlandı: canlı kullanıcı/sohbet stream, açıklamalı boş durum ve aynı ekranda retry; cihaz yerleşimi testi açık|
|7|Yinelenen takip isteği|Kodlandı: transaction içinde güncel pending kontrolü|
|8|Yinelenen arkadaşlık isteği|Kodlandı: aynı transaction kontrolü|
|9|Bildirim gönderen isimlerinin mor olması|Mevcut Inbox; Activity kalın isimleri de mor yapıldı|
|10|Sohbet işlemlerindeki gereksiz yükleme|Build432 kodlandı: sayaç/liste/kart tek 200 kayıt sorgusu; hata veren kullanıcı cache kaydı atılır. Telefon performans ölçümü açık|
|11|Video hikâye yanıtı küçük önizlemesi|Kodlandı: video URL artık resim decoder'ına verilmez|
|12|Uzun video hikâye yükleme|Build432 kodlandı: 30 saniye initialization, devam eden preload bekleme, 15 saniye kayıt sorgusu sınırı. Uzun video cihaz testi açık|
|13|Başarısız videoda sonsuz yükleme|Build432 kodlandı: runtime video hatası, 20 saniye buffering sınırı, controller kapatma ve retry. Telefon testi açık|
|14|Hikâye kartının doğru içeriği açması|Mevcut: storyId bağlantısı; iki hesap testi gerekli|
|15|Arşiv ilk açılış yüklemesi|Build429 kodlandı: yükleme / hata / yeniden dene|
|16|Süresi dolan hikâyelerin otomatik arşivlenmemesi|Build429 filtre kodlandı; kalıcı server temizliği açık|
|17|Silinen hikâyenin medya ve kayıt temizliği|Build429 + owner/r2-video yolu düzeltmesi; cihaz testi gerekli|
|18|Hikâye videolarının tekrar yüklemesini azaltma|Build432 kodlandı: aynı preload tamamlanmadan yeniden kurulmaz; aktif video aynı hazırlığı kullanır. Ölçüm açık|
|19|Profil zilinin yalnız Bildirimler'e açılması|Kodlandı: iki gerçek profil düzeni de AktivitePage açar|
|20|Bildirim ekranında sohbet sekmeleri olmaması|Kodlandı: bağımsız AktivitePage|
|21|Profil zilinde kırmızı okunmamış sayaç|Kodlandı: ortak unread helper ile badge|
|22|Okunanların backend ve sayaçtan düşmesi|Kodlandı: read update, silinen kayıt yeniden yaratılmaz|
|23|Sıfır sayacın gizlenmesi|Kodlandı: count>0 şartı|
|24|Bildirim listesinin yükleme/hata durumu|Mevcut Activity; Inbox hata/yenileme eklendi|
|25|Profil içi arama performansı|Build432 kodlandı: retained replay stream, 220ms debounce ve retry; telefon performans ölçümü açık|
|26|Hikâye arşivi yükleme göstergesi/sorgusu|Build432 kodlandı: stateful retained arşiv sorgusu, bounded yükleme ve yerinde retry. Telefon ölçümü açık|
|27|Canlı geçmişinde eski kayıtlara saklama kuralı|Açık|
|28|Arşivde silinmiş içeriklerin gizlenmesi|Build432 kodlandı: owner/deleted/isDeleted/removed/hiddenFor ve yerel silme ID filtresi; eski snapshot da silineni gizler. Cihaz testi açık|
|29|Yavaş profil geçişleri|Build432 kodlandı: birleşik profil future yeniden buildlerde korunur; işlem/UID/oturum değişiminde temizlenir. Telefon ölçümü açık|
|30|Yeşil noktanın gerçek aktifliğe bağlı olması|Mevcut: heartbeat / 120 saniye sınırı|
|31|Son görülme|Mevcut; 16d/1s/2g formatı kodlandı|
|32|Son görülme süresinin güncellenmesi|Mevcut: 30 saniye timer / heartbeat; cihaz testi gerekli|
|33|Aktiflik gizliliği|Kodlandı: shared online helper showActivityStatus=false durumunu gizler|
|34|Kalıcı hikâye silme|Build429 kodlandı; telefon doğrulaması gerekli|
|35|Hikâye videosunun medya temizliği|Kodlandı: gerçek videos/uid R2 yolu desteklenir|
|36|Süresi dolan kaydedilmemiş hikâyenin temizlenmesi|Sunucu kodu hazır; Firebase önizleme 50 aday buldu, medya sahipliği doğrulanamadığı için 50 aday atlandı; zamanlanmış silme açık|
|37|Kaydedilmemiş canlı yayın geçmişinin tutulmaması|Açık|
|38|Silinen canlı yayın kaydı ve medya temizliği|Açık|
|39|Silinen gönderi ve ilişkili medya|Kodlandı: güncel sahip + medya temizliği tamamlanmadan kayıt kaldırılmaz|
|40|Silinen fotoğraf dosyası|Kodlandı: gönderi helper'ında beklenen güvenli R2/Firebase silme|
|41|Silinen video dosyası|Kodlandı: aynı helper; hata kaybolmaz|
|42|Silinen yorum kaydı|Mevcut: gönderi alt kayıt temizliği; tek yorum davranışı doğrulanmalı|
|43|Silinen tepki kaydı|Mevcut: likes/yorum likes temizliği; tek tepki davranışı doğrulanmalı|
|44|Benden sil / herkesten sil ayrımı|Mevcut: message hidden/deletedForEveryone; medya retry eksik|
|45|Silinen içerik önbelleği|Build430 medya eviction + Build432 arşiv/arama silme revizyonu; eski query satırı anında gizlenir. Mesaj medyası cache kontrolü açık|
|46|Sahipsiz medya güvenli temizliği|Açık: sunucu sahiplik/referans taraması gerekir|

## Koruma

Mesaj gönderme/alma, hikâye yanıtının DM'e gitmesi, kartın storyId'yi açması ve mevcut Firestore erişim kuralları korunur. Başka UID veya farklı Firebase bucket medyası silinmez. Kaydedilmiş/öne çıkarılmış içerikler otomatik silme kapsamına alınmadı.

## Doğrulama

Build395–429 kaynak oluşturma ve koruma zinciri yerel olarak geçti. Build430 kaynak kontratı geçti. GitHub Actions 38029954325 başarılı: Flutter analizi, 8 davranış testi, Firestore emulator testleri ve imzalı Build430 APK geçti. APK SHA256 ve artifact SHA256 doğrulandı. Gerçek cihaz sonuçları henüz yok. **46/46 tamamlandı iddiası yok.**

Sunucu read-only preview 38030838672 başarılı: 50 süresi dolmuş kaydedilmemiş hikâye adayı; medya sahipliği doğrulanmış 0, tanımlanamayan 50. Silinen kayıt/dosya 0. Otomatik silme etkin değil.

## Build430 cihaz kontrolü / Build431 takip

45636–45648 görüntülerinde Yapı430 kuruldu; profil zili ayrı Aktivite ekranını açtı ve kırmızı 2 sayacı okumadan sonra kayboldu. Gelen Kutusu gri ekranda kalmadan, mesaj ve grup listeleriyle açıldı. Mesaj istekleri boş durum ekranı açıldı. Bu tek deneme, aralıklı performans/gri ekran sorununun tamamen kapandığını kanıtlamaz.

Bildirimler sekmesindeki Yeni bildirim / Şimdi satırları ve sosyal istek sayısının mesaj kartıyla karışması Build431 paketinde düzeltildi. Analiz, 12 davranış testi, Firestore emulator ve imzalı APK üretimi geçti (Actions 38042908726). Üç ayrı istek kartı ve bildirim içeriklerinin cihaz testi açık.

## Build432 kapsamı

45651 cihaz regresyonu + 6, 10, 12, 13, 18, 25, 26, 28, 29, 45 numaralı 10 ek maddede kod değişikliği. Ayrıntılar QA/BUILD-432-TEN-FOLLOWUPS.md. Kod/CI ile telefon doğrulaması ayrı tutulur; kapalı madde sayısı uydurulmaz.

Build432 CI 38047626631 başarılı: üretim/koruma zinciri, Flutter analizi, 18 davranış testi, Firestore emulator, imzalı APK ve hash doğrulaması geçti. Telefon testi açık.
