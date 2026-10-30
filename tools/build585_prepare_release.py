"""Promote the exact Build585 APK already verified and delivered for review."""
from pathlib import Path
import hashlib
import json
import zipfile

files=list(Path('verified-apk').rglob('*.apk'))
assert len(files)==1,'Expected one tested APK'
raw=files[0].read_bytes()
digest=hashlib.sha256(raw).hexdigest()
assert len(raw)==50220533,'APK size differs from the reviewed artifact'
assert digest=='a2bfe028ab4f63c1b44a36083081c89827793a92575fb404cc3d5a3e6f26eb7d','APK differs from the reviewed artifact'
with zipfile.ZipFile(files[0]) as archive:
    assert archive.testzip() is None
    assert 'lib/arm64-v8a/libapp.so' in archive.namelist()
    assert 'assets/flutter_assets/AssetManifest.bin' in archive.namelist()
name='NgelX-1.0.355-Build585.apk'
Path(name).write_bytes(raw)
Path(name+'.sha256').write_text(digest+'  '+name+'\n')
feed={
    'schema':1,'package':'com.nnentx.ngelx_app','abi':'arm64-v8a',
    'version':'1.0.355','build':585,'size':len(raw),'sha256':digest,
    'url':'https://github.com/Nnentx/Ngelx/releases/download/v1.0.355-build585/'+name,
    'notes':'Ludo taşları hızlandırıldı. Yalnızca bir taş oynanabiliyorsa hamle otomatik yapılır. Büyük zar/GO, geri sayım ve hazır mesaj butonları gizlendi; oyuncu yanındaki zar, Auto ve sohbet korundu. Arama bildirimi cihaz kaydı iyileştirildi. Mevcut uygulama düzeni korundu.',
    'testedSource':'e9fe66729db9727710963eedb8ebb4558bc73156',
    'buildRun':41110486403,
}
Path('android-update.json').write_text(json.dumps(feed,ensure_ascii=False,indent=2)+'\n')
Path('release-notes.md').write_text('NgelX 1.0.355 / Build585\n\n'+feed['notes']+'\n\n184 sunucu testi, 70 uygulama testi, referans ekran kontrolleri, Android derlemesi ve mevcut imza doğrulandı. Arka planda arama için iki fiziksel telefonda kontrol bekleniyor. Arama sunucusu değişiklikleri bu yayına dahil değildir.\n\nMevcut uygulamanın üzerine güncellenir.\n')
print('Exact reviewed Build585 APK verified:',len(raw),digest)
