# NgelX Build 575 — Güvenli yayın ve geri dönüş kılavuzu

**Durum:** İnceleme amaçlıdır. Bu dosyanın hazırlanması, NgelX Build 575'in yayımlandığı anlamına gelmez.

## 1. Dağıtıma geçmeden önce
- En son Build575 kod revizyonunda hem `NgelX-BUILD575-LUDO.yml` hem `NgelX-BUILD575-WORKER-DRYRUN.yml` iş akışlarının **success** olduğundan emin olun. Geçmiş revizyonların başarılı işlerini yeterli saymayın.
- `NgelX-Build575-Review-APK` dosyası sadece GitHub Actions artefaktıdır; `Nnentx/ngelx-web` yayımlama klasörüne otomatik olarak taşınmaz.
- Android APK sertifika SHA-256 değeri CI'daki mevcut Build574 fingerprint denetimiyle **aynı** olmalı. Cihazda güncellemeyi ayrıca test edin.
- Kabul sonuçlarını `QA/BUILD575-DEVICE-ACCEPTANCE.md` içinde iki ayrı Android cihazla kaydedin. 2 kişi/4 kişi/2v2, Auto, manuel mod, rövanş, hediyeler, günlük ödül, bot, kopan bağlantı ve izleyici sonuç animasyonu zorunludur.
- Canlı Cloudflare, Firebase veya reklam sağlayıcı konfigürasyonunu test dışı ortama taşımayın. Hesap bilgilerinin kendisi kodda, ekran görüntülerinde, issue veya sohbetlerde saklanmamalıdır.

## 2. Cloudflare Ludo API doğrulaması (reklamsız)
- Önce mevcut Worker'a ait doğrulanmış proje/hesap ve deploy yetkilerini ayrı kontrol edin. `wrangler deploy --dry-run` **sadece paketlemeyi** kontrol eder; canlıya yükleme değildir.
- Başarılı ve geri dönüşü hazırlanmış canlı Worker dağıtımından sonra `GET /health` yanıtında `ludo575.sourceVersion == 575` ve `ludo575.configured == true` koşullarını sağlayın. Bu kontroller sunucu kodunun ve temel Firebase projesinin beklenen sürüm olduğunu gösterir; tek başlarına oyun akışının çalıştığını kanıtlamaz.
- Yeni `GET /health` yanıtı yalnızca boolean yapılandırma bayrakları içerir; kimlik bilgileri ve moderatör UID listesi dönmez. `rewardedAdsConfigured` ve `moderationAllowlistConfigured` özelliklerinin `false` olması, ilgili fonksiyonun çalıştığı anlamına **gelmez**.
- Firebase JWT sahibi iki ayrı test hesabıyla `/ludo` API'sinde oluştur/katıl/senkronizasyonu, 10 saniyelik Auto turunu ve kesintiden geri dönüşü kontrol edin.
- Firestore üzerinden cüzdan ve hediye işlemlerini gerçek test hesabında idempotent olarak doğrulayın; işlem onaylanmadan uygulama para/çip miktarı değiştirmesin. Rapor listesi normal oyuncu için **403** dönmeli.

## 3. Opsiyonel AdMob / şikâyet moderasyonu
- Gerçek AdMob App ID ve Rewarded Ad Unit ID ilgili yayıncı hesabından doğrulanıp mobil SDK ve Worker üzerinden **eşleşen** biçimde tanımlanmalıdır. Resmî Google *demo* reklam kimlikleri yalnızca bağımsız CI smoke testinde kullanılmalı; üretim APK'sına girmemelidir.
- Google AdMob SSV callback URL'sini tam olarak Worker `/ludo/admob/ssv` yoluna bağlayın; gerçek imzalı test callback geldiğini ve token'ın sadece bir kez 30 sanal çip kazandırdığını kontrol edin. Yerel `onUserEarnedReward` çağrısı para kazanmak için **yeterli değildir**.
- Gizlilik/onay mekanizması, kullanım şartları ve sağlayıcı kuralları tamamlanmadan ödüllü video düğmesi açılmamalıdır. Ads ayarları olmayan varsayılan APK reklamsız kalır.
- `LUDO_MODERATOR_UIDS` ortam değeri yalnızca gerçek ve yetki verilen Firebase UID'lerini içermelidir. Boşsa moderasyon API'si kimseye açılmaz.
- Şikâyet incelemesi için `tools/ludo575_moderator_cli.mjs` kullanılabilir; moderatörün kısa ömürlü Firebase ID token'ı ve doğrulanmış HTTPS Worker endpoint'i **sadece gizli ortam değişkenlerinden** verilmelidir. Token değerlerini CI/log/git/ekran görüntüsü/iletilere yazmayın. Her sonuçlandırma kararını operatör ayrı doğrulasın.

## 4. Yayın kararı
- Yukarıdaki kontroller gerçek cihazda bitip QA kontrol listesinde kaydedilmeden `Nnentx/ngelx-web/android-update.json` dosyasına dokunmayın.
- Yayın öncesinde mevcut Build574 APK, web manifest ve çalışan Worker yapılandırmasının güvenli geri dönüş yolu hazır olmalı. Build575 dosyası yalnızca doğru sertifikayla imzalanmış, sürümü `1.0.345+575` ve gerçek telefon testi geçmişse yayımlanabilir.
- Sorun görülürse kullanıcıların yeni kurulum yapmasını tetiklemeyin. Sağlıklı Build574 güncelleme manifestini koruyun/geri döndürün; Worker için geri dönüşü doğrulanmış önceki dağıtımı kullanın. **Eski uygulama ile yeni Worker protokolünün uyumu**, geri dönüş sırasında ayrıca kontrol edilmelidir.

## Son teyit edilmesi gerekenler
- [ ] Son Android CI başarı, son Worker dry-run başarı, artefakt SHA/fingerprint kontrolü
- [ ] İki fiziksel Android cihazla bütün kritik Ludo senaryoları
- [ ] Gerçek canlı Worker'da `/health`, `/ludo`, Firebase ve Firestore testi
- [ ] Moderasyon UID'leri ve gerçek inceleme sorumlusu
- [ ] AdMob gerçek hesap kurulumu veya özellik **kapalı** yayın kararı
- [ ] Güncelle manifesti, APK imzası ve geri dönüş prosedürü onayı

**Canlı sürüm:** `NgelX 1.0.344 / Build 574`, `Nnentx/ngelx-web/android-update.json`. Build575 PR #190 taslak olarak kalır.
