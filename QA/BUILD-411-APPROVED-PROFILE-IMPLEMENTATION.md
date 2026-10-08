# Build 411 — Onaylanan profil tasarımlarının güvenli uygulama paketi

## Amaç ve kaynak
Kullanıcının görsel olarak onayladığı dört ekran baz alınır:
1. Başka kullanıcının **kapaksız profil görünümü** — büyük ortalı avatar, beyaz zemin, mor detaylar, takip/mesaj/arkadaş/ortak gruplar, 4 sayaç, tanıtım videosu ve gönderiler.
2. Başka kullanıcının **kapaklı profili** — o kullanıcının `coverPhotoUrl` görseli görünmeli; karşı profile edit ikonu eklenmez.
3. **Kendi kapaklı profili** — mevcut gerçek kapak fotoğrafı, fotoğraf değiştirme, istatistikler, arkadaşlar, tanıtım videosu, hızlı kısayollar, hikâyeler ve grid.
4. **Kendi kapaksız profili** — kapak banner'ı olmadan üstte ortalı avatar ve mor motif; alt bölümlerdeki mevcut tıklanabilir işlevler aynen korunur.
5. **Profili Düzenle** — kapaklı/kapaksız seçim, gerçek fotoğraflar, ad/kullanıcı adı/biyografi/konum, değiştir/kaldır, tanıtım videosu, önizleme, Kaydet.

## Gerçek kod
- `tools/apply_build411_profile_appearance.py`: Owner/visitor profiline `profileViewMode` ekler, eski hesaplar için kapak yoksa sade görünüm seçer. Daha önceki kapak, hikâye, canlı yayın, takip, mesaj, engel ve gizlilik kontrollerine dokunmaz.
- `tools/apply_build411_editor_screen.py`: Gerçek Flutter **Profili Düzenle** sayfası. Firebase kullanıcı kaydına `profileViewMode` ve normal profil alanlarını `SetOptions(merge:true)` ile kaydeder. Mevcut kapak ve fotoğraf yükleme işlevlerini kullanır. Katılma tarihi doğrulanmış `createdAt` verisinden gelir, değiştirilemez.
- `tools/check_build411_profile.py`: Tasarımların veri ve işlev koruma kontrolleri; eski Build 395–409 patch ve regresyonları da korunur.
- `.github/workflows/NgelX-BUILD-411-APPROVED-PROFILE-RELEASE.yml`: Firebase emulator güvenlik testleri, Flutter analizi, 1.0.186+411 imzalı APK üretimi.

## Kırılmaması gereken koşullar
- Profil görünüm tercihi **kişiye özel**; izleyici kendi tercihini değil profil sahibininkini görür.
- Gerçek `coverPhotoUrl` varsa kapaklı modda gösterilir; yoksa kırık ya da boş dev banner çıkarılmaz.
- `Kapaksız` seçimi fotoğrafı silmez; sadece üst paneli gizler.
- Kişinin gerçek profil fotoğrafı, kullanıcı adı, tarih, içerik ve sayılar Firestore'dan gelir. Görseldeki örnek sayılar veya örnek fotoğraflar koda sabitlenmez.
- Başka kullanıcının ekranında kendi hesabını düzenleme butonları gösterilmez.
- CANLI rozeti için Build 408'deki aktif yayın doğrulaması, kurucu/yönetici onaylı grup katılımı ve Build 409 arama düzeltmeleri korunur.
- Firestore güvenlik kuralları değiştirilmeyecek ve yeniden dağıtılmayacak.

## Durum
**Kod kaynak yamaları eklendi ve hızlı kaynak uygulama testi geçti.** Tam derleme ve gerçek telefon görsel doğrulaması sonuçlarına göre devam edilecek. Onaylı ekranlarla telefon ekranındaki ince farklar ayrıca rötuşlanacak. Test yapılmadan birebir piksel sonucu veya sorunsuz entegrasyon iddia edilmez.

## Devam kodlaması — görsel faz / güncel düzeltmeler
- Profili Düzenle'den geri çıkınca `profiliGetir()` yeniden çalışır. Kapak kaldırma, fotoğraf/video değiştirme gibi **hemen kaydedilen** işlemler de görünür olur; yalnız `Kaydet` basılması şart değildir.
- `coverPhotoUrl` boş kullanıcıda editor başlangıç seçimi **kapaksız** olur. Fotoğraf eklenmeden kapaklı moda yanlışlıkla kaydetmeye izin verilmez.
- Başka kişinin profilinde intro-video aynı oynatma bileşeniyle takip/mesaj/arkadaş eylemlerinden **sonra** gösterilir.
- Kaynak patch testi geçti: <https://github.com/Nnentx/Ngelx/actions/runs/37850523721>.
- Son değişiklikler için bağımsız Flutter analizi: <https://github.com/Nnentx/Ngelx/actions/runs/37850586007> (sonuç gelmeden geçti sayılmaz).
- APK üretimi bağımsız olarak devam ediyor; <https://github.com/Nnentx/Ngelx/actions/runs/37850523831>. Telefon üstü görsel karşılaştırma hâlâ bekleniyor.

**Güvenli teslim:** Onaylı referans görsellerdeki piksel, boyut, sıralama ve üst menü ayrıntılarını ancak Build 411 kurulup gerçek ekran görüntüleri geldikten sonra kesinleştir. Bu aşamada yalnız kaynak kodu ve CI doğrulaması vardır; gerçek cihazda "birebir aynısı doğrulandı" deme.

## Gerçek telefon QA — 2026-10-09, kullanıcı videosu 45266.mp4 (102 saniye)

**Telefondan görülenler (görsel kanıt):**
- 00:00 Ayarlar uygulama sürümü: **v1.0.186 / Yapı 411**.
- ~00:04–00:12 Rojin Candan'ın kendi **kapaksız** profili görüntüleniyor; ortalı avatar, dört sayaç, içerik grid'i, alt navigasyon var. Profili Düzenle tam sayfa açılıyor.
- ~00:16–00:36 `Profil görünümü` altında **kapaklı / kapaksız** seçenekleri ve alt önizleme kartları görünüyor; kullanıcı seçenekleri değiştiriyor. Gerçek kapak yokken kapaklı modda **“Kapaklı görünüm için önce bir kapak fotoğrafı ekle”** geri bildirimi gösteriliyor.
- ~00:44–01:00 galeri ve kadraj düzenleyici açılıp bir kapak seçiliyor; resim **Profili Düzenle** üzerinde görülüyor. ~01:08–01:16 ana profilde yeni kapak fotoğrafı görünüyor; mevcut arkadaşlar listesi de açılıyor.
- ~01:20–01:36 hesap değişimi / arama ile aynı kişi başka hesap üzerinden ziyaret ediliyor; **diğer kullanıcı profilinde gerçek kapak fotoğrafı** yüklü, dört sayaç, mesaj / takip / arkadaşlık / ortak gruplar ve intro-video görünüyor.
- Ekran kaydında gözle görülür uygulama çökmesi yok.

**Onaylanan görsellerle hâlâ uyuşmayan detaylar (tasarım borcu; düzeltilmeden birebir sayılmayacak):**
1. **Diğer kullanıcı profili**: dört sayı hâlâ ayrı düz yazılar; onaylı görseldeki mor ikonlu, ayıraçlı, tek yuvarlak lavanta kart değil.
2. **Diğer kullanıcı profili**: takip, mesaj, arkadaşlık ve ortak gruplar ayrı iki/üç satıra yayılıyor; onaylı görselde aynı görsel aksiyon barında, daha derli toplu düzen var. Gizlilik/takip/arkadaşlık callbacks *değiştirilmemeli*.
3. **Diğer kullanıcı profili**: tanıtım videosu kartı gerçek olsa da onaylı yan yana açıklama/thumbnail kart görünümünden farklı; oynatma callback'ini koru.
4. **Kapaklı kendi profili**: avatar/ad/kapak geçişi ve üstteki düğmeler referansın aralık ve hizasına tamamen eş değil.
5. **Profili Düzenle**: genel düzen/doğru kontrol alanları mevcut ama üst resim, avatar çakışması, seçim kartları ve önizleme kartlarında ince ölçü / görsel kalite rötuşu gerekiyor.
6. **Fotoğraf ve kullanıcı verileri** dinamik kalmalı; örnek Dilek ekranındaki metin/sayılar koda yazılmamalı.

**Doğrulanmayan noktalar:** kapaksız moda geçilip *kaydedildikten sonra diğer hesaptan* yeniden açıldığında kapak gizlendiği, tüm butonların aksiyonlarının doğru tamamlandığı ve piksel-birebir eşleşme videoda eksiksiz test edilmedi. Bunları geçti diye raporlama. Mor spinner hakkında önceki kullanıcı açıklaması geçerlidir: **bu alanda sorun yok, değiştirme**.

**Takip:** Build 411 işlevsel temel geçti; tasarım ince uyumu için yeni bir Work değişiklik paketi ve yeni APK/telefon testi gerekir.

## Kapaksız görünüm son-kare telefon testi — 45267.mp4 (~49.96 s)

**Video baştan sona, son kareye kadar incelendi.**
- **00:00–00:07 Dilek Akçay kendi profili:** `Profili Düzenle` içinde `Kapaksız sade görünüm` seçildi. Önizleme kartında kapaksız seçenek de seçili görünüyor; kullanıcı `Kaydet` tuşuna bastı, `Kaydediliyor...` geri bildirimi gösterildi.
- **00:08–00:09:** Dilek'in **kendi kapaksız profili** gerçekten görünüyor. Kapak banner'ı yok; ortalı avatar, kullanıcı adı, bio/konum/katılma bilgisi, dört mor ikonlu sayaç (2/4/26/3), Profili Düzenle, Arkadaşlar ve tanıtım videosu kartı var. **Kendi hesapta kapaksız kaydetme/açma GEÇTİ.**
- **00:10–00:14, 00:21–00:24:** Hikâye görüntüleme açılıyor, kısa yüklemeden sonra video hikâye görüntüleniyor ve profile dönüş çalışıyor. Geçici yükleme gösterimini veya eski kullanıcının mor spinner notunu hata diye etiketleme.
- **00:18–00:27:** Kaydedilenler, Arşiv, Hikâyeler, Gizlilik, Ayarlar kısayolları; öne çıkanlar ve üç sütunlu gönderi grid'i kapaksız profil altında görünüyor. Kısayollara tek tek basılıp işlevleri sınanmadı.
- **00:28–00:31:** Hesap değiştirme ekranından Dilek hesabı yerine **Rojin Candan** hesabına geçildi; Rojin satırı `Bu hesap` durumuna geldi. Başka kullanıcıların e-posta adreslerini QA'ya kopyalama.
- **00:32–00:44:** Rojin hesabındayken `r` aramasıyla **Rojin'in kendi** profiline gidildi, profilin **kapaklı** hali ve gerçek fotoğrafları görüntülendi; grid aşağı kaydırıldı. Rojin'in kendi hesabı olduğu için takip/mesaj/arkadaşlık eylemlerinin çıkmaması bu videoda **hata kanıtı değil**.
- **00:45–00:47:** Profil paylaş menüsü açıldı, NgelX içi / diğer uygulamalarda paylaş seçenekleri görüntülendi. Paylaşımın tamamlandığı test edilmedi.
- **00:48–video bitişi (~00:49.96):** Paylaş menüsü kapatıldı, Rojin'in kapaklı profil ekranına dönüldü. **Son kare kontrol edildi.**
- **Gözlenen cihaz sonucu:** Görünür uygulama çökmesi yok, ama kullanıcı işlemlerinin yalnız göründüğü ölçüde doğrulandığını belirt.

**Açık doğrulama:** Rojin hesabından **Dilek Akçay'ın kapaksız profiline** girilmedi. Dolayısıyla **kapaksız görünümün başka hesaba yansıması bu videoda doğrulanmadı**. Sonradan yapılacak çapraz hesap testi: Rojin aktifken Dilek'i arayıp aç; kapağın görünmemesini, fotoğrafın ortalanmasını ve yalnızca ziyaretçiye ait işlem butonlarını doğrula. Şimdilik kullanıcıdan ek test istemek zorunda değiliz.

**Referans tasarım farkı:** Rojin'in ziyaretçi profilini oluşturan ekranında sayaçlar hâlâ düz sayısal satır; onaylı diğer-profil görselindeki mor ikonlu lavanta stats kartı yok. Bu **görsel eksik**; gerçek verileri, gizliliği ve mevcut buton işlevlerini bozmadan tasarım fazında ele alınmalı. Gerçek kullanıcı fotoğrafları/sayıları referans görselden kopyalanmamalı.

**QA sınıflaması:** `Dilek kendi profilinde kapaksız kaydetme: GEÇTİ`; `Rojin kendi profilinde kapaklı görünüm: GÖRÜLDÜ`; `Kapaksız görünümün diğer hesapta gösterimi: TEST EDİLMEDİ`; `Profil paylaş seçenekleri: GÖRÜLDÜ (paylaşım tamamlanmadı)`.

## Cross-account profile choice VERİFİKASYONU — 45268.mp4, 2026-10-09, 78.95 s

**Bu test, 45267.mp4 için yazılan "başka hesaptan kapaksız görünüm test edilmedi" notunu günceller: ARTIK TEST EDİLDİ.**

- ~00:00: ADEM baykar kendi profili kapaksız, mor istatistik kartı ve çalışan alt navigasyon görülüyor.
- ~00:03–00:09: Adem hesabından kullanıcı aramasında **DİLEK Akçay** seçiliyor.
- **~00:10–00:22: Adem (ziyaretçi) → Dilek kapaksız profil GERÇEKTEN açılıyor.** Üstte fotoğraf banner'ı yok; avatar ortada. Gönderiler sekmesi ve 3 sütunlu gerçek paylaşımlar kaydırılıyor. Takip / Mesaj / Arkadaşsınız / Ortak gruplar kontrolü görünüyor. Bu işlemlerin tamamı tıklanıp test edilmiş sayılmaz.
- ~00:25–00:31: Hesap değiştirici ile Adem'den **DİLEK Akçay** hesabına geçiliyor.
- ~00:32–00:45: Dilek kendi profili kapaksız. Profili Düzenle'de görünüm seçimi **Kapaksız sade görünüm → Kapaklı görünüm** yapılıyor, Kaydet seçiliyor.
- ~00:46–00:56: Dilek kendi kapaklı profilini, mevcut fotoğrafları, sayaçları ve intro videosunu görüyor. Ekran görüntüsü paylaşımı Android sistemi üzerinden deneniyor; gerçek sosyal paylaşıma dair kanıt değil.
- ~00:59–01:03: Hesap değiştirme ile **Adem** hesabına dönülüyor; arama Dilek profiline yöneliyor.
- **~01:06–01:19 / SON KARE: Adem (ziyaretçi) → Dilek artık kapaklı olarak açılıyor.** Kapak gerçek fotoğrafla gösteriliyor. Hızlı açılışta gösterilen kısa yükleme animasyonu birkaç saniye sonra kayboluyor; bu konuda kullanıcı daha önce 'mor sorun yok, dokunma' dedi. **Hata sayılmayacak.**

### Build 411 çapraz hesap sonuçları
- Ziyaretçi hesabında kapaksız görünümün yansıması: **GEÇTİ / kullanıcı video doğrulaması**.
- Görünüm kapaklıya değiştirildikten sonra başka hesabın kapak fotoğrafını göstermesi: **GEÇTİ / kullanıcı video doğrulaması**.
- Canlı hesabın profil sahibinin tercihini kullanması: **görsel kanıtla doğrulandı**; Firestore altyapısını değiştirme.
- Bekleyen konu: **piksel/yerleşim bire bir referans uyumu henüz GEÇMEDİ**.

### Kaydedilen tasarım farkları ve kesin gereksinim
Referans resimleri: kullanıcı konuşmasındaki `45247.png` (kapaksız ziyaretçi profil) ve `45230.png` (kapaklı ziyaretçi profil). Bunlar örnek düzen, örnek kullanıcı/avatar ve sayaç verisi gerçeğe kopyalanmayacak.

1. **Kapaksız ziyaretçi:** Avatar daha büyük ve dekoratif mor halka/balonlarla ortalanmalı; isim, bio, aktiflik ve profil bilgisi aynı hiyerarşide.
2. **Kapaklı ziyaretçi:** Profil fotoğrafı kapağın **sol-altını örtecek biçimde taşmalı**; isim/@bilgisi fotoğrafın **sağında** ve bio/tarih aşağıdaki hizada olmalı. Şu anda fotoğraf kapağın altında ortada ve içerik çok aşağı kayıyor; gerçek video bunu gösteriyor.
3. **Her ikisinde** `Takip / Takipçi / Etkileşim / Arkadaşlar` değerleri **mor ikonlu dört bölmeli lavanta kartta**, aynı yükseklik/boşluk ile gösterilmeli. Mevcutta yalnız çıplak 4 sayı ve etiket var; eksik tasarım.
4. **Her ikisinde** takip / mesaj / arkadaşlık / ortak gruplar **tek hizalı aksiyon satırına** göre yerleşmeli; mevcut iki yarım + iki tam satır tasarımla uyuşmuyor. Ancak küçük ekranlarda okunabilirlik ve mevcut çalışan eylemler/gizlilik/engel kuralları korunmalı.
5. Kullanıcının onayladığı görseldeki gibi **Tanıtım videosu açıklaması solda, küçük kapak/oynatıcı sağda tek kart**, ardından sekmeler `Gönderiler | Reels | Etiketlenenler`, gerçek içerik grid'i.
6. Önceden ziyaretçi profilinde bulunan büyük açıklama kartı (`Takip, içerikleri Akışında gösterir...`) referans ziyaretçi görselinde yok; görsel sadeleştirmede mümkünse bu alanda gösterilmemeli, fakat takip/arkadaşlık/gizlilik davranışları silinmemeli.
7. **Sadece görüntü düzenini değiştir**; gerçek kullanıcı adı, resimler, takip/arkadaşlık sayıları, etkinlik, canlı yayın rozeti mantığı, profil gizliliği, arkadaşlığı kaldırma, takip isteği ve mevcut intro video oynatma bozulmayacak.

**Sonuç: İşlevsel iki görünümün karşı hesaba yansıması doğrulandı. Eksik olan yalnızca onaylanmış iki ziyaretçi görünümüne bire bir görsel uyarlama ve sonraki sürümde gerçek cihaz kontrolü.**

## Yeni gerçek telefon hata bildirimi — 2026-10-09 01:31, 45271.jpg

**AÇIK HATA / görsel taşma — `Profili Düzenle` ekranının en altı.** Kullanıcının gerçek Android ekran görüntüsünde, `Profili önizle` bölümünün altındaki **`Kaydet`** ve **`Önizleme aç`** yan yana işlem butonları ekranın alt kenarına fazla yakın. Butonların alt tarafı yarı saydam/soluk bir alana ve Android sistem gezinme çubuğuna doğru taşıyor; tamamı rahatça görünmüyor. Bu `Kapaksız sade görünüm` seçiliyken gözlendi. Kullanıcı açıkça “düzenle girince en altta taşma var not et” dedi.

**Gereken düzeltme (sonraki UI paketi):** `NgelXOnayliProfilDuzenlePage` içinde `Scaffold` / `SafeArea` ve `SingleChildScrollView` alt boşluğunu doğru ayarla. Cihazın gerçek `MediaQuery.viewPadding.bottom`, `viewInsets.bottom` ve klavye durumunu hesaba kat. `Kaydet` ve `Önizleme aç` düğmelerinin **tam yüksekliği, gölgeleri ve etiketleri** her ekranda görünmeli, telefonun sistem gezinme düğmelerine binmemeli. Gerekirse alt eylemleri ekranın güvenli bölgesindeki ayrı sabit bir alana koy veya kaydırılabilir içerikte yeterli alt tampon ekle. Küçük ekran, Android 3 tuşlu gezinme ve klavye açık/kapalı hallerini kontrol et.

**Koruma şartı:** Mevcut `Kaydet`, `Önizleme aç`, kapaklı/kapaksız tercih kaydı, fotoğraf/intro videosu, Firestore güvenliği ve referans tasarım aynı kalacak. Bu, çalışan profil işlemlerine dokunmadan yalnızca **responsive / alt güvenli alan (safe area)** hatası olarak çözülecek.

**Durum:** Kullanıcı ekran görüntüsüyle **tespit edildi ve Work QA listesine kaydedildi**. Henüz kodda düzeltilmiş / cihazda yeniden test edilmiş değildir.

## Telefon UI isteği — 2026-10-09 01:35, 45274.jpg — Uyarı mesajına renk

**Kullanıcı talebi:** "En alttaki uyarı yazısında renkli yap not et."

- `Profili Düzenle` ekranında `Kapaklı görünüm` seçilip hesapta henüz kapak fotoğrafı yokken altta görünen `Kapaklı görünüm için önce bir kapak fotoğrafı ekle.` uyarısı mevcut koyu gri/siyah Snackbar, beyaz metin yerine **görünür, modern renkli bir uyarı** olmalı. Mor NgelX paletine uygun ikon/vurgu; dikkat gerektiren koşul için sıcak turuncu/amber tonlu açık bir arka plan ve koyu okunaklı yazı veya eşdeğer erişilebilir belirgin kombinasyon tercih edilebilir. Metin kontrastı yüksek olmalı; yalnız yazıyı değiştirmek yeterli değil.
- Bu bir **tasarım/geri bildirim renk değişikliği talebi**; mevcut doğrulama şartını kaldırma. Kapak fotoğrafı eklenmeden kapaklı modun kaydedilmesine izin verme.
- `_hata('Kapaklı görünüm için önce bir kapak fotoğrafı ekle.')` bildirimi için UI değişikliği; diğer hata ve başarı geri bildirimleriyle tutarlı, erişilebilir, güvenli alana yerleşen renkli Snackbar / uyarı bileşeni.
- Daha önce 45271.jpg ile kaydedilmiş **en alttaki Kaydet / Önizleme aç taşma hatası** ayrı ve açık bug: ikisini de alt safe area düzenlemesiyle sonraki konsolide tasarım paketinde çöz. Uyarı Snackbar'ı bu butonları örtememeli veya Android üç tuşlu gezinmeye binmemeli.
- **Durum:** Kullanıcı isteği Work QA listesine kaydedildi. Henüz tasarım koduna uygulanmadı / telefonda test edilmedi.
