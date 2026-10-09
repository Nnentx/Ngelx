# NgelX Build 426 — 45529.jpg: yinelenen istek ve aynı kişinin iki kez gösterilmesi

**Tarih:** 2026-10-09, cihaz saati 23:16. **Kanıt:** Kullanıcı ekran görüntüsü `45529.jpg` ve şu geri bildirimi: “İstek yollarken 2 defa Alperen çıkıyor; bir profile istek atarken ikinci defa istek yerine basınca gitmesin, tek istek gitsin.”

## Ekrandaki kesin bulgu
Gelen Kutusu > İstekler'de **Alperen Yarbay** adı iki kartta görülüyor. Bir kart **Arkadaşlık isteği** (25 dk önce), diğer kart **Takip isteği** (4 saat önce). Bu iki satır **aynı tür isteğin yinelenmesi için tek başına kanıt değildir**; ayrı istek türleridir. Kullanıcının asıl talebi, tekrar tekrar dokunulduğunda yeni kayıt oluşturulmaması ve aynı kişinin gereksiz yere listede çoğalmamasıdır.

## Kabul kriterleri / yapılacak düzeltmeler
1. Aynı gönderen UID, alıcı UID ve istek türü için **eşzamanlı en fazla bir bekleyen istek** bulunabilir. Bekleyen istek sırasında ikinci/üçüncü basma yeni kayıt, bildirim veya sayaç yaratmaz.
2. Birinci dokunuşun ardından düğme **“İstek gönderildi”** / bekliyor durumuna geçer; ağ yanıtı gelene kadar yeniden tıklamaya kapalı olur. Çok hızlı tıklama, iki telefon/oturum veya yeniden denemelerde de veritabanı seviyesinde idempotent davranmalıdır; yalnızca listede duplicate gizlemek yetmez.
3. Alıcı İstekler listesinde aynı kişiden farklı türde iki ayrı istek varsa (arkadaşlık + takip), gönderen adı gereksiz tekrarlanmasın; **tek kişi kartında** iki ayrı tür ve her birinin kendi karar durumu/aksiyonları net biçimde gösterilebilir. Bu iki ayrı türü yanlışlıkla tek işlem sayıp isteklerden birini kaybetme.
4. Onayla/Sil işlemleri ilgili türdeki bekleyen isteği doğru günceller, gönderici-alıcı durumları ve kırmızı sayaçlar tutarlı senkronize olur. Eski mükerrer pending kayıtların sunucu tarafı temizliği/güvenli migration ayrıca değerlendirilmeli.
5. Çalışan arkadaşlık ve takip ilişkileri, mahremiyet kontrolleri, bildirimler ve sohbet özellikleri korunmalı.

**Durum:** Yüksek öncelik — **açık**, henüz kod düzeltmesi veya cihazda tekrar testi yapılmadı. Build 426 kaynak testlerinin başarılı olması bu yeni istek akışı testi geçti anlamına gelmez.
