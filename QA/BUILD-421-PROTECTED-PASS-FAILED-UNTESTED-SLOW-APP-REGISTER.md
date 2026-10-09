# NgelX — Build 421 Beş Cihaz Videosu: GEÇEN / GEÇMEYEN / TEST EDİLMEYEN — Work Koruma Listesi

**09.10.2026.** Kullanıcı talebi: kapaklı/kapaksız profil, hikâye, arkadaşlık/takip istekleri, tüm açık testleri tek listede sırala; geçenleri koru; uygulamanın çok yavaş olmasını ekle. Dayanak: `45335.mp4`, `45362.mp4`, `45371.mp4`, `45372.mp4`, `45375.mp4`, ilgili ekran görüntüleri ve ayrı `QA/BUILD-421-VIDEO-*.md` raporları. Sürüm: **Build 421 v1.0.196**, videolarda doğrulandı. Derleme CI: `37911442946` başarı; bu sonuç bütün cihaz senaryolarının geçtiği anlamına gelmez.

## A. GEÇEN: ÇALIŞAN KODU VE VERİYİ KORU
1. **Kapaklı profil:** avatar, kapak, sayaç, gönderi alanı ve temel fotoğraf gösterimi açılıyor.
2. **Kapaksız profil:** Adem'de mod seçimi kaydedildi; sahibin ortalanmış avatarı ve Umay'dan açılan ziyaretçi kapaksız görünüm **Video4'te geçti**. Kamera/özet/sosyal eylemler korunmalı.
3. **Dört profil sayacı** ve arkadaş listesi: test edilen hesapların sahip/ziyaretçi sayıları tutarlı; “Arkadaşsınız”, “Arkadaşın” ve bazı ortak arkadaş bilgileri çalışıyor.
4. **Normal takip:** Umay→Adem, Takip et→Takip ediyorsun, takipçi 1→2; diğer hesapta takipçi listesinde Umay gösteriliyor.
5. **Eski bekleyen istek eylemleri:** var olan bir arkadaşlık isteğinin reddi ve takip isteğinin kabulü sırasında bekleyen istek sayısının 3→2→1 değişimi görüldü. Bu, yeni gönderilmiş istek uçtan uca testinin yerine geçmez.
6. **Genel arama:** `uma`, `ade`, `adem`, `r` sorguları kişi sonuçları veriyor.
7. **Hesap değiştirme temel doğruluğu:** Umay↔Adem geçişi ve farklı profil bilgileri geliyor, fakat gecikme ciddi.
8. **Sohbet açma ve gönderici baloncukları**, profili özel mesaja paylaşma, gelen kutusundaki kayıtlar; alıcı teslimi ayrıca test edilmeli.
9. **Hikâye açma/oynatma** ve seçenekleri (yanıt **ayrı başarısız**).
10. **Engelli profile erişim sınırlaması** ve temel gizlilik ekranı.

**Değişmez koruma şartı:** Build 421 kaynak kodu/CI geçmişi ve önceki Build 395–420 regresyon testleri, Firestore güvenlik kuralları ve canlı hesap verileri korunacak. Yeni geliştirmelerde kapaklı/kapaksız kaydetme, sosyal kayıtlar, kullanıcı arama, hesap geçişi, sohbet ve medya oynatma **yeniden regresyon testine girecek**. “Koruma” bu QA sözleşmesidir; henüz ek otomatik test kodu yazıldığı anlamına gelmez.

## B. GEÇEMEYEN — GERÇEKTEN HATA VEREN / DÜZELTME GEREKTİREN
| Öncelik | Durum | Bulgular ve kabul koşulu |
|---|---|---|
| **P1** | **Hikâye yanıtı GÖNDERİLEMİYOR** | Video1 ve Build421 doğrulanmış Video3'te tekrar tekrar “Hikâye yanıtı gönderilemedi”. Gerçek Firebase hata kodu ve chat/izin adımı tespit edilip geçerli yanıtın karşı hesaba teslimi ispatlanmalı. Hikâye oynatma ve izin sınırları korunmalı. |
| **P1** | **UYGULAMA ÇOK YAVAŞ** | Video4 hesap değişiminden sonra **yaklaşık 8 sn siyah Akış/Radar yüklemesi**; profil, fotoğraf, sayılar, hikâye ve gezinmede tekrar eden spinner ve gecikmeler (Video1–4). Uygulama açılışı, hesap değişimi, Akış, Keşfet, profil, sohbet açılışı için cihazda süre ölçülmeli. Tekrar eden sorgular, sayfalama, görsel cache ve gereksiz rebuild analiz edilmeli; karanlık boş ekran yerine anlamlı durum, hata/yeniden dene eklenmeli. **Kullanıcı ayrıca “uygulama çok yavaş çalışıyor” diye işaretledi.** |
| **P2** | **Katılım tarihi kırpılıyor** | Kapaklı ve kapaksız **sahip profilinde** Eylül/Ekim 2026 tarihinde… diye kesiliyor (Video2/4). Konumdan ayrı tam okunabilir satır, taşma testleri; tarih hesabını bozmadan düzelt. |
| **P2** | **Aktivite/Gelen Kutusu tekrar navigasyonu** | Bildirimden ayrı tekrar Aktivite açılıyor, bildirimler iki kez listeleniyor (Video5). Tek Gelen Kutusu > Bildirimler / İstekler; bildirimden doğrudan gönderen profiline. |
| **P2 / YENİ TASARIM** | **İstekler kişi listesi ve profil Yanıtla yok** | Arkadaşlık **ve gizli takip** isteklerinde fotoğraf+ad+**gerçek görünürlüğü izinli N ortak arkadaş**+küçük avatarlar+Onayla/Sil; bildirime tıklayınca doğrudan profil; yalnızca `pending` ise Yanıtla→Kabul et/Reddet. Zaten arkadaşsa “Arkadaşsınız”, tamamlanmış normal takipte onay yok. Kullanıcı referansı `45385.jpg`/`45387.jpg`/`45388.jpg`/`45386.jpg`. |
| **P3** | **Kapak fotoğrafı değiştir kontrolü görseli örtüyor** | Video1'de büyük siyah alan. Kamera/cover edit işlemini koruyarak sadeleştir. |
| **P3** | **Belirsiz “Yeni bildirim” metinleri** | Video5'te bazı satırlarda kişi/olay bağlamı eksik. Güvenilir gönderici adı ve doğru olay metni korunarak gösterilsin. |

**Önemli:** İstekler kişi listesi, yeni profil Yanıtla davranışı ve Aktivite'nin kaldırılması mevcut Build 421'de henüz kodlanmış değildir; bunlar kullanıcı tarafından kabul edilmiş **sonraki Work tasarımıdır**. Geçmeyen listesinde “eksik/yeni iş” diye ayrıştırılmalı.

## C. HENÜZ TAM TEST EDİLMEYENLER — BAŞARISIZ DEĞİL, AÇIK
1. Yeni arkadaşlık isteği: A→B aynı anda gönderim/alım, kabul/ret, iki hesap listesi.
2. Gizli hesap takip isteği: A→B pending, onay/ret, gizlilik, karşı sayaç.
3. Yeni takip ve arkadaşlık bildiriminin **karşı cihaza** iletilmesi.
4. Mesajın **alıcı hesabında** görünmesi, okunmadı/okundu.
5. Hikâyenin tam paylaşım/bitiş saatleri ve kalan zamanın gerçek cihazda doğrulanması (hikâye oynatma geçti; yanıt geçmedi).
6. İstek geri çekme: iki tarafta durum temizlenmesi; internetsiz hatada yanlış başarı yazmaması.
7. Avatar değiştirildikten sonra arkadaş, arama, sohbet ve ziyaretçi profilinde yenilenmesi.
8. Fotoğraf/video/yazı gönderisi: yayın, Akış sıralama, beğeni/yorum/kaydet ve profil Kaydedilenler.
9. Grup oluşturma, katılma, grup mesajı/bildirim.
10. Uygulamanın tamamen kapatılıp yeniden açılması sonrası oturum, sohbet ve profil verilerinin korunması.

## D. YENİ WORK SIRASI / KABUL KAPISI
1. **P1** Hikâye yanıtı: gerçek Firebase hatasını izole et, emülatör ve iki gerçek hesapla düzelt.
2. **P1** Performans: ölçümler, 8 sn hesap geçişi, siyah ekran, gereksiz istekler/caching/pagination; somut önce/sonra süre.
3. **P2** Gelen Kutusu & İstekler için ortak kişi listesi, gerçek mutual count/avatarlar, direkt profil Yanıtla ve bildirim doğru yönlendirme; güvenlik korunur.
4. **P2** Katılım tarihi tam okunur, kapaklı/kapaksız modlar için.
5. **P3** Kapak düzenle aksiyonu ve animasyon/geçici yükleme iyileştirmesi.
6. **Uçtan uca QA**: Açık C senaryolarını gerçek iki hesapta tekrar et; çalışan A maddelerini tekrar doğrula.

**Not:** Bu belge yalnızca Work kapsamı ve test koruma kaydıdır. Üretim kaynak koduna, canlı Firebase verisine ve APK'ya bu adımda değişiklik yapılmadı.
