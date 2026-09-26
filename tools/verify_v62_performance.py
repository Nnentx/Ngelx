#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
app = (ROOT / "app/lib/main.dart").read_text(encoding="utf-8")

checks = [
    (
        "Arka plan slideri lokal, tek yazma",
        "onChangeEnd:(x)async" in app
        and "setSliderState(()=>sliderOpacity=x)" in app
        and "onChanged:(x)async{\n                    if(!await ngelxCanManageGroup" not in app,
    ),
    (
        "Mesaj spinner her durumda kapanir",
        "finally{\n      if(mounted)setState(()=>mesajGonderiliyor=false);" in app,
    ),
    (
        "Gizli kelime tam kelime/eslesme filtresi",
        "bool ngelxHiddenWordMatches(" in app
        and app.count("ngelxHiddenWordMatches(metin,gizliKelimeListesi)") == 2
        and "metin.toLowerCase().contains(x.toLowerCase())" not in app,
    ),
    (
        "Sabitleme sunucu dogrulamasi",
        "GetOptions(source:Source.server)" in app
        and "pin_not_persisted" in app,
    ),
    (
        "Tekrarlayan eski grup arka plan menusu kaldirildi",
        "Future<void> grupArkaPlanMenusu()async{" not in app
        and "Future<void> _grupArkaPlanOlayi(String eylem)async{" not in app,
    ),
    (
        "Hizli emoji gereksiz yazma engeli",
        "toString()==emoji?null:()=>unawaited(ref.set({'quickEmoji':emoji}" in app,
    ),
    (
        "Okundu bilgisi gereksiz chat rebuild yapmaz",
        "if(okunmamis<=0)return;" in app
        and "if(okunmamis>0)'unread_$ben':0" not in app,
    ),
]

failed = []
for name, ok in checks:
    print(("PASS" if ok else "FAIL") + " | " + name)
    if not ok:
        failed.append(name)

if failed:
    print("\nV62 performans dogrulamasi BASARISIZ: " + ", ".join(failed))
    sys.exit(1)

print("\nV62 performans dogrulamasi basarili: %d/%d" % (len(checks), len(checks)))
