# NgelX Build 403 – Sesli Odalar gerçek cihaz video testi

**Tarih:** 2026-10-08. **Video:** Kullanıcı tarafından bu sohbette gönderilen `45084.mp4`, yaklaşık 2 dk 23 sn, dikey Android ekran kaydı. Bu belge gözlenen arayüzü kaydeder; canlı sunucu, karşı cihaz sesi ve alıcı mesajı erişimi bulunmuyor.

## A. Çalıştığı görülen ve korunacak akışlar

| Yaklaşık zaman | Cihazda görünen sonuç ve sınırı |
| --- | --- |
| 00:00–00:15 | Ayarlar sayfasının alt ve üst kısımları; yalnız **Premium ve Cüzdan** satırının açık mavi/mavi olduğu, diğerlerinin beyaz kaldığı görülüyor. Keşfet arama açılıyor, geri dönülüyor; Sesli sekmesi açılıyor, kapalı oda boş durumu `Henüz açık sesli oda yok` yazıyor. |
| 00:17–00:35 | `Sesli oda oluştur` sayfası açılıyor. Kategori, başlık (80 karakter), herkese açık/takipçi/arkadaş kitlesi ve mor `Sesli odayı başlat` düğmesi görünür. Oda başlığı yazılıp başlatılıyor; uygulama odaya geçiyor. |
| 00:36–00:48 | Oda sahibi arayüzünde `SESLİ CANLI`, `1/12 konuşmacı`, `2. kişi bekleniyor`, sayaç, sahibin avatarı, sahne yuvaları, Dinleyiciler/Tepki/Davet, mikrofon ve Bitir yer alıyor. `Odaki kişiler` paneli açılıyor, yalnız yönetici hesap görünüyor. Başka dinleyici yokken 1/12 ve 2. kişi bekleniyor hata sayılmaz. |
| 00:48–01:02 | Kalp tepkisi ekranda görülüyor. Davet panelinde **üç kişi seçiliyor**, düğme `3 sohbete gönder` olarak güncelleniyor; işlemden sonra `3 sohbete gönderildi` bildirimi çıkıyor. Seçim sayısı ve bildirim tutarlı; **karşı kullanıcıların mesajı alması ayrıca doğrulanmadı**. |
| 01:04–01:22 | Oda sohbetinde metin gönderiliyor, iki ayrı gönderi sohbet balonu olarak görünüyor; mikrofon düğmesi `Mikrofon açık`/`Mikrofon kapalı` şeklinde değişiyor. Bu, başka cihazda sesin duyulduğunu kanıtlamaz. |
| 01:23–01:35 | `Müzik` paneli açılıyor, ses düzeyi ayarı ve NgelX Müzik Kütüphanesi / bağımsız sanatçılar / lisanslı katalog seçenekleri açılıyor. Gerçek bir parça `Seç` ile odaya ekleniyor; parça başlığı oda ekranında ve başarı bildiriminde görünüyor. Dinleyicinin sesi işittiği doğrulanmadı. |
| 01:36–02:04 | Oda sürerken Akış, Keşfet, Sohbet ve Ben ekranlarına geçiliyor; oda başlığı/süre içeren sabit mini bar üstte kalıyor. Akış'ta ilk video kısa siyah spinner gösteriyor fakat ardından videolar oynuyor. Sohbet içinde önceki yazışmalar ve `SESLİ ODA / AKTİF / Katıl` paylaşım kartı görünüyor. Mevcut oda kaybolmuyor. |
| 02:05–02:17 | Mini barla odaya geri dönülüyor. `Oda müziği` panelinden ses düzeyi değiştiriliyor ve müzik duraklatılıyor; `Müzik duraklatıldı` metni görünüyor. Daha sonra oda Bitir ile sonlandırılıyor; `Bu sesli oda sona erdi` ekranı geliyor. |
| 02:18–02:23 | Oda bittikten sonra Keşfet/Sesli sekmesine dönülüyor, açık oda yok boş durumu gösteriliyor. **Bu sırada oda zaten bitmiş olduğundan boş liste normal.** |

## B. Öncelikli sorunlar ve tasarım eksikleri

### P0/P1 – Oda oluşturma kategori çiplerinde kontrast bozukluğu (00:18–00:33)
- `Sohbet / Müzik / Teknoloji / Spor / Gündem` kategorilerinin **seçili olmayanları siyah zemin + çok koyu yazı** ile gösteriliyor, okunması çok güç. Seçili kategori lavanta/mor ve okunabilir.
- Build 403'te kategori yazılarının rengi kodda koyu ayarlanmışken, seçili olmayan `ChoiceChip` tema arka planı siyah kalmış olabilir. Kök neden kod incelemesiyle doğrulanmalı; görsel hata ise videoda nettir.
- **Kabul kriteri:** Tüm çipler açık beyaz/lavanta zeminde yüksek kontrastlı koyu yazı; seçili çip mor zemin veya lavanta arka planla net işaretlenmiş olsun. Dar ekran/sistem açık-koyu temasıyla test; mevcut kategori değerleri ve oda oluşturma işlevi korunacak.

### P1 – Söz istekleri ekranının davranışı bu videoda sınanmadı
- `İstekler` kontrolü oda içinde görünüyor (ör. 00:36–00:42, 01:12–01:21, 02:09). Ancak kullanıcı bu kontrolün panelini **açmıyor**.
- Bu nedenle önceki videoda uzun spinner gösteren panelin Build 403'te `7 sn sonra açıklama + Yeniden dene` durumunu verdiği kanıtlanmıyor. **Düzeltildi/bozuk** diye kesin hüküm verme.
- Sonraki cihaz testi: paneli açıp 10–15 saniye bekle; istek yok, yavaş sorgu ve hata durumlarını, başka bir cihazdan söz isteme/izin verme/ret sonuçlarını ölç.

### P1/P2 – Akış videosunda ilk yükleme gecikmesi (01:36–01:39)
- Oda mini barı ekranda kalırken açılan ilk Akış videosunda siyah spinner var; ancak daha sonra gerçek görüntü ve diğer videolar oynuyor.
- Önceki videodan farklı olarak uzun süren kalıcı açılmama bu kayıtta kanıtlanmıyor. Video hazır olana kadar kapak resmi, süreli bekleme ve gerekirse retry; oda sesiyle medya sesinin karışma/düşürülme mantığı iki cihazda ayrıca test edilmeli.

### P2 – Sesli oda içi düzen ve bilgi hiyerarşisi
- `2. kişi bekleniyor` için sarı şerit ekranın üstünde çok alan kaplıyor; oda başlığı/süre/aktif mikrofon/katılımcı sayısı tek kompakt özet kartında gösterilebilir.
- Görünen ilk üç sahne yuvası büyük ve geri kalan dokuz koltuğun nasıl açıldığı anlaşılmıyor. Gerçek 12 kişilik kapasite veya izinleri değiştirmeden yatay kaydırma/diğer konuşmacılar açıklaması geliştir.
- `Dinleyiciler / Tepki / Davet / Müzik / İstekler` kontrolleri dağınık; tek bir eylem çubuğunda anlamlı gruplara ayrılabilir. Mikrofon açık/kapalı metni belirgin, bu korunmalı.
- Oda adı emoji içerdiğinde taşma için 320–400dp, büyük metin/ekran okuyucu testleri yapılmalı.
- Oda oluştur ekranının alt yarısında boş alan yoğun; yardım metni ve örnek kullanım bilgisiyle denge, fakat çalışma akışını kalabalıklaştırma.

### P2 – Davet paneli ve sohbet UX
- Üç seçili kişi ve başarılı 3 sohbete gönder bildirimi tutarlı; göndermeyi yalnız seçilen UID'ler için yapmak ve iki hesapla karşı tarafta `Katıl` kartını test etmek gerekiyor.
- Sohbet klavyesi geldiğinde giriş alanı alt güvenli bölgede kalıyor; buton ve mesaj listesi daha küçük cihazda, büyük fontta ve yatay döndürmede test edilmeli.

### P2 – Oda müziği görünümü / veri sınırları
- Parça seçme/duraklatma ve ses yüzdesi arayüzde doğru görünüyor, müziğin gerçekten 2. kullanıcıya aktarıldığı bilinmiyor.
- Kütüphanedeki `Lisanslı katalog`, gerçek hak/abonelik durumuna bağlanmalı; kategoriler ve `Seç` düğmeleri açık/metin-kontrastı korunmalı.

## C. Özellikle hata sayılmayacak görüntüler
- Oda henüz açılmadan ve oda bittikten sonra `Henüz açık sesli oda yok` yazması.
- Tek kişi varken `1/12 konuşmacı`, `2. kişi bekleniyor` ve yalnız adminin görünmesi.
- Kullanıcı kendi hesabıyla oda davetlerini gönderiyor; bu alıcılarda gerçek teslim kanıtı değildir.
- Mini bar sürerken ilk birkaç kare siyah olan Akış videosunun sonradan açılması, kalıcı oynatma hatası değil açılış performans notudur.

## D. Korunacak ve sonraki Work paketi
- **Korunacak:** oda oluşturma, başlık/kategori/gizlilik değerleri, LiveKit bağlantısı, odadaki konuşmacı/dinleyici durumu, mikrofon değişimi, tepki, oda sohbeti, 3 kişiye davet, müzik seçim/kütüphane/duraklatma, oda mini barı, odadan ayrılma/bitirme, Beşli navigasyon, sadece Premium ve Cüzdan ayar satırının mavi vurgusu.
- **Öncelik:** Kategori çiplerinde siyah üzerine koyu yazıyı düzelt; ardından Söz İstekleri panelini gerçek cihazda tekrar test et; Akış'ı oda açıkken medya süreleriyle ölç; sonra sesli oda ekranını referans tasarım diline göre sadeleştir.
- **İki cihazlı test:** Diğer hesap Keşfet/Sesli sekmesinden odanın aktifken keşfedilebilmesi, `Katıl` daveti, izinli kullanıcının giriş/mikrofon/söz isteme, gerçek ses/müzik karışımı.
- **Durum:** Bu belge yalnız video QA notudur; uygulama koduna dokunulmadı, Build 404/APK üretilmedi.
