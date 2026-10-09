# NgelX Build 426 — 45534.jpg: Bildirimler sayacı sıfırlanmıyor

**Kullanıcı bildirimi:** Gelen Kutusu > Bildirimler rozetinde **32** görünüyor. Kullanıcı sekmeye girip çıkıyor, yeniden giriyor, sayı hâlâ **32**. Ekran görüntüsü 32 rozetini gösteriyor; giriş/çıkış davranışı kullanıcı anlatımına dayanıyor.

**Beklenen:** Bildirimler açıldığında gerçekten görülen/okunan bildirimler okunmuş olarak işaretlenmeli. Kırmızı rozet yalnızca okunmamış bildirimleri saymalı; okunma durumu backend, istemci ve hesap değiştirme akışında senkron kalmalı. Sadece sekmeye girilmesi tüm bildirimlerin okundu sayılması ürün kararına bağlıysa tutarlı uygulanmalı; görünmeyen bildirimleri yanlışlıkla okunmuş saymamak için liste görünürlüğü veya açık 'tümünü okundu işaretle' davranışı değerlendirilmeli. İstekler sayacı ayrı ve gerçek pending sayısına bağlı kalmalı. Mevcut mor kişi adları ve diğer çalışan UI bozulmamalı.

**Durum:** Açık QA hatası; kod değişikliği yapılmadı.