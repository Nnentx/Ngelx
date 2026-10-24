# NgelX Build561 — Build560 yapısı korunarak takip düzeltmeleri

Taban: Build560 / PR #182, `1db8f671e604605c0963a7e0c4db30fc4d8a8bd2`. Aday sürüm: `1.0.331 (561)`. Ana dal ve canlı veritabanı kuralları değiştirilmez.

## Değişiklikler

- **Profil → Gönderiler → Yorumlar:** Profilin tam ekran gönderi görüntüleyicisi, yorum klavyesi animasyonu sırasında arka plandaki medyayı yeniden boyutlandırmaz. Klavye inset bağımlılığı ve medya çizim katmanı ayrılır. Yorum Firestore akışı ekran ömrü boyunca tek örnektir; sıralama/yanıt/izin verisi yeniden çizimlerinde yeni abonelik açılmaz. Gönder düğmesi ağdaki izin kontrolünden önce kilitlenir, tüm erken dönüş/hata yollarında serbest bırakılır. Mevcut yorum yetkileri, gizli kelime filtreleri, yazma verileri, yanıtlar, sayaç ve bildirim işleri korunur. Telefonda gecikme ölçümü yapılmadı; kullanıcının gerçek cihaz kabulü beklenir.
- **Topluluk bildirimleri:** Görseldeki Gelen Kutusu, ayrı Bildirimler sayfasından farklı bir metin oluşturucu kullanıyordu. Asıl Gelen Kutusu da ortak topluluk bileşenine bağlandı. Gerçek topluluk adı mor, kalın ve Türkçe büyük harfle gösterilir. Boş `targetTitle` alanı gerçek `communityName` değerini engellemez; eski kayıtların topluluk kimliğiyle adı okunur. İsim bulunamazsa uydurma bir isim yazılmaz. Grup bildirimleri ve bildirim tıklama davranışı korunur.
- **Doğrulama e-postası:** Onaylanan tasarım yönünde HTML şablonu, zarf/kalkan görseli ve gerçek “E-postamı Doğrula” bağlantısı hazırlandı. Mevcut kayıt ve yeniden gönderme noktaları tek yardımcıya bağlandı. Özel gönderim hizmeti yapılandırılmadıysa mevcut Firebase gönderimi sürer; bu durumda yeni görsel e-postanın canlı olduğu iddia edilmez. Servis etkinleştirme ayrıntıları `server/verification561/README.md` içinde.
- **Gelen Kutusu:** Build560 başlığı/arama açma-kapatma, sekmeler, sayaçlar, kompakt profil şeridi ve alt gezinme korunur. Bu sürümde yalnızca topluluk bildirimi metin sunumu değişir.

## Kaynak ve kontroller

Mevcut tarihsel üretim zinciri korunur. Sonunda `tools/apply_build561_quality.py` yalnızca tam Build560 özetine uyan `main.dart` dosyasına yama uygular ve yeni `build561_quality.dart` bölümünü ekler. Kaynak sapması/yarım uygulama reddedilir; tekrar uygulama aynı sonucu verir. Diğer uygulama Dart dosyaları ve Firestore kuralları Build560 ile birebir korunur.

Yerel kontroller:

- 7 yeni arayüz/davranış testi: 280/393/600 piksel ve büyük metinde topluluk adı, Türkçe büyük harfler ve eski kayıtlar; klavye boyunca medyanın boyut/yeniden çizim sayısı; yazarken yorum listesinin yeniden kurulmaması; gönderim bekleme durumu.
- Önceki Build558/Build560 arayüz regresyonlarıyla birlikte 23 test.
- 7 e-posta şablonu/servis testi.
- Soğuk yama, tekrar uygulama, kaynak sapması ve mevcut izin/yazma/veri akışı koruma kontrolü.
- Flutter analizinde sıfır hata hedeflenir; önceki uyarı/bilgi borcu bu değişiklikte topluca temizlenmez.

APK derlemesi ve imza/gerçek cihaz kabul durumu tamamlandıkça bu rapora eklenir. Canlı e-posta gönderimi, yeni gönderim hizmeti dağıtımı, mağaza yayını veya ana dala birleştirme bu aday çalışmanın tamamlanmış parçası olarak sunulmaz.

## Tamamlanan yerel doğrulama

- Son 23 Flutter arayüz testi geçti; Flutter analizinde 0 hata var. Mevcut uyarı/bilgi kayıtları korunuyor.
- 7 e-posta testi ve soğuk/tekrar/sapma/kapsam testi geçti.
- Build560 ile karşılaştırmada mevcut 56 diğer Dart dosyası birebir aynı. Yalnızca `main.dart` değişti ve `build561_quality.dart` eklendi.
- Otomatik onay incelemesi, açık kullanıcı onayı bulunmadığı gerekçesiyle GitHub'a kod/iş akışı gönderimini engelledi. Değişiklikler yerel `fix/build561-comments-community-email` dalında tutuluyor. GitHub derlemesi başlatılmadı; Build561 APK henüz üretilmedi. Bu nedenle telefondaki sürümün değiştiği veya sorunların gerçek cihazda giderildiği iddia edilmez.
- E-posta şablonu kod ve servis testleriyle kontrol edildi. Bu ortamda HTML ekran görüntüsü için tarayıcı kurulumu tamamlanamadı; gerçek posta istemcisi görünümü ve canlı gönderim kabulü beklenir.
