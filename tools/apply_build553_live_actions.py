from pathlib import Path
import sys
from apply_build553_live_review import once
TAG='// Build553 safe guest joins PK invitation feedback and gift effects'
def apply(root=Path('app')):
 p=root/'lib/live_broadcast_studio.dart';s=p.read_text()
 if TAG in s:return
 s=once(s,'  int _lastVisibleVideoSecond = 0;',Path('tools/build553_moderation_methods.dart').read_text()+'\n  int _lastVisibleVideoSecond = 0;')
 s=once(s,"      final yeniPk=v['pkActive']==true;",'''      final mods553=Set<String>.from(List<String>.from(v['moderatorUids553']??const[]));
      final until553=(v['commentMuteUntil553'] is Map)?v['commentMuteUntil553'][FirebaseAuth.instance.currentUser?.uid]:null;
      if(mounted&&(!setEquals(_moderators553,mods553)||_myCommentMute553!=until553))setState((){
        _moderators553=mods553;_myCommentMute553=until553 is Timestamp?until553:null;
      });
      final yeniPk=v['pkActive']==true;''')
 s=once(s,'  Widget _liveBottom540()=>Column(mainAxisSize:MainAxisSize.min,children:[','  Widget _liveBottom540()=>Column(mainAxisSize:MainAxisSize.min,children:[\n    _commentMuteBanner553(),')
 s=once(s,'      if(!widget.yayinSahibi&&\n         List<String>.from(v[','''      final until553=v['commentMuteUntil553'] is Map?v['commentMuteUntil553'][user.uid]:null;
      if(until553 is Timestamp&&until553.toDate().isAfter(DateTime.now())){
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Yorum susturman henüz bitmedi. Kalan süre ekranda gösteriliyor.')));return;
      }
      if(!widget.yayinSahibi&&
         List<String>.from(v[''')
 s=once(s,'                      trailing:widget.yayinSahibi&&uid.isNotEmpty','                      trailing:_canModerate553&&uid.isNotEmpty')
 a=s.index("                            if(secim=='mute'){");b=s.index('                          },\n                          itemBuilder:',a)
 s=s[:a]+"                            await _viewerAction553(uid,secim);\n"+s[b:]
 s=once(s,"                            const PopupMenuItem(value:'invite'", "                            if(widget.yayinSahibi)const PopupMenuItem(value:'invite'")
 s=once(s,"                            PopupMenuItem(value:'mute',child:ListTile(contentPadding:EdgeInsets.zero,leading:Icon(Icons.volume_off_rounded),title:Text('Yorumlarını sustur'))),",'''                            if(widget.yayinSahibi)const PopupMenuItem(value:'mute5',child:Text('Yorumları 5 dakika sustur')),
                            if(widget.yayinSahibi)const PopupMenuItem(value:'unmuteComment',child:Text('Yorum susturmasını kaldır')),
                            if(widget.yayinSahibi)PopupMenuItem(value:_moderators553.contains(uid)?'unmoderator':'moderator',child:Text(_moderators553.contains(uid)?'Moderatör yetkisini kaldır':'Moderatör seç')),''')
 s=once(s,"title:Text(ad.isEmpty?'NgelX izleyicisi':ad,style:","title:Text((_moderators553.contains(uid)?'🛡 Moderatör · ':'')+(ad.isEmpty?'NgelX izleyicisi':ad),style:")
 s=once(s,'    if(!widget.yayinSahibi)return;\n    final uid=(y[','    if(!_canModerate553)return;\n    final uid=(y[')
 s=once(s,'          onLongPress:widget.yayinSahibi?', '          onLongPress:_canModerate553?') if '          onLongPress:widget.yayinSahibi?' in s else s.replace('onLongPress:widget.yayinSahibi?()=>_yorumYonet','onLongPress:_canModerate553?()=>_yorumYonet')
 # Only host may pin or assign comment mutes; moderators may delete comments.
 a=s.index('  Future<void> _yorumYonet(');b=s.index('  bool _guestAudioMuted489',a)
 section=s[a:b].replace('        ListTile(\n          leading:const Icon(Icons.push_pin_rounded', '        if(widget.yayinSahibi)ListTile(\n          leading:const Icon(Icons.push_pin_rounded')
 section=section.replace("        if(uid.isNotEmpty&&uid!=widget.ownerId)ListTile(","        if(widget.yayinSahibi&&uid.isNotEmpty&&uid!=widget.ownerId)ListTile(")
 section=section.replace("await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).set({'mutedUsers':FieldValue.arrayUnion([uid])},SetOptions(merge:true));","await _viewerAction553(uid,'mute5');")
 section=section.replace("kullanıcısını sustur", "kullanıcısını 5 dakika sustur")
 s=s[:a]+section+s[b:]
 s=once(s,'children:[Text(name,maxLines:1,overflow:TextOverflow.ellipsis,style:',"children:[Text((_moderators553.contains((y['uid']??y['userId']??'').toString())?'🛡 ':'')+name,maxLines:1,overflow:TextOverflow.ellipsis,style:")
 s=once(s,'  // Build511 QA gift event animations.','  bool _reduceGiftEffects553=false;\n  // Build511 QA gift event animations.')
 s=once(s,'milliseconds:score>=25?3400:1750',"milliseconds:const ['Aslan','Evren','Galaksi'].contains(next['name'])?7000:score>=25?3400:1750")
 s=once(s,"    final big=gift?['big']==true;","""    final big=gift?['big']==true;
    if(gift!=null&&const ['Aslan','Evren','Galaksi'].contains(gift['name'])){
      return MediaQuery(data:MediaQuery.of(context).copyWith(disableAnimations:
        _reduceGiftEffects553||MediaQuery.disableAnimationsOf(context)),child:Ngelx553GiftEffect(
          key:ValueKey(_giftKey511),kind:gift['name'].toString(),sender:gift['sender'].toString(),
          quantity:(gift['quantity'] as num?)?.toInt()??1));
    }""")
 s=once(s,"      {'ad': 'Galaksi', 'emoji': '🌌', 'puan': 100},","""      {'ad': 'Galaksi', 'emoji': '🌌', 'puan': 100},
      {'ad': 'Aslan', 'emoji': '🦁', 'puan': 150},
      {'ad': 'Evren', 'emoji': '🪐', 'puan': 200},""")
 s=once(s,"          Row(children:[\n            const Text('Adet'", """          SwitchListTile.adaptive(contentPadding:EdgeInsets.zero,
            title:const Text('Hareketi azalt',style:TextStyle(color:Colors.white)),
            value:_reduceGiftEffects553,onChanged:(v){
              if(mounted)setState(()=>_reduceGiftEffects553=v);
              setGiftAmount((){});
            }),
          Row(children:[
            const Text('Adet'""")
 # Preserve the grid layout while fitting long gift labels.
 # Flexible gift content supports large accessibility text without fixed cell overflow.
 s=once(s,"                  child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [\n                    Text(h['emoji']", "                  child: FittedBox(fit:BoxFit.scaleDown,child:Column(mainAxisAlignment: MainAxisAlignment.center, children: [\n                    Text(h['emoji']")
 pos=s.index("                    Text(h['emoji']");end=s.index('                  ]),',pos);s=s[:end]+s[end:].replace('                  ]),','                  ])),',1)
 s=once(s,'  Future<bool> _geri() async {','''  DateTime? _guestBack553;
  bool _guestLeaving553=false;
  Future<bool> _geri() async {''')
 s=once(s,'    await _klavyeyiKapat();\n    if(widget.yayinSahibi){','''    if(_guestLeaving553)return false;
    if(!widget.yayinSahibi&&(_guestActive448||_guestWanted448)){
      if(MediaQuery.viewInsetsOf(context).bottom>0){await _klavyeyiKapat();return false;}
      final now=DateTime.now();
      if(_guestBack553==null||now.difference(_guestBack553!)>const Duration(seconds:5)){
        _guestBack553=now;
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
          content:Text('Konukluktan ayrılacaksın. Çıkmak için tekrar geri bas.'),
          duration:Duration(seconds:5)));
        return false;
      }
      _guestLeaving553=true;
      _guestConsent548=false;
      await _guestSync448(false);
      final uid=FirebaseAuth.instance.currentUser?.uid;
      if(uid!=null&&mounted)await ngelx448GuestAction(context,widget.belgeId,widget.ownerId,uid,'reject');
    }
    await _klavyeyiKapat();
    if(widget.yayinSahibi){''')
 s=s.replace('Ngelx448GuestControls(liveId:', 'Ngelx448GuestControls(moderation553:_hostGuestAction489,liveId:')
 s=once(s,'  Future<void> _hostGuestAction489(String uid,String action)async{','''  Future<void> _hostGuestAction489(String uid,String action)async{
    if(action=='ban'){
      if(widget.yayinSahibi&&FirebaseAuth.instance.currentUser?.uid==widget.ownerId)await _viewerAction553(uid,'remove');
      return;
    }''')
 s=s.replace("const PopupMenuItem(value:'kick',child:Text('Konukluktan çıkar')),", "const PopupMenuItem(value:'kick',child:Text('Konukluktan çıkar')),\n              const PopupMenuItem(value:'ban',child:Text('Bu yayından engelle')),")
 s=once(s,"                    const PopupMenuItem(value:'kick',", "                    const PopupMenuItem(value:'ban',child:Text('Bu yayından engelle')),\n                    const PopupMenuItem(value:'kick',")

 p.write_text(s+'\n'+TAG+'\n')
 p=root/'lib/main.dart';s=p.read_text();s=once(s,"import 'build552_policy.dart';","import 'build552_policy.dart';\nimport 'build553_gift_effect.dart';");p.write_text(s)
 (root/'lib/build553_gift_effect.dart').write_text(Path('tools/build553_gift_effect.dart').read_text())
 p=root/'pubspec.yaml';s=p.read_text()
 if('    - assets/gifts553/' not in s):
  s=once(s,'  assets:\n','  assets:\n    - assets/gifts553/\n')
  p.write_text(s)
 p=root/'lib/build548_policy.dart';s=p.read_text();s=once(s,"'Galaksi':100","'Galaksi':100,'Aslan':150,'Evren':200");p.write_text(s)
 p=root/'lib/build448_live_guests.dart';s=p.read_text()
 s=once(s,'20+MediaQuery.viewInsetsOf(sheet).bottom','20+MediaQuery.viewInsetsOf(sheet).bottom+MediaQuery.viewPaddingOf(sheet).bottom')
 s=once(s,'isScrollControlled:true,showDragHandle:true,backgroundColor:', 'isScrollControlled:true,useSafeArea:true,showDragHandle:true,backgroundColor:')
 s=once(s,"return SizedBox(height:math.min(MediaQuery.sizeOf(c).height*.48,100.0+ids.length*78.0)", "return SizedBox(height:math.min(MediaQuery.sizeOf(c).height*.66,150.0+ids.length*100.0)")
 s=once(s,"title:Text(name,maxLines:1,overflow:TextOverflow.ellipsis),subtitle:Text(status=='accepted'?'Kabul edildi':status=='invited'?'Davet gönderildi':status=='pending'?'Katılmak istiyor':'Canlı izleyicisi'),trailing:Row(mainAxisSize:MainAxisSize.min,children:[", "title:Text(name,maxLines:1,overflow:TextOverflow.ellipsis),subtitle:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[Text(status=='accepted'?'Kabul edildi':status=='invited'?'Davet gönderildi':status=='pending'?'Katılmak istiyor':'Canlı izleyicisi'),Wrap(crossAxisAlignment:WrapCrossAlignment.center,children:[")
 s=once(s,'          ]));','          ])]));')
 s=once(s,'150.0+ids.length*100.0),child:Column(children:[','150.0+ids.length*100.0),child:SingleChildScrollView(child:Column(children:[')
 s=once(s,'Expanded(child:ListView.builder(itemCount:ids.length,','ListView.builder(shrinkWrap:true,physics:const NeverScrollableScrollPhysics(),itemCount:ids.length,')
 s=once(s,'        });})),\n      ]));','        });}),\n      ])));')

 s=once(s,'  final bool connected548;final VoidCallback? onLeaving548;','  final Future<void> Function(String,String)? moderation553;\n  final bool connected548;final VoidCallback? onLeaving548;')
 s=once(s,'this.compact=false,this.viewerUids=const[]','this.moderation553,this.compact=false,this.viewerUids=const[]')
 s=once(s,"if(status=='accepted')const Tooltip(message:'Konuğu çıkarmak için canlı yayın konuk kartındaki üç nokta menüsünü kullan.',child:Icon(Icons.more_horiz_rounded,color:Colors.deepPurple)),",'''if(status=='accepted')PopupMenuButton<String>(tooltip:'Konuk yönetimi',
              onSelected:(action){moderation553?.call(id,action);},
              itemBuilder:(_)=>const [
                PopupMenuItem(value:'mute',child:Text('Mikrofonu sustur')),
                PopupMenuItem(value:'unmute',child:Text('Mikrofon iznini aç')),
                PopupMenuItem(value:'kick',child:Text('Konukluktan indir')),\n                PopupMenuItem(value:'ban',child:Text('Bu yayından engelle')),
              ]),''')
 p.write_text(s)
 p=root/'lib/live_pk.dart' ;s=p.read_text()
 # Missing documents cannot be read under member-only rules. Create a unique request
 # while locking only the known owned live document in a transaction.
 a=s.index("                              final id=ngelxCanliPkBelgeId(liveId,d.id);")
 b=s.index('                              unawaited(uygulamaBildirimiGonder(',a)
 s=s[:a]+"""                              if(busy553)return;
                              refresh553(()=>busy553=true);
                              try{
                              final ref=FirebaseFirestore.instance.collection('calls').doc();
                              final id=ref.id;
                              final own=FirebaseFirestore.instance.collection('live_streams').doc(liveId);
                              await FirebaseFirestore.instance.runTransaction((tx)async{
                                final current=(await tx.get(own)).data()??<String,dynamic>{};
                                final target=(await tx.get(FirebaseFirestore.instance.collection('live_streams').doc(d.id))).data()??<String,dynamic>{};
                                if(!ngelxCanliKaydiTaze(target)||target['ownerId']!=hedefUid||target['pkActive']==true)throw StateError('inactive');
                                final targetUntil=target['pkInviteExpiresAt'];
                                if(target['pkInviteStatus']=='pending'&&targetUntil is Timestamp&&targetUntil.toDate().isAfter(DateTime.now()))throw StateError('pending');
                                if(!ngelxCanliKaydiTaze(current)||current['ownerId']!=ownerUid||current['pkActive']==true)throw StateError('inactive');
                                final until=current['pkInviteExpiresAt'];
                                if(current['pkInviteStatus']=='pending'&&until is Timestamp&&until.toDate().isAfter(DateTime.now()))throw StateError('pending');
                                tx.set(ref,{
                                  'type':'live_pk','members':<String>[ownerUid,hedefUid],
                                  'startedBy':ownerUid,'inviterLiveId':liveId,'inviteeLiveId':d.id,
                                  'inviterUid':ownerUid,'inviteeUid':hedefUid,
                                  'inviterName':(current['username']??'NgelX').toString(),'inviteeName':ad,
                                  'status':'pending','durationSeconds':180,
                                  'createdAt':FieldValue.serverTimestamp(),'clientCreatedAt':Timestamp.now(),
                                  'requestExpiresAt':Timestamp.fromDate(DateTime.now().add(const Duration(seconds:45))),
                                });
                                tx.set(own,{
                                  'pkInviteStatus':'pending','pkInviteSessionId':id,
                                  'pkInviteToLiveId':d.id,'pkInviteToUid':hedefUid,
                                  'pkInviteExpiresAt':Timestamp.fromDate(DateTime.now().add(const Duration(seconds:45))),
                                },SetOptions(merge:true));
                              },maxAttempts:3).timeout(const Duration(seconds:15));
"""+s[b:]
 a=s.index("content:Text('PK isteği gönderildi.')");b=s.index('                            },',a)
 s=s[:b]+"""                              }catch(error){
                                if(sheetContext.mounted)ScaffoldMessenger.of(sheetContext).showSnackBar(SnackBar(content:Text(
                                  error is StateError&&error.message=='pending'
                                    ?'Açık bir PK daveti var. Yanıtı veya süresinin dolmasını bekle.'
                                    :'PK daveti doğrulanamadı. Bağlantıyı kontrol edip tekrar dene.')));
                              }finally{
                                if(sheetContext.mounted)refresh553(()=>busy553=false);
                              }
"""+s[b:]
 s=once(s,"label:const Text('Davet et',style:TextStyle(fontWeight:FontWeight.w900)),","label:Text(busy553?'Gönderiliyor…':'Davet et',style:const TextStyle(fontWeight:FontWeight.w900)),")
 s=once(s,'  if(!context.mounted)return;\n  await showModalBottomSheet<void>(', '  if(!context.mounted)return;\n  bool busy553=false;\n  await showModalBottomSheet<void>(')
 s=once(s,'    builder:(sheetContext)=>Theme(data:ThemeData.dark(),child:SafeArea(', '    builder:(sheetContext)=>StatefulBuilder(builder:(sheetContext,refresh553)=>Theme(data:ThemeData.dark(),child:SafeArea(')
 a=s.index('    builder:(sheetContext)=>StatefulBuilder');b=s.index('\nclass NgelXCanliPkKatmani',a);section=s[a:b];section=once(section,'    )),\n  );','    ))),\n  );');s=s[:a]+section+s[b:]
 # Put the invitation below long names instead of crowding ListTile.trailing.
 s=once(s,"                          subtitle:Text('@$ad • $izleyici izleyici'),\n                          trailing:FilledButton.icon(","                          subtitle:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[Text('@$ad • $izleyici izleyici'),\n                          FilledButton.icon(")
 a=s.index("label:Text(busy553?'Gönderiliyor…'");b=s.index('                          ),',a);s=s[:b]+s[b:].replace('                          ),','                          )]),',1)
 p.write_text(s)
if __name__=='__main__':apply(Path(sys.argv[1]) if len(sys.argv)>1 else Path('app'))
