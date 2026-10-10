bool ngelx433KayitSaklanmis(Map<String,dynamic> v)=>v['saved']==true||v['archivedAt']!=null||v['highlighted']==true;
bool ngelx433CanliTemizlenir(Map<String,dynamic> v,DateTime now){
  if(ngelxCanliKaydiTaze(v))return false;
  if(v['active']==true&&v['status']!='ended')return false;
  if(v['deleting']==true)return true;
  if(!ngelx433KayitSaklanmis(v))return true;
  final stamp=v['endedAt']??v['startedAt'];
  return stamp is Timestamp&&now.difference(stamp.toDate())>=const Duration(days:30);
}
List<QueryDocumentSnapshot<Map<String,dynamic>>> ngelx433SosyalIstekler(List<QueryDocumentSnapshot<Map<String,dynamic>>> docs,String uid){
  final sorted=docs.where((d)=>d.data()['toUid']==uid).toList()..sort((a,b){
    int ms(Map<String,dynamic> v){final t=v['createdAt']??v['clientCreatedAt'];return t is Timestamp?t.millisecondsSinceEpoch:0;}
    return ms(b.data()).compareTo(ms(a.data()));
  });
  final seen=<String>{};
  return sorted.where((d){final v=d.data(),kind=(v['type']??'').toString(),from=(v['fromUid']??'').toString();
    if((kind!='follow_request'&&kind!='friend_request')||from.isEmpty)return false;
    if(!seen.add(kind+'|'+from))return false;
    return v['status']=='pending';
  }).toList();
}
Widget ngelx433RenkliBildirim(Map<String,dynamic> v,{int maxLines=2}){
  final text=ngelxBildirimMetni(v),name=(v['senderName']??v['fromName']??'').toString().trim();
  final pos=name.isEmpty?-1:text.indexOf(name);
  return Text.rich(TextSpan(children:pos<0?[TextSpan(text:text)]:[
    if(pos>0)TextSpan(text:text.substring(0,pos)),
    TextSpan(text:name,style:const TextStyle(color:mor,fontWeight:FontWeight.w900)),
    TextSpan(text:text.substring(pos+name.length)),
  ]),maxLines:maxLines,overflow:TextOverflow.ellipsis,style:TextStyle(color:const Color(0xFF111827),fontWeight:v['read']==true?FontWeight.w600:FontWeight.w900));
}
Future<void> ngelx433CanliSil(String id)async{
  final uid=FirebaseAuth.instance.currentUser?.uid;
  if(uid==null)throw StateError('Oturum gerekli.');
  final ref=FirebaseFirestore.instance.collection('live_streams').doc(id);
  await FirebaseFirestore.instance.runTransaction((tx)async{
    final snap=await tx.get(ref),v=snap.data();
    if(v==null)return;
    if(v['ownerId']!=uid)throw StateError('Yalnız yayın sahibi silebilir.');
    if(ngelxCanliKaydiTaze(v)||v['active']==true)throw StateError('Devam eden yayın silinemez.');
    tx.update(ref,{'deleting':true,'deleteRequestedAt':FieldValue.serverTimestamp()});
  }).timeout(const Duration(seconds:12));
  final snap=await ref.get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:12));
  final v=snap.data();if(v==null)return;
  if(v['ownerId']!=uid||v['active']==true||v['deleting']!=true)throw StateError('Silme durumu değişti.');
  final urls=<String>{};
  for(final field in ['mediaUrl','videoUrl','recordingUrl','audioUrl','thumbnailUrl','posterUrl','coverUrl']){
    final value=(v[field]??'').toString().trim();if(value.isNotEmpty)urls.add(value);
  }
  for(final url in urls){await ngelxMedyaSil(url);}
  for(final name in ['comments','reactions','viewers']){
    while(true){
      final q=await ref.collection(name).limit(200).get().timeout(const Duration(seconds:12));
      if(q.docs.isEmpty)break;
      final batch=FirebaseFirestore.instance.batch();for(final d in q.docs){batch.delete(d.reference);}
      await batch.commit().timeout(const Duration(seconds:12));
    }
  }
  await ref.delete().timeout(const Duration(seconds:12));
}
