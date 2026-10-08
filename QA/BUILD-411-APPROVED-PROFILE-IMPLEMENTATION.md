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
