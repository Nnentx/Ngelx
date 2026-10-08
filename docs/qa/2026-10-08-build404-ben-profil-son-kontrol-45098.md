# NgelX Build 404 — Ben/Profil SON cihaz testi (`45098.mp4`)

**Tarih:** 2026-10-08. **Kaynak:** Kullanıcının gönderdiği 136,09 saniyelik (1080×2392) Android ekran videosu. **Uygulama sürümü:** Ayarlar > Uygulama güncellemeleri satırında `v1.0.180 • Yapı 404` görülüyor (0–3 sn). **Amaç:** Eski Build 403 profil QA'sından sonra son açık eksikleri, tasarım durumunu ve korunacak akışları kaydetmek. **Bu belge yalnız QA kaydıdır; kod/derleme/cihaz üzerinde uzaktan değişiklik yapmaz.**

## A. Gözlenen ve KORUNACAK çalışan özellikler

| Süre (yaklaşık) | Gözlenen davranış |
| --- | --- |
| 0–5 sn | Ayarlar ve gizlilik ekranı; Build 404 sürüm etiketi; yalnız `Premium ve Cüzdan` açık mavi satır olarak duruyor, diğer ayarlar mor ikon/beyaz kart. Üst kısımda hesap/gizlilik sayfaları yerinde. |
| 4–17 sn | `Ben` profili: Gerçek kapak ve avatar, kullanıcı adı/isim, biyografi, şehir, katılma tarihi, dört istatistik (Takip/Takipçi/Etkileşim/Arkadaşlar), `Profili Düzenle` ve `Arkadaş Ekle` butonları, gerçek `00:40` tanıtım videosu, beyaz kısayollar, hikâye balonları, beşli alt navigasyon görüntüleniyor. |
| 17–25 sn | `Tanıtım videosunu değiştir` alt paneli okunur olarak açılıyor. Sistem galeri seçicisi açılıyor. Seçici telefonun/sistemin arayüzüdür, NgelX temasıyla bire bir uyuşması gerekmiyor. |
| 25–53 sn | Profil kapağı, avatar ve tanıtım videosu gösteriliyor. Yeni tanıtım video kaydı için `Profil tanıtım videosu kaydedildi` bildirimi görünüyor; mevcut medya/biyografi/istatistikler kaybolmuyor. |
| 60–70 sn | Kullanıcı Android ana ekranına çıkıp uygulamayı yeniden açıyor; beyaz NgelX splash, yeniden profil. Bu hareketin kendisi **uygulama çökmesi kanıtı değildir**. Yeni tanıtım video önizlemesi önce yükleniyor, sonra **gerçek `00:34` süreli yeni içerik** gösteriliyor. |
| 70–76 sn | Yeni video oynuyor, süre `00:34` doğru görünüyor; videonun üstündeki ses aç/kapat düğmesi mevcut; profil kısayolları ve 4 istatistik korunuyor. |
| 77–94 sn | Profil `Yeni` hikâye menüsünden sistem galerisi açılıyor, gerçek görsel seçiliyor. `Hikâyen 24 saat boyunca yayında` bildirimi görülüyor; hikâye görüntüleyicisi açılıyor ve resimli/video hikâyeler arasında ilerliyor. |
| 94–101 sn | Hikâye görüntüleyicisi üstte dört parçalı ilerleme çubuğu, kullanıcı etiketi, süre, görüntülenme/yorum/tepki simgeleri gösteriyor. Bazı hikâyelerde siyah yükleme ekranı var, sonra medya gösteriliyor. |
| 102–118 sn | `Kaydedilenler` listesinde gerçek tek video kapağı görünüyor; videoya dokunulunca NgelX paylaşımı açılıyor, gerçek görüntü oynuyor, tekrar listeye dönülüyor. Build 403'teki çoklu uzun gri-placeholder durumu **bu örnekte tekrarlanmıyor**. Kayıt silme bu videoda test edilmedi. |
| 120–129 sn | `Gizlilik` ekranında `Gizli hesap`, `Profilimi kimler görüntüleyebilir?`, `Aktiflik durumu`, `Profil paylaşımını arkadaşlarla sınırla`, `Yorumları arkadaşlarla sınırla`, `Gizli kelime filtresi`, `Engellenen hesaplar`, `İstek geçmişi` seçenekleri açılıyor. |
| 129–136 sn | Ayarlara ve ardından profil/akışa dönüş; alt gezinti ve gerçek gönderilerin oynatılması korunuyor. |

## B. Önceliklendirilmiş SON eksikler / belirsizlikler

### P1 — Hikâyeden hikâyeye geçişte siyah spinner (yaklaşık 95–101 sn)
- Dört hikâyelik görüntüleme sırasında bazı içeriklerde tamamen siyah ekran + ortada dönen beyaz spinner görülüyor; diğer hikâyeler gerçek fotoğraf/video olarak açılıyor.
- **Başarısız içerik varsayma:** Birkaç medya sonradan yüklendiğinden “hikâyeler bozuk” veya “sunucuda dosya kayıp” sonucu çıkarma.
- Sonraki kod işi: hikâye viewer'a **önceki/sonraki medya ön yükleme**, varsa gerçek poster/thumbnail ile skeleton, süre ölçümü, ağ/decoder hatasında açık `Tekrar dene` ve ilerleme çubuğunun yükleme boyunca yanlış tüketilmemesi. Tarih/zaman bilgisi ve gerçek medyanın kendisi korunmalı.
- Test: art arda 4+ hikâye (foto+video), ilk giriş ve geri giriş, zayıf mobil veri, offline→online.

### P2 — Tanıtım video önizlemesi kaydetme ve soğuk başlatma sonrası gri/loading (53–70 sn)
- **Olumlu:** 00:40 eski video başarıyla **00:34 yeni videoya** dönüşüyor, yeni video uygulama yeniden açıldığında görüntüleniyor. Önceki Build 403'teki düzeltme iş görüyor.
- **Süren eksik:** Yeni kayıt sonrası kısa siyah/placeholder, profil yüklenirken ve soğuk başlangıçta gri oynatıcı önizlemesi/loader, birkaç saniyelik görsel boşluk.
- Sonraki kod işi: kaydetme sonrası yeni URL/generation key ile eski video controller'ını düzgün dispose et; yerel son-kare/poster kullan; önizleme cache'i; medya init timeout/yeniden dene korunacak. **Kaydı tekrar tekrar başlatma**, sahte başarı veya gerçek medyayı silme yapma.
- Test: 1 video değiştir, ekrandan ayrıl-dön, uygulamayı elle kapat-aç; 00:34 gerçek süre ve oynatma devam etmeli.

### P2 — Avatar/kapak fotoğrafının kısa süre yeniden hazırlanması (yaklaşık 33–50 ve 65–90 sn)
- Profil fotoğrafında dönen ince yükleme işareti, uygulama yeniden açıldığında ilk birkaç kare üst kapakta beyaz/boş görünüm görülüyor; ardından gerçek kapak/avatar geri geliyor.
- Sonraki kod işi: ağ resmi cache, eski görüntüyü yeni görüntü gelene kadar tutma, gereksiz refetch/rebuild sayısını azaltma; kapak/avatar yükleme başarısız olursa anlamlı tekrar deneme. Bu videoda **kalıcı fotoğraf kaybı kanıtı yok**.

### P2 — Gizlilik ayarlarının anlaşılır olması ve doğru sunucu etkisi (120–129 sn)
- `Gizli hesap` AÇIK; `Profilimi kimler görüntüleyebilir?` altında `Herkes` SEÇİLİ. Bu iki kavram *ayrı kontrol* olabilir (takip isteklerini onaylamak vs profili görüntüleme), dolayısıyla **kesin hata değildir**.
- Kullanıcıya kısa açıklama: `Gizli hesap yeni takipçilere onay gerektirir` ile `profili kimler görebilir` ayarının birlikte sonucu. Sunucu erişimini **iki gerçek hesapla** doğrula (anonim/takipçi/arkadaş).
- `Gizli kelime filtresi` AÇIK iken `Henüz kelime eklenmedi` yazıyor. Etkinin boş kelime listesinde olmadığı açıkça gösterilebilir; düğmeyi kendi kendine kapatma, kullanıcı seçimini bozma.

### P3 — İnce tasarım/etiket düzeltmeleri
- Profil kısayollarında `Kaydedilenler` etiketi iki satır ve diğerlerinden daha dar; dar ekran/dinamik fontta tekdüze spacing ve okunabilirlik.
- Sahibi tarafından görüntülenen profilde `Arkadaş Ekle` butonu var. Buton işlevi bu videoda denenmedi; sahibine arkadaş önerme/ekleme mi yoksa arkadaşları yönetme mi olduğu kontrol edilip **doğru CTA etiketi** seçilmeli, işlevsilmeden.
- Video kaydetme sonrası mavi SnackBar birkaç saniye büyük bölümü kaplıyor; küçük ekran ve ekran okuyucuda taşma/zamanlama kontrolü.
- Süre etiketi `00:34` ve `00:40` gerçek player verisiyle tutarlı, kaybolmasın.

## C. Bu videoda **sorun olarak kaydedilmeyecekler**
- 10–13 ve 37–40 saniyelerde görülen dikey ses kontrolü, Android sistem ses panelidir; NgelX tasarım hatası değil.
- 17–23 ve 80–86 saniyelerdeki Fotoğraflar/Videolar/Koleksiyonlar seçici telefonu yöneten Android/galeri arayüzüdür.
- 60–64 saniyede Android ana ekranı, ardından NgelX splash gösterilmesi **manuel uygulama yeniden açılışı**. Videoda kanıt olmadan “kendiliğinden çöktü” diye kaydedilmeyecek.
- Tanıtım videosunun içindeki TikTok işaretleri kaynak medya içeriğidir, uygulamanın eklediği sahte logo değildir.
- Gerçek kullanıcı adı, avatar, kapak, takip/sayılar ve görsellerin örnek tasarımdan farklı olması kusur sayılmayacak.

## D. KORUMA ve gerçek kabul kriteri
1. Başarılı çalışan 00:40→00:34 tanıtım video değişimi, gerçek süre/oynatıcı, avatar/kapak, stat kartı, kullanıcı verisi, Premium mavi vurgu, yeni hikâye paylaşımı, Kaydedilenler video açılması **korunacak**.
2. Düzeltmeler öncelikle **hikâye siyah geçiş spinner** ve medya yükleme gecikmelerine odaklanacak; profili baştan değiştirme.
3. Mevcut kullanıcı hikâyesi/gönderisi/kaydedileni/verileri silme. `Kaydedilenlerden kaldır` ayrı bir aksiyon olmaya devam edecek.
4. Gizlilik ayarlarının gerçek etkisi iki cihazla ve gizli hesap herkese açık profil kombinasyonuyla test edilecek. Sadece arayüzde toggle görünmesi yeterli değil.
5. Bir sonraki kod paketinde regresyon, Flutter analyze, imzalı APK ve Android video testi istenir. **Bu not kodlamanın yapıldığı anlamına gelmez.**

**Kapsam sınırı:** Bu video Ben/Profil, Ayarlar, Hikâye, Kaydedilenler ve bir kısa Akış gezintisidir. Canlı Yayın/Sesli Odalar karşı kullanıcı testleri bu videoyla yapılmadı. Bunlar Build 404 konsolide Work planında açık kalır.
