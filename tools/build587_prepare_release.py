"""Publish only the exact reviewed Build587 APK."""
from pathlib import Path
import hashlib,json,zipfile
files=list(Path('verified-apk').rglob('*.apk'))
assert len(files)==1,'Expected one tested APK'
raw=files[0].read_bytes();digest=hashlib.sha256(raw).hexdigest()
assert len(raw)==50237265,'APK size differs from reviewed artifact'
assert digest=='be0d3093a60c3f439a683dc3df778f0c270665644388837c582b0cd4a7aed36b','APK differs from reviewed artifact'
with zipfile.ZipFile(files[0]) as archive:
 assert archive.testzip() is None
 assert 'lib/arm64-v8a/libapp.so' in archive.namelist()
 assert 'assets/flutter_assets/AssetManifest.bin' in archive.namelist()
name='NgelX-1.0.357-Build587.apk'
Path(name).write_bytes(raw)
Path(name+'.sha256').write_text(digest+'  '+name+'\n')
feed={'schema':1,'package':'com.nnentx.ngelx_app','abi':'arm64-v8a',
 'version':'1.0.357','build':587,'size':len(raw),'sha256':digest,
 'url':'https://github.com/Nnentx/Ngelx/releases/download/v1.0.357-build587/'+name,
 'notes':'Ludo GO tek dokunuşta bir kez zar atar; hamle yoksa sıra diğer oyuncuya geçer. Zar olasılıkları tüm oyuncular ve makine için eşittir. Hediyeler onay sormadan gönderilir ve yan yana sıralanır. Kalp efektleri, alt yorum alanı, yarı yükseklikte kaydırılabilir sohbet, yeni emojiler, yönetici seçenekleri ve PK görünümü yenilendi.',
 'testedSource':'b996a43665323126ba6016879fa45fd7902bef2c','buildRun':41346489478}
Path('android-update.json').write_text(json.dumps(feed,ensure_ascii=False,indent=2)+'\n')
Path('release-notes.md').write_text('NgelX 1.0.357 / Build587\n\n'+feed['notes']+'\n\nSunucu testleri, uygulama etkileşim testleri, ekran kontrolleri, Android derlemesi ve mevcut uygulamayla imza eşleşmesi doğrulandı. Fiziksel telefon kontrolü ayrıca yapılmalıdır.\n')
print('Exact reviewed Build587 APK verified:',len(raw),digest)
