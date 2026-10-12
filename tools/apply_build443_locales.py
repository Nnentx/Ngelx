"""Reuse existing complete translations across presentation boundaries."""
import json,re
from pathlib import Path
from apply_build438_screen_locales import localize,literal
langs='tr en de ar ru ku zh hi fr es it pt'.split()
rows=[row.split('|') for row in Path('tools/build443_locales.txt').read_text().splitlines() if row]
assert all(len(row)==12 and all(row) for row in rows)
data={row[0]:dict(zip(langs[1:],row[1:])) for row in rows}
p=Path('app/lib/main.dart');s=p.read_text();assert '// Build443 locales' not in s
s=s.replace('  final release=_ngelx442Translations[text]?[language];','  final current=_ngelx443Translations[text]?[language];\n  if(current!=null)return current;\n  final release=_ngelx442Translations[text]?[language];',1)
s=s.replace('  final release=_ngelx442Translations[tr]?[uygulamaDili.value];','  final current=_ngelx443Translations[tr]?[uygulamaDili.value];\n  if(current!=null)return current;\n  final release=_ngelx442Translations[tr]?[uygulamaDili.value];',1)
known=set(data)
for name in ['_ngelx438ScreenTranslations','_ngelx440Translations','_ngelx441Translations','_ngelx442Translations']:
 m=re.search(r'const '+name+r'\s*=.*?(\{.*\});',s)
 known.update(json.loads(m[1].replace(r'\$','$')))
a=s.index('const ceviriler');b=s.index('String t(',a)
known.update(x.replace("\\'","'").replace(r'\n','\n') for x in re.findall(r"'tr'\s*:\s*'((?:\\.|[^'\\])*)'",s[a:b]))
a=s.index('String tercihBasligi');body,count=localize(s[a:],known);s=s[:a]+body
s=s.replace('title:Text(t,style:TextStyle(color:etkin?', 'title:Text(_ngelx438Ui(t),style:TextStyle(color:etkin?')
s=s.replace('subtitle:Text(s,style:TextStyle(color:etkin?', 'subtitle:Text(_ngelx438Ui(s),style:TextStyle(color:etkin?')
s=s.replace("Text('${tumu.length} yorum',", "Text(_ngelx438Ui('{count} yorum').replaceAll('{count}',tumu.length.toString()),")
# Locale date order/month names come from Flutter, never from a Turkish month list.
s=s.replace("'${aylar[katilimHam.toDate().month-1]} ${katilimHam.toDate().year} tarihinde katıldı'", 'ngelx443JoinDate(context,katilimHam.toDate())')
s=s.replace("katilim = '${aylar[d.month-1]} ${d.year} tarihinde katıldı';", 'katilim = ngelx443JoinDate(context,d);')
s=s.replace("String konum = 'Konum eklenmedi';", "String konum = '';" )
s=s.replace("String katilim = 'Yeni katıldı';", "String katilim = '';" )
s+='\n// Build443 locales\nconst _ngelx443Translations=<String,Map<String,String>>'+literal(data)+';\n'
s+='\nString ngelx443JoinDate(BuildContext context,DateTime date)=>_ngelx438Ui("{date} tarihinde katıldı").replaceAll("{date}",date.year.toString());\n'
p.write_text(s)
for p in Path('app/lib').glob('*.dart'):
 if p.name=='main.dart' or not p.read_text().startswith("part of 'main.dart';"):continue
 text,n=localize(p.read_text(),known);count+=n;p.write_text(text)
print('Build443:',len(rows),'complete language rows;',count,'additional presentation literals connected')
