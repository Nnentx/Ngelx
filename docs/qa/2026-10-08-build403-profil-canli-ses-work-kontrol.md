# NgelX Build 403 — Ben/Profil, Canlı Yayın, Sesli Oda ve Premium Work

Kaynak: 2026-10-08 telefon kayıtları; `docs/qa/2026-10-08-build402-cihaz-video-karsilastirma.md` ve `docs/qa/2026-10-08-build402-kesfet-canli-sesli-video-incelemesi.md`. Kullanıcının son onayı: tek pakette kodla; çalışanları koru.

## Bu pakette uygulanan kod

1. **Profil tanıtım videosu:** Gerçek video oynatıcı tamamen aynı; player başlatılıp metadata erişildiğinde gerçek `mm:ss` süresi göster.
2. **Kaydedilenler:** Thumbnail boşsa sırasıyla `coverUrl`, `posterUrl`, `imageUrl` seçeneklerini dene; gerçek video ilk kare işlenmesi 12 saniye aşarsa sonsuz spinner yerine yeniden deneme eylemi göster. Eski gönderiye dokunma/kaydedilenlerden kaldır işlevi değişmedi.
3. **Ayarlar / Premium ve Cüzdan:** **Yalnız bu satır** açık mavi arka plan, mavi metin ve mavi ikon kazanır. Diğer tüm ayar satırlarının fonksiyonları/renkleri korunur.
4. **Sesli Oda / Söz istekleri:** Firebase sorgusu, dinleyici isteği ve yönetici kabul/ret yolu korunur. Yüklenmede açıklama göster, 7 saniye boyunca ilk veri gelmezse 'İstekler hâlâ yükleniyor' + 'Yeniden dene'; bu arıza ve boş durumu birbirine karıştırmaz.
5. **Sesli Oda oluşturma:** Kategori seçimi mor temaya uyumlu hale geldi; herkese açık/takipçiler/arkadaşlar seçimine ilişkin açıklama alanı eklendi.
6. **Canlı yayın hazırlama:** Uzun kaydırıcılı Görüntü Stüdyosu başlangıçta katlanmış bir panelde; tıklanınca aynı filtreler, kalite ayarları ve ışık kontrolleri açılır. Kamera, kalite, mikrofon, yayın izleyicileri ve yayın başlatma fonksiyonları aynı kalır.

## Korunanlar
- Firebase/Firestore, R2 kapak yükleme `kind:'profiles'`, profil kimliği/kullanıcı adı/biyografi, kaydetme, arkadaş/mesaj/istek, hikâye, kaydedilenler.
- Canlı yayın başlat/bitir, 3-2-1, kamera/mikrofon, PK, yorum ve yayın sonu analitiği; LiveKit token/oda yönetimi değiştirilmedi.
- Sesli oda giriş, oda müziği, izin/gizlilik, söz isteme/onay/red, sohbet, oda sonlandırma ve Akış mini-bar.
- Sahte profil, sahte hikâye, sahte izleyici veya yapay katalog içeriği üretilmedi.

## Hâlâ açık gerçek cihaz testleri
- Başka hesapta canlı yayın ve sesli oda Keşfet listesinde görünüyor mu? Ses/mikrofon ve müzik gerçekten iletiliyor mu?
- Akış video spinner'ı oda açıkken uzun sürüyor mu? Süresi/cihaz belleği/ağ ölçümü olmadan çözüldü denmeyecek.
- Söz istekleri Firestore bağlantısı gerçekten geliyor mu? Başka kullanıcıdan istek kabul/red testi gerekir. Bu pakette yükleme UX düzenlemesi var; sunucu sorunu varsa kendiliğinden çözüldü demek doğru değildir.
- Kaydedilenler'de gri görünen video yanlış thumbnail metadata yüzünden mi yoksa video URL erişimi yüzünden mi? Yeniden deneme/timeout bu durumu kullanıcıya görünür yapar, ancak medya kaynak hatasını zorunlu olarak çözmez.
- Profil referansındaki bazı ince hizalama farkları ve diğer yeni özellik istekleri bu pakette ele alınmadı; Build 402'nin çalışan tasarımı korunuyor.

## Uygulama/teslim ölçütleri
`tools/apply_build403_profile_live_audio.py` ardından `tools/check_build403_regression.py` → Flutter analizi → sabit imzalı release APK 1.0.179+403 → artifact. Sonrasında gerçek cihaz görüntüsü ve iki hesapla bağlantı testleri.
**Bu not, tek başına telefon testinin geçtiğine ilişkin kanıt değildir.**

## CI ve teslim sonucu — 2026-10-08
- GitHub Actions: https://github.com/Nnentx/Ngelx/actions/runs/37762165024
- Sonuç: **success**. Build 399–403 regresyonları, Flutter analizi, imzalı release APK ve artifact yükleme başarılı.
- APK: **NgelX 1.0.179 (Build 403)**. Artifact: https://github.com/Nnentx/Ngelx/actions/runs/37762165024/artifacts/11543391577
- APK ZIP'ten çıkarıldı; SHA-256 değeri checksum dosyasıyla eşleşti. Android'de canlı/oda işlemlerinin gerçek sonuçları ayrıca cihazda test edilmeli.
- Not: Mevcut sesli oda açılışı/yayın akışı zaten çalışıyordu; Build 403 yeni medya transfer protokolü/LiveKit sunucu değişikliği değildir.

## Build 403 gerçek cihaz: Profil/Ayarlar video QA — 45082.mp4

- Video süresi 61,33 sn; tam rapor: [Build 403 profil telefon testi](./2026-10-08-build403-profil-gercek-cihaz-video-incelemesi.md).
- **Cihazda gözlenen geçişler başarılı:** Premium ve Cüzdan satırının yalnız mavi vurgusu; profil kapak/avatar/ad/sayaçlar; tanıtım videosu `00:40` süre; okunur video değiştirme/kaldırma alt menüsü; gerçek hikâyeler ve seçenek menüsü; Kaydedilenler'de videoyu açma, 2 kayıttan 1 kayda kaldırma ve başarı bildirimi; beyaz beşli alt navigasyon.
- **Açık P1:** Kaydedilmiş video thumbnail'leri bazı tekrar girişlerde önce gri, sonra yükleniyor. Medya gerçekten açılıp oynadığı için kaynak dosyanın tamamen bozuk olduğu söylenemez. Önizleme/cache ve gerçek hata/timeout ayrımı ölçülecek.
- **Açık P1/P2:** Hikâye, video ve Akış geçişlerinde zaman zaman siyah spinner ile bekleme. Süre/tekrar sayısı ve cihaz ağ koşullarını ölçmeden çözüldü denmeyecek.
- **Açık P2:** Tanıtım videosunda kısa yeniden başlatma/yükleme spinner; referanstaki süre etiketi yerleşimi ve kısayol etiket yazı boyutu küçük tasarım farkları.
- **Test edilmedi:** Canlı Yayın, Sesli Oda, karşı hesapta mesaj/izin/arkadaşlık, Premium satın alma ve beş profil sekmesinin tümü. Kullanıcı bu kaydı özellikle profil videosu olarak gönderdi.
- Sadece QA notu kaydedildi; yeni APK ve uygulama kod değişikliği yapılmadı.

## Build 403 Sesli Odalar telefon testi — 45084.mp4

- Kullanıcının yaklaşık 2:23 dakikalık Sesli Odalar ekran kaydı incelendi. Ayrıntı: [Sesli Odalar Build 403 QA](./2026-10-08-build403-sesli-odalar-telefon-video-incelemesi.md).
- **Gözlenen ve korunacak:** Keşfet/Sesli, gerçek oda oluşturma, başlık/kategori/erişim seçimi, 1/12 konuşmacı ve 2. kişi bekleniyor, kişiler/tepki, odada sohbet mesajı, mikrofon açık/kapalı, 3 sohbet seçip davet gönderme ve onayı, müzik kütüphanesinden parça seçme, oynatıcı kontrolü/duraklatma, Akış/Keşfet/Sohbet/Ben üzerinde aktif oda mini barı, odaya dönme/bitirme.
- **Öncelikli gerçek görsel hata:** `Sesli oda oluştur` ekranında **seçili olmayan kategori ChoiceChip'leri siyah zeminde siyah/koyu yazılı ve okunamıyor.** Kontrast ve tema arka planını düzelt, oda oluşturma değerlerini ve işlevlerini koru.
- **Söz istekleri henüz doğrulanmadı:** Video boyunca `İstekler` düğmesi var ancak alt panel açılmadı. Build 403 yükleme/yeniden dene değişikliğinin çalıştığı bu kayıttan çıkarılamaz.
- **Akış medya notu:** Oda sürerken ilk video kısa siyah spinner gösteriyor, sonra videolar oynuyor; eski 'kalıcı açılmama' bu kayıtta doğrulanmadı. Geçiş süresi/performance ölçümü açık.
- **Test edilmedi:** İkinci telefonun odayı canlıyken Keşfet/Sesli'de bulması, davetlerin karşı kişiye teslimi, sesli sohbetin/oda müziğinin ikinci cihazda duyulması, söz isteğinin alınması/ kabul/red.
- Boş oda listesi kayıt başında/oda bitince normal; hata sayılmayacak.
- **Durum:** Gözlem ve Work kaydı. Kod değişmedi, Build 404 APK üretilmedi. Kullanıcıdan şimdi sıradaki Canlı Yayın videosu bekleniyor.
