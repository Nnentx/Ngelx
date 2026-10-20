part of 'main.dart';

const _communityDeleteEndpoint543=String.fromEnvironment('NGELX_COMMUNITY_DELETE_URL');
final Set<String> _communityDeleting543={};
Future<void> ngelx543DeleteCommunity(BuildContext context,String id)async{
  if(_communityDeleting543.contains(id))return;
  final user=FirebaseAuth.instance.currentUser;
  if(user==null||user.isAnonymous)return;
  final ref=_communities450.doc(id);
  try{
    final value=(await ref.get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:10))).data();
    if(!context.mounted)return;
    if(value==null){Navigator.pop(context);return;}
    if(value['founderId']!=user.uid||!List<String>.from(value['members']??const[]).contains(user.uid)){
      ngelxDurumMesaji(context,'Topluluğu yalnızca mevcut kurucusu silebilir.',tip:'hata');return;
    }
    final endpoint=Uri.tryParse(_communityDeleteEndpoint543);
    if(endpoint==null||endpoint.scheme!='https'||endpoint.userInfo.isNotEmpty||
       !(endpoint.host.endsWith('.cloudfunctions.net')||endpoint.host.endsWith('.run.app'))){
      ngelxDurumMesaji(context,'Topluluğu tamamen silme hizmeti henüz etkin değil. Topluluğun silinmedi.',tip:'uyari');return;
    }
    final name=(value['name']??'').toString();
    final typed=await showDialog<String>(context:context,builder:(_)=>Ngelx543DeleteConfirmation(name:name));
    if(typed!=name||!context.mounted||FirebaseAuth.instance.currentUser?.uid!=user.uid)return;
    _communityDeleting543.add(id);
    final progress=showDialog<void>(context:context,barrierDismissible:false,builder:(_)=>const PopScope(canPop:false,
      child:AlertDialog(content:Row(children:[CircularProgressIndicator(),SizedBox(width:18),Expanded(child:Text('Topluluk ve bağlı kayıtları siliniyor…'))]))));
    try{
      final token=await user.getIdToken(true);
      if(token==null||FirebaseAuth.instance.currentUser?.uid!=user.uid)throw StateError('session_changed');
      final client=HttpClient()..connectionTimeout=const Duration(seconds:12);
      try{
        final request=await client.postUrl(endpoint).timeout(const Duration(seconds:15));
        request.headers.set(HttpHeaders.authorizationHeader,'Bearer $token');
        request.headers.contentType=ContentType.json;
        request.write(jsonEncode({'communityId':id,'confirmName':name,'confirmDelete':true}));
        final response=await request.close().timeout(const Duration(seconds:90));
        final body=jsonDecode(await utf8.decoder.bind(response).join().timeout(const Duration(seconds:10)));
        if(response.statusCode!=200||body is! Map||body['deleted']!=true)throw StateError('community_delete_not_confirmed');
      }finally{client.close(force:true);}
      if(context.mounted){Navigator.of(context,rootNavigator:true).pop();await progress;if(context.mounted)Navigator.pop(context);}
    }catch(error){
      if(context.mounted){Navigator.of(context,rootNavigator:true).pop();await progress;
        if(context.mounted)ngelxDurumMesaji(context,'Silme sonucu doğrulanamadı. Topluluk durumunu yenileyip tekrar dene.',tip:'hata');}
    }finally{_communityDeleting543.remove(id);}
  }catch(error){if(context.mounted)_communityError450(context,error);}
}
class Ngelx543DeleteConfirmation extends StatefulWidget{
  final String name;
  const Ngelx543DeleteConfirmation({super.key,required this.name});
  @override State<Ngelx543DeleteConfirmation> createState()=>_Ngelx543DeleteConfirmationState();
}
class _Ngelx543DeleteConfirmationState extends State<Ngelx543DeleteConfirmation>{
  final controller=TextEditingController();
  @override void dispose(){controller.dispose();super.dispose();}
  @override Widget build(BuildContext context)=>AlertDialog(
    title:const Text('Topluluğu tamamen sil?'),
    content:Column(mainAxisSize:MainAxisSize.min,crossAxisAlignment:CrossAxisAlignment.start,children:[
      const Text('Topluluk, gönderiler, yorumlar, istekler ve diğer bağlı kayıtlar kalıcı olarak silinir. Bu işlem geri alınamaz.'),
      const SizedBox(height:12),Text('Onaylamak için topluluk adını yaz: ${widget.name}'),
      TextField(controller:controller,onChanged:(_)=>setState((){}),decoration:const InputDecoration(labelText:'Topluluk adı')),
    ]),actions:[TextButton(onPressed:()=>Navigator.pop(context),child:const Text('Vazgeç')),
      FilledButton(style:FilledButton.styleFrom(backgroundColor:Colors.red),onPressed:controller.text==widget.name?()=>Navigator.pop(context,controller.text):null,child:const Text('Kalıcı olarak sil'))]);
}
