# Build454 topluluk testi — 47215.mp4
Tarih: 14 Ekim 2026, Europe/Istanbul. Kayıt: 148.12 saniye, 1080x2392.
Kullanıcı topluluk tasarımı, yorum yapma, tepkiler ve sayaçların tamamının incelenmesini istedi. Bu aşamada yalnız kayıt alındı; yeni uygulama değişikliği yapılmadı.

## Doğrudan gözlem
1. Yaklaşık 0–4 sn: topluluk listesi kısa yükleme sonrasında geliyor. “Topluluk ara” yazısı önceki beyaz üzerine beyaz soruna göre okunabilir.
2. PANELCİLER LİVE kapağı ve topluluk avatarı görünür. Yeni oluşturulan Süleyman topluluğunda da seçilmiş kapak ve avatar görünür. “Tüm görseller yok” denemez; tasarım yeterliliği ayrı açık konu.
3. Topluluk başlığı, kurucu/üye bilgileri, sekmeler, paylaşım düğmesi, gönderi tarihi ve etkileşim yazıları çok küçük/sıkışık. Fotoğraflar büyük alan kaplarken metin/eylem hiyerarşisi zayıf. Sağdaki sekme alanı dar. Beyaz tema ve mevcut yapı korunarak daha okunur düzen gerekli.
4. Yaklaşık 10–22 sn: kalp mor dolu duruma geçiyor. Yorumlar panelinde DİLEK Akçay tarafından kısa yorum gönderiliyor; kapatıp yeniden açınca aynı yorum görünür. Bu kayıtta yorum gönderme bütünüyle bozuk değil.
5. Gönderi kartında beğeni sayısı, yorum sayısı, paylaşım sayısı ve görüntülenme sayısı görünmüyor; yalnız “Beğen / Yorum yap / Paylaş” var. Sayıların saklama/güncellenme doğruluğu ekrandan doğrulanamıyor. Gerçek veriye bağlı sayaçların gösterimi ve anlık artış/azalış testi gerekli.
6. Yorum paneli tek küçük isim/metin satırı ve geniş boş alan gösteriyor. Yorum avatarı/tarih, yanıt, yorum beğeni/tepki ve ilgili sayaçları görünmüyor. Kaydırma ve klavye açılınca panel tam ekran gibi büyüyor; giriş tek alt çizgili alan ve küçük gönder oku. Daha belirgin yorum/yanıt düzeni isteniyor.
7. Görünen tepki eylemi yalnız kalp beğenisi. Diğer tepki seçenekleri ve tepki dağılımı kayıtla görünür değil; uzun basma denenmediği için mevcut olmadıkları kesin söylenemez.
8. Yaklaşık 28–30 sn: gönderi altındaki Paylaş, Android “Metin paylaşılıyor” panelini açıyor. Paylaşılan metin “NgelX topluluk: <topluluk kimliği>”; gönderiye özgü içerik/bağlantı görünmüyor. Gönderi paylaşımının hedefi topluluk paylaşımıyla karışmış olabilir; kök neden incelenmeli.
9. Mevcut topluluk Videolar sekmesinde “Henüz gönderi yok”; Fotoğraflar sekmesinde fotoğraf görünüyor. Yeni toplulukta boş sekmeler normal olabilir, tek başına veri kaybı kanıtı değil.
10. Yaklaşık 50–108 sn: topluluk oluşturma formunda avatar/kapak seçimi, açıklama/kurallar, önizleme ve oluşturma tamamlanıyor. Önizleme koyu diyalog ve yalnız metin; seçilen görsellerin önizlemesi yok. Oluşturma boyunca form uzun süre “Oluşturuluyor…” ve devre dışı; belirgin aşama bilgisi yok. Yaklaşık 95–108 sn civarındaki bekleme için gerçek süre/log ölçümü gerekli.
11. Topluluk yönetiminde üyelik istekleri, bekleyen gönderiler, şikayetler, istatistikler, üyeler, ayarlar küçük düğmeler halinde; bu kayıtta yalnız boş bekleyen kayıt ekranı görüldü. Diğer işlevler doğrulanmadı.
12. Yaklaşık 120–148 sn: video seçimi sonrası önce önizleme yükleme göstergesi, ardından dikey video önizlemesi, oynatma düğmesi ve süre etiketi görünür. İlk video 46643.mp4 sonra başka video 45869.mp4 seçiliyor. Önizleme tümden eksik değil.
13. Kayıt Paylaş düğmesi hâlâ açıkken sona eriyor. Bu kayıtta yükleme başladığı veya tamamlandığı doğrulanmıyor; yüzde/MB yükleme sayacı bu yüzden başarısız diye işaretlenemez. Önceki47200 yükleme sorunu gerçek paylaşım testiyle yeniden doğrulanmalı.
14. Video önizlemesinin yatay kartında dikey medya dar kalıyor ve geniş boşluk var; paylaşım formu/medya sunumu tasarım kontrolüne dahil.

## Toplu düzeltme kabulü
- İki hesapla beğen/beğeniyi geri al, yorum ekle/sil/yanıtla; sayıları iki cihazda ve yeniden açılışta karşılaştır.
- Tepki seçimi varsa açılışını ve dağılımını kontrol et; sayıları varsayımsal üretme.
- Gönderi paylaşımı gönderiye yönlendirmeli; topluluk paylaşımı ayrı hedef kullanmalı.
- Video önizleme süresi/oynatma, yükleme yüzdesi/MB, kayıt aşaması, hata/tekrar deneme ve tamamlandıktan sonra doğru sekmede görünme ayrıca test edilmeli.
- Topluluk başlık, görseller, sekmeler, gönderi kartı ve yorum alanında okunur font/boşluk/kontrast; beyaz tema ve mevcut mimari korunmalı.
