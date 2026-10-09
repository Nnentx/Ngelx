# Build 426 QA — 45531.jpg

Gelen Kutusu > İstekler. Kullanıcı bazen kırmızı isteklere ait sayaçta 3 gördüğünü, ancak karşılık gelen yeni bildirim/isteğin görünmediğini bildiriyor. Ekran görüntüsünde sayaç 2 ve iki kart var: Alperen Yarbay arkadaşlık isteği ve takip isteği. Bu tek kare sayaç 3 hatasını kanıtlamıyor; **aralıklı, kullanıcı tarafından bildirilen** sorun olarak tekrar üretim gerekiyor.

İstenen: İstekler rozeti, gerçek bekleyen ve kullanıcıya gösterilebilir isteklerin tekil kayıt sayısıyla tutarlı olsun; kabul/sil/iptal ve oturum değişiminde anlık senkronize olsun; gizli veya eski kayıtlar sayılmasın. Bildirimler sekmesinin kendi sayacıyla karıştırılmasın. Önceki idempotent istek oluşturma ve aynı gönderen+tür için tek pending kuralı korunmalı.

İkinci sorun ekran görüntüsünde açık: sekme çubuğu ile 'Mesaj İstekleri' kutusu arasında büyük dikey boşluk var. Kutuyu sekmelerin hemen altına taşı; altında arkadaşlık ve takip istekleri normal aralıklarla sıralansın. Güvenli alan ve alt gezinme çubuğu korunmalı.

Durum: QA kaydı; kod değişikliği veya cihazda doğrulama yapılmadı.