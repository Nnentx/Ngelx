# Build454 — yükleme ve durum bildirimi tasarımı
Tarih:14 Ekim2026. Kanıt47219.mp4,45.70s.
Kullanıcının isteği: video yükleniyor/MB alanı küçültülsün, renkli olsun; fotoğraf/video yüklendi gibi uyarılar ve alttaki durum yazıları renkli, büyük olmayan bir tasarım kullansın.

## Kabul edilen tasarım yönü
- Yükleme kartının yüksekliği, iç boşlukları ve kapladığı alan azaltılmalı; sayaç metni okunamayacak kadar küçültülmemeli.
- İnce renkli ilerleme çubuğu; kompakt yüzde ve gönderilen/toplam MB satırı korunmalı.
- Fotoğraf/video hazırlanıyor, yükleniyor, kaydediliyor ve tamamlandı durumları kısa, küçük ve okunur renkli bildirimler olmalı.
- Genel “Gönderin paylaşıldı” yerine uygun yerde medya türüne göre “Fotoğraf paylaşıldı” / “Video paylaşıldı” gibi açık metin tercih edilmeli; dosya aktarımı ile paylaşım kaydı tamamlanması ayrılmalı.
- Başarı, işlem ve hata durumları ikon/metinle de anlaşılmalı; yalnız renk farkına bağlı kalmamalı.
- Alt bildirimler büyük kutular halinde ekran kaplamamalı; beyaz tema ve mevcut yapı korunmalı.
- Kullanıcının “altyazılar” ifadesi bu bağlamda alttaki durum/bildirim yazıları olarak yorumlandı; video konuşma altyazısı özelliği için yeni kapsam varsayılmadı.

## Kayıtta doğrulanan
45869.mp4 yüklemesinde yüzde32→64→84→100 ve MB2.3/6.8→4.4/6.8→5.8/6.8→6.8/6.8 görünüyor. Video ardından topluluk gönderisinde görünüyor ve “Gönderin paylaşıldı” koyu alt bildirimi çıkıyor. Bu denemede yükleme çalışıyor; yeni istek ağırlıklı olarak kompakt renkli sunum.
Son örnek karede Videolar sekmesi kısa süre boş görünür; önceki karede gönderi var. Bunun yükleme/yeniden kurulan akış kaynaklı geçici durum olup olmadığı ayrıca incelenmeli, kalıcı kayıp diye işaretlenmedi.
Bu aşamada kod değişmedi; toplu düzeltmeye not edildi.
