# Canlı yayın sunucusu (taslak)

Node 22 Firebase Functions: `ngelxLive` ve imzalı `ngelxLiveWebhook`.
Dağıtımdan önce LIVEKIT_URL parametresi ve LIVEKIT_API_KEY / LIVEKIT_API_SECRET secret değerleri ayarlanmalıdır.
Flutter derlemesine `--dart-define=NGELX_LIVE_API_URL=https://.../ngelxLive` eklenmelidir.
LiveKit webhook adresi `ngelxLiveWebhook` fonksiyonuna yönlendirilmelidir.
Firestore rules ve functions birlikte dağıtılmalıdır; canlı yayın belgeleri ve cüzdanlar yalnızca sunucudan yazılır.
İstemcideki eski test token servisi canlı yayın için kullanılmaz. Mevcut eski yayınlara geçiş planı gerekir.
Ödeme/yükleme ve para çekme yoktur. İstemci hiçbir şekilde jeton bakiyesi oluşturamaz.

Doğrulama: `npm ci`, `npm test`, `npm run check`.
Henüz yapılmayanlar: Flutter analyze/build, emulator transaction/rules entegrasyonu, iki gerçek cihazda davet/PK/hediye ve ağ kopması testleri.
Üretim öncesi: eski yayıncı tokenlarının ayrılma sonrası tekrar kullanımına karşı server-side session doğrulaması, misafir yayın yetkisi güncellemesi ile ayrılma yarışının entegrasyon testi, otomatik PK finalizasyonu, host bağlantı kaybı temizliği ve token yenileme tamamlanmalıdır.
Bu değişiklik üretime hazır APK değildir.
