#!/usr/bin/env python3
"""Build512 read-only gift-history pager, previous live features preserved."""
import importlib.util
from pathlib import Path

spec=importlib.util.spec_from_file_location('build512','tools/apply_build512_gift_history.py')
assert spec and spec.loader
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

source=Path('app/lib/live_broadcast_studio.dart').read_text(encoding='utf-8')
assert mod.transform(source)==source, 'Build512 must be idempotent'
view=source[source.index('class _CanliYayinPageState'):source.index('class _CanliOzetSatiri')]
start=view.index('  // Build512: paged read-only gift history.')
end=view.index('  Future<void> _hediyePaneli() async {',start)
history=view[start:end]
for required in (
  mod.MARK,
  "orderBy('createdAt',descending:true).limit(50).get()",
  "startAfterDocument(last!).limit(50).get()",
  "d.data()['kind']=='gift'",
  "gifts.addAll(page.docs.where(",
  'Daha eski hediyeleri getir',
  'Gönderen · Hediye · Adet · Zaman',
  "onPressed:loading?null:moreGifts",
  'Hediye kaydı bulunamadı.',
  'created is Timestamp',
  "final qty=((d['quantity'] as num?)?.toInt()??1).clamp(1,10)",
  'if(c.mounted)refresh(()=>loading=false);',
):
  assert required in history, 'Missing pagination/read-only behavior: '+required
assert ".add(" not in history, 'History must not write new events'
for forbidden in ('.set(','.update(','.delete(','.runTransaction(','.disconnect(',
                  '.setCameraEnabled(','.setMicrophoneEnabled('):
  assert forbidden not in history, 'History mutates app state/server: '+forbidden
for preserved in (
  '_giftScreen511()',
  '_newCommentChip510()',
  '_guestRail488()',
  '_yorumYonet(d.id,y)',
  '_yayinKamerasiniAcKapat',
  '_kalpDegistir()',
  'Hediye adedi',
  "'giftCount'",
  'onTap:_giftHistory512',
  "label:'Toplam hediye $n, geçmişi aç'",
):
  assert preserved in view, 'Build512 lost existing feature: '+preserved
assert source.count(mod.MARK)==1
print('Build512 SOURCE PASS: cursor paging, 50 events per page, gift-only display and timestamps')
print('Build512 SOURCE PASS: history is read only; live/gifts/comments/camera controls preserved')
print('Build512 LIMIT: Flutter/Android device and large gift-history QA pending')
