from pathlib import Path
from apply_build438_screen_locales import tokens
s=Path('app/lib/main.dart').read_text()
a=s.index('class _ArsivSohbetlerPageState');b=s.index('class MesajIstekleriPage',a);archive=s[a:b]
assert "'dismissedArchiveChats':FieldValue.arrayUnion([id])" in archive
assert ".collection('chats').doc(id).set(" not in archive
assert ".where('highlighted',isEqualTo:true).limit(30)" in s
assert "if(ngelxPlayRelease441)throw StateError" in s
for p in Path('app/lib').glob('*.dart'):
 source=p.read_text();tokens(source)
 if p.name!='main.dart':assert 'DevelopmentTokenSource' not in source
rows=[r.split('|') for r in Path('tools/build441_locales.txt').read_text().splitlines()]
assert all(len(r)==12 and all(r) for r in rows)
settings=Path('app/lib/build258_settings.dart').read_text();assert '{3,30}' not in settings and 'controller:kullanici,maxLength:30' not in settings
print('Build441 token-aware source checks, twelve-language rows, username boundary and production guard passed')
