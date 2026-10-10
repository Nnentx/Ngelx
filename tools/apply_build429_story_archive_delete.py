#!/usr/bin/env python3
"""Build429: keep archive semantics and safely remove owner story media."""
from pathlib import Path

def one(s, old, new, label):
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'Build429 source drift ({label}): {n} matches')
    return s.replace(old,new,1)

p=Path('app/lib/main.dart')
s=p.read_text(encoding='utf-8')
if "import 'package:firebase_storage/firebase_storage.dart';" not in s:
    part="part 'story_v66.dart';"
    if s.count(part)!=1: raise SystemExit('Build429 main.dart part anchor drift')
    s=s.replace(part,"import 'package:firebase_storage/firebase_storage.dart';\n\n"+part,1)
old="""          final docs=(s.data?.docs??[]).toList()
            ..sort((a,b){"""
new="""          final simdi=DateTime.now();
          final docs=(s.data?.docs??[]).where((d){
            final v=d.data(),bitis=v['expiresAt'];
            final suresiDolmus=bitis is Timestamp&&!bitis.toDate().isAfter(simdi);
            return v['type']=='story'&&
              (v['archivedAt'] is Timestamp||suresiDolmus||v['highlighted']==true);
          }).toList()
            ..sort((a,b){"""
s=one(s,old,new,'archive only saved/expired stories')
p.write_text(s,encoding='utf-8')

p=Path('app/lib/story_v66.dart')
s=p.read_text(encoding='utf-8')
anchor="class NgelXHikayeSeriPage extends StatefulWidget{"
helper="""Future<void> ngelxHikayeKaliciSil(
  DocumentReference<Map<String,dynamic>> ref,
  Map<String,dynamic> veri,
)async{
  final uid=FirebaseAuth.instance.currentUser?.uid;
  if(uid==null||uid.isEmpty||ref.id.isEmpty||
      (veri['ownerId']??'').toString()!=uid){
    throw StateError('Yalnızca kendi hikâyeni silebilirsin.');
  }

  final storage=FirebaseStorage.instance;
  final kaynaklar=<String>{};
  for(final key in ['storagePath','mediaPath','storageRef','mediaUrl','videoUrl','playbackUrl','downloadUrl','url']){
    final raw=(veri[key]??'').toString().trim();
    if(raw.isNotEmpty)kaynaklar.add(raw);
  }
  final silinecek=<String,Reference>{};
  for(final raw in kaynaklar){
    try{
      Reference? dosya;
      if(raw.startsWith('gs://')||raw.contains('firebasestorage.googleapis.com')){
        dosya=storage.refFromURL(raw);
      }else if(!raw.startsWith('http')&&
          (raw.contains('/')||raw.startsWith('stories/'))){
        dosya=storage.ref(raw);
      }
      if(dosya==null)continue;
      // Never follow an arbitrary URL/path to another user's object.
      if(!dosya.fullPath.split('/').contains(uid)){
        throw StateError('Hikâye medya yolu sahibiyle eşleşmiyor.');
      }
      silinecek[dosya.fullPath]=dosya;
    }on FirebaseException catch(e){
      if(e.code=='object-not-found')continue;
      rethrow;
    }
  }
  for(final dosya in silinecek.values){
    try{
      await dosya.delete();
    }on FirebaseException catch(e){
      if(e.code!='object-not-found')rethrow;
    }
  }
  await ref.delete();
}

"""
s=one(s,anchor,helper+anchor,'owner-only story media deletion helper')
old="await FirebaseFirestore.instance.collection('videos').doc(storyId).delete();"
new="""final silinecekRef=FirebaseFirestore.instance.collection('videos').doc(storyId);
        await ngelxHikayeKaliciSil(silinecekRef,veri);"""
s=one(s,old,new,'story delete uses guarded storage cleanup')
p.write_text(s,encoding='utf-8')

p=Path('app/lib/main.dart')
s=p.read_text(encoding='utf-8')
for old,new in [("defaultValue: '428'","defaultValue: '429'"),("defaultValue: '1.0.203'","defaultValue: '1.0.204'")]:
    s=one(s,old,new,'Android app version '+old)
p.write_text(s,encoding='utf-8')

p=Path('app/pubspec.yaml')
s=p.read_text(encoding='utf-8')
if '  firebase_storage: ^13.6.0\n' not in s:
    anchor='  firebase_auth: ^6.7.0\n'
    if s.count(anchor)!=1: raise SystemExit('Build429 pubspec Firebase dependency anchor drift')
    s=s.replace(anchor,anchor+'  firebase_storage: ^13.6.0\n',1)
s=one(s,'version: 1.0.203+428','version: 1.0.204+429','pubspec version')
p.write_text(s,encoding='utf-8')
print('Build429 archive filtering, guarded story media deletion and version applied')
