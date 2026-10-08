# NgelX Build 403 — Ben/Profil gerçek cihaz QA (video 45082.mp4)

**Kaynak:** Kullanıcının bu sohbet içinde gönderdiği `45082.mp4`, 61,33 saniye, dikey Android ekran videosu (1080×2392). İnceleme 2026-10-08 tarihinde yapıldı. Kullanıcı bunu Build 403 profil testi olarak sundu; **Ayarlar > Uygulama güncellemeleri altındaki sürüm etiketi bu video içinde ayrıca açılmadı**. Bu dosya video gözlemidir, otomatik uçtan uca test değildir.

**Tasarım referansı:** Önceden onaylanan beyaz profil, üstte kapak + solda avatar, yanında ad/@kullanıcı adı, dört ikonlu istatistik kartı, tanıtım video kartı, öne çıkanlar, beş içerik sekmesi ve beyaz alt menü. Yalnız gerçek hesap içeriği kullanılacak.

## A. ÇALIŞAN / CİHAZDA GÖRÜLEN — BOZMA

| Yaklaşık zaman | Gözlem |
| --- | --- |
| 00–04s | Ayarlar ve gizlilik ekranı açılıyor. **Premium ve Cüzdan** satırı yalnız kendisi açık mavi, mavi ikon/başlıkla vurgulanıyor; çevresindeki hesap/gizlilik ayar satırları beyaz ve mor ikonlu. Premium sayfasına giriliyor; başlık ve ayrıcalık kartları açılıyor. Premium abonelik/satın alma işlevi bu testte yapılmadı. |
| 05–11s | `Ben` bölümünde kapak gerçek fotoğrafla, avatar-kamera, ad/@kullanıcı adı avatarın sağında, biyografi-konum/katılım tarihi, 4 mor ikon/sayı ve yatay mor kart, `Profili Düzenle`, `Arkadaş Ekle` düğmeleri görüntüleniyor. |
| 08–14s, 17–24s, 33–37s | Tanıtım videosu gerçek görüntüyle hazırlanıyor, oynatıcı ve gerçek süre etiketi **00:40** gösteriliyor. Bir girişte video önizlemesi kısa süre dönen yükleme göstergesi gösteriyor, sonra görüntüleniyor. Videonun üzerindeki ses kontrolü gözüküyor. |
| 20–24s | `Tanıtım videosunu değiştir` tıklanınca alt panelde `değiştir` / `kaldır` seçenekleri açılıyor; kaldırma uygulanmıyor, video korunuyor. Menü metni okunur. |
| 17–21s, 34–38s | Profilin beş kısayol ikonu (Kaydedilenler, Arşiv, Hikâyeler, Gizlilik, Ayarlar), `Yeni` ve gerçek `Video` hikâye balonları, profil gönderilerindeki gerçek görselli 3 sütunlu grid görünüyor. |
| 27–33s | Hikâye görüntüleyici (birden çok hikâye) çalışıyor; resim ve video hikâyeler arası geçiş var. Menüsü `Hikâyeyi paylaş`, `Öne çıkanlara ekle`, `Arşive taşı`, `Hikâyeyi sil`, `Kapat` yazılarıyla okunur. Hikâye silme, paylaşma veya arşive taşıma **bu kayıtta uygulanmadı**. |
| 39–55s | Kaydedilenler açılıyor. Başlangıçta videoların kapakları 1-3 saniye gri veya boş; daha sonra iki gerçek küçük resim geliyor. Bir kaydedilmiş video tam ekran açılıp oynuyor. Geri dönünce basılı tutma alt paneli, `Kaydedilenlerden kaldır`, `Vazgeç` görünüyor; kaldırma sonrası liste 2 kayıttan 1 kayda iniyor ve başarı bildirimi beliriyor. Gerçek gönderi silinmiyor, yalnız kaydedilen bağlantısı kaldırılıyor. |
| 55–61s | Ben ekranına dönüş, profil içeriği/kısayolları ve beyaz `Akış / Keşfet / Üret / Sohbet / Ben` alt barı korunuyor. Ortadaki Üret mor-mavi ve belirgin. |

## B. SÜREN TEKNİK/GÖRSEL SORUNLAR — ÖNCELİKLER

**P1 — Kaydedilenler gridinde girişte gri video kapağı ve tekrar eden önizleme hazırlığı (yaklaşık 04–06, 43–51s)**
- Kaydedilmiş video karesi başlangıçta gri + oynat simgesi; bir süre sonra gerçek kapak görünüyor. Video tam ekran **açılıp oynadığı için** medya dosyası tamamen bozuk/eksik olarak sınıflandırma.
- Bu kayıt `Tekrar dene` butonunun gerçekten devreye girdiğini doğrulamıyor; bir hata/timeout olayı gözlenmedi.
- Geliştirme: thumbnail metadata (coverUrl/posterUrl/thumbnailUrl) kaynak ve cache hit oranı; video ilk kare kontrolörü tekrar oluşturma sayısı; uzak ağ süresi; ekranlar arası kapak cache. Var olan video açma/kaydedilenden kaldırma işlemleri bozulmadan kalıcı küçük resim ve skeleton/fallback iyileştir.

**P1/P2 — Hikâye/Akış/Video açılışında siyah yükleme ekranları (29s, 41–47s, 57–58s)**
- Birkaç geçişte medya sayfası siyah ve dönen işaretle bir süre bekliyor; diğer açılışlar başarılı, bu nedenle 'hiç çalışmıyor' deme.
- İlgili medya başlığı/placeholder'ı eklemek, yükleme uzunluğunu ölçmek, kesilme durumunda retry gösterimi değerlendirilsin. Her siyah geçişin sebebi aynı olmayabilir.

**P2 — Tanıtım video kartının ilk yüklenmesinde spinner/yeniden çizim (10–12, 37–39s)**
- Video süre etiketi doğru görünüyor; buna rağmen birkaç kez karta dönüşte gri geçici arka plan veya spinner görülüyor. Mevcut gerçek video oynatıcısı ve mavi olmayan kart tasarımını koru.
- Uzun videoda etiket sığması, kısa videoda mm:ss formatı, ses/durdurma, uygulama arka plana alma ayrıca test edilmeli.

**P2 — Tasarımın kalan ince farkları**
- Referansta tanıtım videosu daha büyük ve süre etiketi sağ üstte; Build 403 gerçek `00:40` etiketi sol üstte görünüyor. Süre görünür olduğu için eksik değil, yalnız konum/tipografi farkı.
- Öne çıkanlar referansta çok sayıda isimli daire; gerçek hesapta sadece `Yeni` / `Video` gösterimi doğru. Olmayan albüm/medya uydurma; daha iyi boş durum/isimlendirme ileride tasarlanabilir.
- Kısayol `Kaydedilenler` dar ekranda iki satıra bölünüyor, fakat çok küçük ve kısa çizgili metin görünümüne yakın; tekdüze ikon/etiket aralığı iyileştirilebilir.
- `Etiketlenenler` sekmesi bu videoda yatay sıra dışında/sağda kalıyor; beş içerik sekmesinin tümüne gidildiği test edilmedi. Sekme kaldırılmamalı.
- Önceki referans mockup'ı ile gerçek hesap fotoğrafları, isim, sayaç değerleri, şehir veya gönderi sayılarındaki farklar **bug değil**.

## C. Bu videoda doğrulanmayanlar
- Başka hesapta takip, arkadaşlık, mesaj ve profil gizlilik izinleri; bütün düğmelerin sunucu etkisi.
- `Tanıtım videosunu değiştir/kaldır` işlemini gerçekten tamamlama.
- Gri video kapağında `Tekrar dene` butonunun hata halinde çalışması (ekranda timeout tetiklenmedi).
- Hikâye silme/paylaşma/arşivleme etkileri, bütün `Gönderiler/Reels/Hikâyeler/Kaydedilenler/Etiketlenenler` sekme verileri.
- Canlı Yayın / Sesli Oda. **Bu kayıt yalnızca Profil/Ayarlar/Hikâye/Kaydedilenler testidir.** Canlı ve sesli odalar için sonraki iki video bekleniyor.
- Premium ve Cüzdan sayfasında satın alma, ödeme, mavi tik veya jeton bakiye işlemi.

## D. Sonraki Work paketi koruma sözleşmesi
1. Build 403'te görünen profil header/kapak, dört sayaç kartı, gerçek profil/video süresi, çalışan menüler, beyaz alt menü, videolu hikâye, gerçek Kaydedilenler verisi ve kaldırma akışını aynen koru.
2. **Yalnız Premium ve Cüzdan ayar satırı mavi** kalsın. Diğer ayarlara toplu mavi tema uygulama.
3. Kaydedilenler medyasında kalıcı thumbnail önbellekleme, gerçek video ilk kare zaman aşımı ve retry UX optimize edilecek; veriyi ve kaydedilen içerikleri silme.
4. Profil ve hikâye siyah yükleme geçişlerine ölçülebilir zaman aşımı/geri dönüş, skeleton ve yinele ekleme değerlendirmesi.
5. Kod değişikliği yapılırsa Flutter analizi, koruma testleri, imza doğrulaması, sonra gerçek cihaz video testi. Bu QA kaydı **yeni APK değildir**.
