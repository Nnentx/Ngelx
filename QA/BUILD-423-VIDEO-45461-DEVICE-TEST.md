# NgelX Build 423 — 45461.mp4 cihaz test kaydı

**Tarih:** 2026-10-09, cihaz saati yaklaşık 20:56–20:57, **video süresi:** 58 saniye.
**Kanıt:** Bu konuşmada paylaşılan `45461.mp4` ekran kaydı. Ses izi sessiz; yalnızca görülen görsel eylemleri değerlendir.
**Sürüm:** 00:00 civarında Ayarlar ve gizlilik içinde `Uygulama güncellemeleri / v1.0.198 · Yapı 423` açıkça görünüyor.
**Kapsam:** Gelen Kutusu, sekme sayaçları, bildirim renkleri, grup etiketleri ve sohbet navigasyonu.
**Değişiklik politikası:** Kaynak kodu değişikliği yok; test bulguları ayrı kaydedildi. Gösterilen bir özellik için karşı hesap teslimini varsayma.

## Videoda doğrulanan / geçenler

| Yaklaşık süre | Gözlem | Durum |
| --- | --- | --- |
| 00:00–00:04 | Build 423 sürüm bilgisi; Ayarlar'dan Gelen Kutusu'na geçiş, kısa yüklemeden sonra liste açılıyor. | Geçti — uygulama açılıyor; yükleme gecikmesi ayrıca ölçülmedi |
| 00:04–00:08, 00:20–00:25, 00:34–00:57 | `Tümü`, `Mesajlar`, `Gruplar`, `Bildirimler`, `İstekler` sekmeleri açılıyor ve kırmızı sayı rozetleri görünüyor. Örnek: Tümü 88, Gruplar 21, Bildirimler 67. | Geçti — rozet görünümü; verilerin doğruluğu ayrıca karşılaştırılmalı |
| 00:09–00:12 | Umay profil ekranı ve takip/arkadaşlık/mesaj eylem düğmeleri açılıyor. | Geçti — görünüm; istek kabul/ret test edilmedi |
| 00:15–00:19 | Özel sohbet açılıyor; eski ve yeni mesaj baloncukları, yazma alanı ve sohbet arka planı görünüyor. | Geçti — görünürlük/navigasyon; karşı tarafa teslim test edilmedi |
| 00:20–00:25 | Mesajlar sekmesi listeleniyor; Gruplar sekmesindeki sohbetlerde küçük yeşil `Grup` etiketi mevcut. | Geçti — grup ayırt etme tasarımı |
| 00:26–00:30 | Bir grup sohbetine giriliyor, “Bu grupta engellediğin bir kişi var” uyarısı gösteriliyor, `Gruba gir` seçildikten sonra mesaj yazılıp gönderiliyor; grup liste önizlemesinde yeni mesaj ve zaman güncelleniyor. | Geçti — yerel ekranda gösterim; karşı hesap teslimi test edilmedi |
| 00:34–00:53 | Bildirimler sekmesinde kullanıcı adları mor ve “canlı yayın” kırmızı, “sesli oda” mor vurgulu. | Geçti — renk hiyerarşisi |
| 00:54–00:56 | İstekler sekmesi açılıyor; `Mesaj İstekleri` kutusu üstte, altında sosyal istek kartı yok; 00:57 Bildirimler'e geçilebiliyor. | Geçti — sekme navigasyonu/boş durum; bekleyen istek bulunduğuna dair kanıt yok |

## Hâlâ açık / bu video ile doğrulanamayanlar

1. **Kritik:** Hikâye yanıtı gönderiminin iki hesap arasında çalışması, hikâyeye bağlantılı mesajın alıcı sohbetine ulaşması (**45407**) videoda test edilmedi. Önceki cihaz hatası açık tutulmalı.
2. **Kritik:** Gönderenin profilindeki **Yanıtla** → okunabilir **Kabul et / Reddet** alt paneli ve gerçek kabul/ret işlemi (**45411**) videoda test edilmedi. Eski boş panel hatası kapanmadı.
3. **Yüksek:** Kullanıcı önceki videolarda **aynı göndericiden tekrar eden istek kayıtları** bildirdi. Bu videoda aktif bekleyen sosyal istek yok; tekilleştirme ve sunucu durum tutarlılığı doğrulanamadı.
4. **Yüksek:** Hesap değiştirildikten sonra Akış'ın siyah `Akış hazırlanıyor...` beklemesinin süresi bu videoda ölçülmedi.
5. **Ürün kalitesi:** Sekme rozetlerinin backend okunmamış/istek sayılarıyla gerçekten eşleşmesi, Bildirimler ve Tümü sayaçlarının çift sayım yapmaması, grup unread sayılarının açınca azalması cihaz karşı-testini bekliyor.
6. **Hikâye UI:** İsim/üst bilgi sıkışması, başlangıç-bitiş zamanı ve kalan süre eksikleri 45407 sonucuna göre açık; video bu ekranları göstermiyor.
7. İstekler'de yalnızca mesaj istekleri görünmesi **tek başına hata kanıtı değildir**: Bildirimler'de geçmiş “sana arkadaşlık isteği gönderdi” olayının görünmesi, isteğin hâlâ beklediğini kanıtlamaz. Aktif bekleyen ilişkiyle yeniden test edilmeli.

## Beklenmedik sayılmaması gereken davranışlar

- Gruptaki **engellenmiş kişi uyarısı**, kullanıcı onayıyla girilebilen bir gizlilik bilgilendirmesi şeklinde görünüyor; tek başına bug olarak yazılmadı.
- Özel sohbetin üstündeki “Özel sohbet” bilgilendirme şeridi kısa süre görünüyor; normal geçiş olabilir.
- Girilen mesajın grupta görünmesi, uzaktaki tüm üyelere teslim edildiğini kanıtlamaz.

**Genel sonuç:** Build 423 Gelen Kutusu görsel düzeltmelerinin bir bölümü telefon üzerinde başarılı. Kritik hikâye/istek işlevleri için cihaz kabulü hâlâ eksik. GitHub otomatik derleme/test başarısını cihaz testiyle karıştırma.
