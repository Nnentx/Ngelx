import json,re
from pathlib import Path
from apply_build438_screen_locales import localize,literal
langs='tr en de ar ru ku zh hi fr es it pt'.split()
rows=[l.split('|') for l in Path('tools/build441_locales.txt').read_text().splitlines() if l]
assert all(len(r)==12 and all(r) for r in rows)
assert len({r[0] for r in rows})==len(rows)
data={r[0]:dict(zip(langs[1:],r[1:])) for r in rows}
p=Path('app/lib/main.dart');s=p.read_text();assert '// Build441 locales' not in s
s=s.replace("final device=_ngelx440Translations[text]?[language];", "final store=_ngelx441Translations[text]?[language];\n  if(store!=null)return store;\n  final device=_ngelx440Translations[text]?[language];",1)
s=s.replace("final device=_ngelx440Translations[tr]?[uygulamaDili.value];", "final store=_ngelx441Translations[tr]?[uygulamaDili.value];\n  if(store!=null)return store;\n  final device=_ngelx440Translations[tr]?[uygulamaDili.value];",1)
a=s.index('const ceviriler =');b=s.index('String t(String',a)
known=set(re.findall(r"'tr'\s*:\s*'((?:\\.|[^'\\])*)'",s[a:b]));known={x.replace("\\'","'").replace('\\n','\n') for x in known};known.update(data)
start=s.index('String tercihBasligi');body,n=localize(s[start:],known);s=s[:start]+body
s+='\n// Build441 locales\nconst _ngelx441Translations=<String,Map<String,String>>'+literal(data)+';\n';p.write_text(s)
for p in Path('app/lib').glob('*.dart'):
 if p.name=='main.dart' or not p.read_text().startswith("part of 'main.dart';"):continue
 src,n=localize(p.read_text(),known)
 if p.name=='build258_settings.dart':
  src=src.replace('title:Text(a,','title:Text(_ngelx438Ui(a),').replace('subtitle:Text(s)','subtitle:Text(_ngelx438Ui(s))').replace('title:Text(e.$2)','title:Text(_ngelx438Ui(e.$2))').replace('Text(widget.baslik)','Text(_ngelx438Ui(widget.baslik))')
  src=src.replace("bottom:const TabBar(","bottom:TabBar(").replace("Tab(text:'Engellenen')","Tab(text:_ngelx438Ui('Engellenen'))").replace("Tab(text:'Kısıtlanan')","Tab(text:_ngelx438Ui('Kısıtlanan'))")
  src=src.replace('^[a-z0-9_.]{3,30}$','^[a-z0-9_.]{3,20}$').replace('controller:kullanici,maxLength:30','controller:kullanici,maxLength:20')
 p.write_text(src)
print('Build441 added',len(rows),'complete twelve-language rows; translated presentation only')
