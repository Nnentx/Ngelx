#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN=(ROOT/'app/lib/main.dart').read_text(encoding='utf-8')
PUB=(ROOT/'app/pubspec.yaml').read_text(encoding='utf-8')

def require(c,m):
    if not c:
        raise SystemExit('Build 302 birleşik fotoğraf hattı eksik: '+m)

require('version: 1.0.83+302' in PUB,'Build 302 sürümü')
require("defaultValue: '1.0.83'" in MAIN and "defaultValue: '302'" in MAIN,'uygulama içi sürüm')

for kind in ('profiles','groups','stories','chat-backgrounds','support'):
    require(("kind:'"+kind+"'") in MAIN or ("kind: '"+kind+"'") in MAIN,
            kind+' medya türü')

require('Future<String> ngelxFotografYukle({' in MAIN,
        'ortak fotoğraf file+fallback yardımcısı')
require(MAIN.count('ngelxFotografYukle(')>=9,
        'kritik fotoğraf akışlarının ortak yardımcısı')

profile_start=MAIN.index("final yol = 'profiles/")
profile_end=MAIN.index("await FirebaseFirestore.instance.collection('users').doc(user.uid).set",profile_start)
require('ngelxFotografYukle(' in MAIN[profile_start:profile_end] and
        ('dosya:dosya' in MAIN[profile_start:profile_end] or 'dosya: dosya' in MAIN[profile_start:profile_end]),
        'profil fotoğrafı ortak yüklemesi')

group_avatar=MAIN.index("avatar_")
require('ngelxFotografYukle(' in MAIN[group_avatar:group_avatar+1200],
        'grup avatarı ortak yüklemesi')

create_story=MAIN.index("Future<void> _hikayePaylas")
create_story_end=MAIN.index("Future<void> _videoDuzenle",create_story)
story_block=MAIN[create_story:create_story_end]
require("await ngelxMedyaYukleDosya(dosya:dosya,kind:'stories'" in story_block,
        'Üret hikâye foto/video ortak dosya hattı')
require('ngelxMedyaYukleBytes(' not in story_block,
        'Üret hikâyede eski bytes fotoğraf hattının kaldırılması')

profile_story=MAIN.index("Future<void> hikayeYukle() async")
profile_story_end=MAIN.index("Future<void> hikayeyiAc()",profile_story)
profile_story_block=MAIN[profile_story:profile_story_end]
require("await ngelxMedyaYukleDosya(" in profile_story_block and "kind:'stories'" in profile_story_block,
        'profil hikâye ortak dosya hattı')
require('ngelxMedyaYukleBytes(' not in profile_story_block,
        'profil hikâyede eski bytes fotoğraf hattının kaldırılması')

require("final bytes=await foto!.readAsBytes()" not in MAIN,
        'grup oluştururken gereksiz tam bellek fotoğraf okumasının kaldırılması')
require("bytes:await ekran!.readAsBytes()" not in MAIN,
        'destek ekran görüntüsünde gereksiz bytes yolu kaldırılması')

print('Build 302 profil/grup/hikâye/arka plan/destek fotoğraf hattı doğrulandı.')
