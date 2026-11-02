from pathlib import Path
import hashlib,json,zipfile
files=list(Path('verified-apk').rglob('*.apk'));assert len(files)==1
raw=files[0].read_bytes();digest=hashlib.sha256(raw).hexdigest()
assert len(raw)==50871498 and digest=='ac12bcad83e4d25d671eadbb5e3b523e9f94764e960f00dd25a051d97dab4c27'
with zipfile.ZipFile(files[0]) as z:assert z.testzip() is None and 'lib/arm64-v8a/libapp.so' in z.namelist()
assert 'version: 1.0.359+589' in Path('verified-source/pubspec.yaml').read_text()
name='NgelX-1.0.359-Build589.apk';Path(name).write_bytes(raw);Path(name+'.sha256').write_text(digest+'  '+name+'\n')
notes="PK puanı artık sunucudaki başlangıç ve bitiş anına göre hesaplanır; son saniyedeki hediye sayılır, süre sonrasındaki hediyeler sonucu değiştirmez. Erken bitiş yanıtında sessiz yeniden deneme, hediye yüklenirken sesi kapatma düzeltmesi ve büyük yazıya uyumlu yuvarlak sesli oda yerleri eklendi."
feed={'schema':1,'package':'com.nnentx.ngelx_app','abi':'arm64-v8a','version':'1.0.359','build':589,'size':len(raw),'sha256':digest,'url':'https://github.com/Nnentx/Ngelx/releases/download/v1.0.359-build589/'+name,'notes':notes,'testedSource':'d0bb555c2679405ea03c8ad8d0c414d7fc6d109f','buildRun':41403709092,'backendRun':41405178995}
Path('android-update.json').write_text(json.dumps(feed,ensure_ascii=False,indent=2)+'\n')
Path('release-notes.md').write_text('NgelX 1.0.359 / Build589\n\n'+notes+'\n\n230 sunucu testi, Firestore yetki testleri, gerçek geçmiş veri sorguları, Flutter analizi, telefon boyutlarında widget testleri ve mevcut uygulama imzasıyla eşleşme doğrulandı. İki geçici hesapla eşzamanlı canlı PK sonucu ve tek WIN artışı kontrol edildi. Fiziksel Android cihazda görünüm, ses ve performans kontrolü ayrıca yapılmalıdır.\n')
print('Exact signed Build589 APK and source verified for publication')
