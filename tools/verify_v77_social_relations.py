#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN=(ROOT/"app/lib/main.dart").read_text(encoding="utf-8")
PUB=(ROOT/"app/pubspec.yaml").read_text(encoding="utf-8")

def require(cond,msg):
    if not cond:
        raise SystemExit("Build 296 sosyal ilişki kontrolu eksik: "+msg)

require("version: 1.0.81+300" in PUB,"Build 300 surumu")
require("defaultValue: '1.0.81'" in MAIN and "defaultValue: '300'" in MAIN,"uygulama ici surum")
require(".where('fromUid',isEqualTo:user.uid)" in MAIN and ".where('toUid',isEqualTo:hedefUid)" in MAIN,
        "istek gondermeden once kullanici-cifti bazli bekleyen istek kontrolu")
require("GetOptions(source:Source.server)" in MAIN,
        "takip/arkadaslik icin sunucu dogrulamasi")
require("hedefVeri['followers']" in MAIN and "hedefVeri['friends']" in MAIN,
        "iki tarafli iliski dogrulamasi")
require("final gonderildi=await sosyalIstekGonder" in MAIN,
        "kesfet istek sonucunu dikkate aliyor")
require("if(!gonderildi)" in MAIN and "Bu hesabı zaten takip ediyorsun." in MAIN,
        "kesfette sahte basarili takip bildirimi engeli")
require("final hedefTakipcileri=List<String>.from(v['followers']??const[]);" in MAIN,
        "profilde hedef takipci listesi")
require("final takipte=benimTakipEttiklerim.contains(uid)||(me!=null&&hedefTakipcileri.contains(me));" in MAIN,
        "profil takip durumu iki tarafli")
require("final hedefArkadaslari=List<String>.from(v['friends']??const[]);" in MAIN,
        "profilde hedef arkadas listesi")
require("final arkadas=benimArkadaslarim.contains(uid)||(me!=null&&hedefArkadaslari.contains(me));" in MAIN,
        "profil arkadaslik durumu iki tarafli")
require("final ayniBekleyen=<QueryDocumentSnapshot<Map<String,dynamic>>>[]" in MAIN,
        "kabul/red sirasinda yinelenen istek temizligi")
require("for(final istek in ayniBekleyen)" in MAIN,
        "tum ayni bekleyen isteklerin tek sonuca alinmasi")
require("limit(20).snapshots()" in MAIN,
        "profil istek akisini kullanici ciftiyla sinirlama")

print("Build 296 takip ve arkadaslik istekleri dogrulandi.")
