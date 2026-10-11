"""Canonical group-target requests; apply after apply_build438_qa_fixes.py."""
from pathlib import Path


def apply():
    p=Path('app/lib/main.dart');s=p.read_text()
    if 'final pending438=' not in s:
        start=s.index('  Future<void> uyeEkle(List<String> mevcut)')
        end=s.index('  Future<void> ayril(List<String> uyeler',start)
        part=s[start:end]
        old="    final izinli=<String>{"
        assert part.count(old)==1
        part=part.replace(old,"""    final pending438=await ref.collection('joinRequests').where('status',isEqualTo:'pending').get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:8));
    final pendingTargets438=pending438.docs.map((d)=>(d.data()['targetUid']??d.data()['uid']??d.id).toString()).toSet();
    final izinli=<String>{""",1)
        part=part.replace('..removeAll(mevcut);','..removeAll(mevcut)..removeAll(pendingTargets438);',1)
        part=part.replace("await ref.collection('joinRequests').doc(me+'_'+hedef.id).set({","final request438=ref.collection('joinRequests').doc(hedef.id);\n        await FirebaseFirestore.instance.runTransaction((tx)async{\n          final group438=await tx.get(ref);\n          final previous438=await tx.get(request438);\n          if(List<String>.from(group438.data()?['members']??const[]).contains(hedef.id)||previous438.data()?['status']=='pending')return;\n          tx.set(request438,{",1)
        old="        },SetOptions(merge:true));\n      }\n      if(mounted)"
        assert old in part
        part=part.replace(old,"        });\n        }).timeout(const Duration(seconds:12));\n      }\n      if(mounted)",1)
        part=part.replace("secilen.length.toString()+' üye ekleme isteği yönetici onayına gönderildi.'","'Üye talepleri kontrol edildi. Yeni talepler yönetici onayına gönderildi.'",1)
        s=s[:start]+part+s[end:];p.write_text(s)
    p=Path('firestore.rules');s=p.read_text()
    if '// Build438 canonical group target' not in s:
        start=s.index('      match /joinRequests/{requestUid}')
        end=s.index('\n    match /group_archives/',start)
        part=s[start:end]
        part=part.replace("&& request.resource.data.get('type', '') == 'member_add'","&& request.resource.data.get('type', '') == 'member_add'\n          // Build438 canonical group target\n          && requestUid == request.resource.data.get('targetUid', '')",1)
        part=part.replace('          || isGroupAdmin(chatId)\n        );\n        allow list: if isGroupAdmin(chatId);',"          || request.auth.uid in groupDoc(chatId).data.get('members', [])\n          || isGroupAdmin(chatId)\n        );\n        allow list: if signedIn() && (request.auth.uid in groupDoc(chatId).data.get('members', []) || isGroupAdmin(chatId));",1)
        part=part.replace('        allow update: if isGroupAdmin(chatId) || (',"""        allow update: if isGroupAdmin(chatId) || (
          signedIn()
          && request.auth.uid in groupDoc(chatId).data.get('members', [])
          && resource.data.get('status', '') in ['rejected', 'cancelled']
          && request.resource.data.get('type', '') == 'member_add'
          && requestUid == request.resource.data.get('targetUid', '')
          && request.resource.data.get('uid', '') == requestUid
          && request.resource.data.get('requestedBy', '') == request.auth.uid
          && request.resource.data.get('status', '') == 'pending'
          && !(requestUid in groupDoc(chatId).data.get('members', []))
          && request.resource.data.keys().hasOnly(['type','uid','targetUid','targetName','targetPhoto','requestedBy','requestedByName','requestedByPhoto','status','createdAt','updatedAt'])
        ) || (""",1)
        s=s[:start]+part+s[end:];p.write_text(s)
    p=Path('tools/firestore_rules_test.mjs');s=p.read_text()
    s=s.replace('joinRequests/bob_mallory','joinRequests/mallory')
    s=s.replace('  serverTimestamp,','  runTransaction,\n  serverTimestamp,') if '  runTransaction,' not in s else s
    marker='  // Build438 canonical '
    if marker in s:
        start=s.index(marker)
        end=s.index("  console.log('Firestore rules testleri başarılı.');",start)
        s=s[:start]+s[end:]
    s=s.replace("  console.log('Firestore rules testleri başarılı.');",Path('tools/build438_pending_rules_test.mjs').read_text()+"\n  console.log('Firestore rules testleri başarılı.');")
    p.write_text(s)


if __name__=='__main__':apply()
