# NgelX — Gelen Kutusu > İstekler için istenen tasarım ve ortak arkadaşlar

**Tarih:** 09.10.2026. **Kullanıcı görselleri:** 45385.jpg (Facebook arkadaşlık istekleri referansı) ve 45387.jpg (NgelX Gelen Kutusu > İstekler).  
**Kullanıcı ek isteği:** “Örneğin Ayaz Atabey ortak arkadaş yazmış o modelde not et.”  
**Durum:** Yalnızca QA/Work tasarım notudur; henüz uygulama kodu, canlı Firebase veya kullanıcı verisi değiştirilmedi.

## Tasarım hedefi
NgelX'in mevcut **Gelen Kutusu > İstekler** sekmesinde yer alan iki büyük “Takip ve arkadaşlık istekleri” / “Mesaj istekleri” yönlendirme kartı yerine, bekleyen arkadaşlık ve takip isteklerini Facebook/Messenger örneğindeki gibi **aynı sayfada kişi satırları** olarak göster. NgelX'in özgün beyaz zemin, mor/mavi buton ve alt navigasyon kimliği korunacak; dış uygulamanın marka ve ekranı birebir kopyalanmayacak.

## Arkadaşlık istekleri — satır bileşenleri
1. Solda yuvarlak profil fotoğrafı; sağda gönderenin görünür adı.
2. **Adın hemen altında “N ortak arkadaş”** metni: örnek resimdeki **“Ayaz Atabey · 127 ortak arkadaş”** modeli. Sayının yanına mümkünse **en fazla 2–3 minik ortak arkadaş avatarı** ve kalanların sayısı yerleşsin.
3. Ortak arkadaş sayısı **gerçek iki hesabın ortak, görünür ve erişime izinli arkadaşlarının kesişiminden** hesaplanmalı. **127** sabit veya uydurulmuş veri değildir, yalnızca referans görseldeki örnektir. Ortak arkadaş yoksa “0 ortak arkadaş” yazısını gereksiz yere göstermemek; gizlilik/engelleme nedeniyle açıklanmaması gereken ad/avatarları asla ifşa etmemek.
4. Altında iki yatay düğme: **Onayla** (NgelX mor-mavi ton) ve **Sil** (gri, gerçekte isteği reddet/geri çevir — hiçbir kullanıcı hesabını veya diğer mesajları silme).
5. Ad veya avatara dokununca doğrudan o kişinin profili açılmalı; bekleyen istek varsa profilde de Kabul / Reddet eylemleri bulunabilir.
6. Başarılı onaydan sonra “İstek kabul edildi” metni; başarılı ret sonrası bekleyen listeden düşme. Beklemede, hata ve ağ kesintisi için durum göster; yazma işlemi başarıyla tamamlanmadan olumlu durum gösterme.
7. Üstte **Arkadaşlık istekleri** bölüm başlığı ve gerektiğinde **Tümünü gör**. Hiç istek yoksa açık boş durum.

## Takip ve mesaj istekleri
- Arkadaşlık listesinin ardından, **gerçek onay isteyen özel hesap takip istekleri** aynı fotoğraf + isim + zaman + varsa görünür ortak arkadaş bilgisi + Onayla / Sil modeliyle sunulabilir.
- **“X seni takip etmeye başladı”** tamamlanmış takiptir, onay gerektiren istek değildir; **Bildirimler** sekmesinde kalır, seçilince takip edenin profili açılır.
- **Mesaj istekleri** ayrı bölümde kalır; mesaj izinleri, istek onayı ve sohbet akışı korunur.

## Aktivite ile çakışmayı kaldır
Mevcut **Tümü / Mesajlar / Gruplar / Bildirimler / İstekler** üst sekmeleri yerinde kalır. Bildirim/istek seçildiğinde aynı Aktivite sayfasına tekrar tekrar yönlendirme yapılmaz. Yeni tek Gelen Kutusu liste akışından doğrudan gönderici profiline veya mevcut güvenli onay/ret eylemine gidilir. Eski aktivite bağlantıları çökmeden doğru bölüme yönlenmeli.

## QA sözleşmesi
- Umay'dan başka bir henüz arkadaş olmayan hesaba istek gönder → Gelen Kutusu > İstekler'de Umay avatarı, adı, **gerçek ortak arkadaş sayısı ve varsa minik resimleri**, Onayla / Sil.
- Kabul → iki hesapta arkadaşlık durumu ve sayaçlar tutarlı; aynı isteği ikinci kez kabul edememe.
- Sil/Reddet → iki hesap için eski bekleyen istek kapanır; arkadaşlık yanlışlıkla oluşmaz.
- Ortak arkadaş gizli/engelli → adı/fotoğrafı gösterilmez; toplam izinli kullanıcıları yansıtır.
- Onay gerektirmeyen takip bildirimi → profil açılır, gereksiz onay gösterilmez.
- Diğer Bildirimler/Mesajlar/Gruplar ekranları ve önceki başarılı Build421 özellikleri korunur.

**Not:** Ayaz Atabey ve “127 ortak arkadaş” yalnızca kullanıcı tarafından paylaşılan üçüncü taraf arayüzünün görsel örneğidir; NgelX verisi değildir. 
