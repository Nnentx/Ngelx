import json,re
from pathlib import Path
from apply_build438_screen_locales import localize,literal,tokens
langs='tr en de ar ru ku zh hi fr es it pt'.split()
rows=[line.split('|') for line in Path('tools/build440_locales.txt').read_text().splitlines() if line]
assert all(len(row)==12 and all(row) for row in rows)
data={row[0]:dict(zip(langs[1:],row[1:])) for row in rows}
# Case variants are visual labels, not stored filters or enum values.
for row in rows:
 for name in [row[0].lower(),row[0].upper()]:
  if name not in data:data[name]=data[row[0]]
data['Görüntülü grup araması']=data['Görüntülü Grup Araması']
data['NgelX Görüntü Stüdyosu']={k:'NgelX '+v for k,v in data['Görüntü Stüdyosu'].items()}
p=Path('app/lib/main.dart');s=p.read_text()
if '// Build440 locales' in s:raise SystemExit('Build440 locales already applied')
a=s.index('const ceviriler =');b=s.index('String t(String',a)
known=set(re.findall(r"'tr'\s*:\s*'((?:\\.|[^'\\])*)'",s[a:b]));known={v.replace("\\'","'").replace('\\n','\n') for v in known}
known.update(data)
known.update(json.loads(s[s.index('const _ngelx438ScreenTranslations'):].split('>>',1)[1].split(';',1)[0]))
s=s.replace("final newer=_ngelx439Translations[text]?[language];","final device=_ngelx440Translations[text]?[language];\n  if(device!=null)return device;\n  final newer=_ngelx439Translations[text]?[language];")
s=s.replace("// Build438 extra inline translations","final device=_ngelx440Translations[tr]?[uygulamaDili.value];\n  if(device!=null)return device;\n  // Build438 extra inline translations",1)
start=s.index('String tercihBasligi');body,count=localize(s[start:],known);s=s[:start]+body
# Helpers receive untranslated labels because their values also select routes/filters.
for name in ['etiket','follow?\'Takip istekleri\':\'Arkadaşlık istekleri\'']:
 pass
# Wrap only known presentation helper variables; never user names, posts or messages.
for anchor in ['Widget _kesfetSekmesi(', 'Widget _aramaKontrol(', 'Widget _efektChip(', 'Widget sekme(']:
 if anchor in s:
  a=s.index(anchor)
  ts=tokens(s[a:]);pairs={};stack=[]
  for i,(token,_,_) in enumerate(ts):
   if token in ('(','[','{'):stack.append(i)
   elif token in (')',']','}'):
    if stack:opened=stack.pop();pairs[opened]=i
  formal=next(i for i,t in enumerate(ts) if t[0]=='(')
  j=pairs[formal]+1
  if ts[j][0]=='{':b=a+ts[pairs[j]][2]
  else:
   assert ts[j][0]=='=' and ts[j+1][0]=='>'
   j+=2
   while ts[j][0]!=';':
    j=pairs[j]+1 if ts[j][0] in ('(','[','{') else j+1
   b=a+ts[j][2]
  if b>0:
   part=s[a:b]
   for var in (['ad'] if anchor=='Widget sekme(' else ['etiket','yazi','label']):
    part=part.replace('Text('+var+',','Text(_ngelx438Ui('+var+'),')
   s=s[:a]+part+s[b:]
a=s.index("if(tur=='call'){");b=s.find("if(tur==",a+20);part=s[a:b].replace('Text(baslik,','Text(_ngelx438Ui(baslik),');s=s[:a]+part+s[b:]
s=s.replace("Text('$count bekleyen istek')","Text(_ngelx440Format('{count} bekleyen istek',{'count':count}))")
s=s.replace("Text('$mesajIstek bekleyen mesaj isteği')","Text(_ngelx440Format('{count} bekleyen mesaj isteği',{'count':mesajIstek}))")
s+='\n// Build440 locales\nconst _ngelx440Translations=<String,Map<String,String>>'+literal(data)+';\nString _ngelx440Format(String key,Map<String,Object> values){var text=_ngelx438Ui(key);for(final entry in values.entries){text=text.replaceAll(\"{${entry.key}}\",entry.value.toString());}return text;}\n'
p.write_text(s)
counts={'main.dart':count}
for p in Path('app/lib').glob('*.dart'):
 if p.name=='main.dart' or not p.read_text().startswith("part of 'main.dart';"):continue
 source,n=localize(p.read_text(),known)
 if p.name=='build258_settings.dart':
  for var in ['title','sub','widget.bosMetin','widget.buton']:
   source=source.replace('Text('+var+',','Text(_ngelx438Ui('+var+'),').replace('Text('+var+')','Text(_ngelx438Ui('+var+'))')
 if p.name=='live_broadcast_studio.dart':
  source=source.replace('labelText:etiket,','labelText:_ngelx438Ui(etiket),').replace('Text(gizlilik,','Text(_ngelx438Ui(gizlilik),').replace('Text(etiket,','Text(_ngelx438Ui(etiket),').replace('child:Text(e,','child:Text(_ngelx438Ui(e),')
 p.write_text(source);counts[p.name]=n
print('Build440: localized presentation literals across',counts)
