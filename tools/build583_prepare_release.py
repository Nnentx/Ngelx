"""Promote only the immutable APK that passed Build583 review."""
from pathlib import Path
import hashlib
import json
import os
import zipfile

files=list(Path('verified-apk').rglob('*.apk'))
assert len(files)==1, 'Expected one tested APK'
raw=files[0].read_bytes()
digest=hashlib.sha256(raw).hexdigest()
assert len(raw)==50218877
assert digest=='17b7a7368476a6d1eb7da3536fafb6f8d55fa1bbcbba9144bfb222d5402b6575'
with zipfile.ZipFile(files[0]) as z:
    assert z.testzip() is None
    assert 'lib/arm64-v8a/libapp.so' in z.namelist()
    assert 'assets/flutter_assets/assets/ludo575_home.wav' in z.namelist()
name='NgelX-1.0.353-Build583.apk'
Path(name).write_bytes(raw)
Path(name+'.sha256').write_text(digest+'  '+name+'\n')
feed={
 'schema':1,'package':'com.nnentx.ngelx_app','abi':'arm64-v8a',
 'version':'1.0.353','build':583,'size':len(raw),'sha256':digest,
 'url':'https://github.com/Nnentx/Ngelx/releases/download/v1.0.353-build583/'+name,
 'notes':'Ludo tahtası ve taşların dokunma alanları genişletildi. GO tek basışla çalışır. Hamle süresi 15 saniye oldu; Auto dengelendi. Hediye yazıları okunaklı, hediyeler ekranda hareketlidir. Taş yuva sesleri ve aramaya katılım göstergeleri yenilendi. Özel ve grup davetindeki titreme ile masadan ayrılma çakışmaları düzeltildi.',
 'testedSource':'ffc4dfb7dfcf0716ff8b038f7ce1a7fe11498c4a',
 'buildRun':40743800801,'liveAcceptanceRun':int(os.environ['GITHUB_RUN_ID']),
}
Path('android-update.json').write_text(json.dumps(feed,ensure_ascii=False,indent=2)+'\n')
Path('release-notes.md').write_text('NgelX 1.0.353 / Build583\n\n'+feed['notes']+'\n\n153 sunucu testi, 49 arayüz testi, referans ekranları, Android derlemesi ve mevcut imza doğrulandı. Canlı API kontrolü geçtikten sonra yayımlanır; fiziksel cihaz testi yapılmış sayılmaz.\n\nMevcut uygulamanın üzerine güncellenir.\n')
print('Exact tested Build583 APK verified:',len(raw),digest)
