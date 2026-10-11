"""Closed phone-round message UI fixes, applied after existing 438 patches."""
from pathlib import Path


def apply():
    path=Path('app/lib/main.dart')
    source=path.read_text()
    def replace(old,new):
        nonlocal source
        if new in source:return
        assert source.count(old)==1,old[:100]
        source=source.replace(old,new)

    replace(
        "onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>SabitlenenGrupMesajlariPage(chatId:widget.chatId))),",
        "onTap:()async{final result=await Navigator.push<String>(context,MaterialPageRoute(builder:(_)=>SabitlenenGrupMesajlariPage(chatId:widget.chatId)));if(mounted)await jumpToMessage(result);},",
    )
    replace(
        "_grupSatir(Icons.push_pin_outlined,lt('Sabitlenen mesajlar','Pinned messages'),lt('Önemli mesajlara hızlı ulaş','Quickly access important messages'),()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>SabitlenenGrupMesajlariPage(chatId:widget.chatId))))",
        "_grupSatir(Icons.push_pin_outlined,lt('Sabitlenen mesajlar','Pinned messages'),lt('Önemli mesajlara hızlı ulaş','Quickly access important messages'),()async{final result=await Navigator.push<String>(context,MaterialPageRoute(builder:(_)=>SabitlenenGrupMesajlariPage(chatId:widget.chatId)));if(context.mounted&&result!=null)Navigator.pop(context,result);})",
    )
    start=source.index('class SabitlenenGrupMesajlariPage ')
    end=source.index('\nclass ',start+1)
    block=source[start:end]
    if 'Navigator.pop(context,d.id)' not in block:
        block=block.replace('return NgelXPremiumCard(',"return GestureDetector(\n                  behavior:HitTestBehavior.opaque,\n                  onTap:()=>Navigator.pop(context,d.id),\n                  child:NgelXPremiumCard(",1)
        block=block.replace('''                  ]),
                );
              }),''','''                  ]),
                ));
              }),''',1)
    # Video URLs are not image URLs; use the chat's bounded video preview.
    block=block.replace("url=(v['mediaUrl']??'').toString();", "url=ngelxMesajMedyaUrl(v,video:tur=='video');")
    old="child:ClipRRect(borderRadius:BorderRadius.circular(14),child:SizedBox(height:128,width:double.infinity,child:NgelXAgResmi(url:url,fit:BoxFit.cover,error:const SizedBox(height:100,child:Center(child:Icon(Icons.broken_image_outlined))))))"
    new="child:ClipRRect(borderRadius:BorderRadius.circular(14),child:SizedBox(height:128,width:double.infinity,child:tur=='video'?IgnorePointer(child:NgelXSohbetVideoOnizleme(url:url,thumbnailUrl:ngelxMesajVideoKapagi(v))):NgelXAgResmi(url:url,fit:BoxFit.cover,error:const SizedBox(height:100,child:Center(child:Icon(Icons.broken_image_outlined))))))"
    # Reuse source thumbnail lookup after checking its actual symbol below.
    if old in block:block=block.replace(old,new)
    block=block.replace('onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>TamEkranMedyaPage(url:url))),','onTap:()=>Navigator.pop(context,d.id),')
    source=source[:start]+block+source[end:]

    start=source.index('  Widget _ozelMesajKarti435(')
    end=source.index('\n  Future',start)
    block=source[start:end]
    old='child:Column(crossAxisAlignment:CrossAxisAlignment.end,mainAxisSize:MainAxisSize.min,children:['
    label="""child:Column(crossAxisAlignment:CrossAxisAlignment.end,mainAxisSize:MainAxisSize.min,children:[
            if(v['forwarded']==true)Padding(
              padding:const EdgeInsets.fromLTRB(8,6,8,4),
              child:Row(mainAxisSize:MainAxisSize.min,children:[
                Icon(Icons.forward_rounded,size:14,color:sadeMedya?ngelxPrivateBlue:(benimMaviBalon?Colors.white70:Colors.black54)),
                const SizedBox(width:4),
                Text(lt('İletilen mesaj','Forwarded message'),style:TextStyle(fontSize:11,fontWeight:FontWeight.w700,color:sadeMedya?ngelxPrivateBlue:(benimMaviBalon?Colors.white70:Colors.black54))),
              ]),
            ),"""
    if "if(v['forwarded']==true)" not in block:
        assert block.count(old)==1
        block=block.replace(old,label)
    source=source[:start]+block+source[end:]
    # The compact approval path had no system message at all. Both paths now
    # commit membership, request decision and a deterministic event together.
    start=source.index('  static Future<void> kararHizli(')
    end=source.index('  const GrupKatilmaIstekleriPage(',start)
    if 'join_decision438_' not in source[start:end]:
        source=source[:start]+'''  static Future<void> kararHizli(String chatId,QueryDocumentSnapshot<Map<String,dynamic>> d,bool onay)async{
    final uid=(d.data()['targetUid']??d.data()['uid']??d.id).toString();
    final me=FirebaseAuth.instance.currentUser?.uid;
    if(uid.isEmpty||me==null)return;
    final chat=FirebaseFirestore.instance.collection('chats').doc(chatId);
    final profiles=await Future.wait([
      FirebaseFirestore.instance.collection('users').doc(me).get(),
      FirebaseFirestore.instance.collection('users').doc(uid).get(),
    ]).timeout(const Duration(seconds:10));
    String name(Map<String,dynamic>? v,String fallback)=>(v?['displayName']??v?['username']??fallback).toString();
    final actor=name(profiles[0].data(),'Bir yönetici'),target=name(profiles[1].data(),'Bir üye');
    final requested=(d.data()['requestedByName']??'').toString().trim();
    final event=requested.isNotEmpty&&requested!=actor
      ?actor+', '+requested+' tarafından istenen '+target+' adlı üyeyi gruba ekledi.'
      :actor+', '+target+' adlı üyeyi gruba ekledi.';
    await FirebaseFirestore.instance.runTransaction((tx)async{
      final request=await tx.get(d.reference),group=await tx.get(chat);
      if(request.data()?['status']!='pending')return;
      final gv=group.data()??<String,dynamic>{};
      if(gv['createdBy']!=me&&!List<String>.from(gv['admins']??const[]).contains(me))throw StateError('Yönetici yetkisi gerekli.');
      final members=List<String>.from(gv['members']??const[]);
      if(onay&&!members.contains(uid)&&members.length>=60)throw StateError('Grup dolu.');
      tx.set(d.reference,{'status':onay?'accepted':'rejected','decidedAt':FieldValue.serverTimestamp(),'decidedBy':me},SetOptions(merge:true));
      if(onay){
        tx.update(chat,{
          'members':FieldValue.arrayUnion([uid]),'formerMembers':FieldValue.arrayRemove([uid]),'hiddenFor':FieldValue.arrayRemove([uid]),
          'removedAt_'+uid:FieldValue.delete(),'leftAt_'+uid:FieldValue.delete(),
          'exitType_'+uid:FieldValue.delete(),'exitActorUid_'+uid:FieldValue.delete(),'exitActorName_'+uid:FieldValue.delete(),
          'updatedAt':FieldValue.serverTimestamp(),
          if(!members.contains(uid))'lastMessage':event,
        });
        final generation=request.data()?['createdAt'];
        final suffix=generation is Timestamp?generation.microsecondsSinceEpoch.toString():'legacy';
        if(!members.contains(uid))tx.set(chat.collection('messages').doc('join_decision438_'+d.id+'_'+suffix),{
          'senderId':me,'type':'system','systemAction':'member_added','actorUid':me,
          'targetUids':<String>[uid],'text':event,'createdAt':FieldValue.serverTimestamp(),
        });
      }
    }).timeout(const Duration(seconds:12));
    if(onay){await ngelxClearGroupArchive(uid,chatId);await ngelxGrupDavetMetaSenkronla(chat);}
  }
''' + source[end:]
    start=source.index('  Future<void> _karar(BuildContext context,QueryDocumentSnapshot<Map<String,dynamic>> d,bool onay)')
    end=source.index('\n  @override Widget build',start)
    block=source[start:end]
    if 'await kararHizli(chatId,d,onay);' not in block:
        a=block.index('    final batch=')
        b=block.index('      unawaited(chat.get().then',a)
        block=block[:a]+"    await kararHizli(chatId,d,onay);\n    if(onay){\n"+block[b:]
        source=source[:start]+block+source[end:]
    path.write_text(source)


if __name__=='__main__':apply()
