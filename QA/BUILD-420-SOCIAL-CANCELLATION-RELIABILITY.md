# Build 420 — Takip ve arkadaşlık isteği geri çekme tutarlılığı

## Bulunan somut hata
`sosyalIstekIptalEt` mevcut kodunda giden isteğin sunucu belgesini okurken çıkan hata `catch(_){}` ile yutuluyordu. Hiçbir istek güncellenmediğinde bile fonksiyon sorunsuz dönüyor; çağıran ekran **“İstek geri çekildi”** mesajını gösterebiliyordu. Bu durum daha sonraki yüklemelerde **“Takip isteği bekliyor”** metninin yeniden belirmesine yol açar.

## Build 420 düzeltmesi
- İstek veya istek bildirimi bulunamadığında açıklayıcı hata verir.
- **Giden istek** belgesinin sunucu okumasında zaman aşımı/yetki/haberleşme hatası artık saklanmaz; asıl iptal yazısı gerçekleşmeden başarı bildirilmez.
- Önceden kullanılan `status:cancelled`, `cancelledAt`, bildirim `read:true` ve `batch.commit` korunur.
- Hem istek hem bildirimde iptal edilecek bekleyen kayıt kalmamışsa açıkça iptal gerçekleştirilemedi der.
- Bildirimin ikincil okuması başarısız olsa da ana giden istek doğrulanıp güncellenebiliyorsa güvenli biçimde iptal edilir; karşı hesap eski bildirimi açtığında isteğin iptal edildiğini görebilir.

## Korunanlar
Build 419'un ayrı bildirim gönderimi ve giden istek yükleme kontrolü, Build 412–418 kapaklı/kapaksız profil, arama, arkadaşlar, takipçi, mesaj, bildirim, kimlik doğrulama ve kaydedilmiş hesap akışı korunur. Firestore kuralları ve canlı üretim kayıtları değiştirilmez.

## Cihaz testi
- İstek gönder -> geri çek -> gönderici/alıcının durumu kısa süre sonra uyumlu olmalı.
- İnternet kesikken iptal et -> yanlış başarı mesajı çıkmamalı.
- Çoktan cevaplanmış/silinmiş isteği iptal et -> gerçekte değişiklik yoksa başarı gösterilmemeli.
- Arkadaşlık, takip, gizlilik ve kapaklı/kapaksız görünüm regresyonları aynı kalmalı.

**Durum:** Kod ve CI zinciri hazır. Firebase emulator, Flutter analyze, APK ve gerçek cihaz testleri tamamlanmadan tüm maddeler bitmiş sayılmaz.
