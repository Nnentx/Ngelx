# NgelX Cloudflare R2 medya katmani

Bu klasor V47 icin hazirlanan medya servisidir. Amaç Supabase Storage egress kotasini yeni yuklemeler icin devreden cikarmak ve R2'nin ucretsiz katmanindan yararlanmaktir.

## Mimari

- Firebase Auth kullanici kimligini vermeye devam eder.
- Firestore mesaj, profil ve sosyal verileri tutar.
- R2 fotograf, video, hikaye, GIF, profil medyasi ve sohbet medyasini tutar.
- Worker yukleme/silme islemlerinde Firebase ID token'i dogrular.
- Eski Supabase URL'leri okunmaya devam eder; yeni dosyalar R2'ye gecebilir.
- NGELX_MEDIA_API_BASE tanimli degilse uygulama otomatik olarak Supabase Storage'a geri doner. Boylece gecis tek seferde uygulamayi bozmaz.

## Kurulum

1. Cloudflare hesabinda R2 aboneligini etkinlestir.
2. Standard storage sinifinda `ngelx-media` adinda bucket olustur.
3. Bu klasorde `wrangler.toml.example` dosyasini `wrangler.toml` olarak kopyala.
4. `FIREBASE_WEB_API_KEY` degerini Firebase projesindeki Web API key ile doldur.
5. `npx wrangler deploy` ile Worker'i yayinla.
6. Uygulamayi `--dart-define=NGELX_MEDIA_API_BASE=https://<worker-adresi>` ile derle.
7. Daha sonra istersen R2 bucket'a `media.ngelxsocial.com` custom domain bagla ve `PUBLIC_BASE_URL` degerini ona cevir.

R2 ucretsiz katmani sinirsiz degildir. Kod dosya boyutunu sinirlar ve istemci thumbnail/cache kullanir; yine de depolama ve islem kotalari takip edilmelidir.
