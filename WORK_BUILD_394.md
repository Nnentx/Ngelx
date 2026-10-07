# NgelX Build 394 — Inbox / Chat / Activity / Search Fixes

## Korunan davranışlar
- Build 393 takip isteği gönderme -> karşı hesaba Aktivite -> kabul -> "Takip ediyorsun".
- Arkadaşlık isteği gönderme -> karşı hesaba düşme -> kabul -> "Arkadaşsınız".
- Özel mesaj gönderme ve karşı hesaba teslim.
- Okunmamış özel mesaj sayacının sohbet açılınca temizlenmesi.
- Gruptan ayrılınca/çıkarılınca eski konuşmanın korunması ve yeni mesajların eski üyeye gösterilmemesi.
- Engelleme/engel kaldırma ve grup içi engellenmiş mesaj davranışları.
- Kurucu/yönetici/üye izin sınırları.

## Build 394 düzeltmeleri
- Gelen Kutusu: kilitli eski gruplar ile aktif sohbetler tek ListView içinde, tek kaydırma alanı.
- Grup eski üye ekranı: "engellediğin kişi var / gruba gir" uyarısı artık gösterilmez.
- Eski üyede sesli/görüntülü arama butonları gizlenir; eski çağrı kartında "Tekrar Ara" aktif olmaz.
- Gruptan çıkarılma Aktivite kaydı doğrudan üyelik olayı olarak yazılır.
- Özel sohbet: cache -> server geçişinde açılış kaydırması son mesaja sabitlenir; PageStorageKey ile konum daha kararlı tutulur.
- Özel sohbet: klavye açılışında scrollPadding azaltıldı.
- Özel sohbet arka planı: ortak backgroundUrl boşsa eski iki katılımcı alanlarından güvenli fallback.
- Takip/Takipçi/Arkadaşlar araması: sabit controller + focus; yazı kendiliğinden silinmez; gerçek filtre sonuç sayısı gösterilir.
- Profil etkileşim sayacı yüklenirken yanlış 0 göstermek yerine yükleme durumu gösterir.

## Cihaz testleri
1. Gelen Kutusu tek kaydırma: kilitli gruplar + aktif sohbetler birlikte hareket etmeli.
2. Çıkılmış gruba gir: engelli kişi modalı çıkmamalı, arama ikonları görünmemeli.
3. ADEM -> DİLEK gruptan çıkar: Aktivite'de "ADEM baykar seni TEST GRUP 392 grubundan çıkardı." görünmeli.
4. Özel sohbetten Sohbet bilgisi/profil/tarayıcıya gidip geri dön: konum eski mesajlara sıçramamalı.
5. Mesaj yazarken klavye: sohbet gereksiz yukarı fırlamamalı.
6. DİLEK/Rojin arka planı iki hesapta aynı görünmeli.
7. Takip/Takipçi/Arkadaşlar aramasına uzun isim yaz: klavye ve metin korunmalı; sonuç sayısı doğru olmalı.

Build workflow trigger: source fixes ready for CI validation.
