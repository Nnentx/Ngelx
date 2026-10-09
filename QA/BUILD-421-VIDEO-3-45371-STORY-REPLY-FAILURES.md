# NgelX Build 421 — 3. cihaz videosu (45371.mp4)

**Kayıt:** 09.10.2026 · yaklaşık 59,7 saniye · Android ekranı.  
**Sürüm doğrulama:** Kayıtta Ayarlar ve gizlilik > Uygulama güncellemeleri bölümünde **v1.0.196 / Yapı 421** gösteriliyor.  
**Amaç:** Bu, Video 1 (`45335.mp4`) ve Video 2 (`45362.mp4`) ardından üçüncü, ayrı QA gözlemidir. Kod/sunucu verisi değiştirilmedi.

## Kritik bulgu — tekrar eden hikâye yanıtı hatası (P0/P1)

- **Yaklaşık 00:02, 00:36, 00:44 ve 00:58:** Hikâye ekranında mavi uyarı **“Hikâye yanıtı gönderilemedi.”** tekrar tekrar görünüyor.
- Kullanıcı metin alanına kısa deneme metinleri (`slm` vb.) yazıp gönderme simgesine dokunuyor. Birden çok denemede başarısızlık görülüyor.
- Hikâye içeriği olarak hem video görüntüsü (konuşan kişi) hem başka bir fotoğraf/ekran videosu görünüyor. Tüm tekrarların aynı hikâye belgesi olduğu varsayılmamalı.
- **Kesin sonuç:** Build421'in gerçek cihaz testinde hikâyeye yanıt gönderme akışı güvenilir biçimde çalışmıyor. Hikâye oynatılıyor olsa bile mesajın sohbet alıcısına ulaştığı doğrulanamıyor.
- **Bilinmeyen:** Hangi Firebase hata kodu döndü, sohbet belgesi gerçekten oluştu mu, hedef kullanıcı mesaj izinleri neydi, mevcut tekil sohbetin member/permission durumu neydi? Video tek başına kök nedeni kanıtlamaz.

## İlgili kaynak kod araştırma ipucu

- Build 413'teki `tools/apply_build413_social_search_story.py` mevcut `_HikayeGosterPageState._yanitGonder` fonksiyonunu değiştiriyor ve `videos/{storyId}.replyCount` gibi izleyicinin yazma yetkisi olmayan sayaç güncellemesini çıkartıyor.
- Bu yama hâlâ hatanın tamamını çözememiş görünüyor. Kaynaktaki `chat.get()`, olası yeni `chats` oluşturma, `batch.update(chat)` ve `batch.set(messages)` işlemlerini **Firebase emulator / gerçek izin kuralları** ile test etmek; `FirebaseException.code` ve işlem safhasını kullanıcıya gizli veri içermeden kaydetmek gerekiyor.
- İşlevin şu anki genel hata mesajı ağ, auth, Firestore izin ve sohbet durumu sebeplerini ayırt etmeye yetmiyor. Gelecek Work paketi önce hatanın **gerçek aşamasını** belirlemeli; hiçbir hesabın mesaj/gizlilik haklarını genişletmemeli.

## Diğer görülenler

| Yaklaşık zaman | Bulgular | Sınıflandırma |
| --- | --- | --- |
| 00:06–00:12 ve 00:54 | Arkadaşlar listesinde Adem hesabı görünüyor; Umay / Adem profilinde **Takip ediyorsun** ve **Arkadaşsınız** gibi eylemler görüntüleniyor. | Çalışıyor görünen mevcut ilişki arayüzü; yeni istek ve karşı tarafta teslim testi değil. |
| 00:08–00:10 | Beş kayıtlı hesap arasında geçiş ekranı açılıyor. | Ekranın açıldığı doğrulandı; başarılı hesap değişimi bu kısa klipte açık değil. |
| 00:30 | Hikâye seçenekleri açılıyor, **Video hikâye** ve göreli yayın/bitiş zamanı `5 dk önce · 23 saat sonra sona erecek` benzeri yazıyla gösteriliyor. | Eski göreli bilgi var; Build421'in beklenen **tam tarih-saat ve kalan süre** paneli bu klipte net biçimde doğrulanamıyor. Kullanılan hikâye açma yolunu gözden geçir. |
| 00:20–00:22, 00:28, 00:52 | Arkadaşlar veya genel aramada yükleme göstergesi ve klavye açılıyor; sonuç görmeden kesiliyor. | **Belirsiz**, sonuç alınamadı demek için yeterli kanıt yok. |
| 00:00, 00:04, 00:26, 00:48–00:50 | Akış/Radar ekranına dönüşte kısa siyah/yükleniyor durumu. | UX/yükleme izlemesi; kalıcı çökme gösterilmedi. |
| 00:46 | Ziyaretçi profilinde avatar, katılım tarihi, dört sayaç, **Mesaj / Arkadaşsınız / Ortak gruplar** düğmeleri. | Çalışan görünüm. |

**Gizlilik:** Ekran videosundaki kaydedilmiş hesapların e-postaları veya mesaj içerikleri bu rapora kopyalanmaz.

## İlk üç video birleştirilince kalan Work adayları

1. **Öncelik P0/P1:** Hikâye yanıtı reddediliyor (Video1 ve Video3; Video3 Build421 sürüm doğrulandı). Teknik hata safhasını kanıtla; çalışan DM ve hikâye oynatma işlevlerini bozma.
2. **Öncelik P2:** Profil sahibinin katılım tarihi satır sonunda kesiliyor (Video2, Build421).
3. **Öncelik P3:** Kapak fotoğrafı üzerindeki siyah değiştirme alanı fotoğrafı örtüyor (Video1).
4. **Öncelik P3:** Profil ve Akış/Radar sayfalarında geçici yükleme göstergeleri ve olası düzen sıçraması (Video1/Video2/Video3). Kalıcı yüklenmeme kanıtı yok.
5. **Açık şüphe:** Bazı arama kaynaklı kullanıcı profili ekranlarında sosyal eylem düğmelerinin görünmemesi (Video2); aynı rota ile yeniden test.
6. **Cihaz testleri açık:** yeni arkadaşlık isteği, bildirimlerin alıcıya teslimi, mesajın karşı hesaba ulaşması, isteği geri çekme, gerçek kapaksız görünümü kaydetme, hikâye tam saat paneli, farklı hesapta profil fotoğrafı güncelleme, gönderi kaydetme/grup kurma.

## Work değişiklik kuralı

Bu aşamada **yalnız QA raporu** hazırlanır. Üç cihaz videosunun birleştirilmiş sorunu, kullanıcı istediğinde **tek sonraki Work geliştirme paketinde** ele alınır. Canlı Firestore kuralları genişletilmez; başarılı Build421 APK ve kaynak koruma testleri başlangıç noktasıdır.
