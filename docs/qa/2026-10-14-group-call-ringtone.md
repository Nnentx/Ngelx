# Grup sesli araması — zil çalmıyor

2026-10-14 01:14 Europe/Istanbul: Kullanıcı grup sesli aramasında karşı tarafta zil çalmadığını tekrar bildirdi. Kritik ve açık hata olarak takip edilmeli. Build452 sunucu yayını ve APK teslimi bu davranışın gerçek cihazda düzeldiğini kanıtlamaz; kurulu sürüm bu mesajda ayrıca gösterilmedi.

Kontrol kapsamı: çağrı kaydının ve grup alıcılarının doğru belirlenmesi; çağrıyı başlatan cihazın Worker isteği; sunucunun FCM gönderimi; alıcı cihaz token kaydı ve bildirim izinleri; ön plan/arka plan/ekran kapalı davranışı; Android gelen arama bildirim kanalı ve zil sesi; iptal ve zaman aşımında bildirim temizliği. Nedeni henüz doğrulanmadı.

Kabul ölçütü: İki gerçek telefonda grup sesli araması başlatıldığında uygun alıcı cihazda gelen arama ekranı ve sesli zil görülmeli/duyulmalı; uygulama açık, arka planda ve ekran kapalı senaryoları ayrı doğrulanmalı. Tamamlandı olarak işaretleme yalnızca cihaz testi sonrası yapılmalı.
