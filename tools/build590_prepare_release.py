from pathlib import Path
import hashlib,json,zipfile
files=list(Path('verified-apk').rglob('*.apk'));assert len(files)==1
raw=files[0].read_bytes();digest=hashlib.sha256(raw).hexdigest()
assert len(raw)==50873066 and digest=='ef49dab0566743bac94c483c2f6f3500c4e2e1314a8a0ad06b4a6a79e8f96e0d'
with zipfile.ZipFile(files[0]) as z:assert z.testzip() is None and 'lib/arm64-v8a/libapp.so' in z.namelist()
assert 'version: 1.0.360+590' in Path('verified-source/pubspec.yaml').read_text()
name='NgelX-1.0.360-Build590.apk';Path(name).write_bytes(raw);Path(name+'.sha256').write_text(digest+'  '+name+'\n')
notes="Sesli oda ekranı referansa göre baştan düzenlendi: üstte küçük yayıncı/takip/dinleyici alanı, tek ekranda 3×3 büyük yuvarlak mikrofon yerleri, siyah zemin üzerinde yorum akışı ve sabit yazma/işlem çubuğu. Büyük bilgi kartı, kaydırmalı ana sayfa ve ayrı mavi sohbet kutusu kaldırıldı. Mikrofon, söz isteği, moderatör işlemleri, takip, PK, müzik, davet ve küçültme kontrolleri yeni yerleşime bağlandı. Büyük yazı ve klavye görünümü düzeltildi."
feed={'schema':1,'package':'com.nnentx.ngelx_app','abi':'arm64-v8a','version':'1.0.360','build':590,'size':len(raw),'sha256':digest,'url':'https://github.com/Nnentx/Ngelx/releases/download/v1.0.360-build590/'+name,'notes':notes,'testedSource':'6a7342f992964cd597f76470151a1e80c7115599','buildRun':41414031341,'visualRun':41414886813,'backendRun':41405178995}
Path('android-update.json').write_text(json.dumps(feed,ensure_ascii=False,indent=2)+'\n')
Path('release-notes.md').write_text('NgelX 1.0.360 / Build590\n\n'+notes+'\n\n230 sunucu testi, Firestore yetki kontrolleri, Flutter analizi ve 30 Flutter testi geçti. Tam ekran görselleri örnekle karşılaştırıldı; profil konumu/çapı, dokuz yerin görünmesi, büyük yazı, klavye ve düğme işlemleri doğrulandı. Ek görsel kabul kontrolünde yazma alanının çizilmesi denetlendi. Sunucu kodu ve veritabanı kuralları değiştirilmedi. Fiziksel Android cihazda canlı ses ve görünüm kontrolü ayrıca yapılmalıdır.\n')
print('Exact signed Build590 APK and assembled application source verified')
