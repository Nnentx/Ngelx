part of 'main.dart';

/// Resolve semantic content before the sender. Ignore empty legacy aliases.
({String kind, String id}) ngelx563NoticeTarget(Map<String,dynamic> data) {
  if(ngelx561IsCommunity(data)) {
    return (kind:'community',id:ngelx561First(data,['communityId','sourceId','belgeId','targetId']));
  }
  final type=ngelx561First(data,['type','kind','notificationType']).toLowerCase();
  final event=ngelx561First(data,['eventKind']).toLowerCase();
  final target=ngelx561First(data,['targetKind']).toLowerCase();
  if(['like','comment','interaction','video_like','post_like','post_comment','video_comment'].contains(type)||
      ['post','video','photo','content'].contains(target)||
      ['post_like','post_comment','video_like','video_comment','comment_reply','comment_like'].contains(event)) {
    return (kind:'content',id:ngelx561First(data,['postId','contentId','videoId','sourceId','belgeId','targetId']));
  }
  return (kind:'other',id:'');
}

Future<bool> ngelx563OpenContentNotice(BuildContext context,Map<String,dynamic> data) async {
  final target=ngelx563NoticeTarget(data);
  if(target.kind=='other')return false;
  if(!context.mounted)return true;
  if(target.id.isEmpty) {
    ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Bu bildirimin içerik bağlantısı bulunamadı.')));
    return true;
  }
  await Navigator.push(context,MaterialPageRoute(builder:(_)=>target.kind=='community'
    ?NgelXCommunityDetail450(id:target.id):IcerikBaglantiPage(icerikId:target.id)));
  return true;
}

Future<void> ngelx563OpenNotice(BuildContext context,Map<String,dynamic> data) async {
  if(await ngelx563OpenContentNotice(context,data)||!context.mounted)return;
  final type=ngelx561First(data,['type','kind','notificationType']);
  final event=ngelx561First(data,['eventKind']);
  if(type=='call'||event=='group_audio_call'||event=='group_video_call') {
    await ngelx445OpenCallChat(context,data);return;
  }
  final from=ngelx561First(data,['fromUid','senderId','senderUid','userId']);
  if(from.isNotEmpty)await Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:from)));
}

/// The keyboard reduces the modal viewport once; the input never animates a
/// second full keyboard-sized padding inside an already constrained Column.
class Ngelx563CommentViewport extends StatelessWidget {
  final Widget child;
  const Ngelx563CommentViewport({super.key,required this.child});
  @override Widget build(BuildContext context) {
    final keyboard=MediaQuery.viewInsetsOf(context).bottom;
    final height=MediaQuery.sizeOf(context).height;
    return LayoutBuilder(builder:(context,box) {
      final available=math.max(0.0,box.maxHeight-keyboard);
      return Padding(
        padding:EdgeInsets.only(bottom:keyboard),
        child:SizedBox(
          height:math.min(height*.72,available),
          child:MediaQuery.removeViewInsets(context:context,removeBottom:true,child:child),
        ),
      );
    });
  }
}
