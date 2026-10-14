# Build 457 cihaz hata paketi — geliştirme/test aşamasında

Build456 onaylanmış başarı SHA: `3e8ff6cfc52a99e27fc060f8670d01017333a03e`; kayıtlar #47–#52 ve 47456.mp4 videosu. Build 457 yeni dalda hazırlanır, `main` değiştirilmez. Çalışan topluluk video yükleme korunur.

## İlk değişiklikler (henüz Android cihazında doğrulanmadı)
- Canlı yayın video track henüz gelmiyorsa 10 saniye sonra sonsuz spinner yerine açıklama + yayıncı için kamerayı yeniden başlat, izleyici için yeniden bağlan seçenekleri.
- Canlı yayında görüntü ayarları Firestore dinleyicisi ekranın saniye sayacı yeniden çizdikçe yeniden oluşturulmasın.
- Eksik track için uygulama testleri; önceki giriş, sohbet, medya yükleme ve sunucu yetkileri korunur.

## Takip edilen cihaz hataları
- #47 Akış siyah ekran ve medya yüklemesi; #48 canlı/topluluk/video siyah ekran — P0.
- #49 çağrı zil sesi duyulmuyor; #50 Keşfet topluluk avatarları spinner'da kalıyor.
- #51 canlı yayın boş beyaz alt modal + referans yayıncı/izleyici tasarımı.
- #52 Gelen Kutusu farklı UID / kullanıcı profil adının yanlış eşlemesi, yanlış alıcı riski.
- 47456.mp4: kapak kadrajı kurucu için bile izinsiz; sohbet fotoğraf %100 sonrası mesaj görünürlüğü; geri dönüşlerde siyah ekran / tekrar yükleme.

**Önemli:** Kodun başarılı derlenmesi kamera/RTC görüntüsünün gerçekten geldiğini kanıtlamaz; siyah görüntü devam ediyorsa ayrıca sunucu ve cihaz loglarıyla teşhis gerekir. Hesaplar/veriler silinmez, ücretli Cloud Functions/Firestore canlı kuralları izinsiz dağıtılmaz. PR inceleme taslağıdır.
