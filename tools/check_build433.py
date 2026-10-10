from pathlib import Path
s=Path('app/lib/main.dart').read_text();r=Path('firestore.rules').read_text()
checks={
 'dedicated request page titles and no category tabs':"String get _sayfaBasligi" in s and "if(!_istekSayfasi&&!widget.notificationOnly)Container(" in s,
 'profile bell notification-only and white background':"const AktivitePage(notificationOnly:true)" in s and 'IconButton.styleFrom(backgroundColor:Colors.white' in s,
 'request names and full approve/delete buttons':"child:Text(kabul?'Onayla':'Sil')" in s,
 'counter and page share newest request state':s.count('ngelx433SosyalIstekler(')>=3,
 'inbox names use rich colored text':'title:ngelx433RenkliBildirim(v)' in s,
 'live cleanup requires owner and rejects active':"v['ownerId']!=uid" in s and "Devam eden yayın silinemez" in s,
 'media cleaned before root record':s.index('for(final url in urls){if(!await ngelx433MedyaKullaniliyor(url,id))await ngelxMedyaSil(url);}',s.index('Future<void> ngelx433CanliSil'))<s.index('await ref.delete()',s.index('Future<void> ngelx433CanliSil')),
 'live child cleanup authorized for host':r.count('get(/databases/$(database)/documents/live_streams/$(streamId)).data.ownerId == request.auth.uid')==3,
 'working story source unchanged':"label:const Text('Tekrar dene')" in Path('app/lib/story_v66.dart').read_text(),
 'release version':'version: 1.0.208+433' in Path('app/pubspec.yaml').read_text(),
}
for name,ok in checks.items():print(('PASS ' if ok else 'FAIL ')+name)
assert all(checks.values())
