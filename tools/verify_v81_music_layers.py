#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN=(ROOT/'app/lib/main.dart').read_text(encoding='utf-8')
EDITOR=(ROOT/'app/lib/create_music_editor.dart').read_text(encoding='utf-8')


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit('V81 müzik katmanı kontrolü eksik: '+message)


require('Future<void> _cihazdanSesSec()' in EDITOR,
        'cihazdan ses dosyası seçimi')
require("extensions:['mp3','m4a','aac','wav','ogg']" in EDITOR,
        'desteklenen güvenli ses uzantıları')
require("boyut>15*1024*1024" in EDITOR and "'licenseStatus':'user-owned'" in EDITOR,
        '15 MB sınırı ve kullanım hakkı kaydı')
require("kind:'music'" in MAIN and "'sourceType':'user-upload'" in MAIN,
        'kullanıcı sesinin doğrulanmış medya servisine yüklenmesi')
require("'originalAudioVolume':tur=='video'?orijinalSesSeviyesi:0" in MAIN,
        'orijinal video sesi seviyesinin Firestore kaydı')
require("'musicVolume':yayinMuzik==null?0:muzikSesSeviyesi" in MAIN,
        'müzik ses seviyesinin Firestore kaydı')
require("widget.originalAudioVolume.clamp(0,1)" in MAIN and
        "widget.musicVolume.clamp(0,1)" in MAIN,
        'oynatıcıda iki ayrı ses seviyesinin uygulanması')
require("double.tryParse(widget.veri['musicVolume']??'')" in MAIN,
        'fotoğraflı gönderide müzik seviyesinin uygulanması')
require("if(tur=='video')Row(children:[" in EDITOR and
        "const SizedBox(width:104,child:Text('Müzik sesi'" in EDITOR,
        'üretim ekranı ses karıştırma denetimleri')

print('V81 fotoğraf/video müzik katmanı ve ses seviyeleri doğrulandı.')
