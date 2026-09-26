#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
app = (ROOT / "app/lib/main.dart").read_text(encoding="utf-8")

checks = [
    (
        "Grup verisi girdi islemlerinde onbellekten kullaniliyor",
        "Future<Map<String,dynamic>> _grupVerisiHizli()async" in app
        and "final grupData=await _grupVerisiHizli();" in app
        and "final v=await _grupVerisiHizli();" in app,
    ),
    (
        "Yaziyor durumu klavye acilisindan sonra gecikmeli yaziliyor",
        "_typingBaslatZamanlayici=Timer(const Duration(milliseconds:220)" in app
        and "_typingBaslatZamanlayici?.cancel();" in app,
    ),
    (
        "Mention aramasi cache ve stale-query korumali",
        "final surum=++_mentionAramaSurumu;" in app
        and "surum!=_mentionAramaSurumu" in app
        and "kisiSayisi>=8" in app,
    ),
    (
        "Mention paneli klavye acikken tasma yapmiyor",
        "maxHeight:MediaQuery.viewInsetsOf(context).bottom>0?170:300" in app,
    ),
    (
        "Mesaj duzenle overlay kapanisini bekliyor",
        "await ngelxOverlayKapanisiniBekle();" in app
        and "autofocus:true,minLines:2,maxLines:4" in app
        and "buildCounter:(_, {required int currentLength,required bool isFocused,required int? maxLength})=>null" in app,
    ),
    (
        "Mesaj duzenleme kaydi timeout ve hata geri bildirimi kullaniyor",
        "Düzenleme kaydedilemedi. Tekrar dene." in app
        and ".timeout(const Duration(seconds:5))" in app,
    ),
]

failed = []
for name, ok in checks:
    print(("PASS" if ok else "FAIL") + " | " + name)
    if not ok:
        failed.append(name)

if failed:
    print("\nV63 girdi performans dogrulamasi BASARISIZ: " + ", ".join(failed))
    sys.exit(1)

print("\nV63 girdi performans dogrulamasi basarili: %d/%d" % (len(checks), len(checks)))
