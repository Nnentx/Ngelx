# Build 417 — Hesap değişimi, arkadaş avatarları ve profil oturumu

## Build 412–416 koruma sözleşmesi
- Kapaklı/kapaksız görünüm, profil tanıtım videosu, gönderi grid'i, dört profil işlemi, arkadaşlık/takip istekleri, mesajlaşma ve arama aynen korunur.
- Firebase kimlik doğrulama ve şifre saklama politikası değiştirilmez; hiçbir yeni yetki verilmez.
- `firestore.rules` ve canlı veritabanı değiştirilmez. Mevcut koruma, Firestore emulator, Flutter analyze, APK imza kontrolleri çalışır.

## Tespit edilen kaynak sorunları
1. Hesap değiştir ekranındaki `FutureBuilder` içinde `future:_profil(email)` kullanılıyordu. Her yeniden çizimde yeni bir Future ve Firestore okuması oluşabiliyor, yeni yanıt gelene kadar isim/avatar yerine e-posta ve varsayılan simge görülebiliyordu.
2. `_ArkadaslarPageState` ilk `users.limit(250)` sorgusunda olmayan arkadaş profillerini bir kez `.get()` ile yüklüyor, sonra avatar/isim güncellenmesine abone olmuyordu.
3. `_ProfilPageState.profiliGetir` asenkron isteği tamamlanırken oturum değişmişse eski UID'nin profilini hâlâ ekrana yazma riski taşıyordu.

## Build 417 kaynak düzeltmeleri
- Hesap/e-posta başına yeniden kullanılan bir Future; sadece kullanıcı isterse ilgili e-postanın profilini yeniden deneme.
- Beklerken “Profil yükleniyor...” durumu; hata durumunda profil adının e-postaya düşmesi yerine açık durum ve yeniden deneme.
- Kaydedilmiş e-posta/UID eşlemesi korunur; bilinmeyen UID için kullanıcı profili uydurulmaz.
- İlk sorguda bulunamayan arkadaşlar için canlı Firestore profil dinleyicisi. Eksik/silinmiş kullanıcı belgesine karşı hata durumu.
- Sahip profilinin eski UID yanıtının oturum değişiminden sonra ekranı güncellemesini engelleme.

## Cihazda yeniden doğrulanacaklar
- Sultan -> Adem -> Rojin hesapları arasında geçiş, farklı ad/fotoğraf/arkadaş sayısı ve doğru oturum.
- İnternet yavaşken hesap kartlarının “Profil yükleniyor...” göstermesi; her karakter güncellemesinde tekrar istek atmaması.
- Bir hesaptan profil fotoğrafını değiştirme, diğer hesaptaki arkadaş listesinde yenilenmesi.
- Sohbet/Arkadaş/Profil arası gezinmede hesap değişimine ait eski değerlerin görünmemesi.
- Gerçek çift taraflı arkadaşlık, takip ve bildirim teslimleri hâlâ cihaz testi bekler.

**Durum:** Build 417 kaynak kodu ve test zinciri hazırlanmıştır. Otomatik test ve APK sonucu görülmeden tamamlandı denmez.
