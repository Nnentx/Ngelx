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

## Ekran örneği 45388.jpg / 45386.jpg — bildirimden direkt profil, “Yanıtla” durumu

Kullanıcının istediği tam akış:

1. **Gelen Kutusu > Tümü/Bildirimler** satırı: **“Umay Umay sana arkadaşlık isteği gönderdi”**. Satıra veya Umay'ın fotoğrafına basılınca **yeni Aktivite ekranı açma**; doğrudan **Umay'ın ziyaretçi profiline git**. Bildirim içindeki `fromUid` / güvenilir gönderen UID'sini kullan, ad üzerinden profil tahmini yapma.
2. Profilde gerçek **gelen arkadaşlık isteği durumu `pending` ise**, ekrandaki arkadaşlık eyleminin yerinde **“Yanıtla”** düğmesi olsun. Basınca **“Kabul et” / “Reddet”** alt menüsü/diyaloğu gösterilsin. Kullanıcının ayrıca Aktivite'ye dönmesi gerekmesin.
3. **İstek zaten kabul edilmiş ve kişiler arkadaşsa**, mevcut **“Arkadaşsınız”** etiketi ve arkadaşlığı yönetme davranışı kalsın; **tekrar “Kabul et” sunulmasın**. Kullanıcının örneğindeki ekran “Arkadaşsınız” gösteriyor; bu durum yeniden onay gerektiren istek değildir.
4. **İstek reddedilmiş, geri çekilmiş veya silinmişse**, profil artık “Yanıtla” göstermemeli. Canlı Firestore `friend_requests`/istek belgesi durumu ve `users.friends` ile tutarlılık kontrol edilmeli; yalnızca eski bildirim metnine göre buton çizilmemeli.
5. **“Umay seni takip etmeye başladı”** satırı da Umay profiline gitmeli. Bu *tamamlanmış takip* bildirimi için “Yanıtla / Kabul et” gösterme; kullanıcı profilden isteğe bağlı karşı takip edebilir.
6. **Gerçek gizli-hesap “takip isteği”** bildirimi ayrı olaydır. Gelen `follow_request` hâlâ bekliyorsa profilde **“Yanıtla → Kabul et / Reddet”** kullanılabilir.
7. Kabul/ret sunucu işlemi onaylanınca Gelen Kutusu > İstekler sayacı ve iki taraftaki ilgili profil durumları **canlı güncellensin**. Hata veya bekleme varken işlemin tamamlandığı yazılmasın.
8. **Doğrudan profil açılması ve bekleyen istek düğmesi**, profil gizliliği, engelleme, oturum sahipliği ve Firestore erişim kurallarını bypass etmemeli.

**Görüntü referansı:** Kullanıcının `45388.jpg` profil ekranında “Arkadaşsınız” düğmesi; `45386.jpg` Gelen Kutusu ekranında Umay'ın takip ve arkadaşlık bildirimi. Yalnızca istek gerçekten beklemedeyken o düğmenin yerini “Yanıtla” alması isteniyor.

**QA:** Yeni, henüz arkadaş olmayan hesap A → B arkadaşlık isteği gönder; B'nin Gelen Kutusu bildirimine bas → A profili → Yanıtla → Kabul et veya Reddet; sonuç her iki profilde ve gelen kutusunda güncellenmeli. Zaten arkadaş olan Umay/Adem çiftinde “Arkadaşsınız” korunmalı.

## EK TALEP — Takip istekleri de aynı Messenger tipi model olsun

**Kullanıcı talebi:** “Takip içinde öyle model istiyorum.”

- **Gelen Kutusu > İstekler** bölümünde ayrı **Takip istekleri** alt başlığı; arkadaşlık istekleriyle aynı satır düzeni: solda yuvarlak fotoğraf, ad, isteğin zamanı, gerçekten varsa görünürlüğü izinli **N ortak arkadaş** ve 2–3 küçük profil fotoğrafı. Sabit sayı veya sahte kişi kullanılmaz.
- **Gizli hesaba gelen, hâlâ bekleyen takip isteği** satırında **Onayla / Sil** düğmeleri; “Sil” yalnız isteği reddeder, hesabı/mesajı silmez. Satıra dokununca direkt gönderen profiline gidilir, burada **Yanıtla → Kabul et / Reddet** seçenekleri gösterilir.
- **Herkese açık hesapta “X seni takip etmeye başladı”** olayı *takip isteği değildir*; **Bildirimler** sekmesinde görünür ve satıra basınca kişinin profili açılır. **Onayla/Sil veya Yanıtla** gösterilmez. İstenirse karşı takip normal “Takip et” ile yapılabilir.
- **Takip isteği kabul edilince** iki hesapta gerçek takip/takipçi sayaçları ve düğmeleri doğru güncellenir; listeden bekleyen istek kaldırılır. **Reddedilince** takip ilişkisi oluşmaz; bekleyen kayıt/sayaç düşer.
- Aynı kişiden birden fazla bildirim, eski isteğin kabul edilmiş/reddedilmiş/geri çekilmiş hâli veya gizlilik değişikliği varsa **gerçek güncel Firestore durumuna göre** eylem gösterilir. Okunmamış durum ve bildirim geçmişi silinmez.
- **Bildirimden veya istek satırından tekrar ayrı Aktivite ekranına yönlendirme yapılmaz.** Profil gizliliği, karşılıklı engel, veri okuma yetkileri ve mevcut mesaj/grup yolları korunur.
- Test: gizli hesap A'ya B'den takip isteği → A'nın Gelen Kutusu/İstekler bölümünde B fotoğrafı, gerçek varsa ortak arkadaş metni, Onayla/Sil → satıra basınca B profili ve Yanıtla → kabul/ret → hem A hem B'de bekleyen/takip durumları tutarlı. Açık hesaba doğrudan takip ayrıca test edilir.

**Durum:** Work tasarım notudur; henüz kodlama veya canlı hesaplara değişiklik uygulanmadı.

## KALDIRMA KARARI — ayrı Aktivite sayfasına son ver

**09.10.2026 kesin onay:** Kullanıcı gereksiz tekrar eden **Aktivite ekranının kaldırılmasını** istedi.

- Gelen Kutusu → **Bildirimler** ve **İstekler**, aktivitelerin tek UI kaynağı olacak. **Aktivite adındaki ikinci/tekrar ekran uygulama navigasyonundan çıkarılacak.**
- Önceden Aktivite'ye götüren bildirim zili, menü ve eski bağlantılar **Gelen Kutusu → ilgili sekmeye** yönlenecek.
- Bildirim/istek satırına basınca doğrudan kişinin profiline gidilecek; gönderen UID'sine dayalı rota kullanılacak.
- Sadece **bekleyen** gizli takip veya arkadaşlık isteği profilde **Yanıtla → Kabul et / Reddet** açacak; tamamlanmış takip ve “Arkadaşsınız” durumu olduğu gibi korunacak.
- **Sakın bildirim veya isteği veritabanından silme:** Aktivite sayfasının kaldırılması sadece fazladan ekran/navigasyon kaldırmadır. Okundu, tarih, grup bildirimleri, sayaçlar ve mevcut sohbet işlevleri korunur.
- Yalnız Work notuna eklendi; kod henüz değiştirilmedi.
