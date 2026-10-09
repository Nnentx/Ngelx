# NgelX Build 422 — Hikâye bölümü eksikleri, 45407.mp4

**Test kaydı:** 09.10.2026; yaklaşık **55,38 saniye**, Android ekranı (1080×2392).  
**Sürüm bağlamı:** Kullanıcının hemen önce gönderdiği Ayarlar görüntüsünde **v1.0.197 / Yapı 422** doğrulanmıştı. Bu kaydın kendisinde sürüm ekranı yeniden açılmıyor; bu nedenle teknik bağlam “Build 422 kurulumundan sonraki oturum” olarak değerlendirilmeli.  
**Durum:** Video ve ekran görüntülerinden gözlem kaydı. **Bu işlemde APK, kaynak kodu, Firestore ve üretim hesapları değiştirilmedi.** Kullanıcının isteği: “Hikaye bölümü eksikleri not et.”

## A. Geçemeyenler / açık sorunlar

| Zaman | Öncelik | Bulgular | Doğrulama ve kabul ölçütü |
| --- | --- | --- | --- |
| **~29–32, 35–38, 40–43 sn** | **P1 / KRİTİK** | Hikâyede `slm` metni yazılıp gönderilmek istendiğinde tekrar tekrar **“Hikâye yanıtı gönderilemedi.”** uyarısı görünüyor. Son fotoğraf hikâyesinde de aynı uyarı var. Önceki Build421 video 3'ün aynı sorunu sonradan alınan kayıtla yeniden gözlendi. | Tekil ve art arda metin/emoji cevaplarında alıcı DM teslimi gerçek iki hesapta doğrulanmalı. İstemci hatasında Firestore işlem adımı ve `FirebaseException.code` görünür/test edilebilir olmalı; gizlilik ve bloklama kuralları gevşetilmemeli. Yanıt tamamlanmadan “başarılı” gösterilmemeli. |
| **~20–26, 32–42 sn** | **P2 / GÖRSEL** | Hikâye üst çubuğunda **`@irazumayy`** kullanıcı adı 2–3 satıra kırılıyor, **“1 sa önce” / “1 dk önce”** zaman bilgisi de daralana düşüyor. Takip Et / İstek gönderildi, ses, seçenekler ve X arasında avatar/isim için yetersiz alan var. | Tek satırlı/elipsli ad, ayrı okunur küçük zaman satırı; küçük ekran ve büyük yazı ölçeği kontrolü. Takip, sesi aç/kapat, seçenekler, kapat düğmeleri korunmalı. |
| **~20–43 sn** | **P2 / EKSİK KONTROL** | Hikâye izleyicisi üstünde **yalnız göreli yayımlanma zamanı** görünür. Build 421–422'de hedeflenen **tam paylaşım tarih-saat, tam bitiş tarih-saat ve kalan süre** bu hikâye rotasında açıkça görünmüyor. | Hikâyenin kaydedilmiş `createdAt` ve `expiresAt` değerleriyle gerçek saatler net ve taşmadan gösterilmeli; alan yoksa uydurma saat yazılmamalı. Önceki zaman panelinin bu rota için çalışıp çalışmadığı kontrol edilmeli. |
| **~21–22, 27–28, 35–38 sn** | **P2 / AKIŞ** | Yanıt gönderme sırasında kısa spinner/yükleme oluyor; başarısızlıktan sonra metin yeniden yazılıyor, tekrar gönderme deneniyor. | Gönderim boyunca tek istek, istenirse retry, gönderilememe nedeni, aynı yanıtın çift gönderimini önleme. Metin başarısızlıkta kaybolmamalı. |
| **~43–45 sn** | **İNCELEME** | Hikâye ekranından Umay sohbetine geçince ekranın altında **“Hikâye yanıtı gönderilemedi”** mesajı görünmeye devam ediyor; sohbet içinde aynı dakikaya ait 👍 baloncukları var. Bunların önceki hikâye tepkileri mi normal sohbet mesajları mı olduğu videodan kesin çıkarılamaz. | Her hikâye yanıtı/emoji tepkisini `storyId`, `senderId`, `chatId` ve mesaj tipiyle eşleştir; karşı hesaptaki doğru mesajın teslimini test et. Başarılı baloncuk görüntüsünü genel hikâye yanıtı testi geçmiş sayma. |

## B. Çalışan ve korunması gerekenler

1. Genel arama `u` sorgusu, Umay ziyaretçi profilini açma (yaklaşık 12–18 sn).
2. Ziyaretçi profilindeki arkadaşlık/mesaj ve takip düğmelerinin görünmesi (yaklaşık 16–19 sn).
3. Profil hikâye halkasına dokununca **hikâyenin açılması**, fotoğraf ve video medyasının yüklenip görüntülenmesi (20–43 sn).
4. Hikâyeler arasında geçiş ve ilerleme çubukları; yeni hikâyede süre etiketi değişiyor.
5. Hikâyedeki **Takip Et → İstek gönderildi** görünümü (31–34 sn): gizli takip isteğinin UI'da oluştuğunu gösterir, karşı hesaba ulaşıp onaylandığını kanıtlamaz.
6. Hikâyenin metin yanıt alanı, gönder simgesi, emoji seçenekleri ve telefon klavyesi açılıyor. **Bu yalnız UI açılmasıdır; yanıtın gönderilmesi başarısızdır.**
7. Hikâyeden sohbetin açılması ve Umay sohbetinde geçmiş mesajların görünmesi (44–53 sn); yeni başarısız hikâye metninin alıcıya teslimini kanıtlamaz.

## C. Build 422 koduyla özel inceleme

Build 422'deki `tools/apply_build422_story_delivery.py` hikâye yanıtının yeni sohbet oluşturma yolunu değiştirdi; ancak bu kayıtta **genel** “Hikâye yanıtı gönderilemedi.” metni görülüyor. Kaydın tam derleme versiyonu, bütün hikâye açma yolları ve farklı gönderim callback'leri karşılaştırılmalı. **Tek başına bu metinden hata kodu veya kesin kök neden çıkarma.** Her görüntüleme yolunda (profil halkası, Hikâye şeridi, Keşfet, özel paylaşımlar) gerçekten aynı gönderme fonksiyonunun kullanıldığını kodla doğrula. Mevcut DM oluşturma/mesaj yetki kuralları değişmeden gerçek Firebase emülatör testleri ekle.

## D. Öncelik sırası

1. **P1:** Hikâye yanıtı gerçek gönderim ve alıcıya teslim; emoji tepkisi/metin senaryoları ve hata aşaması.
2. **P2:** Hikâye üst satırında kullanıcı adı, avatar, saat ve takip düğmesi taşma/kırpılma.
3. **P2:** Yayımlanma/bitiş tarih-saatinin ve kalan sürenin okunur gösterimi; her hikâye görüntüleme yolunda.
4. **P2/P3:** Yanıt yükleme/yeniden deneme deneyimi; başarısızlıkta mesaj taslağının korunması ve çift gönderimin engellenmesi.

## E. Regresyon sözleşmesi

Kapaklı/kapaksız profil, hikâye görüntüleme, otomatik ilerleme, medya ses kontrolü, normal/gizli takip ayrımı, mesaj gizliliği, engellenen hesap sınırları, Gelen Kutusu ve önceki Build395–422 testleri **korunmalı**.

**Rapor niteliği:** Kodlanmış düzeltme iddiası yok; videoda **başarısız** görülenler yeni Work hata listesine eklendi.