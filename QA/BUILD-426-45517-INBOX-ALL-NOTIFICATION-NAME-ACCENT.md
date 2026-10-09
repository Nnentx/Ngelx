# NgelX Build 426 — 45517.jpg: Tümü sekmesinde bildirim adı mor değil

**Tarih:** 2026-10-09. **Kanıt:** Ekran görüntüsü `45517.jpg`.

## Bulgular
Gelen Kutusu > **Bildirimler** sekmesinde kişi isimleri doğru biçimde mor vurgulanıyor (önceki cihaz testi 45527). Ancak **Tümü** sekmesindeki bildirim olaylarında **“Alperen Yarbay sana arkadaşlık isteği gönderdi”**, **“ADEM baykar sana arkadaşlık isteği gönderdi”**, **“Rojin Candan seni takip etmek istiyor”** gibi isimler siyah. Bu, aynı tür bildirim için farklı sekmelerde tutarsızlık.

## Düzeltilmesi gerekenler
- **Tümü** sekmesinde *bildirim* tipindeki her öğenin gönderen kişi adı mor (Bildirimler'dekiyle aynı mor, örn. #9353DE) ve açıklama metni koyu/siyah olsun. Aynı isim iki kez eklenmesin.
- Sadece bildirim satırları değişsin: normal bire bir mesaj ve grup sohbeti başlıklarının renk ve satır hiyerarşisini bozma.
- `canlı yayın` kırmızı ve `sesli oda` mor vurguları iki sekmede de aynı olsun.
- Hâlihazırdaki kırmızı sekme sayaçları, beyaz tema ve yeşil Grup etiketi korunsun.
- **Tümü** ve **Bildirimler** aynı ortak bildirim metni renklendirme bileşenini kullanmalı; farklı tasarım kodları yüzünden tekrar regresyon oluşmamalı.
- Kapsam testi: arkadaşlık isteği, takip isteği, canlı yayın ve sesli oda bildirimi iki sekmede görsel tutarlılık göstermeli.

**Durum:** UI regresyonu, Orta/Yüksek öncelik. Sadece QA notu kaydedildi; **kod değişikliği yapılmadı / cihaz testi geçmedi**.
