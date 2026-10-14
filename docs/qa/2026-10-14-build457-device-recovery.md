# Build 457 cihaz hata paketi — geliştirme/test aşamasında

Build456 onaylanmış başarı SHA: `3e8ff6cfc52a99e27fc060f8670d01017333a03e`; kayıtlar #47–#52 ve 47456.mp4 videosu. Build 457 yeni dalda hazırlanır, `main` değiştirilmez. Çalışan topluluk video yükleme korunur.

## İlk değişiklikler (henüz Android cihazında doğrulanmadı)
- Canlı yayın video track henüz gelmiyorsa 10 saniye sonra sonsuz spinner yerine açıklama + yayıncı için kamerayı yeniden başlat, izleyici için yeniden bağlan seçenekleri.
- Canlı yayında görüntü ayarları Firestore dinleyicisi ekranın saniye sayacı yeniden çizdikçe yeniden oluşturulmasın.
- Eksik track için uygulama testleri; önceki giriş, sohbet, medya yükleme ve sunucu yetkileri korunur.

## Takip edilen cihaz hataları
- #47 Akış siyah ekran ve medya yüklemesi; #48 canlı/topluluk/video siyah ekran — P0.
- #49 çağrı zil sesi duyulmuyor; #50 Keşfet topluluk avatarları spinner'da kalıyor.
- #51 canlı yayın boş beyaz alt modal + referans yayıncı/izleyici tasarımı.
- #52 Gelen Kutusu farklı UID / kullanıcı profil adının yanlış eşlemesi, yanlış alıcı riski.
- 47456.mp4: kapak kadrajı kurucu için bile izinsiz; sohbet fotoğraf %100 sonrası mesaj görünürlüğü; geri dönüşlerde siyah ekran / tekrar yükleme.

**Önemli:** Kodun başarılı derlenmesi kamera/RTC görüntüsünün gerçekten geldiğini kanıtlamaz; siyah görüntü devam ediyorsa ayrıca sunucu ve cihaz loglarıyla teşhis gerekir. Hesaplar/veriler silinmez, ücretli Cloud Functions/Firestore canlı kuralları izinsiz dağıtılmaz. PR inceleme taslağıdır.

## Gelen Kutusu kişi kimliği düzeltme aşaması
- Birebir sohbet satırlarında sohbetin karşı üyeleri arasında **kendi hesabın dışında UID yoksa** satır artık mevcut kullanıcı profili gibi gösterilmez.
- Profil dinleyicileri kullanıcı UID'siyle sabitlenir, her sohbet satırı `chatId + karşı taraf UID` ile anahtarlanır; sıralama veya filtrelemede eski satırın profilinin gösterilmesi engellenir.
- Dinleyiciden gelen belge UID'si beklenen karşı üye UID'siyle eşleşmezse isim ve görsel gösterilmez. Hata durumunda yeniden dene sunulur.
- Sohbetin kimliği, kayıtlı mesajlar, karşı tarafın bilerek tanımlanmış takma adı ve grup sohbetleri korunur. Bu değişiklik **yanlış kişiye mesaj teslim edildiği kanıtı değildir**; #52 cihaz testi gerekir.

## Derleme sırası düzeltmesi
İlk Build 457 koşusu #53 commit `a5f55fb`, eski `tools/build448.patch` canlı yayın kaynağına uygulanamadığından başarısız oldu. Bu, **APK oluşturulmadan** gerçekleşen CI yama çakışmasıdır. Orijinal canlı yayın kaynak dosyası geri konularak Build448 önce uygulanır; yeni Build457 video toparlama kodu **Build456 yamalarından sonra** güvenli, tek seferlik kaynak dönüştürmesiyle eklenir. Build448'in zaten var olan `_liveStream448` ve `_clock448` optimizasyonları tekrar oluşturulmaz; video kurtarma düğmesi için saniyelik `ValueListenableBuilder` kullanılır. Yeni CI sonucu bekleniyor.

## Keşfet avatar görüntüleme (#50)
Topluluk kartlarının görsel yüklemesi süresince dönen gösterge yerine yer tutucu grup ikonu; URL başarısız olduğunda **yeniden dene** ikonuyla kullanıcı etkileşimi. Mevcut `NgelXAgResmi`/kimlikli URL çözümlemesi ve çalışan video yükleme akışı korunur. Bu görüntüleme UX düzeltmesi, ağdaki gerçek erişim sorununu çözdüğü anlamına gelmez.

## Kimlik koruması üretim zinciri notu
Üçüncü CI denemesinde canlı kurtarma ve Keşfet görsel düzeltmesi test adımlarına kadar ilerledi; ancak eski Gelen Kutusu üretimi beklenen sohbet satırını içermediğinden kimlik yaması güvenli biçimde uygulanamadı. Yeni adım eşleşmeyen kodu değiştirmez, yalnız derleme kaydında kullanıcı verisi içermeyen kaynak bölümünü gösterir. #52 **çözülmüş kabul edilmeyecek**; kimlik eşlemesi gerçek kod üzerinde ayrıca test edilecek. Diğer düzeltmelerin derlemesini bu ayrı teşhis aşaması engellemez.


## 15 Ekim — Gerçek oluşturulan sohbet kodunda takma ad modeli (#52)
İlk inceleme ham `main.dart` dosyasındaki eski `nicknames.$me` kaydını görüp takma adların görüntüleyen UID'siyle saklandığını varsaydı. CI'da üretilen **nihai** kodun incelemesi bu varsayımın yanlış olduğunu gösterdi: `SohbetBilgiPage.takmaAd()` `nicknames:{uid:...}` alanına, yani **takma ad verilen kişinin UID'sine** yazıyor; Sohbet başlığı da `nicks[widget.digerUid]` okuyor. Bu nedenle Build455'teki `takmalar[other]` dönüşümü doğru, yanlışlıkla kaldıran taslak değişiklik geri alındı. Güncel regresyon testi nihai üretilen kaynakta bu üç erişimin uyuşmasını kontrol eder.

Asıl güvenlik/karışma riski: birebir Gelen Kutusu satırında karşı taraf bulunmazsa `other` kendi UID'sine düşebiliyor; `StreamBuilder` da satır kimliğine sabitlenmemişti. Yeni yama, güncel CI'ın ürettiği `_profiles453` dinleyicisine **sohbet + UID anahtarı, eksik/hatalı profil durumları ve kendi hesabına düşmeyi engelleyen kontrol** ekler. Mesaj belgeleri, kullanıcı profilleri ve gerçek adlar yazılarak değiştirilmez. Gerçek cihazda iki hesaplı test bitmeden #52 kapatılmamalı.

## Build457 — Topluluk kapak yetkisi ve gereksiz yazma (#54)
Kurucu `founderId` alanıyla doğrulanır; eski toplulukta `admins` eksikse sadece istemci yanlışlıkla `yetki` demesin. Ancak Firebase sunucu kuralları hâlâ son yetkili mercidir; kurucu istemcide kabul edilse bile eski dağıtılmış kural reddederse **sunucu güvenlik kuralları kontrol edilmeli** uyarısı gösterilir, kural atlatılmaz. Kadraj tek başına değiştiğinde `coverUrl` gönderilmez ve değişiklik yoksa belgeye boş yere yazılmaz. Çalışan topluluk video/fotoğraf yüklemeleri, hesaplar ve izinler korunur; sunucu kuralları otomatik dağıtılmaz. Flutter saf fonksiyon testi eklenir; gerçek cihaz kaydı hâlâ kabul testi bekler.
