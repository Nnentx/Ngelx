# NgelX Build 421 — Gelen Kutusu / Aktivite / istek akışı düzenleme talebi

**Kayıt:** 09.10.2026, ekran görüntüsü `45376.jpg` ve yaklaşık 29,6 saniyelik ekran videosu `45375.mp4`.  
**Kaynak:** Kullanıcının açık UX isteği + telefon ekran kaydı.  
**Durum:** **Toplu Work paketine not edildi; henüz uygulama kodu değiştirilmedi.** Mevcut arkadaşlık, takip, grup ve bildirim kayıtları korunmalı.

## Sorun: Gelen Kutusu içindeki bildirim/isteklerden ikinci bir Aktivite ekranına düşülüyor

- **00:00–00:06:** Gelen Kutusu > Tümü, Mesajlar, Gruplar, Bildirimler, İstekler sekmeleri görülüyor. `Tümü` içinde `Umay Umay Seni takip etmeye başladı` ve `Umay Umay sana arkadaşlık isteği gönderdi` gibi eylem bağlamı taşıyan satırlar var. Bildirimler sekmesinin gösterdiği bazı öğeler yalnız `Yeni bildirim` yazıyor; gönderen ve olay bağlamını kaybediyor.
- **00:08–00:12 ve 00:18–00:22:** Ayrı `Aktivite` ekranı açılıyor, `Tümü 15 / Takip istekleri / Arkadaşlık istekleri / Gruplar...` sekmeleri ve aynı bildirim/istekler tekrar görünüyor. Kullanıcı bunun fazla tekrar olduğunu, istek/bildirime basınca önce Aktivite'nin yeniden açılmamasını istiyor.
- **Ekran görüntüsü:** Aktivite > Tümü içinde Umay'ın takip bildirimi ve Umay'ın arkadaşlık isteği ayrı satırlarla gösteriliyor; arkadaşlık isteğinde yeşil onay simgesi var.
- **Belirsizlik:** Videoda belirli bir alt sekmeye tam hangi dokunuşun hangi rotayı tetiklediği frame örneklerinden tek başına kanıtlanamıyor. Kullanıcının doğrudan bildirimi de tasarım gereksinimi olarak kaydedildi.

## İstenen yeni tasarım — tek Gelen Kutusu bildirim/istek akışı

1. **Çift Aktivite ekranı kaldırılmalı / ikinci sayfaya zorunlu yönlendirme iptal edilmeli.** `Gelen Kutusu` içindeki **Bildirimler** sekmesi bildirimleri aynı sayfada doğrudan göstermeli; **İstekler** sekmesi de bekleyen arkadaşlık ve gizli hesap takip isteklerini aynı sayfada listelemeli. Diğer türdeki grup/etkileşim/bildirimleri kaybetmeden mevcut tek bir veri kaynağı/filtre kullanılmalı.
2. **`Umay Umay seni takip etmeye başladı` satırına tıklayınca** Umay'ın profilini doğrudan açmalı; sırf bu bildirim için yeni bir `Aktivite` sayfası açılmamalı. Bu satır, açık profilde **gerçekleşmiş bir takibi** anlatır; otomatik 'onayla' işlemi gerekmez. Profilden karşılık takip ve profil incelemesi yapılabilir.
3. **`Umay Umay sana arkadaşlık isteği gönderdi` satırına tıklayınca** Umay'ın profili açılmalı; **bekleyen istek varsa** profilde **Arkadaşlığı kabul et / Reddet** eylemleri görünmeli ve gerçek Firebase `friend_requests` belgesi üzerinden işlensin. İstek zaten kabul edilmiş, reddedilmiş veya geri çekilmişse profil artık yanlış 'onayla' sunmamalı.
4. **`Takip isteği gönderdi` satırında** hedef hesap gizli ve istek hâlâ bekliyorsa profilden **Takip isteğini kabul et / Reddet** sunulmalı. **`Seni takip etmeye başladı`** ile **`Takip isteği gönderdi`** olayları birbirine karıştırılmamalı.
5. Başarıdan sonra **Gelen Kutusu > İstekler** ve ilgili bildirim satırları canlı güncellensin; bekleyen sayaç azalsın, ilgili kişi profiline dönüldüğünde ilişki durumu doğru görünsün. Kullanıcı başka bir Aktivite sayfasını dolaşmak zorunda kalmasın.
6. Bildirim listelerinde `Yeni bildirim` gibi belirsiz satırlar mümkün olduğunca **gönderen + olay** olarak gösterilsin; okunmuş/okunmamış durumu, deduplikasyon, zaman bilgisi ve grup bildirimleri korunsun.
7. `Gelen Kutusu` ekranındaki mevcut **Tümü / Mesajlar / Gruplar / Bildirimler / İstekler** tasarımı ve sohbet açma işlevleri korunmalı. Kullanıcının kastı bildirimleri silmek değil, **tekrarlanan Aktivite navigasyonunu kaldırmak ve doğru profil/istek eylemine gitmek**.
8. Profil üzerinde eylem eklenirken kullanıcı gizliliği, engelleme ve Firestore izinleri korunmalı; takipçi olmak, arkadaşlık veya mesaj izni otomatik verilmemeli.

## Geliştirme öncesi test sözleşmesi

- Gelen Kutusu > Tümü > gerçekleşmiş takip bildirimi -> gönderen profil, **onay istemeden**.
- Gelen Kutusu > Tümü / İstekler > bekleyen arkadaşlık isteği -> gönderen profil -> Kabul Et -> her iki hesapta arkadaşlık doğru ve sayaçlar güncel.
- Bekleyen arkadaşlık -> Reddet -> hiçbir hesap yanlış `Arkadaşsınız` yazmamalı.
- Gizli profile takip isteği -> gönderen profil -> Kabul/Reddet ve bekleyen sayaç doğru.
- Bildirimler sekmesi **ayrı Aktivite sayfası açmadan** gönderenin olayını göstermeli.
- Eski aktivite/deeplink kaynaklarından uygulama çökmeden yeni Gelen Kutusu/Bildirimler akışına yönlendirme yapılabilmeli.
- Mesaj, grup, sesli/görüntülü arama, bildirim okundu durumu, sosyal istek ve güvenlik regresyon testleri tekrar çalışmalı.

## Dört önceki video ile birleştirme

Bu beşinci kayıtta yeni bir **Bildirim/Gelen Kutusu akış tasarımı** isteği vardır. Önceki kayıtlardaki açık P1 hikâye yanıtı gönderme hatası, katılım tarihi kırpılması, uzun açılış yüklemesi ve kapak değiştirme düğmesi ayrı maddeler olarak durur; yeni tek Work paketiyle birleştirilecektir.

**Üretim hesapları, Firebase/Firestore kayıtları veya uygulama kodu bu QA raporuyla değiştirilmedi.**

## KALDIRMA KARARI — gereksiz ikinci Aktivite ekranı

**09.10.2026 kullanıcı onayı:** “Tamam gereksiz aktivite bölümünü sil istersen not et.”

- **Bağımsız/tekrar eden “Aktivite” sayfası, yeni tasarımdaki gezinmeden kaldırılacak.** Gelen Kutusu'nda Bildirimler ve İstekler zaten olduğundan kullanıcı tekrar aynı bildirimleri ayrı ekranlarda dolaşmayacak.
- **Gelen Kutusu → Tümü / Mesajlar / Gruplar / Bildirimler / İstekler** korunacak; Bildirimler/İstekler içerikleri *aynı ekran içinde* gösterilecek, ikinci Aktivite sayfası açılmayacak.
- Üst menü/bildirim zili gibi eski **Aktivite** girişleri uygun **Gelen Kutusu → Bildirimler** sekmesine yönlenecek. Eski deeplink veya kaydedilmiş bildirim tıklamaları çökmeyecek.
- **Silinecek şey yalnız gereksiz ekran ve tekrar eden navigasyon.** Mevcut bildirim kayıtları, takip/arkadaşlık/grup istekleri, okundu bilgileri, geçmiş, sayaçlar, canlı güncellemeler **kesinlikle silinmeyecek**.
- “Umay seni takip etmeye başladı” gibi tamamlanmış takip bildiriminde gönderenin profiline gidilecek; sırf bunun için onay istenmeyecek.
- Bekleyen **arkadaşlık veya gizli hesap takip isteğinde** istek gönderenin profiline gidilecek; yalnızca `pending` durumunda **Yanıtla → Kabul et / Reddet**. İstekler listesinde **Onayla / Sil**, gerçek ortak arkadaş sayısı (varsa) ve küçük profil fotoğrafları gösterilecek.
- Değişiklikten sonra mevcut çalışan sohbet/grup/arkadaşlık/takip ve Firebase yetkileri korunmalı; canlı bildirim teslimi ve okundu durumu uçtan uca test edilmeli.

**Durum:** Bu bir **Work kapsam/ürün kararı**dır. Kod şu anda silinmedi veya değiştirilmedi. Silme sırasında veri temizliği yapılmayacak.
