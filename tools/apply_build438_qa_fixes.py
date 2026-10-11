"""Apply phone-QA fixes after the Build437 source generation pipeline.

Do not commit the generated app tree: keep the reproducible patch here.
"""
from pathlib import Path
import re


def apply():
    path = Path('app/lib/main.dart')
    source = path.read_text()

    def replace(old, new, count=1):
        nonlocal source
        if new and source.count(new) == count and old in new:
            return
        if old not in source and source.count(new) >= count:
            return
        assert source.count(old) == count, (old[:100], source.count(old), count)
        source = source.replace(old, new)

    # Recreate the auth root instead of returning to a route that may retain a
    # login/account gate from the previous session. The root owns userChanges.
    replace(
        'ngelxNavigatorKey.currentState?.popUntil((route)=>route.isFirst);',
        "ngelxNavigatorKey.currentState?.pushNamedAndRemoveUntil('/',(route)=>false);",
    )
    # A cache read can hang during an auth transition too; bound every stage.
    replace(
        'final onbellek=await ref.get(const GetOptions(source:Source.cache));',
        'final onbellek=await ref.get(const GetOptions(source:Source.cache)).timeout(const Duration(seconds:2));',
    )
    replace(
        'unawaited(ref.get(const GetOptions(source:Source.server)).then((guncel){',
        'unawaited(ref.get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:8)).then((guncel){',
    )
    # Restriction suppresses notifications (the existing notification filter
    # already enforces it), while block/permission checks still deny messages.
    replace(
        "      final onunKisitladiklari=List<String>.from(diger['restrictedUsers']??const[]);\n",
        '      // Restriction filters notifications; it does not block sending.\n',
    )
    replace(
        "      else if(onunKisitladiklari.contains(ben))engel='Bu kullanıcı mesajlarını sınırlandırdı.';\n",
        '',
    )
    replace(
        "      if(stringList(hedef['restrictedUsers']).contains(me)){\n"
        "        if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Bu kullanıcı mesajlarını sınırlandırdı.')));\n"
        "        return;\n      }\n",
        '      // Restricted senders may open a chat; their notifications are filtered.\n',
    )
    replace(
        "if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(kisitli?'Kısıtlama kaldırıldı.':'Kullanıcı kısıtlandı. Bildirimleri sessizce filtrelenecek.')));",
        "if(context.mounted)ngelxDurumMesaji(context,kisitli?'Kısıtlama kaldırıldı.':'Kullanıcı kısıtlandı. Bildirimleri sessizce filtrelenecek.',tip:'basari');",
    )
    replace(
        "if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Kurtarma seçenekleri kaydedildi.')));",
        "if(mounted)ngelxDurumMesaji(context,'Kurtarma seçenekleri kaydedildi.',tip:'basari');",
    )
    replace(
        "liste(diger['blocked']).contains(ben.uid)||\n         liste(diger['restrictedUsers']).contains(ben.uid)",
        "liste(diger['blocked']).contains(ben.uid)",
    )
    # Quoted previews use the same access/expiry-aware jump as message search.
    for marker, end in [
        ('if(yanit.isNotEmpty)Container(', "                if(tur=='sticker'"),
        ("if((v['replyText']??'').toString().trim().isNotEmpty)\n              Container(", '            if(photo)'),
    ]:
        if marker not in source:
            continue
        start = source.index(marker)
        stop = source.index(end, start)
        block = source[start:stop]
        container = block.index('Container(')
        block = block[:container] + "GestureDetector(\n                  onTap:()=>jumpToMessage((v['replyToId']??'').toString()),\n                  child:" + block[container:]
        last = block.rfind('),')
        block = block[:last] + ')),' + block[last + 2:]
        source = source[:start] + block + source[stop:]
    replace(
        "builder:(c)=>AlertDialog(title:Text(baslik),content:Text(aciklama),actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),FilledButton(onPressed:()=>Navigator.pop(c,true),style:FilledButton.styleFrom(backgroundColor:Colors.red),child:Text(dugme))])",
        "builder:(c)=>Theme(data:ThemeData.light(),child:AlertDialog(backgroundColor:Colors.white,surfaceTintColor:Colors.white,title:Text(baslik),content:Text(aciklama),actions:[TextButton(onPressed:()=>Navigator.pop(c,false),child:const Text('Vazgeç')),FilledButton(onPressed:()=>Navigator.pop(c,true),style:FilledButton.styleFrom(backgroundColor:Colors.red,foregroundColor:Colors.white),child:Text(dugme))]))",
    )
    feed_start = source.index('class _VideoAkisiState')
    feed_end = source.index('class AramaPage', feed_start)
    feed = source[feed_start:feed_end]
    if 'return SafeArea(bottom:false,child:Stack(children:[' not in feed:
        assert feed.count('return Stack(children:[') == 1
        feed = feed.replace('return Stack(children:[', 'return SafeArea(bottom:false,child:Stack(children:[', 1)
        stop = feed.rfind('    ]);')
        assert stop >= 0
        feed = feed[:stop] + feed[stop:].replace('    ]);', '    ]));', 1)
        source = source[:feed_start] + feed + source[feed_end:]
    # Registration already enforces 3..20; make the limit visible too.
    source = re.sub(r'(?:3–20 karakter • )+Boşluk kullanılamaz', 'Boşluk kullanılamaz', source)
    replace("Boşluk kullanılamaz • harf, sayı, nokta ve _", "3–20 karakter • Boşluk kullanılamaz • harf, sayı, nokta ve _")
    if 'Future<void> ngelx438TransferBeforeExit(' not in source:
        helper = Path('tools/build438_group_successor.dart').read_text() + '''
Future<void> ngelx438TransferBeforeExit(DocumentReference<Map<String,dynamic>> ref,String leaving)async{
  await FirebaseFirestore.instance.runTransaction((tx)async{
    final snapshot=await tx.get(ref);
    final data=snapshot.data()??<String,dynamic>{};
    final members=List<String>.from(data['members']??const[]);
    if(!members.contains(leaving))throw StateError('Artık bu grubun üyesi değilsin.');
    if(data['createdBy']!=leaving)return;
    final admins=List<String>.from(data['admins']??const[]);
    final successor=ngelx438Successor(members,admins,leaving);
    if(successor==null)return;
    tx.update(ref,{'createdBy':successor,'admins':FieldValue.arrayUnion([successor]),'updatedAt':FieldValue.serverTimestamp()});
  }).timeout(const Duration(seconds:12));
}
'''
        source += '\n' + helper
        sections=[
            ('  Future<void> gelenKutusundanGruptanAyril(', '  Future<void> sohbetMenusu(', 'ben', 'id'),
            ('  Future<void> ayril(List<String> uyeler,List<String> admins)', '  @override', 'me', 'widget.chatId'),
            ('  Future<void> _ayril(BuildContext context,Map<String,dynamic> v)', '  @override', 'uid', 'chatId'),
        ]
        for start_marker,end_marker,who,chat in sections:
            start=source.index(start_marker)
            end=source.index(end_marker,start)
            part=source[start:end]
            guard=f'    if(kurucu=={who}&&uyeler.length>1){{'
            a=part.index(guard)
            b=part.index('    if(admins.length==1',a)
            part=part[:a]+part[b:]
            part=part.replace(f'if(admins.length==1&&admins.contains({who})&&uyeler.length>1)',f'if(kurucu!={who}&&admins.length==1&&admins.contains({who})&&uyeler.length>1)',1)
            part=part.replace('    if(!ok)return;',f'''    if(!ok)return;
    try{{await ngelx438TransferBeforeExit(ref,{who});}}
    catch(_){{if(context.mounted)ngelxDurumMesaji(context,'Kuruculuk devri veya çıkış kontrolü tamamlanamadı. Tekrar dene.',tip:'hata');return;}}''',1)
            source=source[:start]+part+source[end:]
    # Do not recreate the stream on every keystroke. A new stream briefly
    # replaces the entire search subtree with a spinner and drops keyboard focus.
    start=source.index('class _KullaniciListesiPageState')
    end=source.index('\nclass ',start+10)
    part=source[start:end]
    if '_people438Stream' not in part:
        part=part.replace("  String arama='';", """  String arama='';
  late final Stream<DocumentSnapshot<Map<String,dynamic>>> _people438Stream;
  Future<List<DocumentSnapshot<Map<String,dynamic>>>>? _people438Future;
  String _people438Ids='';
  @override void initState(){
    super.initState();
    _people438Stream=FirebaseFirestore.instance.collection('users').doc(widget.uid).snapshots();
  }
  Future<List<DocumentSnapshot<Map<String,dynamic>>>> _people438Profiles(List<String> ids){
    final key=ids.join('|');
    if(_people438Future==null||key!=_people438Ids){
      _people438Ids=key;
      _people438Future=Future.wait(ids.map(_profilGetir));
    }
    return _people438Future!;
  }""",1)
        part=part.replace("stream:FirebaseFirestore.instance.collection('users').doc(widget.uid).snapshots(),",'stream:_people438Stream,',1)
        part=part.replace('future:Future.wait(ids.map(_profilGetir)),','future:_people438Profiles(ids),',1)
        source=source[:start]+part+source[end:]
    path.write_text(source)

    # Keep search aliases on the combined entries instead of duplicate results.
    settings = Path('app/lib/build258_settings.dart')
    text = settings.read_text()
    for label in ['Engellenen hesaplar', 'Kısıtlanan hesaplar', 'Hesap kurtarma']:
        text, _ = re.subn(
            r"    _NgelXAyarOgesi\(\n      bolum:'[^']+',baslik:'" + label + r"',[\s\S]*?\n    \),\n",
            '', text, count=1,
        )
    settings.write_text(text)


if __name__ == '__main__':
    apply()
