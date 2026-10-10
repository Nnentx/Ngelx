# Build434 — cihaz testi takip paketi

## Doğrulanan ve korunacak davranışlar

45677: takip/arkadaşlık ayrı sayfaları, onay sonrası 2→1 sayaç, elle yenileme.
45678: beyaz yuvarlak mor zil, sekmesiz Bildirimler, onaylama, profile geçiş, tümünü okundu rozeti.
45692: takip/arkadaşlık ret mesajı ve kırmızı sonuç işareti, tekrar arkadaşlık gönderme/kabul.
Kullanıcı hikâye video/retry/doğru hikâye, arşiv, profil araması/geçiş hızını tamamlandı dedi; yeniden açılmaz.

## Düzeltmeler

- Bildirim ekranında kabul/ret eski kopyaları aynı işlemde sonuçlandırır; yeni nesil isteği yanlışlıkla kapatmaz.
- Kabul/ret/iptal bildirim metni sonuca göre yazılır. Gelen Kutusu canonical istek durumunu canlı okur.
- İstekler kök sayfasında yalnız üç kategori kartı; eski inline Onayla/Sil listesi kaldırılır.
- Canlı bitiş ve grup katılım sonucu kişi isimleri mor.
- Mesajlar/Tümü ve Arkadaşlar fotoğraf yanında yeşil aktif nokta veya dakika/saat/gün etiketi; gizlilik kapalıysa hiçbir durum gösterilmez. 30 saniyede yaş etiketi yenilenir, 120 saniye heartbeat sınırı korunur.
- Ayarlar sürümü 1.0.209 Yapı434 ile gerçek APK sürümü eşleşir.
- Yeni kayıt zaten privateAccount=false, profileViewPermission=all, discoverableProfile=true, showActivityStatus=true oluşturur. Oturum tamamlama yalnız eksik alanları doldurur; mevcut tercihleri ezmez.

## Açık doğrulamalar ve kalan kapsam

Yeni mesaj isteği sayaç/kabul/sil cihaz testi, ret sonrası sayaç testi, presence iki cihaz/gizlilik testi ve canlı geçmiş/silme testi açık.
36 otomatik eski hikâye temizliği, 44 mesaj medyası retry, 45 mesaj medya cache, 46 sahipsiz medya taraması tamamlanmış sayılmaz. 46/46 iddiası yok.
CI sonucu daha sonra kaydedilir; APK hazır varsayılmaz.
