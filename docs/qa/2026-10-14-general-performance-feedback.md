# Genel uygulama yavaşlığı — kullanıcı bildirimi
2026-10-14 01:22 Europe/Istanbul. Kullanıcı uygulamanın her tarafında ekran geçişlerinin ve klavye açılıp kapanmasının geç gerçekleştiğini bildirdi. Toplu düzeltme paketine dahil.

İncelenecekler: ana iş parçacığındaki pahalı işlemler; ekran açılışından önce beklenen ağ çağrıları; build içinde yeniden kurulan Firestore akışları/future işlemleri; geniş widget ağacını sık yenileyen sayaçlar ve streamler; görsellerin çözünürlüğe göre yüklenmesi; klavye odağının ve widget kimliğinin korunması. Gerçek cihazda performans ölçümü olmadan bütün uygulamanın hızlandığı veya sorun nedeninin bulunduğu iddia edilmeyecek.
