# NgelX — Build 402 gerçek cihaz QA / Ben referans karşılaştırması

**Tarih:** 2026-10-08. **Kaynak:** Sohbette paylaşılan `45058.mp4` (yaklaşık 03:19 Android ekran kaydı). Referans: kullanıcı tarafından onaylanan kapaklı, açık renkli, mor-mavi Ben/Profil ekranı. İnceleme kullanıcı tarafından gönderilen gerçek cihaz kaydına dayalıdır; uygulama sunucusuna veya karşı hesap mesajlarına doğrudan erişim yoktur.

## A. Videoda doğrulanan, kesinlikle korunacaklar

1. **Build 402 yeni Profil tasarımı (24–60sn):** Kapak fotoğrafı, büyük avatar + kamera düğmesi, ad/@kullanıcı adı avatarın sağında, biyografi/konum/katılım, dört mor ikonlu ve dikey ayırıcılı istatistik kartı, iki eylem butonu, beş kısayol, öne çıkan gerçek hikâyeler, 3 sütun gönderiler ve beyaz alt menü görünür. Orta mor-mavi Üret belirginleşmiş.
2. **Aktivite bildirimleri (4–8sn):** Aktivite sayfası açılır; istek ve etkileşim kalemleri listelenir. İsteği kabul/ret düğmelerinin sunucu sonucu bu kayıtta test edilmedi.
3. **Profil menüsü ve ziyaretçi önizleme (8–18sn):** 3 nokta menüsü; Profil önizleme, Arşiv, Ayarlar ve gizlilik seçenekleri açılır. Önizlemede tanıtım videosu/istatistikler ve 'Bu profil sınırlı' gizlilik paneli görünüyor; kapalı profil davranışıyla ayrıca sınanmalı.
4. **Profil bağlantısını NgelX özel mesajla paylaşma (20–25sn):** Kişi seçme alt paneli, canlı seçim sayacı ve gönderme tuşu açılır; önce bir kişi, hemen ardından ikinci kişi de seçiliyor (yaklaşık 22.3sn); buton **'2 kişiye gönder'** oluyor. Sonuç ekranında **'2 kişiye profil gönderildi'** mesajı gösteriliyor. Seçim ile bildirim tutarlı; karşı hesap teslimi ayrıca test edilmedi.
5. **Hikâyeyi izleme/oluşturma ve paylaşma (26–100sn):** Hikâye video izleyicisi açılır, oynatma, menü ve 'Hikâyeyi paylaş / Öne çıkanlara ekle / Arşive taşı / Hikâyeyi sil / Kapat' görünür. Yeni video hikâye 24 saat boyunca yayında bilgisiyle yayınlanır. Harici paylaşma menüsünden WhatsApp seçilir; bağlantı WhatsApp sohbetine yapıştırılıp karşı sohbette görünür. Mesaj içeriklerini veya karşı tarafın kişisel bilgilerini kaydetme.
6. **Tanıtım videosu (30–107sn):** Gerçek video oynatma/önizleme kartı ve değiştir/kaldır seçenekli menüsü çalışıyor. **Yaklaşık 106sn'de kullanıcının 'Tanıtım videosunu kaldır' işlemi sonrasında profil boş tanıtım videosu durumuna dönüyor. Bu beklenen davranış; kaybolma bug'ı diye raporlama.**
7. **Arkadaşlar (108–134sn):** İki arkadaş listesi, arama filtresi (hedef isim yazınca sonuç azalıyor), kişi üç nokta menüsü, diğer kullanıcının profiline geçiş. 'Takipten çık' onayı ardından diğer profilin takipçi sayısı azalıyor ve 'Takipten çıktın' bildirimi geliyor; arkadaşlık durumu ayrı kalıyor. Ardından takip etme/yeniden takip göstergesi gözleniyor. Geri dönüşler çalışıyor.
8. **Profil düzenleme (135–143sn):** Ad, kullanıcı adı, biyografi, konum alanları açılıyor; kullanıcı adı değiştiriliyor, 'Profilin güncellendi' onayı ve sayfada güncel kullanıcı adı görünüyor.
9. **Gizlilik (144–148sn):** Gizli hesap, profil görünürlüğü, arama görünürlüğü, aktiflik, arkadaşla paylaşım, yorum izni, gizli kelime, engellenen ve istek geçmişi ayarları açılır, metin ve düğmeler görünür. Arka uç etkileri test edilmedi.
10. **Kaydedilenler (154–160sn):** İki video/medya karosu, basılı tutup Kaydedilenlerden kaldır alt paneli, vazgeç düğmesi açılıyor; menü çıkışları çalışıyor. Kaldırma eylemi bu kayıtta nihayete kadar yapılmadı.
11. **Akış/Üret/Sohbet (164–196sn):** Akış sekmesi, Üret alanı (fotoğraf/video/yazı/efekt), Gelen Kutusu, konuşma listesi ve sohbet açılıyor, önceki mesajlar ve yeni ileti mesajları gösteriliyor. Gerçek gönderme ve karşı taraf teslimi bu kesitte kesin olarak doğrulanmıyor.

## B. Yeni veya süren kusur/riske göre iş listesi

### Düzeltme — Profil paylaşım sayısı tutarlı (21.5–24sn)
- Yüksek frekanslı kare kontrolünde önce bir kişi işaretli, hemen sonra ikinci kişi de işaretleniyor ve buton **'2 kişiye gönder'** oluyor (22.3sn). Sonuç mesajı da **'2 kişiye profil gönderildi'**. İlk kareden çıkarılan '1 seçilmiş ama 2 gönderilmiş' iddiası **yanlıştı ve geri çekildi**.
- Sunucuya gerçekten kaç mesaj düştüğünü bu tek cihaz videosu göstermez. Gönderilenler/karşı sohbet testi ileride yapılabilir, ama görüntüde sayı uyuşmazlığı yok. Gereksiz paylaşım kodu değiştirilmesin.

### P1 — Kaydedilenler boş/gri video kapağı (154–159sn)
- Bir video küçük resmi yaklaşık 5 saniye boyunca tek renk gri + oynat simgesi halinde kalıyor. Yanındaki video gerçek kapak görseliyle açılıyor.
- **Ölçülmeli:** Url/thumbnail eksikliği mi, yükleme performansı mı, media türü mü? Video açılması/gerçek dosyanın erişilebilirliği ayrıca test edilsin. Fallback/yeniden dene/hata metni düşünülmeli; içerik silinmemeli.

### P2 — Profil gizlilik ayarlarında açıklama tutarlılığı (12–16, 144–148sn)
- Ziyaretçi önizlemesi 'Bu profil sınırlı' gösteriyor; gizlilik ayarlarında 'Gizli hesap' açıkken 'Profili kimler görüntüleyebilir? Herkes' seçili görünüyor. Bu farklı izin seviyeleri olabilir, otomatik sunucu bug'ı kanıtı değildir.
- Test: herkese açık profil bilgisi vs gönderi görünürlüğünü iki hesapta açıkça anlat; ziyaretçi önizleme hâlâ uygun veriyi gösteriyor mu kontrol et.

### P2 — Hikâye açılışında gecikme/siyah spinner (60–64sn)
- Hikâye açılırken kısa siyah ekran/yükleyici var, arkasından medya sorunsuz görüntüleniyor. Bağlantı/video hazırlama süresi ölçülsün; hiç açılmıyor olarak sınıflandırma.

### P2 — Referansla kalan farklar
- Alt ortadaki Üret butonu daha büyük fakat referanstaki kadar iri/yükseltilmiş değil; çalışan yönlendirme korunarak değerlendirilsin.
- Referans tanıtım videosu kartında 00:28 gibi süre etiketi var, Build 402'de süre metni görülmüyor. Videonun silinmiş olduğu sonraki boş hali sorun değil.
- Öne çıkanlar: gerçek 'Yeni' ve 'Video' görünüyor; referansın isimli koleksiyonları ancak hesapta veri varsa çıkmalı, sahte albüm üretme.
- Kısayol alanında 'Kaydedilenler' iki satırda okunuyor ama küçük, diğer kısayollardan görsel uyum iyileştirilebilir.
- Geliştirilen renkler ve stat kartı referansa çok yaklaştı; geniş yeni tasarım değişikliğiyle çalışan layout geri alınmamalı.
- Bazı profil açılışlarında resim/medya yüklenirken kısa spinner var, performansı ölçmeden kesin ağ hatası deme.

## C. Aynen korunacak teknik sözleşme
- Build 400 kapak medya yükleme sözleşmesi `kind:'profiles'`, gerçek kapak/avatara veri bağlantısı, kullanıcı fotoğrafı/kadrajı.
- Build 401 görünür kapak/hikâye menü yazıları, hikâye 24 saat yükleme ve gerçek arşiv kayıtları, gelen kutusu/grup/arama, kaydedilenler, yorum/medya.
- Build 402 avatar-ad yan yana, dört sayaç ve canlı takip/arkadaşlık Firestore sorguları, intro video gerçek oynatıcı, gerçek öne çıkanlar, profile grid, profil arama/editleme, beş alt sekme, arkadaş-istekleri ve dış paylaşım.
- Dış paylaşımda yalnızca seçilen kişilere gönder, izin/engelleme kontrollerini koru. Kullanıcının WhatsApp konuşmalarının metnini, kişilerinin adını veya sohbet görüntülerini GitHub'a kopyalama.

## D. Test edilmemiş/yapıldı sanılmayacak
- Seçilen iki alıcının her birinin profil bağlantısını gerçekten **birer kez** alıp almadığı.
- Kaldırılan tanıtım videosunun medya depodan gerçekten temizlenmesi.
- Kaydedilenler'deki gri videonun dokunulunca tam oynayıp oynamadığı.
- Gizli hesap/görünürlük politikalarının ikinci test hesabına nasıl uygulandığı.
- Gerçek yeni kullanıcıya takip/arkadaşlık isteği, bildirim ve gizlilik kombinasyonları.
- Bu kayıt yalnız QA bulgusudur; kod değişikliği veya Build 403 APK'si değildir.

## E. Öncelikli sonraki kod akışı
1. Kaydedilenler gridindeki gri video kapağının kök nedenini bul; gerçek medya erişimini koruyarak önizleme fallback/timeout iyileştir.
2. Profil gizlilik açıklamasını iki hesapta doğrula ve kalan küçük tasarım farklarını tamamla.
3. Paylaşım seçimi/sayacı tutarlı, mevcut çalışan paylaşımı bozma; yalnız iki hesapla teslimat regresyonu yap.
4. Regresyon + Flutter analyze + sabit imzalı release + gerçek cihaz testleri; Build 402'de çalışan ekranları bozma.
