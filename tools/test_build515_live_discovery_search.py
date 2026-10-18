#!/usr/bin/env python3
"""Build515 QA: active live search, safe legacy join, no backend mutations."""
import importlib.util
from pathlib import Path

spec=importlib.util.spec_from_file_location('build515','tools/apply_build515_live_discovery_search.py')
assert spec and spec.loader
patch=importlib.util.module_from_spec(spec)
spec.loader.exec_module(patch)

source=Path('app/lib/live_feed_card.dart').read_text(encoding='utf-8')
assert patch.transform(source)==source, 'Build515 UI must be idempotent'
a=source.index(patch.MARK)
b=source.index('class NgelXAkisCanliKarti extends StatelessWidget{',a)
search=source[a:b]
for needle in (
    "Future<void> ngelxCanliAramaAc(BuildContext context) async",
    "showModalBottomSheet<String>",
    "isScrollControlled:true",
    "final selected=await",
    "if(selected==null||selected.isEmpty||!context.mounted)return;",
    "ngelxCanliYayinaKatil(context,selected);",
    "State<_NgelxCanliAramaSheet515>",
    "late final Stream<QuerySnapshot<Map<String,dynamic>>> _activeRooms515=",
    "where('active',isEqualTo:true).limit(60).snapshots()",
    "stream:_activeRooms515",
    "ngelxCanliKaydiTaze(data)",
    "onChanged:(_)=>setState((){})",
    "maxLength:70",
    "onPressed:(){_search515.clear();setState((){});}",
    "title.contains(needle)",
    "username.contains(",
    "needle.startsWith('@')?needle.substring(1):needle",
    "onTap:()=>Navigator.pop(context,d.id)",
    "if(snapshot.hasError)",
    "if(!snapshot.hasData)",
    "rooms.isEmpty",
    "İlk 60 aktif yayında arama",
    "Canlı yayınlar yüklenemedi",
    "_search515.dispose();",
):
    assert needle in search, 'Build515 missing live search query/UI safety: '+needle
for forbidden in ('.set(','.update(','.delete(','.runTransaction(','.add(','.signIn(','.disconnect('):
    assert forbidden not in search, 'Build515 discovery must not modify backend or call session: '+forbidden
for preserved in (
    "part of 'main.dart';",
    "class NgelXCanliTakipButonu extends StatefulWidget",
    "class NgelXAkisCanliKarti extends StatelessWidget",
    "onTap:canli?()=>ngelxCanliYayinaKatil(context,liveId)",
    "onPressed:()=>ngelxCanliAramaAc(context)",
    "tooltip:'Canlı yayın ara'",
    "if(canli)NgelXCanliTakipButonu(ownerId:owner)",
    "ngelxCanliTrendPuani(",
):
    assert preserved in source, 'Build515 changed existing Keşfet card: '+preserved
assert source.count(patch.MARK)==1
assert source.count("onPressed:()=>ngelxCanliAramaAc(context)")==1
assert source.count("onTap:()=>Navigator.pop(context,d.id)")==1
print('Build515 SOURCE PASS: active streams filtered by title/username, bounded to 60 and updated live')
print('Build515 SOURCE PASS: safe legacy join path, no backend writes, existing cards/follows untouched')
print('Build515 LIMIT: active search is scoped to 60 returned rooms; full indexed multi-page discovery and two-phone QA pending')
