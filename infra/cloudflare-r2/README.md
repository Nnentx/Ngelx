# NgelX R2 ücretsiz medya katmanı

V47 yeni medya yüklemelerini Cloudflare R2'ye yönlendirebilecek şekilde hazırlanmıştır.

- Firebase Auth: kullanıcı kimliği
- Firestore: mesaj/profil/sosyal veri
- Cloudflare R2: fotoğraf, video, hikâye, sohbet medyası
- CachedNetworkImage: cihaz tarafında disk cache
- Video gridleri: gerçek MP4'ü önizleme için indirmez

Uygulama `NGELX_MEDIA_API_BASE` boşsa güvenli geçiş için Supabase Storage'a geri döner. R2 etkinleştirildiğinde APK şu şekilde derlenir:

`flutter build apk --debug --dart-define=NGELX_MEDIA_API_BASE=https://WORKER-ADRESI`

Cloudflare tarafında:
1. R2'yi etkinleştir.
2. `ngelx-media` bucket oluştur.
3. `wrangler.toml.example` dosyasını `wrangler.toml` olarak kopyala.
4. Firebase Web API key'i gir.
5. `npx wrangler deploy` çalıştır.
6. İstersen daha sonra `media.ngelxsocial.com` custom domain bağla.

Ücretsiz katman sınırsız değildir. Ama bu mimari Supabase cached egress darboğazını ortadan kaldırmak ve ilk kullanıcı döneminde maliyeti minimumda tutmak için hazırlanmıştır.
