# NgelX Build 412 — Profil Tasarım/Hata Düzeltme Paketi

## Referans ve kapsam
Kullanıcının 45247.png kapaksız ziyaretçi ve 45230.png kapaklı ziyaretçi profil görselleri **onaylı tasarım sözleşmesidir**. Gerçek kullanıcı fotoğrafları, isim, tarih, istatistik, gönderiler ve durumları her zaman Firestore'dan dinamik gelir. Görseldeki Dilek örnek verileri koda sabitlenmez.

Cihazdan test edilmiş Build411 işlevleri korunur: profil sahibinin kapaklı/kapaksız seçimi diğer hesaptan görünür; gerçek kapak fotoğrafı yüklenir, kaldırılır, farklı kullanıcılar birbirlerinin profilini açar. Geçmişteki hayalet CANLI hatası 408'de gerçek telefonda düzelmişti; bu kodlara dokunulmaz.

## Gerçek uygulanan değişiklikler
1. `tools/apply_build412_visitor_layout.py`: Ziyaretçi kapaksız profilinde ortalanmış büyük avatar, mor dekor; kapaklı profilinde kapak fotoğrafının **sol-altına taşan** avatar, sağda ad ve kullanıcı adı, altta bio/konum/katılım tarihi. Gerçek üyelik ve aktiflik verileri korunur. Dört sayaç tek mor ikonlu lavanta kartta; sayaçların gerçek Firestore okuması / tıklama hedefleri korunur. Var olan intro-video oynatıcısı aynı kalır; solda açıklama ve sağda küçük önizleme kartı halinde yerleşir.
2. `tools/apply_build412_visitor_actions.py`: **Takip / Mesaj / Arkadaşlık / Ortak gruplar** dört öğesi tek yatay aksiyon sırasında ve mor/beyaz paletle gösterilir. Var olan takip isteği, gizlilik, engelleme, mesaj başlatma, arkadaşlık iptal etme/çıkarma, ortak grup callbacks aynen bırakılmıştır. Sadece açıklayıcı uzun bilgi kutusu gizlenmiştir.
3. `tools/apply_build412_visitor_grid.py`: Üç sütunlu gerçek gönderi/video grid'ine yuvarlatılmış daha kare kutucuklar ve paylaşımın **gerçek** beğeni/yorum sayısını gösteren koyu yarı saydam alt bant ekler; dokununca orijinal içerik sayfasına açma işlemi korunur.
4. `tools/apply_build412_editor_safe_area.py`: Ekranın altında **Kaydet / Önizleme aç** düğmelerinin Android 3-tușlu navigasyon çubuğuna taşmaması için ScrollView alt boşluğu gerçek `MediaQuery.viewPadding.bottom` ve `viewInsets.bottom` dikkate alınarak artırılmıştır. Kapaklı modda kapak fotoğrafı yoksa görünen `Kapaklı görünüm için önce bir kapak fotoğrafı ekle.` uyarısına amber/turuncu dolgu, koyu yüksek kontrastlı metin ve uyarı ikonu ekler. Doğrulama şartı kaldırılmaz.
5. `tools/apply_build412_version.py`: sürüm `1.0.187+412`.
6. `tools/check_build412_profile_ui.py`: yapısal koruma testleri, Build395–411 regresyonları üstüne.

## Açık güvenlik ve altyapı koruması
- **Firestore güvenlik kuralları değişmez ve canlıya deploy edilmez.** Tam paket, mevcut kuralları Firebase emulatorunda yeniden test eder.
- Canlı yayının kırmızı etiketinin yalnız gerçekten aktif oturumda görünmesi korunur.
- Profil güvenliği, bloklama, gönderi kitle/hiddenFor ve ziyaretçi izinleri sorguları değiştirilmez.
- Profil video oynatıcı / fotoğraf yükleme ve Cloud R2 akışı değiştirilmez; tasarım sadece mevcut widget'ları yeniden düzenler.
- Profil sahibi görünüm tercihi başka hesaba yansır; Firestore `profileViewMode` eski şekilde okunur.
- Kullanıcının daha önce `mor yükleme göstergesi sorun değil` açıklaması aynen geçerlidir; spinner tarafına dokunulmaz.

## Yayın ve cihaz doğrulaması
- Kaynak patch + geriye dönük koruma: [Build 412 hızlı test](https://github.com/Nnentx/Ngelx/actions/runs/37855860108) **başarılı** (son grid sonrası).
- Flutter analizi: [Build 412 design check](https://github.com/Nnentx/Ngelx/actions/runs/37855860066) sonuç bekleniyor.
- Güvenlik emulatoru, Flutter analyze, Android apk, imza ve artifact: [Build 412 release](https://github.com/Nnentx/Ngelx/actions/runs/37855915145) devam ediyor.
- **Gerçek Android telefonu üstünde yeniden kontrol yapılmadan "görsellerle piksel-birebir eşleşti" diye işaretleme.** Test edilecek: Adem hesabından Dilek kapaksız/kapaklı açılması; dört butonun okunması ve eylemleri; intro oynatma; gerçek sayaçlar; post grid; Android alt gezinme tuşlarıyla Kaydet ve Önizleme aç tamamen görünmesi; renkli uyarı.

## Sonraki paket için kalanlar
Kullanıcının daha eski listesinde ayrıca Gelen Kutusu renkli Grup rozeti/isimleri, kapsamlı Üret anket ve konum/etiket kontrolleri, videolar arasında kısa siyah ekran, gelişmiş arama indeksleri ve diğer platform özellikleri bulunuyor. **Build412 bu tamamını bitti saymaz**; burada açıkça kayıt altına alınan profil tasarım ve iki cihaz bulgusu önceliklidir. Yeni tasarım ihtiyacı olmayan çalışan bileşenlere müdahale edilmez.
