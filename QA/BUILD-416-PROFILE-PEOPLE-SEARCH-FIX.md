# NgelX Build 416 — Profil aramasında kişiler yolu (09.10.2026)

## Cihaz ekranıyla eşleşen kök neden
Kullanıcı ekranında `adem` arandığında **Tümü / Fotoğraf / Video / Yazı** sekmeleri ve **Eşleşen paylaşım bulunamadı** metni görünüyor. Bu ekran `ProfilAramaPage` ve `videos.where('ownerId', ...) ` üzerinde **yalnız o kişinin paylaşımlarını** arar. Genel kullanıcı aramasından farklıdır. Bir arkadaşın burada gösterilmemesi doğrudan arkadaşlık kaydının silinmesi anlamına gelmez.

## Güvenli ekleme
- Profil paylaşım aramasına görünür **Kişiler** kategorisi eklenir. Dokununca mevcut `AramaPage(baslangicSorgu:q)` açılır; yazılan sorgu korunur.
- Eşleşen paylaşım yoksa **Kişilerde ara** düğmesi aynı işlemi yapar.
- Arama kutusunun ipucu artık paylaşım araması ile kişiler seçeneğini açıklar.
- Fotoğraf/video/yazı filtreleri, gerçek gönderi gezinmesi, kullanıcı gizliliği, engelleme ve Firestore kuralları aynen bırakılır.
- Build 413'te genişletilen kişi araması olduğu gibi yeniden kullanılır; ikinci bir sonuç veri modeli geliştirilmez.

## Test beklentisi
1. Rojin / Adem ilişkisi arkadaş listesinde doğru görünmeli.
2. Profil -> arama -> `adem` -> **Kişiler** -> genel arama sayfasında uygun/görünür Adem sonucu çıkmalı.
3. Profil -> arama -> Fotoğraf/Video/Yazı önceki gibi gerçek profil paylaşımlarını süzmeli.
4. Arama ve diğer tüm akışlar küçük ekranlarda kullanılabilir olmalı.

**Sınır:** Bu paket iki arama yüzeyi arasındaki yönlendirme UX'ini düzeltir. Kullanıcıya özel görünürlük, hesap gizlilik tercihleri ve veritabanı indeksleri cihaz testiyle ayrıca doğrulanacaktır.
