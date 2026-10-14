# Topluluk paylaşımı ve tasarımı — 47200.mp4

14 Ekim 2026, 10:49 (Europe/Istanbul). Video yaklaşık 85 saniye. Kullanıcı topluluk görsellerinin/tasarımının eksik olduğunu, video paylaşımının uzun beklediğini ve yükleme sayacı olmadığını bildiriyor.

Videoda doğrulananlar:
- PANELCİLER LİVE topluluğunda kapak ve avatar var. SENİNLEYİM topluluğunda genel grup simgesi görülüyor; bu kayıt tüm topluluk görsellerinin yüklenmediğini kanıtlamaz.
- Topluluk gönderi alanında başta ve sonda “Gönderi akışı henüz hazır değil. Biraz sonra yeniden dene.” ve “Tekrar dene” mesajı var; gönderiler/medya görüntülenemiyor.
- Galeriden 47037.mp4 seçiliyor. Paylaşım ekranında yalnızca dosya adı ve kaldırma X'i var; video küçük resmi, oynatılabilir önizleme ve süre görünmüyor.
- Yaklaşık 36. saniye örneğinden 72. saniyeye kadar “Yükleniyor...” yazısı sürüyor. Yüzde, ilerleme çubuğu, yüklenen boyut veya kalan süre görünmüyor; işlemin hangi aşamada olduğu anlaşılmıyor.
- Videonun son bölümünde topluluk ekranına dönülüp “Gönderin paylaşıldı.” bildirimi görünüyor; ancak gönderi akışı hâlâ açılamıyor. Bu nedenle hiçbir zaman kaydedilmedi diye kesinleştirilemez; kullanıcı açısından sonuç görünmediğinden paylaşım doğrulanamıyor.
- Paylaşım sayfası büyük boş metin alanı, küçük soluk medya düğmeleri ve dosya adından oluşuyor; mevcut topluluk görünümü ve yönetim sekmeleri de kullanıcının beklentisine göre eksik.

Sonraki toplu paket kabul ölçütleri:
1. Topluluk gönderi akışını gerçek backend hatasına göre düzelt; indeks/izin/ağ hatasını ayır. Önceden bilinen posts COLLECTION status ASC / createdAt DESC indeksi yetki engeli olası ilişkili neden, bu videodan kesin teşhis değildir.
2. Medya yüklemede gerçek yüzde/ilerleme, aşama bilgisi (hazırlanıyor/yükleniyor/paylaşılıyor) ve mümkünse yüklenen/toplam boyut sun. Sahte yüzde veya tahmini süreyi kesin veri gibi gösterme.
3. Uzun bekleme/hata durumunda anlaşılır hata, iptal ve güvenli yeniden deneme; aynı gönderinin iki kez oluşmasını engelle. Başarı mesajından sonra gönderi görünürlüğünü doğrula.
4. Seçilen fotoğraf/video için net küçük resim/önizleme ve video süresi göster; kaldır/değiştir eylemleri okunaklı olsun.
5. Topluluk avatar/kapak, medya kartları, paylaşım ve yönetim alanlarının tasarımını beyaz tema ve mevcut yapıyı koruyarak tamamla; eksik görsel ile hiç görsel seçilmemiş durumunu ayır.

Durum: sonraki toplu düzeltme için not edildi. Bu turda kod veya APK değiştirilmedi.
