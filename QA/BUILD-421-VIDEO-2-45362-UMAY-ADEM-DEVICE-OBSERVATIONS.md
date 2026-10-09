# NgelX — 2. cihaz videosu: Umay ve Adem (45362.mp4)

**Tarih:** 09.10.2026. **Süre:** 02:27 (147,4 saniye). **Sürüm:** Ayarlar > Uygulama güncellemeleri ekranında **v1.0.196 • Yapı 421** açıkça görülüyor (00:00–00:03).  
**Amaç:** İlk video `45335.mp4` ile birlikte tek toplu Work QA kaydı oluşturmak. **Bu commit yalnız rapor; uygulama kodu ve üretim verileri değiştirilmedi.** Hesapların e-posta/şifrelerini rapora kopyalama.

## Doğrudan kanıtlanan başarılı akışlar

| Zaman | Test | Gözlem | Kapsam sınırı |
| --- | --- | --- | --- |
| 00:00–00:04 | Sürüm doğrulama | NgelX v1.0.196 / Yapı 421 açıkça görünüyor. | Bu video için sürüm belirsizliği yok. |
| 00:04–00:08 | Umay profil / arkadaş | Umay profilinde 1 arkadaş, Arkadaşlar listesinde Adem bulunuyor. | Zaten arkadaş olan çift; yeni arkadaşlık isteği burada gönderilmiyor. |
| 00:15–00:22 | Genel arama + takip | `ade` ile Adem profili açılıyor. “Takip et” işleminden sonra “Takip ediyorsun” görünüyor; Adem'in takipçileri 1'den 2'ye yükseliyor. | Canlı hedef cihazda yeni bildirim görülmüyor. |
| 00:20–00:26 | Arkadaşlık durumunu koruma | Adem profili “Arkadaşsınız” gösteriyor. “Arkadaşlıktan çıkarılsın mı?” onay penceresi açılıyor; sonraki arkadaş listesinde Adem hâlâ görünüyor, yanlışlıkla ilişki silinmemiş. | İsteği gönderme/yeniden arkadaş olma yolu test edilmedi. |
| 00:28–00:46 | Özel sohbet yazma ve ayarları | Umay'dan Adem sohbeti açılıyor; kısa test mesajları mavi giden baloncuk olarak yazılı/gönderilmiş görünüyor; sohbet bilgi/mesaj ayarı açılıyor. | Adem tarafında gelen mesajın karşı hesaba gerçekten teslim edildiği gösterilmedi. |
| 00:55–01:08 | Hesap değiştirme | Hatırlanan 5 hesap görüntüleniyor; Umay'dan Adem hesabına geçiliyor ve Adem'in kendi profilindeki fotoğraf, sayılar ve arkadaşlar listesi geliyor. | Şifre sorulması, başarısız giriş veya başka cihaz testi yapılmadı. |
| 01:08–01:15 | Arkadaşlar / takipçiler | Adem profilinde 2 arkadaş (Umay ve Dilek), 2 takipçi; takipçi listesinde Umay görülüyor. | İki hesap arasında Umay'ın takibi ve arkadaşlık kaydı tutarlı görünüyor. |
| 01:19–01:26 | Profil görünümü ayarları | Profil düzenle sayfasında hem kapaklı hem kapaksız seçeneği açılıyor, önizleme kartları çalışıyor. Seçim daha sonra **yeniden kapaklıya çevrilerek** kaydediliyor ve kapaklı profil görünüyor. | Kapaksız modu kaydedip karşı hesaptan görüntüleme bu videoda gerçekleşmedi; bunu geçilmiş test sayma. |
| 01:36–01:46 | Global arama | `uma` ile Umay ve `ade` ile Adem kişi sonuçları görülüyor. | Belirli kısa isimler çalışıyor; tüm hesap arama varyantları garanti değil. |
| 02:04–02:14 | Gelen Kutusu > İstekler | Başlangıçta **3 bekleyen istek** görünür. Dilek'in eski arkadaşlık isteği reddedilince sayaç **2**, Adem'in eski takip isteği kabul edilince **1** oluyor. İşlem sonuç mesajları doğru görünüyor. | Bunlar daha önceki (1 gün önce) kayıtlar; bu videoda gönderilen yeni istek değil. |
| 02:24–02:27 | Umay profil sonuç | Umay profilinin takip/takipçi sayıları 1/1, arkadaş sayısı 1. | Önceki kabul ve takip akışlarının profil sonucuyla uyumlu. |

## Gerçek düzeltme / inceleme adayları

| Zaman | Şiddet | Sorun veya şüphe | Gerekçe ve çözüm önceliği |
| --- | --- | --- | --- |
| **00:04–00:13, 01:04–01:18, 02:24** | **ORTA — görsel kusur** | **Profil sahibinin katılım tarihi kesiliyor:** “Ekim 2026 tarihinde…” / “Eylül 2026 tarihinde…” | Build421 tarih metninin doğru biçimi mevcut; fakat konum + katılım bilgisinin yan yana dar yerleşimi tamamını göstermiyor. Tarihi ayrı satıra geçir veya kırılabilir/çok satırlı alan ver, sağdan taşmayı önle; yeni tarihi hesaplama mantığını değiştirme. |
| 00:17–00:20, 01:48–01:52 | DÜŞÜK/UX, izle | **Ziyaretçi profil sayaçları ve sosyal düğmelerin ilk yüklemesi** birkaç saniye dairesel göstergelerle geliyor. | Sonrasında 2/2 ve “Arkadaşsınız” gibi değerler düzgün; kalıcı veri yüklenmeme kanıtı yok. Sıçramasız skeleton/tek yükleme iyileştirmesi değerlendirilebilir. |
| **01:40–01:43** | **BELİRSİZ/İNCELE** | Umay'ın `uma` aramasından açılan profil ekranında sayaçlardan sonra doğrudan “Gönderiler / Reels / Etiketlenenler” görünüyor; **takip/mesaj/arkadaş düğmeleri bu görünümde yok**. | Sayfa başka bir profil önizleme yüzeyi mi, gizlilik/ilişki durumuna göre mi gizleniyor; kaynak UI ve tekrar testle ayrıştırılmalı. Tek bir kareyle kesin bug denemez. |
| 00:12, 01:00, 01:32–01:35 | DÜŞÜK/UX, izle | Video/akış geçişlerinde ortada kısa süre dairesel ağ yükleme göstergesi var. | Ağ veya sayfa ön-yükleme gecikmesi olabilir; kalıcı boş ekran kaydedilmedi. |

## Bu videoda test edilmedi / testin sınırları

- **Yeni arkadaşlık isteği:** Umay ile Adem zaten arkadaş. Yeni istek gönderme, diğer hesapta görme ve aynı anda kabul test edilmedi.
- **Hikâye yanıtı:** Bu videoda görülmüyor; ilk video `45335.mp4` sonundaki “Hikâye yanıtı gönderilemedi” hatası açık öncelik olmaya devam ediyor. İlk videonun sürüm numarası ayrıca belirsiz.
- **Hikâye başlangıç ve bitiş paneli:** Gösterilen koyu video Akış videosu; yeni hikâye paneli/saatleri bu videoda doğrulanmadı.
- **Kapaksız profilin kaydedilmiş hâli:** Kapaksız görünüm seçildi ancak **yeniden kapaklı** seçilip kaydedildi; kapaksız profil cihazda doğrulanmış sayılmaz.
- **Mesajın karşı hesapta okunması/teslimi:** Giden baloncuklar var; Adem gelen kutusunda aynı yeni mesaj açılıp gösterilmiyor.
- **Yeni takip bildirimi alıcıya ulaştı mı:** Takip sayaçları tutarlı; anlık bildirim varış ve ses testi kayıtta yok.
- **İstek geri çekme:** Var olan isteği iptal etme ve sonra alıcıda kaybolduğunu görme yolu test edilmedi.
- **Profil fotoğrafı yenileme:** Bu kayıtta gerçek fotoğraf değiştirme ve diğer hesapta yenisinin belirmesi yok.

## İlk video ile birleşik Work öncelikleri

1. **P1 — hikâye yanıtı başarısızlığı** (Video1 02:28–02:33, açık hata mesajı): gerçek Build421'de aynı akışı tekrar et, Firestore/durum/gizlilik açıklamasıyla hata kodunu yakala. Karşı hesapta mesaj teslimi doğrula. Videodan kök nedeni kesinleştirme.
2. **P2 — profil sahibinin katılım tarihi satır sonundan kesiliyor** (Video2): yeni Build421 biçimi doğru olmasına rağmen dar metadata satırında taşma; kapaklı/kapaksız sahibi ve ziyaretçi için kayıpsız metin düzeni.
3. **P3 — kapak fotoğrafını değiştirme siyah etiketi görseli çok örtüyor** (Video1); eski işlevi koruyarak küçük kamera simgesi veya yumuşak kaplama.
4. **P3 — profil açılırken yükleme göstergeleri / düzen sıçraması** (Video1 + Video2); kalıcı veri hatası değil, yalnız UI iyileştirmesi.
5. **Doğrulanacak şüphe — `uma` profil aramasında sosyal düğmelerin görünmediği ayrı profil görünümü** (Video2 01:40–01:43).
6. **Cihaz QA açık:** yeni arkadaşlık isteği/karşı hesap bildirimi, profil güncelleme, kapaksız görünüm, hikâye zaman paneli, mesaj karşı hesap teslimi, istek iptali.

**Uyarı:** Bu dosya, gerçek cihaz videosunun gözlem kaydıdır. Kod değişikliği yapılmadı, açık fonksiyonlar “tam düzeldi” sayılmadı.
