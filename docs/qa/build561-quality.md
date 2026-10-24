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

Canlı e-posta hizmeti dağıtımı, mağaza yayını ve ana dala birleştirme yapılmadı. Gerçek cihaz kabulü beklenir.

## Tamamlanan doğrulama ve APK

GitHub derlemesi başarıyla tamamlandı: https://github.com/Nnentx/Ngelx/actions/runs/40096703443 . Derlenen kaynak commit'i `605cb8acec0a0938b094b1b25c887c057ef4b4fc`; bu rapor güncellemesi uygulama kodunu değiştirmez.

- 23 Flutter arayüz testi ve 111 sunucu testi geçti. Tam uygulama analizinde sıfır hata; mevcut bilgi/uyarı borcu korunuyor.
- Soğuk yama, tekrar uygulama, kaynak sapması ve izin/yazma verisi koruma kontrolleri geçti. Build560 tabanındaki 56 diğer Dart dosyası değişmedi.
- İndirilen kaynak arşivindeki 58 Dart dosyası yerelde test edilen son kaynaklarla birebir eşleşiyor. `main.dart` özet değeri ve yeni yardımcı dosya, yayımlanan yama/manifest ile eşleşiyor.
- GitHub artifact SHA256 değerleri ve ZIP bütünlüğü doğrulandı. APK SHA256, derleme çıktısındaki `.sha256` kaydıyla eşleşiyor.
- Paket `com.nnentx.ngelx_app`, sürüm `1.0.331`, yapı `561`; ARM64 uygulama ve Flutter çalışma zamanı dosyaları mevcut.
- `apksigner` doğrulaması geçti; sertifika önceki güncelleme imzası `be20b27f0ba1f4decd2941d410b1536de89e48dc894f04f038f9d26b11ecd6aa` ile aynı.
- APK boyutu: 47.507.815 bayt. SHA256: `3b26fe276b53ecb0f0bf63cd62998c33a35122bd98aa08c71fdf400b7f6cac92`.
- Özel e-posta endpoint'i derleme kaydında boş: `NGELX_VERIFICATION_EMAIL_URL=""`. Bu nedenle bu APK'da mevcut native Firebase e-posta gönderimi aktif kalır; onaylanan özel HTML şablonu henüz canlı gönderimde kullanılmaz. Şablon/servis kodu ve testleri hazırdır; gönderen alan adı/anahtarı ve gerçek servis adresi etkinleştirilmelidir.
- Gerçek telefonda performans ölçümü veya Gmail/Outlook canlı e-posta görünümü kabul testi yapılmadı. HTML görüntüsü için yerel tarayıcı kurulumu tamamlanamadı; e-posta kod ve servis testleri geçti.
