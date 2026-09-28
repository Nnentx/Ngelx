#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN=(ROOT/'app/lib/main.dart').read_text(encoding='utf-8')
PUB=(ROOT/'app/pubspec.yaml').read_text(encoding='utf-8')

def require(c,m):
    if not c:
        raise SystemExit('Build 302 Firestore tutarlılık kontrolu eksik: '+m)

require('version: 1.0.83+302' in PUB,'Build 302 sürümü')
require("defaultValue: '1.0.83'" in MAIN and "defaultValue: '302'" in MAIN,'uygulama içi sürüm')

require('Future<void> ngelxBatchCommitDogrula({' in MAIN,
        'belirsiz timeout sonrası mesaj belgesiyle commit doğrulama')
require("GetOptions(source:Source.server)" in MAIN and
        "marker.get(const GetOptions(source:Source.server))" in MAIN,
        'sunucudan commit marker doğrulaması')
require(MAIN.count('ngelxBatchCommitDogrula(')>=5,
        'grup/özel mesaj ve medya batch commit doğrulaması')

notify_start=MAIN.index('Future<void> uygulamaBildirimiGonder({')
notify_end=MAIN.index('final Set<String> _sosyalIstekIslemleri',notify_start)
notify=MAIN[notify_start:notify_end]
require('String? dedupeKey' in notify,'bildirim dedupe anahtarı')
require('ngelxBildirimBelgeId' in notify,'güvenli deterministik bildirim belge kimliği')
require("if(mevcut.exists)return;" in notify,'mevcut bildirimi yeniden oluşturmama')
require("doc.set(payload)" in notify,'deterministik bildirim yazımı')

require("dedupeKey:'group_msg_" in MAIN,'grup mesajı bildirim tekilleştirme')
require("dedupeKey:'private_msg_" in MAIN,'özel mesaj bildirim tekilleştirme')
require("dedupeKey:'private_photo_" in MAIN,'özel fotoğraf bildirim tekilleştirme')
require("dedupeKey:'private_extra_" in MAIN,'özel medya/dosya bildirim tekilleştirme')
require("dedupeKey:'group_mention_" in MAIN,'grup mention bildirim tekilleştirme')

print('Build 302 mesaj/bildirim çift kayıt ve timeout tutarlılığı doğrulandı.')
