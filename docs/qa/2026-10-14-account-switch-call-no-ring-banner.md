# Hesap geçişi sonrası zil yok; gelen arama kartı arama ekranını açmıyor

14 Ekim 2026, 10:46 (Europe/Istanbul). Referans: 47191.jpg.

Kullanıcı hesap değiştirip Dilek'i aradığını, zil sesinin hâlâ olmadığını bildiriyor. Görselde Akış üzerinde ADEM baykar / Gelen sesli arama kartı ve kırmızı ret, yeşil kabul düğmeleri var. Kullanıcı kartın Adem adı/gövdesine basılamadığını ve basınca arama ekranına gitmesini istiyor.

İki ayrı açık hata:
1. Gerçek cihazda hesap geçişi sonrasında gelen arama zili hâlâ duyulmuyor. Arama kartının görünmesi zilin/sesin çalıştığını kanıtlamaz. Önceki otomatik testler nedeniyle hata çözülmüş sayılmamalı. Bu kullanıcı bildirimi sesli aramayla ilgili; burada grup veya görüntülü aramanın ayrıca test edildiği varsayılmadı.
2. Gelen arama kartının adı/gövdesine dokununca ilgili gelen arama ekranı açılmıyor. Kart dokunulabilir olmalı; Akış'ta bırakmamalı.

Sonraki toplu paket kabul ölçütleri:
- Hesap A'dan B'ye geçiş sonrası güncel hesap cihaz kaydı ve arama dinleyicileri doğru hesaba bağlı olmalı; gerçek iki telefonda zil doğrulanmalı.
- Normal ses/bildirim izinleri açıkken gelen arama duyulur zil üretmeli; kabul/ret/bitiş/zaman aşımında zil durmalı. Kullanıcının cihazındaki izin/ses ayarları görselden bilinmiyor; sorun otomatik olarak ayarlara bağlanmamalı.
- Kart gövdesi/adı ilgili arama ekranını açmalı. Ekranı açmak aramayı kendiliğinden kabul etmemeli; kullanıcı kabul/ret kararını korumalı.
- Kırmızı ve yeşil düğmelerin ayrı ret/kabul davranışı korunmalı; gövde dokunuşu düğme eylemleriyle çakışmamalı.
- Aynı çağrı yeniden oluşturulmamalı; sona ermiş çağrı açılmamalı.

Önceki devam eden görüşme bildiriminin Akış açması kaydıyla ilişkili ama farklı bir giriş noktasıdır; ikisi de test edilmeli.

Durum: kullanıcı isteğiyle toplu düzeltme listesine kaydedildi. Bu turda kod veya APK değiştirilmedi.
