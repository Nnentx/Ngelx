# Canlı yayın onaylı görsel referansları ve eksikler
Tarih: 2026-10-14 Europe/Istanbul.
Referanslar: 47016.png (izleyici), 47015.png (yayıncı). Kullanıcı bu iki görseli canlı yayın için istenen tasarım olarak tekrar belirtti.
Test kaydı: 47134.mp4; önceki bulgular docs/qa/2026-10-14-live-test-47134.md.

## Ortak düzen
- Tam ekran kamera görüntüsü.
- Üstte kırmızı CANLI rozeti, yayın süresi, göz simgeli izleyici sayacı ve sağda kapatma X.
- Altında yarı saydam koyu yayıncı kartı: avatar, ad ve kullanıcı adı.
- Yorumlar sol altta ayrı yarı saydam koyu kartlarda; her kartta yorumcu avatarı, adı ve mesaj. Ortak geniş koyu blok ve yayıncı hoş geldin kartıyla yorumları örtme yerine görseldeki ayrı kart düzeni uygulanmalı.
- Alt beyaz yuvarlak üst köşeli panel: yorum girişi, emoji düğmesi, ayrı turkuaz dairesel gönder düğmesi. İkon boyutları, aralıkları ve hizaları bu referanslara göre düzenlenmeli.
- Kamera görüntüsü panel yüksekliği değiştiğinde veya klavye açıldığında sıçramamalı.

## İzleyici ekranı — 47016.png
- Yayıncı kartında turkuaz çerçeveli Takip et.
- Sağ tarafta yükselen kalpler.
- Alt eylemler: Beğen, Hediye, Konuk ol, Paylaş.
- Panel altında Konuk olmak için yayıncıya istek gönder metni.
- Yayıncı kontrol satırı bu ekranın eylem satırı olarak kullanılmamalı.

## Yayıncı ekranı — 47015.png
- Yayıncı kartı içinde yeşil noktalı Bağlı göstergesi.
- Görüntü üzerinde sağ altta turkuaz Konuk ekle düğmesi; panel ortasındaki tek başına davet ikonu yerine.
- Alt eylemler: Mikrofon, Kamera, PK, Efektler, Paylaş.
- Kontrollerin altında geniş kırmızı Yayını bitir düğmesi.
- Yayıncı ve izleyici eylemleri rollerine göre ayrı gösterilmeli.
- Kullanıcının onayladığı açık kontrol paneli tasarımı, yalnızca önceki kompakt üç nokta önerisiyle değiştirilmemeli; görünür alan dengesi bu referanslarla sağlanmalı.

## Kullanıcı tarafından bildirilen hata
Yayıncı olarak yorum yazarken klavye beklenmedik şekilde kapanıyor ve yazmayı kesiyor. Kullanıcı 01:09 mesajında bunu açıkça bildirdi. Odak, text controller ve yeniden oluşturma davranışı incelenmeli; yazılan metin ve odak korunmalı. Bu hata henüz düzeltilmiş veya nedeni doğrulanmış değil.

## Test kaydından diğer açıklar
- Klavye açıkken yorum satırı kısmen kesiliyor.
- Mevcut alt araç kartındaki boşluklar görüntüyü fazla kapatıyor; referanstaki düzenle birlikte ele alınmalı.
- Boş katılım isteği paneli gereğinden yüksek.
- Karşı cihaz sesi, konuk kabulü, PK ve yayın sonlandırma henüz bu kayıtla doğrulanmadı.

Bu belge yalnızca kabul edilen referansı ve eksikleri kaydeder. Uygulamaya bu tasarım henüz uygulanmadı; toplu düzeltme paketine dahil edilecek.

## 01:13 kullanıcı eklemesi: kalp animasyonu
Kullanıcı kalbe basınca referans görseldeki gibi kalplerin çoğalıp yükselerek kaybolmadığını bildirdi. Bu, kullanıcı tarafından bildirilen açık hatadır; henüz düzeltilmedi.
Kabul ölçütü: Her beğeni dokunuşunda sağ tarafta yeni kalp oluşmalı; seri dokunuşlarda birden fazla kalp eşzamanlı görünmeli; kalpler yukarı hareket ederken saydamlaşıp kaldırılmalı. Yorum girişi ve yayın kontrollerinin dokunmasını engellememeli; biten animasyonlar temizlenmeli.

## Kullanıcının not edilmesini onayladığı ek öneriler
Bu maddeler öneri ve kontrol kapsamıdır; kod incelemesi/cihaz testi yapılmadan doğrulanmış hata veya tamamlanmış iş sayılmaz.
- Yorum yazılırken metin, taslak ve odak korunmalı; yeni yorum/panel değişikliği klavyeyi kapatmamalı.
- Konuk isteğinde gönderildi, bekliyor, kabul edildi, reddedildi durumları ve iptal işlemi.
- Bağlantı koptuğunda yeniden bağlanıyor durumu; yanlışlıkla yayın sonlandırmama.
- Mikrofon/kamera açık-kapalı durumlarının ikonlarda belirgin gösterimi.
- Yayını bitirme onayı; bitişte süre ve izleyici özeti.
- Yayıncı için yorum silme, kullanıcı susturma ve engelleme.
- İzleyicinin çıkması yayını bitirmemeli; konuk ayrılınca yayıncı devam etmeli.
- Hediye işlevi hazır değilse çalışır gibi sunulmamalı.
Öncelik: Klavye hatası, onaylı tasarım ve kalp animasyonu; ardından konuk akışı, bağlantı ve gerçek cihaz ses testleri.

## 01:13 Konuk ekle zorunlu işlevi
Kullanıcı Konuk ekle düğmesinin çalışmasını istedi. Toplu düzeltme paketinin zorunlu kabul ölçütü:
- Yayıncı düğmeye dokununca mevcut izleyiciler ve bekleyen konuk istekleri görünmeli; boş durum açıkça gösterilmeli.
- Yayıncı mevcut izleyiciyi davet edebilmeli; davet izleyici ekranında görünmeli.
- İzleyici daveti kabul veya reddedebilmeli; Konuk ol üzerinden istek gönderebilmeli; yayıncı kabul veya reddedebilmeli.
- Kabul, gerekli mikrofon/kamera izinleriyle gerçek konuk bağlantısına dönüşmeli; durum göstergesi yalnızca bağlantı kurulunca bağlı olmalı.
- Yayıncı ve konuğun görüntü/sesi iki gerçek cihazda doğrulanmalı.
- Konuk ayrılabilmeli veya yayıncı konuğu çıkarabilmeli; ana yayın devam etmeli.
Bu işlevin şu an tamamlandığı veya testten geçtiği iddia edilmedi.
