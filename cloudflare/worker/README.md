# NgelX ücretsiz medya katmanı (Cloudflare R2)

Bu Worker, NgelX fotoğraf/video dosyalarını Cloudflare R2 üzerinde depolamak ve Firebase Authentication ile güvenli yükleme/silme işlemleri yapmak için hazırlanmıştır.

## Güvenlik
- Upload ve delete istekleri Firebase Authentication ID token ile doğrulanır.
- Kullanıcı yalnızca kendi yüklediği R2 nesnesini silebilir.
- Dosya türleri ve boyutları sunucu tarafında sınırlandırılır.
- Firebase service-account anahtarı mobil uygulamaya veya repoya konmaz.

## İlk kurulum
1. Cloudflare hesabında `ngelx-media` isimli bir R2 bucket oluştur.
2. Bu klasörde `npm install` çalıştır.
3. `npx wrangler login` ile hesabı bağla.
4. `npm run deploy` çalıştır.
5. Worker adresini not al. Örnek: `https://ngelx-media.<hesap>.workers.dev`.
6. Firestore'da `app_config/media` belgesine `uploadApi` alanı olarak bu adresi yaz.

Uygulama `app_config/media` belgesindeki `uploadApi` adresini kullanır. Yeni medya yalnızca Cloudflare R2'ye yüklenir.

## Ücretsiz kota yaklaşımı
R2 depolama ve işlem ücretsiz kotası aşıldığında ücret oluşabilir; bu yüzden uygulamadaki thumbnail/cache/boyut limitleri ayrıca korunur.
