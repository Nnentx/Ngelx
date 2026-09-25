# NgelX V42 Work Paketi – Test Notları

## Gelen kutusu

- Tümünü okundu yap düğmesi gerçek sohbet ve aktivite sayaçlarını sıfırlar.
- Tümü, Okunmamış, Arkadaşlar ve Gruplar filtreleri ayrıştırıldı; uzun etiketlerin taşması önlendi.
- Arkadaşlar filtresi yalnızca gerçek arkadaşları gösterir.
- Arama grup adı, kişi adı, kullanıcı adı ve son mesaj üzerinde çalışır.
- Sabitlenen sohbetler önce gösterilir.
- Grup ve özel sohbet açıldığında okunmamış sayısı sıfırlanır.
- Sohbet açıldığında ve yeni mesaj geldiğinde liste otomatik olarak en son mesaja gider.
- Sessize alma için 1 saat, 8 saat, 1 hafta ve süresiz seçenekleri eklendi.
- Arşivleme ve arşivden çıkarma korunur.

## Mesaj istekleri

- Kabul edilmemiş istekler normal gelen kutusuna sızmaz.
- İstek önizleme ekranı eklendi.
- Kabul et, reddet ve engelle işlemleri gerçek veriye bağlıdır.
- Kabul edilen istekten sonra arkadaşlık gizlilik kuralı yanıt göndermeyi yanlışlıkla engellemez.

## Grup oluşturma ve yönetim

- Grup adı en fazla 16 kelimedir.
- Yönetici dahil toplam üye sınırı 60'tır.
- Grup fotoğrafı oluşturma sırasında seçilip önizlenebilir.
- Grup adı ve fotoğrafını yalnızca yöneticiler değiştirebilir.
- Yönetici ekleme/çıkarma ve üyeyi gruptan çıkarma onaylı işlemlerdir.
- Gruptan ayrılma ve son üyenin grubu silmesi onay ister.
- Tek yönetici, yönetimi devretmeden dolu gruptan ayrılamaz.
- Yönetici yeni üye ekleyebilir; 60 kişi sınırı burada da uygulanır.
- Yalnızca yöneticiler yazabilsin, geçmiş görünürlüğü ve katılma onayı ayarları eklendi.
- Yöneticiye özel veri değişiklikleri Firestore güvenlik kurallarıyla korunur.

## Grup sohbeti

- Anket özelliği grup sohbetinden tamamen kaldırıldı ve geri eklenmemesi sözleşme testiyle korunuyor.
- @ menüsü “Kişiler” ve “Mesaj seçenekleri” olarak ayrıldı; @herkes ve @sessiz seçenekleri görsel olarak belirginleştirildi.
- Mesaj tepkilerine genişletilmiş emoji seçici eklendi.
- Sesli mesaj oynatıcıya oynat/duraklat, ilerleme çubuğu, ileri-geri sarma ve süre göstergesi eklendi.
- Cevapsız aramalarda tam ekran “Arama cevaplanmadı” görünümü, “Tekrar Ara” ve “Sohbete dön” seçenekleri eklendi; bire bir aramalarda da karşı taraf katılmadıysa cevapsız durumuna düşer.
- Mesajlarda gönderen adı ve profil fotoğrafı görünür.
- Metin, fotoğraf, video, ses, dosya, konum, çıkartma, GIF ve bağlantı gönderilebilir.
- Kamera, galeri, video, dosya, konum, çıkartma ve GIF menülerinin metin etiketleri vardır.
- Fotoğraflar ve GIF'ler tam ekran açılır.
- Emoji seçici ve `@kullanıcı` önerileri eklendi.
- Uzun basma ile yanıtla, kopyala, düzenle, sil, tepki, şikâyet ve yönetici için sabitleme çalışır.
- Mesaj silme işlemi onay ister; grup yöneticisi gerektiğinde üye mesajını da kaldırabilir.
- Sabitlenen mesajlar ile medya/bağlantılar ayrı ekranlarda listelenir.
- Yalnızca yöneticiler yazabilir ayarı gönderim sırasında da uygulanır.
- Sesli ve görüntülü grup araması LiveKit odasına bağlanır; diğer üyelere arama bildirimi oluşturulur.

## Özel sohbet

- Mesaj uzun basma menüsü, tepkiler, düzenleme, silme, yanıtlama ve şikâyet eklendi.
- Fotoğraf tam ekran açılır.
- Emoji seçici eklendi.
- Sesli ve görüntülü arama LiveKit üzerinden gerçek odaya bağlanır.
- Sohbet bilgileri beyaz tasarıma geçirildi.
- Takma ad, sohbet içinde arama, özel arka plan rengi, medya, sabit mesajlar, sessize alma, kısıtlama, engelleme, kaldırma ve şikâyet seçenekleri bağlandı.

## İçerik ve kaydedilenler

- İçerik dili tercihi artık uygulamanın genel dilini yanlışlıkla değiştirmez; içerik bazında saklanır.
- Altyazı bulunmayan içerikte sahte çalışan anahtar yerine açık durum bilgisi gösterilir.
- Silinmiş içeriklerin bozuk kartları kaydedilenlerden otomatik temizlenir.

## Güvenlik ve yayınlama notu

- Yeni sohbet, grup yönetimi, tepki, sabitleme ve arama kayıtları için Firestore kuralları güncellendi.
- Uygulama koduyla birlikte `firestore.rules` dosyası da yayınlanmalıdır.
- APK üretmeden önce Flutter analizinin hatasız geçmesi ve iki farklı hesapla arama/mesaj isteği testinin yapılması gerekir.


## 2026-09-20 Konsolide test durumu

### Telefonda test edildi ve çalışan davranışlar
- Özel sohbetten fotoğraf/logo arka planı seçme çalıştı.
- Takma ad kaydetme çalıştı.
- Kişiyi paylaş Android paylaşım ekranını açtı.
- Sohbeti listeden kaldırma işlemi çalıştı.
- Sohbet bilgi ekranı beyaz ve bölümlü tasarıma geçti.
- Medya / sabitlenmiş mesajlar / sessize alma / bildirimler / mesaj izinleri / kısıtla / engelle / sohbeti sil satırları görünür durumda.
- Alttaki yinelenen ikinci “Şikâyet et” satırı kaldırıldı; sağ üst üç nokta menüsündeki şikâyet kaldı.
- Özel arka planı kaldırma artık onay istemeden silmeyecek şekilde değiştirildi.
- Kısıtla / Engelle / Sohbeti sil onay pencerelerindeki beyaz üstüne beyaz yazı sorunu düzeltildi.

### Kodlandı, yeni APK’da yeniden test edilecek
- Mesaj / fotoğraf / paylaşılan içerikte çift dokununca ❤️ bırakma.
- Uzun basma tepkileri ve “Daha fazla” menüsü.
- Sesli ve görüntülü arama ekranının bildirim işleminden bağımsız açılması.
- Kamera / mikrofon çalışma zamanı izinleri ve LiveKit video render akışı.
- Görüntülü aramada yerel görüntü, uzak görüntü, efektler, rötuş ve bulanıklaştırma.
- Özelleştir içinden hızlı gönderme emojisi seçme.
- Özelleştir içinden arka plan görünürlüğü seçme, mesaj yazı boyutu seçme ve tüm özelleştirmeyi sıfırlama.
- Mesaj yanıtını “↪ metin” yerine gerçek alıntı kartı olarak gösterme.
- Profilde Takip et / Takiptesin durumunu canlı güncelleme ve takipten çıkarken onay isteme.
- Kişiyi paylaş metnini kısa ve temiz NgelX profil bağlantısına dönüştürme.
- Yorumlarda uzun basma tepki satırı, çift dokunma kalbi ve yorum silme / gönderimden kaldırma.

### Bilinen açık hata — özellikle sonraya bırakıldı
- Grup sohbetine girildiğinde “Mesajlar sunucudan alınıyor…” ekranında kalma / donma. Kullanıcıyla birlikte bu alanı daha sonra ayrı ele alma kararı verildi. Bu nedenle yeni sohbet/profil paketlerinde grup mesaj yükleme koduna dokunulmuyor.
- Grup tarafındaki arama ve medya davranışları, grup mesaj yükleme sorunu çözülmeden “tamamlandı” sayılmayacak.

### Proje kapsamındaki kalan kabul edilmiş işler — tek tek doğrulanacak
- Ortak gruplar.
- Profil tanıtım videosu.
- Profil ziyaretçisine özel önizleme görünümü.
- Profil paylaşım gizliliği.
- Takip isteği geçmişi.
- Arkadaşlık yıldönümü.
- Takipçi arama / filtreleme ve takipçiyi kaldırma.
- Profil ziyaret izinleri ve içerik gizleme kitle seçenekleri.
- Hikâye arşivi / öne çıkanlar.
- Profilde en fazla 3 sabitlenmiş gönderi kuralının uçtan uca doğrulanması.
- Gizli kelimeler için yalnızca aç/kapat değil, kullanıcıya özel kelime listesi yönetimi.
- Hesap kurtarma seçeneklerinin e-posta/telefon akışlarıyla uçtan uca tamamlanması.
- Profil ziyaret eğilimleri ve en çok etkileşim alan gönderiler gibi sahip analitiklerinin doğrulanması.
- Giriş yapılan cihazlardan uzaktan çıkış işlevinin doğrulanması.
- Akışta yeni içeriklerin üstte sıralanması, tüm gönderi tiplerinde tarih/saat gösterimi ve geri tuşu kullanmadan sonraki/önceki içeriğe geçişin her içerik tipinde test edilmesi.

### Paket yayınlama kuralı
- Son APK “hazır” sayılmadan önce son commit için Flutter analiz, test, release APK ve imza doğrulama adımlarının tamamı yeşil olmalı.
- Sesli/görüntülü arama ve mesaj tepkileri en az iki ayrı gerçek hesapla telefonda tekrar denenmeli.
- Grup mesaj yükleme sorunu çözülmedikçe grup bölümü için “tamamlandı” ifadesi kullanılmamalı.

### 2026-09-23 yeni açık hata — Gizli kelimeler
- Profil > Gizlilik > Gizli kelimeler ekranında kelime girip listeye ekleme sırasında/sonrasında uygulama kırmızı Flutter hata ekranına düşüyor.
- Telefonda görülen assertion: `framework.dart: Failed assertion: line 6281 pos 12: '_dependents.isEmpty': is not true.`
- Örnek durumda mevcut kelimeler `aleyna`, `kandemir`; yeni olarak `test` yazılırken/eklenirken hata görüldü.
- Bu hata unutulmayacak; final Work paketinde gizli kelime ekleme/silme, bottom-sheet kapanışı ve ilgili widget yaşam döngüsü birlikte düzeltilip gerçek cihazda tekrar test edilecek.

### 2026-09-23 giriş ekranı değişikliği — Misafir girişi kaldırılacak
- Giriş ekranındaki **“Misafir olarak keşfet”** bölümü gereksiz bulundu ve kaldırılacak.
- Giriş ekranında yalnızca normal giriş, şifremi unuttum ve hesap oluşturma akışları kalacak.
- Misafir/anonim girişe bağlı buton, yönlendirme ve gereksiz kodlar final Work paketinde temizlenecek; mevcut çalışan giriş/kayıt akışları korunacak.

### 2026-09-23 giriş/kayıt UX — sade iyileştirmeler
- Kullanıcı adı yazılırken anlık uygunluk kontrolü gösterilecek: “Kullanılabilir” / “Bu kullanıcı adı alınmış”.
- E-posta alanında yazım hataları mümkün olduğunca anında gösterilecek; uygun yerlerde `@gmail.com` benzeri alan adı önerisi verilecek.
- Kayıttan sonra ayrı ve sade bir e-posta doğrulama ekranı olacak: **Doğrulama e-postasını tekrar gönder** ve **Doğruladım, devam et** seçenekleri bulunacak.
- Form hataları yalnızca SnackBar ile değil, ilgili giriş alanının hemen altında küçük ve anlaşılır hata metniyle gösterilecek.
- Giriş butonuna basıldığında işlem tamamlanana kadar buton kilitlenecek ve yükleme göstergesi çıkacak; böylece üst üste istek ve donmuş hissi azaltılacak.
- Bu paket sade tutulacak; şimdilik Google/Apple/QR/biyometrik giriş gibi ek akışlar eklenmeyecek.

### 2026-09-23 uygulama simgesi — NgelX logosu
- Telefonda uygulama listesinde görünen **NgelX “N” logosu** resmi uygulama simgesi olarak kullanılacak.
- APK kurulurken / güncellenirken, ana ekranda ve uygulama çekmecesinde aynı NgelX simgesi görünmeli.
- Android adaptive icon, round icon ve normal launcher icon sürümleri aynı tasarımdan üretilecek; eski/geçici simgeler kaldırılacak.
- Simgenin arka planı ve kırpılması farklı Android cihazlarda bozulmayacak şekilde kontrol edilecek.

### 2026-09-23 uygulama dili — tüm ekranlarda tek dil
- Uygulama dili hangi dil seçiliyse uygulama içindeki tüm metinler aynı dili takip edecek.
- Türkçe seçiliyse ekranlar, butonlar, hata mesajları ve açıklamalar Türkçe; İngilizce seçiliyse İngilizce olacak.
- Sabit kodlanmış Türkçe/İngilizce metinler temizlenip mevcut dil sistemi üzerinden gösterilecek.
- Dil değiştirildiğinde mümkün olan tüm ekranlar yeniden giriş gerektirmeden güncellenecek; karışık dil görünümü olmayacak.

### 2026-09-23 genel kod temizliği — güvenli sadeleştirme
- Giriş, Üret, Keşfet, Ayarlar, Profil ve bağlı ekranlarda gerçekten kullanılmayan / yinelenen kodlar temizlenecek.
- Çalışan özellikleri bozabilecek agresif silme yapılmayacak; yalnızca derleyici tarafından kullanılmadığı doğrulanan veya davranışı tamamen yinelenen kod kaldırılacak.
- Bu ilk temizlikte kullanılmayan medya hata değişkeni, Üret içindeki kullanılmayan kapak değişkeni, kullanılmayan grup aktif-üye yardımcı kodu, kullanılmayan arama durumu değişkeni ve Profil içindeki kullanılmayan takip snapshot değişkeni kaldırıldı.
- Her temizlik turundan sonra analiz + test + APK derleme adımları yeşil olmadan paket hazır sayılmayacak.

### 2026-09-23 profil — çoklu hesap ve hesap değiştirme
- NgelX’te aynı cihazda **en fazla 5 kayıtlı hesap** tutulması planlanıyor.
- Profil ekranında kullanıcı adının yanında küçük bir `⌄` oku olacak; dokununca alttan beyaz bir hesap seçme paneli açılacak.
- Panelde kayıtlı hesaplar profil fotoğrafı + ad + `@kullanıcıadı` ile listelenecek; aktif hesabın yanında `✓` gösterilecek.
- Panelin altında **Başka hesap ekle** ve **Hesapları yönet** seçenekleri bulunacak.
- Hesaba dokununca diğer hesabın oturumu kapanmadan doğrudan hesap değiştirilecek.
- **Çıkış yap** ile **Hesap değiştir** ayrı işlemler olacak.
- İkinci erişim noktası: Ayarlar ve gizlilik > Hesaplar > Hesap değiştir / Hesap ekle.
- Her hesabın oturum bilgisi ayrı ve güvenli tutulacak; hesaplar birbirinin mesaj, bildirim veya taslak verilerini karıştırmayacak.

### 2026-09-23 Üret ekranı — aktif yayınlama düzeltmesi
- Üret ekranı sadeleştirildi; ana akış artık **Video / Fotoğraf / Yazı** üzerine kurulu.
- Galeriden fotoğraf ve video seçme, kameradan fotoğraf/video çekme ve yayınlama akışı gerçek işlemlere bağlandı.
- Fotoğraf için 10 MB, video için 50 MB sınırı kullanıcıya seçim sırasında gösteriliyor ve kontrol ediliyor.
- Video yükleme büyük dosyayı tamamen RAM'e almadan akış (stream) olarak medya servisine gönderiliyor; yavaş bağlantıda daha uzun yükleme süresi destekleniyor.
- Firestore'daki medya servis adresi bozuk/eski olursa APK içindeki güvenli Worker adresi ikinci aday olarak deneniyor.
- Yükleme sırasında gerçek ilerleme çubuğu ve yüzde bilgisi gösteriliyor; işlem devam ederken tekrar yayınlama engelleniyor.
- Android galeriden/kameradan dönüşte işletim sistemi uygulamayı yeniden oluşturursa ImagePicker `retrieveLostData()` ile seçilen medya kurtarılıyor.
- Seçilen fotoğraf için gerçek önizleme, video için belirgin seçili medya kartı ve “seçimi kaldır” eklendi.
- **Hikâye** hızlı butonu artık 24 saatlik gerçek fotoğraf hikâyesi yayınlıyor; **Reels** video galerisine, **Kamera** kamera seçimine, **Canlı** canlı yayın hazırlığına bağlı.
- Çalışmayan/sahte “Kırp, Filtre, Efekt, Hız, Metin, GIF/çıkartma, Kolaj, Kapak, Seslendirme, Önce/sonra” chip'leri kaldırıldı; yalnızca gerçekten çalışan kontroller bırakıldı.
- Boş çalışan **Zamanla**, geri alınamayan **Taslak kaydet**, gerçek işlem yapmayan **Otomatik altyazı**, **Ortak gönderi**, kalite seçimi ve fotoğrafa müzik ekleme kontrolleri Üret ekranından kaldırıldı; yeniden eklenirse uçtan uca çalışan haliyle eklenecek.
- “Yeniden paylaşıma izin ver” ayarı artık gerçek paylaşım menüsünde uygulanıyor; kapalı içerik sahibi dışındaki kullanıcılar yeniden paylaşamıyor.
- Eski/tekrarlı `EskiYuklePage` tamamen kaldırıldı.
- Son doğrulama: fotoğraf, video ve yazı paylaşımı iki gerçek hesapla cihazda yeniden test edilecek; yayınlanan içerik hem Akış'ta hem Profil'de görünmeli.

### 2026-09-23 Akış ekranı — gerçek içerik / performans temizliği
- Akıştaki demo/örnek videolar tamamen kaldırıldı; artık yalnızca Firestore'daki gerçek NgelX paylaşımları gösterilecek.
- Akış en yeni `createdAt` içeriği üstte olacak şekilde kalacak; sorgu limiti 20'den 50'ye çıkarıldı.
- Takip, arkadaş, engellenen hesaplar, `hiddenContent` ve `notInterestedIds` kullanıcı belgesinden canlı takip ediliyor; gizlenen/ilgilenilmeyen içerik akıştan anında düşecek.
- Bozuk/eksik medya kaydı (videosuz video, fotosuz fotoğraf, boş yazı) akışta boş kart üretmeyecek.
- `viewCount` akışta gerçek görüntülemede, aynı oturumda içerik başına bir kez artırılıyor; kendi içeriği için artırılmıyor.
- Video kartındaki sabit “Anı yakala...” / sahte “Özgün ses” metni kaldırıldı; gerçek gönderi açıklaması gösterilecek.
- Fotoğraf/yazı kartında kullanıcı adına dokununca paylaşan kişinin profili açılacak; fotoğraf yüklenirken görünür loading durumu eklendi.
- Fotoğraf/yazı ve video kartlarındaki kullanılmayan aggregate beğeni/yorum sorguları kaldırıldı; aynı etkileşim için tekrar tekrar Firestore okuması azaltıldı.
- Kullanılmayan `CanliEtkilesimOzet` widget'ı ve eski `ornek_` koşulları temizlendi.
- Yazı gönderilerinde anlamsız “İndir” seçeneği gösterilmeyecek.
- Video uzun basma menüsündeki, zaten “Araçlar > Oynatma hızı” içinde bulunan ikinci hız seçimi kaldırıldı.
- Eski verilerde `allowDownload` string olarak tutulmuş olsa bile indirme gizliliği korunacak.
- Şu an “Sana Özel” gerçek öneri algoritması değil; izin verilen gerçek içerikleri kronolojik gösteriyor. Kullanıcı tabanı büyüyünce ayrı sıralama/pagination çalışması yapılmalı.


### 2026-09-23 sürüm etiketi + grup fotoğrafı sağlamlaştırma
- Ayarlar > Uygulama güncellemeleri bölümündeki sabit **V42** kaldırıldı; APK artık `pubspec.yaml` içindeki gerçek sürüm ve build numarasını derleme sırasında alıp gösteriyor.
- Mevcut paket için ekranda **v1.0.57 • Yapı 211** görünmesi bekleniyor; sonraki sürümlerde aynı alan CI tarafından otomatik güncellenecek.
- Yeni grup oluştururken seçilen grup fotoğrafının yüklenmesi için dış 12 saniyelik erken zaman aşımı kaldırılıp 75 saniyeye çıkarıldı; R2 medya servisinin gerçek bağlantı/yükleme süresine izin veriliyor.
- Grup fotoğrafı yüklemesi yine de başarısız olursa grup oluşturma akışı çökmeyecek ve kullanıcıya fotoğrafın atlandığı açıkça bildirilecek.

### 2026-09-23 grup medya bellek/çökme koruması
- Grup sohbetinde video gönderimi artık 80 MB'a kadar dosyanın tamamını RAM'e almıyor; dosya medya servisine stream olarak yükleniyor.
- Grup dosya gönderimi de 30 MB dosyayı `readAsBytes()` ile belleğe kopyalamak yerine diskten stream ediyor.
- Bu değişiklik düşük/orta RAM'li Android cihazlarda büyük grup videosu veya dosyası gönderirken uygulamanın ağırlaşma/çökme riskini azaltıyor.
- CI sözleşmesine grup video/dosya akışının tekrar `readAsBytes()` kullanımına dönmesini engelleyen kontrol eklendi.

### 2026-09-23 hesap izolasyonu + uygulama dili + Keşfet kişi kartları
- Oturumdaki Firebase kullanıcı kimliği değiştiğinde `UygulamaDurumKapisi` ve `AnaEkran` artık UID ile yeniden anahtarlanıyor. Böylece önceki hesaptan kalan profil, gelen arama/oda katmanı, mesaj önbelleği veya sekme state'i yeni hesaba taşınmıyor.
- Bu koruma özellikle hesap değiştirme akışı için eklendi; farklı hesaba ait aktivite/profil bilgisinin aynı ekranda kalma riski azaltıldı.
- Ayarlar, Profil, Keşfet ve Üret ekranlarının ana görünür başlık/aksiyonları mevcut ortak dil sistemine bağlandı. Türkçe/İngilizce yanında mevcut Almanca/Arapça/Rusça sözlük karşılıkları da eklendi.
- Üret ekranında gizlilik ve yorum hedefi Firestore'da mevcut sabit kodlarla tutulmaya devam ediyor; kullanıcıya gösterilen etiket seçilen uygulama diline göre çevriliyor. Böylece veri sözleşmesi bozulmadan arayüz dili değişiyor.
- Keşfet > Kişiler artık aktif hesabın kendisini öneri kartı olarak göstermiyor ve `deactivated` hesapları ayıklıyor.
- Keşfet kişi kartındaki yeşil çevrimiçi noktası artık herkese sabit gösterilmiyor; yalnızca gerçekten `isOnline=true` olan ve aktiflik görünürlüğünü kapatmamış hesaplarda çıkıyor.
- Dil dönüşümü henüz tüm ikincil dialog/hata metinlerinde tamamlanmış sayılmıyor; sonraki temizlik turunda Sohbet, grup ayrıntıları ve kalan yardımcı ekranlardaki sabit metinler ortak dil sistemine taşınacak.

### 2026-09-23 Gelen Kutusu — dil ve hesap güvenliği turu
- Gelen Kutusu başlığı, arama alanı, ana filtreler, Aktivite, Mesaj İstekleri, arşiv ve sohbet menüsü ana eylemleri ortak uygulama diline bağlandı.
- `Tümü / Okunmamış / Arkadaşlar / Gruplar` filtrelerinin Firestore/UI iç mantık kodları değiştirilmedi; yalnızca kullanıcıya gösterilen etiketler seçili dile çevriliyor. Böylece filtre davranışı dil değişiminden etkilenmiyor.
- Arşivlenen sohbetler ve mesaj isteği ekranlarının temel başlık/boş durum/kabul-red-engelle metinleri de seçili dili takip ediyor.
- CI sözleşmesine Gelen Kutusu filtrelerinin sabit iç kodlarını korurken çevrilmiş etiket göstermesini kontrol eden koruma eklendi.

### 2026-09-23 profil > mesaj gizliliği bağlantısı
- Başka kullanıcının profilindeki **Mesaj** butonu artık hedef hesabın `messagePermission` ayarını kontrol ediyor.
- `Herkes`, `Takip ettiklerim`, `Arkadaşlar`, `Kimse` seçenekleri profil üzerinden yeni sohbet açarken uygulanıyor; izin yoksa boş/donmuş ekran yerine açıklayıcı uyarı gösteriliyor.
- `Takip ettiklerim` seçeneğinde hedef hesabın gerçekten mesaj gönderen kullanıcıyı takip edip etmediği, `Arkadaşlar` seçeneğinde karşılıklı arkadaş kaydı kontrol ediliyor.
- Bu davranışın yanlışlıkla tekrar kaldırılmaması için CI sözleşmesine mesaj gizliliği kontrolü eklendi.

### 2026-09-23 yeni sohbet — mesaj gizliliği
- Gelen Kutusu > Yeni sohbet kişi seçicisinde de hedef hesabın `messagePermission` ayarı uygulanıyor.
- Hedef yalnızca arkadaşlarından veya kendi takip ettiği hesaplardan mesaj kabul ediyorsa yeni sohbet açılmadan önce ilişki kontrol ediliyor.
- Daha önce zaten var olan bir sohbet varsa kullanıcı mevcut konuşmasına erişebiliyor; gizlilik kontrolü yeni konuşma oluşturmayı sınırlandırıyor.
- Yeni sohbet ekranının başlık, arama ve boş durum metinleri de uygulama diline bağlandı.

### 2026-09-23 mesaj gizliliği — Firestore sunucu koruması
- Özel sohbet oluşturma artık yalnızca istemci butonlarında değil, Firestore güvenlik kurallarında da `messagePermission` ile korunuyor.
- `all`, `friends`, `following`, `none` izinleri sunucu tarafında doğrulanıyor; sahte/eski bir istemci gizlilik kontrolünü atlayarak yeni özel sohbet oluşturamıyor.
- Özel sohbet adı altında 3+ üyeli sahte sohbet oluşturma da reddediliyor; gerçek grup sohbeti akışı ayrı kurallarla çalışmaya devam ediyor.
- Emulator testlerine herkes/arkadaş/takip edilen/kimse izinleri ve sahte 3 üyeli özel sohbet senaryoları eklendi.

### 2026-09-23 özel sohbet medya kararlılığı
- Özel sohbette 30 MB'a kadar dosya gönderimi artık dosyanın tamamını RAM'e almıyor; grup sohbetindeki gibi diskten stream yükleme kullanıyor.
- Özel sohbet fotoğraf yüklemesindeki dış 12 saniyelik erken zaman aşımı 60 saniyeye çıkarıldı; yavaş bağlantıda gereksiz başarısızlık azaltıldı.
- CI sözleşmesine özel sohbet dosyasının yeniden `readAsBytes()` ile tamamen belleğe alınmasını engelleyen kontrol eklendi.

### 2026-09-23 mesaj gizliliği — mevcut sohbet uyumu
- Mesaj gizliliği sonradan sıkılaştırılsa bile daha önce karşı tarafça kabul edilmiş özel sohbetler profil ve Yeni sohbet ekranından yeniden açılabiliyor.
- Kabul edilmemiş eski bir mesaj isteği ise hedef hesabın güncel `messagePermission` kuralını atlamıyor.
- Profil ve Yeni sohbet giriş noktaları artık `SohbetPage` içindeki gerçek gönderim izni davranışıyla aynı mantığı izliyor.

### 2026-09-23 Mesaj izinleri + Aktivite dili
- Ayarlar > Mesaj izinleri ekranındaki `all / following / friends / none` veri kodları değiştirilmeden görünen başlık ve açıklamalar uygulama diline bağlandı.
- Aktivite ekranının başlığı, tümünü okundu yap eylemi, yükleme hatası ve boş durum metinleri ortak dil sistemine taşındı.
- Böylece gizlilik verisi mevcut Firestore sözleşmesini korurken Türkçe/İngilizce/Almanca/Arapça/Rusça arayüz etiketi seçili dile göre değişiyor.


## 2026-09-24 kritik cihaz düzeltmeleri — Build 249

- Giriş ekranındaki **Misafir olarak keşfet** metni/kodu kaynakta tamamen temizlendi.
- Eski APK'lardan cihazda kalmış anonim Firebase oturumu açılışta kapatılıyor; anonim kullanıcı artık Ana Ekran'a düşmüyor.
- **Gizli kelimeler** yönetimi klavye + modal bottom-sheet yaşam döngüsü çakışmasını önlemek için ayrı beyaz sayfaya taşındı.
- Gizli kelime ekleme/silme sırasında TextEditingController artık setState içinde temizlenmiyor; Firestore yazımı tamamlandıktan sonra liste güncelleniyor ve odak güvenli biçimde kapatılıyor.
- Firestore'daki eski/bozuk hiddenWords değerleri String'e normalize edilerek okunuyor.
- Telefonda görülen framework.dart / _dependents.isEmpty assertion hatasının tekrarını engellemek için eski _GizliKelimeSheet kaldırıldı.
- Üret ekranındaki Connection reset by peer medya hatası için Android'e ağ katmanı fallback'i eklendi:
  - Worker /upload/presign çağrısı Dio bağlantı hatasında yerel HttpURLConnection ile tekrar deneniyor.
  - Signed R2 PUT Dio'da bağlantı hatası verirse fotoğraf/byte yüklemesi yerel PUT ile, video/dosya yüklemesi dosyadan stream edilen yerel PUT ile tekrar deneniyor.
  - Birincil ve yedek Worker adresleri korunuyor.
- Sürüm **v1.0.57 • Yapı 249** olarak yükseltildi.
- tools/verify_ngelx_contract.py içine misafir girişinin geri gelmesini, eski gizli-kelime bottom-sheet'inin geri gelmesini ve Android medya fallback'lerinin kaybolmasını engelleyen sözleşme kontrolleri eklendi.

### Build 249 gerçek cihaz doğrulama sırası

1. Uygulamayı güncelle ve Ayarlar > Uygulama güncellemeleri alanında **Yapı 249** yazdığını doğrula.
2. Çıkış yap; giriş ekranında **Misafir olarak keşfet** görünmemeli.
3. Profil > Gizlilik > Gizli kelimeler: test ve ikinci bir kelime ekle, birini sil, klavyeyi aç/kapat, geri dön. Kırmızı Flutter ekranı çıkmamalı.
4. Üret > Fotoğraf: küçük bir fotoğraf yayınla; ardından yaklaşık 5–10 MB fotoğraf dene.
5. Üret > Video: kısa bir video yayınla. presign bağlantı / Connection reset by peer hatası tekrar ederse ekranda görülen yeni hata metni kaydedilecek.
6. Yayınlanan fotoğraf/video hem Akış'ta hem Profil'de görünmeli.


## 2026-09-24 — Build 251 özel sohbet + aktiflik + grup diyalog paketi

- Grup çıkış/kuruculuk diyaloglarında beyaz zemin üstünde kaybolan başlık ve açıklamalar koyu renge sabitlendi.
- Profil aktiflik satırı canlı hale getirildi: çevrimdışında **Az önce aktifti / X dk önce aktifti / X saat önce aktifti / X gün önce aktifti** gösteriyor.
- Özel sohbette **@herkes kaldırıldı**; @herkes yalnızca grup sohbetlerinde kalıyor.
- Özel mesajlaşma, grup sohbetindeki yeşil premium tasarımın mavi karşılığına geçirildi:
  - mavi başlık ve avatar halkası,
  - mavi/beyaz premium mesaj balonları,
  - mavi yazma göstergesi, cevap kartı ve alt mesaj paneli,
  - mavi Sohbet Bilgisi / Özelleştir görünümü.
- Özel sohbet taslakları cihazda saklanıyor; sohbetten çıkıp dönünce yazılmamış metin geri geliyor.
- Özel sohbete doğrudan **video / video çek** gönderimi eklendi.
- Mesajlara tarih ayraçları (Bugün / Dün / tarih) eklendi.
- Gönderilen mesaj için **Mesaj bilgisi** ekranı eklendi; gönderim ve görülme durumu gösteriliyor.
- Build **v1.0.57 • Yapı 251**.

### Build 251 gerçek cihaz testi

1. Gelen Kutusu > bir grup > ayrıl/kuruculuk uyarısını aç: başlık ve açıklama görünür olmalı.
2. Rojin gibi bir profilde kullanıcı uygulamayı kapattıktan sonra aktiflik satırının dakika/saat sayacına dönmesini kontrol et.
3. Özel sohbette @ yaz: **@herkes çıkmamalı**. Grup sohbetinde @herkes çıkmalı.
4. Özel sohbet başlığı, mesaj balonları, yazma alanı ve Sohbet Bilgisi ekranı mavi tasarımda görünmeli.
5. Bir metin yazıp göndermeden sohbetten çıkıp geri gir: taslak geri gelmeli.
6. Özel sohbetten kısa video gönder ve tam ekran oynat.
7. Bir mesajı uzun bas > Daha fazla > Mesaj bilgisi ekranını aç.

## 2026-09-25 — Build 259 yorum + özel sohbet güvenilirlik düzeltmesi

- Akış yorum gönderimi artık kullanıcı profil belgesinin ağdan gelmesini beklemiyor; yorum önce güvenli bir yerel kullanıcı adıyla yazılıyor, profil adı/fotoğrafı arka planda tamamlanıyor.
- Yorum seçenekleri açılırken içerik sahibi sorgusu en fazla 1,5 saniye bekletiliyor; zayıf bağlantıda menünün hiç açılmaması önlendi.
- Yorumdaki **Şikâyet et** ve **Kullanıcıyı engelle** kullanıcı etkileşimleri artık 12 saniyelik dış zaman aşımıyla kesilmiyor.
- Özel sohbet yazma satırındaki ayrı Kamera ve Galeri kısayolları kaldırıldı; bu seçenekler **+** menüsünde duruyor. Böylece mesaj alanı genişledi ve **Mesaj** yazısındaki son harfin alt satıra düşmesi engellendi.
- Sürüm **v1.0.57 • Yapı 259**.

### Build 259 gerçek cihaz testi

1. Akış > Yorumlar: **slm** yazıp gönder; yorum birkaç saniye içinde görünmeli ve metin alanı temizlenmeli.
2. Bir yoruma uzun bas veya üç nokta menüsüne dokun; menü zayıf bağlantıda da açılmalı.
3. **Kopyala** ile yorumu panoya kopyala; ardından **Şikâyet et** ve **Kullanıcıyı engelle** akışlarının kullanıcı seçim süresi yüzünden kapanmadığını kontrol et.
4. Özel sohbete gir; alt alanda **Mesaj** tek satır görünmeli, son **j** aşağı düşmemeli.
5. Kamera ve Fotoğraf seçeneklerinin özel sohbette **+** menüsü altında hâlâ çalıştığını doğrula.

## 2026-09-25 — Build 260 yorum performans ve Kopyala düzeltmesi

- Yorum üç-nokta/uzun-bas menüsü açılmadan önce yapılan içerik sahibi Firestore sorgusu kaldırıldı; menü artık anında açılıyor.
- İçerik sahibi bilgisi yorum ekranı açılırken arka planda bir kez yükleniyor ve tüm yorum kartları tarafından paylaşılıyor.
- **Kopyala** işlemi artık bottom-sheet kapandıktan sonra beklemiyor; panoya yazma doğrudan Kopyala satırına dokunulduğu anda yapılıyor ve kullanıcıya "Yorum panoya kopyalandı" bildirimi gösteriliyor.
- Yorum ekranı Firestore yerel önbelleğini açılışta kullanıyor; önbellek varsa ağ beklenmeden yorumlar gösteriliyor.
- Yorum akışı tek seferde en fazla 120 kayıt dinliyor.
- Her yorum için tüm beğeni alt koleksiyonunu dinlemek yerine yalnızca aktif kullanıcının beğeni belgesi dinleniyor; toplam sayı yorum belgesindeki likeCount alanından okunuyor. Bu, yorum listesindeki eşzamanlı Firestore yükünü ciddi biçimde azaltıyor.
- Yorum gönderiminde içerik gizlilik/izin bilgisi açılışta yüklenen gönderi metasından kullanılıyor; aynı bilgi tekrar tekrar ağdan istenmiyor.
- Düzenle / Sil / Şikâyet / Engelle gibi menüden sonra açılan ikinci katmanlar için yalnızca kısa 120 ms geçiş payı bırakıldı.
- Sürüm **v1.0.57 • Yapı 260**.

### Build 260 gerçek cihaz testi

1. Yorumları aç: daha önce görüntülenen yorumlar mümkünse bekleme çarkı olmadan gelmeli.
2. Bir yorumdaki üç noktaya dokun: menü gecikmeden açılmalı.
3. **Kopyala**'ya dokun: menü kapanmalı ve "Yorum panoya kopyalandı ✅" bildirimi gelmeli; başka bir metin alanına yapıştırınca yorum metni çıkmalı.
4. Kendi yorumunda **Düzenle** ve **Yorumu sil** akışlarını tekrar dene.
5. Başka bir kullanıcının yorumunda **Şikâyet et** ve **Kullanıcıyı engelle** akışlarını dene.
6. Yorum listesini birkaç kez aç/kapat ve hızlı kaydır; takılma/boş beyaz ekran/uzun spinner olmamalı.

## 2026-09-25 — Build 261 özel sohbet hız/menü turu + logo koruması

- Kullanıcının talebi gereği **eski NgelX logo tasarım kodlamaları ve iki özgün logo asset'i korunuyor**. Belirli ekranlarda logo görünmeyecekse ortak logo kodu silinmeyecek; yalnızca o ekranın görünürlük/yerleşim davranışı değiştirilecek.
- CI sözleşmesine `Logo` widget'ı, `assets/ngelx_logo.png` ve `assets/ngelx_logo_horizontal.png` için koruma eklendi; yanlışlıkla silinmeleri build'i durduracak.
- Özel sohbet açılışında son 100 mesajın Firestore yerel önbelleği kullanılıyor; ağ akışı gelene kadar daha önce görülen sohbet boş görünmeyecek.
- Özel mesaj **Kopyala** işlemi yorumlardaki yeni güvenilir davranışa geçirildi: dokunulduğu anda panoya yazılıyor ve kullanıcıya açık başarı bildirimi veriliyor.
- Mesaj uzun-bas menüsündeki gereksiz 360 ms genel beklemeler kaldırıldı; yalnızca ikinci katman açılışlarında 100 ms güvenli geçiş bırakıldı.
- Yazma göstergesi ilk tuşta ek Firestore okuması yapmıyor; önceden alınmış sohbet ayarını kullanıyor.
- Mesaj gönderim izin/sohbet hazırlığı önbelleği 15 saniyeden 60 saniyeye çıkarıldı. Firestore güvenlik kuralları yine nihai yetki kontrolünü yapmaya devam ediyor.
- Sürüm **v1.0.57 • Yapı 261**.

### Build 261 gerçek cihaz testi

1. Daha önce mesaj bulunan özel sohbete gir: mesaj listesi gereksiz boş ekran/spinner göstermeden gelmeli.
2. Bir metin mesajına uzun bas > **Kopyala**: menü kapanmalı, "Mesaj panoya kopyalandı ✅" bildirimi görünmeli ve başka alana yapıştırınca aynı metin gelmeli.
3. Uzun bas > Yanıtla / Tepki / Daha fazla: menüler hızlı ve dengeli açılmalı.
4. Daha fazla > Düzenle / Mesaj bilgisi / Sabitle / Herkesten sil akışlarını kontrol et.
5. Birkaç kısa mesajı peş peşe gönder; gönderim alanı gereksiz beklememeli ve mesajlar ekranda görünmeli.
6. Yazı yazarken "yazıyor" göstergesi sohbeti ağırlaştırmamalı.
7. Logo kullanılan mevcut ekranları kontrol et: eski logo görünümü değişmemiş olmalı.

