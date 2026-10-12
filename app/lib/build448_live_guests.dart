part of 'main.dart';

DocumentReference<Map<String,dynamic>> ngelx448GuestRef(String live,String uid)=>FirebaseFirestore.instance.collection('live_streams').doc(live).collection('guest_requests').doc(uid);
Future<void> ngelx448GuestAction(BuildContext context,String live,String owner,String guest,String action)async{
  final me=FirebaseAuth.instance.currentUser?.uid;if(me==null)return;
  if(action=='request'||action=='accept'){
    final permissions=await [Permission.microphone,Permission.camera].request();
    if(permissions.values.any((p)=>!p.isGranted)){if(context.mounted)ngelxDurumMesaji(context,'Yayına katılmak için kamera ve mikrofon izni gerekli.',tip:'uyari');return;}
  }
  try{
    await FirebaseFirestore.instance.runTransaction((tx)async{
      final liveRef=FirebaseFirestore.instance.collection('live_streams').doc(live);
      final ref=ngelx448GuestRef(live,guest);
      final l=await tx.get(liveRef),d=await tx.get(ref);
      final v=l.data()??<String,dynamic>{},old=d.data()??<String,dynamic>{};
      if(v['active']!=true||v['ownerId']!=owner||guest==owner)throw StateError('live_ended');
      final status=old['status'];
      String next;
      if(action=='request'&&me==guest)next='pending';
      else if(action=='invite'&&me==owner)next='invited';
      else if(action=='accept'&&((status=='pending'&&me==owner)||(status=='invited'&&me==guest)))next='accepted';
      else if(action=='reject'&&(me==owner||me==guest))next='rejected';
      else throw StateError('invalid_transition');
      tx.set(ref,{'liveId':live,'hostUid':owner,'guestUid':guest,'status':next,'startedBy':next=='pending'?guest:next=='invited'?owner:old['startedBy'],'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
    });
  }catch(_){if(context.mounted)ngelxDurumMesaji(context,'Yayın katılım işlemi tamamlanamadı.',tip:'hata');}
}

class Ngelx448GuestControls extends StatelessWidget{
  final String liveId,ownerUid;final bool host;
  const Ngelx448GuestControls({super.key,required this.liveId,required this.ownerUid,required this.host});
  Future<void> _panel(BuildContext context)async{
    await showModalBottomSheet<void>(context:context,isScrollControlled:true,backgroundColor:Colors.white,builder:(c)=>Theme(data:ThemeData.light(),child:SafeArea(child:SizedBox(height:MediaQuery.sizeOf(c).height*.65,child:Column(children:[
      const ListTile(title:Text('Yayına katılım istekleri',style:TextStyle(fontWeight:FontWeight.w800))),
      Expanded(child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(stream:FirebaseFirestore.instance.collection('live_streams').doc(liveId).collection('guest_requests').snapshots(),builder:(_,snap){
        final docs=(snap.data?.docs??[]).where((d)=>['pending','invited','accepted'].contains(d.data()['status'])).toList();
        if(docs.isEmpty)return const Center(child:Text('Henüz katılım isteği yok. İzleyici listesinden davet edebilirsin.'));
        return ListView.builder(itemCount:docs.length,itemBuilder:(_,i){final d=docs[i],v=d.data();return FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(future:FirebaseFirestore.instance.collection('users').doc(d.id).get(),builder:(_,p){
          final name=(p.data?.data()?['displayName']??p.data?.data()?['username']??'İzleyici').toString();
          return ListTile(title:Text(name),subtitle:Text(v['status']=='accepted'?'Yayında':v['status']=='invited'?'Davet gönderildi':'Katılmak istiyor'),trailing:Row(mainAxisSize:MainAxisSize.min,children:[
            if(v['status']=='pending')IconButton(tooltip:'Yayına al',icon:const Icon(Icons.check,color:Colors.green),onPressed:()=>ngelx448GuestAction(c,liveId,ownerUid,d.id,'accept')),
            IconButton(tooltip:'Reddet / yayından indir',icon:const Icon(Icons.close,color:Colors.red),onPressed:()=>ngelx448GuestAction(c,liveId,ownerUid,d.id,'reject')),
          ]));
        });});
      })),
    ])))));
  }
  @override Widget build(BuildContext context){
    if(host)return IconButton.filledTonal(tooltip:'Yayına katılım istekleri',onPressed:()=>_panel(context),icon:const Icon(Icons.person_add_alt_1));
    final uid=FirebaseAuth.instance.currentUser?.uid;if(uid==null||ownerUid.isEmpty)return const SizedBox.shrink();
    return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:ngelx448GuestRef(liveId,uid).snapshots(),builder:(_,s){
      final status=s.data?.data()?['status'];
      if(status=='invited')return Wrap(spacing:8,children:[FilledButton.icon(onPressed:()=>ngelx448GuestAction(context,liveId,ownerUid,uid,'accept'),icon:const Icon(Icons.videocam),label:const Text('Yayın davetini kabul et')),TextButton(onPressed:()=>ngelx448GuestAction(context,liveId,ownerUid,uid,'reject'),child:const Text('Reddet'))]);
      return TextButton.icon(onPressed:()=>ngelx448GuestAction(context,liveId,ownerUid,uid,status=='pending'||status=='accepted'?'reject':'request'),icon:Icon(status=='accepted'?Icons.logout:Icons.pan_tool_alt),label:Text(status=='accepted'?'Yayından in':status=='pending'?'İsteği iptal et':'Yayına katılma isteği'));
    });
  }
}
