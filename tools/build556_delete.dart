part of 'main.dart';

const _deleteEndpoint556=String.fromEnvironment('NGELX_COMMUNITY_DELETE_URL',defaultValue:'https://ngelx-live-moderation.alihancaglar76.workers.dev/community/delete');
bool _resumingDeletes556=false;
Timer? _deleteRetry556;
void _scheduleDeleteRetry556(){
  _deleteRetry556??=Timer.periodic(const Duration(seconds:30),(_)=>unawaited(ngelx556ResumeCommunityDeletes()));
}
String _deleteKey556(String uid,String id)=>'pending_community_delete_556_${uid}_$id';
Uri _deleteUri556(){
  final uri=Uri.parse(_deleteEndpoint556);
  if(uri.scheme!='https'||uri.userInfo.isNotEmpty||uri.host!='ngelx-live-moderation.alihancaglar76.workers.dev'||uri.path!='/community/delete'||uri.hasQuery||uri.hasFragment)throw StateError('delete_service_unavailable556');
  return uri;
}
Future<bool> _processDelete556(User user,String id,String name,{int maxChunks=48})async{
  final uri=_deleteUri556(),prefs=await SharedPreferences.getInstance();
  final deadline=DateTime.now().add(const Duration(seconds:75));
  final client=HttpClient()..connectionTimeout=const Duration(seconds:10);
  try{
    for(var chunk=0;chunk<maxChunks&&DateTime.now().isBefore(deadline);chunk++){
      if(FirebaseAuth.instance.currentUser?.uid!=user.uid)return false;
      final token=await user.getIdToken();if(token==null)return false;
      final request=await client.postUrl(uri).timeout(const Duration(seconds:12));
      request.headers.set(HttpHeaders.authorizationHeader,'Bearer $token');request.headers.contentType=ContentType.json;
      request.write(jsonEncode({'communityId':id,'confirmName':name,'confirmDelete':true}));
      final response=await request.close().timeout(const Duration(seconds:25));
      final raw=await utf8.decoder.bind(response).join().timeout(const Duration(seconds:8));
      if(response.statusCode==404||response.statusCode==405)throw StateError('delete_service_unavailable556');
      if(response.statusCode==401||response.statusCode==403){
        // A denied owner identity must not be retried as another account.
        await prefs.remove(_deleteKey556(user.uid,id));throw StateError('delete_permission556');
      }
      if(response.statusCode>=500||response.statusCode==429)return false;
      final decoded=jsonDecode(raw);
      if(response.statusCode==200&&decoded is Map&&decoded['deleted']==true){await prefs.remove(_deleteKey556(user.uid,id));return true;}
      if(response.statusCode!=202||decoded is! Map||decoded['pending']!=true)throw StateError('delete_not_confirmed556');
      await Future<void>.delayed(const Duration(milliseconds:800));
    }
    return false;
  }finally{client.close(force:true);}
}
Future<void> ngelx556DeleteCommunity(BuildContext context,String id)async{
  if(_communityDeleting543.contains(id))return;
  final user=FirebaseAuth.instance.currentUser;if(user==null||user.isAnonymous)return;
  bool queued=false;
  try{
    _deleteUri556();
    final value=(await _communities450.doc(id).get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:10))).data();
    if(!context.mounted)return;
    if(value==null){Navigator.maybePop(context);return;}
    if(value['founderId']!=user.uid||!List<String>.from(value['members']??const[]).contains(user.uid))throw StateError('delete_permission556');
    final name=(value['name']??'').toString();
    final typed=await showDialog<String>(context:context,builder:(_)=>Ngelx543DeleteConfirmation(name:name));
    if(typed!=name||!context.mounted||FirebaseAuth.instance.currentUser?.uid!=user.uid)return;
    final prefs=await SharedPreferences.getInstance();
    if(!await prefs.setString(_deleteKey556(user.uid,id),jsonEncode({'uid':user.uid,'id':id,'name':name})))throw StateError('delete_queue556');
    queued=true;
    _scheduleDeleteRetry556();
    _communityDeleting543.add(id);
    final navigator=Navigator.of(context,rootNavigator:true);
    final dialog=DialogRoute<void>(context:context,barrierDismissible:false,builder:(_)=>const PopScope(canPop:false,child:AlertDialog(
      content:Row(children:[CircularProgressIndicator(),SizedBox(width:16),Expanded(child:Text('Topluluk ve bağlı kayıtları siliniyor…'))]),
    )));
    unawaited(navigator.push(dialog));
    bool done=false;
    try{done=await _processDelete556(user,id,name);}
    finally{_communityDeleting543.remove(id);if(dialog.isActive)navigator.removeRoute(dialog);}
    if(!context.mounted)return;
    if(done){ngelxDurumMesaji(context,'Topluluk tamamen silindi.',tip:'basari');Navigator.maybePop(context);}
    else{ngelxDurumMesaji(context,'Silme işlemi kaydedildi. Bağlantı kurulduğunda arka planda tamamlanacak.',tip:'uyari');Navigator.maybePop(context);}
  }catch(error){
    _communityDeleting543.remove(id);
    if(context.mounted)ngelxDurumMesaji(context,error is StateError&&error.message=='delete_service_unavailable556'?'Topluluk silme hizmetine ulaşılamıyor.':error is StateError&&error.message=='delete_permission556'?'Topluluğu yalnızca mevcut kurucusu silebilir.':queued?'Silme tamamlanamadı. Kaydedilen işlem bağlantı kurulduğunda tekrar denenecek.':'Silme başlatılamadı. Bağlantını kontrol edip tekrar dene.',tip:'hata');
  }
}
Future<void> ngelx556ResumeCommunityDeletes()async{
  if(_resumingDeletes556)return;
  final user=FirebaseAuth.instance.currentUser;if(user==null||user.isAnonymous){_deleteRetry556?.cancel();_deleteRetry556=null;return;}
  _resumingDeletes556=true;
  try{
    final prefs=await SharedPreferences.getInstance(),prefix='pending_community_delete_556_${user.uid}_';
    final keys=prefs.getKeys().where((k)=>k.startsWith(prefix)).toList();
    if(keys.isEmpty){_deleteRetry556?.cancel();_deleteRetry556=null;return;}
    _scheduleDeleteRetry556();
    for(final key in keys){
      if(FirebaseAuth.instance.currentUser?.uid!=user.uid)return;
      final value=jsonDecode(prefs.getString(key)??'{}');if(value is! Map||value['uid']!=user.uid||value['id'] is! String||value['name'] is! String)continue;
      final id=value['id'] as String;
      if(!_communityDeleting543.add(id))continue;
      try{await _processDelete556(user,id,value['name'] as String,maxChunks:12);}catch(_){}
      finally{_communityDeleting543.remove(id);}
    }
  }catch(_){/* Local preference/network failures never block application startup. */}
  finally{_resumingDeletes556=false;}
}
