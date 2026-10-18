# Build488 — Canlı yayın video referansı / B1 cihaz kabul testi

**Durum:** QA derlemesi sürüyor; fiziksel Android cihaz testleri **yapılmadı**. Mevcut üretim Build484 dağıtımı ve site indirme bağlantıları değişmez.

## Kullanıcı video referansına göre B1 hedefi
- Yayın gerçek LiveKit oda ve video üstünde devam etsin.
- Küçük üst profil; adın **altında kalp/beğeni sayacı**. Takip ilişkisine göre küçük **Takip et / Takiptesin**.
- İzleyici videoya **çift dokununca** kalp animasyonu mevcut beğeni olayını bir defa tetiklesin; tek dokunma ve diğer düğmeler yanlışlıkla beğeni göndermesin.
- Sağ alt-orta tarafta **sadece küçük “+”** görünsün, yanına **Talep** yazılmasın.
- + açılınca sağ tarafta **yukarıdan aşağı en fazla 10 kabul edilmiş konuk** küçük avatar/isim olarak sıralansın. Dar şerit kaydırılabilir olsun; host video merkezini, yüzünü, yorum alanını veya çıkış düğmelerini kapatmasın.
- Mevcut katılım isteği, yayıncı konuk yönetimi, yorum, hediye, paylaş, PK, yayını bitir, kamera/mikrofon ve tekrar bağlanma çalışmaya devam etsin.
- Kaldırılması istenen lig/hedef seviye/hediye ustası kutularını **yeni ekran overlayine eklemeyin**.

## Manuel Android QA
- [ ] Yayıncı ve izleyici olmak üzere iki ayrı test hesabıyla iki telefonda başlat; arka planda video durmasın.
- [ ] Takip etmeyen görür: **Takip et**; takip ettikten sonra **Takiptesin**; yeniden açınca doğru durum.
- [ ] Gerçek beğenilerde yayıncı adının hemen altındaki sayaç güncellenir; TR sayı biçimi.
- [ ] Çift dokunma aynı anda yorum yazmayı, hediye göndermeyi veya + konuk düğmesini yanlış tetiklemez.
- [ ] 0, 1, 5, 10 ve 11 kabul edilmiş konuk: şerit en fazla 10 küçük pencere gösterir; taşma olmaz, kapat/aç çalışır.
- [ ] 3 tuşlu/jest Android gezinme ve küçük ekran: + konumlanması, çentik/safe area, klavye açık/kapalı, yorum bileşeni.
- [ ] Konuk kabulü/iptali, bağlantı kopması, yayını bitir, PK, hediye ve paylaş eski davranışlarını korur.
- [ ] Yayıncı kafası/yüzü sağ konuk şeridi nedeniyle örtülmez.
- [ ] Ekran görüntüleri gerçek cihazlarda karşılaştırılır ve hatalar #106 ile paylaşılır.

## Henüz B2'ye kalanlar
- **Gerçek 10 konuk video thumbnail'i** (B1 sadece avatar/isim mini kutularıdır).
- Her bir konuk için güvenli **Sessize al / Sesten at** ses moderasyonu, mevcut yetki kurallarıyla.
- Katılma isteğinin video referansındaki alttan açılan panel tasarımına uyarlanması; canlı arayüzün tamamının video referansıyla eşleşmesi.

Kaynak: [canlı yayın #106](https://github.com/Nnentx/Ngelx/issues/106) • [PR #108](https://github.com/Nnentx/Ngelx/pull/108).
