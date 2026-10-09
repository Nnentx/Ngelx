# NgelX — Build 421 cihaz testi / 1. video (45335.mp4)

**Kayıt:** 09.10.2026 · yaklaşık 2 dk 38 sn · Android ekran kaydı.  
**Değişiklik ilkesi:** Video QA gözlemleri burada toplanır. Bu kayıtla **kod değiştirilmez**; diğer video gelince birleşik Work düzeltme planı çıkarılır.  
**Sürüm ihtiyatı:** Bu kayıtta `Ayarlar > Sürüm` ekranı açılmadığı için çalışan APK'nın Build 421 olduğu doğrudan doğrulanamadı. Videonun son kesiminde cihaz saatinin 12:55'ten 23:08'e atladığı görülüyor; son hikâye klibi farklı oturumdan/ayrı kesitten olabilir.

## Doğrudan görülen sorunlar

| Zaman | Öncelik | Bulgu | Kanıt / beklenen |
| --- | --- | --- | --- |
| **02:28–02:33** | **YÜKSEK** | Hikâye yanıtı gönderimi başarısız. | Hikâye oynarken altta mavi **“Hikâye yanıtı gönderilemedi.”** uyarısı görülüyor. Önceki Build 413 hikâye cevabı düzeltmesi yapıldığı hâlde gerçek kullanılan APK/senaryoda hata devam edebiliyor. Mesaj gizlilik izni, hikâye sahibinin UID'si, chat oluşturma ve Firestore hatası ayrı ayrı incelenmeli; kesin kök neden yalnız videodan çıkarılamaz. |
| **00:04–00:14, 00:28** | **DÜŞÜK/UX** | Kapak fotoğrafı üzerindeki siyah **“Kapak fotoğrafını değiştir”** eylem alanı görseli fazla örtüyor. | Profilin üst kapak fotoğrafının kenarında koyu etiket görülüyor. Kamera simgesi ve dokunma alanı korunarak daha sakin tasarım değerlendirilmeli. |
| **01:24–01:30** | **DÜŞÜK/İZLENECEK** | Başka bir profil açıldığında sayaç alanında geçici yükleme göstergesi görülüyor. | Profil fotoğrafı ve tanıtım videosu alanları görünürken sayılar kısa süre gecikiyor, ardından 5/2/14/3 yerleşiyor. Kalıcı hata değil; bekleme görünümü/layout shift iyileştirilebilir. |
| **00:18–00:22** | **BELİRSİZ** | `ad` aramasında yükleme simgesi görünüyor. | Kullanıcı başka uygulamaya geçtiği için sonucun gelip gelmediği görülmüyor. Bu video **“Adem bulunamadı”** sorununu yeniden kanıtlamaz. |

## Bu videoda çalıştığı görülenler

1. **00:04–00:14, 00:28 ve 01:28–01:40:** Kapaklı Rojin ve Dilek profilleri açılıyor; avatar, kapak, katılım tarihi, dört sayaç ve tanıtım videosu önizlemesi görünüyor.
2. **00:32–00:36, 01:48:** Rojin'in Arkadaşlar sayfasında üç kişi listeleniyor. Adem ve Dilek satırlarında **“Arkadaşın · 1 ortak arkadaş”**, Sultan'da **“Arkadaşın”** yazıyor. Önceki yanlış-ilişki etiketi bu kayıtta düzelmiş görünüyor.
3. **00:48–00:56:** Gizlilik seçenekleri (gizli hesap, profil görünürlüğü ve diğer tercihler) açılıyor. Gizli hesap açık olsa bile “Herkes” izninin kapsamı açıklama metninde anlatılmış; bunun doğrudan veri sızıntısı olduğu çıkarılamaz.
4. **01:00–01:06:** Engellenen/erişime izin verilmeyen profil **“Bu profile erişilemiyor”** uyarısı gösteriyor; engellenen profile paylaşım girişiminde de uyarı çıkıyor.
5. **01:12–01:16:** Aktivite bildirimleri (takip, arkadaşlık, grup vb.) listeleniyor. Bu yalnızca **liste görünürlüğünü** doğrular, yeni gönderilmiş bildirimin karşı telefona anında ulaştığını doğrulamaz.
6. **01:16–01:24:** Gelen Kutusu sohbet listesi açılıyor.
7. **01:40–01:44:** Genel aramada `r` sorgusuyla kullanıcı ve paylaşım sonuçları görüntüleniyor. Bu, en azından bu sorgunun sonuç döndürdüğünü doğrular.
8. **01:48–01:56:** Takip edilenler listesinde 5 kişi görülüyor ve Dilek profili açılabiliyor.
9. **01:56–02:08:** Dilek'in profili **“Takip ediyorsun”** ve **“Arkadaşsınız”** durumlarını aynı anda gösteriyor; iki farklı ilişki türünün ayrımı doğru. `1 gündür arkadaşsınız` bilgisi görünüyor.
10. **02:08–02:12:** Profil paylaşımı -> NgelX içinde özele gönder -> kişi seçimi -> **“1 kişiye profil gönderildi ✅”** mesajı görülüyor.
11. **02:12–02:20:** Dilek ile sohbet açılıyor, gönderilmiş profil bağlantısı ve mesaj kutusu görünüyor. Buradan mesajın karşı cihazda okunduğu sonucu çıkarılmaz.
12. **02:24–02:32:** Hikâye oynatma arayüzü ve emoji/yanıt kontrolleri açılıyor; yanıt hatası ayrı madde.

## Bu kayıttan kesin test edilemeyenler

- Yeni kurulan **Build 421** sürümünün tam sürüm numarası ve imzası (ayarlar/sürüm ekranı yok).
- **Kapaksız** sahibin ve ziyaretçi profilinin yeni kompakt görünümü (kapaklı profiller gösterilmiş).
- Hikâyede yeni **tam paylaşım tarihi / bitiş tarihi / kalan süre** panelinin aynı Build 421 üzerinde çalışması: son kesimde arayüz ve saat farklılaşıyor, güvenilir sürüm eşlemesi yok.
- Yeni takip/arkadaşlık isteğinin gerçekten **gönderici ve alıcı** hesaplarda aynı duruma dönüşmesi, kabul/ret ve bildirim teslimi.
- `ad` arama sorgusunun tamamlanması ve Adem'in bu arama kapsamından bulunması.

## Toplu düzeltme paketine aktarım

- **Öncelik 1:** Hikâye yanıtı başarısızlığını, Build 421 cihaz sürümü doğrulaması sonrası gerçek hata koduyla araştırmak (UID, gizlilik, iki kişilik sohbet, Firestore batch, gönderi tipi).
- **Öncelik 2:** Profil yükleme titreşimi ve kapak üstündeki eylem etiketinin görsel sadeleşmesi (çalışan işlevleri bozmadan).
- **Öncelik 3:** İkinci video gelince hesaplar arası takip/arkadaşlık, arama, bildirim ve hikâye kontrollerini birleştirerek tek Work QA listesi hazırlamak.

**Not:** Bu dosya yalnızca kayıt ve analizdir; üretim verileri, kod veya test hesapları üzerinde değişiklik yapılmadı.
