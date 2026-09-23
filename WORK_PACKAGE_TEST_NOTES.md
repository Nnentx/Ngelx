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
