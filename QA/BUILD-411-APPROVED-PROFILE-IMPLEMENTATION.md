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
