# NgelX Build 422 — Gelen Kutusu, istekler ve profil “Yanıtla” telefonu (45411.mp4)

**Tarih:** 09.10.2026; **yaklaşık 59,5 saniye**. Alperen ve Umay hesapları üzerinden sosyal istek test akışı. Build 422'nin yüklenmiş olduğu önceki Ayarlar ekranıyla doğrulandı; bu video içinde sürüm menüsü yeniden açılmadı.
**Kural:** Video gözlemleri dışında kök neden uydurma; kullanıcı e-postalarını rapora aktarma; mevcut ilişki ve bildirim kayıtlarını silme.

## P1 — Kanıtlanan cihaz sorunları

| Yaklaşık zaman | Sorun | Gerçek gözlem / kabul şartı |
| --- | --- | --- |
| **00:33–00:36 ve 00:53–00:55** | **“Yanıtla” menüsü boş beyaz alt panel olarak açılıyor.** | Alperen'in ziyaretçi profilindeki mor **Yanıtla** düğmesine basılınca alttan neredeyse tamamen **boş beyaz sheet** geliyor; “Kabul et” ve “Reddet” satırları okunmuyor. Sol altta mor tik benzeri simge var. Tekrarlanan denemede benzer davranış. Menü yazı/eylem alanları erişilebilir ve görünür olmalı; mevcut friends / follow estado yanlış güncellenmemeli. Bu video herhangi bir isteğin kabul veya reddini doğrulamaz. |
| **00:47–00:50** | **Gelen Kutusu → İstekler sosyal istekleri göstermiyor.** | **Tümü** ve **Bildirimler** bölümlerinde “Alperen Yarbay sana arkadaşlık isteği gönderdi” ve “seni takip etmek istiyor” görünürken **İstekler** sekmesinde yalnız **Mesaj istekleri** kartı ve onun “Yeni mesaj isteği yok” ekranı çıkıyor. Onayla/Sil satırları, kişi fotoğrafı ve ortak arkadaş bilgisi görünmüyor. Filtre/istek belge okuma/hatalı boş durum ayrıştırılmalı. |
| **00:19–00:24** | **Hesap değiştirince Akış/Radar beklemesi.** | Ekran yaklaşık **3–4 saniye** koyu/siyah ve “Akış hazırlanıyor...” yükleme göstergesinde; sonunda açılıyor. Kalıcı çökme yok ama performans sorunu önceki videodaki ~8 saniyelik yüklemeye eklenmeli; önce/sonra süreleri ölçülmeli. |

## Bu kayıtta çalıştığı görülenler ve korunması gerekenler

1. **00:02–00:09:** Umay profili genel aramadan bulunuyor, profil açılıyor. Özel/gizli profile ilişkin “Bu profil sınırlı” alanı görünüyor.
2. **00:04–00:08:** Başka hesabın özel profiline takip isteği gönderildiği ve arkadaşlık isteği gönderildiği için ayrı ayrı yeşil başarı mesajları görülüyor; düğmeler **Takip isteği bekliyor** ve **Arkadaşlık isteği bekliyor** biçimine dönüyor. **Karşı alıcının kabulü bu videoda gerçekleşmiyor.**
3. **00:14–00:20:** Hesap değiştirme ekranında birden fazla kayıtlı hesap listeleniyor, seçilen hesaba geçiliyor; şifre bilgileri rapora alınmıyor.
4. **00:28–00:32:** Gelen Kutusu → Tümü içinde Alperen'den gelen iki istek bildirimi ile sohbet/grup bildirimleri gösteriliyor. İstek bildirimlerinin üzerine basılabiliyor.
5. **00:32–00:33, 00:51–00:53:** İstek bildirimine basıldığında **ayrı Aktivite sayfası açılmadan**, doğrudan Alperen'in ziyaretçi profili açılıyor; “Yanıtla” düğmesi mevcut. Bu yeni yönlendirme **geçti**; alt panel ise yukarıdaki gibi başarısız.
6. **00:40–00:47:** Normal özel sohbet açılıyor, mesaj baloncukları ve yazma kutusu çalışıyor; test mesajlarını karşı hesabın gördüğü kesin olarak kanıtlanmıyor.
7. **00:51–00:54:** Bildirimler sekmesinde hem arkadaşlık/takip istekleri hem geçmiş olaylar görünüyor. Kullanıcı profiline gidip geri dönebiliyor; gereksiz Aktivite döngüsü bu kayıtta tekrarlanmıyor.
8. **00:56–00:59:** Gruplar sekmesi açılıyor; boş grup durumu gösteriliyor. Boş liste tek başına grup altyapı hatası kanıtlamaz.
9. **~00:33:** Alperen'in profilindeki “Takip ediyorsun”, Mesaj ve dört sayaç görünür. Fotoğraf yerine harf avatar mevcut (fotoğraf yoksa beklenen).

## Ürün gereksinimi — bu videodaki gerçek kabul koşulları
- **İstekler** sekmesinde bekleyen gelen **arkadaşlık ve gizli hesap takip istekleri**, Messenger-benzeri fotoğraflı kişi satırları olarak doğrudan yer almalı. **Onayla / Sil** gerçek istek kaydını değiştirmeli; varsa gerçek ve görünürlüğü izinli ortak arkadaş sayısı/mini avatarlar.
- Aynı istek bildirimi → gönderen profili → **Yanıtla** → açıkça görünen **Kabul et / Reddet**; bekleyen istek yoksa Yanıtla gösterilmemeli.
- “X seni takip etmeye başladı” tamamlanmış takip bildirimidir, ayrıca onay gerektirmez.
- Kabul/ret sonrası iki tarafta ilişki ve sayaçlar, Gelen Kutusu/İstekler filtreleri ve geçmiş bildirimler tutarlı kalmalı.
- Görsel alt panelin beyaz modda beyaz metin üretmediği, yerleşimi aşmadığı ve istem dışı sistem overlay oluşturmadığı kontrol edilmeli.
- Hesap değişimi, Akış ilk yükleme, profil yükleme başlangıç/bitiriş süreleri gerçek cihazda ölçülmeli; sadece spinner değiştirmek performans çözümü sayılmamalı.

## Hikâye ile çapraz kontrol

Bu `45411.mp4` videosunda **hikâye yanıtı veya hikâye saatleri ayrıca test edilmiyor**; önceki `45407.mp4` videosundaki tekrar eden **“Hikâye yanıtı gönderilemedi.”** sorunu AÇIK kalıyor. Bu video hikâye hatasının düzeldiğini kanıtlamaz.

**Durum:** Sadece QA raporu oluşturuldu; uygulama kaynak kodu/Firebase veri ve kuralları bu raporla değiştirilmedi.