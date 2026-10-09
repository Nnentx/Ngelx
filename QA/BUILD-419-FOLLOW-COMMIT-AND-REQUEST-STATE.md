# Build 419 — Takip ve arkadaşlık düğmelerinde tutarlı sunucu durumu

## Kaynakta bulunan hata

`takipDurumuDegistir` önce takipçinin `following` ve hedef hesabın `followers` listesini tek bir batch ile başarıyla güncelliyor, sonra `await uygulamaBildirimiGonder(...)` çağırıyordu. Bildirim izni, ağ hatası veya zaman aşımı gerçekleşirse tamamlanmış takip işlemi yanlışlıkla başarısız raporlanabiliyor, ekranda yerel durum geri alınıyor ve iki hesap arasında kısa süre farklı yazı görünebiliyordu.

Ayrıca ziyaretçi profilindeki takip/arkadaşlık isteği düğmeleri, kullanıcı profil bilgileri gelse bile ilgili `outgoing` istek belgesi daha gelmeden **Takip et / Arkadaş ekle** gösterebiliyordu. Gerçekte hâlâ bekleyen istek varsa bu gösterim yanıltıcıdır.

## Build 419 ile kodlanan düzeltmeler
1. İki yönlü takip ilişkisinin `batch.commit()` sonucu takip işleminin tek doğruluk kaynağıdır.
2. Takip bildirimi aynı mevcut bildirim işleviyle arka planda, hatası yakalanarak gönderilir; bildirim gönderimindeki hata ilişki kaydını iptal edilmiş gibi göstermez.
3. Takip ve arkadaşlık giden istek snapshot'ları alınmadan bu düğmeler yükleniyor gösterir. Firestore okuma hatasında yanlış "yeni istek" eylemi yerine açık hata metni gösterir.
4. Şema, veritabanı ilişkileri, istek/iptal/kabul işlemleri, profil tasarımları, mesajlaşma ve Firestore güvenlik kuralları değiştirilmedi.

## Test beklentileri
- Hesap A -> B'yi takip et -> ağ/bildirim sorunu olsa bile, iki kullanıcıda gerçek takip ilişkisi korunmalı.
- Gizli hesapta bekleyen takip isteği varken profil açıldığında önce yüklenme, sonra “Takip isteği bekliyor” görülmeli.
- Bekleyen arkadaşlık isteği aynı biçimde yüklenmeli; “Arkadaş ekle” geçici olarak görünmemeli.
- Takipten çıkma, arkadaşlığı kaldırma, mesaj, ortak gruplar ve kapaklı/kapaksız profil işlevleri eskisi gibi çalışmalı.
- Aktivite ve gelen kutusu bildiriminin gerçekten karşı cihaza düşmesi ayrıca canlı cihaz testidir.

**Durum:** Build 419 kodu hazırlanıp CI başlatıldı. Otomatik test ve telefon QA olmadan tüm sorunlar çözülmüş sayılmaz.
