"""Keep former group conversations in inbox without exposing future previews."""
from pathlib import Path


def apply():
    p=Path('app/lib/main.dart');s=p.read_text()
    start=s.index('class _MesajPageState ');end=s.index('\nclass ArsivSohbetlerPage ',start)
    block=s[start:end]
    if '_eskiGrupAboneligi438' not in block:
        marker='  Set<String> engellenenler={};'
        helper='''  StreamSubscription<QuerySnapshot<Map<String,dynamic>>>? _eskiGrupAboneligi438;
  List<QueryDocumentSnapshot<Map<String,dynamic>>> _eskiGruplar438=[];
  void _eskiGruplariIzle438(){
    final ben=uid;if(ben==null)return;
    _eskiGrupAboneligi438=FirebaseFirestore.instance.collection('chats')
      .where('formerMembers',arrayContains:ben).limit(200).snapshots().listen((snap){
        if(mounted&&uid==ben)setState(()=>_eskiGruplar438=snap.docs);
      },onError:(Object error){
        if(mounted&&uid==ben)ngelxDurumMesaji(context,'Eski grup sohbetleri yüklenemedi. Yenile ve tekrar dene.',tip:'uyari');
      });
  }
  List<QueryDocumentSnapshot<Map<String,dynamic>>> _inboxBelgeleri438(List<QueryDocumentSnapshot<Map<String,dynamic>>> current){
    final combined=<String,QueryDocumentSnapshot<Map<String,dynamic>>>{
      for(final d in _eskiGruplar438)d.id:d,
      for(final d in current)d.id:d,
    };
    return combined.values.toList();
  }
  Map<String,dynamic> _inboxVerisi438(DocumentSnapshot<Map<String,dynamic>> d){
    final v=d.data()??<String,dynamic>{},ben=uid;
    if(v['isGroup']!=true||ben==null||List<String>.from(v['members']??const[]).contains(ben)||!List<String>.from(v['formerMembers']??const[]).contains(ben))return v;
    final actor=(v['exitActorName_'+ben]??'').toString().trim();
    final preview=v['exitType_'+ben]=='left'?'Gruptan ayrıldın.':actor.isEmpty?'Gruptan çıkarıldın.':actor+' seni gruptan çıkardı.';
    return {...v,'lastMessage':preview,'updatedAt':v['removedAt_'+ben],'lastMessageClientAt':v['removedAt_'+ben],'unread_'+ben:0};
  }

'''
        assert marker in block;block=block.replace(marker,helper+marker,1)
        block=block.replace('super.initState();tercihleriGetir();','super.initState();tercihleriGetir();_eskiGruplariIzle438();',1)
        block=block.replace('@override void dispose(){for(final cache','@override void dispose(){_eskiGrupAboneligi438?.cancel();for(final cache',1)
        block=block.replace('for(final d in chatSnap.data?.docs??const <QueryDocumentSnapshot<Map<String,dynamic>>>[]){','for(final d in _inboxBelgeleri438(chatSnap.data?.docs??const <QueryDocumentSnapshot<Map<String,dynamic>>>[])){',1)
        block=block.replace('final docs=(s.data?.docs??[]).where((d){','final docs=_inboxBelgeleri438(s.data?.docs??[]).where((d){',1)
        # Substitute only consumer reads, not the helper's own source read.
        helper_end=block.index('  Set<String> engellenenler={};')
        tail=block[helper_end:].replace('satir.d.data()','_inboxVerisi438(satir.d)').replace('d.data()','_inboxVerisi438(d)').replace("a.data()['updatedAt']","_inboxVerisi438(a)['updatedAt']").replace("b.data()['updatedAt']","_inboxVerisi438(b)['updatedAt']")
        block=block[:helper_end]+tail
        # Voluntary leave must not silently archive the conversation.
        block=block.replace("'archivedChats':FieldValue.arrayUnion([id]),","'archivedChats':FieldValue.arrayRemove([id]),")
        block=block.replace('arsivSohbetler.add(id);','arsivSohbetler.remove(id);')
    s=s[:start]+block+s[end:]
    s=s.replace("set({'archivedChats':FieldValue.arrayUnion([widget.chatId])},SetOptions(merge:true));", "set({'archivedChats':FieldValue.arrayRemove([widget.chatId])},SetOptions(merge:true));")
    s=s.replace("set({'archivedChats':FieldValue.arrayUnion([chatId])},SetOptions(merge:true));", "set({'archivedChats':FieldValue.arrayRemove([chatId])},SetOptions(merge:true));")
    p.write_text(s)
    # Comparing every protected metadata field twice exhausted the emulator's
    # expression budget in a multi-document approval. Diff protects the same
    # field set without permitting any metadata edits through this fallback.
    p=Path('firestore.rules');s=p.read_text()
    a=s.index('    function groupMetadataUnchanged() {');b=s.index('\n    // Build436',a)
    if 'affectedKeys().hasAny' not in s[a:b]:
        import re
        fields=list(dict.fromkeys(re.findall(r"request\.resource\.data\.get\('([^']+)'",s[a:b])))
        assert len(fields)>=18
        body="    function groupMetadataUnchanged() {\n      return !request.resource.data.diff(resource.data).affectedKeys().hasAny([\n        "+', '.join(repr(x) for x in fields)+"\n      ]);\n    }\n"
        s=s[:a]+body+s[b:];p.write_text(s)
    p=Path('tools/firestore_rules_test.mjs');s=p.read_text()
    if '// Closed phone round: former members' not in s:
        marker="  console.log('Firestore rules testleri başarılı.');"
        assert marker in s
        s=s.replace(marker,Path('tools/build438_closed_round_rules.mjs').read_text()+'\n'+marker)
        p.write_text(s)


if __name__=='__main__':apply()
