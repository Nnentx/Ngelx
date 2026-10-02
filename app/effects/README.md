# NgelX Pro Beauty (Build 369)

Bu klasör profesyonel yüz efekt motorunun resmi effect paketleri içindir.

## Kalite kuralı

NgelX'te eski basit blur/parlaklık rötuşu "Pro Beauty" olarak sunulmaz.
Pro mod yalnızca gerçek yüz takipli, bölgesel çalışan profesyonel motor hazırsa açılır.

## Gerekli kurulum

1. Banuba Face AR / TouchUp için geçerli bir Client Token edin.
2. Banuba'nın resmi **TouchUp** effect paketini bu konuma yerleştir:
   `app/effects/TouchUp/`
3. Paket içinde en az resmi config ve gerekli modül/assets dosyaları bulunmalı.
4. Build'i şu tanımlarla üret:

```
flutter build apk --release \
  --dart-define=BANUBA_CLIENT_TOKEN=<TOKEN> \
  --dart-define=BANUBA_TOUCHUP_READY=true
```

İstenirse effect yolu ayrıca değiştirilebilir:

```
--dart-define=BANUBA_TOUCHUP_EFFECT=effects/TouchUp
```

## Güvenlik

Client token kaynak koda commit edilmez. CI secret / dart-define ile verilir.

## Hedeflenen gerçek kontroller

- Skin.softening / Pürüzsüz
- FaceMorph eyes
- FaceMorph nose
- FaceMorph face narrowing / jaw / chin
- FaceMorph lips
- Eyes whitening
- Teeth whitening

Bu kontroller yalnız UI değildir; Banuba TouchUp effect motoruna `evalJs` ile gerçek zamanlı iletilir.

## Regresyon koruması

Bu kamera çalışması yapılırken daha önce cihazda geçen:
- takip/arkadaşlık istekleri,
- Mesaj İstekleri,
- normal mesajlaşma unread sayaçları,
- Aktivite/zil senkronizasyonu

bozulmayacaktır.
