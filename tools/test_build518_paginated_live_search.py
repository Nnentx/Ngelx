#!/usr/bin/env python3
"""Build518 contract: every active page can be scanned with Firestore cursors."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('b518','tools/apply_build518_paginated_live_search.py')
assert spec and spec.loader
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
src=Path('app/lib/live_feed_card.dart').read_text(encoding='utf-8')
assert mod.transform(src)==src,'Build518 must be idempotent'
assert src.count(mod.MARK)==1
a=src.index(mod.MARK)
b=src.index('class NgelXAkisCanliKarti extends StatelessWidget{',a)
s=src[a:b]
for term in (
    'final Map<String,QueryDocumentSnapshot<Map<String,dynamic>>> _pages518={}',
    '_scanDelay518?.cancel();',
    'const Duration(milliseconds:500)',
    'if(_scanRunning518||_scanStarted518)return',
    "where('active',isEqualTo:true)",
    'orderBy(FieldPath.documentId).limit(60)',
    'query.startAfterDocument(cursor)',
    'final page=await query.get()',
    'if(docs.length<60)',
    'cursor=docs.last',
    'while(mounted)',
    "_pages518[d.id]=d",
    'if(needle.isNotEmpty)..._pages518',
    'ngelxCanliKaydiTaze(data)',
    'title.contains(needle)||username.contains(term)',
    "onTap:()=>Navigator.pop(context,d.id)",
    'if(!mounted)return;',
    'if(needle.isNotEmpty&&_scanRunning518)',
    '_scanError518',
    '_retry518()',
):
    assert term in s,'Build518 missing '+term
for unsafe in ('.set(','.update(','.delete(','.runTransaction(','.disconnect(','.DevelopmentTokenSource('):
    assert unsafe not in s,'Search must remain read-only: '+unsafe
assert 'İlk 60 aktif yayında arama' not in s,'Outdated misleading label'
assert "ngelxCanliYayinaKatil(context,selected);" in src, 'Join uses verified permission path'
assert "class NgelXAkisCanliKarti extends StatelessWidget" in src
print('Build518 SOURCE PASS: pages cursor through all active stream IDs on explicit search, not 60-only')
print('Build518 SOURCE PASS: single scan per sheet, debounce input, stale guard, error/retry, auth join')
print('Build518 LIMIT: on-device/full-data integration and server-side search index unverified')
