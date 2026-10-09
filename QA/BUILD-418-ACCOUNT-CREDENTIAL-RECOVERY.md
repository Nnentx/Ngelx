# Build 418 — Hesap değişiminde hatalı kaydedilmiş şifreyi kurtarma

## Kaynakta bulunan sebep
`HesapDegistirPage._giris` daha önceki hızlı giriş şifresini güvenli hafızadan okuyup doğrudan yeniden kullanıyor; Firebase bu şifreyi reddetse bile giriş hep aynı şifreyle tekrarlanabiliyordu. Ayrıca şifreye `.trim()` uygulanması başında veya sonunda boşluk bulunan gerçek şifreleri değiştirebiliyordu.

## Düzeltilenler
- Şifreler asla kırpılmaz; kullanıcı tarafından girildiği veya güvenli depoda saklandığı biçimde kullanılır.
- Sadece güvenli hafızadan alınmış şifrenin Firebase `wrong-password` / `invalid-credential` koduyla reddedilmesi halinde o hesabın eski şifre anahtarı silinir. E-posta/UID listesi, diğer hesaplar veya sunucu verileri silinmez.
- Ekranda **“Kaydedilmiş şifre kabul edilmedi. Geç’e yeniden dokunup güncel şifreni gir.”** açıklaması gösterilir. Sonraki tıklamada şifre yeniden istenir.
- Güvenli şifre saklama, hesap ekleme, beş hesap sınırı, kilit/hata metinleri, çıkış ve profil yükleme akışları korunur.

## Test
- Yanlış kaydedilmiş şifreyle hesap değiştirme -> açıklayıcı uyarı; yeniden deneyince şifre ekranı açılmalı.
- Doğru şifreyle hızlı hesap değiştirme aynen çalışmalı.
- Gerçekten içinde boşluk bulunan şifre kesilmemeli.
- Diğer cihaz kayıtları, kullanıcı avatarları ve arkadaş listesi aynen kalmalı.

**Durum:** Kodlandı, otomatik kontroller ve gerçek Android cihaz testi bekliyor. Firestore kuralları değişmiyor.
