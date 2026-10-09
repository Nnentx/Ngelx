# NgelX Build 422 — Toplu Work kodlama, koruma ve cihaz kabul sözleşmesi

**Tarih:** 09.10.2026. **Temel:** Build 421 v1.0.196 / 5 telefon videosu / iki ekran tasarım referansı. **Hedef:** v1.0.197+422.

## Korumaya alınan ve yeniden test edilecek başarılı altyapı

- Kapaklı/kapaksız profil: Adem'de kaydedilmiş kapaksız modun Umay'dan doğru görüntülenmesi, avatar, istatistik, dört aksiyon, tanıtım videosu ve gönderiler.
- Normal takip: Takip et → Takip ediyorsun; her iki hesapta takipçi/takip sayacı; gizli hesap isteği ile normal takibin ayrımı.
- Var olan arkadaşların “Arkadaşsınız” durumu; arkadaşlar listesi, gerçek ortak arkadaş bilgisi, karşılıklı sayı tutarlılığı.
- Genel arama `uma`, `ade`, `adem` sorguları; engellenmiş profil kısıtlaması.
- Umay↔Adem hesap değiştirme kimlik doğruluğu ve farklı avatarları; önceden kaydedilmiş hesap şifrelerinin güvenli saklanması.
- Gelen Kutusu'nda özel sohbet/gönderici mesaj baloncukları, grup konuşmaları, profili DM'ye gönderme ve eski arkadaş/takip isteklerinin kabul/ret verileri.
- Hikâye açma/oynatma, yayın/bitiş zamanlarının kaydı ve 24 saat yaşam süresi.
- Bildirim kayıtları, okunma bilgisi, Firestore güvenlik kuralları, bloklama/gizlilik.
- Build 395–421 regresyon testleri; veritabanı migrasyonu veya erişim kuralı genişletmesi **yok**.

## Kodlanan Build 422 kaynak değişiklikleri (otomatik test sonucu ayrıca takip edilir)

### 1. Hikâye yanıtı P1
- Var olmayan deterministik sohbet belgesinde izinsiz `.get()` kullanımı yerine, gönderenin üyesi olduğu mevcut sohbetler üzerinden bulma.
- Mevcut sohbetin deterministik olmayan ID'sini de kullanma; yeni sohbet için profil > Mesaj yolundaki gizlilik izinleri ve collision-safe oluşturma.
- Mesaj ve son sohbet bilgisini batch ile gönderme; bildirim hatasını başarılı mesajın başarısızlığına dönüştürmeme.
- Kullanıcıya safha bazlı hata ve gizlilik uyarısı; Firebase hata kodu debug kaydı.
- **Telefon zorunlu:** A/B arasında gerçek hikâye yanıtı gönderim/teslim; gizli mesaj izni ve engel senaryoları; kullanıcının üyesi olmadığı sohbet görünmemeli.

### 2. Tek Gelen Kutusu / Messenger tipi istekler
- Bildirim satırı gönderen profile gitmeli; ayrı Aktivite sayfasına zorlamamalı.
- Gelen arkadaşlık ve gizli takip istekleri satırlarında gerçek kişi avatarı/adı/zamanı, gizliliğe uygun **N ortak arkadaş** ve küçük avatarlar, **Onayla / Sil**.
- Profilden gerçek `pending` duruma göre **Yanıtla → Kabul et / Reddet**; zaten arkadaşsa **Arkadaşsınız** değişmez; açık hesaba gerçekleşmiş takip için onay gerekmez.
- Takip/arkadaşlık kabul, ret ve sayaç Firestore kayıtları güvenli batch ile; istek listesi canlı güncellenmeli.
- Eski bağımsız Aktivite ekranı kullanıcı gezinmesinden çıkarılır; kodu tam fiziksel silmeden önce eski bağlantıların rotası yeni Bildirimler sekmesine devredilir. Bildirim **verileri** kesinlikle silinmez.

### 3. Yavaşlık P1
- Akış ve Gelen Kutusu içinde aynı Firestore sorgusuna sürekli yeni `.snapshots()` akışı oluşturmayı önleyen abonelik kimliği önbelleği.
- Akış yüklenirken anlamlı bir açıklama; önceki blok/arkadaş gizleme filtresini veri gelmeden kaldırma **yok**.
- **Cihaz performans kabulü:** Umay→Adem hesap geçişi, ilk Akış açılışı, sohbet, kullanıcı arama ve profil açılışı süreleri ölçülecek. Videoda **~8 saniyelik** siyah yükleme vardı. Gerçek ölçüm olmadan “hız düzeldi” denmez.

### 4. Katılım tarihi ve görsel hatalar
- Sahibin kapaklı/kapaksız profilinde konum ve katılım tarihi ayrı, kırılabilir satırlar olacak; ay/yıl metni kesilmeyecek.
- Kapak editörde Build 414'te küçültülen kamera düğmesi ve mevcut kapak/kapaksız seçimi korunur.
- Sayaçların ilk veriyi gösterme süresi ve görüntü/ses oynatımı cihazda gözlemlenir.

## Otomatik koruma ve manuel kabul testleri

1. Build 395–421 eski yamalar/kontroller, Build 422 kaynak koruma, Firebase emulator ve `flutter analyze` başarı.
2. Aynı uygulama kimliği/imza ile imzalı release APK üretimi.
3. Kapaklı/kapaksız sahibi ve ziyaretçisi; kamera, fotoğraf, sosyal aksiyonlar.
4. Umay → arkadaş olmayan yeni hesaba istek gönder → alıcı Gelen Kutusu/İstekler (Onayla/Sil + gerçek ortaklar) → profilden Yanıtla → Kabul/Ret → her iki hesapta doğrulama.
5. Gizli takip isteği gönder → Yanıtla/Kabul/Ret; açık profilde doğrudan takip ayrı doğrulanır.
6. Bildirime tıkla → doğrudan profil; eski Aktivite döngüsü tekrar etmemeli; eski bildirimler korunmalı.
7. Gerçek hikâye yanıtı/emoji tepkisi gönder → karşı hesap Gelen Kutusu; engel ve mesaj izni.
8. Yavaşlık ölçümleri önce/sonra; siyah ekranda kalıcı kilitlenme olmaması.
9. Mesaj, grup, genel arama, istek iptal, cihaz değişimi, kapak kaydı, hikâye zamanı ve avatar değiştirme regresyonları.

**Durum:** Kod dalında çalışılıyor; otomatik test/telefon sonucu olmadan tamamlandı demiyoruz. Kullanıcının çalışan Build 421 uygulamasını silmesini veya üretim verilerini sıfırlamasını gerektirmez.
