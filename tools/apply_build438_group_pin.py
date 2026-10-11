"""Align group pin UI with server permissions and use fresh transactional state."""
from pathlib import Path
p=Path('app/lib/main.dart');s=p.read_text()
if 'Future<bool> ngelx438SetGroupPin' not in s:
    old="""    final grupData=await _grupVerisiHizli();
    final yonetici=List<String>.from(grupData['admins']??const[]).contains(uid)||(grupData['createdBy']??'').toString()==uid;
    final sabitleyebilir=yonetici||grupData['onlyAdminsCanPin']!=true;"""
    assert s.count(old)==1
    s=s.replace(old,"""    Map<String,dynamic> grupData;
    try{
      grupData=(await chatRef.get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:4))).data()??<String,dynamic>{};
      _grupVerisiniOnbellekle(grupData);
    }catch(_){grupData=await _grupVerisiHizli();}
    if(!mounted)return;
    final yonetici=List<String>.from(grupData['admins']??const[]).contains(uid)||(grupData['createdBy']??'').toString()==uid;
    final sabitleyebilir=ngelx438CanPin(grupData,uid);""")
    start=s.index("    }else if(sec=='pin'){",s.index('Future<void> mesajMenusu('))
    end=s.index("    }else if(sec=='hide435'){",start)
    s=s[:start]+"""    }else if(sec=='pin'){
      try{
        final yeniDurum=await ngelx438SetGroupPin(chatRef,d.reference);
        if(mounted)ngelxDurumMesaji(context,yeniDurum?'Mesaj sabitlendi.':'Sabitleme kaldırıldı.',tip:'basari');
      }catch(e){
        if(mounted)ngelxDurumMesaji(context,ngelx436Error(e),tip:'hata');
      }
"""+s[end:]
    old="                          await d.reference.set({'pinned':false,'pinnedAt':FieldValue.delete(),'pinnedBy':FieldValue.delete()},SetOptions(merge:true));"
    assert s.count(old)==1
    s=s.replace(old,"""                          try{
                            await ngelx438SetGroupPin(FirebaseFirestore.instance.collection('chats').doc(chatId),d.reference,pinned:false);
                            if(context.mounted)ngelxDurumMesaji(context,'Sabitleme kaldırıldı.',tip:'basari');
                          }catch(e){if(context.mounted)ngelxDurumMesaji(context,ngelx436Error(e),tip:'hata');}""")
    s+='\n'+Path('tools/build438_pin_permission.dart').read_text()+'''
Future<bool> ngelx438SetGroupPin(
  DocumentReference<Map<String,dynamic>> group,
  DocumentReference<Map<String,dynamic>> message,{bool? pinned})async{
  final uid=FirebaseAuth.instance.currentUser?.uid;
  return FirebaseFirestore.instance.runTransaction<bool>((tx)async{
    final groupData=(await tx.get(group)).data()??<String,dynamic>{};
    final data=(await tx.get(message)).data();
    if(!ngelx438CanPin(groupData,uid))throw StateError('Bu grupta mesaj sabitleme yetkin yok.');
    if(data==null)throw StateError('Mesaj artık mevcut değil.');
    final target=pinned??(data['pinned']!=true);
    if(target&&data['deletedForEveryone']==true)throw StateError('Silinmiş mesaj sabitlenemez.');
    tx.update(message,{
      'pinned':target,
      'pinnedAt':target?FieldValue.serverTimestamp():FieldValue.delete(),
      'pinnedBy':target?uid:FieldValue.delete(),
    });
    return target;
  }).timeout(const Duration(seconds:12));
}
'''
    p.write_text(s)

p=Path('tools/firestore_rules_test.mjs');s=p.read_text()
marker='  // Build438 transactional pin coverage.'
if marker in s:
    start=s.index(marker);end=s.index("  console.log('Firestore rules testleri başarılı.');",start)
    s=s[:start]+s[end:]
s=s.replace("  console.log('Firestore rules testleri başarılı.');",Path('tools/build438_pin_rules_test.mjs').read_text()+"\n  console.log('Firestore rules testleri başarılı.');")
p.write_text(s)
