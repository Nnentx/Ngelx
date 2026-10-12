from pathlib import Path
import json,re
from apply_build438_screen_locales import tokens
s=Path('app/lib/main.dart').read_text()
for p in Path('app/lib').glob('*.dart'):tokens(p.read_text())
m=re.search(r'const _ngelx442Translations=.*?(\{.*\});',s)
data=json.loads(m[1].replace(r'\$','$'));assert len(data)==32
langs=set('en de ar ru ku zh hi fr es it pt'.split())
assert all(set(values)==langs and all(values.values()) for values in data.values())
for marker in ['Widget _finalUretKart(', 'Widget _finalUretSekme(', 'Widget _finalUretArac(', 'Widget _secenek(', 'Widget _profilKucukOnizleme(']:
 a=s.index(marker);m=re.search(r'\n  (?:Widget|Future|InputDecoration|void|String) ',s[a+len(marker):]);b=a+len(marker)+m.start() if m else len(s)
 block=s[a:b]
 assert '_ngelx438Ui(' in block,marker
 for label in ['ad','aciklama','baslik','alt','yazi']:assert 'Text('+label+',' not in block,marker
assert "_ngelx438Ui('{count} bekleyen mesaj isteği').replaceAll('{count}',count.toString())" in s
assert 'Text(_ad.text,' in s and 'Text(_bio.text,' in s
settings=Path('app/lib/build258_settings.dart').read_text()
assert "_bool('reviewTagsBeforeProfile',v)" in settings
assert "_str('sensitiveContentLevel',v)" in settings
assert 'title:Text(_ngelx438Ui(a),' in settings
assert 'title:Text(_ngelx438Ui(e.$2))' in settings
print('Build442 12-language video labels, display helpers, dynamic count and stored-value boundaries passed')
