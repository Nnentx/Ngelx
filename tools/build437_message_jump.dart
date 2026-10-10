// Fetch a bounded context window around search results, including old messages.
// The existing chat renderer remains responsible for media, permissions and deletes.
mixin Ngelx437MessageJump<T extends StatefulWidget> on State<T> {
  String get jumpChatId;
  ScrollController get jumpScroll;
  final Map<String,QueryDocumentSnapshot<Map<String,dynamic>>> _jumpDocs={};
  final GlobalKey _jumpKey=GlobalKey();
  String? _jumpId;
  bool _jumpMoving=false;
  int _jumpGeneration=0;

  List<QueryDocumentSnapshot<Map<String,dynamic>>> jumpMerge(Iterable<QueryDocumentSnapshot<Map<String,dynamic>>> recent){
    final all={..._jumpDocs,for(final d in recent)d.id:d};
    final result=all.values.toList();
    result.sort((a,b){
      int time(QueryDocumentSnapshot<Map<String,dynamic>> d){final v=d.data(),t=v['createdAt']??v['clientCreatedAt'];return t is Timestamp?t.millisecondsSinceEpoch:0;}
      final order=time(a).compareTo(time(b));return order==0?a.id.compareTo(b.id):order;
    });
    return result;
  }
  Key jumpRowKey(String id)=>id==_jumpId?_jumpKey:ValueKey(id);
  bool get jumpActive=>_jumpId!=null;

  Future<void> jumpToMessage(Object? result)async{
    if(result is! String||result.isEmpty||!mounted)return;
    final generation=++_jumpGeneration;
    try{
      final ref=FirebaseFirestore.instance.collection('chats').doc(jumpChatId).collection('messages');
      final target=await ref.doc(result).get().timeout(const Duration(seconds:10));
      if(!mounted||generation!=_jumpGeneration)return;
      final stamp=target.data()?['createdAt'];
      if(!target.exists||stamp is! Timestamp||!ngelx435MesajErisilebilir(target.data()??{},FirebaseAuth.instance.currentUser?.uid)||ngelx437MessageExpired(stamp,DateTime.now()))throw StateError('Mesaj artık görüntülenemiyor.');
      final windows=await Future.wait([
        ref.orderBy('createdAt').endAt([stamp]).limitToLast(25).get(),
        ref.orderBy('createdAt').startAt([stamp]).limit(25).get(),
      ]).timeout(const Duration(seconds:12));
      if(!mounted||generation!=_jumpGeneration)return;
      final around={for(final w in windows)for(final d in w.docs)d.id:d};
      // Same-timestamp ties must not drop the selected document.
      if(!around.containsKey(result)){
        final exact=await ref.where(FieldPath.documentId,isEqualTo:result).limit(1).get();
        if(!mounted||generation!=_jumpGeneration)return;
        for(final d in exact.docs)around[d.id]=d;
      }
      setState((){_jumpDocs..clear()..addAll(around);_jumpId=result;_jumpMoving=true;});
      await WidgetsBinding.instance.endOfFrame;
      if(!mounted||!jumpScroll.hasClients)return;
      jumpScroll.jumpTo(0);
      // Lazy variable-height rows are located by materializing one viewport at a time.
      for(var attempt=0;attempt<160;attempt++){
        await WidgetsBinding.instance.endOfFrame;
        if(!mounted||generation!=_jumpGeneration||!jumpScroll.hasClients)return;
        final row=_jumpKey.currentContext;
        if(row!=null){
          await Scrollable.ensureVisible(row,alignment:.35,duration:const Duration(milliseconds:220));
          return;
        }
        final p=jumpScroll.position;
        final next=(p.pixels+p.viewportDimension*.65).clamp(0.0,p.maxScrollExtent).toDouble();
        if(next<=p.pixels)break;
        jumpScroll.jumpTo(next);
      }
      if(mounted)ngelxDurumMesaji(context,'Mesaj konumu yüklenemedi. Tekrar dene.',tip:'uyari');
    }catch(e){if(mounted)ngelxDurumMesaji(context,e is StateError?e.message.toString():ngelx436Error(e),tip:'hata');}
    finally{if(mounted&&generation==_jumpGeneration)setState(()=>_jumpMoving=false);}
  }
  Widget jumpHighlight(String id,Widget child)=>DecoratedBox(
    decoration:BoxDecoration(color:id==_jumpId?const Color(0x222478FF):Colors.transparent,borderRadius:BorderRadius.circular(12)),child:child);
}
