# NgelX Build 424 — hikâye yanıtının Build 423'te tekrar başarısız olması

**Tarih:** 2026-10-09. Kullanıcı Build 423 testinin devamında “Hikaye yine ayni” dedi.
**Kaynak:** Önceki 45407 kritik hikâye yanıtı başarısızlığı; yeni bir ayrı hata olarak çoğaltılmadı.

## Gerçek cihaz sonucu
- **Build 423:** Hikâye yanıtı hâlâ başarısız — **Geçmedi / Kritik**.
- Kullanıcı bu mesajda yeni hata kodu, aşama veya ekran videosu paylaşmadı. Dolayısıyla 423 canlı kök nedeni kesin olarak saptanmış değildir.
- Önceki video 45407 ve Build 422 inceleme kayıtlarıyla ilişkilidir.

## Build 424 adayı
- Hikâyenin gerçek sahibi `videos/{storyId}.ownerId` üzerinden denetlenir.
- Üye olunan eski sohbetler aranırken sorgu hata verirse engelleme/gizlilik koşulları korunarak yeni izinli bire bir sohbet oluşturma yoluna geçilir.
- Hikâye mesajı, sohbet önizlemesi ve okunmamış sayacından **ayrı, öncelikli** kaydedilir; önizleme güncellenmezse mesaj geri alınmaz.
- Başarısız adım ve Firebase hata kodu, kişisel veri yazdırmadan kullanıcıya gösterilir.
- Firestore güvenlik kuralları ve mevcut canlı hesap verileri değiştirilmedi.
- Yeni Firebase emülatör senaryosu: yetkili kullanıcının gönderdiği hikâye mesajı alıcı tarafından okunabilir; özel/kapalı hedefe izinsiz DM reddedilir.

**Otomatik test:** GitHub Actions 37974274829 başarılı: kaynak koruma testleri, Firebase emülatörü, Flutter analiz, APK oluşturma ve imza kontrolü.

**Cihaz kabul kriteri HÂLÂ AÇIK:** Build 424'te iki ayrı hesap ile hikâyeye yazılı yanıt ve emoji tepkisi gönder; gönderim başarılı, alıcı sohbetinde hikâyeye bağlı olarak görünür, spam/çift mesaj oluşmaz. Gönderilemezse yeni hata aşaması/kodu ve hesabın ekranı kaydedilsin. Otomatik test başarıları canlı teslimin kanıtı değildir.
