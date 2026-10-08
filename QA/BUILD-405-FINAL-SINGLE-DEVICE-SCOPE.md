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
