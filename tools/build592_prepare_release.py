from pathlib import Path
import hashlib,json,os,zipfile

files=list(Path('verified-apk').rglob('*.apk'))
assert len(files)==1,'Expected one tested APK'
raw=files[0].read_bytes()
assert 45_000_000<len(raw)<70_000_000
with zipfile.ZipFile(files[0]) as z:
    assert z.testzip() is None
    assert 'lib/arm64-v8a/libapp.so' in z.namelist()
source=Path('verified-source/NgelX-Build592-Source.zip')
with zipfile.ZipFile(source) as z:
    assert z.testzip() is None
    assert 'version: 1.0.362+592' in z.read('pubspec.yaml').decode()
    assert 'lib/build592_gifts.dart' in z.namelist()
    assert all('assets/gifts592/'+kind+'.mp3' in z.namelist() for kind in ['rooster','bucket','tomato','flame','balloon'])
name='NgelX-1.0.362-Build592.apk'
digest=hashlib.sha256(raw).hexdigest()
Path(name).write_bytes(raw)
Path(name+'.sha256').write_text(digest+'  '+name+'\n')
Path(source.name).write_bytes(source.read_bytes())
notes='Dört kişilik Ludo daveti üçüncü ve dördüncü oyuncuya açık kalır; masa dolunca oyun otomatik başlar. Zar dağılımı dört oyuncu için eşit dengelenir. Taş dokunuşları arka plan yenilemesini beklemez, hareketler hızlandırıldı. Hediyeler resimleriyle görünür: horoz ötüşü, balonlar, patlayan domates, iki saniyelik tam ekran ateş ve sesli su dökülmesi eklendi. Ses kapatma ve arka plana geçiş kontrolleri korundu. Nefes mavi tiki ve önceki sesli oda tasarımı korundu.'
feed={'schema':1,'package':'com.nnentx.ngelx_app','abi':'arm64-v8a','version':'1.0.362','build':592,'size':len(raw),'sha256':digest,'url':'https://github.com/Nnentx/Ngelx/releases/download/v1.0.362-build592/'+name,'notes':notes,'testedSource':os.environ['NGELX_TESTED_SHA'],'buildRun':int(os.environ['NGELX_QA_RUN']),'backendRun':int(os.environ['GITHUB_RUN_ID'])}
Path('android-update.json').write_text(json.dumps(feed,ensure_ascii=False,indent=2)+'\n')
Path('release-notes.md').write_text(notes+'\n\n234 sunucu testi, Flutter analizi, dokunma/davet/hediye/sessize alma testleri ve mevcut APK imzası doğrulandı. Dört geçici hesapla canlı katılım, otomatik başlangıç, zar dağılımı ve hediye ödeme tekrarı kontrol edildi. Fiziksel Android cihazda ses ve akıcılık kontrolü yapılmadı.\n')
print(json.dumps({'size':len(raw),'sha256':digest,'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest()}))
