# NgelX — Build 404 Canlı Yayın Telefon Video Testi

- Tarih: 2026-10-08
- Test kaydı: Kullanıcının gönderdiği ~1:42 ekran videosu (`45103.mp4`); video GitHub deposuna yüklenmedi.
- Test edilen sürüm: NgelX 1.0.180 / Build 404 (önceki oturumun sürüm bilgisi)
- Kaynak dal: `work/build-404-profile-live-voice-fixes`
- Kapsam: Keşfet > Canlı > yayın hazırlama > yayın > davet/yorum/filtre/PK > bitirme.
- İş modeli: Hataları ve doğrulama gerektiren adımları Build 405 tek düzeltme paketinde toplamak; çalışan özellikleri korumak.

## A. Videoda gözlenen çalışan akışlar

| Akış | Kayıt zamanı (yaklaşık) | Sonuç |
| --- | --- | --- |
| Keşfet > Canlı ve Canlı yayın başlat | 00:00–00:04 | Hazırlık ekranı açılıyor |
| Ön/arka kamera önizlemesi ve kamera geçişi | 00:04–00:20 | İki kamera da görüntü veriyor (hazırlanıyor kısa geçişi mevcut) |
| Yayın ayarları: format/kategori/kalite/gizlilik/FPS | 00:08–00:28 | Seçenekler görüntüleniyor, 720p > 1080p seçiliyor; gerçek ağ çıkış kalitesi ölçülmedi |
| Görüntü Stüdyosu filtre/presetleri | 00:24–00:30 | Presetler ve kontroller açılıyor |
| Yayın başlığı girişi ve 3-2-1 başlangıç | 00:30–00:39 | Yayın başlıyor, bağlanma sonrasında sayaç işliyor |
| Canlı ekranı | 00:39–00:52 | Görüntü ve yayın süresi mevcut; izleyici sayısı 0 (tek cihaz testinde hata kanıtı değil) |
| Canlı yayın davet/paylaş | 00:52–01:00 | Kişi seçiliyor; “Canlı yayın 1 kişiye Aktivite ve Sohbet üzerinden gönderildi” onayı görülüyor; alıcı tarafı kontrol edilmedi |
| Yayında kamera kapat/aç | 01:04–01:16 | “Kamera kapalı” durumu ve yeniden görüntüye dönüş var |
| Canlı yorum | 01:08–01:16 | Gönderilen yorum yayın ekranında görüntüleniyor; diğer istemciyle eşzamanlama kontrol edilmedi |
| Görüntü ayarlarını yayında değiştirme | 01:20–01:28 | Güzellik/parlaklık/kontrast vb. paneli açılıyor, görüntü değişiyor |
| Canlı Yayın PK | 01:32 | Panel açılıyor ama “Şu anda uygun PK rakibi yok”; rakiple karşılaşma test edilmedi |
| Bitirme onayı, bitiş durumu, Keşfet’e dönüş | 01:38–01:41 | Yayın kapatılıyor ve Keşfet’e dönülüyor |

## B. Kesin video bulgusu — Build 405 için hata

### P1 / UX-LIVE-END-001 — Yayın sonu katman çakışması ve özetin kaybolması

**Görülen:** Yayın bitirildikten sonra “CANLI YAYIN SONA ERDİ” tam ekran durumu açılıyor. Videonun yaklaşık **01:40.0** anında bunun arkasında “Canlı yayın özeti” paneli (süre 0:57, en yüksek izleyici 0, yorum sayısı 1, hediye 0) kısa süreliğine beliriyor; iki katman görsel olarak üst üste geliyor. **01:40.2** civarında kullanıcı özetle etkileşemeden Keşfet’e dönüyor. Özet okunabilir ve onaylanabilir şekilde sunulamıyor.

**Beklenen:** Yayını bitir > bitiş animasyonu (varsa) > **tek bir açık, okunabilir yayın özeti** > kullanıcı “Tamam” veya “Keşfet’e dön”e basınca Keşfet. Birbiriyle çakışan overlay ve kendiliğinden özeti atlama olmamalı.

**Kontrol koşulu:** Özet sayfası kapanma eylemi yapılana kadar görünür kalmalı; süre/izleyici/yorum/hediye metrikleri görünmeli; geri tuşu, yönlendirme ve ekran kapanışında tutarlılık korunmalı.

## C. Bug diye işaretlenmemesi gereken, ayrıca doğrulanacak senaryolar

1. İkinci kullanıcı/telefondan Keşfet’te yayını görme, canlıya katılma/ayrılma, izleyici sayısı ve yayın sona erdi olayının gerçek zamanlı ulaşması.
2. Davet alan kişinin Aktivite ve Sohbet’te bildirimi/linki alması ve doğru yayını açması. Gönderim onayı tek başına alım doğrulaması değildir.
3. Sunucudan sesin karşı tarafa iletilmesi, mikrofon sessiz/aç, kamera ve izin davranışları; yalnızca yerel kontrol gözlendi.
4. İkinci cihazdan yorum gönderimi ve yayıncı/izleyici tarafında sıralama/sayım/görünüm.
5. PK eşleşmesi, davet, kabul/ret, sürenin ilerlemesi ve sonuç ekranı (testte uygun rakip yok).
6. Hediye akışı ve puan toplamının iki tarafta doğru görünmesi.
7. 720p/1080p ve FPS seçeneklerinin **gerçek medya çıkışı** ile tutarlılığı, düşük ışık ve ağ kopup gelme/yeniden bağlanma.
8. Canlı yayın başlığının zorunlu/opsiyonel olma kuralı ve en az 3 karakter doğrulamasının ayrı regresyon testi.
9. Yayın özeti değerlerinin gerçek backend verisiyle karşılaştırılması ve yayıncı/izleyici ekranı tutarlılığı.

## D. Build 405 tek paket doğrulama şartları

- **Önce kesin bug:** Bitirme > yayın özeti UI katmanları çakışmayacak, özet kalıcı ve okunabilir olacak.
- **Sonra çift cihaz E2E:** Yayına giriş, izleyici sayısı, yorum, davet, mikrofon/kamera ve bitiş olayları uçtan uca doğrulanacak.
- **PK & hediye:** Karşı kullanıcı ve uygun test şartları olduğunda uçtan uca kontrol edilecek; bu kayıttan çalışıyor diye işaretlenmeyecek.
- **Regresyon koruması:** Ön/arka kamera, yayın başlatma/sayaç, yorum, filtre, kamera aç-kapat, davet gönderim onayı ve kapatma akışları bozulmayacak.
- **Not:** Bu dosya yalnızca QA bulgusu/iş planıdır. Kod değişikliği, düzeltme, yeni APK veya Build 405 üretimi yapılmış değildir.
