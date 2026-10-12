from pathlib import Path
p=Path('app/lib/main.dart');s=p.read_text()
assert "part 'build445_inbox_model.dart';" not in s
s="import 'build445_inbox_policy.dart';\n"+s
s=s.replace("part 'story_v66.dart';","part 'story_v66.dart';\npart 'build445_inbox_model.dart';",1)
s=s.replace('final ngelxCallSession444=NgelxCallSession444();','final ngelxCallSession444=NgelxCallSession444()..onChanged=ngelx445CallChanged;',1)
s=s.replace('const NgelxSesliMiniGlobalOverlay()]','const NgelxSesliMiniGlobalOverlay(),const Ngelx445CallOverlay()]',1)
s=s.replace('Future<void> ngelxArkaPlanAramayiTemizle(String roomName)async{','Future<void> ngelxArkaPlanAramayiTemizle(String roomName)async{\n  ngelx445CallDetails.remove(roomName);\n  ngelx445CallChanged();',1)
s=s.replace("    final durum=(v['callStatus']??'').toString();\n    final kayitliOda=(v['callRoomName']??'').toString();","    final durum=(v['callStatus']??'').toString();\n    final connected445=v['callConnectedAt'];\n    if(connected445 is Timestamp&&v['callRoomName']==roomName){_ngelxArkaPlanAramaBaslangiclari[roomName]=connected445.toDate();}\n    final kayitliOda=(v['callRoomName']??'').toString();",1)
s=s.replace('  _ngelxArkaPlanAramaOdalari[roomName]=room;','  _ngelxArkaPlanAramaOdalari[roomName]=room;\n  ngelx445CallChanged();',1)
s=s.replace('  final room=_ngelxArkaPlanAramaOdalari.remove(roomName);\n  if(room==null)return null;','  final room=_ngelxArkaPlanAramaOdalari.remove(roomName);\n  ngelx445CallDetails.remove(roomName);\n  ngelx445CallChanged();\n  if(room==null)return null;',1)
s=s.replace('      oda=arkaPlan.room;','      oda=arkaPlan.room;\n      mikrofon=arkaPlan.room.localParticipant?.isMicrophoneEnabled()??true;\n      kamera=arkaPlan.room.localParticipant?.isCameraEnabled()??widget.goruntulu;\n      hoparlor=lk.AudioManager.instance.isSpeakerOutputPreferred;',1)
s=s.replace('      ngelxArkaPlanAramaSakla(\n        roomName:widget.roomName,',"      ngelx445CallDetails[widget.roomName]=(title:widget.baslik,photo:widget.foto,uid:FirebaseAuth.instance.currentUser?.uid??'',video:widget.goruntulu,ref:widget.aramaRef);\n      ngelxArkaPlanAramaSakla(\n        roomName:widget.roomName,",1)
s=s.replace('  await FirebaseAuth.instance.signOut();\n  ngelxKokRotayaDon();','  for(final name in _ngelxArkaPlanAramaOdalari.keys.toList()){await ngelx445EndBackground(name);}\n  await FirebaseAuth.instance.signOut();\n  ngelxKokRotayaDon();',1)
a=s.index('class _MesajPageState');b=s.index('\nclass ArsivSohbetlerPage',a);region=s[a:b]
region=region.replace('  final sohbetAra=TextEditingController();','  final sohbetAra=TextEditingController();\n  final _search445=FocusNode();',1)
region=region.replace('sohbetAra.dispose();super.dispose();','sohbetAra.dispose();_search445.dispose();super.dispose();',1)
region=region.replace("sekme('Tümü',bildirimler+istekler+mesajlar+gruplar)","sekme('Tümü',ngelx445AllUnread(mesajlar,gruplar))",1)
region=region.replace("      ?tumIcerigi()","      ?sohbetlerIcerigi()",1)
# Existing helper hides pending requests based on the application's privacy model.
region=region.replace("            if(filtre=='Mesajlar'&&grup)return false;\n            if(filtre=='Gruplar'&&!grup)return false;", "            if(!ngelx445ChatFilter(filtre,group:grup,pending:ngelxBekleyenMesajIstegi(v,ben??'',arkadaslar),hidden:false))return false;",1)
region=region.replace('fontSize:30,fontWeight:FontWeight.w900','fontSize:30,fontWeight:FontWeight.w900',1)
region=region.replace('onPressed:()=>setState(()=>_aramaAcik=!_aramaAcik),','onPressed:()=>_search445.requestFocus(),',1)
region=region.replace('icon:Icon(_aramaAcik?Icons.close_rounded:Icons.search_rounded,color:const Color(0xFF07142E),size:29),','icon:const Icon(Icons.search_rounded,color:mor,size:27),',1)
region=region.replace('icon:const Icon(Icons.add_rounded,color:Color(0xFF07142E),size:32),','icon:const Icon(Icons.add_circle_rounded,color:mor,size:32),',1)
# Move permanently visible search before filter row; keep all existing filtered search logic.
start=region.index('            AnimatedSwitcher(\n              duration:const Duration(milliseconds:160),',region.index('    return Theme('))
end=region.index('            Expanded(child:RefreshIndicator',start)
region=region[:start]+region[end:]
marker='''            Padding(
              padding:const EdgeInsets.fromLTRB(12,0,12,10),
              child:ngelxSekmeliSayaclar(),
            ),'''
assert marker in region
region=region.replace(marker,'''            Padding(padding:const EdgeInsets.fromLTRB(16,0,16,14),child:TextField(
              key:const ValueKey('inbox-search445'),focusNode:_search445,controller:sohbetAra,
              onChanged:(v)=>setState(()=>sohbetSorgu=v.trim().toLowerCase()),
              style:const TextStyle(color:Color(0xFF111827),fontSize:14),
              decoration:InputDecoration(
                hintText:filtre=='İstekler'?lt('İsteklerde ara','Search requests'):filtre=='Bildirimler'?lt('Bildirimlerde ara','Search notifications'):t('searchChats'),
                prefixIcon:const Icon(Icons.search_rounded,color:Color(0xFF8C879D)),
                contentPadding:const EdgeInsets.symmetric(horizontal:16,vertical:12),
                filled:true,fillColor:const Color(0xFFF3F0F9),
                border:OutlineInputBorder(borderRadius:BorderRadius.circular(20),borderSide:BorderSide.none),
              ),
            )),
'''+marker+'''
            if(ben!=null)Ngelx445FriendsStrip(key:ValueKey('inbox-friends445-'+ben),uid:ben),
            const Ngelx445InboxCallBanner(),''',1)
# Inline notification cards also route call events to the chat, without joining.
region=region.replace("                  try{await d.reference.update({'read':true,'readAt':FieldValue.serverTimestamp()});}catch(_){}\n                  final from=(v['fromUid']??'').toString();","                  unawaited(d.reference.update({'read':true,'readAt':FieldValue.serverTimestamp()}).timeout(const Duration(seconds:5)).catchError((_){ }));\n                  final event=(v['eventKind']??'').toString();\n                  if(tur=='call'||event=='group_audio_call'||event=='group_video_call'){if(context.mounted)await ngelx445OpenCallChat(context,v);return;}\n                  final from=(v['fromUid']??'').toString();",1)
# Rows retain tap/long-press/archive/mute and unread behavior, with approved colors and spacing.
region=region.replace('Color(0xFF1678F4),shape:BoxShape.circle','Color(0xFF8249ED),shape:BoxShape.circle')
region=region.replace('EdgeInsets.symmetric(horizontal:4,vertical:5)','EdgeInsets.symmetric(horizontal:4,vertical:8)')
region=region.replace('fontSize:15.5,fontWeight:unread','fontSize:16,fontWeight:unread')
# Thin separators preserve the approved conversation list geometry.
start=region.index('    Widget sohbetlerIcerigi(){');end=region.index('    Widget govde=',start)
rows=region[start:end].replace('return ListView.builder(', 'return ListView.separated(',1)
rows=rows.replace('itemCount:satirlar.length,','itemCount:satirlar.length,\n                separatorBuilder:(_,__)=>const Divider(height:1,thickness:.7,indent:68,color:Color(0xFFEDEAF5)),',1)
# Wrap unread/time trailing widgets with a live return action only for the
# currently owned minimized call; the conversation row still opens the chat.
position=0
while True:
 found=rows.find('trailing:SizedBox(',position)
 if found<0:break
 opening=rows.index('(',found);depth=0;quote=None;i=opening
 while i<len(rows):
  char=rows[i]
  if quote:
   if char=='\\':i+=2;continue
   if char==quote:quote=None
  elif char in ["'",'"']:quote=char
  elif char=='(':depth+=1
  elif char==')':
   depth-=1
   if depth==0:break
  i+=1
 assert depth==0
 widget=rows[found+len('trailing:'):i+1]
 replacement='trailing:ngelx445CallTrailing(v,'+widget+')'
 rows=rows[:found]+replacement+rows[i+1:];position=found+len(replacement)
region=region[:start]+rows+region[end:]
# Delete the obsolete merged renderer so notifications cannot accidentally return to All.
start=region.index('    Widget tumIcerigi(){');end=region.index('    Widget sohbetlerIcerigi(){',start)
region=region[:start]+region[end:]
s=s[:a]+region+s[b:]
# A private-call notification opens its conversation rather than the sender profile.
marker="    if(kaynak.isNotEmpty&&(tur=='interaction'||tur=='like'||tur=='comment')){"
assert marker in s
s=s.replace(marker,"""    if(tur=='call'&&kaynak.isNotEmpty&&hedefTuru!='group'){
      try{
        final d=await FirebaseFirestore.instance.collection('chats').doc(kaynak).get().timeout(const Duration(seconds:8));
        final cv=d.data()??<String,dynamic>{},me=FirebaseAuth.instance.currentUser?.uid;
        final members=List<String>.from(cv['members']??const[]);
        if(me==null||!members.contains(me)||List<String>.from(cv['hiddenFor']??const[]).contains(me))return;
        final other=members.firstWhere((x)=>x!=me,orElse:()=>from);
        if(other.isEmpty)return;
        final user=await FirebaseFirestore.instance.collection('users').doc(other).get().timeout(const Duration(seconds:8));
        final profile=user.data()??<String,dynamic>{};
        if(context.mounted)Navigator.push(context,MaterialPageRoute(builder:(_)=>SohbetPage(chatId:kaynak,digerUid:other,ad:(profile['displayName']??profile['username']??'').toString(),foto:(profile['photoUrl']??'').toString())));
      }catch(_){if(context.mounted)ngelxDurumMesaji(context,lt('Sohbet açılamadı. Tekrar dene.','Could not open chat. Try again.'),tip:'hata');}
      return;
    }

"""+marker,1)
# Resuming one's minimized group call must not emit a second join event.
s=s.replace("    final oda=(v['callRoomName']??'').toString();\n    if(ben==null||oda.isEmpty)return;","    final oda=(v['callRoomName']??'').toString();\n    if(ben==null||oda.isEmpty)return;\n    if(ngelxCallSession444.room==oda&&ngelxCallSession444.background){await ngelx445ReturnCall(oda);return;}",1)
s=s.replace('child: Text(_ngelx438Ui("Katıl"),style:TextStyle(color:Colors.white,fontSize:10,fontWeight:FontWeight.w900)),', """child: Text(_ngelx438Ui(ngelxCallSession444.room==(tv['callRoomName']??'')&&ngelxCallSession444.background?"Aramaya dön":"Katıl"),style:TextStyle(color:Colors.white,fontSize:10,fontWeight:FontWeight.w900)),""",1)
# Reuse the established profile-to-chat preparation path, including existing IDs,
# message permissions and deterministic-ID collision recovery. Do not invent a
# second empty conversation when the user already has a chat with this contact.
signature='  Future<void> profildenMesajAc(BuildContext context,{required String ad,required String foto})async{'
start=s.index(signature);end=s.index('  Future<void> profiliPaylas(',start)
method=s[start:end]
helper=method.replace(signature,'Future<void> ngelx445OpenPrivateChat(BuildContext context,{required String uid,required String ad,required String foto})async{',1)
s=s[:start]+'  Future<void> profildenMesajAc(BuildContext context,{required String ad,required String foto})=>ngelx445OpenPrivateChat(context,uid:uid,ad:ad,foto:foto);\n\n'+s[end:]
s+='\n'+helper
p.write_text(s)
print('Build445 approved inbox integration applied; existing backend and conversations preserved')
