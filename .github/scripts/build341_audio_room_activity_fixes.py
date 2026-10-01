from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
main_path = ROOT / "app/lib/main.dart"
audio_path = ROOT / "app/lib/audio_live_rooms.dart"
pub_path = ROOT / "app/pubspec.yaml"

def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f"{label}: beklenen kaynak bulunamadi")
    return text.replace(old, new, 1)

main = main_path.read_text(encoding="utf-8")
audio = audio_path.read_text(encoding="utf-8")
pub = pub_path.read_text(encoding="utf-8")

main = replace_once(main, "defaultValue: '1.0.121'", "defaultValue: '1.0.122'", "version name")
main = replace_once(main, "defaultValue: '340'", "defaultValue: '341'", "build number")
pub = replace_once(pub, "version: 1.0.121+340", "version: 1.0.122+341", "pubspec version")

audio = replace_once(
    audio,
    "TextField(controller:baslik,maxLength:80,decoration:InputDecoration(labelText:'Oda başlığı',filled:true,fillColor:const Color(0xFFF5F5F8),border:OutlineInputBorder(borderRadius:BorderRadius.circular(18),borderSide:BorderSide.none)))",
    "TextField(controller:baslik,maxLength:80,cursorColor:mor,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w800),decoration:InputDecoration(labelText:'Oda başlığı',labelStyle:const TextStyle(color:Colors.black54,fontWeight:FontWeight.w700),floatingLabelStyle:const TextStyle(color:mor,fontWeight:FontWeight.w800),hintText:'Örn. Akşam sohbeti',hintStyle:const TextStyle(color:Color(0xFF9A9AA2)),counterStyle:const TextStyle(color:Colors.black45),filled:true,fillColor:const Color(0xFFF5F5F8),enabledBorder:OutlineInputBorder(borderRadius:BorderRadius.circular(18),borderSide:const BorderSide(color:Color(0xFFE5E2EA))),focusedBorder:OutlineInputBorder(borderRadius:BorderRadius.circular(18),borderSide:const BorderSide(color:mor,width:1.5)),border:OutlineInputBorder(borderRadius:BorderRadius.circular(18),borderSide:BorderSide.none)))",
    "audio title field contrast",
)

audio = replace_once(
    audio,
    "Map<String,dynamic> veri={};bool mikrofon=false,bitti=false,kapatiliyor=false,yeniden=false;String durum='';",
    "Map<String,dynamic> veri={};bool mikrofon=false,mikrofonTercihi=false,bitti=false,kapatiliyor=false,yeniden=false;String durum='';",
    "audio connection state fields",
)

audio = replace_once(
    audio,
    "String? get uid=>FirebaseAuth.instance.currentUser?.uid;bool get sahibiyim=>uid==widget.ownerId;List<String> get speakers=>List<String>.from(veri['speakerIds']??const[]);bool get konusmaciyim=>uid!=null&&speakers.contains(uid);",
    "String? get uid=>FirebaseAuth.instance.currentUser?.uid;bool get sahibiyim=>uid==widget.ownerId;List<String> get speakers=>List<String>.from(veri['speakerIds']??const[]);bool get konusmaciyim=>uid!=null&&speakers.contains(uid);bool get bagli=>widget.oda.connectionState==lk.ConnectionState.connected;",
    "audio connected getter",
)

audio = replace_once(
    audio,
    "@override void initState(){super.initState();mikrofon=widget.yayinSahibi;widget.oda.addListener(odaDegisti);",
    "@override void initState(){super.initState();mikrofon=widget.yayinSahibi;mikrofonTercihi=widget.yayinSahibi;widget.oda.addListener(odaDegisti);",
    "audio init microphone preference",
)

audio = replace_once(
    audio,
    "void odaDegisti(){if(mounted)setState((){});if(widget.oda.connectionState==lk.ConnectionState.disconnected&&!kapatiliyor&&!bitti)unawaited(tekrarBaglan());}",
    """void odaDegisti(){
    if(!mounted)return;
    final koptu=widget.oda.connectionState==lk.ConnectionState.disconnected;
    if(koptu&&mikrofon)mikrofon=false;
    setState((){
      if(koptu&&!kapatiliyor&&!bitti)durum='Bağlantı koptu. Yeniden bağlanılıyor...';
      if(!koptu&&bagli)durum='';
    });
    if(koptu&&!kapatiliyor&&!bitti)unawaited(tekrarBaglan());
  }""",
    "audio disconnect listener",
)

old_reconnect = "Future<void> tekrarBaglan()async{if(yeniden||kapatiliyor||bitti)return;yeniden=true;for(var i=1;i<=3;i++){if(mounted)setState(()=>durum='Tekrar bağlanılıyor $i/3');try{await Future.delayed(Duration(milliseconds:500*i));await widget.oda.connect(widget.serverUrl,widget.participantToken).timeout(const Duration(seconds:10));if(konusmaciyim&&mikrofon)await widget.oda.localParticipant?.setMicrophoneEnabled(true);yeniden=false;if(mounted)setState(()=>durum='');return;}catch(_){}}yeniden=false;if(mounted)setState(()=>durum='Bağlantı kurulamadı.');}"
new_reconnect = """Future<void> tekrarBaglan()async{
    if(yeniden||kapatiliyor||bitti)return;
    final user=FirebaseAuth.instance.currentUser;if(user==null)return;
    yeniden=true;
    for(var i=1;i<=4;i++){
      if(mounted)setState(()=>durum='Tekrar bağlanılıyor $i/4');
      try{
        await Future.delayed(Duration(milliseconds:450*i));
        final d=await FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId).get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:8));
        final v=d.data()??<String,dynamic>{};
        if(!d.exists||v['active']!=true){bitti=true;throw StateError('audio_room_ended');}
        final roomName=(v['roomName']??'').toString();if(roomName.isEmpty)throw StateError('room_name');
        final p=(await FirebaseFirestore.instance.collection('users').doc(user.uid).get()).data()??<String,dynamic>{};
        final ad=(p['displayName']??p['username']??user.displayName??'NgelX').toString();
        final cevap=await lk.DevelopmentTokenSource(id:liveKitTestSunucuId).fetch(lk.TokenRequestOptions(roomName:roomName,participantIdentity:user.uid,participantName:ad,participantAttributes:{'role':sahibiyim?'host':'listener','mode':'audio'}));
        await widget.oda.connect(cevap.serverUrl,cevap.participantToken).timeout(const Duration(seconds:12));
        final micAcik=konusmaciyim&&mikrofonTercihi;
        await widget.oda.localParticipant?.setMicrophoneEnabled(micAcik);
        yeniden=false;
        if(mounted)setState((){mikrofon=micAcik;durum='';});
        return;
      }catch(_){}
    }
    yeniden=false;
    if(mounted)setState((){mikrofon=false;durum=bitti?'Bu sesli oda sona erdi.':'Bağlantı kurulamadı. Tekrar denemek için dokun.';});
  }"""
audio = replace_once(audio, old_reconnect, new_reconnect, "audio reconnect reliability")

audio = replace_once(
    audio,
    "Future<void> mic()async{if(!konusmaciyim)return;final yeni=!mikrofon;if(yeni&&!(await Permission.microphone.request()).isGranted)return;try{await widget.oda.localParticipant?.setMicrophoneEnabled(yeni);if(mounted)setState(()=>mikrofon=yeni);}catch(_){}}",
    """Future<void> mic()async{
    if(!konusmaciyim)return;
    if(!bagli){if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Ses bağlantısı yok. Yeniden bağlanılıyor...')));unawaited(tekrarBaglan());return;}
    final yeni=!mikrofonTercihi;
    if(yeni&&!(await Permission.microphone.request()).isGranted)return;
    try{
      await widget.oda.localParticipant?.setMicrophoneEnabled(yeni);
      if(mounted)setState((){mikrofonTercihi=yeni;mikrofon=yeni;});
    }catch(_){
      if(mounted)setState(()=>mikrofon=false);
      unawaited(tekrarBaglan());
    }
  }""",
    "audio microphone sync",
)

old_requests = "Future<void> istekler()async{if(!sahibiyim)return;await showModalBottomSheet<void>(context:context,backgroundColor:Colors.white,showDragHandle:true,builder:(c)=>SizedBox(height:420,child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(stream:FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId).collection('speaker_requests').where('status',isEqualTo:'pending').limit(30).snapshots(),builder:(_,s){final docs=s.data?.docs??[];if(docs.isEmpty)return const Center(child:Text('Bekleyen söz isteği yok.'));return ListView.builder(itemCount:docs.length,itemBuilder:(_,i){final d=docs[i],v=d.data();return ListTile(title:Text((v['displayName']??'NgelX').toString()),trailing:Wrap(children:[IconButton(onPressed:()=>istekSonuc(d.id,true),icon:const Icon(Icons.check,color:Colors.green)),IconButton(onPressed:()=>istekSonuc(d.id,false),icon:const Icon(Icons.close,color:Colors.red))]));});}))));}"
new_requests = """Future<void> istekler()async{
    if(!sahibiyim)return;
    await showModalBottomSheet<void>(
      context:context,
      backgroundColor:Colors.white,
      showDragHandle:true,
      shape:const RoundedRectangleBorder(borderRadius:BorderRadius.vertical(top:Radius.circular(26))),
      builder:(c)=>Theme(
        data:ThemeData.light().copyWith(scaffoldBackgroundColor:Colors.white),
        child:SafeArea(
          top:false,
          child:SizedBox(
            height:320,
            child:Column(children:[
              Padding(
                padding:const EdgeInsets.fromLTRB(18,0,10,8),
                child:Row(children:[
                  const Icon(Icons.pan_tool_alt_rounded,color:mor),
                  const SizedBox(width:9),
                  const Expanded(child:Text('Söz istekleri',style:TextStyle(color:Colors.black87,fontSize:18,fontWeight:FontWeight.w900))),
                  IconButton(tooltip:'Kapat',onPressed:()=>Navigator.pop(c),icon:const Icon(Icons.close_rounded,color:Colors.black54)),
                ]),
              ),
              const Divider(height:1,color:Color(0xFFEDE8F2)),
              Expanded(
                child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
                  stream:FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId).collection('speaker_requests').where('status',isEqualTo:'pending').limit(30).snapshots(),
                  builder:(_,s){
                    if(s.connectionState==ConnectionState.waiting)return const Center(child:CircularProgressIndicator(color:mor));
                    if(s.hasError)return const Center(child:Padding(padding:EdgeInsets.all(24),child:Column(mainAxisSize:MainAxisSize.min,children:[Icon(Icons.cloud_off_rounded,color:Colors.redAccent,size:36),SizedBox(height:8),Text('İstekler yüklenemedi.',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w900)),SizedBox(height:3),Text('Bağlantını kontrol edip tekrar dene.',style:TextStyle(color:Colors.black45))])));
                    final docs=s.data?.docs??[];
                    if(docs.isEmpty)return const Center(child:Padding(padding:EdgeInsets.all(24),child:Column(mainAxisSize:MainAxisSize.min,children:[Icon(Icons.pan_tool_alt_outlined,color:mor,size:38),SizedBox(height:9),Text('Bekleyen söz isteği yok',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w900)),SizedBox(height:3),Text('Bir dinleyici söz istediğinde burada görünecek.',textAlign:TextAlign.center,style:TextStyle(color:Colors.black45))])));
                    return ListView.separated(
                      padding:const EdgeInsets.symmetric(vertical:6),
                      itemCount:docs.length,
                      separatorBuilder:(_,__)=>const Divider(height:1,indent:70,color:Color(0xFFF0EDF3)),
                      itemBuilder:(_,i){
                        final d=docs[i],v=d.data(),foto=(v['photoUrl']??'').toString();
                        return ListTile(
                          leading:CircleAvatar(backgroundColor:const Color(0xFFF0E8FF),backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person,color:mor):null),
                          title:Text((v['displayName']??'NgelX').toString(),style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w900)),
                          subtitle:const Text('Konuşmacı olmak istiyor',style:TextStyle(color:Colors.black45)),
                          trailing:Wrap(spacing:2,children:[
                            IconButton(tooltip:'Kabul et',onPressed:()=>istekSonuc(d.id,true),icon:const Icon(Icons.check_circle_rounded,color:Colors.green)),
                            IconButton(tooltip:'Reddet',onPressed:()=>istekSonuc(d.id,false),icon:const Icon(Icons.cancel_rounded,color:Colors.redAccent)),
                          ]),
                        );
                      },
                    );
                  },
                ),
              ),
            ]),
          ),
        ),
      ),
    );
  }"""
audio = replace_once(audio, old_requests, new_requests, "audio request sheet")

audio = replace_once(
    audio,
    "style:const TextStyle(fontSize:10.5,fontWeight:FontWeight.w900))",
    "style:const TextStyle(color:Colors.black87,fontSize:10.5,fontWeight:FontWeight.w900))",
    "audio owner/speaker name contrast",
)

audio = replace_once(
    audio,
    "actions:[if(sahibiyim)IconButton(onPressed:istekler,icon:const Icon(Icons.pan_tool_alt_rounded,color:mor))]",
    "actions:[if(sahibiyim)IconButton(tooltip:'Söz istekleri',onPressed:istekler,icon:const Icon(Icons.pan_tool_alt_rounded,color:mor))]",
    "audio request icon tooltip",
)

audio = replace_once(
    audio,
    "if(durum.isNotEmpty)Container(width:double.infinity,padding:const EdgeInsets.all(8),color:const Color(0xFFFFF5D9),child:Text(durum,textAlign:TextAlign.center,style:const TextStyle(fontWeight:FontWeight.w800)))",
    "if(durum.isNotEmpty)InkWell(onTap:!yeniden&&!bitti?()=>unawaited(tekrarBaglan()):null,child:Container(width:double.infinity,padding:const EdgeInsets.all(9),color:const Color(0xFFFFF5D9),child:Row(mainAxisAlignment:MainAxisAlignment.center,children:[Icon(bitti?Icons.stop_circle_outlined:Icons.wifi_off_rounded,size:18,color:bitti?Colors.redAccent:Colors.black54),const SizedBox(width:7),Flexible(child:Text(durum,textAlign:TextAlign.center,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)))])))",
    "audio reconnect banner",
)

audio = replace_once(
    audio,
    "onPressed:konusmaciyim&&!bitti?mic:null,icon:Icon(mikrofon?Icons.mic:Icons.mic_off),label:Text(konusmaciyim?(mikrofon?'Mikrofon açık':'Mikrofon kapalı'):'Dinleyici'))",
    "onPressed:konusmaciyim&&!bitti&&bagli?mic:null,icon:Icon(mikrofon?Icons.mic:Icons.mic_off),label:Text(!bagli?'Bağlantı bekleniyor':konusmaciyim?(mikrofon?'Mikrofon açık':'Mikrofon kapalı'):'Dinleyici'))",
    "audio microphone button disconnected state",
)

old_activity = """          final birlesik=<String,QueryDocumentSnapshot<Map<String,dynamic>>>{};
          for(final d in s.data?.docs??<QueryDocumentSnapshot<Map<String,dynamic>>>[])birlesik[d.id]=d;
          for(final d in _sunucuAktiviteleri)birlesik[d.id]=d;
          final gelenDocs=birlesik.values.toList();
          int bildirimZamani(QueryDocumentSnapshot<Map<String,dynamic>> d){
            final ham=d.data()['createdAt'];
            return ham is Timestamp?ham.millisecondsSinceEpoch:0;
          }"""
new_activity = """          int bildirimZamani(QueryDocumentSnapshot<Map<String,dynamic>> d){
            final ham=d.data()['createdAt'];
            return ham is Timestamp?ham.millisecondsSinceEpoch:0;
          }
          String bildirimTekrarAnahtari(QueryDocumentSnapshot<Map<String,dynamic>> d){
            final v=d.data();
            final eventId=(v['eventId']??v['dedupeKey']??'').toString();
            if(eventId.isNotEmpty)return 'event:$eventId';
            final ham=v['createdAt'];
            if(ham is! Timestamp)return 'doc:'+d.id;
            final actor=(v['fromUid']??v['senderId']??v['actorUid']??v['userId']??'').toString();
            final hedef=(v['groupId']??v['chatId']??v['postId']??v['storyId']??v['callId']??v['messageId']??'').toString();
            final tur=(v['type']??v['kind']??v['notificationType']??'').toString();
            final metin=(v['body']??v['message']??v['text']??v['title']??'').toString();
            final zamanKovasi=ham.millisecondsSinceEpoch~/15000;
            return '$tur|$actor|$hedef|$metin|$zamanKovasi';
          }
          final birlesik=<String,QueryDocumentSnapshot<Map<String,dynamic>>>{};
          for(final d in s.data?.docs??<QueryDocumentSnapshot<Map<String,dynamic>>>[])birlesik[d.id]=d;
          for(final d in _sunucuAktiviteleri)birlesik[d.id]=d;
          final tekil=<String,QueryDocumentSnapshot<Map<String,dynamic>>>{};
          for(final d in birlesik.values){
            final anahtar=bildirimTekrarAnahtari(d),onceki=tekil[anahtar];
            if(onceki==null||bildirimZamani(d)>bildirimZamani(onceki))tekil[anahtar]=d;
          }
          final gelenDocs=tekil.values.toList();"""
main = replace_once(main, old_activity, new_activity, "activity duplicate filter")

main = replace_once(
    main,
    """          final tekil=<String,QueryDocumentSnapshot<Map<String,dynamic>>>{};
          for(final d in birlesik.values){
            final anahtar=bildirimTekrarAnahtari(d),onceki=tekil[anahtar];
            if(onceki==null||bildirimZamani(d)>bildirimZamani(onceki))tekil[anahtar]=d;
          }
          final gelenDocs=tekil.values.toList();""",
    """          final tekilOlay=<String,QueryDocumentSnapshot<Map<String,dynamic>>>{};
          for(final d in birlesik.values){
            final anahtar=bildirimTekrarAnahtari(d),onceki=tekilOlay[anahtar];
            if(onceki==null||bildirimZamani(d)>bildirimZamani(onceki))tekilOlay[anahtar]=d;
          }
          final gelenDocs=tekilOlay.values.toList();""",
    "activity local dedupe variable collision",
)

main_path.write_text(main, encoding="utf-8")
audio_path.write_text(audio, encoding="utf-8")
pub_path.write_text(pub, encoding="utf-8")

print("Build 341 audio room + activity fixes applied")
