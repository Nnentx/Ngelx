"""Reproducible closed phone-round inbox fixes; run after other 438 patches."""
from pathlib import Path


def apply():
    path = Path('app/lib/main.dart')
    source = path.read_text()
    old = "            items.sort((a,b)=>(b['time'] as int).compareTo(a['time'] as int));"
    new = """            // Pinned conversations precede both conversations and notifications.
            bool pinned(Map<String,dynamic> item)=>item['kind']=='chat'&&
              sabitSohbetler.contains((item['doc'] as QueryDocumentSnapshot<Map<String,dynamic>>).id);
            items.sort((a,b){
              final ap=pinned(a),bp=pinned(b);
              if(ap!=bp)return ap?-1:1;
              return (b['time'] as int).compareTo(a['time'] as int);
            });"""
    if new not in source:
        assert source.count(old) == 1
        source = source.replace(old, new)
    old = """    await FirebaseFirestore.instance.collection('users').doc(ben).set({alan:ekle?FieldValue.arrayUnion([chatId]):FieldValue.arrayRemove([chatId])},SetOptions(merge:true));
    if(!mounted)return;
    setState((){final hedef=alan=='archivedChats'?arsivSohbetler:sabitSohbetler;ekle?hedef.add(chatId):hedef.remove(chatId);});"""
    new = """    try{
      await FirebaseFirestore.instance.collection('users').doc(ben).set({alan:ekle?FieldValue.arrayUnion([chatId]):FieldValue.arrayRemove([chatId])},SetOptions(merge:true)).timeout(const Duration(seconds:12));
      if(!mounted||uid!=ben)return;
      setState((){final hedef=alan=='archivedChats'?arsivSohbetler:sabitSohbetler;ekle?hedef.add(chatId):hedef.remove(chatId);});
      ngelxDurumMesaji(context,alan=='archivedChats'?'Sohbet arşivlendi.':ekle?'Sohbet sabitlendi.':'Sohbet sabitlemesi kaldırıldı.',tip:'basari');
    }catch(error){
      if(mounted&&uid==ben)ngelxDurumMesaji(context,'İşlem doğrulanamadı. Bağlantını kontrol edip yeniden dene.',tip:'hata');
    }"""
    if new not in source:
        assert source.count(old) == 1
        source = source.replace(old, new)
    # A failed archive query must not be rendered as a successful empty result.
    old = """          if (docs.isEmpty) {
            return Center(child: Text(t('noArchivedChats'), style: const TextStyle(color: Colors.black54)));
          }"""
    new = """          if(snap.hasError)return ngelx432YuklemeHatasi(()=>setState((){}),'Arşivlenen sohbetler yüklenemedi.');
          if (docs.isEmpty) {
            return Center(child: Text(t('noArchivedChats'), style: const TextStyle(color: Colors.black54)));
          }"""
    if new not in source and 'if(snap.hasError||(_arsivKismi&&docs.isEmpty))' not in source:
        assert source.count(old) == 1
        source = source.replace(old, new)
    old = """    await FirebaseFirestore.instance.collection('users').doc(ben).set({'mutedChats':sessiz?FieldValue.arrayUnion([chatId]):FieldValue.arrayRemove([chatId])},SetOptions(merge:true));
    if(!sessiz)await FirebaseFirestore.instance.collection('users').doc(ben).update({'mutedChatUntil.$chatId':FieldValue.delete()});
    if(mounted)setState(()=>sessiz?sessizSohbetler.add(chatId):sessizSohbetler.remove(chatId));"""
    new = """    try{
      // One write: never leave the mute membership and deadline out of sync.
      await FirebaseFirestore.instance.collection('users').doc(ben).set({
        'mutedChats':sessiz?FieldValue.arrayUnion([chatId]):FieldValue.arrayRemove([chatId]),
        if(!sessiz)'mutedChatUntil':{chatId:FieldValue.delete()},
      },SetOptions(merge:true)).timeout(const Duration(seconds:12));
      if(!mounted||uid!=ben)return;
      setState(()=>sessiz?sessizSohbetler.add(chatId):sessizSohbetler.remove(chatId));
      ngelxDurumMesaji(context,sessiz?'Sohbet sessize alındı.':'Sohbetin sessizliği kaldırıldı.',tip:'basari');
    }catch(error){
      if(mounted&&uid==ben)ngelxDurumMesaji(context,'Bildirim tercihi doğrulanamadı. Yeniden dene.',tip:'hata');
    }"""
    if new not in source:
        assert source.count(old) == 1
        source = source.replace(old, new)
    old = """    await kullanici.set({'mutedChats':FieldValue.arrayUnion([chatId])},SetOptions(merge:true));
    await kullanici.update({'mutedChatUntil.$chatId':DateTime.now().add(secim).toUtc().toIso8601String()});"""
    new = """    await kullanici.set({
      'mutedChats':FieldValue.arrayUnion([chatId]),
      'mutedChatUntil':{chatId:DateTime.now().add(secim).toUtc().toIso8601String()},
    },SetOptions(merge:true)).timeout(const Duration(seconds:12));"""
    if new not in source:
        assert source.count(old) == 1
        source = source.replace(old, new)
    # set(merge) takes nested maps, not update-style dotted field paths.
    old = """    if(secim=='forever')g['mutedChatUntil.$chatId']=FieldValue.delete();
    else{
      final sure=secim=='1h'?const Duration(hours:1):secim=='8h'?const Duration(hours:8):const Duration(days:7);
      g['mutedChatUntil.$chatId']=DateTime.now().add(sure).toUtc().toIso8601String();
    }"""
    new = """    if(secim=='forever')g['mutedChatUntil']={chatId:FieldValue.delete()};
    else{
      final sure=secim=='1h'?const Duration(hours:1):secim=='8h'?const Duration(hours:8):const Duration(days:7);
      g['mutedChatUntil']={chatId:DateTime.now().add(sure).toUtc().toIso8601String()};
    }"""
    if new not in source:
        assert source.count(old) == 1
        source = source.replace(old, new)
    old = """class _ArsivSohbetlerPageState extends State<ArsivSohbetlerPage> {
  Future<List<DocumentSnapshot<Map<String,dynamic>>>> arsivGetir() async {"""
    new = """class _ArsivSohbetlerPageState extends State<ArsivSohbetlerPage> {
  late Future<List<DocumentSnapshot<Map<String,dynamic>>>> _arsiv = arsivGetir();
  bool _arsivKismi=false;
  void _arsivYenile()=>setState((){_arsiv=arsivGetir();});
  Future<List<DocumentSnapshot<Map<String,dynamic>>>> arsivGetir() async {
    _arsivKismi=false;"""
    if new not in source:
        assert source.count(old) == 1
        source = source.replace(old, new)
    old = """    final eski=await FirebaseFirestore.instance.collection('chats').where('formerMembers',arrayContains:widget.uid).limit(60).get();
    final kayitlar=await FirebaseFirestore.instance.collection('group_archives').doc(widget.uid).collection('items').limit(60).get();
    final ids=<String>{
      ...manuel,
      ...eski.docs.map((e)=>e.id),
      ...kayitlar.docs.map((e)=>(e.data()['chatId']??e.id).toString()).where((e)=>e.isNotEmpty),
    };
    final docs=await Future.wait(ids.map((id)=>FirebaseFirestore.instance.collection('chats').doc(id).get()));"""
    new = """    // Legacy group discovery must not hide manually archived private chats.
    final ids=<String>{...manuel};
    try{
      final eski=await FirebaseFirestore.instance.collection('chats').where('formerMembers',arrayContains:widget.uid).limit(60).get().timeout(const Duration(seconds:12));
      ids.addAll(eski.docs.map((e)=>e.id));
    }catch(_){_arsivKismi=true;}
    try{
      final kayitlar=await FirebaseFirestore.instance.collection('group_archives').doc(widget.uid).collection('items').limit(60).get().timeout(const Duration(seconds:12));
      ids.addAll(kayitlar.docs.map((e)=>(e.data()['chatId']??e.id).toString()).where((e)=>e.isNotEmpty));
    }catch(_){_arsivKismi=true;}
    final docs=<DocumentSnapshot<Map<String,dynamic>>>[];
    await Future.wait(ids.map((id)async{
      try{
        final d=await FirebaseFirestore.instance.collection('chats').doc(id).get().timeout(const Duration(seconds:12));
        docs.add(d);
      }catch(_){_arsivKismi=true;}
    }));"""
    if new not in source:
        assert source.count(old) == 1
        source = source.replace(old, new)
    # Scope replacements to archive state, preserving unrelated refresh behavior.
    start=source.index('class _ArsivSohbetlerPageState ')
    end=source.index('\nclass ',start+1)
    block=source[start:end]
    block=block.replace('if (mounted) setState(() {});','if (mounted) _arsivYenile();')
    block=block.replace('if(mounted)setState((){});','if(mounted)_arsivYenile();')
    block=block.replace('future: arsivGetir(),','future: _arsiv,')
    block=block.replace("if(snap.hasError)return ngelx432YuklemeHatasi(()=>setState((){}),'Arşivlenen sohbetler yüklenemedi.');", "if(snap.hasError||(_arsivKismi&&docs.isEmpty))return ngelx432YuklemeHatasi(_arsivYenile,'Arşivlenen sohbetler yüklenemedi.');")
    # Nonempty partial results remain visible, with an explicit retry notice.
    if 'Expanded(child:ListView.separated(' not in block:
        block=block.replace('return ListView.separated(', "return Column(children:[\n            if(_arsivKismi)ListTile(title:const Text('Bazı arşiv kayıtları yüklenemedi.'),trailing:TextButton(onPressed:_arsivYenile,child:const Text('Yeniden dene'))),\n            Expanded(child:ListView.separated(")
    marker='''          );
        },
      ),'''
    if 'Expanded(child:ListView.separated(' in block and marker in block:
        block=block.replace(marker,'''          ))]);
        },
      ),''',1)
    source=source[:start]+block+source[end:]
    path.write_text(source)


if __name__ == '__main__':
    apply()
