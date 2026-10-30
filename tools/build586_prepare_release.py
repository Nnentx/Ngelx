"""Promote the exact Build586 APK already verified and delivered for review."""
from pathlib import Path
import hashlib
import json
import zipfile

files=list(Path('verified-apk').rglob('*.apk'))
assert len(files)==1,'Expected one tested APK'
raw=files[0].read_bytes()
digest=hashlib.sha256(raw).hexdigest()
assert len(raw)==50221561,'APK size differs from the reviewed artifact'
assert digest=='b1a4e85d75fcaea97e4ac77106a571a328c054cab8efe41627001e23c7dd0f0c','APK differs from the reviewed artifact'
with zipfile.ZipFile(files[0]) as archive:
    assert archive.testzip() is None
    assert 'lib/arm64-v8a/libapp.so' in archive.namelist()
    assert 'assets/flutter_assets/AssetManifest.bin' in archive.namelist()
name='NgelX-1.0.356-Build586.apk'
Path(name).write_bytes(raw)
Path(name+'.sha256').write_text(digest+'  '+name+'\n')
feed={
    'schema':1,'package':'com.nnentx.ngelx_app','abi':'arm64-v8a',
    'version':'1.0.356','build':586,'size':len(raw),'sha256':digest,
    'url':'https://github.com/Nnentx/Ngelx/releases/download/v1.0.356-build586/'+name,
    'notes':'Ludo GO düğmesinde tek dokunuş yeterlidir. Başlangıç zar hakları otomatik işlenir ve sonuçlar gösterilir. Dokunma alanı genişletildi; gecikme ve durum çakışmalarında basışın kaybolması düzeltildi. Tasarım ve oyun kuralları korundu.',
    'testedSource':'c4ac01363a19a842a21a63043f9334df9b786853',
    'buildRun':41118732958,
}
Path('android-update.json').write_text(json.dumps(feed,ensure_ascii=False,indent=2)+'\n')
Path('release-notes.md').write_text('NgelX 1.0.356 / Build586\n\n'+feed['notes']+'\n\n184 sunucu testi, 77 uygulama testi, referans ekran kontrolleri, Android derlemesi ve mevcut imza doğrulandı. Gerçek telefonda dokunma kontrolü bekleniyor.\n\nMevcut uygulamanın üzerine güncellenir.\n')
print('Exact reviewed Build586 APK verified:',len(raw),digest)
