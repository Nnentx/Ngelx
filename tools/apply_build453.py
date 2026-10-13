from pathlib import Path

def replace_once(s, old, new):
    assert old in s, old[:100]
    return s.replace(old,new,1)

p=Path('app/lib/main.dart');s=p.read_text()
s="import 'package:flutter/foundation.dart';\n"+s
s=replace_once(s,"part 'build448_incoming_calls.dart';","part 'build448_incoming_calls.dart';\npart 'build453_widgets.dart';")
a=s.index('class NgelXSohbetFotoOnizleme');b=s.index('class NgelXSohbetVideoOnizleme',a)
s=s[:a]+"class NgelXSohbetFotoOnizleme extends StatelessWidget{final String url;const NgelXSohbetFotoOnizleme({super.key,required this.url});@override Widget build(BuildContext context)=>Ngelx453Photo(url:url);}\n\n"+s[b:]
s=s.replace('constraints:const BoxConstraints(maxWidth:290)', 'constraints:BoxConstraints(maxWidth:math.min(340.0,MediaQuery.sizeOf(context).width*.8))')
# Dispatch directly after a committed call message, independently of inbox query limits.
needle="      await callMessageRef.set({"
position=0
while True:
    start=s.find(needle,position)
    if start<0:break
    end=s.find('},SetOptions(merge:true));',start)
    if end<0:break
    end+=len('},SetOptions(merge:true));')
    s=s[:end]+"\n      unawaited(ngelx448Incoming.dispatchCommitted453(callMessageRef.parent.parent!));"+s[end:]
    position=end+110
# Private calls use a transactional batch instead of callMessageRef.
a=s.index("      final aramaVerisi=<String,dynamic>{")
b=s.index("      if(!mounted)return;",a)
s=s[:b]+"      unawaited(ngelx448Incoming.dispatchCommitted453(ref));\n"+s[b:]
# Sender metadata for new group message previews, with no extra blocking profile read.
s=s.replace("final g=<String,dynamic>{'lastMessage':sonMesaj,", "final g=<String,dynamic>{'lastSenderId':ben,'lastMessageKind':veri['type']??'text','lastMessage':sonMesaj,",1)
a=s.index('class _MesajPageState');b=s.index('\nclass ArsivSohbetlerPage',a);inbox=s[a:b]
inbox=replace_once(inbox,"  String? get uid=>", "  final Map<String,Stream<DocumentSnapshot<Map<String,dynamic>>>> _profiles453={};\n  String? get uid=>")
inbox=inbox.replace("stream:FirebaseFirestore.instance.collection('users').doc(other).snapshots(),", "stream:_profiles453.putIfAbsent(other,()=>FirebaseFirestore.instance.collection('users').doc(other).snapshots()),")
inbox=inbox.replace('fontSize:30,fontWeight:FontWeight.w900,letterSpacing:-.8','fontSize:26,fontWeight:FontWeight.w800,letterSpacing:-.6')
inbox=inbox.replace('unread>0?FontWeight.w900:FontWeight.w800','unread>0?FontWeight.w800:FontWeight.w500')
inbox=inbox.replace('horizontal:4,vertical:8','horizontal:4,vertical:5')
inbox=inbox.replace('Ngelx434AktifAvatar(uid:other,','Ngelx434AktifAvatar(radius:30,uid:other,')
inbox=inbox.replace("Text((v['lastMessage']??t('groupCreated')).toString(),maxLines:1,\n                        overflow:TextOverflow.ellipsis,style:const TextStyle(color:Color(0xFF7C86A0),fontSize:13))", "Ngelx453InboxPreview(chat:v,me:ben??'',unread:unread>0)")
inbox=inbox.replace("subtitle:Text((v['lastMessage']??t('newChat')).toString(),maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Color(0xFF7C86A0),fontSize:13))", "subtitle:Text((v['lastMessage']??t('newChat')).toString(),maxLines:1,overflow:TextOverflow.ellipsis,style:TextStyle(color:unread>0?const Color(0xFF252B36):const Color(0xFF727886),fontSize:14,fontWeight:unread>0?FontWeight.w700:FontWeight.w400))")
old="""return StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
            stream:ben==null?null:FirebaseFirestore.instance.collection('group_archives').doc(ben).collection('items').limit(30).snapshots(),
            builder:(_,eskiSnap){"""
inbox=replace_once(inbox,old,"return Builder(builder:(_){")
s=s[:a]+inbox+s[b:]
p.write_text(s)

p=Path('app/lib/build448_incoming_calls.dart');s=p.read_text()
s=replace_once(s,'class Ngelx448IncomingCalls {','class Ngelx448IncomingCalls with WidgetsBindingObserver {')
s=replace_once(s,'_started=true;','_started=true;WidgetsBinding.instance.addObserver(this);')
a=s.index('      try{\n        await Permission.notification.request();');b=s.index('      if(FirebaseAuth.instance.currentUser?.uid!=user.uid)return;',a)
s=s[:a]+"      unawaited(registerDevice453());\n"+s[b:]
pos=s.index('  final Set<String> _dispatch452=')
s=s[:pos]+"""  bool _registering453=false;
  @override void didChangeAppLifecycleState(AppLifecycleState state){if(state==AppLifecycleState.resumed)unawaited(registerDevice453());}
  Future<void> registerDevice453()async{
    final user=FirebaseAuth.instance.currentUser;if(user==null||user.isAnonymous||_registering453)return;
    _registering453=true;
    try{
      await Permission.notification.request();
      for(var n=0;n<3;n++){
        if(FirebaseAuth.instance.currentUser?.uid!=user.uid)return;
        try{
          final token=await channel.invokeMethod<String>('getPushToken');
          if(token==null||token.isEmpty)throw StateError('token_not_ready');
          if(FirebaseAuth.instance.currentUser?.uid!=user.uid)return;
          await FirebaseFirestore.instance.collection('_call_devices').doc(user.uid).collection('tokens').doc(token.hashCode.toUnsigned(32).toString()).set({'token':token,'uid':user.uid,'updatedAt':FieldValue.serverTimestamp()}).timeout(const Duration(seconds:8));
          return;
        }catch(_){if(n<2)await Future<void>.delayed(Duration(seconds:n+1));}
      }
    }finally{_registering453=false;}
  }
  Future<void> dispatchCommitted453(DocumentReference<Map<String,dynamic>> ref)async{
    final uid=FirebaseAuth.instance.currentUser?.uid;if(uid==null)return;
    try{final doc=await ref.get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:8));await _pushOutgoing452(ref.id,doc.data()??<String,dynamic>{},uid);}catch(_){}
  }
"""+s[pos:]
s=s.replace("if((response.statusCode??503)>=500)return false;","if((response.statusCode??503)>=500||response.statusCode==429)return false;")
p.write_text(s)

p=Path('app/lib/build445_inbox_model.dart');s=p.read_text()
s=s.replace('SizedBox(height:108,child:ListView.builder(', 'SizedBox(height:126,child:ListView.builder(').replace('itemExtent:66','itemExtent:84').replace('CircleAvatar(radius:23,','CircleAvatar(radius:32,').replace('fontSize:11,fontWeight:FontWeight.w600','fontSize:12.5,fontWeight:FontWeight.w600').replace('width:13,height:13','width:17,height:17').replace('width:18,height:18','width:22,height:22')
p.write_text(s)

p=Path('app/lib/live_broadcast_studio.dart');s=p.read_text()
start=s.index('class _CanliYayinPageState');head,body=s[:start],s[start:]
body=replace_once(body,'  final yorum = TextEditingController();',"""  final yorum = TextEditingController();
  final _commentFocus453=FocusNode();
  final _composerKey453=GlobalKey();
  final _hearts453=ValueNotifier<int>(0);
  StreamSubscription<QuerySnapshot<Map<String,dynamic>>>? _reactionSub453;
  final Map<String,int> _reactionCounts453={};
  final Map<String,Future<DocumentSnapshot<Map<String,dynamic>>>> _commentProfiles453={};
  bool _reactionsReady453=false;
  int _pendingHearts453=0;
""")
body=replace_once(body,'    widget.oda.addListener(_yenile);',"""    widget.oda.addListener(_yenile);
    _reactionSub453=FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('reactions').snapshots().listen((snapshot){
      for(final d in snapshot.docChanges){
        final count=(d.doc.data()?['count'] as num?)?.toInt()??0;
        final before=_reactionCounts453[d.doc.id]??0;
        _reactionCounts453[d.doc.id]=count;
        if(_reactionsReady453&&d.doc.id!=FirebaseAuth.instance.currentUser?.uid){
          for(var n=0;n<math.min(8,math.max(0,count-before));n++)_hearts453.value++;
        }
      }
      _reactionsReady453=true;
    },onError:(_){ });
""")
body=replace_once(body,'    yorum.dispose();',"    _reactionSub453?.cancel();\n    _hearts453.dispose();\n    _commentFocus453.dispose();\n    yorum.dispose();")
a=body.index('  Widget _yorumPaneli(){');b=body.index('  Future<void> _goruntuStudyoPaneli()',a)
body=body[:a]+Path('tools/build453_live_comments.fragment').read_text()+body[b:]
a=body.index('  Future<void> _kalpDegistir()');b=body.index('  Future<void> _yorumGonder()',a)
body=body[:a]+"""  Future<void> _kalpDegistir()async{
    final user=FirebaseAuth.instance.currentUser;if(user==null||kapatildi||yayinBitti)return;
    _hearts453.value++;_pendingHearts453++;
    if(kalpIsleniyor)return;kalpIsleniyor=true;
    final ref=FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('reactions').doc(user.uid);
    try{
      while(_pendingHearts453>0&&mounted&&!kapatildi&&!yayinBitti){
        final amount=_pendingHearts453;_pendingHearts453=0;
        await FirebaseFirestore.instance.runTransaction((tx)async{
          final d=await tx.get(ref),v=d.data()??<String,dynamic>{};
          tx.set(ref,{'uid':user.uid,'userId':user.uid,'type':'heart','count':((v['count'] as num?)?.toInt()??0)+amount,'updatedAt':FieldValue.serverTimestamp(),if(!d.exists)'createdAt':FieldValue.serverTimestamp()});
        });
        yerelKalpSerisi+=amount;
      }
    }catch(_){_pendingHearts453=0;if(mounted)ngelxDurumMesaji(context,'Beğeni gönderilemedi. Tekrar dene.',tip:'hata');}
    finally{kalpIsleniyor=false;}
  }

"""+body[b:]
# Keep the draft until the actual write succeeds; typing during the write is retained.
body=replace_once(body,'    yorum.clear();\n    final profil=', '    final profil=')
body=replace_once(body,"    sonYorumZamani=DateTime.now();", "    if(mounted&&yorum.text.trim()==metin)yorum.clear();\n    sonYorumZamani=DateTime.now();")
# Stronger role-specific header, without opening new streams for every comment update.
body=body.replace("Text('@$username • ${widget.baslik}'", "Text('@$username'")
body=body.replace("foregroundColor:Colors.white,backgroundColor:takipte?Colors.white12:const Color(0xFFFF1744)","foregroundColor:const Color(0xFF20C5CA),side:const BorderSide(color:Color(0xFF20C5CA)),backgroundColor:Colors.transparent")
body=body.replace('fontSize:12.5,fontWeight:FontWeight.w900','fontSize:16,fontWeight:FontWeight.w800')
body=body.replace('fontSize:10.5,fontWeight:FontWeight.w600','fontSize:12,fontWeight:FontWeight.w600')
body=body.replace('CircleAvatar(radius:18,backgroundImage:foto', 'CircleAvatar(radius:24,backgroundImage:foto')
a=body.index('  bool _liveTools451=false;');b=body.index('  @override\n  Widget build(BuildContext context)',a)
body=body[:a]+Path('tools/build453_live_controls.fragment').read_text()+body[b:]
body=replace_once(body,"          if(yayinBitti)Positioned.fill", "          if(!yayinBitti)Positioned(right:12,bottom:MediaQuery.of(context).viewInsets.bottom+(widget.yayinSahibi?220:172),child:Ngelx453Hearts(pulses:_hearts453)),\n          if(yayinBitti)Positioned.fill")
a=body.index('              Align(alignment:Alignment.centerLeft,child:_yorumPaneli()),');b=body.index('            ]),\n          )),',a)
body=body[:a]+Path('tools/build453_live_bottom.fragment').read_text()+body[b:]
p.write_text(head+body)
print('Build453 preserved architecture: stable live composer, approved role layouts, hearts, full-ratio photos and larger inbox avatars')
