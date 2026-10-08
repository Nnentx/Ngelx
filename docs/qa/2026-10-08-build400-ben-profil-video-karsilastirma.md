# NgelX Build 400 — Ben/Profil telefon testi ve referans karşılaştırması

- Tarih: 2026-10-08
- Kanıt: Kullanıcının bu sohbet içinde gönderdiği yaklaşık 59 saniyelik cihaz videosu (45041.mp4).
- Referans: Kullanıcının daha önce gönderdiği kapaklı, mor-mavi, beyaz alt menülü Ben ekranı mockup'ı.
- Test hesabı videoda: DİLEK Akçay (@dilekizmm).
- KURAL: Aşağıda "açılıyor/görünüyor" denmesi uçtan uca işlevsel doğrulama demek değildir. Gerçek cihazda gözlenen davranışlar korunacak; eksikler tek konsolide Work paketinde giderilecek. Bu not tek başına kodu değiştirmez.

## A — ÇALIŞAN / GÖZLENEN YAPILAR: GERİYE DÖNÜK BOZMA
1. Build 400'de kapak fotoğrafını galeriden seçme ve fotoğraf kadrajını düşey kaydırma çalışıyor (yaklaşık 3–15s). Kaydet sonrası fotoğraf 20s sonrasında ve ekranlara girip çıkıldıktan sonra profil kapağında görünüyor (22, 32, 52, 56s). Önceki `HTTP 400 invalid_kind` hatası videoda tekrarlanmıyor.
2. Profilin açılması; avatar ve kamera simgesi, isim, @kullanıcı adı, biyografi, konum satırı, katılma tarihi ve dört istatistik sayısı görünümü.
3. Üstte arama, üç nokta, bildirim, ayarlar ikonları ve kapak değiştir butonu mevcut; ikonların tamamının işlevi test edilmedi.
4. "Profili Düzenle" formu açılıyor; görünen ad, kullanıcı adı, biyografi, konum alanları ve Kaydet butonu var (35–36s). Kaydetme sonucu test edilmedi.
5. "Arkadaşlar" listesi açılıyor, videoda iki kayıt görünüyor (3–4, 37–41s). Arkadaş üç nokta menüsü açılınca "Profili aç", "Takipten çık", "Arkadaşlıktan çıkar" seçenekleri geliyor (41s); bu işlemlerin arka uç sonuçları test edilmedi.
6. Profil içi arama ekranı açılıyor, mevcut paylaşımlar listeleniyor; Tümü, Fotoğraf, Video filtresi ve yazılı arama güncelleniyor (23–30, 58s). "an" ile sonuç görünmemesi tek başına hata kanıtı değildir.
7. Hikâye videolu görüntüleyicide açılıyor ve oynuyor, göreli yaş ("7 sa önce") gösteriliyor (45–50s). Hikâye gönderme/paylaşım sonucu doğrulanmadı.
8. Gönderiler bölümünde gerçek gönderi küçük resimleri, üç sütunlu grid ve beğeni/yorum sayıları görünüyor (1–2, 42–44s). Reels ve diğer tabların tamamı çalışıyor diye varsayılmamalı.
9. Alt gezinmede Akış, Keşfet, Üret, Sohbet, Ben görünüyor. Kayıtlı arkadaşlık / takip / gizlilik / mesaj altyapısı ve imza anahtarı değiştirilmemeli.

## B — VİDEODA GÖRÜLEN SOMUT HATALAR (ÖNCELİK)
**P0 — Kapak işlemleri alt menüsünde görünmez metin (54–55s).**
- Alt panel beyaz. Üstteki başlık, "Galeriden seç" ve "Kapağı yeniden konumlandır" satırlarının yazıları ekranda görünmüyor; yalnız ikonları görülüyor. En alt kırmızı "Kapak fotoğrafını kaldır" metni okunuyor.
- Muhtemel tema/metin-kontrast sorunu. Tüm seçenek etiketlerini yüksek kontrastla görünür yap; panel aç/kapat, dosya seçme, yeniden kadrajlama, kaldırma ve hata durumlarını koru ve test et.

**P0 — Hikâye paylaşım alt paneli çoğunlukla boş (47–49s).**
- Hikâye açılıyor, sonra beyaz panel geliyor; paylaş/send ikonları var, kişi veya açıklama satırları görünmüyor. Seçeneklerin/sonucun yüklenip yüklenmediği belirsiz.
- İçerik boşsa açık boş-durum metni koy; varsa metin ve kişiler görünür olsun; gerçek gönderme/Android paylaşım testi yap.

**P1 — Kapak görselinde yükleme/flicker (16–22s).**
- Kaydet sonrası önce açık mor placeholder, bir karede beyaz boş alan, ardından seçilen kapak görünüyor. Yeniden girişte de ilk yüklenme durumunu kontrol et.
- Önceki görselin yerinde kalmasını ve tutarlı skeleton/placeholder kullanımını test et. "Yükleme başarısız" demek için kanıt yok.

## C — REFERANS GÖRSELE GÖRE EKSİK/GÖRSEL FARKLAR
**P1 — Ana profil üst düzeni:** Referansta büyük tam geniş kapak, önde avatar ve ad/@kullanıcı adı avatarın sağında; gerçek ekranda avatar sol altta, ad/bio ise aşağıda merkezlenmiş. Kapak yüksekliği/boşluk ve içerik hiyerarşisi eşitlenmeli. Referanstaki geri tuşu gerçek öz-profil sayfasında bulunmuyor; bu, navigasyon bağlamına göre değerlendirilmeli.
**P1 — İstatistik kartı:** Referansta arka planlı tek yatay kart, mor ikonlar ve dikey ayırıcılar. Gerçekte dört sayı düz beyaz zeminde, ikonlar/ayırıcılar yok.
**P1 — Öne çıkanlar:** Referansta Yeni/Öne Çıkanlar/İstanbul/Seyahat/Doğa/Yaşam gibi resimli halka koleksiyonları. Gerçekte yalnız Yeni ve "Video" yuvarlağı gösteriliyor. Hesapta öne çıkan içerik yoksa sahte içerik ekleme; boş-durumu referans diline göre düzenle. Var olan öne çıkanlar veri akışı ayrıca test edilmeli.
**P1 — Tanıtım videosu:** Referansta başlıklı/betimli, video görselli, oynat ve süre etiketli ayrı kart. Videoda yalnız "Profil tanıtım videosu ekle" ince butonu var. Video yoksa da düzgün ve anlaşılır boş kart, varsa gerçek önizleme/süre göster.
**P1 — Sekme sırası/eksik sekme:** Referans: Gönderiler, Reels, Hikâyeler, Kaydedilenler, Etiketlenenler. Gerçek: Gönderiler, Reels, Etiketlenenler, Hikâyeler (42–44s). Kaydedilenler yalnız kısayol simgesinde bulunuyor; istenen üst sekme eksik. Altyapıyı kopyalamadan aynı Kaydedilenler verisine bağla.
**P1 — Alt gezinme teması:** Referansta beyaz zemin, büyük mor-mavi Üret ve belirgin etiketler. Gerçekte siyah zemin, daha küçük ikonlar/Üret ve etiketler. Beyaz referansla hizala, 5 sekmenin bütün gezinmesini koru.
**P2 — Buton ve kısayollar:** "Arkadaş Ekle" iki satıra bölünüyor. Alt kısayollardaki "Kaydedilen..." metni kesiliyor. Referans ölçeğine yaklaşırken metin taşmasını ve dar telefon ekranlarını test et.
**P2 — Gönderi sekme vurgusu:** Gerçekte aktif sekme altında turkuaz çizgi, referansta mor çizgi.
**P2 — Profil içi arama sonuçları:** "Adsız paylaşım" genelleştirilmiş etiketleri kullanılıyor; içerik türü/süre/açıklama/medya önizlemesi zenginleştirilebilir. Arama/filtre akışı bozulmadan geliştir.
**P2 — Hikâye zamanı:** "7 sa önce" mevcut; kullanıcı daha önce başlangıç ve bitiş/kalan süreyi de görmek istemişti. Bu videoda bitiş/kalan süre etiketi görülmüyor.
**Veri farkı, otomatik hata değil:** Konumun "Konum eklenmedi" olması ve "Ekim 2026'te katıldı" tarihi referanstaki İstanbul/Eylül değerlerinden farklıdır çünkü iki ekran aynı hesap verisi değildir. Statik referans verisini gerçek hesaba kopyalama.
**Test edilmedi:** Profil fotoğrafını gerçekten değiştirme, kapak silme, arkadaş ekleme/çıkarma sonuçları, Profili Düzenle -> Kaydet sonucu, 5 profil içerik tabının her biri, tüm üst ikonlar, hikâye paylaşımının tamamlanması, sabitlenen gönderi kuralları.

## D — WORK İÇİN UYGULAMA / REGRESYON KURALI
- Önce P0 görünmeyen alt panel metinleri ve hikâye paylaşım panelini düzelt; ardından referans profili birebir daha yakın tasarla.
- Çalışan Build 400 kapak R2 yükleme `kind:'profiles'` sözleşmesini, kapak yerleşim/kadraj değerlerini, avatar, arkadaş listesi, takip/arkadaş altyapısı, profil içi arama, videolu hikâye oynatma, profil gönderi listesi, kayıt/sohbet, 5 ana tabı koru.
- Alt panel her seçeneğinde yüksek kontrast, erişilebilir dokunma hedefi, SafeArea ve geri/iptal testi yap.
- Boş/henüz oluşturulmamış video ve öne çıkanlar için gerçek veri olmadan demo veri ekleme.
- Reels, Hikâyeler, Kaydedilenler, Etiketlenenler tablarını gerçek veriye bağla; çalışan ekranları silme.
- Değişiklikler tek konsolide Work paketinde, önce kod analizi ve test, sonra release APK + imza doğrulama, ardından gerçek cihaz testi ile teslim edilmeli.
- Bu belge gözlem/not kaydıdır, kod veya yeni APK düzeltmesi değildir.

## E — 2026-10-08 / Build 401 uygulama durumu (cihazda henüz yeniden test edilmedi)
- Kod yaması: `tools/apply_build401_profile_stability.py`.
- P0 kapak eylemleri alt panelinde açık `Colors.black87/black54` metin ve açık `ThemeData.light()` uygulandı. Galeri seçme / kadraj değiştirme / silme işlemleri korunmuştur.
- P0 eski `HikayeGosterPage` seçenek panelinde metin renkleri ve açık tema eklendi; mevcut `SharePlus` ve `ngelxOzeldenPaylas` çağrıları korunmuştur. Yeni `NgelXHikayeSeriPage` panelindeki mevcut kontrast ayarlarına dokunulmadı.
- Dört profil sayacına mor ikon eklendi; Firestore sayaç sorguları ve tap rotaları değişmedi.
- Profil sekme sırası: Gönderiler / Reels / Hikâyeler / Kaydedilenler / Etiketlenenler. Mevcut ekran işleyicileri kullanılıyor.
- Tanıtım videosu için veri yokken boş kart, varsa gerçek oynatıcı kartı gösteriliyor; video seçme/değiştirme kodu korundu.
- Ana beşli navigasyon çubuğu beyaz zemine/mor seçili renge geçirildi; navigasyon callback'leri korunmuştur.
- `Arkadaş Ekle` etiketine tek satırda kesme koruması eklendi.
- `tools/check_build401_profile_regression.py` statik koruma kontrollerini gerçekleştirdi; GitHub Actions kod ve Flutter analiz sonucuna göre statü ayrıca belirlenecek.

### Henüz çözülmemiş / ayrıca ele alınacak
- Referanstaki isim/avatara göre yatay hizalama ve kapak yerleşimi birebir tamamlanmadı.
- Referanstaki öne çıkan hikâye albümleri yalnız gerçek kullanıcının kayıtlarından oluşturulabilir; olmayan veriler sahte görsellerle doldurulmayacak.
- Kapak görselinde yükleme anında görülen geçici boşluk/titreme hâlâ gerçek cihazda izlenecek.
- Hikâye menüsünün kullanıcı tarafından seçilmesi, paylaşma işleminin tamamlanması, profil verisini kaydetme, arkadaş kaldırma, bütün içerik sekmeleri ve beyaz alt navigasyon cihazda yeniden doğrulanmalıdır.
- Kodun geçirilmesi `gerçek cihazda doğrulandı` anlamına gelmez.

### Build 401 CI teslim doğrulaması
- GitHub Actions run: https://github.com/Nnentx/Ngelx/actions/runs/37738991907
- Sonuç: **success** — Build 399/400/401 regresyonları, Flutter analizi, release APK, imza doğrulaması ve artifact yükleme başarılı.
- Artifact: NgelX-1.0.177-Build-401-PROFILE-STABILITY-REFERENCE (GitHub artifact 11533242546).
- **Gerçek cihaz görsel ve işlev testi bekleniyor; Build 401’in menü kontrastı, beyaz navigasyon ve profil kartı sonuçları kullanıcı cihazında tekrar görülmeden cihazda doğrulandı denmeyecek.**

## Build 401 cihaz tekrar testi — 2026-10-08

- Kullanıcının 03:52 ekran videosu ayrıntılı incelendi. Tam rapor: [Build 401 gerçek cihaz incelemesi](./2026-10-08-build401-cihaz-video-incelemesi.md).
- Kapak menüsündeki ve hikâye menüsündeki yazılar görünür; kapak seçme/kadraj/kaydetme, profil biyografi kaydetme, hikâye yayınlama ve arşivleme, kaydedilenlerden kaldırma (3→2), Üret fotoğraf paylaşımı ve Akış'ta yeni fotoğrafın görünmesi cihazda gözlendi.
- Referansa göre avatar/isim yatay yerleşimi, bölücülü istatistik kartı, öne çıkan albümler, tanıtım videosunun yatay düzen/süre etiketi, büyük Üret butonu ve kesilen Arkadaş Ekle/Kaydedilenler yazıları hâlâ eksik.
- Kısa avatar yükleme spinner'ı ve medya/yorumların ilk açılış beklemesi performans notuna eklendi.
- Çalışan özellikleri ve gerçek kullanıcı verilerini koru; yeni APK çıkarılmadı. Sonraki birleştirilmiş Work paketine aktar.
