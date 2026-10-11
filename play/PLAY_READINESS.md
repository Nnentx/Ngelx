# NgelX — Play Store hazırlığı, Build441

Durum: İnceleme ve kapalı test hazırlığı. Üretime hazır sürüm beyanı değildir.

## Paket ve dağıtım

- Uygulama kimliği: `com.nnentx.ngelx_app`; sürüm 1.0.216, versionCode 441.
- Android minSdk 26, compileSdk/targetSdk 36. Kamera ve otomatik odak donanımı zorunlu değildir; izinler ihtiyaç anında istenir.
- Test APK'sı mevcut test anahtarını korur. Play için ayrı upload anahtarıyla imzalanmış AAB gerekir. Test/debug imzalı AAB mağazaya yüklenmemeli.
- Play App Signing sertifikasının SHA-1/SHA-256 değerleri Console'dan alındıktan sonra Firebase/Google giriş ve Android App Links yapılandırmasına eklenmelidir. Upload sertifikası bunun yerine geçmez.
- ELF 16 KB hizalama kontrolü CI'da çalışır; Android 16 KB cihaz/emülatör ve bundle paketleme kontrolleri ayrıca yapılmalıdır.
- Yeni kişisel geliştirici hesabı: en az 12 kişinin kapalı teste aralıksız 14 gün katılımı, ardından üretim erişimi başvurusu. Tek geliştiricinin testi bu gerekliliği karşılamaz.

## Console'a girilecek taslak bilgiler

| Alan | Hazırlanan değer / işlem |
|---|---|
| Ad | NgelX |
| Kategori | Sosyal |
| Destek | ngelx.support@gmail.com — posta kutusunun sahipliği ve takibi doğrulanmalı |
| Web sitesi | https://ngelxsocial.com |
| Gizlilik | https://ngelxsocial.com/privacy.html — gerçek veri akışı ve saklama politikasıyla eşleşmeli |
| Hesap silme | https://ngelxsocial.com/delete-account.html — dışarıdan talep erişimi ve sunucu temizliği uçtan uca doğrulanmalı |
| Çocuk güvenliği | child-safety.html hazır; web deposuna yazma yetkisi olmadığı için henüz yayımlanmadı |
| Mağaza metinleri | metadata/listings.json: 12 dil taslağı; Kürtçe için Console'un desteklediği yerel ayar ayrıca kontrol edilmeli |
| Uygulama erişimi | İnceleme için geliştiriciye ait demo hesap ve erişim talimatı gerekli; gerçek kullanıcı parolaları kullanılmamalı |
| Ekran görüntüleri | Temiz demo verileriyle gerçek uygulamadan çekilmeli; kişisel test videolarındaki kullanıcılar mağaza görseli olarak kullanılmadı |
| İçerik derecelendirmesi | Kullanıcı içeriği, mesajlaşma, canlı özellikler ve moderasyon durumuyla tutarlı yanıtlar gerekli; derecelendirme uydurulmadı |
| Hedef kitle | Gerçek yaş kabul politikasıyla seçilmeli; yaş grubu geliştirici adına varsayılmadı |
| Reklamlar | SDK ve yayın yapılandırması son kez kontrol edilmeden “reklam yok” beyanı kesinleştirilmemeli |
| Dijital ürünler | Premium/jeton satın alma etkin değil. Etkinleştirilirse Play Billing, sunucu makbuz doğrulama ve iade/iptal eşitlemesi gerekli |

## Veri Güvenliği çalışma tablosu

Bu bir kod envanteridir; tamamlanmış Console beyanı değildir. SDK'ların gerçek üretim yapılandırması, kullanım amaçları, veri aktarımı ve silme davranışı doğrulanmalı.

| Veri / özellik | Kodda görülen kullanım | Beyan ve doğrulama |
|---|---|---|
| Ad, kullanıcı adı, e-posta, kullanıcı kimliği | Firebase Auth / kullanıcı profili | Hesap işlevi; depolama, silme ve görünürlüğü doğrula |
| Telefon, doğum tarihi, profil biyografisi | Profil alanları | Gerçekte toplanan zorunlu/isteğe bağlı alanları açıkla |
| Fotoğraf ve video | Paylaşım, hikâye, profil, medya servisi | Kullanıcının yayınlama tercihi, sunucu saklama ve silme |
| Ses | Sesli mesaj, görüşme, sesli oda | Aktarım ve varsa kayıt/saklama; kayıt yok beyanını doğrulamadan yapma |
| Mesaj, yorum, tepki, sosyal ilişkiler | Firestore | Uygulama işlevi ve güvenlik; katılımcı erişimi ve saklama |
| Rapor ve destek içerikleri | reports / support_requests | Güvenlik/moderasyon; erişim ve yasal saklama |
| Çeviriye gönderilen metin | Firebase doğrulamalı medya API'si ve AI çeviri | Hizmet sağlayıcı işlemesi ve isteğe bağlı kullanım |
| Cihaz / bildirim belirteçleri | Bildirim ve cihaz oturumu | Gerçek kullanılan tanımlayıcılar ve amaç |
| Konum | Kullanıcının konum paylaşım akışı | İzin/arka plan toplama ayrımı, gerçek gönderilen veri |
| Tanılama / üçüncü taraf SDK | Flutter/Firebase/LiveKit bağımlılıkları | Analytics/Crashlytics ve diğer SDK ayarlarını ayrı denetle |

“Hiç veri toplanmıyor” bu uygulamanın mevcut işlevleriyle tutarlı değildir. Aktarım şifrelemesi, üçüncü tarafa paylaşım istisnaları ve silme talepleri gerçek sunucu davranışına göre işaretlenmeli.

## Değişiklikler ve açık işler

- Arşiv: erişilemeyen eski kimlikler kişinin kendi arşiv kaydı olarak gösterilir; kaldırma yalnızca kendi kullanıcı tercihi ve arşiv kaydını değiştirir. Ağ hatalarında yeniden deneme korunur.
- Öne çıkan: ownerId + highlighted sorgusu yeni hikâyeyi eski 100 normal hikâyenin sınırından kurtarır. Başarı mesajı sunucu teyidinden sonra gösterilir.
- Diller: 119 yeni satırın tümü 12 dilde. Ayar gösterim yardımcıları çeviriye bağlandı. CI çıktısındaki `build441-untranslated.tsv` hâlâ kapsamlı kalan metinler içerir; tüm ekranlar bitmiş değildir.
- Kullanıcı adı: eski ayar ekranındaki 30 karakter sınırı da 3–20 karaktere indirildi.
- Çocuk güvenliği: uygulama rapor menüsünde kategori eklendi. Sunucu moderasyon kuyruğunu izleyen kişi, kaldırma ve bölgesel bildirim operasyonu ayrıca kurulmalı/doğrulanmalı.
- Görüşmeler: Play build test token sunucusuna dönemez. Sunucu token çekirdeği 11 testle doğrulandı; gerçek Firebase Admin/oda yetkilendirme/rate limiter adaptörleri ve HTTPS dağıtımı henüz kurulmadı.
- Kullanıcı adı ve doğrulanmış telefonla giriş bağlantısı tamamlanmadı. Çalıştığı doğrulanan e-posta oturumu korunur.
- Bildirim sesinin sessizlik kaldırılınca gerçek cihazda dönmesi ve iki cihazlı ses/video görüşmesi açık doğrulamalardır.
- Yeni hikâyenin 24 saat sınırı otomatik testte kontrol edildi; gerçek süre testi tamamlanmış olarak işaretlenmedi. Süresi biten hikâye aktif bölümden çıkar; arşiv/öne çıkanların ayrı saklama işlevi korunur.
- Hesap silme zamanlanmış temizliğinin gerçek üretim ortamında çalışması doğrulanmadan Play veri silme uygunluğu tamamlandı sayılmaz.

## Kapalı test akışı

1. Console kimlik, telefon/e-posta ve Android cihaz doğrulamasını tamamla.
2. Eksik çevirileri, üretim görüşme uç noktasını, politika bağlantılarını ve moderasyon işlemlerini kapat.
3. Gerçek demo hesapla temiz ekran görüntüleri üret; erişim talimatı ve veri beyanlarını tamamla.
4. İmzalı ve doğrulanmış AAB'yi önce dahili teste al; Play'den kurulum, güncelleme, giriş/çıkış ve silme akışını doğrula.
5. En az 12 kişinin kapalı teste aralıksız 14 gün katılmasını sağla. Geri bildirimleri ve düzeltmeleri gerçek test kanıtlarıyla kaydet.
6. Üretim erişimine başvur; sonuç olmadan herkese açık yayın gerçekleşmiş sayılmaz.

## Resmî kaynaklar

- Hedef API: https://support.google.com/googleplay/android-developer/answer/11926878
- Kişisel hesap testi: https://support.google.com/googleplay/android-developer/answer/14151465
- Çocuk güvenliği: https://support.google.com/googleplay/android-developer/answer/14747720
- Hesap silme: https://support.google.com/googleplay/android-developer/answer/13327111
- Play App Signing: https://support.google.com/googleplay/android-developer/answer/9842756
- 16 KB sayfa boyutu: https://developer.android.com/guide/practices/page-sizes
- LiveKit token endpoint: https://docs.livekit.io/frontends/build/authentication/endpoint/
