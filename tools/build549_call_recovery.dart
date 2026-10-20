part of 'main.dart';

bool ngelx549Quota(Object error)=>error is FirebaseException&&error.code=='resource-exhausted';
String ngelx549CallError(Object error){
  if(ngelx549Quota(error))return 'Arama hizmetinin sunucu kotası doldu. Şu anda aramaya bağlanılamıyor. Lütfen daha sonra tekrar dene.';
  if(error is TimeoutException)return 'Arama sunucusuna ulaşılamadı. Bağlantını kontrol edip tekrar dene.';
  if(error is FirebaseException&&error.code=='permission-denied')return 'Bu aramaya katılım izni doğrulanamadı.';
  return 'Arama işlemi tamamlanamadı. Görüşme hâlâ açıksa tekrar deneyebilirsin.';
}
void ngelx549CallNotice(Object error){
  final context=ngelxNavigatorKey.currentContext;
  if(context!=null&&context.mounted)ngelxDurumMesaji(context,ngelx549CallError(error),tip:'uyari');
}
final Map<String,Ngelx549RequestGate> _heartbeatGates549={};
Future<void> ngelx549Heartbeat(DocumentReference<Map<String,dynamic>> ref,String name,
    {required bool Function() alive})async{
  final uid=FirebaseAuth.instance.currentUser?.uid;
  if(uid==null||!alive())return;
  final key='$uid|$name';
  if(_heartbeatGates549.length>100)_heartbeatGates549.removeWhere((_,v)=>!v.running);
  final gate=_heartbeatGates549.putIfAbsent(key,Ngelx549RequestGate.new);
  if(!gate.enter(DateTime.now()))return;
  var quota=false;
  try{
    await FirebaseFirestore.instance.runTransaction((tx)async{
      if(!alive()||FirebaseAuth.instance.currentUser?.uid!=uid)return;
      final snap=await tx.get(ref),v=snap.data();
      if(!alive()||FirebaseAuth.instance.currentUser?.uid!=uid||v==null||
         v['callRoomName']!=name||!const {'ringing','active'}.contains(v['callStatus'])||
         !List<String>.from(v['members']??const[]).contains(uid)||
         !List<String>.from(v['callParticipants']??const[]).contains(uid))return;
      final stamp=v['callHeartbeatAt'];
      // Other participants may already have refreshed this shared heartbeat.
      if(stamp is Timestamp&&DateTime.now().difference(stamp.toDate()).inSeconds<50)return;
      tx.update(ref,{'callHeartbeatAt':FieldValue.serverTimestamp()});
    },maxAttempts:2);
  }catch(error){quota=ngelx549Quota(error);}
  finally{gate.finish(DateTime.now(),quota:quota);}
}
final Map<String,DateTime> _leaveRetryAfter549={};
Object? ngelx549LastLeaveError;
