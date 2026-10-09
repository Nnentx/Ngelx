# NgelX Build 421 — 4. cihaz videosu (45372.mp4)

**Kayıt tarihi:** 09.10.2026. **Süre:** yaklaşık **54,6 saniye**. Android ekran kaydı.  
**Senaryo:** Adem hesabında kapaksız görünümü seç ve kaydet; Umay hesabına geç; arama ile Adem'in profilini ziyaretçi olarak aç.  
**Sürüm sınırı:** Bu klipte Ayarlar > Sürüm ekranı ayrıca açılmıyor. Önceki video `45362.mp4` Build421'i doğrulamış olsa da bu kayıtta numara tek başına okunmuyor.  
**İlke:** Gözlem ve regresyon testi kaydıdır; **kod, canlı veritabanı ve test hesapları değiştirilmedi**. Ekran görüntülerindeki e-posta adresleri/özel veriler rapora alınmaz.

## Doğrudan doğrulanan başarılı davranışlar

| Yaklaşık saniye | Gözlem | Sonuç |
| --- | --- | --- |
| 00:00–00:02 | Adem'in kapaklı sahibi profili açılıyor; takip 3, takipçi 2, etkileşim 51, arkadaşlar 2. | Profilin mevcut sayıları ve içerik bölümü görünür. |
| 00:02–00:11 | Profil Düzenle ekranında kapaklı ve **Kapaksız sade görünüm** seçenekleri var. Kapaksız seçildiğinde küçük önizleme kartı aynı seçimi yansıtıyor. | Seçenek/önizleme çalışıyor. |
| 00:11–00:15 | **Kaydet** düğmesine dokunuluyor; kaydediliyor yükleme durumu çıkıyor; düzenleyiciden çıkılıyor. | Kapaksız görünümün kaydedilmesi başarılı görünüyor. |
| **00:16–00:20** | Adem'in kendi profili artık kapaksız; avatar ortalanmış, kamera düğmesi yerinde, istatistik ve aksiyonlar korunmuş. | **Build421 kapaksız sahibi profili cihazda geçti.** |
| 00:23–00:27 | Hesap değiştir menüsünde Adem'den Umay hesabına geçiş başlatılıyor. | Kimlik değiştirme eylemi başlıyor. |
| 00:37–00:40 | Umay hesabının genel aramasına `uma` yazıldığında **Umay Umay** kişi sonucu görüntüleniyor. | Kısa kullanıcı adı araması sonuç veriyor. |
| 00:41–00:54 | `adem` aramasıyla **ADEM baykar** sonucu geliyor; profil açıldığında kapaksız avatar, biyografi, konum, katılım tarihi, **3 takip / 2 takipçi / 51 etkileşim / 2 arkadaş** değerleri görülüyor. | **Kapaksız ziyaretçi profili başka hesapta doğru açılıyor ve sayıların sahibi profiliyle tutarlılığı görülüyor.** |
| 00:46–00:52 | Ziyaretçi Adem profilinde **Takip ediyorsun / Mesaj / Arkadaşsınız / Ortak gruplar** düğmeleri, tanıtım videosu ve gönderiler görünüyor. | Sosyal işlem düğmeleri bu arama rotasında görünür; bu klipte dokunulup işlem yapılmıyor. |

## Kanıtlanan açık kusurlar / gözlenen iyileştirme adayları

| Yaklaşık saniye | Öncelik | Gözlem | Güven düzeyi |
| --- | --- | --- | --- |
| **00:00–00:02, 00:16–00:20** | **P2 — açık UI hatası** | **Sahip profili katılım tarihi kesiliyor:** konumla aynı dar satırda `Eylül 2026 tarihinde ...` biçiminde eksik. | **Doğrulandı**. 2. videodaki aynı hata, kapaksız görünümde de devam ediyor. |
| **00:28–00:35 (yaklaşık 8 s)** | **P2 — performans/UX** | Umay'a geçiş sonrası **siyah Akış / Radar ekranında belirgin dönen yükleme simgesi**; birkaç saniye sonra içerik yükleniyor. | **Doğrulandı: uzun geçici yükleme**, fakat kalıcı kilitlenme/çökme değil. |
| **00:42–00:47** | **P3 — performans/UX** | Aramadan Adem profilini açınca geçici karartılmış ekran / birden fazla dönen sayaç göstergesi, avatar ve video önizlemesinde kademeli yükleme. Sonunda tüm sayı ve düğmeler geliyor. | **Doğrulandı: geçici yükleme**, veri tutarsızlığı değil. |
| **00:04–00:11** | **P3 — ürün UX incelemesi** | Editörde kapaksız görünüm seçilmişken yukarıdaki mevcut kapak fotoğrafı düzenleme alanında görünmeye devam ediyor; alttaki gerçek `Kapaksız` önizlemesi doğru. | **Belirsiz kusur**: kapak görselini gelecekte yeniden kullanmak için editörde saklamak kasıtlı olabilir. Otomatik kaldırma yapılmamalı. |
| 00:42–00:44 | **Kontrol** | Arama sonucu sonrası kullanıcı profilinin ilk açılışında profil resminin yüklenmesi birkaç saniye sürüyor. | Yukarıdaki yükleme maddesiyle birlikte ele alınabilir. |

## Önceki videolarla çapraz kontrol

- Video 2'de `Kapaksız` seçeneği gösterilip **yeniden kapaklı olarak** kaydedilmişti. Bu video ilk kez seçeneğin **kaydedildiğini ve diğer hesaptan gerçekten kapaksız görüldüğünü** gösteriyor; önceki açık cihaz testi bu senaryoda kapandı.
- Video 2 ve Video 4 aynı **katılım tarihi kesilmesini** yeniden doğruluyor.
- Video 3'te açık olan **Build421 hikâye yanıtı reddi** bu videoda test edilmedi; hata açık kalır.
- Video 1'de kapak üstünde gereğinden büyük görünen değiştirme düğmesi kapaksız moda geçilince artık görünmüyor; kapaklı moddaki UX sorunu ayrıca açık.
- Video 2'de aramadan açılan profilde eylem düğmelerinin yok olduğu şüphesi, bu videoda Adem arama rotası için **tekrarlanmıyor** (düğmeler var). Başka rotaları genel geçer geçmiş sayma.

## 4 video sonrasında tek Work paketine aktarılacaklar

1. **P1:** Hikâye yanıtı gönderilemiyor; Video 3'te Build421 üzerinde tekrarlı doğrulandı. Firebase sohbet izinleri/mesaj yazma kuralı ve hata safhası test edilerek düzeltilmeli.
2. **P2:** Sahip profilindeki **katılım tarihi kesilmesini**, kapaklı/kapaksız tasarımların ikisinde de metni tam gösterecek esnek satır düzeniyle düzelt. Tarihin hesaplama doğruluğu korunmalı.
3. **P2:** Hesap değişiminden Akış/Radar'a dönüşte yaklaşık 8 saniyelik siyah yükleme ekranına bir bekleme açıklaması ve mümkünse daha hızlı ilk veri; başarısızlık ve tekrar deneme durumu sun. Sabit sürede 'çözüldü' deme.
4. **P3:** Ziyaretçi profili geçici sayaç / foto / video yükleme geçişleri ve kapaklı profil değiştir düğmesinin fazla örtmesi.
5. **Açık cihaz QA:** Yeni arkadaşlık isteği/karşı hesap bildirim teslimi, hikâye tarihi/yanıt, mesajın karşı hesapta teslimi, istek geri çekme, gerçek avatar değiştirme ve gruplar/gönderi kaydetme.

**Bu video için kod değişikliği yapılmadı. Çalışan kapaksız görünüm korunmalı.**
