# Canlı yayın sunucusu (taslak)

Node 22 Firebase Functions: `ngelxLive` ve imzalı `ngelxLiveWebhook`.
Dağıtımdan önce LIVEKIT_URL parametresi ve LIVEKIT_API_KEY / LIVEKIT_API_SECRET secret değerleri ayarlanmalıdır.
Flutter derlemesine `--dart-define=NGELX_LIVE_API_URL=https://.../ngelxLive` eklenmelidir.
LiveKit webhook adresi `ngelxLiveWebhook` fonksiyonuna yönlendirilmelidir.
Firestore rules ve functions birlikte dağıtılmalıdır; canlı yayın belgeleri ve cüzdanlar yalnızca sunucudan yazılır.
İstemcideki eski test token servisi canlı yayın için kullanılmaz. Mevcut eski yayınlara geçiş planı gerekir.
Ödeme/yükleme ve para çekme yoktur. İstemci hiçbir şekilde jeton bakiyesi oluşturamaz.

Doğrulama: `npm ci`, `npm test`, `npm run check`.
GitHub run 38353264548: Flutter 3.47.7 paket çözümlemesi, analiz, endpoint testleri ve debug APK derlemesi geçti. Henüz yapılmayanlar: release APK dağıtımı, emulator transaction/rules entegrasyonu, iki gerçek cihazda davet/PK/hediye ve ağ kopması testleri.
Üretim öncesi: eski yayıncı tokenlarının ayrılma sonrası tekrar kullanımına karşı server-side session doğrulaması, misafir yayın yetkisi güncellemesi ile ayrılma yarışının entegrasyon testi, token yenileme ve gerçek LiveKit/Firestore üzerinde oturum-yetki entegrasyon testleri tamamlanmalıdır.
Bu değişiklik üretime hazır APK değildir.

PK kabulünde sunucuya özel `live_pk_deadlines` kaydı aynı transaction içinde oluşturulur. `ngelxFinishExpiredPK` her dakika en fazla 500 vadesi geçmiş kaydı kontrol eder; kayıt kimliği eski PK ile eşleşmiyorsa yeni maça dokunmaz. Sonuç sunucuda gecikmeli görünebilir (normalde yaklaşık bir dakika, yük/hata halinde daha uzun); süre sonrası hediyeler PK puanına dahil edilmez. Açık ekran ayrıca süre bitiminde `pk-finish` çağrısını otomatik yapar.

LiveKit participant_joined/participant_left webhookları katılımcı SID ve milisaniye katılım zamanı ile eşleştirilir; eski bağlantının ayrılması yeni bağlantıyı kapatmaz. Yayıncı ayrılınca Firestore yayını ve medya odası kapanır; konuk ayrılınca PK sonuçlanır, ana yayın sürer. Bu davranışlar imzalı webhookların doğru adrese teslim edilmesini gerektirir. Yeni eklenen 9 lifecycle testi ve 3 oturum sıralama testi dahil `npm test` ile doğrulanır.

Konuk ekranında mikrofon/kamera aç-kapat, katılım başarısızlığında tekrar deneme ve konuk yayından ayrılma kontrolleri bulunur. Yayıncı ve konuk görüntüleri sabit kimlik sırasıyla gösterilir; kamerayı kapatmak görüntü yerlerini değiştirmez. Bağlantı hatasında yerel oda her durumda temizlenmeye çalışılır; başarısız yayın başlatma kaydı sunucudan kapatılır ve kapatılamazsa yeni yayın açmadan önce yeniden denenir. Çoklu hediyelerin olay kaydı toplam jetonu `coins`, tek hediye fiyatını `unitCoins` alanında tutar.

PR doğrulama akışı: `.github/workflows/ngelx-live-draft-checks.yml` Node testlerini, Flutter 3.47.7 paket çözümlemesini, analizi, endpoint testlerini ve debug APK derlemesini çalıştırır. Derleme anahtarı geçicidir; APK yayınlanmaz veya kullanıcıya kurulum paketi olarak verilmez. Endpoint için GitHub repository variable `NGELX_LIVE_API_URL` kullanılabilir. Değer boş/geçersiz olduğunda uygulama canlı yayın başlatmayı kapatır ve kullanıcıya geçici kullanılamıyor mesajı gösterir. Secret anahtarlar APK'ya eklenmez. Bu akış Firebase dağıtımı yapmaz.

Mevcut Build 347 release workflow da public repository variable NGELX_LIVE_API_URL değerini dart-define ile alır. Bu değişiklik release çalıştırmaz; imzalı kurulum paketi ve sürüm yükseltmesi ayrıca hazırlanmalıdır.

Yayın yetkisi: yeni tokenlar yayıncı dahil salt izleyici izniyle üretilir. Kamera/mikrofon açılmadan önce publish endpoint mevcut rolü, katılım yuvasını ve LiveKit SID değerini kontrol eder; izin verildikten sonra tekrar doğrular. Eşzamanlı ayrılmada rol önce kapatılır, ardından medya katılımcısı çıkarılır. İzin geri alma başarısızsa katılımcıyı çıkarmayı dener; hata gizlenmez. Eski yayın tokenıyla yeniden katılım imzalı webhook üzerinden güncel rol ile uzlaştırılır. Webhook teslimindeki gecikmeler ve gerçek LiveKit reconnect/token yenileme davranışı hâlâ iki cihaz entegrasyon testinde doğrulanmalıdır. Sekiz ek yetki yarışı testi dahil toplam 26 Node testi geçmektedir.

Hediye tekrar denemesinde önce sunucu işlem makbuzu okunur: aynı işlem yayın kapandıktan sonra da başarıyla doğrulanır, yeni işlem kapalı yayına gönderilemez. Değişmiş alıcı/adet aynı requestId ile kullanılamaz. Yedi ek gift transaction akışı testi toplam 33 Node testine dahildir; bu testlerin transaction adapteri bellektedir, gerçek Firestore transaction yük/yarış testi yerine geçmez.

Canlı yayın Firestore kuralları mevcut `tools/firestore_rules_test.mjs` emülatör akışına bağlandı. `tools/live_rules_test.mjs` cüzdan mahremiyetini, istemcinin jeton/PK/hediye/kabul kaydı yazamamasını, istek görünürlüğünü, yorum kimliği ve uzunluk denetimini, kapalı yayına yorum/tepki engelini test eder. Yorumlar en fazla 500 karakterdir; serverTimestamp zorunludur. 407faf4 için GitHub run 38355373976 üzerinde yeni canlı yayın kuralları emulator adımı geçti.

Gerçek proje bağlantısı, secret kurulumu, eski APK geçişi ve iki cihaz adımları: [DEPLOYMENT.md](DEPLOYMENT.md).

Keşfet grup katılımı: onay isteyen keşfedilebilir gruplarda kullanıcı kendi katılma isteğini gönderir/iptal eder. Reddedilen veya iptal edilmiş istek yeniden gönderilebilir; onaylı üyelik ana grup stream'i güncellenince Aç düğmesine dönüşür. Özel/silinmiş/dolu gruplar ve onayı istemciden atlatma Firestore kurallarıyla engellenir. Görünen en fazla 60 grup yerelde updatedAt/createdAt ve kararlı ID sırasıyla düzenlenir; bu tüm veritabanını sıralayan bir sorgu değildir. `tools/discovery_group_rules_test.mjs` mevcut emülatör akışında onay/iptal/yeniden gönderim ve erişim denemelerini doğrular. Yeni testlerin GitHub sonucu beklenmelidir.
