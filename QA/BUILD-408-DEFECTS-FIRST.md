# NgelX Build 408 — Önce Eksik/Bozuk İşlevler, Sonra Onaylı Tasarımlar

**Kullanıcının son öncelik kararı:** "Önce eksikleri kodla sonra tasarımlar". Build 407 çalışan ekranları korunacak. Bu dal **yalnız doğrulanmış işlevsel hatalar** için; daha önce onaylanan kapaklı/kapaksız profil ve Profili Düzenle görselleri ayrı sonraki paket.

## Uygulanan hedefli düzeltmeler
1. **Başka kullanıcının profilinde hayalet CANLI (45218):** `users.isLive/currentLiveId` aday bilgi; kırmızı CANLI ve "Canlı yayını izle" sadece `live_streams/{currentLiveId}` gerçek zamanlı belge akışında **`ngelxCanliKaydiTaze`** olumlu dönerse görünür. İlgili yayın biter/kapanır/geçerliliğini kaybederse rozet ve buton gizlenir. Kullanıcının çevrimiçi durumu, hikâye halkası, takip/mesaj/arkadaş/istatistik ve tanıtım videosu korunur. Veri silme veya sunucuya durum yazma yapılmaz.
2. **Grup sohbetlerinde tekrarlayan engellenmiş üye diyaloğu (45219):** grup ID + mevcut kullanıcı + gerçekten engel ilişkisi bulunan üye kümesinin imzasına göre kullanıcının "Gruba gir" onayı cihazda hatırlanır. Kullanıcı gruba tekrar geldiğinde uyarı yeniden gösterilmez; engel ilişkisi değişirse tekrar sorulur. "Geri dön" seçildiyse onay saklanmaz. Engellenen üye mesaj gizleme/özel görüşme engelleri aynen çalışmaya devam eder.
3. **Yönetici onayından sonra bayat "katılmak istiyor" bildirimi (45216):** Gelen Kutusu (Tümü/Bildirimler) ve Aktivite için durum `chats/{chatId}/joinRequests/{fromUid}.status` belge akışıyla doğrulanır. `accepted`, `rejected`, `cancelled` gerçekleşirse eski bekleme metni, sonucu bildiren geçmiş metne dönüşür. Bilinmeyen/pending durumda eski olay bilgisi korunur. Bildirimi silmeyiz, üyelik veri modelini değiştirmeyiz.

## Değiştirilmeden korunanlar
- Build 407'de telefonda geçen **Çevrem | Radar**, NgelX başlığı, kısa gönderi zamanı, video ileri sarma, bildirim gönderen isimleri ve grup kurucu/yönetici onayı
- Canlı yayın hazırlık, PK, ses, sohbet, medya, takip, arkadaşlık ve tüm mevcut Firestore gruplar/izinler
- Firestore rules **değişmedi, yeniden dağıtılmayacak**; Build 407'nin canlı yönetici onayı izni korunacak

## Test / teslim kapıları
- `tools/apply_build408_defects_first.py` 395–407 patch'leri **ardından** uygulanır.
- `tools/check_build408_defects_first.py` kritik kaynak kontrollerini ve eski Build 395–407 regresyonları doğrular.
- Build 407 ile aynı emulator Firestore yetki testleri, Flutter analyze, imzalı 1.0.184+408 Android APK ve artifact CI sonucu beklenecek.
- Gerçek telefon smoke henüz geçmedi: Dilek'in bitmiş CANLI etiketinin gizlenmesi; grup engel uyarısının ikinci girişte tekrarlamaması; grup talebi kabul/ret edildiğinde eski bildirimlerin güncellenmesi. Eşzamanlı yeni yayın başlatma/bitirme sınır durumları ayrıca izlenecek.

## Tasarım fazı, bu Build 408'e KASITLI OLARAK ALINMADI
- Kapak fotoğraflı **karşı profil** tasarımının kullanıcının onayladığı görseline bire bir uyarlanması
- Kapaksız görünüm: hem **kendi profilinde** hem **başka profillerde** kapak banner'ı kaldırılmış, ortalı avatar ve onaylı mor detaylı tasarım
- Profili Düzenle'deki kapaklı/kapaksız seçimi, gerçek önizleme ve kaydetme; örnekteki **katılma tarihi gerçek oluşturulma verisidir, keyfi düzenlenebilir alan yapılmaz**
- Gelen Kutusu "Grup" rozeti, kişi adının renkli ve grup adının farklı vurgu renginde görünmesi
- Üret tam anket sistemi, gelişmiş arama indeksleri, Akış Araçlar menüsü ve diğer birikmiş tasarım/ürün işleri

**Durum:** Kod GitHub dalında; otomatik test ve APK sonucu için CI takip edilir. Kaynak testleri geçmeden veya APK kurulmadan "tamamlandı" denmeyecek.

## Gerçek telefon QA — 2026-10-09 00:32–00:33, 45244.jpg / 45245.jpg

- **Kurulum doğrulandı:** 45244.jpg Ayarlar > Uygulama güncellemeleri: `v1.0.184 · Yapı 408`.
- **GEÇTİ / canlı yayın hatası:** 45245.jpg DİLEK Akçay (@dilekizmmz) diğer kullanıcı profilinde, eski bitmiş yayından kalan kırmızı `CANLI` halkası/rozeti ve `Canlı yayını izle` butonu artık görünmüyor. Avatar, ad, biyografi ve tanıtım videosu yerinde. Eski hayalet CANLI hatası bu telefon testinde **tekrarlanmadı**.
- **Yükleme simgesi:** Tek fotoğrafta istatistikler bölgesinde mor spinner görünüyor. Kullanıcı hemen ardından açıkça **"Yok sorun yok başka test yoksa"** dedi; bunu bug olarak işaretleme, **kullanıcı sorun bildirmedi**.
- **Henüz gerçek telefonda ayrıca doğrulanmayan Build 408 değişiklikleri:** grupta engellenen kişi uyarısının aynı koşulda ikinci girişte yinelenmemesi; onay/ret sonrası eski istek bildirim metninin duruma dönüşmesi. Kullanıcı bu aşamada başka test istemediğinden **telefon testlerini zorlamadan beklemeye al**; geçti diye raporlama.
- **Canlı yeni yayın lifecycle testi:** Yeni yayını başlat/bitir çevrimi kayıtta yok; sadece eski bitmiş yayının yanlış görünmemesi doğrulandı.
