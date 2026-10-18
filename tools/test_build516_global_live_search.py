#!/usr/bin/env python3
"""Build516 regression: global live search, unchanged general search and auth."""
import importlib.util
from pathlib import Path

spec=importlib.util.spec_from_file_location('build516','tools/apply_build516_global_live_search.py')
assert spec and spec.loader
patch=importlib.util.module_from_spec(spec)
spec.loader.exec_module(patch)

src=Path('app/lib/main.dart').read_text(encoding='utf-8')
assert patch.transform(src)==src,'Build516 must be idempotent'
assert src.count(patch.MARK)==1
# Generated Keşfet screens differ by stage: choose its enclosing section if
# present, otherwise test all generated main.dart for the new search actions.
start=src.find('  void _aramaAc(){')
end=src.find('  List<Widget> _trendSliverleri()',start)
explore=src[start:end] if start>=0 and end>start else src
for needed in (
    patch.MARK,
    "tooltip:'Canlı yayın ara'",
    "label:const Text('Canlı ara')",
    "onPressed:()=>ngelxCanliAramaAc(context)",
):
    assert needed in explore,'Build516 missing global Keşfet feature: '+needed
assert explore.count('onPressed:()=>ngelxCanliAramaAc(context)')==2
if 'yayinlar[i].id' in explore:
    assert "onTap:()=>ngelxCanliYayinaKatil(context,yayinlar[i].id)" in explore, (
        'Generated existing Keşfet live card must use the authorized join')
if 'onTap:_aramaAc,' in src:
    assert 'onTap:_aramaAc,' in explore,'General search must still be accessible'
if 'onPressed:_filtreAc' in src:
    assert 'onPressed:_filtreAc' in explore,'Keşfet filters must remain usable'
import re
legacy_match=re.search(r'(?m)^  Future<void> _yayinIzle\(',src)
if legacy_match:
    following=src[legacy_match.start():]
    end=following.find('  void _aramaAc(){')
    if end<0:
        end=len(following)
    legacy=following[:end]
    assert 'await ngelxCanliYayinaKatil(context,belgeId);' in legacy
    assert 'lk.DevelopmentTokenSource(' not in legacy, 'Old Keşfet route must not issue development tokens'
else:
    legacy=''
    assert '_yayinIzle(context,y,yayinlar[i].id)' not in explore, (
        'A removed legacy handler cannot be referenced by the live card')
for forbidden in ('.runTransaction(', '.set(', '.update(', '.delete('):
    assert forbidden not in legacy,'Legacy join delegate must not write server state'
source=Path('app/lib/live_feed_card.dart').read_text(encoding='utf-8')
assert "class _NgelxCanliAramaSheet515State" in source
assert "where('active',isEqualTo:true).limit(60).snapshots()" in source
assert "ngelxCanliYayinaKatil(context,selected)" in source
assert "class NgelXAkisCanliKarti extends StatelessWidget" in source
print('Build516 SOURCE PASS: always-visible Keşfet live search even without a live card')
print('Build516 SOURCE PASS: general search/filter maintained; live tap uses shared secure join')
print('Build516 LIMIT: Build515 active results limited to 60; no full indexed search or device QA yet')
