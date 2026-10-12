from pathlib import Path
import json,re
from apply_build438_screen_locales import tokens
s=Path('app/lib/main.dart').read_text()
for p in Path('app/lib').glob('*.dart'):tokens(p.read_text())
data=json.loads(re.search(r'const _ngelx443Translations=.*?(\{.*\});',s)[1].replace(r'\$','$'))
assert len(data)==48
assert all(set(v)==set('en de ar ru ku zh hi fr es it pt'.split()) and all(v.values()) for v in data.values())
assert s.count('child:_buildProfile(context)')==2
assert "set({'allowProfileCapture':value},SetOptions(merge:true))" in s
assert 'title:Text(_ngelx438Ui(t),style:TextStyle(color:etkin?' in s
guard=Path('app/lib/build443_capture_guard.dart').read_text()
assert '!snapshot.metadata.isFromCache' in guard and '!snapshot.metadata.hasPendingWrites' in guard
assert 'revision == _policyRevision' in guard
native=Path('app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt').read_text()
assert 'if (captureLeases.isNotEmpty())' in native
assert 'window.addFlags(WindowManager.LayoutParams.FLAG_SECURE)' in native
assert 'window.clearFlags(WindowManager.LayoutParams.FLAG_SECURE)' in native
print('Build443 generated sources, locale completeness and capture integration passed; widget/native build checks run in CI')
