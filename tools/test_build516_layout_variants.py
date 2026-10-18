#!/usr/bin/env python3
"""Preflight Build516 Keşfet header variants without Flutter/Android setup.

These are TEXT-transform fixture tests, not fake Dart build passes. They catch
brittle matching before the costly 200-step integration workflow.
"""
import importlib.util

spec=importlib.util.spec_from_file_location(
    "build516", "tools/apply_build516_global_live_search.py")
assert spec and spec.loader
patch=importlib.util.module_from_spec(spec)
spec.loader.exec_module(patch)

def fixture(header):
    return """part 'live_feed_card.dart';
class MockKesfet {
  Future<void> _yayinIzle(BuildContext context, Map<String, dynamic> veri, String belgeId) async {
    final source = lk.DevelopmentTokenSource(id: 'not-for-production');
  }

  void _aramaAc(){}
  Widget build(BuildContext context){
    final mock=[
"""+header+"""
      onTap:_aramaAc,
      onPressed:_filtreAc,
      _kesfetSekmesi(Icons.live_tv_rounded,t('live'),0),
          if(kategori==0)..._canliSliverleri(),
    ];
  }

  List<Widget> _canliSliverleri({bool trend=false})=>[
    onTap:()=>_yayinIzle(context,y,yayinlar[i].id),
  ];
}
"""

variants={
    "old title and spacer": """              Text(t('explore'),style:const TextStyle(color:Colors.black,fontSize:29,fontWeight:FontWeight.w900)),
              const Spacer(),
              IconButton(tooltip:t('filter'),onPressed:_filtreAc,icon:const Icon(Icons.tune_rounded)),
""",
    "generated alternate title": """              ExploreHeading(label:t('explore')),
              const Spacer(),
              IconButton(onPressed:_filtreAc,icon:const Icon(Icons.tune_rounded)),
""",
    "no spacer title": """              Text(t('explore'),style:const TextStyle(fontSize:27)),
              IconButton(onPressed:_filtreAc,icon:const Icon(Icons.tune_rounded)),
""",
}
for label,header in variants.items():
    original=fixture(header)
    result=patch.transform(original)
    assert result!=original, 'No transform applied: '+label
    assert patch.transform(result)==result, 'Non-idempotent: '+label
    assert result.count(patch.MARK)==1, 'Marker duplicated: '+label
    assert result.count("onPressed:()=>ngelxCanliAramaAc(context)")==2, (
        "Expected global and section search: "+label)
    assert "label:const Text('Canlı ara')" in result
    assert "await ngelxCanliYayinaKatil(context,belgeId);" in result
    assert "onTap:()=>ngelxCanliYayinaKatil(context,yayinlar[i].id)," in result
    assert "lk.DevelopmentTokenSource(" not in result
    assert "onTap:_aramaAc" in result
    assert "onPressed:_filtreAc" in result
    print('Build516 fixture PASS:',label)
print('Build516 preflight PASS: old and generated layouts, empty live card, secure shared join')
