# NgelX Build 407 — Tek Paket Çalışma ve Teslim Kontrolü

**Temel kaynak:** `QA/BUILD-406-EIGHT-FIXES-RELEASE.md` ve kullanıcının en son kararı: **geçerli grup daveti de kurucu/yönetici onayı bekleyecek**. Mevcut Build 406 fotoğraf/video paylaşımı, sohbet, canlı yayın, sesli oda, profil, hikâye, kaydedilenler ve Firebase verileri korunacak.

## Kodlanan işlerin kapsamı (telefon testi henüz yapılmadı)
- **P1 / Grup güvenliği:** davet kodu sadece `pending` katılma isteği oluşturur, `chats.members` alanına başvuran kendini ekleyemez, kullanıcıya bekleme mesajı gösterilir. Kurucu/yöneticiye best-effort bildirim; yönetici listesinde bekleyen kayıt görünürlüğü korunur. Eski Build 406 `autojoin` başvurularını güvenle `pending` durumuna yenileme. Onay ve ret yalnız kurucu/yönetici yetkisinde. **App kodu + Firestore kuralları birlikte**.
- **P1 / Bildirimler:** Gelen Kutusu `Tümü` ve `Bildirimler` satırlarında gerçek gönderen UID→user profilinden ad ve avatar çözümü (Build 406 yalnız `Aktivite` satırında çözmüştü). Eski bildirimler ve silinen hesabın açık yedek metni. İstekler/Aktivite akışları korunur.
- **P2 / Akış:** `Çevrem | Radar` onaylı sekme adları, Akış'a özgü büyük renkli N ikonunu kaldırıp `NgelX` yazısını koruma, sadece kısa göreli zaman (`12 dk önce`) ve dokunmayla gerçek tarih tooltip'i, video seek esnasında çoklu yarışan `seekTo` isteklerini kaldırma.
- **P2 / Üret:** Dar kartta tam kelimeli başlık/alt metin için ölçekli yerleşim; `Canlı Yayın` sekme adının kesilmesini azaltma; yayınlanma sonrası kısa 3 saniyelik floating snackbar.
- **P2 / Arama:** İki sözcüklü Türkçe ad/konu (`Cemil Tugay`) eşleşmesi, başlık/açıklama/etiket/kullanıcı adı ve yerel alaka sıralaması. Kaynak sorgu ilk 100 kayıtla sınırlı kalabilir; tüm ölçekli dizin araması henüz bu değişiklikle tamamlandı sayılmaz.

## Açık kalan / tam yapılmadığı için tamamlandı denmeyecek işler
- Tam işleyen **Anket** oluşturma, oy verme, oy sayımı ve Firestore kuralları (önce mevcut model ve içerik sayfalarıyla uyumlu tasarlanmalı; yarım sahte anket teslim edilmeyecek).
- Akış Araçlar menüsü bölümlemeleri, `İlgilenmiyorum` ile `İçeriği gizle` açıklamaları ve video geçişlerinin tüm ağlarda sıfır bekleme garantisi.
- Profil medya cache yükleme sorunları, Kaydedilenler ve gizlilik açıklamalarının yeni telefonda son kontrolü.
- Gerçek uçtan uca grup davetinin karşı yönetici tarafından alınması, ses, PK, alıcı bildirimleri gibi **ikinci telefon testleri kullanıcının kararıyla ertelendi**.

## Build 407 teslim güvenlik kapıları
1. Mevcut 395–406 koruma betikleri ve `tools/apply_build407_consolidated.py`, `tools/check_build407_regression.py`.
2. Firestore emulator: geçerli davette `pending` başarılı, `autojoin` ve kendi `members` listesine yazma **reddedilir**; yalnız yetkili admin ekleyip isteği kabul edebilir; diğer admin olmayan işlem başarısız.
3. Flutter analyze, imzalı release APK `1.0.183+407`, sha256 ve GitHub artifact; ardından doğrulanmış `firestore.rules` dosyasını `ngelx-44eed` projesine dağıt. Dağıtım başarılı olmadan admin onayı zorunlu canlı sistem olarak duyurulmayacak.
4. Tek telefon kısa smoke: Ayarlar 407, Akış yeni başlıklar ve seek, Bildirimler gerçek gönderen, Üret etiket, aramada çok kelimeli sorgu. İkinci telefona ihtiyaç olmayanlar bile test edilmeden onaylı sayılmaz.

**Durum:** GitHub Work çalışma dalında kodlama ve CI devam ediyor. Kullanıcı kayıtları silinmeyecek, Build 406 telefon APK'si uzaktan güncellenmiş sayılmaz.

## Build 407 otomatik teslim ve Firebase güvenlik dağıtımı SONUÇ (2026-10-08)

- Workflow: https://github.com/Nnentx/Ngelx/actions/runs/37834541785
- **Build job: SUCCESS; deploy-rules job: SUCCESS**.
- Sürüm: **1.0.183+407**. Python 395–407 koruma testleri, Build 407 kod uygulama/özellik kontrolleri, Firebase emülatör güvenlik testleri, Flutter analyze, imzalı APK build/apksigner, SHA256 ve GitHub artifact upload başarılı.
- APK ZIP: https://github.com/Nnentx/Ngelx/actions/runs/37834541785/artifacts/11575562209 — `NgelX-1.0.183-Build-407-CONSOLIDATED`. ZIP içindeki APK ve .sha256 dosyasını telefonda kullan.
- Emülatörden geçmiş güvenlik kuralları artifact: https://github.com/Nnentx/Ngelx/actions/runs/37834541785/artifacts/11574807049.
- **Canlı Firebase güvenlik dağıtımı DOĞRULANDI:** `deploy-rules` GitHub Actions logları `Deploying to 'ngelx-44eed'`, `rules file firestore.rules compiled successfully`, `released rules firestore.rules to cloud.firestore`, `Deploy complete!` çıktılarını doğruladı. Böylece Build406'da izin verilen özel link `autojoin` yolu üretim Firestore kurallarında kapatıldı; davet linkiyle katılım için `pending` ve kurucu/yönetici onayı beklenir. Bağımsız keşfedilebilir/açık gruplarda izinli genel katılım kuralları kapsam dışında korunmuştur.
- **Telefon testi sınırı:** APK CI başarıyla üretildi, ama bu Build407 APK'nin gerçek Android cihazda kurulduğu ve sekme/tarih/seek/bildirim davranışlarının telefonda geçtiği henüz kanıtlanmadı. İkinci telefon testleri ertelendi. Karmaşık anket oluşturma/oylama özellikleri ve tüm ölçekli indeksli arama halen yapılmadı; **22 başlığın tamamı bitmiş** denmeyecek.
- **Kısa doğrulama:** v1.0.183 Yapı 407, `NgelX | Çevrem | Radar`, süre etiketi, manuel video ileri sarma, Bildirimler ve Tümü gerçek gönderen adları, Üret kart etiketleri, başarılı paylaşım toast; daha sonra geçerli linki olan başvuranın yönetici onayına düşmesi (özel güvenlik kuralları üretime dağıtıldı, iki hesap E2E beklemede).

## Build 407 gerçek cihaz / Akış manuel ileri sarma kontrolü — 45215.mp4 (2026-10-08)

**Kaynak:** Kullanıcının gönderdiği yaklaşık **41,9 saniyelik 1080×2392** Android ekran kaydı. Daha önce Ayarlar'da **v1.0.183 / Yapı 407** ve Akış'ta **NgelX | Çevrem | Radar** görünümü telefon ekranıyla doğrulandı.

**Gözlemler:**
- **0–9 sn:** `Radar` akışında 34 saniyelik video oynuyor. Kullanıcının video zaman çubuğuyla etkileşimi sırasında **`00:07 / 00:34`** önizleme göstergesi beliriyor; ilerleme çizgisi ve videodaki görüntü daha ileri sahnelere geçiyor. Önceki Build 406 videosunda iletilen yaklaşık 10 saniyeyi aşan aynı karede kalma davranışı **bu kayıtta tekrarlanmıyor**.
- **9–14 sn:** Görüntü `TikTok` yazılı outro'ya geliyor; bu yazı **yüklenen videonun içeriği**, NgelX tarafından yeni eklenen uygulama logosu olarak değerlendirilmemeli.
- **14–17 sn:** Bir sonraki videoya geçerken kısa siyah ekran ve turkuaz spinner görünüyor; ardından `selam yazii` videonun içeriği açılıyor. **Başka videoya ilk girişte kısa medya yükleme**, manuel seek donmasıyla karıştırılmamalı.
- **18–24 sn:** `Çevrem` sekmesine geçiş, kısa yükleme ve paylaşımlar gözleniyor; ardından profil/arama açılıyor. Bu bölüm video ileri sarma testinin kapsamına girmez.
- **34–42 sn:** `Radar` fotoğraf içerikleri kaydırılıyor; sabit fotoğraflardaki değişmeyen sahneler seek gecikmesi sayılmamalı.
- Kayıt boyunca uygulama çökmesi veya uzun süre boyunca kilitlenmiş ekran görünmüyor.

**QA kararı:** **Build 407 video ileri sarma için tek cihaz smoke — OLUMLU; önceki uzun donma tekrar etmedi.** Ancak cihazın gerçek `seekTo` tamamlanma zamanını ölçen telemetri ve farklı ağ/video kodlayıcılarında tekrar test olmadığı için her koşulda kesin kapandı iddiası yok. **Ayrı P2 açık performans rötuşu:** yeni videoya geçişte yaklaşık 1–3 saniyelik siyah ekran/spinner görülebiliyor; poster/buffer göstergesi ve medya ön yükleme iyileştirmesi sonraki toplu paket için kayıtlı. TikTok outro, kullanıcının yüklediği kaynak medyanın kendisidir.

**Bu işlem:** QA notu; **mevcut Build 407 kaynak kodu/APK ve canlı Firebase kuralları değiştirilmedi**. İkinci telefon testleri kullanıcı isteğiyle beklemede kalır.

## Build 407 gerçek cihaz / Gelen Kutusu gönderen adı ve yönetici onaylı grup daveti — 45216.mp4 (2026-10-08)

**Kaynak:** Kullanıcının paylaştığı **174,44 saniyelik / 1080×2392** Android ekran kaydı, daha önce ekrandan **v1.0.183 / Yapı 407** doğrulandı. Bu kayıtta birden çok hesap arasında geçiş, grup daveti başvurusu ve yönetici onayı tek cihazda gösteriliyor. Test sonucu yalnız gözlenmiş davranışa dayanır.

### Doğrulanan olumlu sonuçlar
- **00–24 sn:** Gelen Kutusu `Tümü`, `Mesajlar`, `Gruplar`, `Bildirimler` sekmeleri açılıyor ve bildirimler yükleniyor. `Bildirimler` sekmesinde **Umay Umay seni takip etmek istiyor**, **Alperen Yarbay sana arkadaşlık isteği gönderdi**, **Alperen Yarbay seni takip etmek istiyor**, **Rojin Candan** ile başlayan canlı yayın/bildirim satırları gerçek adlarla görüntüleniyor; bazı satırlarda gerçek avatar var. Build 406'daki isimsiz `seni takip etmek istiyor` ve `sana arkadaşlık isteği gönderdi` şikâyeti bu kayıtta **tekrarlanmadı**.
- **24–29 sn:** `İstekler` sekmesi açılıyor; istek kategorileri gösteriliyor. `+` menüsünden `Gruba katıl` sayfası açılıyor.
- **42–65 sn:** Mevcut grup sohbeti, **Grup ayarları**, **Davet bağlantısı** ve `Davetler / Katılma istekleri` alanı görüntüleniyor. Gerçek grup davet bağlantısı oluşturulabiliyor/kopyalanabiliyor; grup gizlilik ve katılma isteğini onaylama ayarı mevcut.
- **76–95 sn:** Hesap değiştirme üzerinden başvuran hesapta `Gruba katıl` alanına davet bağlantısı giriliyor. `Gruba katıl` seçilince **`Katılma isteğin kurucu veya yönetici onayına gönderildi.`** bildirimi görünüyor ve doğrudan grup sohbeti açılmıyor. **İlk adım geçti**: davet linki kendiliğinden üyelik yaratmıyor.
- **110–140 sn:** Yönetici/kurucu tarafında `Aktivite` ve grup sohbetinde **`Rojin Candan ALE YNA AŞK grubuna katılmak istiyor`** bildirimi görünüyor. Grup sohbetinde üstte **`1 katılma isteği var`** uyarısı, `Davetler ve istekler` sayfasında **Rojin Candan** gerçek adı/avatarsıyla `Onayla` ve `Reddet` eylemleri var. Kullanıcı **Onayla** seçeneğine dokunuyor, istek sayfadan kayboluyor ve **`İstek onaylandı.`** bildirimi gösteriliyor. **Yöneticiye ulaşma ve onaylama tek cihazlı hesaplar arası test geçti**.
- **144–168 sn:** Grup sohbetine geri dönüş ve mesaj / etiketleme denemeleri var; uygulama çökmesi veya kalıcı bloke görünmüyor.
- **170–174 sn:** Gelen Kutusu `Tümü` yeniden açılıyor; gönderen isimleri görünür.

### Sınırlar ve küçük takip
1. **P1 bildirimlerde gönderen adları:** Bu kayıtta `Tümü` ve `Bildirimler` isimli satırları doğru gösteriyor; **tek cihaz smoke geçti**. Silinmiş hesap, eski UID'siz arşiv kaydı ve tüm fotoğraflar ayrı denenmediğinden evrensel doğrulama sayılmaz.
2. **Grup davet yönetici onayı:** Başvuru `pending` akışı ve onay butonunun sonucu görülüyor. **Başvuran hesaba tekrar dönüp yeni üyelik kaydı, grup mesajlarına erişim ve onay bildirimi açıkça doğrulanmadı**; grup onayı E2E'nin bu son adımı için hedefli kontrol gerekir.
3. **P3 bildirim durumu metni:** Onaydan sonra, son `Tümü` listesinde önceki bildirim **`Rojin Candan ALE YNA AŞK grubuna katılmak istiyor`** olarak duruyor. Bu yalnız geçmiş başvuru bildirimi olabilir; **isteğin hâlâ pending olduğunu kanıtlamaz**. İyi UX için sonuçlanmış istekte geçmiş bildirimi `gruba katılma isteği onaylandı` gibi güncelleme veya durum rozeti gösterme incelensin. Eski bildirim silinmesin.
4. Bildirimlerdeki bazı mesaj/istek türleri ile grup yöneticisi rolünü değiştirme ve gerçek ikinci cihaz teslimi bu kayıtla tamamen doğrulanmadı.

**QA kararı:** Build 407 **gönderen adları gerçek telefon testinde GEÇTİ**. **Davet linkiyle yöneticiye istek gönderme ve yöneticinin isteği onaylaması GEÇTİ**. **Onaylanmış başvuranın yeni grup üyeliğine erişimi — ayrı kısa doğrulama bekliyor**. Toplu geri kalan düzeltmelere dokunulmadı; QA raporu güncellendi, **APK/kod/Firebase değiştirilmedi**.

## Gerçek Android / 45219.mp4 — ALEYNA AŞK grup sohbeti ve renkli Grup etiketi talebi (2026-10-08)

**Kaynak:** Kullanıcının yaklaşık **54,1 saniyelik** Android ekran videosu. Kullanıcı bu videonun incelenip incelenmediğini tekrar sordu; önceki cevapta yalnızca "Grup" rozeti tasarımı konuşulmuş, videonun somut test sonucu verilmemişti.

**Gözlemlenenler:**
- Gelen Kutusu > Tümü listesinde **ALEYNA AŞK** sohbeti ve diğer özel/grup sohbetleri birlikte görünüyor (ilk 0–3 sn).
- Sohbete girildiğinde **ALEYNA AŞK** üst başlığı, grup mesaj geçmişi, yazma alanı, kalp/mesaj ve grup işlemleri görünür; kayıt içinde kısa metin yazma/gönderme denemeleri ve gruptaki mesajlar bulunuyor (yaklaşık 6–16 sn ve 24–27 sn). Bu kayıtla grup ekranının **açıldığı ve sohbet içeriğinin göründüğü** doğrulandı.
- **Gruba üye ekle** seçiminde kullanıcıları seçme ekranı açılıyor; ardından **"3 üye ekleme isteği yönetici onayına gönderildi"** başarı bildirimi gösteriliyor (18–25 sn). Bu işlem başvuruların gerçekten yönetici tarafından sonuçlandırıldığını tek başına kanıtlamaz.
- Grup bilgi kartı ve grup seçeneklerinde **4 üye**, **Sohbet üyelerini gör**, **Davetler ve istekler** alanları görünüyor (yaklaşık 20–23 ve 42–44 sn).
- Aynı video içinde Gelen Kutusu > Gruplar filtresi, diğer grup listeleri açılıp yenilenebiliyor.
- **Uyarı/UX konusu:** **"Bu grupta engellediğin bir kişi var"** başlıklı güvenlik diyaloğu ALEYNA AŞK'a girişte ve başka bir grup geçişinde tekrar ortaya çıkıyor (yaklaşık 6, 33 ve 39 sn). Uyarı güvenlik için gerekli olabilir; engelleme/gizlilik koruması kaldırılmadan, tekrar sıklığı, dokunma akışı ve ilgili grup özelinde doğru tetiklenip tetiklenmediği incelensin. Engellenen hesabın bilgisi ifşa edilmesin.
- **Test sınırı:** Kayıt, yönetici onayından sonra *özellikle Rojin Candan hesabının* yeni üyelik kazandığını hesap kimliği ekranıyla kesin olarak eşleştirmiyor. Grup ekranına erişim **geçti**, ancak "Rojin'in onay sonrası erişimi uçtan uca tam kanıtlandı" iddiası yapılmayacak.

**Kullanıcının kesin yeni tasarım isteği: Gelen Kutusu / grup etiketi**
- **ALEYNA AŞK** gibi grup konuşmaları, **Gelen Kutusu > Tümü** listesindeyken normal özel mesajlarla karışmasın diye sohbet satırının **sol altındaki mesaj önizlemesi yakınına**, örneğin küçük ve yumuşak mor/mavi arka planlı **"Grup"** rozeti/etiketi gösterilecek.
- Yalnız veritabanındaki gerçek grup türüne göre göster; başlıkta "grup" kelimesi geçmesine veya kişi adına göre kestirim yapma. Grup adları, mesaj önizlemesi, son mesaj saati, okunmamış sayaç, grup fotoğrafı ve sohbeti açma davranışı korunacak.
- Normal 1:1 özel sohbetler **etiketsiz** kalacak; `Gruplar` sekmesinde aynı rozet gereksiz tekrar etmeyecekse özel olarak değerlendirilip tek biçim seçilecek.
- Küçük ekranda metin taşması ve erişilebilirlik kontrastı kontrol edilecek. Koyu büyük rozet değil, **küçük renkli "Grup" etiketi**.
- **Durum:** Kullanıcı tarafından istenmiş UI rötuşu olarak not edildi; **henüz uygulama koduna işlenmedi, yeni APK çıkarılmadı**.

**QA kararı:** ALEYNA AŞK sohbet ekranına geçiş ve grup bilgilerinin açılması tek cihaz kaydında **olumlu**. Uyarının tekrar etmesi için **küçük UX kontrol maddesi**; renkli Grup rozeti için **açık UI geliştirmesi**. Kullanıcı hesap kimliği doğrulaması ve gerçek çok cihaz testi önceki sınırlara tabidir.
