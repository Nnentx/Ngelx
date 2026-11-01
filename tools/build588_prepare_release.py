from pathlib import Path
import hashlib,json,zipfile
files=list(Path('verified-apk').rglob('*.apk'));assert len(files)==1
raw=files[0].read_bytes();digest=hashlib.sha256(raw).hexdigest()
assert len(raw)==50872938 and digest=='852185e6ed679079c07a54444cc2aff76a58056aeee81c6df09849f36c36a730'
with zipfile.ZipFile(files[0]) as z:assert z.testzip() is None and 'lib/arm64-v8a/libapp.so' in z.namelist()
assert 'version: 1.0.358+588' in Path('verified-source/pubspec.yaml').read_text()
name='NgelX-1.0.358-Build588.apk';Path(name).write_bytes(raw);Path(name+'.sha256').write_text(digest+'  '+name+'\n')
notes='Kamerasız yayında profil resmi, yuvarlak sesli oda mikrofonları, çoklu hediye akışı, gerçekçi kedi/kaplan görselleri ve hayvan/uzay sesleri eklendi. Moderatör yetkileri tamamlandı. PK sonunda sonuç ve WIN serisi gösterilir; yeni PK’de devam eder, yenilgide sıfırlanır.'
feed={'schema':1,'package':'com.nnentx.ngelx_app','abi':'arm64-v8a','version':'1.0.358','build':588,'size':len(raw),'sha256':digest,'url':'https://github.com/Nnentx/Ngelx/releases/download/v1.0.358-build588/'+name,'notes':notes,'testedSource':'f99ff01dc298102ce5e285f93144fb11edaa631d','buildRun':41358497846,'backendRun':41359532044}
Path('android-update.json').write_text(json.dumps(feed,ensure_ascii=False,indent=2)+'\n')
Path('release-notes.md').write_text('NgelX 1.0.358 / Build588\n\n'+notes+'\n\n219 sunucu testi, tam Flutter analizi, eski/yeni etkileşim testleri ve imza eşleşmesi geçti. Canlı sunucu ve Firestore kuralları güncellendi. İki gerçek geçici hesapla eşzamanlı PK bitişi, ortak sonuç, tek WIN artışı, tekrar güvenliği ve istemciden WIN değiştirilememesi doğrulandı. Fiziksel Android cihazda görünüm ve performans kontrolü ayrıca yapılmalıdır.\n')
print('Exact Build588 APK and source verified for publication')
