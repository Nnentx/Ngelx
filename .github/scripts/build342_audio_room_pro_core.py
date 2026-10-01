from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
main_path=ROOT/'app/lib/main.dart'
audio_path=ROOT/'app/lib/audio_live_rooms.dart'
pub_path=ROOT/'app/pubspec.yaml'
rules_path=ROOT/'firestore.rules'

def rep(text,old,new,label):
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f'{label}: kaynak bulunamadi')
    return text.replace(old,new,1)

main=main_path.read_text(encoding='utf-8')
audio=audio_path.read_text(encoding='utf-8')
pub=pub_path.read_text(encoding='utf-8')
rules=rules_path.read_text(encoding='utf-8')

# Imports/parts and version.
if "package:share_plus/share_plus.dart" not in main:
    p=main.find("part '")
    if p<0: raise SystemExit('first part directive missing')
    main=main[:p]+"import 'package:share_plus/share_plus.dart';\n"+main[p:]
if "package:flutter/services.dart" not in main:
    p=main.find("part '")
    if p<0: raise SystemExit('first part directive missing for services')
    main=main[:p]+"import 'package:flutter/services.dart';\n"+main[p:]

main=rep(main,"part 'audio_live_rooms.dart';","part 'audio_live_rooms.dart';\npart 'audio_live_rooms_pro.dart';",'audio pro part')
main=rep(main,"defaultValue: '1.0.122'","defaultValue: '1.0.123'",'version name')
main=rep(main,"defaultValue: '341'","defaultValue: '342'",'build number')
pub=rep(pub,'version: 1.0.122+341','version: 1.0.123+342','pubspec version')

# Listener profile registration.
audio=rep(
    audio,
    "final ad=(p['displayName']??p['username']??user.displayName??'NgelX').toString();",
    "final ad=(p['displayName']??p['username']??user.displayName??'NgelX').toString(),foto=(p['photoUrl']??'').toString();",
    'listener profile fields',
)
audio=rep(
    audio,
    "await oda.localParticipant?.setMicrophoneEnabled(false);\n    if(!context.mounted)",
    "await oda.localParticipant?.setMicrophoneEnabled(false);\n    await ngelxSesliKatilimciYaz(roomId:odaId,uid:user.uid,ad:ad,foto:foto,rol:'listener');\n    if(!context.mounted)",
    'listener participant register',
)

# Host participant registration.
host_doc="final d=await FirebaseFirestore.instance.collection('audio_rooms').add({'roomName':roomName,'ownerId':user.uid,'ownerName':ad,'ownerPhotoUrl':foto,'title':baslik.text.trim(),'category':kategori,'visibility':gizlilik,'active':true,'startedAt':FieldValue.serverTimestamp(),'lastHeartbeatAt':FieldValue.serverTimestamp(),'speakerIds':[user.uid],'moderatorIds':<String>[],'speakerCount':1,'listenerCount':0,'maxSpeakers':ngelxSesliMaksKonusmaci,'maxModerators':ngelxSesliMaksModerator,'mode':'audio'});"
audio=rep(
    audio,
    host_doc,
    host_doc+"\n      await ngelxSesliKatilimciYaz(roomId:d.id,uid:user.uid,ad:ad,foto:foto,rol:'speaker');",
    'host participant register',
)

# State and roles.
audio=rep(
    audio,
    "Timer? heartbeat;StreamSubscription<DocumentSnapshot<Map<String,dynamic>>>? abonelik;Map<String,dynamic> veri={};",
    "Timer? heartbeat;StreamSubscription<DocumentSnapshot<Map<String,dynamic>>>? abonelik;StreamSubscription<DocumentSnapshot<Map<String,dynamic>>>? katilimAboneligi;Map<String,dynamic> veri={};",
    'participant subscription field',
)
audio=rep(
    audio,
    "String? get uid=>FirebaseAuth.instance.currentUser?.uid;bool get sahibiyim=>uid==widget.ownerId;List<String> get speakers=>List<String>.from(veri['speakerIds']??const[]);bool get konusmaciyim=>uid!=null&&speakers.contains(uid);bool get bagli=>widget.oda.connectionState==lk.ConnectionState.connected;",
    "String? get uid=>FirebaseAuth.instance.currentUser?.uid;bool get sahibiyim=>uid==widget.ownerId;List<String> get speakers=>List<String>.from(veri['speakerIds']??const[]);List<String> get moderatorler=>List<String>.from(veri['moderatorIds']??const[]);bool get moderatorum=>uid!=null&&moderatorler.contains(uid);bool get yoneticiyim=>sahibiyim||moderatorum;bool get konusmaciyim=>uid!=null&&speakers.contains(uid);bool get bagli=>widget.oda.connectionState==lk.ConnectionState.connected;",
    'moderator getters',
)

# Participant kick listener.
init_tail="});if(widget.yayinSahibi){unawaited(kalp());heartbeat=Timer.periodic(const Duration(seconds:6),(_)=>unawaited(kalp()));}}"
audio=rep(
    audio,
    init_tail,
    "});final ben=uid;if(ben!=null){katilimAboneligi=FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId).collection('participants').doc(ben).snapshots().listen((d){final v=d.data();if(v!=null&&v['removed']==true&&!sahibiyim&&!kapatiliyor)unawaited(odadanCikarildi());});}if(widget.yayinSahibi){unawaited(kalp());heartbeat=Timer.periodic(const Duration(seconds:6),(_)=>unawaited(kalp()));}}",
    'participant kick subscription',
)

marker="  void odaDegisti(){"
insert="""  Future<void> odadanCikarildi()async{
    if(kapatiliyor)return;
    kapatiliyor=true;
    mikrofon=false;mikrofonTercihi=false;
    try{await widget.oda.localParticipant?.setMicrophoneEnabled(false);}catch(_){}
    try{await widget.oda.disconnect();}catch(_){}
    if(mounted){
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Oda yöneticisi seni odadan çıkardı.')));
      Navigator.pop(context);
    }
  }
"""
if insert not in audio:
    if marker not in audio: raise SystemExit('room changed marker missing')
    audio=audio.replace(marker,insert+marker,1)

# Heartbeat and peak count for host, presence heartbeat for everyone.
old_kalp="  Future<void> kalp()async{if(!widget.yayinSahibi||kapatiliyor||bitti)return;try{await FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId).set({'lastHeartbeatAt':FieldValue.serverTimestamp(),'listenerCount':widget.oda.remoteParticipants.length,'speakerCount':speakers.isEmpty?1:speakers.length},SetOptions(merge:true));}catch(_){}}"
new_kalp="""  Future<void> kalp()async{
    if(kapatiliyor||bitti)return;
    final ben=uid;
    if(ben!=null){
      try{await FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId).collection('participants').doc(ben).set({'active':true,'lastSeenAt':FieldValue.serverTimestamp()},SetOptions(merge:true));}catch(_){}
    }
    if(!widget.yayinSahibi)return;
    try{
      final dinleyici=widget.oda.remoteParticipants.length;
      final onceki=(veri['peakListenerCount'] is num)?(veri['peakListenerCount'] as num).toInt():0;
      await FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId).set({
        'lastHeartbeatAt':FieldValue.serverTimestamp(),
        'listenerCount':dinleyici,
        'peakListenerCount':dinleyici>onceki?dinleyici:onceki,
        'speakerCount':speakers.isEmpty?1:speakers.length,
      },SetOptions(merge:true));
    }catch(_){}
  }"""
audio=rep(audio,old_kalp,new_kalp,'heartbeat presence')

# Reconnect original-token fallback before fresh token.
needle="""      try{
        await Future.delayed(Duration(milliseconds:450*i));
        final d=await FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId).get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:8));"""
replacement="""      try{
        await Future.delayed(Duration(milliseconds:450*i));
        if(i==1){
          try{
            await widget.oda.connect(widget.serverUrl,widget.participantToken).timeout(const Duration(seconds:10));
            final micAcik=konusmaciyim&&mikrofonTercihi;
            await widget.oda.localParticipant?.setMicrophoneEnabled(micAcik);
            yeniden=false;
            if(mounted)setState((){mikrofon=micAcik;durum='';});
            return;
          }catch(_){}
        }
        final d=await FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId).get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:8));"""
audio=rep(audio,needle,replacement,'reconnect fallback')

# Moderators can open and process requests.
audio=rep(audio,"    if(!sahibiyim)return;\n    await showModalBottomSheet<void>","    if(!yoneticiyim)return;\n    await showModalBottomSheet<void>",'request moderator guard')

# Sort and number hand requests.
audio=rep(
    audio,
    "final docs=s.data?.docs??[];\n                    if(docs.isEmpty)",
    "final docs=(s.data?.docs??[]).toList()..sort((a,b){final aa=a.data()['createdAt'],bb=b.data()['createdAt'];final am=aa is Timestamp?aa.millisecondsSinceEpoch:0,bm=bb is Timestamp?bb.millisecondsSinceEpoch:0;return am.compareTo(bm);});\n                    if(docs.isEmpty)",
    'request order sort',
)
audio=rep(
    audio,
    "return ListTile(\n                          leading:CircleAvatar(backgroundColor:const Color(0xFFF0E8FF),backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person,color:mor):null),",
    "return ListTile(\n                          leading:Stack(clipBehavior:Clip.none,children:[CircleAvatar(backgroundColor:const Color(0xFFF0E8FF),backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person,color:mor):null),Positioned(right:-5,bottom:-5,child:CircleAvatar(radius:9,backgroundColor:mor,child:Text('${i+1}',style:const TextStyle(color:Colors.white,fontSize:9,fontWeight:FontWeight.w900))))]),",
    'request order badge',
)

# Owner/mod request actions.
audio=rep(audio,"actions:[if(sahibiyim)IconButton(tooltip:'Söz istekleri'","actions:[if(yoneticiyim)IconButton(tooltip:'Söz istekleri'",'appbar moderator requests')
audio=rep(audio,"const Spacer(),if(sahibiyim)TextButton.icon(onPressed:istekler","const Spacer(),if(yoneticiyim)TextButton.icon(onPressed:istekler",'stage moderator requests')

# End/leave tracks duration and participant state.
old_bitir="  Future<void> bitir()async{if(!sahibiyim)return;final ok=await showDialog<bool>(context:context,builder:(c)=>AlertDialog(title:const Text('Sesli oda bitsin mi?'),actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),FilledButton(onPressed:()=>Navigator.pop(c,true),child:const Text('Bitir'))]));if(ok!=true)return;kapatiliyor=true;heartbeat?.cancel();await FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId).set({'active':false,'endedAt':FieldValue.serverTimestamp(),'endReason':'host_ended'},SetOptions(merge:true));final ben=uid;if(ben!=null)await FirebaseFirestore.instance.collection('users').doc(ben).set({'isAudioLive':false,'currentAudioRoomId':FieldValue.delete()},SetOptions(merge:true));try{await widget.oda.disconnect();}catch(_){}if(mounted)Navigator.pop(context);}"
new_bitir="""  Future<void> bitir()async{
    if(!sahibiyim)return;
    final ok=await showDialog<bool>(context:context,builder:(c)=>AlertDialog(title:const Text('Sesli oda bitsin mi?'),actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),FilledButton(onPressed:()=>Navigator.pop(c,true),child:const Text('Bitir'))]));
    if(ok!=true)return;
    kapatiliyor=true;heartbeat?.cancel();
    final bas=veri['startedAt'];
    final sure=bas is Timestamp?DateTime.now().difference(bas.toDate()).inSeconds:0;
    await FirebaseFirestore.instance.collection('audio_rooms').doc(widget.odaId).set({'active':false,'endedAt':FieldValue.serverTimestamp(),'durationSeconds':sure<0?0:sure,'endReason':'host_ended'},SetOptions(merge:true));
    final ben=uid;
    if(ben!=null){
      await ngelxSesliKatilimciAyril(widget.odaId,ben);
      await FirebaseFirestore.instance.collection('users').doc(ben).set({'isAudioLive':false,'currentAudioRoomId':FieldValue.delete()},SetOptions(merge:true));
    }
    try{await widget.oda.disconnect();}catch(_){}
    if(mounted)Navigator.pop(context);
  }"""
audio=rep(audio,old_bitir,new_bitir,'room end stats')

old_ayril="  Future<void> ayril()async{if(sahibiyim){await bitir();return;}kapatiliyor=true;try{await widget.oda.disconnect();}catch(_){}if(mounted)Navigator.pop(context);}"
new_ayril="""  Future<void> ayril()async{
    if(sahibiyim){await bitir();return;}
    kapatiliyor=true;
    final ben=uid;if(ben!=null)await ngelxSesliKatilimciAyril(widget.odaId,ben);
    try{await widget.oda.disconnect();}catch(_){}
    if(mounted)Navigator.pop(context);
  }"""
audio=rep(audio,old_ayril,new_ayril,'participant leave')

# Duration + pro toolbar + reactions.
old_head="Text(bitti?'SONA ERDİ':'SESLİ CANLI',style:TextStyle(color:bitti?Colors.redAccent:mor,fontWeight:FontWeight.w900)),const Spacer(),const Icon(Icons.headphones,size:17,color:Colors.black45),Text(' ${widget.oda.remoteParticipants.length}',style:const TextStyle(fontWeight:FontWeight.w800))"
new_head="Text(bitti?'SONA ERDİ':'SESLİ CANLI',style:TextStyle(color:bitti?Colors.redAccent:mor,fontWeight:FontWeight.w900)),const SizedBox(width:8),NgelxSesliSureSayaci(baslangic:veri['startedAt'] is Timestamp?(veri['startedAt'] as Timestamp).toDate():null,bitti:bitti),const Spacer(),const Icon(Icons.headphones,size:17,color:Colors.black45),Text(' ${widget.oda.remoteParticipants.length}',style:const TextStyle(fontWeight:FontWeight.w800))"
audio=rep(audio,old_head,new_head,'duration counter header')

toolbar_marker="])),const SizedBox(height:14),Row(children:[const Text('Sahne'"
toolbar_new="""])),NgelxSesliTepkiAkisi(roomId:widget.odaId),const SizedBox(height:10),Wrap(spacing:8,runSpacing:8,children:[
  OutlinedButton.icon(onPressed:()=>ngelxSesliKatilimcilarAc(context,widget.odaId,widget.ownerId),icon:const Icon(Icons.headphones_rounded,size:18),label:const Text('Dinleyiciler')),
  OutlinedButton.icon(onPressed:()=>ngelxSesliSohbetAc(context,widget.odaId,yoneticiyim),icon:const Icon(Icons.chat_bubble_outline_rounded,size:18),label:const Text('Sohbet')),
  PopupMenuButton<String>(
    tooltip:'Tepki gönder',
    onSelected:(x)=>ngelxSesliTepkiGonder(widget.odaId,x),
    itemBuilder:(_)=>['❤️','👏','😂','🔥','🎉'].map((x)=>PopupMenuItem(value:x,child:Text(x,style:const TextStyle(fontSize:24)))).toList(),
    child:Container(padding:const EdgeInsets.symmetric(horizontal:12,vertical:8),decoration:BoxDecoration(border:Border.all(color:const Color(0xFFD5CEDD)),borderRadius:BorderRadius.circular(20)),child:const Row(mainAxisSize:MainAxisSize.min,children:[Icon(Icons.add_reaction_outlined,size:18,color:mor),SizedBox(width:6),Text('Tepki',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w700))])),
  ),
  OutlinedButton.icon(onPressed:()=>ngelxSesliPaylas(context,widget.odaId,(veri['title']??widget.baslik).toString()),icon:const Icon(Icons.ios_share_rounded,size:18),label:const Text('Davet')),
]),const SizedBox(height:14),Row(children:[const Text('Sahne'"""
audio=rep(audio,toolbar_marker,toolbar_new,'audio pro toolbar')

# Dispose cleanup.
audio=rep(
    audio,
    "heartbeat?.cancel();abonelik?.cancel();widget.oda.removeListener(odaDegisti);",
    "heartbeat?.cancel();abonelik?.cancel();katilimAboneligi?.cancel();widget.oda.removeListener(odaDegisti);",
    'participant sub dispose',
)
audio=rep(
    audio,
    "if(!widget.yayinSahibi)unawaited(widget.oda.disconnect());unawaited(widget.oda.dispose());super.dispose();",
    "final ben=uid;if(ben!=null&&!bitti)unawaited(ngelxSesliKatilimciAyril(widget.odaId,ben));if(!widget.yayinSahibi)unawaited(widget.oda.disconnect());unawaited(widget.oda.dispose());super.dispose();",
    'participant leave dispose',
)

# Firestore audio room update: moderators can manage speaker stage only.
old_room_update="""      allow update: if signedIn()
        && resource.data.ownerId == request.auth.uid
        && request.resource.data.get('speakerIds', []).size() <= 12
        && request.resource.data.get('moderatorIds', []).size() <= 3;"""
new_room_update="""      allow update: if signedIn()
        && request.resource.data.get('speakerIds', []).size() <= 12
        && request.resource.data.get('moderatorIds', []).size() <= 3
        && (
          resource.data.ownerId == request.auth.uid
          || (
            request.auth.uid in resource.data.get('moderatorIds', [])
            && request.resource.data.diff(resource.data).affectedKeys().hasOnly(['speakerIds', 'speakerCount', 'updatedAt'])
          )
        );"""
rules=rep(rules,old_room_update,new_room_update,'audio moderator room update')

# New audio subcollections.
rules_marker="""      match /speaker_requests/{uid} {
        allow read: if signedIn() && (
          isMe(uid)
          || get(/databases/$(database)/documents/audio_rooms/$(roomId)).data.get('ownerId', '') == request.auth.uid
          || request.auth.uid in get(/databases/$(database)/documents/audio_rooms/$(roomId)).data.get('moderatorIds', [])
        );
        allow create: if isMe(uid)
          && request.resource.data.get('userId', '') == request.auth.uid
          && request.resource.data.get('status', '') == 'pending';
        allow update: if signedIn() && (
          (
            isMe(uid)
            && request.resource.data.get('userId', '') == request.auth.uid
            && request.resource.data.get('status', '') in ['pending', 'cancelled']
          )
          || get(/databases/$(database)/documents/audio_rooms/$(roomId)).data.get('ownerId', '') == request.auth.uid
          || request.auth.uid in get(/databases/$(database)/documents/audio_rooms/$(roomId)).data.get('moderatorIds', [])
        );
        allow delete: if signedIn() && (
          isMe(uid)
          || get(/databases/$(database)/documents/audio_rooms/$(roomId)).data.get('ownerId', '') == request.auth.uid
        );
      }"""
rules_insert=rules_marker+"""
      match /participants/{uid} {
        allow read: if signedIn();
        allow create: if isMe(uid)
          && request.resource.data.get('userId', '') == request.auth.uid
          && (
            request.resource.data.get('role', 'listener') == 'listener'
            || get(/databases/$(database)/documents/audio_rooms/$(roomId)).data.get('ownerId', '') == request.auth.uid
          );
        allow update: if signedIn() && (
          (
            isMe(uid)
            && request.resource.data.diff(resource.data).affectedKeys().hasOnly(['active', 'lastSeenAt', 'leftAt', 'joinedAt', 'displayName', 'photoUrl'])
          )
          || get(/databases/$(database)/documents/audio_rooms/$(roomId)).data.get('ownerId', '') == request.auth.uid
          || request.auth.uid in get(/databases/$(database)/documents/audio_rooms/$(roomId)).data.get('moderatorIds', [])
        );
        allow delete: if false;
      }
      match /messages/{messageId} {
        allow read: if signedIn();
        allow create: if signedIn()
          && request.resource.data.get('userId', '') == request.auth.uid
          && request.resource.data.get('text', '') is string
          && request.resource.data.get('text', '').size() <= 600;
        allow update: if signedIn()
          && (
            get(/databases/$(database)/documents/audio_rooms/$(roomId)).data.get('ownerId', '') == request.auth.uid
            || request.auth.uid in get(/databases/$(database)/documents/audio_rooms/$(roomId)).data.get('moderatorIds', [])
          )
          && request.resource.data.diff(resource.data).affectedKeys().hasOnly(['pinned', 'updatedAt']);
        allow delete: if signedIn() && (
          resource.data.get('userId', '') == request.auth.uid
          || get(/databases/$(database)/documents/audio_rooms/$(roomId)).data.get('ownerId', '') == request.auth.uid
          || request.auth.uid in get(/databases/$(database)/documents/audio_rooms/$(roomId)).data.get('moderatorIds', [])
        );
      }
      match /reactions/{reactionId} {
        allow read: if signedIn();
        allow create: if signedIn()
          && request.resource.data.get('userId', '') == request.auth.uid
          && request.resource.data.get('emoji', '') is string;
        allow update: if false;
        allow delete: if signedIn() && (
          resource.data.get('userId', '') == request.auth.uid
          || get(/databases/$(database)/documents/audio_rooms/$(roomId)).data.get('ownerId', '') == request.auth.uid
        );
      }"""
rules=rep(rules,rules_marker,rules_insert,'audio pro subcollections')

main_path.write_text(main,encoding='utf-8')
audio_path.write_text(audio,encoding='utf-8')
pub_path.write_text(pub,encoding='utf-8')
rules_path.write_text(rules,encoding='utf-8')
print('Build 342 audio room pro core patch applied')
