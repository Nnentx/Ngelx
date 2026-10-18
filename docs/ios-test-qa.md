# NgelX iPhone test sürümü — iOS QA (öncelikli)

İlgili görev: #145. Bu çalışma **yalnızca gerçek iPhone testi** içindir; App Store'da herkese açık yayın, mevcut Android Build484 dağıtımı veya production Firebase/LiveKit ortamının değiştirilmesi kapsam dışındadır.

## 19 Ekim 2026 itibarıyla doğrulanan durum

- Flutter projesi `app/` içindedir; Android uygulaması mevcuttur.
- Hem `main` hem Build514 QA kaynak ağacında `app/ios/` dizini bulunmadı.
- Bu daldaki macOS iş akışı iOS platformunu **geçici çalışma alanında** üretir. Gerçek iPhone'a yüklenebilecek imzalı IPA üretmez.
- Build514 (#143) taslak QA PR'ıdır; özelliklerini Android'de hazır/kanıtlanmış veya iOS'ta çalışır saymayın. Aşağıdaki simülatör iş akışı Build514'ün tüm geçmiş Android kaynak-dönüştürme adımlarını yeniden çalıştırmaz; bu nedenle çıkan simülatör derlemesi ayrıca Build514 ile fonksiyonel eşitlik kanıtı değildir.

## İlk hazırlık / simülatör kontrolü

macOS, Xcode ve CocoaPods gerektirir. Ayrı iOS QA dalında:

```bash
cd app
flutter pub get
flutter create --platforms=ios --org com.nnentx --project-name ngelx_app .
cd ..
python3 tools/prepare_ios_qa.py --apply
python3 tools/prepare_ios_qa.py --check
cd app
flutter analyze --no-fatal-infos
flutter build ios --simulator --debug --no-codesign
```

`prepare_ios_qa.py`, oluşturulan iOS Runner'da kamera, mikrofon, fotoğraf seçme/kaydetme ve Bluetooth izin açıklamalarını ve `permission_handler` CocoaPods makrolarını ayarlar; URL şeması `ngelx://` için giriş ekler ve **geçici** minimum iOS sürümünü 15.0 yapar. Bu izin açıklamaları mağazaya çıkmadan önce dil/uygunluk açısından gözden geçirilmelidir. Gerçek arka plan ses, VoIP veya bildirim yetenekleri bu betikle *açılmaz*.

CI: `.github/workflows/NgelX-IOS-SIMULATOR-PREFLIGHT-QA.yml` — test amaçlı macOS, **NO SIGNING / NO IPA / NO DEPLOY**. Başarısızlık ilk teknik engeli raporlar; yeşil sonuç fiziksel cihaz kabulü değildir.

## Gerçek iPhone için engeller

1. **Apple Developer hesabı / uygun Apple Team**, benzersiz ve kullanıcıya ait iOS Bundle ID, sertifika, provisioning profile ve App Store Connect yetkileri doğrulanmalı. Hesap erişimi veya imza anahtarları issue'ya ya da git deposuna eklenmemeli.
2. **Firebase iOS uygulaması** resmi projeye kaydedilmeli; gerçek iOS GoogleService-Info.plist veya uygun per-platform FlutterFire konfigürasyonu eklenmeli; Android ayarı iOS yerine kullanılmamalı. Test ile prod verilerinin ayrımı kararlaştırılmalı.
3. **Bildirimler ve çağrılar** için APNs, gerekiyorsa FCM, izin isteme, gelen arama ve desteklenen iOS CallKit/PushKit akışları ayrıca geliştirilmeli/test edilmeli.
4. **LiveKit WebRTC** için iOS kamera/mikrofon oturumu, ses yönlendirme, uygulama arka planı, yeniden bağlanma, canlı yayıncı/izleyici ve 2+ katılımcılı görüşmeler test edilmeli.
5. **Android overlay ≠ iOS overlay.** iPhone, başka uygulamaların üstüne Messenger tipi keyfî bir pencere çizimine izin vermez. Uygulama içi küçültülmüş çağrı penceresi ile desteklenen iOS video PiP/CallKit seçenekleri ayrı tasarlanmalı.
6. Yayın/hediye/yorum/kamera/arama başlıklarının latest QA kaynağıyla işlevsel eşitliği ve iki fiziksel iPhone testi gereklidir.

## Fiziksel cihaz kabulü — yapılmadan 'hazır' demeyin

- [ ] İmzalı IPA / TestFlight test dağıtımında iPhone 1 ve iPhone 2 kurulum.
- [ ] Kayıt-giriş, sohbet; özel ve grup arama, cevaplama-reddetme-zil; kamera aç/kapat.
- [ ] Yayıncı / izleyici / konuk ekleme / gerçek zamanlı yorumları kaydırma.
- [ ] Hediyenin adı, adedi, göndereni, toplam sayısı ve büyük animasyonu.
- [ ] Mikrofon/kamera izin reddi/geri açma, iOS bildirimleri, ön/arka plan.
- [ ] Ağ değişimi, kopma ve yeniden bağlanma; cihaz logları ve kabul videosu.
- [ ] Kullanıcı onayı olmadan ana dala merge, production servis değişimi veya App Store yayını **yapma**.

İlk canlı test için önceki 10–20 gün yalnızca koşullu bir tahmindi; repo bağımlılıkları, macOS build sonucu, Apple hesabı ve fiziksel cihaz erişimi netleşince yeniden değerlendirilmelidir.
