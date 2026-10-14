# Devam eden görüşme bildirimi yanlış ekranı açıyor

14 Ekim 2026, 09:59 (Europe/Istanbul). Referanslar: 47192.jpg ve 47193.jpg.

Kullanıcı bildirimi: Android bildirim perdesindeki “NgelX görüşmesi devam ediyor / Görüşmeye dönmek için dokun” bildirimi dokununca görüşme yerine Akış ekranını açıyor. İlk görsel bildirimi, ikinci görsel Akış ekranını gösteriyor. Mikrofon göstergesi görünür; görseller tek başına hangi görüşme türünün sürdüğünü veya gerçek ses aktarımını kanıtlamaz.

Sonraki toplu paketin kabul ölçütleri:
- Devam eden görüşme bildirimine dokununca uygulama ilgili mevcut görüşme ekranına dönmeli; Akış açılmamalı.
- Güncel oturum kimliği ve görüşme türü taşınmalı: özel/grup sesli-görüntülü arama veya bildirimi kullanan canlı/sesli oda hangisiyse doğru ekran açılmalı. Kullanıcının bu kayıtta hangi türü kullandığı henüz net değil.
- Mevcut görüşme yeniden kullanılmalı; ikinci görüşme açılmamalı, süre/ses/kamera durumu sıfırlanmamalı.
- Uygulama ön planda, arka planda ve Activity yeniden oluşturulduğunda yönlendirme kontrol edilmeli; uygulama hazır değilse bekleyen işlem giriş/başlatma sonrası işlenmeli.
- Görüşme gerçekten bittiyse bildirim temizlenmeli ve hayalet oturum açılmamalı. Aktif oturumla uyumlu dönüş/kapatma davranışı olmalı.

Durum: toplu düzeltme listesine kaydedildi. Bu turda kod veya APK değiştirilmedi.
