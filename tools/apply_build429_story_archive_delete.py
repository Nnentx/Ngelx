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
    import_line="import 'package:firebase_storage/firebase_storage.dart';\n"
    first_part=__import__('re').search(r'^part\s',s,__import__('re').M)
    if first_part is None: raise SystemExit('Build429 main.dart part anchor drift')
    s=s[:first_part.start()]+import_line+s[first_part.start():]
old="""          final docs=(s.data?.docs??[]).toList()
            ..sort((a,b){"""
new="""          final docs=(s.data?.docs??[]).where((d){
            final v=d.data();
            final hidden=List<String>.from(v['hiddenFor']??const[]);
            return v['type']=='story'&&v['deleted']!=true&&v['isDeleted']!=true&&
              !hidden.contains(uid)&&
              (v['archivedAt'] is Timestamp||v['highlighted']==true);
          }).toList()
            ..sort((a,b){"""
s=one(s,old,new,'archive only saved stories and hide deleted items')
archiveStart=s.index('class HikayeArsiviPage extends StatelessWidget{')
archiveEnd=s.index('class NgelXArsivMerkeziPage',archiveStart)
archive=s[archiveStart:archiveEnd]
oldError="          if(s.connectionState==ConnectionState.waiting)return const Center(child:CircularProgressIndicator(color:mor));"
newError=oldError+"""
          if(s.hasError)return Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
            const Icon(Icons.cloud_off_rounded,color:Color(0xFF8A93A8),size:34),
            const SizedBox(height:10),
            const Text('Hikâye arşivi yüklenemedi.',style:TextStyle(color:Colors.black54)),
            TextButton(
              onPressed:()=>Navigator.pushReplacement(context,MaterialPageRoute(builder:(_)=>const HikayeArsiviPage())),
              child:const Text('Tekrar dene',style:TextStyle(color:mor,fontWeight:FontWeight.w800)),
            ),
          ]));"""
archive=one(archive,oldError,newError,'story archive error and retry state')
s=s[:archiveStart]+archive+s[archiveEnd:]
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
  final current=await ref.get();
  final actual=current.data();
  if(actual==null)return;
  if(actual['type']!='story'||(actual['ownerId']??'').toString()!=uid){
    throw StateError('Yalnızca kendi hikâyeni silebilirsin.');
  }
  final api=await ngelxMediaApiAdresi();
  bool ownR2Key(String key){
    final segments=key.split('/');
    return segments.length>=3&&
      (segments.first=='stories'||segments.first=='videos')&&
      segments[1]==uid&&!segments.contains('..')&&!segments.contains('.');
  }
  final kaynaklar=<String,Reference>{};
  final r2Anahtarlari=<String>{};
  for(final key in ['storagePath','mediaPath','storageRef','mediaUrl','videoUrl','playbackUrl','downloadUrl','url']){
    final raw=(actual[key]??'').toString().trim();
    if(raw.isEmpty)continue;
    if(raw.startsWith('gs://')||raw.contains('firebasestorage.googleapis.com')){
      final dosya=storage.refFromURL(raw);
      if(dosya.bucket!=storage.ref().bucket||!dosya.fullPath.startsWith('stories/'+uid+'/')){
        throw StateError('Hikâye medya yolu sahibiyle eşleşmiyor.');
      }
      kaynaklar[dosya.fullPath]=dosya;
      continue;
    }
    if(raw.contains('/media/')){
      if(api.isEmpty||!raw.startsWith(api+'/media/')){
        throw StateError('Hikâye medya sunucusu doğrulanamadı.');
      }
      final uri=Uri.parse(raw);
      final keyPath=Uri.decodeComponent(uri.path.substring('/media/'.length));
      if(!ownR2Key(keyPath)){
        throw StateError('Hikâye medya yolu sahibiyle eşleşmiyor.');
      }
      r2Anahtarlari.add(keyPath);
      continue;
    }
    if(!raw.startsWith('http')&&raw.contains('/')){
      if(!ownR2Key(raw)){
        throw StateError('Hikâye medya yolu sahibiyle eşleşmiyor.');
      }
      r2Anahtarlari.add(raw);
    }
  }

  if(r2Anahtarlari.isNotEmpty){
    final user=FirebaseAuth.instance.currentUser;
    final token=await user?.getIdToken();
    if(api.isEmpty||token==null||token.isEmpty){
      throw StateError('Hikâye medyası güvenli biçimde silinemedi.');
    }
    for(final key in r2Anahtarlari){
      try{
        await Dio().delete(
          api+'/object',
          queryParameters:{'key':key},
          options:Options(
            headers:{'Authorization':'Bearer '+token},
            sendTimeout:const Duration(seconds:12),
            receiveTimeout:const Duration(seconds:12),
          ),
        );
      }on DioException catch(e){
        if(e.response?.statusCode!=404)rethrow;
      }
    }
  }
  for(final dosya in kaynaklar.values){
    try{
      await dosya.delete();
    }on FirebaseException catch(e){
      if(e.code!='object-not-found')rethrow;
    }
  }
  Future<void> purgeLikes(CollectionReference<Map<String,dynamic>> col)async{
    while(true){
      final page=await col.limit(400).get();
      if(page.docs.isEmpty)return;
      final batch=FirebaseFirestore.instance.batch();
      for(final d in page.docs){batch.delete(d.reference);}
      await batch.commit();
      if(page.docs.length<400)return;
    }
  }
  final comments=ref.collection('comments');
  while(true){
    final page=await comments.limit(200).get();
    if(page.docs.isEmpty)break;
    for(final comment in page.docs){
      await purgeLikes(comment.reference.collection('likes'));
    }
    final batch=FirebaseFirestore.instance.batch();
    for(final comment in page.docs){batch.delete(comment.reference);}
    await batch.commit();
    if(page.docs.length<200)break;
  }
  await purgeLikes(ref.collection('likes'));
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
