# Build 456 — Android cihaz kabul testi (ücretsiz, veri kaybı olmadan)

**Kapsam:** Build 455 üzerine uygulanan Build 456 topluluk tasarımı ve performans paketi; mevcut giriş, sohbet, hikâye, arama ve medya davranışları korunacak. Bu plan test talimatıdır, testin yapılmış olduğuna dair beyan değildir.

## İndirmeden önce
1. Yalnız **yeşil / success** ile tamamlanmış GitHub Actions Build 456 koşusundaki `Artifacts > NgelX-1.0.231-Build-456-CONSOLIDATED-DEVICE-FIXES` ZIP içindeki APK'yı kullan. Hatalı, sürmekte olan veya iptal edilen koşulardan indirme.
2. APK içindeki Build number **456**, versionName **1.0.231** ve imza doğrulaması CI'da geçmeli.
3. Mevcut uygulamayı **kaldırma** ve cihazdaki uygulama verilerini temizleme. Güncellemeyi mevcut uygulamanın üstüne yükle. Android imza uyuşmazlığı gösterirse yüklemeyi durdur ve hata ekranını paylaş.
4. İki ayrı deneme hesabı kullan, telefon rehberi veya gerçek kişilerin bilgilerini test notlarına yazma.

## 1. İlk açılış ve performans
- [ ] Önceki hesapla oturum açılıyor; farklı hesaba geçiliyor; beyaz/sonsuz yükleme olmuyor.
- [ ] Akışta yeni gönderiler ve tarihleri sıralı; mevcut görseller yükleniyor.
- [ ] Akışı ve toplulukları 2–3 dakika aşağı-yukarı kaydır; uygulamanın donduğu ekranı/süreyi not al.
- [ ] Aynı topluluğun gönderi/yorum sekmelerinde aç-kapat ve geri navigasyon; her geçişte boş liste veya gereksiz sürekli yükleme olmamalı.
- [ ] Başka uygulamaya geçip NgelX'e geri dön; beklenmedik yeniden giriş veya uygulama kapanması olmamalı.
- [ ] Gözle görülen hızlanma ile ölçülmüş hızlanmayı karıştırma. Gerekirse Android geliştirici seçeneklerinde kare oluşturma / GPU profilini veya Flutter profile build metriklerini karşılaştır. Fiziksel cihaz ölçümü yapılmadan yüzde performans iddiası yazma.

## 2. Topluluk ve yönetim
- [ ] Kapak fotoğrafı, başlıklar ve beyaz–mor topluluk görünümü küçük ekranda kesilmiyor.
- [ ] Yalnız kurucu/yönetici kapak düzenleme düğmesini görüyor; fotoğraf değiştirme ve yukarı-aşağı kadraj kaydı geri açıldığında kalıcı.
- [ ] Üç nokta seçenekleri eylemi doğrulamadan işlem yapmıyor.
- [ ] Üye profilleri, roller ve üyeler araması; erişim hatasında **Yeniden dene** seçeneği.
- [ ] Kurucu ve yönetici/moderatör sınırları, gerçek sunucu yetkileri etkin olduğu durumda iki hesapla sınanmalı. Sunucu kuralları henüz dağıtılmamışsa **engelli** olarak not et, çalışıyor varsayma.

## 3. Davet, sohbet, kaydet
- [ ] **Davet et** mevcut 1:1 özel sohbeti listeliyor; kişi doğru; başkasının sohbeti görünmüyor.
- [ ] Davet kartına dokununca onay/katılma ekranı açılıyor. Bozuk davet kodu uygulamayı kapatmıyor.
- [ ] Alıcıya mesaj, bildirim ve katılma sonucu çift hesapla doğrulanıyor; mesaj izinleri ve engelleme korunuyor.
- [ ] Topluluk gönderisini kaydet > profilin kaydedilenler bölümünde doğru içeriği aç.
- [ ] Kaydet ekranı çevrimdışıyken hata/yeniden dene gösteriyor, sonsuz yükleme olmuyor.
- [ ] Topluluk üç nokta menüsü internet yokken çökmeden hata gösteriyor.
- [ ] Fotoğraf, video ve yorum paylaşımı başarısız olursa teknik sunucu adresi yerine anlaşılır açıklama gösteriyor.

## Bilinçli olarak canlıda doğrulanmamış özellikler
- Sunucuda planlanmış gönderi yayımlama, topluluk abonelik bildirimleri, sunucu sayaçları ve yeni Firestore moderasyon izinleri **Cloud Functions ve üretim kuralları dağıtılmadan çalışıyor kabul edilemez**.
- Kullanıcının bütçe kısıtı nedeniyle Cloud Functions ve üretim Firestore kurallarının otomatik dağıtımı kapalıdır. Ücretli servis izni istemeden açılmaz.
- APK CI derlemesinin başarılı olması fiziksel cihazdaki akıcılık, iki hesap bildirimi veya sunucu yetkisinin onaylandığı anlamına gelmez.

## Hata kaydı formatı
`Ekran > dokunulan işlem > beklenen sonuç > gerçek sonuç > kaçıncı denemede oldu > Build 456 > ekran görüntüsü/video`.
Özellikle sohbet kimlikleri, kullanıcı adı/e-posta ve kişisel veri görüntülerini paylaşmadan önce gizle.

## Teslim kapıları
- [ ] GitHub Actions tam başarı + APK artifact.
- [ ] En az bir Android cihazda görüntü ve akıcılık.
- [ ] İki hesapla izinli davet, chat, etkileşim akışları.
- [ ] Eski kullanıcı verisi kaybı yok; mevcut imzayla yükseltme.
- [ ] Sunucuya bağlı özellikler ayrı etkinleşme onayına kadar bekliyor.
