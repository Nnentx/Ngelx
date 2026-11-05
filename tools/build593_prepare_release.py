from pathlib import Path
import hashlib,json,os,zipfile

files=list(Path('verified-apk').rglob('*.apk'))
assert len(files)==1,'Expected one tested APK'
raw=files[0].read_bytes()
assert 45_000_000<len(raw)<70_000_000
with zipfile.ZipFile(files[0]) as z:
    assert z.testzip() is None
    assert 'lib/arm64-v8a/libapp.so' in z.namelist()
source=Path('verified-source/NgelX-Build593-Source.zip')
with zipfile.ZipFile(source) as z:
    assert z.testzip() is None
    assert 'version: 1.0.363+593' in z.read('pubspec.yaml').decode()
    assert 'lib/build592_gifts.dart' in z.namelist()
    assert all('assets/gifts592/'+kind+'.mp3' in z.namelist() for kind in ['rooster','bucket','tomato','flame','balloon'])
name='NgelX-1.0.363-Build593.apk'
digest=hashlib.sha256(raw).hexdigest()
Path(name).write_bytes(raw)
Path(name+'.sha256').write_text(digest+'  '+name+'\n')
Path(source.name).write_bytes(source.read_bytes())
notes='Ludo taşı biraz yavaşlatıldı. Eşsiz dört kişilik arkadaş odasında ev sahibi iki oyuncuyla oyunu başlatabilir. İki kişilik klasik oyunda dengeli zar dağılımı etkin. Canlı yayında konuk daveti gizliliği ve yorum susturma menüsü düzeltildi.'
feed={'schema':1,'package':'com.nnentx.ngelx_app','abi':'arm64-v8a','version':'1.0.363','build':593,'size':len(raw),'sha256':digest,'url':'https://github.com/Nnentx/Ngelx/releases/download/v1.0.363-build593/'+name,'notes':notes,'testedSource':os.environ['NGELX_TESTED_SHA'],'buildRun':int(os.environ['NGELX_QA_RUN']),'backendRun':int(os.environ['GITHUB_RUN_ID'])}
Path('android-update.json').write_text(json.dumps(feed,ensure_ascii=False,indent=2)+'\n')
Path('release-notes.md').write_text(notes+'\n')
print(json.dumps({'size':len(raw),'sha256':digest,'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest()}))
