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
CI 38061499114 başarılı: Build395–434 kaynak/koruma zinciri, Flutter analizi (835 uyarı/bilgi; fatal hata yok), 26 davranış testi, Firestore emulator ve release APK üretimi geçti. APK imzası v2 doğrulandı. Test edilen kaynak: 7a3e1b392283fa1f981527ac31d642be9f263d69. APK/ZIP hash doğrulaması ve dosya kaydı aşağıya eklenir.

Aktiflik satırı kullanıcı değiştirdiğinde önceki snapshot silinir; geçmişte sonuçlanmış bir isteğin sonucu yeni istek gönderilince ezilmez.

APK: NgelX-Build434.apk, 145085322 bytes. Native manifest versionName=1.0.209, versionCode=434; arm64 AOT includes Ngelx434AktifAvatar.
SHA256: 1eed8ae3f3d9c1fcff0bb473f63a647578b38258ec5261ee8b7cfc249f25979c
Artifact ZIP SHA256: 51aa65c2a77249b03a792a37b69a1abba7b8480c84cfc3293da015a726d58a80
