# NgelX Build 393 — Social / Group Exit Sync Work Package

## Amaç
Build 392 cihaz testinde başarılı geçen davranışları korurken takip, arkadaşlık, mesajlaşma ve grup çıkış/çıkarılma akışlarını tamamlamak.

## Korunacak davranışlar (regresyon kapısı)
- Sohbet performansı / ağırlaşmanın giderilmiş olması.
- Kısa ve uzun özel mesaj gönderme ve karşı hesaba teslim.
- Web bağlantılarının tıklanabilir olması ve tarayıcıda açılması.
- Engelleme / engeli kaldırma; engel kaldırınca ilişkinin otomatik geri kurulmaması.
- Okunmamış mesaj sayacının sohbet açılınca güncellenmesi.
- Grup oluşturma, grup mesajı gönderme ve diğer hesaba teslim.
- Grup kurucusu/yönetici/üye rollerinin doğru görünmesi.
- Kurucunun korunması; normal yöneticinin kurucu yetkilerine sahip olmaması.
- Yönetici atama ve rolün diğer hesaba senkron olması.
- Yönetici tarafından üye ekleme / çıkarma.
- Engellenen kişinin grup mesajlarının gizlenmesi, dokununca geçici gösterilmesi ve tekrar girişte yeniden gizlenmesi.
- Engellenen profile grup içinden girildiğinde engel ekranının gösterilmesi.

## Build 393 düzeltmeleri

### Grup çıkış / çıkarılma modeli
- Gruptan çıkarılan veya kendi ayrılan kullanıcı için konuşma otomatik silinmez.
- Eski grup, Gelen Kutusu'nda kilitli konuşma olarak görünmeye devam eder.
- Eski mesaj geçmişi çıkış anına kadar okunabilir; çıkıştan sonraki yeni mesajlar alınmaz.
- Alt mesaj yazma alanı yerine sabit uyarı paneli:
  - "Bu gruba mesaj gönderemezsin"
  - "Artık bu grupta değilsin. Tekrar ekleninceye kadar mesaj gönderemez, arama yapamaz ve yeni grup mesajlarını alamazsın."
  - "Konuşmayı sil" butonu.
- Başkası çıkardıysa grup içinde kişiselleştirilmiş sistem satırı: "ADEM baykar seni TEST GRUP 392 grubundan çıkardı."
- Kullanıcı kendi çıktıysa: "Gruptan ayrıldın."
- Gruptan çıkarılınca Aktivite bildirimi oluşur ve bildirime dokunmak eski grup geçmişini açar.
- "Konuşmayı sil" sonrası grup arşiv kartı ve sohbet görünümü kaldırılır.

### Takip / arkadaşlık
- Yeni takip/arkadaşlık isteği Activity dedupe sırasında eski istek tarafından ezilmez.
- Takip ve arkadaşlık istekleri doğru filtrede ve sayaçta görünür.
- Engelleme iki yöndeki bekleyen takip/arkadaşlık isteklerini iptal eder; eski "istek bekliyor" durumu kalmaz.
- Engeli kaldırmak takip/arkadaşlık ilişkisini otomatik geri kurmaz.
- Özel sohbet bilgi ekranındaki arkadaşlık isteği gönderimi eski bildirim kayıtlarına değil kanonik sosyal istek akışına dayanır.

### Mesajlaşma
- Mesaj butonu doğru özel sohbeti açmalı / oluşturmalı.
- Mesaj istekleri ayrı alanda kalmalı; kabul/red durumu iki hesapta senkron olmalı.
- Okunmamış mesaj ve Aktivite sayaçları gerçek durumla eşleşmeli.
- Tarayıcıdan sohbete dönüşte gereksiz eski mesaj konumuna sıçrama ayrıca regresyon testinde kontrol edilecek.
- Hesap değişiminde başka hesabın ilişki, taslak veya mesaj durumu taşınmamalı.

## Cihaz test senaryoları
1. Umay → Rojin takip isteği: Rojin Aktivite/Takip İstekleri'nde yeni istek ve sayaç.
2. Umay → Rojin arkadaşlık isteği: Rojin Arkadaşlık İstekleri'nde görünür; kabul/red iki hesapta senkron.
3. ADEM → DİLEK grup çıkarma: DİLEK Gelen Kutusu'nda grup kalır, Aktivite bildirimi gelir, eski geçmiş açılır, mesaj/arama kapalıdır.
4. Kullanıcı kendi gruptan ayrılır: aynı kilitli konuşma modeli, "Gruptan ayrıldın." metni.
5. Yeniden gruba ekleme: kilit kaldırılır, grup arşiv kaydı temizlenir, mesajlaşma tekrar açılır.
6. Engelle → engeli kaldır: çalışan Build 392 davranışları bozulmaz.
