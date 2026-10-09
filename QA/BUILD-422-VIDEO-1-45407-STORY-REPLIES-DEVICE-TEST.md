# NgelX Build 422 — Hikâye testi (45407.mp4)

**Tarih:** 09.10.2026. **Video süresi:** yaklaşık 55,4 saniye. **Sürüm bilgisi:** Önceden verilen Ayarlar görüntüsü `v1.0.197 · Yapı 422` kurulumunu doğruluyor; video içinde sürüm sayfası tekrar açılmıyor.

## Kesin gözlenen hata — P1
- **~00:24–00:26, 00:30–00:42:** En az bir fotoğraf ve video hikâyesinde yanıt/tepki denemelerinden sonra **“Hikâye yanıtı gönderilemedi.”** mesajı defalarca görülüyor. “slm” gibi kısa yanıtların yazılması ve gönderme simgesine basılması da kayda giriyor.
- Aynı önceki Build 421 sorunu Build 422 kod değişikliklerinden sonra da cihazda görülüyor. Kod ve Firebase emulator testlerinin başarılı olması bu canlı senaryoyu **geçmiş** yapmaz.
- **Kök neden bilinmiyor:** mesaj izinleri, hedef UID, sohbet oluşturma / batch yetkileri, mevcut sohbetin üyeleri, kullanıcı gizliliği veya başka hata olabilir. Firestore hata kodu ve mesajın gerçek alıcı hesabına düşmesi gerekir.

## UI / içerik gösterimi
- **~00:28–00:37:** Uzun kullanıcı adı `@irazumayy` veya benzeri metin ve göreli yayın süresi bazen üst bölümde birden fazla satıra bölünerek dar bir alana sıkışıyor. Kırılma, geçiş progress barının üzerine gelmemeli.
- **Hikâye başlangıç/bitiş paneli** için tam yerel tarih-saat ve kalan süre videoda net doğrulanmıyor. Göreli “1 sa önce” görülüyor; Build 421/422'de eklenen tam zaman panelinin her hikâye açma yolunda gösterilip gösterilmediği ayrıca test edilmeli.
- **~00:39–00:43:** Bir fotoğraf hikâyesinde alt yanıt çubuğu ve açıklama içeriği üst üste gelebiliyor; küçük ekran, klavye açık/kapalı davranışını doğrulamak gerek.

## Çalışan, korunacak
- Hikâye görüntüsü ve videolar açılıyor, birkaç farklı hikâyeye geçiliyor, fotoğraf/video gösterimi sürüyor.
- Mesaj yazma alanı, klavye ve emoji/tepki seçenekleri açılıyor.
- **~00:44–00:51:** Normal sohbet açılıyor; mesaj baloncukları ve yazma kutusu görünüyor. Bu normal DM görünümü hikâyeye yanıtın teslim edildiğini kanıtlamaz.
- **~00:03–00:11:** Hesap değiştirme ekranı açılıyor ve Akış geri geliyor (geçici yükleme var).

## Work düzeltme ve güvenlik kabulü
1. İsteğe özel debug izleme: olay safhası ve `FirebaseException.code` (kimlik/sohbet mesaj içeriğini loglamadan).
2. Hikâye sahibi/izleyici, engelleme ve `messagePermission` izinlerini değiştirmeden izinli yanıtı doğru sohbete göndermek.
3. Mesajın karşı kullanıcının Gelen Kutusu'nda görülmesini iki gerçek hesapla doğrulamak.
4. Hikâyede tam başlangıç ve son bitiş zamanı, kalan süre ve uzun isim yerleşimini küçük ekranda test etmek.
5. Başarılı normal sohbet, video oynatma, 24 saat hikâye TTL ve engel korumasını regresyon testine almak.

**Bu rapor yalnız QA kaydıdır. Kod değiştirilmedi.**