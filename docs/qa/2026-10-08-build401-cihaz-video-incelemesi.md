# NgelX Build 401 — gerçek cihaz video incelemesi (2026-10-08)

**Kaynak:** Kullanıcının bu sohbet içinde paylaştığı `45050.mp4`, yaklaşık **03:52** ekran kaydı, Android cihaz; Build 401, önceki Build 400 üzerinde kurulmuş.
**Tasarım hedefi:** Kullanıcının kapaklı, mor-mavi, beyaz alt menülü **Ben** ekranı referansı. Mevcut gerçek kullanıcı içerikleri korunur, görsel referanstaki sahte/örnek gönderi ve hikâyeler kopyalanmaz.

> Görünüm/açılış, başarılı veri yazma, iki hesaplı işlev testi ve üretim güvenilirliği aynı şey değildir. Yalnızca videoda gözlenen davranışlar «cihazda geçti» diye işaretlendi.

## 1 — Cihazda gözlenen olumlu sonuçlar / çalışırken koru

| Zaman | Bölüm | Kanıt ve sınır |
|---|---|---|
| 00:04–00:06 | **Kapak fotoğrafı menüsü** | `Kapak fotoğrafı`, `Galeriden seç`, `Kapağı yeniden konumlandır`, `Kapak fotoğrafını kaldır` etiketleri artık **siyah/koyu ve okunabilir**. Build 400'deki beyaz üzerine beyaz sorunu giderilmiş görünüyor. |
| 00:07–00:24 | **Kapak fotoğrafı** | Sistem fotoğraf seçicisi açılıyor, resim seçiliyor, yatay kapak önizlemesi açılıyor, konum yukarı kaydırılıyor (kadraj -100%), Kaydet ile profil kapağı gerçekten güncelleniyor. Eski R2 `invalid_kind` hatası bu videoda görülmedi. |
| 00:00–00:45 | **Profil** | Kullanıcı adı, biyografi, avatar, kapak, katılma tarihi, konum satırı, dört sayaç (Takip, Takipçi, Etkileşim, Arkadaşlar), düzenleme/arkadaş butonları, üst ikonlar, gerçek tanıtım videosu kartı, üç sütunlu gönderi küçük resimleri görülüyor. |
| 00:24–00:44 | **Tanıtım videosu** | Daha önce yüklenmiş gerçek video önizlemesi, oynatma ve ses simgesi, `Tanıtım videosunu değiştir` eylemi görünüyor; yükleme/değiştirme işlevinin tamamlanması test edilmedi. |
| 00:32–00:40 | **Arkadaşlar** | İki arkadaşı gösteren liste, takip/öneriler/ortak noktalar sekmeleri açılıyor; gerçek arkadaşlık yönetiminin değiştirilmesi test edilmedi. |
| 00:46–00:57 | **Kaydedilenler** | Üç kayıt görülüyor; uzun basmayla `Kaydedilenlerden kaldır` paneli açılıyor, işlem yapıldıktan sonra liste **üçten ikiye iniyor**. Kalan bir kayıt tam ekran video olarak açılıyor. Kaydetme/kaldırma mantığı korunmalı. |
| 01:00–01:26 | **Hikâye** | Var olan hikâye gösteriliyor; yeni video hikâye yayınlanıyor, `Hikâyen 24 saat boyunca yayında` başarı mesajı beliriyor. Seçenekler alt panelinin yazıları okunuyor: `Hikâyeyi paylaş`, `Öne çıkanlara ekle`, `Arşive taşı`, `Hikâyeyi sil`, `Kapat`. `Hikâye arşive taşındı` başarı mesajı görülüyor. Gerçek üçüncü kişiye paylaşma testi yapılmadı. |
| 01:31–01:46 | **Hikâye oluşturma** | `Yeni hikâye` altında galeri fotoğraf/video ve kamera fotoğraf/video seçimleri açılıyor; görsel seçiminden sonra `Hikâyen 24 saat boyunca yayında` sonucu çıkıyor. |
| 01:59–02:21 | **Profili Düzenle** | Görünen ad/kullanıcı adı/biyografi/konum düzenleme paneli açılıyor; biyografi değiştirildikten sonra `Profilin güncellendi` mesajı ve yeni biyografi profil sayfasında görülüyor. Korunmalı. |
| 02:24–02:52 | **Sohbet** | Gelen Kutusu: Tümü, Gruplar ve arama; mevcut üç grup listeleniyor, `se` araması filtreli sonuç gösteriyor, `ro` ile boş sonuç durumuna geçiyor, arama temizlenince gruplar dönüyor. Sağ üst `+` menüsü Yeni sohbet/Grup oluştur/Gruba katıl/Arşivlenen sohbetler seçeneklerini gösteriyor. Grup oluşturma/gönderme test edilmedi. |
| 02:56–03:28 | **Üret → Akış** | Üret sayfası açılıyor; fotoğraf kamerası açılıyor, çekim yapılıyor, önizleme Üret ekranına geliyor, medya aktarma ilerlemesi %100'e ulaşıyor; `Paylaşım yayınlandı, Akışta ve profilinde görünecek` onayı görünüyor ve yeni fotoğraf Akış üstünde görüntüleniyor. **Profildeki yeni gönderiyi açıp kontrol etme bu videoda yok.** |
| 03:30–03:52 | **Yorum/etkileşim** | Yorum paneli açılıyor ve yükleniyor; metin yazılıp gönderildiğinde yorumlar görünüyor. Kalp/tepki ve uzun basma menüsü açılıyor; yorum silme onay penceresi `Yorum silinsin mi?` olarak açılıyor. Nihai yorum-silme sonucu ayrıca doğrulanmalı. |
| Genel | **Alt navigasyon** | Beş sekme (Akış, Keşfet, Üret, Sohbet, Ben) mevcut, **beyaz alt zemin** ve mor seçili renk Build 401'de görünüyor. Eski siyah alt menü sorunu giderilmiş. |

## 2 — Referans tasarıma göre açık eksikler (gözlem, kodda henüz çözülmedi)

**P1 — Üst profil düzeni tam referans değil.** Referansta avatar kapakla örtüşürken ad/@kullanıcı adı avatarın sağında, yatay hizada. Build 401'de ad ve kullanıcı adı avatarın altına ortalanıyor; buna göre üst bölüm uzun, görsel yoğunluk ve boşluk dengesi farklı. Var olan avatar/kapak veri ve fotoğraf değiştirme işlevlerini koruyarak sadece yerleşimi iyileştir.

**P1 — İstatistik kartı eksik.** Build 401 dört mor ikon ve sayıları gösteriyor (ilerleme), ancak referanstaki tek açık-mor arka planlı, bölücülü yatay kart görünümü yok. Sayaç sorgularına dokunmadan kart/sütun ayırıcılarını ekle.

**P1 — Öne çıkan hikâye koleksiyonları referanstan farklı.** Videoda `Yeni` ve `Video` daireleri var; kapak resimli öne çıkan albüm alanı ve isimlendirme/boş durum görünümü referans kadar gelişmiş değil. Gerçek hesapta `İstanbul/Seyahat/Doğa/Yaşam` verileri olmadığı sürece örnek içerik oluşturma.

**P1 — Tanıtım videosu kartı hedefe tam uymuyor.** Başlık, açıklama, gerçek video önizlemesi ve değiştir eylemi mevcut, fakat referanstaki solda metin/sağda küçük video önizlemesi yerleşimi ve süre etiketi eksik. Mevcut video oynatma ve medya bağlantısını değiştirmeden hizala.

**P1 — Alt navigasyondaki Üret butonu.** Alt zemin artık beyaz, beş sekme yerinde; fakat referanstaki büyük ve belirgin yuvarlak mor-mavi Üret butonu yerine küçük mor hap/ikona benzer kontrol var. Buton tıklama rotası korunarak görsel ölçü geliştirilmeli.

**P2 — `Arkadaş Ekle` etiketi kesiliyor.** İnce ekranlı cihazda ikinci küçük buton hâlâ `Arkadaş ...` şeklinde kısalıyor; önceki iki satırlı kırılma kesmeyle değişmiş, fakat referanstaki tam etiket okunamıyor. İkon/etiket ölçüsü ve buton oranları düzeltilmeli.

**P2 — Kısayol satırındaki uzun etiketler kısalıyor.** `Kaydedilenler` gibi menü adları `Kaydedilen...` görünüyor; tek/iki satırlı esnek dizilim ve etiket boyutu ekran genişliğine uygun hale getirilmeli.

**P2 — Profil içerik sekmeleri.** `Gönderiler`, `Reels`, `Hikâyeler`, `Kaydedilenler` görünüyor; `Etiketlenenler` sağa kaydırılan bölümde kalabilir, bu videoda ayrıca açılıp test edilmedi. Beş sekmenin tamamını gerçek veriyle açarak doğrula; hiçbiri kaldırılmasın.

**P2 — Kapak/avatarın yavaş yeniden çizilmesi.** 01:39–01:44 arasında avatar üzerinde birden fazla kare boyunca yükleme göstergesi dönüyor. Kapak görseli daha sonra korunuyor. Yavaş ağ için mevcut resim/placeholder'ı tutma, gereksiz yenilemeleri azaltma ve hata durumunu açık gösterme değerlendirilsin.

**P2 — Medya/yükleme akışında geçici siyah panel.** Hikâye açılışı/yeniden paylaşımında ve kaydedilmiş video ilk açılırken kısa siyah spinner; yorum paneli 03:30 açılışında kısa boş bekleme görülebiliyor. Video sürekli hata vermiyor; **performans/yükleme UX notu**, kritik bozukluk diye etiketleme.

## 3 — Bu videoda test edilmeyen işlevler (çalışıyor varsayma)
- Üst sağdaki tüm profil ikonlarının uçtan uca davranışı (arama/bildirim/ayarlar/üç nokta).
- Kapak fotoğrafını kaldırıp R2 nesnesini güvenle temizleme; **test amacıyla mevcut kapağı silme**.
- Profil fotoğrafını yeni fotoğrafla değiştirme.
- Hikâyeyi başka bir hesaba özel mesaj olarak gönderme / Android dış paylaşımı ve karşı kullanıcı teslimi.
- `Öne çıkanlara ekle` sonrasında profil albümünde görünürlük.
- Bütün beş profil içerik sekmesinin ve Reels/etiketlenenler verisinin test edilmesi.
- Yeni içerik profil gridinde gerçek görünümü.
- Arkadaş kaldırma/takipten çıkma, grup oluşturma ve grup mesajları, gelen istekleri farklı hesaptan kabul etme.
- Farklı hesaptan gönderi yorumunun görüntülenmesi ve yorumun silinmesinin son veride doğrulanması.
- Diğer dil ayarları / ekran okuyucu / çok küçük cihaz görüntüsü.
- Tek cihaz kaydı kapsamından hiçbir otomatik test veya APK başarısı çıkarımı yapılmaz.

## 4 — Koruma / sonraki Work sözleşmesi

- **Sakla:** Build 400'de düzeltilen `kind:'profiles'` kapak yükleme yolu, kapak yeniden kadrajlama, profil bilgilerini kaydetme, avatar, takip/arkadaş sayaçları, arkadaş listesi/ortak noktalar, gerçek tanıtım video kartı/oynatma, hikâye yayınlama ve arşive taşıma, kaydedilenleri kaldırma, gelen kutusu filtre/arama, kamera/Üret/akış gönderme, yorum yazma/tepki menüsü, 5 sekmeli alt navigasyon.
- **Görsel değişiklikleri izole et:** data modellerini/Firestore güvenlik kurallarını/çalışan Firebase–R2 yollarını rastgele değiştirme. Demo içerikle boş alan doldurma.
- **Öncelik:** önce belirgin etiket kesilmeleri ve eksik kart hizalaması, sonra kalan referans bileşenleri; performans sorunlarını ölçümle çöz.
- **Test şartı:** her kod değişikliğinden sonra regresyon + `flutter analyze` + imzalı release APK. Telefon testi geçmeyen özellikleri «cihazda tamamlandı» diye raporlama.
- **Mevcut durum:** bu not sadece gerçek cihaz QA kaydı; **yeni düzeltme APK'si oluşturmuyor**.
