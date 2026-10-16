# NgelX Build465 — 15 Maddelik Telefon Test Planı

Bu liste **1.0.240 / Build465** QA APK'sı içindir. GitHub Actions testleri, gerçek telefonda UI/doğruluk garantisi değildir. Testleri iki gönüllü test hesabı/telefon ve bir test grubuyla yürütün. **Üretim Firebase kuralları veya kullanıcı verilerine müdahale etmeyin.** Önceki çalışan uygulamayı silmek yerine imza doğrulaması yapılan QA APK'sını aynı pakete normal güncelleme yöntemiyle kurun.

İlk doğrulanan ve imzalanan Messenger düzenleme APK'sı: https://github.com/Nnentx/Ngelx/actions/runs/38903249213

**Arama durum/küçültme devam yaması**: `qa/ngelx-build465-call-ui-finish-20261016`. Bu dalın kendi tam QA koşusu ve imzalı artifact'i oluşmadan arama durumu yeniliğinin telefona ulaştığı söylenmemelidir.

| # | Senaryo | Kabul kriteri |
|---|---|---|
| 1 | Üç kişilik grup sesli araması aç; farklı oranlarda profil fotoğrafları seç | Her fotoğraf köşeleri yuvarlatılmış karede, önemli kısımları kırpılmadan gösterilir |
| 2 | Bir katılımcının üç noktasından **Sustur (benim için)**, ardından **Sesi yeniden aç** yap | Ses yalnızca **test eden telefonda** kapanır/açılır; diğer katılımcının gerçek mikrofonu izinsiz etkinleştirilmez |
| 3 | Grupta bir fotoğraf gönderip o fotoğrafa yanıt ver | Orijinal fotoğraf büyük; yanıtta küçük, tanınabilir fotoğraf alıntısı yer alır |
| 4 | Dikey/yatay/çok geniş fotoğraf gönder | Fotoğrafın köşeleri yuvarlatılmış, tam resim orantılı görünür |
| 5 | Grupta ve özel sohbette yazılı mesaja yanıt ver | Alıntı satırı okunaklı, yanıt metni ayrı; tekrarlanan “yanıt verdi” satırı yok |
| 6 | Fotoğrafı tam ekran aç ve Android üç tuş/jest gezinmeyle dene | Alt sistem çubuğuna taşma yok, görüntü oranı korunur |
| 7 | Grup fotoğrafına çift dokunup kalp bırak | Kalp/rozet fotoğrafın kendi sağ-alt köşesinde kalır |
| 8 | Özel sohbet fotoğrafına çift dokunup kalp bırak | Kalp ekranın sağ ucuna kaçmaz, görsele bağlı durur |
| 9 | Grup profil adı, büyük/küçük emoji ve peş peşe medya mesajı gönder | Avatar, ad, emoji ve balon boşlukları tutarlı, içerik kesilmez |
| 10 | Özel sohbette klavye açık/kapalıyken mesaj yaz, kamera ve galeriye gir | Alt çubuk gruptaki gibi hizalı; kamera/galeri erişilebilir; alt sistem boşluğu iki kez eklenmez |
| 11 | İki cihaz arasında uygulama ön/arka plandayken sesli/görüntülü arama başlat | İzin verilmişse bildirim ve zil çalar; başlığa dokununca sohbet açılır, ikinci yanıt paneli yok ve otomatik kabul olmaz |
| 12 | Önce özel, sonra grup sesli/görüntülü çağrı başlat; arama devam ederken küçült ve sohbete dön | Bağlantıdan önce “Aranıyor…”, cevap sonrası süre; minik çağrı durumu korunur; kontrol düğmeleri dar ekranda taşmaz; Kırmızı **Bitir** yalnızca gerçekten basılınca sonlandırır |
| 13 | Farklı dikey/yatay videoları tam ekran aç | Video alt gezinme çubuğuna taşmaz, oranı korunur ve oynatma kontrolü erişilebilir |
| 14 | Önce gruba sonra özel sohbete gir; çok eski mesajdan çıkıp yeniden aç | Açılışta son mesajlar alt giriş alanı üstünde görünür; kullanıcının yukarı kaydırmasını otomatik kaydırma geri almaz |
| 15 | Özel sohbet açarken ağ bağlantısını kısa süre kesip geri aç | “Kişi bilgisi yükleniyor…” sonsuza dek kalmaz, tekrar dener veya elle yeniden yükleme sunar; uygulamayı tamamen kapatmak gerekmez |

## Doğrulama kanıtı
- Her maddeyi **Geçti / Başarısız / Test edilmedi** olarak işaretleyin.
- Sorun devam ederse Android sürümü, gezinme türü (jest / 3 tuş), grup/özel, uygulama ön/arka planı ve ekran görüntüsü/video ile belirtin; gerçek hesap/kişi bilgilerini redakte edin.
- Bildirim izni reddedildiğinde sessiz bildirim davranışı, telefonun **Rahatsız Etmeyin** veya **Sessiz** ayarıyla karıştırılmamalıdır.
- İşlevsel arama testi en az iki gerçek cihazla yapılır. GitHub Actions, cihazdaki gerçek ses/hoparlör davranışını tek başına kanıtlamaz.
- Hiçbir QA sonucu ana dala otomatik birleştirme, Play Store yayını veya canlı Firebase değişikliği yetkisi vermez.
