from pathlib import Path
strip=Path('app/lib/build445_inbox_model.dart').read_text()
main=Path('app/lib/main.dart').read_text()
story=Path('app/lib/story_v66.dart').read_text()
checks={
 'Self avatar opens profile, not Create': 'body:ProfilPage()' in strip and 'const YuklePage()' not in strip,
 'Small plus has independent note action': 'onTap:()=>_editNote(p)' in strip and 'width:18,height:18' in strip,
 'Note length and expiry are enforced without displayed counters': "maxLength:50" in strip and "counterText:''" in strip and 'Duration(hours:24)' in strip and '_noteClock?.cancel()' in strip,
 'No unused note spacer above avatars': 'SizedBox(height:24,child:note.isEmpty' not in strip and 'SizedBox(height:86' in strip,
 'All tabs retain avatar strip': 'if(ben!=null)Ngelx445FriendsStrip' in main,
 'Create has a Material text surface': 'textStyle:const TextStyle(color:Colors.black87,fontSize:14,decoration:TextDecoration.none)' in main,
 'Group add failures and slow reads are handled': '_uyeEkle446' in main and 'Kişiler yüklenemedi. Tekrar dene.' in main and 'Future.wait(izinli.map(_uyeGetir)).timeout' in main,
 'Story mirror accepted, foreign origins rejected, owner retained': 'Uri.parse(_ngelxMediaApiBackup).origin' in story and "actual['ownerId']" in story and '!ownR2Key(keyPath)' in story,
 'Existing minimized group call controls retained': 'class Ngelx445CallControls' in strip and 'ngelx445ReturnCall' in strip and 'ngelx445EndBackground' in strip,
}
for name,ok in checks.items():print(('PASS ' if ok else 'FAIL ')+name)
assert all(checks.values())
