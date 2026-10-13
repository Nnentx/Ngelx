# NgelX Build 451 — doğrulanmış durum

Sürüm: 1.0.226 / Yapı 451. Temel: work/build-450-approved-discovery-community.

## Bu pakette uygulananlar

- Canlı yorum paneli küçültüldü; son üç yorum gösteriliyor.
- Kamera klavye açılınca küçülmüyor; yorum satırı klavyenin üzerinde kalıyor.
- Yayın araçları varsayılan olarak kapalı; üç noktayla açılıyor ve klavyede gizleniyor.
- Yayını bitirme için üstteki onaylı çıkış kullanılıyor.
- Keşfet ve topluluk kategori filtreleri beyaz/mor.
- Toplulukta toplu üyelik/gönderi onayı ve ret: işlem güncel kayıtları yeniden okuyor, 500 üye sınırını koruyor, eşzamanlı düğmeleri kilitliyor.
- Topluluk akışında yükleme göstergesi ve yeniden deneme var. İndeks eksikliği giderilmiş değildir.
- Arama sonlandırma bildirimi zaman aşımından önce işleniyor; gelen arama bildirimi 60 saniye ile sınırlı ve iptal edildiğinde zamanlayıcısı kaldırılıyor.

## Doğrulama

GitHub Actions: https://github.com/Nnentx/Ngelx/actions/runs/38454496936

- Flutter analizi, küçük ekran testleri, mevcut davranış testleri ve Firestore güvenlik testleri geçti.
- Toplu onayın atomik olması ve yönetici olmayanın onay verememesi test edildi.
- 37 sunucu yetkilendirme/arama testi yerelde geçti.
- 100 sürüm dönüşümü son kodla yerelde başarıyla uygulandı.
- İmzalı APK derlemesi, mevcut sertifika, sürüm ve SHA-256 kontrolleri geçti.

## Gerçek engeller

1. Topluluk gönderi akışı indeksi: `posts`, COLLECTION kapsamı, `status` ASCENDING ve `createdAt` DESCENDING. Önceki oluşturma isteği 403 yetki hatasıyla reddedilmiş. İndeks oluşturulmadan mevcut sıralı sorgu hazır değildir.
2. Arka plan arama push işlevi: `incomingCall448` dağıtımı Cloud Build API kapalı ve hesabın API açma yetkisi olmadığı için başarısız. Arka planda zil çalması doğrulanmış değildir.

Bu işlemler proje yönetici erişimi gerektiriyor. Uygulama değişiklikleri bu sunucu engellerinin yerine geçmez.

## Henüz tamamlanmayan kapsam

- Referans 47052.mp4'teki katılım soruları ve cevapları.
- Gelişmiş otomatik spam/moderasyon uyarıları, topluluk görevleri ve ayrıntılı erişim istatistikleri.
- İki gerçek telefonda izleyici görüntü/ses, davet teslimi, konuk katılımı, PK, özel ve grup araması zil testi.
- Gerçek cihazda klavye, yorum paneli, kamera kadrajı ve yeniden bağlanma kontrolü.

Bu sürüm bütün eksiklerin tamamlandığı nihai paket olarak işaretlenmemelidir. Eski profil, akış ve sohbet kapsamı korunur; yalnızca doğrulanan maddeler tamamlandı olarak kabul edilir.
