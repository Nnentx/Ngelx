# NgelX canlı yayın dağıtımı

Hedef Firebase projesi: `ngelx-44eed` (Android google-services.json ile doğrulandı).
Bu belge uygulanacak adımları tarif eder; dağıtım yapıldığı anlamına gelmez.

## Yapılandırma

LiveKit Cloud projesinin Project URL değerini kullanın (örnek biçim: `wss://PROJE.livekit.cloud`).
Uygulamadaki DevelopmentTokenSource test kimliği bu adresin veya API anahtarlarının yerine geçmez.
LiveKit API key/secret aynı LiveKit projesine ait olmalıdır.

`functions/.env.ngelx-44eed` yerel dosyasına yalnızca public adresi yazın:

```dotenv
LIVEKIT_URL=wss://GERCEK-PROJE.livekit.cloud
```

Dosya git tarafından yok sayılır. API anahtarları Firebase Secret Manager'a interaktif olarak girilir:

```bash
firebase functions:secrets:set LIVEKIT_API_KEY --project ngelx-44eed
firebase functions:secrets:set LIVEKIT_API_SECRET --project ngelx-44eed
```

Firebase CLI oturumu bu projede Functions, Firestore ve ilgili secret/IAM işlemlerini yapabilmelidir.
Eski Firebase servis hesabının var olması bu yetkilerin mevcut olduğunu kanıtlamaz.

## Dağıtım

Repository kökünden testleri çalıştırın:

```bash
npm ci --prefix functions
npm test --prefix functions
npm run check --prefix functions
python tools/verify_ngelx_contract.py
```

Kod ve kurallar incelendikten, LiveKit yapılandırması hazırlandıktan sonra:

```bash
firebase deploy --project ngelx-44eed --only functions:ngelxLive,functions:ngelxLiveWebhook,functions:ngelxFinishExpiredPK,firestore:rules
```

Kurallar canlı yayın belgesi oluşturma/değiştirmeyi istemciden kaldırır. Eski APK'ların test-token ile yayın başlatma yolu bu kurallarla çalışmaz; istemci geçişi dağıtımla birlikte planlanmalıdır.
Başka Functions veya Hosting bileşenlerini bu komuta eklemeyin.

CLI çıktısından **gerçek dağıtılan** ngelxLive ve ngelxLiveWebhook HTTPS adreslerini alın.
Adres tahmini yaparak APK veya webhook yapılandırmayın.
LiveKit projesinde webhook hedefini ngelxLiveWebhook adresi olarak ayarlayın; imza doğrulama anahtarı aynı proje API anahtarı olmalıdır.
Webhook event akışının participant_joined, participant_left ve room_finished olaylarını ulaştırdığını kontrol edin.

## APK bağlantısı

GitHub repository variable `NGELX_LIVE_API_URL` değerini dağıtılan ngelxLive HTTPS adresine ayarlayın.
Bu public adres bir secret değildir. LiveKit API key/secret APK'ya eklenmez.
Yayıncı ve izleyici yeni kodu kullanmalıdır. Mevcut Build 347 workflow eski sürüm numarası taşır;
kurulum paketinde telefondaki APK'dan daha yüksek build numarası ve mevcut imza kullanılmalıdır.
Test amaçlı geçici anahtarla oluşturulan CI APK'sını güncelleme paketi olarak dağıtmayın.

## İki cihaz doğrulaması

1. Yayıncı açılır; ikinci hesap görüntü ve sesi alır.
2. İzleyici onaydan önce kamera yayınlayamaz; katılım isteği/davet kabulünden sonra konuk olur.
3. Konuk mikrofon/kamera aç-kapatır; görüntü yerleri sabit kalır.
4. PK 1/3/5 dakika seçeneklerinde başlar, süre bitiminde sonuçlanır.
5. Yetersiz jeton işlemi reddedilir. Başarılı hediye ve aynı işlem kimliği tekrarının tek ücret oluşturması ayrı test ortamında doğrulanır; üretim bakiyesine test jetonu eklenmez.
6. Konuk ayrılınca yayıncı yayında kalır; yayıncı ayrılınca oda kapanır.
7. Bağlantı kopması/yeniden bağlanma, arka plan ve eski tokenla katılma gerçek LiveKit üzerinde test edilir.
8. Sunucu scheduler'ının ekranlar kapalıyken PK sonuçlandırdığı ve webhook retry'larının sonucu bozmadığı kontrol edilir.

Referans: https://docs.livekit.io/reference/developer-tools/livekit-cli/ (Project URL bilgisi).
