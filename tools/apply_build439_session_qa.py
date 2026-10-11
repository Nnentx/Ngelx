from pathlib import Path
import shutil

def apply():
 p=Path('app/lib/main.dart');s=p.read_text()
 if '// Build439 session QA' in s:return
 s="import 'build439_session_gate.dart';\nimport 'build439_auth_operations.dart';\n"+s
 s=s.replace('FirebaseAuth.instance.signInWithEmailAndPassword(', 'ngelx439EmailSignIn(')
 s=s.replace('FirebaseAuth.instance.signOut()', 'ngelx439SignOut()')
 s+='''
final _ngelx439AuthOperations=NgelXAuthOperations<UserCredential>();
Future<UserCredential> ngelx439EmailSignIn({required String email,required String password})=>
  _ngelx439AuthOperations.signIn(()=>FirebaseAuth.instance.signInWithEmailAndPassword(email:email,password:password));
Future<void> ngelx439SignOut()=>_ngelx439AuthOperations.signOut(()async{
  await FirebaseAuth.instance.signOut();
  ngelxKokRotayaDon();
});
'''
 settings=Path('app/lib/build258_settings.dart')
 settings.write_text(settings.read_text().replace('FirebaseAuth.instance.signOut()', 'ngelx439SignOut()'))

 s=s.replace('void ngelxKokRotayaDon(){',"bool _ngelx439RootScheduled=false;\nvoid ngelxKokRotayaDon(){\n  if(_ngelx439RootScheduled)return;\n  _ngelx439RootScheduled=true;",1)
 s=s.replace("WidgetsBinding.instance.addPostFrameCallback((_){\n    ngelxNavigatorKey.currentState?.pushNamedAndRemoveUntil('/',(route)=>false);", "WidgetsBinding.instance.addPostFrameCallback((_){\n    _ngelx439RootScheduled=false;\n    ngelxNavigatorKey.currentState?.pushNamedAndRemoveUntil('/',(route)=>false);",1)
 old="""child:StreamBuilder<User?>(
          stream:FirebaseAuth.instance.userChanges(),
          initialData:FirebaseAuth.instance.currentUser,
          builder:(_,auth){
            final kullanici=auth.data;"""
 new="""child:NgelXSessionGate<User>(
          changes:FirebaseAuth.instance.userChanges(),
          current:()=>FirebaseAuth.instance.currentUser,
          builder:(_,kullanici){"""
 assert s.count(old)==1;s=s.replace(old,new)
 a=s.index('  Future<void> profiliGetir() async {',s.index('class _ProfilPageState'))
 b=s.index('  Future<void> fotografYukle()',a)
 block=s[a:b].replace('if (user == null) return;',"if(user==null){if(mounted)setState(()=>yukleniyor=false);return;}")
 block=block.replace('.get();','.get().timeout(const Duration(seconds:10));',1)
 block=block.replace('    try {','    if(mounted)setState((){yukleniyor=true;_profilHatasi=false;});\n    try {',1)
 block=block.replace('setState(()=>yukleniyor=false);','setState((){yukleniyor=false;_profilHatasi=true;});')
 s=s[:a]+block+s[b:]
 a=s.index('class _ProfilPageState');b=s.index('\nclass ',a+10)
 block=s[a:b].replace('  bool yukleniyor = true;','  bool yukleniyor = true;\n  bool _profilHatasi=false;',1)
 marker='''    if (yukleniyor) {
      return const Center('''
 assert marker in block
 block=block.replace(marker,"""    if(_profilHatasi)return Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
      Text(_ngelx438Ui('Profil bilgileri alınamadı'),style:const TextStyle(color:Colors.black87)),
      const SizedBox(height:12),
      FilledButton(onPressed:profiliGetir,child:Text(_ngelx438Ui('Tekrar dene'))),
    ]));
"""+marker,1)
 s=s[:a]+block+s[b:]
 # Reject invalid usernames consistently when editing, rather than silently stripping spaces.
 s=s.replace("_kullanici.text.trim().replaceFirst('@','').replaceAll(' ','')","_kullanici.text.trim().replaceFirst('@','')")
 s=s.replace("if(ad.length<2||kullanici.length<3){","if(ad.length<2||!RegExp(r'^[a-zA-Z0-9._]{3,20}$').hasMatch(kullanici)){")
 s=s.replace('TextField(controller:_kullanici,maxLength:30,','TextField(controller:_kullanici,maxLength:20,')
 # Clear stale chat-level mute when unmuting through either user preference UI.
 old="""      await FirebaseFirestore.instance.collection('users').doc(ben).set({
        'mutedChats':sessiz?FieldValue.arrayUnion([chatId]):FieldValue.arrayRemove([chatId]),
        if(!sessiz)'mutedChatUntil':{chatId:FieldValue.delete()},
      },SetOptions(merge:true)).timeout(const Duration(seconds:12));"""
 new="""      final batch=FirebaseFirestore.instance.batch();
      batch.set(FirebaseFirestore.instance.collection('users').doc(ben),{
        'mutedChats':sessiz?FieldValue.arrayUnion([chatId]):FieldValue.arrayRemove([chatId]),
        if(!sessiz)'mutedChatUntil':{chatId:FieldValue.delete()},
      },SetOptions(merge:true));
      if(!sessiz)batch.set(FirebaseFirestore.instance.collection('chats').doc(chatId),
        {'mutedFor':FieldValue.arrayRemove([ben])},SetOptions(merge:true));
      await batch.commit().timeout(const Duration(seconds:12));"""
 assert old in s;s=s.replace(old,new,1)
 old="await ref.set({'mutedChats':FieldValue.arrayRemove([chatId]),'mutedChatUntil':{chatId:FieldValue.delete()}},SetOptions(merge:true));"
 new="""final batch=FirebaseFirestore.instance.batch();
      batch.set(ref,{'mutedChats':FieldValue.arrayRemove([chatId]),'mutedChatUntil':{chatId:FieldValue.delete()}},SetOptions(merge:true));
      batch.set(FirebaseFirestore.instance.collection('chats').doc(chatId),{'mutedFor':FieldValue.arrayRemove([me])},SetOptions(merge:true));
      await batch.commit().timeout(const Duration(seconds:12));"""
 assert old in s;s=s.replace(old,new,1)
 s=s.replace("if(!mounted)return;\n    setState((){\n      engellenenler=", "if(!mounted||uid!=ben)return;\n    setState((){\n      engellenenler=",1)
 # Archive restore is one acknowledged write; the old helper swallowed failures.
 a=s.index('class _ArsivSohbetlerPageState')
 b=s.index('class MesajIstekleriPage',a)
 block=s[a:b].replace(".doc(widget.uid).get();",".doc(widget.uid).get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:10));",1)
 x=block.index('  Future<void> geriAl(String id) async {')
 y=block.index('  Future<void> eskiSohbetiSil',x)
 block=block[:x]+"""  Future<void> geriAl(String id) async {
    if(FirebaseAuth.instance.currentUser?.uid!=widget.uid)return;
    try{
      final batch=FirebaseFirestore.instance.batch();
      batch.set(FirebaseFirestore.instance.collection('users').doc(widget.uid),
        {'archivedChats':FieldValue.arrayRemove([id])},SetOptions(merge:true));
      batch.delete(ngelxGroupArchiveRef(widget.uid,id));
      await batch.commit().timeout(const Duration(seconds:12));
      if(mounted&&FirebaseAuth.instance.currentUser?.uid==widget.uid)_arsivYenile();
    }catch(_){
      if(mounted)ngelxDurumMesaji(context,_ngelx438Ui('Arşivden çıkarılamadı. Bağlantını kontrol edip tekrar dene.'),tip:'hata');
    }
  }

"""+block[y:]
 s=s[:a]+block+s[b:]
 s=s.replace("'displayName':ad,'username':kullanici,", "'displayName':ad,'username':kullanici,'usernameLower':kullanici.toLowerCase(),")
 s=s.replace("'username': yeniKullanici,", "'username': yeniKullanici,'usernameLower':yeniKullanici.toLowerCase(),")
 # Apply the same username policy to the older edit dialog too.
 s=s.replace(".trim()\n                          .replaceAll(' ', '');", ".trim();")
 s=s.replace('yeniKullanici.length < 3',"!RegExp(r'^[a-zA-Z0-9._]{3,20}$').hasMatch(yeniKullanici)")
 # Server reads and child deletion are bounded; media failure no longer prevents
 # deleting the owned database record. Persist cleanup before any irreversible work.
 a=s.index('Future<void> ngelxPaylasimVeAltKayitlariniSil(')
 b=s.index('\nFuture<void> kendiPaylasiminiSil(',a)
 block=s[a:b]
 block=block.replace('source:Source.server));','source:Source.server)).timeout(const Duration(seconds:10));')
 block=block.replace('  for(final url in urls){await ngelxMedyaSil(url);}',
   "  await ngelx439RememberPostCleanup(uid,ref.id,urls);")
 block=block.replace("ref.collection('likes').get()","ref.collection('likes').get().timeout(const Duration(seconds:10))")
 block=block.replace("ref.collection('comments').get()","ref.collection('comments').get().timeout(const Duration(seconds:10))")
 block=block.replace("yorum.reference.collection('likes').get()","yorum.reference.collection('likes').get().timeout(const Duration(seconds:10))")
 block=block.replace('  silinecek.add(ref);','')
 block=block.replace('    await batch.commit();',"    if(FirebaseAuth.instance.currentUser?.uid!=uid)throw StateError('Oturum değişti.');\n    await batch.commit().timeout(const Duration(seconds:12));")
 block=block.replace('  ngelxIcerikSilindi(ref.id);',
   "  if(FirebaseAuth.instance.currentUser?.uid!=uid)throw StateError('Oturum değişti.');\n  await ref.delete().timeout(const Duration(seconds:12));\n  ngelxIcerikSilindi(ref.id);\n  unawaited(ngelx439RetryPostCleanup(uid));")
 s=s[:a]+block+s[b:]
 s=s.replace('super.initState();unawaited(ngelxKullaniciSemasiniTamamla(widget.user));_yenile();',
   'super.initState();unawaited(ngelxKullaniciSemasiniTamamla(widget.user));unawaited(ngelx439RetryPostCleanup(widget.user.uid));_yenile();')
 s+='\n'+Path('tools/build439_post_cleanup.dart').read_text()
 # Keep the same data model/routes/permissions. Generated files are not committed.
 s+='\n// Build439 session QA\n'
 p.write_text(s)
 shutil.copy('tools/build439_session_gate.dart','app/lib/build439_session_gate.dart')
 shutil.copy('tools/build439_auth_operations.dart','app/lib/build439_auth_operations.dart')
if __name__=='__main__':apply()
