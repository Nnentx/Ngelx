# Build456 topluluk ve performans paketi

Temel: Build455 commit 74dc45b. Kullanıcının 47319–47355 cihaz bulguları ve son onaylanan beyaz–mor topluluk görseli. Mevcut kaynak üretim zinciri, kimlik doğrulama, özel/grup sohbetleri, hikâyeler ve aramalar korunur. Değişiklikler Build455 sonrasında uygulanır.

## Uygulananlar
- Kompakt beyaz–mor topluluk başlığı, kurallar, sekmeler ve fotoğraf/video/yazı paylaşım alanı; boş durum.
- Yatay kapak ve avatar önizlemeleri; oluşturma formunda dış başlıklar, hizalı seçenekler ve kaydırılabilir önizleme.
- Kapakta kurucu/yöneticiye özel değiştir ve dikey kadraj ayarı; sunucu izin kontrolü.
- Özel sohbet seçici ve dokunulabilir davet kartı; mevcut sohbet ID ve mesaj gizliliği korunur. Özel/onaylı topluluk davet kapısı korunur.
- Daha sıkı yorum listesi, avatar/isim, kısa zaman, yanıt ve tepki işlemleri; küçük ekran yazma alanı.
- Tek satırlı yorum işlemi, ikonlu sayaçlar, benzersiz kullanıcı sayımı açıklıkları korunur (paylaşım/görüntülenme tekil hesap olayları).
- Bölümlü yönetim paneli ve çalışan istatistik geçişleri; üyelerde arama ve rol filtresi; kurucu/yönetici/moderatör ayrımı, onaylı rol/susturma/çıkarma/engelleme ve işlem kaydı.
- Gönderi seçeneklerinde kaydet, şikâyet, öne çıkar, kaldır, yorum kapat/yavaşlat, üye onayı/susturma/çıkarma/engelleme ve görüş bildirme. Yetkiler sunucuda doğrulanır.
- Üyelere özel bildirim aboneliği, canlı sunucu sayaçları ve 30 güne kadar planlanmış gönderiler için ayrı sunucu bileşenleri.
- Fotoğraf önizlemesi yükleme boyunca korunur. Teknik hata yerine kısa mesaj; DNS hatasında aynı hosta ikinci native PUT atlanır ve mevcut Worker/multipart alternatifleri korunur.
- Lazy SliverList, sabit streamler, önbelleğe alınmış kurucu bilgisi/istatistik sorguları, daha az sayaç okuması; 24 MiB ham fotoğraf bellek bütçesi, eş zamanlı indirme birleştirme ve ekrana uygun çözümleme.

## 14 Ekim devam — ücretsiz test adayı ve dağıtım engeli

Son Build456 CI koşusunda Flutter analizleri, Flutter ekran testleri, Firestore emülatör testleri, Android imza/versiyon doğrulaması ve APK derleme geçti. İş akışı üretim Cloud Functions dağıtımında durdu: `cloudfunctions.googleapis.com` API'sini açmaya çalışan dağıtım kimliğine izin verilmedi. Bu, derleme veya kaynak kod test hatası değildir.

Kullanıcının ücretli hizmet istememe/kullanamama kısıtı nedeniyle CI düzenlendi: her push'ta aynı imzalı APK ve onay bekleyen kurallar test artefaktı olarak yayımlanır; Google Cloud Functions ve canlı Firestore kuralları **varsayılan olarak dağıtılmaz**. Yalnızca proje sahibinin gerekli izinleri ve maliyetleri ayrıca onaylayıp GitHub Actions üzerinde workflow_dispatch `deploy_backend=true` seçmesiyle ayrı üretim dağıtımı denenebilir.

**Dağıtılmayan backend bağımlılıkları:** zamanlanmış gönderilerin sunucuda yayımlanması, yeni bildirim abonelikleri, canlı sunucu sayaçları ve yeni moderasyon/yavaş mod Firestore izinleri, üretim kuralları ve Functions gerçekten kurulmadan doğrulanmış/etkin kabul edilemez. APK **cihaz testi adayıdır**, tamamlanmış canlı sürüm değildir. Mevcut sohbet kimlikleri, kimlik doğrulama ve eski işlevler korunur. Hiçbir üretim verisi silinmedi ve canlıya otomatik kurallar uygulanmadı.

## Doğrulama ve sınırlar
Yeni Dart parser/analiz kontrolleri ve sunucu planlama politika testleri geçmiştir. İlk CI'da yeni/önceki UI testleri ve Flutter analizi geçti; ilk ek Firestore testinde test bağlantısı referansı düzeltildi. İkinci CI'da tüm Firestore testleri geçti. Nihai baş için aynı kontroller, imza/sürüm doğrulaması ve sunucu kuralları read-back tamamlanmadan APK hazır sayılmaz.

Cihazda akıcılık, galeri/kapak sürükleme, yükleme bağlantı alternatifleri, gerçek iki hesap davet/yanıt/tepki teslimi ayrıca test edilecektir. Kasma ölçümü fiziksel cihazda henüz yapılmadı; yüzde hızlanma iddiası yok. DNS sunucusunun cihazdaki erişilebilirliği garanti edilmez.

Sunucu sayaçları/abonelik/planlama yeni servislerin başarılı kurulmasına bağlıdır. Hiçbir hesap/kayıt silinmez; eski uygulama özelliklerini kaldıran bir değişiklik yapılmaz. PR taslak; otomatik merge yok.
