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
Üretim öncesi: eski yayıncı tokenlarının ayrılma sonrası tekrar kullanımına karşı server-side session doğrulaması, misafir yayın yetkisi güncellemesi ile ayrılma yarışının entegrasyon testi, token yenileme ve gerçek LiveKit/Firestore üzerinde oturum-yetki entegrasyon testleri tamamlanmalıdır.
Bu değişiklik üretime hazır APK değildir.

PK kabulünde sunucuya özel `live_pk_deadlines` kaydı aynı transaction içinde oluşturulur. `ngelxFinishExpiredPK` her dakika en fazla 500 vadesi geçmiş kaydı kontrol eder; kayıt kimliği eski PK ile eşleşmiyorsa yeni maça dokunmaz. Sonuç sunucuda gecikmeli görünebilir (normalde yaklaşık bir dakika, yük/hata halinde daha uzun); süre sonrası hediyeler PK puanına dahil edilmez. Açık ekran ayrıca süre bitiminde `pk-finish` çağrısını otomatik yapar.

LiveKit participant_joined/participant_left webhookları katılımcı SID ve milisaniye katılım zamanı ile eşleştirilir; eski bağlantının ayrılması yeni bağlantıyı kapatmaz. Yayıncı ayrılınca Firestore yayını ve medya odası kapanır; konuk ayrılınca PK sonuçlanır, ana yayın sürer. Bu davranışlar imzalı webhookların doğru adrese teslim edilmesini gerektirir. Yeni eklenen 9 lifecycle testi ve 3 oturum sıralama testi dahil `npm test` ile doğrulanır.

Konuk ekranında mikrofon/kamera aç-kapat, katılım başarısızlığında tekrar deneme ve konuk yayından ayrılma kontrolleri bulunur. Yayıncı ve konuk görüntüleri sabit kimlik sırasıyla gösterilir; kamerayı kapatmak görüntü yerlerini değiştirmez. Bağlantı hatasında yerel oda her durumda temizlenmeye çalışılır; başarısız yayın başlatma kaydı sunucudan kapatılır ve kapatılamazsa yeni yayın açmadan önce yeniden denenir. Çoklu hediyelerin olay kaydı toplam jetonu `coins`, tek hediye fiyatını `unitCoins` alanında tutar.

PR doğrulama akışı: `.github/workflows/ngelx-live-draft-checks.yml` Node testlerini, Flutter 3.47.2 paket çözümlemesini, analizi, endpoint testlerini ve debug APK derlemesini çalıştırır. Derleme anahtarı geçicidir; APK yayınlanmaz veya kullanıcıya kurulum paketi olarak verilmez. Endpoint için GitHub repository variable `NGELX_LIVE_API_URL` kullanılabilir. Değer boş/geçersiz olduğunda uygulama canlı yayın başlatmayı kapatır ve kullanıcıya geçici kullanılamıyor mesajı gösterir. Secret anahtarlar APK'ya eklenmez. Bu akış Firebase dağıtımı yapmaz.
