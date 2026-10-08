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
