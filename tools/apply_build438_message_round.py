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
    replace(
        "stream:chatRef.collection('messages').where('pinned',isEqualTo:true).limit(1).snapshots(),",
        "stream:chatRef.collection('messages').where('pinned',isEqualTo:true).limit(50).snapshots(),",
    )
    replace(
        'final pins=pinSnap.data?.docs??[];',
        "final pins=(pinSnap.data?.docs??[]).where((d)=>d.data()['deletedForEveryone']!=true&&!ngelx437MessageExpired(d.data()['createdAt'],DateTime.now())).toList()..sort((a,b)=>a.id.compareTo(b.id));",
    )
    start=source.index('class SabitlenenGrupMesajlariPage ')
    end=source.index('\nclass ',start+1)
    block=source[start:end]
    block=block.replace('final docs=snap.data?.docs??[];',"if(snap.hasError)return const Center(child:Text('Sabitlenen mesajlar yüklenemedi.'));\n          final docs=(snap.data?.docs??[]).where((d)=>d.data()['deletedForEveryone']!=true&&!ngelx437MessageExpired(d.data()['createdAt'],DateTime.now())).toList()..sort((a,b)=>a.id.compareTo(b.id));")
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
    start=source.index('  static Future<bool> kararHizli(') if '  static Future<bool> kararHizli(' in source else source.index('  static Future<void> kararHizli(')
    end=source.index('  const GrupKatilmaIstekleriPage(',start)
    if 'join_decision438_' not in source[start:end]:
        source=source[:start]+'''  static Future<bool> kararHizli(String chatId,QueryDocumentSnapshot<Map<String,dynamic>> d,bool onay)async{
    final uid=(d.data()['targetUid']??d.data()['uid']??d.id).toString();
    final me=FirebaseAuth.instance.currentUser?.uid;
    if(uid.isEmpty||me==null)return false;
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
    final changed=await FirebaseFirestore.instance.runTransaction<bool>((tx)async{
      final request=await tx.get(d.reference),group=await tx.get(chat);
      if(request.data()?['status']!='pending')return false;
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
      return true;
    }).timeout(const Duration(seconds:12));
    if(changed&&onay){await ngelxClearGroupArchive(uid,chatId);await ngelxGrupDavetMetaSenkronla(chat);}
    return changed;
  }
''' + source[end:]
    start=source.index('  Future<void> _karar(BuildContext context,QueryDocumentSnapshot<Map<String,dynamic>> d,bool onay)')
    end=source.index('\n  @override Widget build',start)
    block=source[start:end]
    if 'await kararHizli(chatId,d,onay);' not in block:
        a=block.index('    final batch=')
        b=block.index('      unawaited(chat.get().then',a)
        block=block[:a]+"    final changed=await kararHizli(chatId,d,onay);\n    if(!changed){if(context.mounted)ngelxDurumMesaji(context,'İstek zaten işlenmiş.',tip:'uyari');return;}\n    if(onay){\n"+block[b:]
        source=source[:start]+block+source[end:]
    source=source.replace('static Future<void> kararHizli(', 'static Future<bool> kararHizli(')
    a=source.index('  static Future<bool> kararHizli(');b=source.index('  const GrupKatilmaIstekleriPage(',a)
    part=source[a:b]
    part=part.replace('if(uid.isEmpty||me==null)return;','if(uid.isEmpty||me==null)return false;')
    part=part.replace('    await FirebaseFirestore.instance.runTransaction((tx)async{','    final changed=await FirebaseFirestore.instance.runTransaction<bool>((tx)async{')
    part=part.replace("if(request.data()?['status']!='pending')return;","if(request.data()?['status']!='pending')return false;")
    if 'return changed;' not in part:
        part=part.replace('    }).timeout(const Duration(seconds:12));','      return true;\n    }).timeout(const Duration(seconds:12));')
        part=part.replace('    if(onay){await ngelxClearGroupArchive(uid,chatId);await ngelxGrupDavetMetaSenkronla(chat);}', '    if(changed&&onay){await ngelxClearGroupArchive(uid,chatId);await ngelxGrupDavetMetaSenkronla(chat); }\n    return changed;')
    if 'final eventRef438=' not in part:
        part=part.replace("    final chat=FirebaseFirestore.instance.collection('chats').doc(chatId);", "    final chat=FirebaseFirestore.instance.collection('chats').doc(chatId);\n    final eventRef438=chat.collection('messages').doc();")
        part=part.replace("        final generation=request.data()?['createdAt'];\n        final suffix=generation is Timestamp?generation.microsecondsSinceEpoch.toString():'legacy';\n        if(!members.contains(uid))tx.set(chat.collection('messages').doc('join_decision438_'+d.id+'_'+suffix),{", "        if(!members.contains(uid))tx.set(eventRef438,{")
    source=source[:a]+part+source[b:]
    source=source.replace('    await kararHizli(chatId,d,onay);', "    final changed=await kararHizli(chatId,d,onay);\n    if(!changed){if(context.mounted)ngelxDurumMesaji(context,'İstek zaten işlenmiş.',tip:'uyari');return;}")
    path.write_text(source)


if __name__=='__main__':apply()
