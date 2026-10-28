"""Promote only the immutable APK that passed Build584 review."""
from pathlib import Path
import hashlib
import json
import os
import zipfile

files=list(Path('verified-apk').rglob('*.apk'))
assert len(files)==1, 'Expected one tested APK'
raw=files[0].read_bytes()
digest=hashlib.sha256(raw).hexdigest()
assert len(raw)==50219217
assert digest=='56e8db6c711018687c47348fd3d369d79efdeb533497e0bf46df705f41f9eda0'
with zipfile.ZipFile(files[0]) as z:
    assert z.testzip() is None
    assert 'lib/arm64-v8a/libapp.so' in z.namelist()
    assert 'assets/flutter_assets/assets/ludo575_home.wav' in z.namelist()
name='NgelX-1.0.354-Build584.apk'
Path(name).write_bytes(raw)
Path(name+'.sha256').write_text(digest+'  '+name+'\n')
feed={
 'schema':1,'package':'com.nnentx.ngelx_app','abi':'arm64-v8a',
 'version':'1.0.354','build':584,'size':len(raw),'sha256':digest,
 'url':'https://github.com/Nnentx/Ngelx/releases/download/v1.0.354-build584/'+name,
 'notes':'Ludo: 4 kişilik oda 2 oyuncuyla başlatıldığında oyuncular çapraz yerleşir. Sıra geldiğinde zarda GO görünür. Oyun tahtası dikeyde genişletildi. 2, 3 ve 4 kişilik oyunlarda zar adaleti kontrolleri tamamlandı.',
 'testedSource':'c999d229d68ea9d79911d2e9821a711814d17455',
 'buildRun':40757681279,'liveAcceptanceRun':int(os.environ['GITHUB_RUN_ID']),
}
Path('android-update.json').write_text(json.dumps(feed,ensure_ascii=False,indent=2)+'\n')
Path('release-notes.md').write_text('NgelX 1.0.354 / Build584\n\n'+feed['notes']+'\n\n158 sunucu testi, 62 arayüz testi, referans ekranları, Android derlemesi ve mevcut imza doğrulandı. Canlı API kontrolü geçtikten sonra yayımlanır; fiziksel cihaz testi yapılmış sayılmaz.\n\nMevcut uygulamanın üzerine güncellenir.\n')
print('Exact tested Build584 APK verified:',len(raw),digest)
