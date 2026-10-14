# Build 454 / 1.0.229 — yapı korunarak birleşik takip paketi

Test adayı kaynak: `bb3812282ce1189390dbc7ea3d3983b660c48e09`.
CI: https://github.com/Nnentx/Ngelx/actions/runs/38534413889

Mevcut Flutter, Firebase, LiveKit, Android bildirim servisleri, beyaz tema, mesaj teslim/izin kuralları ve onaylanan sayfa yapısı korunur. Build453 uygulama zincirinin sonunda küçük takip yaması uygulanır; uygulama yeniden yazılmadı.

## Uygulanan 11 başlık

1. Özel/grup sohbet fotoğrafına ekran genişliği ve yüksekliğine göre birlikte sınır; oran korunur ve tam ekran açma davranışı sürer.
2. Gelen metin balonları yumuşak açık gri; özel/grup mesaj ve alıntı yazıları okunaklı, dengeli ölçeklerde.
3. Yanıt/alınan metin daha soluk, yeni yanıt belirgin; özel sohbette yanıt başlığı eklendi. Var olan yanıt-hedefe gitme ve küçük medya önizlemesi korunur.
4. Mesaj yazma alanının yazı/yer tutucu ölçeği ve kontrastı tutarlı; mevcut ekleme, kamera, mikrofon, emoji, gönderme ve güvenli alan davranışı korunur.
5. Üst kişi şeridinin yüksekliği avatar ve adlara göre artırıldı; izin denetimli durum etiketi eklendi. Gelen kutusu sekme, saat ve metadata kontrast/ölçeği artırıldı.
6. Sahibin hikâye menüsünde Öne çıkandan kaldır ve profil dairesinde uzun basma ile kaldırma; onay, transaction sahiplik kontrolü, arşiv koruması. Mevcut veri modelinde her daire bir hikâyedir; daire kaldırılır, arşiv kalır.
7. Canlı yayın hazırlığının dar 430px yüksekliğe bağlı kartı kaldırıldı; kamera seçili oranla ekran genişliğini kullanır. Ayarlar aynı sayfada kaydırılabilir.
8. Gelen arama kartı adı/gövdesi aramayı kabul etmeden arama panelini açar. Android open eylemi işlenir. Devam eden görüşme bildirimi resume eylemini taşır, var olan oda/süre korunarak ekrana dönülür; küçültülmüş görüşme geri geldiğinde dönüş rotası yenilenir. Yerel zil sesi sessiz/DND/bildirim ayarlarına uyar ve ret/kabul/bitiş/zaman aşımında durur. Hesap geçişinde önceki dinleyici ve native zil temizlenir; eski auth callback yeni aboneliği ezemez.
9. Gelen arama sorgusu/profil okumaları ve topluluk akış stream'leri tekrar çizimlerde yeniden oluşturulmaz. Fotoğraf bellek yükü sınırlandırılır. Gerçek cihaz hız kazanımı henüz ölçülmedi.
10. Topluluk ara yazısı, simgesi, metni ve imleci açık zeminde koyu/okunaklı.
11. Topluluk paylaşımı fotoğraf/video önizlemesi ve video süresi, gerçek bayt yüzdesi/MB, hazırlık/yükleme/kayıt aşamaları sunar. Medya yüklemesi başarılı ama kayıt tekrar denenirse aynı taslak kimliği/medya URL'si kullanılır; kayıt zaman aşımında sunucudan sonuç kontrol edilir. Kompozisyon ve topluluk başlığı kartları tamamlandı. Eksik composite indeksinde yalnızca approved kayıtları okuyan tek alanlı akışa geçilir; istemcide tarih sırası ve görünür sayfa limiti korunur. Bu yedek sorgu onaylı kayıtların tamamını dinler; indeks hazır olduğunda tekrar dene/yeniden açma sınırlı kronolojik sorguya döner. İndeks yönetim yetkisi değiştirilmedi.

## Doğrulama ve açık işler

- Yerel 60 sunucu/arama/bildirim yetkilendirme testi geçti; yeni uygulama kodunun Flutter, davranış, güvenlik ve imzalı APK kontrolleri CI'da başarılı.
- Yeni arayüz testi küçük ekranda çok dik fotoğrafın sınırını ve oran korunmasını; birim testi bilinmeyen toplam boyut/yeniden denemede gerçek yükleme yüzdesini kontrol eder.
- Önceki canlı taslak/kalp, küçük ekran, davranış ve Firestore güvenlik testleri tekrar çalışır.
- Fiziksel iki telefonda sesli/görüntülü ve grup çağrısı, hesap değiştirme, ekran kilidi, ret/kabul/zaman aşımı, kart/bildirimden dönüş ayrıca denenmeli. Otomatik testler gerçek zil sesini kanıtlamaz.
- Gerçek cihazda topluluk medya seçimi/yükleme, başarısız bağlantıdan tekrar deneme ve gönderinin akışta görünmesi kontrol edilmeli.
- Hikâye kaldırma sahibinde görünmeli, iptal arşivi/öne çıkanı değiştirmemeli, ziyaretçi işlem yapamamalı.

## Teslim doğrulaması

Derleme başarılı: 38534413889. APK sürümü 1.0.229 / 454; önceki kurulumla uyumlu imza doğrulandı. GitHub artifact ZIP özeti ve içindeki APK özeti yerel indirmede tekrar doğrulandı.
APK SHA256: `76d9e5a34665f73bf32309dc1207df0e2c3e3584608f39986dc60d570fea97a7`.
APK boyutu: 147464133 bayt.
