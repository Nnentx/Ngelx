# NgelX Build 406 — Son 8 Hata Tek Paket

- Kaynak: Build 405 tek telefon video kayıtları (45115.mp4, 45117.mp4, 45121.mp4), gelen kutusu bildirimi (45118.jpg), davet ekranları (45119.jpg, 45120.jpg), `QA/BUILD-405-FINAL-SINGLE-DEVICE-SCOPE.md`.
- Branch: `work/build-406-final-eight-fixes`.
- Build hedefi: **1.0.182+406**.
- Kod uygulama yöntemi: önce mevcut 395–405 CI yamaları, ardından `tools/apply_build406_final_eight.py`. Yeni APK kaynakları çalışma dalındaki uygulama dosyalarında doğrudan değil, doğrulanan CI çalışma kopyasında oluşturulur.

## Sekiz başlık — kod işi

1. **P1 Canlı Yayın / son özeti:** `_CanliOzetSatiri` etiket ve değerlerinin siyah yazı renklere sahip olmasını sağla. Build 405'teki tek kalıcı özet katmanı, onay ve Keşfet'e dönüş değişmeyecek.
2. **P1 Gelen Kutusu / Bildirimler:** Gerçek `fromUid` ile kişiyi Firestore'dan çöz; görünen ad veya kullanıcı adını, gerçek profil resmini kullan. Var olan gönderici bilgisi yoksa belirsiz/kayıp hesap yedeği göster. Eski istek metinlerine isim ekle; tekrar eden isim yazma. Kabul/ret, bildirim zamanı ve okundu durumu aynı.
3. **P2 Gruplar / Davet:** Geçerli, hala aktif grup koduyla `Gruba katıl` doğrudan `autojoin` olacak. `joinApproval` gerçek davet bağlantısında bekleme zorunluluğu olmayacak. Firestore `validInvite`, geçerli chat code, revoked/active/expiresAt, 60 kişi sınırı ve banned listesi korunacak. Açık keşif onaylı katılım yolu değişmeyecek. Bu işlem Firebase kurallarının canlı ortama yayınlanmasını da gerektirir.
4. **P2 Profil / tanıtım videosu:** URL değişince `ValueKey(url)` ile eski oynatıcı/kapak controller'ını düşür ve gerçek yeni player oluştur. Başarılı upload bildirimi, dosya, `mm:ss` süre ve geri dönüş korunacak.
5. **P2 Profil / avatar & kapak:** Mevcut URL için tekrar tekrar yeni provider nesneleri yerine profil kapsamlı kararlı provider cache kullan. Yeni URL olunca yenisi çözülür. Kalıcı yükleme kusuru ölçülmeden tamamen bitti denmez.
6. **P2 Akış / medya geçişi:** Medya önizleme yuvalarında koyu boş ekran yerine açıklayıcı/video önizleme durumu kullan. Bu görsel iyileştirme, tüm ağ/decoder kaynaklı tam ekran Akış siyah spinner gecikmelerini tek başına giderdiğini kanıtlamaz; tek cihazda ayrı smoke gerekir.
7. **P3 Kaydedilenler:** Profil kısayol genişliğini artır, kısa etikette tek satırlı orantılı yazı kullan. Gerçek Kaydedilenler içeriği/kayıt kaldırma işleyicileri değişmeyecek.
8. **P3 Gizlilik:** `Gizli hesap` + `Profilimi kimler görüntüleyebilir?` izinlerinin birlikte nasıl etkili olduğunu açıkla, stored privacy ayarlarını değiştirme.

## Güvenlik, regresyon ve teslim
- Python koruma kontrolleri: 399–406, `tools/check_build406_regression.py`.
- Firebase Firestore emulator birim testleri: `tools/firestore_rules_test.mjs` içinde onaylı grupta geçerli aktif linkle `autojoin` mümkün olmalı; yalnız `pending` kendi kendine üyelik yaratamaz.
- APK: Flutter analyze + imzalı release + sha256 + artifact (önceki paket kimliğini ve çalışan işlevleri koru).
- Firebase üretim kurallarını **yalnız yukarıdaki testler ve başarılı APK CI sonucundan sonra** ayrı `deploy-rules` job'uyla uygula; servis kimliği yoksa iş başarısız olduğu açıkça bildirilecek.
- **İkinci telefon/iki hesap gerçek bağlantı testleri isteğe bağlı beklemede**: live ses, karşı izleyici/yorum, sesli oda, PK, davet teslimi. Başarılı diye işaretlenmez.
- **Gerçek cihaz kontrolü gerekli**: Canlı özet metin/sayı, gelen kutusu gerçek gönderen, profil yeni video & Kaydedilenler, geçerli davet linki. Kod/CI başarısı cihaz uçtan uca onayı değildir.

## Durum
Başlangıç kaydı: Kod yaması ve otomasyon pipeline'ı oluşturuldu, CI sonuçları takip ediliyor. Derleme başarılı olmadan hiçbir maddeye telefonda tamamlandı statüsü verilmeyecek.

## Build 406 CI ve Firebase dağıtım sonucu (2026-10-08)

- **GitHub Actions:** https://github.com/Nnentx/Ngelx/actions/runs/37821753988
- **CI:** Hem `build` hem `deploy-rules` job'ları **SUCCESS**.
- **Sürüm:** **NgelX 1.0.182+406**.
- **Kaynak regresyon:** Build 399–406 Python koruma kontrolleri başarılı.
- **Firestore güvenlik:** Firebase emulator suite başarıyla çalıştı (onaylı gruba geçerli linkle `autojoin`, yalnız bekleyen istekle izin atlatma engeli); doğrulanmış kurallar paketlendi.
- **Flutter:** Analyze başarılı; imzalı release APK oluşturuldu, imza ve SHA256 adımları başarılı, artifact yükleme başarılı.
- **Build 406 APK:** https://github.com/Nnentx/Ngelx/actions/runs/37821753988/artifacts/11570322092 (`NgelX-1.0.182-Build-406-FINAL-EIGHT-FIXES`).
- **Test edilmiş kurallar artifact:** https://github.com/Nnentx/Ngelx/actions/runs/37821753988/artifacts/11569875934.
- **CANLI FIREBASE YAYINI BAŞARILI:** `deploy-rules` loglarında `Deploying to 'ngelx-44eed'`, `rules file firestore.rules compiled successfully`, `released rules firestore.rules to cloud.firestore`, `Deploy complete!` satırları doğrulandı. Bu, değişen `validInvite` + `validSelfJoin` yetkilendirmesinin NgelX Firebase projesine yayımlandığını gösterir.
- **Güvenli doğrulama sınırı:** CI/Firestore emulator testinin başarılı olması, gerçek telefonda tüm sekiz başlık için kusursuz deneyimi kanıtlamaz. İkinci telefon E2E hâlâ kullanıcı isteğiyle beklemede. Özellikle feed medya ilk kare performansı görsel düzenlemeyle iyileştirilmeye çalışıldı, bütün cihaz/ağ koşullarında tamamen çözülmüş sayılmaz.
- **Telefon hızlı son kontrol:** Ayarlar'da 1.0.182/Yapı 406 görünsün; Canlı son özetinin 5 satırı okunabilsin; bildirimlerde eski istekler gerçek profil adını göstersin; geçerli linkle direkt gruba katılım; profil videosunu bir kez değiştirince yeni görüntü; Kaydedilenler kısayolu tek satır. Gerekirse yalnız sorun görülen kısmın kısa videosu yeterli. Yeni büyük test turu istenmiyor.

## Build 406 gerçek Android / Canlı Yayın son kontrol — 45176.mp4 (2026-10-08)

**Kaynak:** Kullanıcının yüklediği yaklaşık 43,6 saniyelik 1080×2392 Android ekran kaydı; hemen önce telefondaki Ayarlar ekranında `v1.0.182 • Yapı 406` doğrulandı. Kapsam: tek telefonla canlı yayın başlatma, paylaşım, kamera/filtre, yayını bitirme, kalıcı özet ve Keşfet dönüşü.

**Görüntüde doğrulanan işlemler:**
- Yaklaşık 0–11 sn: Canlı yayın hazırlama, başlık (`cvcc`), kamera önizlemesi, görüntü kalite 720p / 30 FPS, gizlilik ve `Canlı yayına başla` çalışıyor. Uygulama birkaç saniye içinde yayını başlatıyor.
- 11–21 sn: Canlı oturum sayacı ilerliyor. `Canlı yayını NgelX'te paylaş` kişi listesinde iki kişi seçiliyor ve mavi onay bildirimi `Canlı yayını 2 kişiye Aktivite ve Sohbet üzerinden gönderildi.` gösteriyor. **Bu yalnız gönderici tarafı bildirimi**; karşı taraf teslimi (ikinci telefon testi) hâlâ ertelendi.
- 22–35 sn: Kamera kapatılıp `Kamera kapalı` mesajı gösteriliyor, tekrar açılınca canlı görüntü geri geliyor; Canlı Yayın araçlarındaki filtre/güzellik/görüntü kontrolleri açılıyor.
- 35–42 sn: `Yayın bitsin mi?` onay penceresi açılıyor; yayın sona erdikten sonra `CANLI YAYIN SONA ERDİ` ve **tek kalıcı beyaz `Canlı yayın özeti`** kartı düzgün görüntüleniyor. **Önceki Build 405'te eksik görünen beş başlık ve sayıları artık görünür**: Süre `00:26`, En yüksek izleyici `0`, Beğeni `0`, Yorum `0`, Hediye puanı `0`. İkonlar, etiketler ve değerler okunuyor. `Keşfet'e dön` tıklanınca Keşfet > Canlı ekranına geçiliyor.
- 37 sn civarında yayın sonlandırma/oda bağlantısı kapanırken **kısa yükleme spinner'ı** gözleniyor, ardından özet açılıyor; uzun süren takılma veya çökme görünmüyor.
- Yayın başlığının `cvcc` şeklinde görünmesi, yorum gönderilmiş olduğu anlamına gelmez. Dolayısıyla `Yorum 0` sayısının yanlış olduğu bu video ile kanıtlanmıyor.

**Test kararı:** **Canlı Yayın bitiş özeti yazıları/sayıları görünmüyor P1 maddesi — gerçek telefonda GÖRSEL OLARAK GEÇTİ / KAPATILDI.** Canlı başlatma, kamera kapat/aç, filtre paneli, kapanış onayı, tek özet ve Keşfet dönüşü tek telefon smoke geçti. Sayıların gerçek başka kullanıcı etkileşimleriyle doğru artması, paylaşımın alıcıya teslimi, canlı ses, PK karşılaşması, hediyeler iki hesaplı testler olduğundan halen **ertelendi/doğrulanmadı**. Video tek başına diğer 7 Build 406 maddesinin cihaz testini tamamlamaz.

**İşlem:** QA kaydı güncellendi; yeni kod, Build 407 veya APK oluşturulmadı.

## Build 406 gerçek Android / Gelen Kutusu isimleri — 45178.mp4 (2026-10-08)

**Kaynak:** Kullanıcının gönderdiği ~31,6 sn 1080×2392 Android ekran videosu. Kullanıcı Build 406 yüklemesini daha önce Ayarlar ekranında `v1.0.182 • Yapı 406` olarak doğruladı. Kapsam: `Sohbet → Gelen Kutusu` sekmeleri, İstekler, ayrı Aktivite ekranı ve Grup/Sohbet açılması.

### Olumlu tek-telefon gözlemleri
- **00–03 sn:** Profil → Gelen Kutusu açılıyor; `Tümü` sekmesinde mesajlar, gruplar, bildirimler görünüyor.
- **08–12 sn:** `İstekler` sekmesi açılıyor; bekleyen takip isteği **Umay Umay** gerçek görünen ismi ve profil fotoğrafıyla görüntüleniyor, kabul/ret tuşları mevcut.
- **12–15 sn:** `Aktivite` ayrı sayfasında **Umay Umay seni takip etmek istiyor**, **Alperen Yarbay sana arkadaşlık isteği gönderdi**, **Alperen Yarbay seni takip etmek istiyor** satırlarında gönderen isimleri okunuyor. Kullanıcı takip isteğini kabul ediyor, **`Takip isteği kabul edildi.`** yeşil bildirimi görünüyor.
- **20–26 sn:** Gelen Kutusu → Gruplar listesi açılıyor; kullanıcı grup sohbetini görüntülüyor (canlı sohbet mesajlaşma uçtan uca bu videoyla kanıtlanmaz).
- **28–31 sn:** Profil, avatar/istatistik/kısayollar ve tanıtım videosu görünür.

### Açık hata — Build 406 / P1 gönderen adı düzeltmesi tam sonuç vermedi
- **01–07 sn:** `Gelen Kutusu → Tümü` bölümünde takip bildirimine ait üst satır **`seni takip etmek istiyor`** yazıyor; ismin gelmesini beklerken spinner da görünüyor, fakat videonun bu bölümünde gönderen adı görünür olmuyor.
- **16–19 sn:** `Gelen Kutusu → Bildirimler` bölümünde **`sana arkadaşlık isteği gönderdi`** ve **`seni takip etmek istiyor`** (yaklaşık altı saat önce) bildirimleri **adı olmadan** ve jenerik kullanıcı avatarlarıyla duruyor. `Gelen Kutusu yenilendi` bildirimi görünmesine rağmen eksik isimler giderilmiyor.
- **Aynı uygulamadaki ayrı `Aktivite` ekranında** bazı istekler düzgün gönderici adıyla gösteriliyor. Bu, bildirimleri gösteren **birden fazla UI/render akışının tutarsızlığını** düşündürüyor. Farklı eski bildirimlerin `fromUid` alanı var mı, veritabanında gerçekte gönderen profili erişilebilir mi henüz doğrulanmadı. Aynı kişinin iki farklı bildirim olduğu varsayılmamalı.

### Teknik takip / kabul
1. `Gelen Kutusu → Tümü`, `Gelen Kutusu → Bildirimler`, `İstekler` ve ayrı `Aktivite` ekranı **aynı gerçek gönderen kimlik çözümleme mantığını** kullanmalı. Build 406 yaması, ayrı Aktivite liste satırını ele almış olabilir; Gelen Kutusu iç listelerini de kapsayacak şekilde doğrula.
2. Mevcut bildirimlerde `fromUid` / `senderId` / `senderUid` / varsa `actorUid` / `userId` gibi farklı alanların doğruluğunu güvenli biçimde çöz. Kullanıcı profilindeki `displayName`, `username`, `photoUrl` alanlarını kullan; yanlış/farklı bildirimden isim taşınmasın.
3. Gönderen kaydı silinmiş veya adı erişilemiyorsa uydurma isim verme; **`Gönderenin hesabı kullanılamıyor`** gibi açık bir fallback kullan. Sonsuz spinner yerine bekleme/zaman aşımı ve erişim hata durumu sun.
4. Gönderen profiline dokunma, takip/arkadaşlık isteği kabul-ret, zaman/okunma, gizlilik, etkileşim sıralaması ve gruplar **korunmalı**.
5. **Retest:** Tek cihazla Gelen Kutusu > Tümü ve Bildirimler eski istekler / İstekler / Aktivite satırları gösterilsin; ayrı test için ikinci telefona gerek yok. İkinci telefon uçtan uca teslim senaryoları **ertelendi**.

**QA kararı:** **Build 406 "Bildirimlerde kim gönderdiği görünsün" P1 maddesi gerçek telefonda kısmen çalışıyor fakat **GEÇMEDİ / AÇIK**. Kodun tüm ilgili ekranlarda çalıştığı doğrulanmadı. Bu not, mevcut Build 406 APK veya Firebase kurallarını değiştirmez; yeni APK oluşturulmadı.
