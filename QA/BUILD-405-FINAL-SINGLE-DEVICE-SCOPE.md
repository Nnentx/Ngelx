# NgelX Build 405 — Tek Telefon Son Düzeltme ve Test Kapatma Paketi

**Kullanıcı kararı:** İkinci telefon / iki hesapla canlı bağlantı doğrulamaları **şimdilik beklemede**. Bu nedenle onları hata veya başarılmış test olarak göstermeyin. Profildeki ufak kalanları da aynı pakete ekleyin; gereksiz yeni tur açmayın.

## Kaynaklar
- `QA/BUILD-404-LIVE-BROADCAST-VIDEO-TEST.md` (45103.mp4)
- `docs/qa/2026-10-08-build404-ben-profil-son-kontrol-45098.md`
- `docs/qa/2026-10-08-build404-fixes-preservation-matrix.md`
- `docs/qa/2026-10-08-build403-sesli-odalar-telefon-video-incelemesi.md`

## Kodlanan hedefli düzeltmeler (CI/cihaz testi tamamlanmadan düzeldi iddiası yok)
1. **Canlı Yayın P1:** yayın bitti ekranıyla analiz modalı çakışmasın. Yayın sonu verileri tek ve kalıcı beyaz özet kartında görüntülensin; ağ/oda kapatma sürerken dönüş devre dışı kalsın; çift pop/navigasyon çakışması engellensin. Kamera, yorum, PK ve paylaşım korunur.
2. **Hikâyeler P1:** fotoğraf ve video **gerçekten hazır olana kadar** ilerleme zamanlayıcısı başlamasın. Ön sonraki video ve sonraki görsel önbelleğe alınsın; 12 saniye medya initialize/precache sınırı sonrası kullanıcıya hata ve gerçek yeniden deneme yolu sunulsun. Başarısız video otomatik atlanmasın. Foto/video, saat, görüntülenme, tepki ve gerçek veriler korunur.
3. **Ben / Profil P2–P3:** Sahibin arkadaş listesine açılan yanıltıcı `Arkadaş Ekle` etiketi `Arkadaşlar` olarak netleştirilsin; Kaydedilenler dahil kısayol başlıklarının iki satırlı düzeni aynı yükseklikte hizalansın. Profil medya gerçek süre, video değiştir, avatar/kapak, istatistik ve gizlilik mevcut akışları korunur.
4. **Önceki düzeltilenler:** Sesli Oda kategori kontrastı, kompakt bekleme, isteklerde yenile, müzik/davet/mikrofon; Kaydedilenler video açma, Premium yalnız mavi vurgu; Sohbet, Akış, Keşfet, Üret ve grup/hesap akışları korunma regresyonlarından geçsin.
5. **Versiyon:** NgelX 1.0.181+405; `tools/apply_build405_single_device_final.py`, `tools/check_build405_regression.py`, `.github/workflows/NgelX-BUILD-405-FINAL-SINGLE-DEVICE.yml`.

## Test kapatma kapıları
- **Kaynak/regresyon:** Build 399–405 Python kontrol betikleri başarılı olmalı.
- **Flutter:** `flutter analyze` ve imzalı release APK yapımı/sha256 başarılı olmalı; bu geçmeden teslim onaylı değil.
- **Telefon tek kullanıcı smoke:** Ben/Profil foto ve yeni tanıtım videosu, Kaydedilenler oynatma, art arda 4 hikâye ve Tekrar dene, canlı yayın başlat/yorum/bitir/kalıcı özet/Keşfet dönüşü, sesli oda aç/söz istekleri/bitir. Yeni uzun test turu yerine yalnız sorun tekrarlanırsa kısa video yeterli.
- **İkinci telefon / iki hesap E2E:** yayın keşfi, gerçek ses, başka kullanıcı yorum ve katılımı, izleyici sayısı, oda müziği, söz isteği, PK rakibi, davet alıcısı ve erişim gizliliği **bilinçli olarak sonraya ertelendi**; “geçti” statüsü verilmeyecek.
- **Performans gözlemleri:** Profil ilk video gri yüklenme ve avatar/kapak kısa loader, Akış video spinner gibi ağ/cache durumları Build 405 kaynak düzeltmelerinden tek başına tamamen çözülmüş sayılmamalı. Geri regresyon veya kalıcı spinner görülürse kayıt aç.

## Koruma
Kullanıcı verisi, yüklenen medya, takipçi/arkadaş bağlantıları, mesajlar, hikâye veya kaydedilenler silinmez. Mevcut işlevleri sıfırdan tasarlamak yerine son kalan bariz UI/medya hataları hedeflenir. Üretilen APK gerçek telefonda otomatik çalıştırılmış sayılmaz.

## Build 405 CI / teslim sonucu (2026-10-08)
- GitHub Actions run: https://github.com/Nnentx/Ngelx/actions/runs/37798305369
- Version: **1.0.181+405**.
- 399–405 kaynak koruma/regresyon, Flutter analiz, imzalı release APK oluşturma ve artifact upload adımları: **success**.
- APK ZIP / GitHub artifact: https://github.com/Nnentx/Ngelx/actions/runs/37798305369/artifacts/11560465680
- Artifact etiketi: `NgelX-1.0.181-Build-405-FINAL-SINGLE-DEVICE` (APK ve .sha256 içerir).
- Bu CI başarısı Android gerçek cihaz smoke veya ertelenmiş iki-kullanıcı bağlantı testinin yerine geçmez. Kullanıcı artık çoklu uzun test turu istemediğinden kalan tek-telefon doğrulamaları kısa ve hedefli tutulacak.

## Build 405 gerçek Android Profil video QA — 45115.mp4 (2026-10-08)

**Kaynak:** Bu sohbetten gönderilen yaklaşık 58,5 saniyelik 1080×2392 Android ekran videosu. Bundan hemen önceki Ayarlar ekranında NgelX **v1.0.181 / Yapı 405** doğrulandı. Video sadece **Ben/Profil ve tanıtım videosu değiştirme** akışını kapsıyor; hikâyeler, canlı yayın, Kaydedilenler içeriğini açma ve ikinci kullanıcı akışı test edilmedi.

### Gözlemlenen / korunacak çalışan akışlar
- **00–05 sn:** Beyaz profil sayfası, gerçek kapak ve avatar, profil düzenleme, yeni doğru isimli **Arkadaşlar** butonu; Takip 2 / Takipçi 3 / Etkileşim 21 / Arkadaşlar 3 istatistikleri (yalnız görüntülendi; sunucu değer doğrulaması yapılmadı). Gerçek tanıtım video kartında `00:34` etiket ve oynatıcı görülüyor. Beşli alt navigasyon yerinde.
- **05–08 sn:** `Tanıtım videosunu değiştir` alt menüsü açılıyor. Android sistem video seçicisinde video seçilip `Bitti` ile onaylanıyor. Galerinin arayüzü Android'e ait.
- **08–33 sn:** Profile dönülüyor; kapak, avatar, istatistikler ve tanıtım video kartı yerinde kalıyor; video kartı oynatılıyor. **31–34 sn** civarında `Profil tanıtım videosu kaydedildi` bildirimi görülüyor. Görünür klip/kapak bazı anlarda önceki görüntüyü göstermeye devam ediyor.
- **34–43 sn:** Video kartında `00:34` etiketi korunuyor, bir ara TikTok logolu siyah kare görünüyor (bu kaynak videonun karesi olabilir; NgelX kaynaklı marka overlay veya medya kaybı kanıtı değil). Tanıtım videosu menüsü yeniden açılabiliyor.
- **43–54 sn:** Kullanıcı Android son uygulamalar/ana ekranına çıkıp NgelX'i yeniden başlatıyor. Bu bir **manuel** uygulamadan çıkış; uygulama çökmesi olarak kaydedilmeyecek.
- **50–58 sn:** Uygulamaya dönüşte profil görünür, ilk karede kapak/avatar ve video için kısa yükleme/boş yerler var. Tanıtım kartı `Video hazırlanıyor / Tanıtım videosu oynat` konumundan kısa dönen spinner'a geçiyor, **56–58 sn** civarında seçilen `BE HERE` videonun gerçek posterini/önizlemesini ve `00:34` süre etiketini gösteriyor. Kaydın telefon yeniden başlatılması sonrasında kalıcı görünmesi olumlu; bu kayıt yeni videonun bütün 34 saniyesinin oynatıldığını kanıtlamaz.

### Kalan, derleme döngüsü açmadan kayıt altına alınan küçük kusurlar
1. **P2 — Profil medya cache/refresh:** Video seçimi ve başarılı kaydetme bildirimi sonrası bir süre eski kaynak kareleri görünmeye devam edebiliyor; yeni postere dönüş uygulama yeniden açıldıktan sonra net biçimde görünüyor. Öncelikli teknik kontrol: kaydetme tamamlanınca video URL/generation değişimini dinleme, önceki `VideoPlayerController` ve thumbnail cache geçersizleştirme, bekleyen async sonuçların eski görüntüyü geri yazmaması. Gerçek video dosyasına dokunma.
2. **P2 — Gereksiz avatar/kapak loader:** 14–27 sn video kartıyla uğraşılırken avatar üstünde beyaz spinner tekrarlıyor, profil kısa süre boş kalabiliyor. Girişte son bitmap'i tutup görsel kaynak değişmedikçe refetch etme; yüklemeyi daha sakin göster.
3. **P3 — `Kaydedilenler` kısayolunun kelime kırılması:** Kısayol iki satıra mekanik olarak (`Kaydedilenl` / `er`) bölünüyor. Build 405 satır yüksekliği hizalaması tek başına tipografiyi düzeltmemiş. Dar ekran için anlamı korunmuş tek satır ölçekli veya doğal hece ayarlı metin planlanmalı.
4. **Performans gözlemi, tek başına P1 değil:** 44–46 sn dolaylarında Akış'a geçişte siyah spinner çok kısa görülüyor; başka ekranlar ve video sonradan geliyor. Kalıcı açılmama kanıtı yok. 52–56 sn soğuk başlangıçta tanıtım video hazırlama durumu mevcut ve sonunda görüntü geliyor.

### Kapanış değerlendirmesi
- **Ben / Profil: temel tek-cihaz smoke geçti; P2/P3 görsel/performance notları açık.** Yeni kullanıcı/medya kaydı kaybolma, veri sıfırlanması veya uygulama çökmesi bu videoda kanıtlanmadı. `Arkadaşlar` etiket düzeltmesi telefonda doğrulandı.
- **Kapsam dışı ve hâlâ test edilmemiş:** Kaydedilenler videosunu aç/kaldır, 4+ Hikâyede siyah spinner ve hata yeniden dene, Canlı Yayın **sonlandır > tek ve kalıcı özet > Keşfet** sıralaması, sesli oda söz istekleri. Bu videodan geçmiş sayılmayacaklar.
- **Ertelenen:** İkinci telefon, ikinci hesap, PK karşı kullanıcı, canlı ses ve davet teslimi.
- **Not:** Bu ekleme QA kaydıdır; yeni kod/Build 406/APK üretimi yapılmış değildir. Uzun tekrar testleri istememek kullanıcının kabul edilmiş tercihidir.

## Gelen Kutusu / Bildirimler — gönderen adı görünmüyor (45118.jpg, 2026-10-08)

**Kullanıcının isteği:** Bildirimi kimin gönderdiği her zaman belli olsun; "seni takip etti", "sana arkadaşlık isteği gönderdi", "seni takip etmek istiyor" gibi genel ifadelerin başında gerçek gönderenin adı veya kullanıcı adı yer alsın.

**P1/P2 görsel-işlevsel eksiklik (Build 405 gerçek telefon ekranı):**
- Gelen Kutusu > **Bildirimler** sekmesindeki en üstteki arkadaşlık isteği satırında sadece **"sana arkadaşlık isteği gönderdi"**, altındaki takip isteği satırında sadece **"seni takip etmek istiyor"** yazıyor. Gönderen adı görünmüyor ve jenerik kişi ekle avatarı var. Bu nedenle kimin istek gönderdiği anlaşılmıyor.
- Aynı listede **"Alperen Yarbay Sana bir canlı yayın gönderdi"**, **"ADEM baykar seni ... grubuna ekledi"** ve **"Rojin Candan Gönderine yorum yaptı"** gibi gönderen adı bulunan olaylar görünüyor. Görüntülenen iki istek türünün tutarsız biçimi düzeltilmeli.

**Beklenen yazım örnekleri (isimler temsili; gerçek değerlerden üret):**
- `[Gönderenin görünen adı] sana arkadaşlık isteği gönderdi`.
- `[Gönderenin görünen adı] seni takip etmek istiyor` (**bekleyen takip isteği**).
- `[Gönderenin görünen adı] seni takip etti` (**gerçekleşmiş takip**).
- Diğer bildirim türlerinde de varsa gönderen adı ve avatarı doğru kullanıcıdan gelmeli; kullanıcı adına dokununca gönderen profili açılmalı.

**Teknik kabul şartları:**
1. Olaydaki gerçek `fromUid` / gönderici kimliği üzerinden güncel kullanıcı profili / `displayName` veya `username` çöz; yalnız sabit olay metninden ad çıkarma. Farklı bildirimin adı başka bildirimde görünmemeli.
2. Ad bulunamazsa hatalı veya uydurma isim gösterme; kullanıcı adı varsa onu kullan, hesap silinmiş/erişim yoksa açık ve tarafsız durum metni kullan. Boş başlık bırakma.
3. Gönderenin gerçek profil fotoğrafı varsa kullan; profil fotoğrafı yoksa varsayılan simge doğru bir yedek olabilir.
4. Bekleyen takip isteği ile tamamlanmış takibi karıştırma; kabul/ret eylemleri, okundu durumu, zaman bilgisi, bildirim sıralaması, sohbet / aktivite teslimi ve gizlilik kuralları korunmalı.
5. Tek cihazda eski/yeni arkadaşlık ve takip bildirimi örnekleriyle başlıkların görüntülenmesi doğrulanmalı; iki hesaplı uçtan uca senaryo kullanıcı isteği üzerine ayrıca **ertelendi**.

**Durum:** GitHub QA/Work notuna alındı; **kod henüz değiştirilmedi, yeni APK üretilmedi**. Bir sonraki toplu düzeltmeye dahil edilecek.

## Grup davet bağlantısı ile yönetici onayı olmadan katılım — yeni kullanıcı talebi (45119.jpg, 45120.jpg)

**Kullanıcının isteği (2026-10-08):** Sohbet > '+' > Gruba katıl ekranında, geçerli bir grup davet linkini veya kodunu yapıştırıp **Gruba katıl** seçilince **yönetici onayı beklemeden doğrudan gruba katılabilsin**. Kullanıcının özellikle istediği davranış davet linkinin yetkilendirme kabul edilmesidir; normal 'katılma isteği gönder → yönetici onayı' kuyruğuna sokulmaması gerekir.

**Ekran referansı:** 'Davetle gruba katıl', link/kod alanı, mor 'Gruba katıl' butonu. Alt bilgi kartı şu anda 'Grup yöneticisi onay istiyorsa önce katılma isteğin gönderilir. Onaylandığında bildirim alırsın.' diyor; yeni davet-linki akışıyla tutarlı olarak metin de güncellenmeli.

**İstenen kabul kriterleri (önce kodda incelenecek):**
1. Yalnız **grup yöneticisi/kurucusu tarafından oluşturulan aktif, geçerli, iptal edilmemiş** link/kod kullanıcıya doğrudan üyelik yetkisi versin; link geçersiz, süresi dolmuş veya iptal edilmişse açıklayıcı hata çıksın. Normal keşiften onaylı katılma yolu ayrı kalsın.
2. Davet linki doğrulanıp kullanıcı **Gruba katıl** dediğinde üyelik sunucu tarafında tek işlemle oluşturulsun; ayrıca yönetici onay kuyruğu oluşmasın. Üyelik gerçekleştiyse doğrudan grup ekranına git, zaten üyeyse mevcut grubu aç. Çift dokunma yinelenen üyelik üretmesin.
3. Yönetici tarafından engellenmiş kullanıcılar, silinmiş/kapalı grup, kullanıcı kısıtları ve mevcut **60 kişilik grup kapasitesi** gibi güvenlik kuralları **atlanmasın**. Başarısız doğrulamada üyelik eklenmesin.
4. Grup yöneticisi davet linkini devre dışı bırakabilsin. Yöneticinin ayrıca linkle katılımı sınırlandırabileceği ayar mevcutsa silinmesin; geçerli yönetici bağlantısı için onaysız katılım yetkisinin kapsamı açıkça tanımlansın.
5. 'Grup yöneticisi onay istiyorsa ...' yardım metni bu yeni geçerli bağlantı davranışına göre yeniden yazılsın; geçerli bağlantı ile direkt katılım ve diğer katılma talepleri ayrıştırılsın.
6. Mevcut grup sohbeti, üye izinleri, gruptan ayrılma, bildirimler ve davet akışları korunacak; **ikinci telefon testi şu an ertelenmiş** durumda.

**Durum:** GitHub QA/Work notlarına alındı. **Kodlanmadı; Build 405 APK değiştirilmedi.** Sonraki toplu düzeltme paketine dahil edilecek.
