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

## Build 406 gerçek Android / Üret ve paylaşım testi — 45179.mp4 (2026-10-08)

**Kaynak ve kapsam:** Kullanıcının gönderdiği yaklaşık **99,9 saniyelik**, **1080×2392** Android ekran videosu. `Üret` sayfasından galeriden fotoğraf, kırpma/filtre/açıklama/paylaşım; Akış'ta gönderi yorum akışı; uygulama kamera ekranı; ikinci fotoğraf paylaşımı; Üret'te metin, anket, hikâye menüleri görünüyor. `Video kaydetme / Reels yükleme / canlı yayın / müzik / efekt` seçeneklerinin tamamı bu kayıtta sonuçlanmış uçtan uca test değil.

### Bu videoda çalışan, korunması gereken işlemler
- **00–17 sn:** `Üret` ekranı açılıyor. Galeri alt sayfası (`Fotoğraflar / Koleksiyonlar`) üzerinden fotoğraf seçiliyor. Siyah medya kırpma editöründe `Kırp`, serbest oran, 1:1 / 4:5 / dikey 9:16, döndürme/sıfırlama seçenekleri görünüyor; kullanıcı kırpma çerçevesini değiştirip `Kaydet` ile dönüyor.
- **17–28 sn:** Fotoğraf post hazırlığında gerçek görsel, kırp/döndür, filtreler (`Yok / Parlak / Sıcak / Soğuk`), açıklama, konum/etiket, görünürlük, indirme/yorum/yeniden paylaşım izinleri görünüyor. Açıklama alanına `teknik` yazılıyor; `Paylaş` ile `Fotoğraf 1/1 yükleniyor` ilerlemesi ve ardından **`Paylaşım yayınlandı ✅ Akışta ve profilinde görünecek.`** onayı çıkıyor.
- **28–47 sn:** `Akışa git` bağlantısıyla gönderi Akış'ta gösteriliyor. Kullanıcı yorum çekmecesini açıyor, yorum gönderiyor, ikinci yorum yazıyor, kalp ve `Düzenle` menüsüne giriyor; yorum düzenleme modalı görünüyor. Paylaşılan fotoğrafı bu testte Akış'ta görmek önemli.
- **48–69 sn:** Üret'teki kamera açılıyor. Fotoğraf/video modları ve kamera kontrolleri görünür. Kameradan alınan görüntü post önizlemesine geliyor; ikinci fotoğraf paylaşımı için `Fotoğraf 1/1 yükleniyor` ve yayın başarı bildirimi görülüyor. Video modundaki klibin gerçek kaydedilip yayımlandığı kanıtlanmıyor.
- **70–100 sn:** `Üret` ana ekranı, galeri düğmeleri, metin alanı, `Anket` eylemi ve hikâye oluşturma alt menüsü açılıyor. Hikâye menüsünde galeriden fotoğraf/video, fotoğraf/video çekme seçenekleri var. Metin postunun yayımlandığı, anketin oluşturulduğu veya Reels'in yüklenip oynatıldığı görülmüyor.
- Kayıt boyunca görünür uygulama çökmesi veya kalıcı boş ekranda takılma yok.

### Kalan açık UI / işlev eksikleri (sonraki tek düzeltme paketine)
1. **P2 — Üret ana kartlarında kelimenin kötü bölünmesi.** `Fotoğraf` etiketi **`Fotoğ / raf`**, `Efektler` etiketi **`Efektl / er`** şeklinde bölünüyor; yardımcı yazılarda da `Düşüncel / erini` gibi doğallıktan uzak kırılmalar var (0, 48, 70, 85–99 sn). Dört kartı dar ekran ve dinamik yazı ölçeğine uygun, tam sözcüklü başlıklarla hizala. İkon, eylem ve amaçları korunmalı.
2. **P2/P3 — Kalıcı başarı bildirimi ekranı kapatıyor.** İkinci yayın sonrası mavi `Paylaşım yayınlandı` çubuğu, Üret'e dönüldükten sonra yaklaşık **67–89. saniyeler boyunca** ekranın alt bölümünü kaplıyor; anket eylemi başka bildirim üretince kayboluyor gibi görünüyor. `Akışa git` eylemini koruyarak başarılı snackbar'ı makul sürede otomatik kapat, tekrar eden snack'leri sırala/değiştir, form alanlarına dokunmayı engellemesin.
3. **P2 — Anket düğmesi sadece hazırlık mesajı gösteriyor.** `Anket` seçildiğinde `Anket aracı hazırlanıyor.` bildirimi çıkıyor (yaklaşık 89–91 sn), anket sorusu/şıklarını girecek çalışır düzenleyici görülmüyor. Bu bir **özellik eksikliği**: kullanıcıya eylem sunuluyorsa anket oluşturma ve yayımlama akışı tamamlanmalı veya hazır olmayana kadar açıkça `yakında`/pasif gösterilmeli; sahte başarılı işlem izlenimi verilmemeli.
4. **P3 — Sekme/etiket dar alanda kısalıyor.** Hızlı yayın şeridinde `Canlı Ya...` kırpılmış; erişilebilir/açılır okunur tam etiket veya daha iyi düzen sağlanmalı. Başka metin taşmaları için küçük telefon / yazı ölçeği regresyon kontrolü.
5. **P3 — Başarılı paylaşım sonrası taslak/yeniden giriş mesajlarının netliği.** `Taslak otomatik kaydedildi` yazısı boş Üret formuna dönüşte görülebiliyor. Her başarılı gönderimden sonra form state sıfırlama, taslak durumunun gerçeği yansıtması ve önceki medyanın yanlışlıkla yeniden gönderilmemesi kontrol edilmeli. Bu videoda çift gönderi hatası **kanıtlanmadı**; koruma testi olarak not.
 
### Kapsam dışı / doğrulanmayanlar
- Video çekip post yapma, reels, efekti video/foto üstünde işleyip yayımlama, müzik lisans/oynatma, metin postunu yayınlama, anket yayınlama, hikâyeyi bu ekrandan sonuna kadar yayımlama ayrı uçtan uca onaylı sayılmayacak.
- Diğer kullanıcıda postun gösterimi/yorum eşzamanlaması gibi ikinci telefon/hesap işlemleri **kullanıcının isteğiyle ertelenmiş**.

**QA kararı:** **Üret: fotoğraf ekleme, kırpma, post hazırlama/yayınlama, Akış'ta görünme, yorum menüsü ve kamera fotoğrafı paylaşımı gerçek telefonda GEÇTİ.** Yukarıdaki 3 belirgin UI/özellik noktası ve 2 P3 kontrol notu **açık**; komple Üret modülü “tümü bitti” ilan edilmez. Bu yalnızca QA kaydıdır; **Build 406 APK ve Firebase değiştirilmedi**, Build 407 oluşturulmadı.

## Build 406 gerçek Android / Akış kalite, eksik ve fazlalık denetimi — 45180.mp4 (2026-10-08)

**Kaynak:** Kullanıcının gönderdiği yaklaşık **44,3 saniyelik**, 1080×2392 Android ekran kaydı. Kapsam: `Akış` → `Sana Özel` dikey medya geçişi, kısa video oynatma ve `Araçlar` bottom sheet ayarları. **Kullanıcının isteği:** çalışan parçaları koru, eksik/hatalı/fazla tekrar eden menü ve görsel yoğunluğunu ayır, tek sonraki Work paketine not et. Bu tur **kod / Build 407 / APK değiştirmez**.

### Videoda gerçekten görülen çalışan akış
- **00–02 sn:** İlk kartta en son yayımlanan kullanıcı gönderisi (`teknik` açıklaması) ve gerçek tarih/saat (`08.10.2026 21:56`), göreli zaman (`6 dk önce`) ile `Sana Özel` sekmesinde görünüyor. `Takip`, arama ve beşli alt navigasyon yerinde. Yeni gönderinin burada bulunması doğrulandı; genel öneri/sıralama algoritmasının bütünü test edilmedi.
- **02–20 sn:** Dikey kaydırmayla birden çok gerçek gönderi görüntüleniyor. Sağ aksiyon sütununda hesap avatarı, kalp/beğeni sayısı, yorum simgesi/sayısı, `Kaydet` veya `Kaydedildi`, `Araçlar` ve `Paylaş` bulunuyor. Bazı gönderilerde tarih, açıklama ve `x yorumun tümünü gör` var. Bu kayıtta beğeni, yorum gönderme ve dış paylaşımın tamamı aktif olarak sınanmadı.
- **22–29 sn:** `Araçlar` bottom sheet açılıyor. `İndir`, `İlgilenmiyorum`, `Bildir`, 0.5x/1x/1.5x/2x hız seçenekleri, `Temiz ekran modu`, `Otomatik kaydırma`, `Alt yazılar ve çeviri`, `İçeriği gizle`, `Bağlantıyı kopyala` ve kırmızı `PAYLAŞIMI SİL` eylemleri mevcut; `Otomatik kaydırma` anahtarı kapalıdan açık konuma alınıyor. Anahtarın çalışması **görsel olarak** doğrulandı; videonun bitişinde gerçekten diğer gönderiye otomatik geçtiği ayrı doğrulanmadı.
- **30–36 sn:** Sonraki videoda kısa süre koyu/TikTok açılış karesi ve kısa yüklenme göstergesi görünüyor; daha sonra gerçek video (`selam yazii` altyazılı görüntü) oynuyor. Bu durumda **kalıcı siyah ekran veya kilitlenme** görülmedi. TikTok markası büyük olasılıkla **yüklenen kaynak videonun içeriği**, NgelX'in eklediği zorunlu markalama şeklinde yorumlanamaz.
- **37–44 sn:** Ek video kaydırmaları devam ediyor. Telefonun kendi ses düzeyi katmanı önceki saniyelerde açılıyor; bu Android UI öğesi NgelX çakışma hatası olarak etiketlenmesin.

### Somut kusurlar / tasarım-fazlalık denetimi
1. **P2 — Video değişimindeki anlık karanlık/loader:** 30–35 sn civarında sonraki klibe geçerken karanlık kaynak açılış karesi ve kısa spinner gözleniyor, ardından açılıyor. `Video hazırlanıyor`/poster desteği, sonraki klip önceden hazırlama ve gecikme toleransı değerlendirilsin. **Kalıcı arıza kanıtlanmadı**; TikTok splash'ının kaynak medya olabileceğini ayırt et. Gereksiz yere kullanıcı yüklemesini değiştirme veya silme.
2. **P2/P3 — Araçlar menüsü aşırı uzun / yoğun:** Menü neredeyse tüm ekranı kaplıyor. Kullanımı kolaylaştırmak için `Oynatma` (hız/otomatik kaydır/temiz ekran), `İçerik` (altyazı/çeviri/indir/kopyala), `Tercihler` (ilgilenmiyorum/gizle/bildir) grupları değerlendirilsin; tehlikeli `Paylaşımı sil` en altta ayrı kırmızı kalsın. **Hiçbir çalışan eylem izinsiz kaldırılmayacak.**
3. **P3 — `İlgilenmiyorum` ve `İçeriği gizle` benzer görünüyor:** Biri öneri tercihlerini, diğeri yalnız bu gönderiyi gizliyorsa açıklamalarda bu fark açıkça yazılmalı. Aynı işlemi yapıyorlarsa tekleştirme önerisi hazırlanmalı; test/ürün kararı olmadan ikisinden biri silinmemeli.
4. **P2 güvenlik kontrolü — `PAYLAŞIMI SİL` görünür:** Kırmızı eylem açılan menüde var. **Bu kayıttan başka kullanıcı gönderisinde yetkisiz silme bulunduğu sonucu çıkarılamaz.** Sil yalnız yazarı/yetkili moderatör için sunulsun, gerçek sahiplik Firestore backend'de kontrol edilsin, yanlış dokunmaya karşı açık onay sorulsun. Kayıt sırasında silme işlemi denenmedi.
5. **P3 tasarım — medya üstü bilgi/aksiyon yoğunluğu:** Sağda beş farklı işlem, solda açıklama + iki zaman bilgisi + `yorumun tümünü gör`, ayrıca üst logo/sekme ve alt nav mevcut. Küçük ekranda videodaki yazıların üstünü kapatmayacak güvenli alan/gradyan/opsiyonel temiz mod incelensin. `Yorum` ikonu ile `yorumun tümünü gör` alternatif girişlerinin ikisinin de gerekçesi kontrol edilsin; kullanıcı onayı olmadan kaldırılmasın.
6. **Doğrulanmayan davranışlar:** `Takip` sekmesindeki sıra, gerçek `otomatik kaydırma` sonucu, 0.5/1.5/2x medya hızı, indir, filtreleme, gizleme, şikâyet, altyazı-çeviri, bağlantı kopyalama, temiz ekran modu, geri-navigation ve gerçek silme işlem sonucu bu videoda sonuca kadar denenmedi. Uçtan uca test geçti diye işaretleme.

### Korunacak doğru çözümler ve kapanış
- Dikey kaydırma, `Sana Özel` oynatımı, son paylaşımın görünmesi, iki zaman biçimi, `Kaydet/Kaydedildi` göstergesi, 5'li alt nav, `Araçlar` açılması ve otomatik kaydırma anahtarının durum değiştirmesi **görsel smoke geçti**.
- Akış ana ekranında videoların karanlık zeminde gösterilmesi tek başına tema hatası sayılmasın; kullanıcının genel beyaz tema talebi için navigasyon ve beyaz alt paneli korumak yeterli olabilir.
- **QA kararı:** Akış temel dikey gösterim/gezinti **GEÇTİ**. Kalıcı çökmeye rastlanmadı. **Bir hafif medya geçişi gözlemi, iki menü kullanılabilirliği/karması ve iki güvenlik/tasarım kontrolü açık**. Yeni başlıkları, hâlâ açık `Gelen Kutusu gönderen isimleri` ve `Üret` eksikleriyle sonraki toplu düzeltmede birleştir. **İkinci telefon testleri beklemede**.

## Build 406 / Akış — elle ileri sarma takılması + üst N logosu (45187.mp4, 45186.jpg, 2026-10-08)

**Kullanıcı talebi:** "Sol üstte büyük N logosu kaldır sadece NgelX kalsın" ve "Videoda elle ileri alınca videoyu çok geç düşüyor, onu da hallet, not et." İki kayıt da Akış'ın sonraki **tek toplu düzeltme paketine** dahil.

### A. P1/P2 — Video manuel ileri sarma / seek gecikmesi (45187.mp4)
- Yaklaşık **21,7 saniyelik Android ekran videosunda**, Akış'ta oynayan yüklenmiş kısa videonun zaman çizgisinden elle ileri alma işlemi sonrasında görüntü yeni konuma hemen geçmiyor. Yaklaşık **8–20. saniyeler boyunca içerik aynı karede kalıyor**, 21. saniye civarında görüntü değişiyor. Bu aralıkta statik kamera sahnesi ihtimali olsa da tekrarlanan kareler ve kullanıcının doğrudan geri bildirimi önemli bir seek/decoder gecikmesine işaret ediyor. Görünür uygulama çökmesi yok.
- İlk 0–3 saniyede de yeni video yükleme spinner'ı görünüyor; onu **manuel seek gecikmesiyle aynı hata sanma**. Yüklenmiş kaynak videonun TikTok filigranı veya içeriğini uygulama marka hatası diye etiketleme.

**Teknik inceleme / yapılacaklar:**
1. Akış `VideoPlayerController.seekTo` ve zaman çubuğu gesture kodundaki `seekTo` çağrılarını incele. Sürükleme boyunca ağ/decoder için çok sayıda yarışan istek göndermek yerine önizleme/progress'i kullanıcıya anlık göster, `onChangeEnd` sonrası son konuma tek asıl seek çağrısı yap; gerekiyorsa 100–200 ms debounce/throttle kullan.
2. Eski seek istekleri yeni seçilen konumu geri yazmasın (nesil/token kontrolü); oynatıcı yeniden kurulmasın; kullanıcı ileri aldığında son kare veya küçük, anlaşılır `Video hazırlanıyor` göstergesi ile ekran donmuş gibi kalmasın. Seek tamamlandığı gerçek medya pozisyonunda gösterilsin, oynatma durumu ve ses korunarak devam etsin.
3. Uzak video `Range`/CDN keyframe/codec desteğini ve buffering state'ini denetle; çok uzun keyframe aralığı veya `seekTo` sonrası network yeniden doldurma ihtimalini araştır. Başka kullanıcı videolarını/kaliteyi silme veya değiştirme.
4. **Kabul:** Tek cihazda aynı tür 30–60 sn videoyu üç farklı konuma (ör. ortası, sonuna yakın, geriye) sürüklediğinde gösterge yeni konuma anında tepki versin, kare kabul edilebilir kısa sürede güncellensin; donma 10+ sn sürmesin. Ağ/cihaz kaynaklı bekleme durumunda spinner/açık hata gösterilsin. Önceki oynatma, otomatik kaydırma, 0.5x–2x hız, pause/play, Kaydet/Araçlar/Paylaş işlevleri korunacak.

**Durum:** Gerçek telefon video gözlemiyle **AÇIK, henüz düzeltilmedi**. Sonraki toplu yamada öncelikli; yeni APK üretimi yok.

### B. P3 — Sol üstte büyük N logo fazlalığı (45186.jpg)
- Kullanıcı Akış ekranının en üst solunda görünen **büyük renkli N logosunu kaldırmak**, yanında yalnız **`NgelX` yazısını korumak** istiyor.
- Sadece **Akış AppBar/üst başlığı** kapsamda. Takip / Sana Özel sekmeleri, arama ikonu, üst güvenli alan, alt navigasyon ve marka yazısının mevcut konumu/dengesi korunacak. Profil/Üret/diğer sayfalardaki logolara gereksiz yan etki yapma.
- **Kabul:** Akış üstünde renkli N logosu görünmez, yalnız NgelX metni düzgün sola hizalanır; dar ekranlarda çakışma yaşanmaz.

**Durum:** Bu talepler şimdi GitHub Work QA kaydında; kodlanmadı, Build 406 APK değişmedi. `Gelen Kutusu gönderici isimleri`, `Üret` ve diğer `Akış` rötuşları ile birleştirilecek. İkinci telefon testleri ertelenmiş kalır.

## Akış — zaman/tarih etiketini kısaltma (2026-10-08, @dilekizmmz örneği)

**Kullanıcı isteği:** Akış'ta kullanıcı adı/açıklama yakınındaki `12 dk önce • 08.10.2026 • 21:56` satırı fazla uzun görünüyor. Özellikle video üstündeki metin kalabalığı azaltılsın, ama gerçek paylaşım tarihi kaybolmasın. Kullanıcı öneri de istedi.

**Önerilen UX / sonraki toplu düzeltmeye kayıt (P3):**
- Akış'ta yalnız kısa göreli zaman: `12 dk önce`, `3 sa önce`, `2 gün önce` vb. gösterilsin. Gereksiz tekrar edilen `08.10.2026 • 21:56` aynı satırda yer almasın.
- Kullanıcı kısa zamana dokunduğunda bilgi balonu/alt pencere ya da gönderi ayrıntısında `08.10.2026 • 21:56` tam tarih ve saat gösterilsin. Etkin olmayan dekoratif simge yerine erişilebilir tıklanabilir tarih sunulsun.
- Yerel saat dilimi kullan, oluşturulma zamanı `createdAt` ve sıralama verileri değiştirilmesin; zaman hesabı geçmiş/future, yeni paylaşım, 1 gün ve yıl sınırlarında doğru kalsın. Uzun kullanıcı adı veya büyük fontta satır taşmasın.
- Paylaşım yazısı, kullanıcı adı, video ve diğer aksiyonlar korunacak. Üstteki büyük N logosunu kaldırma ve `seekTo` gecikmesini giderme notlarıyla **tek Akış tasarım/performans paketinde** ele alınsın.

**Durum:** Kullanıcıya öneri olarak sunuldu, GitHub QA/Work notlarına kaydedildi; **kod değiştirilmedi / yeni APK oluşturulmadı**.

## NgelX arama alaka düzeyi — TikTok örnek videosu 45185.mp4 (2026-10-08)

**Kullanıcı isteği:** "Arama kısmına örneğin Cemil Tugay yazdım bak aynı Cemil Tugay videoları çıkıyor onu da not et." Bu yaklaşık **40,5 saniyelik referans video**, **TikTok uygulaması** içindeki arama örneğini gösteriyor; doğrudan NgelX'in çalışmadığına veya NgelX'te mükerrer kayıt üretildiğine dair ekran kanıtı **değil**. Kullanıcının örneği özellikle **aranan ad/konuyla ilgili videoların sonuçlarda görünmesi** beklentisine işaret ediyor. Video sonuçları içinde aynı kişi hakkında farklı klipler görülebiliyor; aynı video dosyasının birebir kopya olarak listelendiği bu videodan kesin çıkarılamaz.

**Sonraki toplu arama geliştirmesi (Keşfet / Akış arama) kabul kriterleri:**
1. `Cemil Tugay` gibi iki sözcüklü kişi/konu sorgusunda adı, video başlığı, açıklaması, hashtag'leri ve kullanıcı adı gibi arama alanlarından **gerçekten alakalı** eşleşen videolar göster. Hem tam ifade hem kelimelere ayrılmış eşleşmeleri dengeli sırala; harf büyüklüğü, Türkçe karakterler ve yazım varyantlarını doğru normalize et.
2. **Alaka düzeyi önce:** tam isim ve başlık eşleşmesi, konu/etiket eşleşmesi, sonra metin içindeki zayıf eşleşmeler. Güncellik ve etkileşimi yardımcı sinyal yap; yalnız popüler olduğu için alakasız videoları üste çıkarma.
3. Aynı kişinin/konunun **farklı videoları ayrı sonuçlar** olarak kalmalı. Yalnız aynı **gönderi/video kimliği** arama sonucu sorgu birleşiminde birden çok kez geliyorsa sonuç listesindeki tekrarları temizle; yanlışlıkla ilgili videoları silme.
4. `Videolar` sekmesi varsa klipler orada listelensin; arama tipi `Kullanıcılar / Videolar / Fotoğraflar / Canlı` ayrımında filtreler doğru çalışsın. İçerik gizliliği, engellenen hesaplar, silinmiş içerikler ve moderasyon filtreleri korunmalı.
5. Arama sonuç kartında açıklama, hesap adı, mümkünse gerçek video posteri göster; karta dokununca **doğru video** açılıp oynasın. Sonuç sayfalandırma/pagination ve boş/az sonuç durumları test edilsin. Metin aynı olsa bile farklı UID/post id'leri yanlış birleştirilmesin.
6. Küçük kapsamlı telefon testi: `Cemil Tugay`, daha uzun `Cemil Tugay konuşması`, kısmi/yanlış yazım ve alakasız sorguda beklenen sıralama/kapsam; yeniden aramada aynı post çoğalmamalı.
7. **Önemli ayrım:** Kullanıcı örnek olarak **TikTok** videosu verdi. Bu kayıt, NgelX'in gerçek arama sonuçları için bir hata teşhisi değil; **ürün davranışı/arama kalitesi geliştirme isteği**dir. Kod ve Firestore dizin/query/index yapısı incelenmeden hazır/bozuk denemez.

**Durum:** Work QA'da **kayıtlı**, henüz kodlanmadı / yeni APK oluşturulmadı. Kullanıcının kabul ettiği tek toplu düzeltme paketinde `Gelen Kutusu gönderen adları`, `Üret` ve `Akış` eksikleriyle birleştir.

## Akış üst sekmeleri — kullanıcı tarafından onaylanan özgün isimler (2026-10-08)

**Kesin kullanıcı kararı:** NgelX Akış üstündeki TikTok'u çağrıştıran `Takip | Sana Özel` sekme başlıklarının yerine **`Çevrem | Radar`** kullanılacak. Bu isimler artık bir öneri değil, **onaylanmış tasarım gereksinimi**.

**Anlamı ve fonksiyon koruma:**
- **Çevrem** = önceki `Takip` sekmesi; kullanıcının takip ettiği hesapların içerikleri. Var olan takip-akışı veri sorgusu ve hesap/gizlilik filtreleri korunacak.
- **Radar** = önceki `Sana Özel` sekmesi; ilgi alanlarına/önerilere dayalı içerik akışı. Mevcut öneri, sıralama, sayfalama ve oynatma mantığı korunacak.
- Başlangıçtaki seçili sekme ve alt çizgi/aktif renk tasarımı mevcut davranışla aynı kalsın; sadece görünen metinler değişsin. Başlıklar dar ekran ve büyük fontta taşmadan yan yana sığmalı.
- Akış üst solundaki **büyük renkli N logosu kaldırılacak, yalnız `NgelX` yazısı kalacak** (önceden kayıtlı onay); arama ikonu korunacak.
- Seçili sekme, takip etme durumu, video ileri sarma ve diğer Akış davranışları etkilenmemeli. Metin değişikliği backend veri yapısı/sekme anahtarlarını gereksiz yere değiştirmemeli.
- Sekme adları uygulamanın diğer yerlerinde kullanıcıya gösteriliyorsa tutarlı dil kullan; farklı veri filtrelerinin semantiğini yanlışlıkla birleştirme.

**Kabul:** Akış başlığı **`NgelX      Çevrem    Radar    [arama]`** anlamını verecek; aktif sekme vurgusu yerinde, iki sekme tıklanınca sırasıyla takip edilenler ve önerilenler açılacak. `Takip | Sana Özel` üst sekme yazıları artık görünmeyecek.

**Durum:** GitHub Work QA notuna **kullanıcı onaylı** olarak eklendi. **Henüz kod değişmedi; Build 406 APK aynı.** Bildirimler, Üret ve Akış'ın kalan işleriyle sonraki tek düzeltme paketinde kodlanacak.

## ONAYLANMIŞ KAPSAM DEĞİŞİKLİĞİ — davet bağlantısı ile katılımda kurucu/yönetici onayı zorunlu (2026-10-08)

**En son kullanıcı kararı (önceki kararın yerini alır):** Kullanıcı geçerli grup davet bağlantısı/koduyla başvursa **bile otomatik üye yapılmayacak**. Talep önce **grup kurucusu veya yetkili yöneticinin onayına** düşecek. Bu, daha önceki "davet koduyla yönetici onayı olmadan doğrudan katıl" isteğini **iptal eder**; nihai ürün gereksinimi budur.

### Beklenen akış
1. Kullanıcı aktif/geçerli davet bağlantısı ya da kodunu girer, **Gruba katıl** seçer. Sistem gerçek üyelik oluşturmak yerine `pending` **katılma isteği** üretir ve kullanıcıya **"Katılma isteğin yönetici onayına gönderildi"** geri bildirimi verir.
2. Grup **kurucusu veya yetkili yöneticileri**, bekleyen isteği bildirimler/katılma istekleri ekranında gerçek gönderen adı ve avatarıyla görür. **Kabul et / Reddet** eylemleri çalışır.
3. Yalnız sunucu tarafında doğrulanmış yetkili kurucu/yönetici onayı sonrasında kullanıcı `members` listesine eklenir, grup sohbeti açılır; onaydan önce özel grup mesajları ve üye verilerine erişim verilmez.
4. Reddedilen istek üyelik yaratmaz; başvuran doğru sonuç bildirimi alır. Zaten üye olan kişi yeniden istek göndermeden grubu açabilir; çift tıklama yinelenen `pending` kayıtları oluşturmaz.
5. Silinmiş, iptal edilmiş veya süresi dolmuş davet; engellenen kişi; kapalı/silinmiş grup ve **grup kapasite limiti** mevcut güvenlik kurallarına tabidir. Kurucu/yönetici dışındaki kullanıcılar kendilerini veya başkalarını onaylayamaz.

### Kritik kod ve sunucu işi
- **Build 406'da doğrudan katılım (`autojoin`) uygulandı ve `ngelx-44eed` canlı Firestore kuralları yayımlandı.** Yalnızca ekrandaki metni değiştirmek YETERLİ DEĞİL. **Gelecek tek paket düzeltmede uygulama akışıyla birlikte Firestore `validSelfJoin` ve `joinRequests` yetki kurallarında davet koduna dayanarak onaysız `autojoin` yetkisini kaldır/güvenli şekilde sınırla.** Sunucu tarafı kısıt geçerli olmadan "onay zorunlu" tamamlandı sayılmayacak.
- Bekleyen istek `pending` yönetici onayı, kullanıcı yetkisi, bildirimler ve reddetme işlemleri gerçek Firestore emülatör testlerinden geçmeli; özellikle **geçerli link sahibi kullanıcı doğrudan `members` dizisine kendini ekleyememeli** testi zorunlu.
- Bu yeni karar, önceki QA notları veya önceki Build 406 uygulamasıyla çelişirse **bu en son kullanıcı kararı önceliklidir**. Daha önce yazılı "davetle direkt katılım" maddeleri artık uygulanacak hedef değildir.
- **Durum:** En son onaylı gereksinim olarak Work notuna kaydedildi; henüz kod/kurallar değiştirilmedi. **Mevcut Build 406'da davetle onaysız katılım mümkün olabilir.** Sonraki toplu düzeltme paketinde güvenli şekilde yeniden kodlanmalı ve canlı Firebase kuralları yeniden dağıtılmalı. İkinci telefon senaryoları kullanıcının isteği üzerine ertelenmiştir.
