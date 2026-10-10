from pathlib import Path
s=Path('app/lib/main.dart').read_text();v=Path('app/lib/story_v66.dart').read_text()
checks={
 'late subscribers replay last event':'if(_hasValue)listener.add(_value as T)' in s,
 'bounded initial wait':'_sendError(TimeoutException' in s,
 'inbox owns and disposes stream cache':'for(final cache in _akislari.values){cache.dispose();}' in s,
 'one chat query shared by card and counter':"putIfAbsent('chat|'+ben," in s,
 'request list has inline retry':'stream:_chats.stream' in s and "ngelx432YuklemeHatasi(_retry,'Mesaj istekleri yüklenemedi.')" in s,
 'profile search debounce and delete revision':'milliseconds:220' in s and '_paylasimCache.dispose()' in s,
 'archive retained stream and no resurrection':'stream:_archive.stream' in s and "d.reference.update({'highlighted':!oneCikan})" in s,
 'archive deletion predicate':'ngelx432ArsivGorunur(d.id,d.data(),uid)' in s,
 'visitor profile retains future and clears after action':'future:profiles' in s and '_profileDocs.clear();setState(change)' in s,
 'video awaits existing preload':'try{await sonrakiVideoHazirlama;}' in v,
 'video initialization 30s':'initialize().timeout(const Duration(seconds:30))' in v,
 'buffering stops progress and has bounded retry':'_bufferTimer??=Timer(const Duration(seconds:20)' in v and '_videoBasarisiz(x)' in v,
 'profile bell and story DM preserved':s.count('const NgelXProfilBildirimZili()')==2 and "'type':'story_reply'" in v,
 'safe delete preserved':'for(final url in urls){await ngelxMedyaSil(url);}' in s and 'parts[1]!=uid' in s,
 'version':'version: 1.0.207+432' in Path('app/pubspec.yaml').read_text(),
}
for name,ok in checks.items():print(('PASS ' if ok else 'FAIL ')+name)
if not all(checks.values()):raise SystemExit('Build432 preservation checks failed')
