"""Connect translated presentation labels without changing persisted enum values or user text."""
import json,re
from pathlib import Path
from apply_build438_screen_locales import localize,literal
langs='tr en de ar ru ku zh hi fr es it pt'.split()
rows=[line.split('|') for line in Path('tools/build442_locales.txt').read_text().splitlines() if line]
assert all(len(row)==12 and all(row) for row in rows)
assert len({row[0] for row in rows})==len(rows)
data={row[0].replace(r'\n','\n'):{k:v.replace(r'\n','\n') for k,v in zip(langs[1:],row[1:])} for row in rows}
p=Path('app/lib/main.dart');s=p.read_text();assert '// Build442 locales' not in s
known=set(data)
for name in ['_ngelx438ScreenTranslations','_ngelx440Translations','_ngelx441Translations']:
 match=re.search(r'const '+name+r'\s*=.*?(\{.*\});',s)
 known.update(json.loads(match[1].replace(r'\$','$')))
a=s.index('const ceviriler');b=s.index('String t(',a)
known.update(x.replace("\\'","'").replace(r'\n','\n') for x in re.findall(r"'tr'\s*:\s*'((?:\\.|[^'\\])*)'",s[a:b]))
s=s.replace("final store=_ngelx441Translations[text]?[language];","final release=_ngelx442Translations[text]?[language];\n  if(release!=null)return release;\n  final store=_ngelx441Translations[text]?[language];",1)
s=s.replace("final store=_ngelx441Translations[tr]?[uygulamaDili.value];","final release=_ngelx442Translations[tr]?[uygulamaDili.value];\n  if(release!=null)return release;\n  final store=_ngelx441Translations[tr]?[uygulamaDili.value];",1)
start=s.index('String tercihBasligi');body,count=localize(s[start:],known);s=s[:start]+body
# These named helper parameters are labels. Profile names, text controllers and enum IDs stay untouched.
for marker in ['Widget _finalUretKart(', 'Widget _finalUretSekme(', 'Widget _finalUretArac(', 'Widget _secenek(', 'Widget _profilKucukOnizleme(']:
 a=s.index(marker);b=s.find('\n  ',a+len(marker))
 # Locate next method declaration rather than the first body line.
 m=re.search(r'\n  (?:Widget|Future|InputDecoration|void|String) ',s[a+len(marker):])
 b=a+len(marker)+m.start() if m else len(s)
 region=s[a:b]
 for label in ['ad','aciklama','baslik','alt','yazi']:
  region=region.replace('Text('+label+',','Text(_ngelx438Ui('+label+'),')
 s=s[:a]+region+s[b:]
s=s.replace('labelText:baslik,filled:','labelText:_ngelx438Ui(baslik),filled:')
s=s.replace("Text('$count bekleyen mesaj isteği')","Text(_ngelx438Ui('{count} bekleyen mesaj isteği').replaceAll('{count}',count.toString()))")
s+='\n// Build442 locales\nconst _ngelx442Translations=<String,Map<String,String>>'+literal(data)+';\n'
p.write_text(s)
for p in Path('app/lib').glob('*.dart'):
 if p.name=='main.dart' or not p.read_text().startswith("part of 'main.dart';"):continue
 text=p.read_text()
 if p.name=='build258_settings.dart':
  text=text.replace('title:Text(a,','title:Text(_ngelx438Ui(a),').replace('subtitle:Text(s)','subtitle:Text(_ngelx438Ui(s))').replace('title:Text(e.$2)','title:Text(_ngelx438Ui(e.$2))')
 text,n=localize(text,known);count+=n;p.write_text(text)
print('Build442:',len(rows),'complete 12-language rows;',count,'presentation literals connected')
