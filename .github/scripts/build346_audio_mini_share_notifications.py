from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
main_path=ROOT/'app/lib/main.dart'
pub_path=ROOT/'app/pubspec.yaml'

main=main_path.read_text(encoding='utf-8')
pub=pub_path.read_text(encoding='utf-8')

def rep(text,old,new,label):
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f'{label}: kaynak bulunamadi')
    return text.replace(old,new,1)

# Part + version.
main=rep(main,"part 'audio_live_rooms_pro.dart';","part 'audio_live_rooms_pro.dart';\npart 'audio_live_rooms_extras.dart';",'extras part')
main=rep(main,"defaultValue: '1.0.126'","defaultValue: '1.0.127'",'version name')
main=rep(main,"defaultValue: '345'","defaultValue: '346'",'build number')
pub=rep(pub,'version: 1.0.126+345','version: 1.0.127+346','pubspec version')

# Global mini audio overlay on every route.
old_builder="builder: (context, child) => Directionality(textDirection: dil=='ar' ? TextDirection.rtl : TextDirection.ltr, child: child!),"
new_builder="builder: (context, child) => Directionality(textDirection: dil=='ar' ? TextDirection.rtl : TextDirection.ltr, child:Stack(children:[Positioned.fill(child:child!),const NgelxSesliMiniGlobalOverlay()])),"
main=rep(main,old_builder,new_builder,'material app mini overlay')

# Activity selection state.
old_fields="""  String _filtre='all';
  List<QueryDocumentSnapshot<Map<String,dynamic>>> _sunucuAktiviteleri=[];
  bool _aktiviteYenileniyor=false;
"""
new_fields="""  String _filtre='all';
  List<QueryDocumentSnapshot<Map<String,dynamic>>> _sunucuAktiviteleri=[];
  bool _aktiviteYenileniyor=false;
  final Set<String> _secilenBildirimler=<String>{};
  bool get _secimModu=>_secilenBildirimler.isNotEmpty;
"""
main=rep(main,old_fields,new_fields,'activity selection fields')

# Activity delete helpers before filter function.
anchor="  bool _filtreUyar(Map<String,dynamic> v){"
helpers="""  void _bildirimSec(String id){
    if(id.isEmpty)return;
    setState((){
      if(!_secilenBildirimler.add(id))_secilenBildirimler.remove(id);
    });
  }

  Future<void> _secilenBildirimleriSil()async{
    final uid=FirebaseAuth.instance.currentUser?.uid;
    final ids=_secilenBildirimler.toList();
    if(uid==null||ids.isEmpty)return;
    try{
      final batch=FirebaseFirestore.instance.batch();
      for(final id in ids){
        batch.delete(FirebaseFirestore.instance.collection('notifications').doc(id));
      }
      await batch.commit().timeout(const Duration(seconds:12));
      if(!mounted)return;
      setState((){
        _sunucuAktiviteleri.removeWhere((d)=>ids.contains(d.id));
        _secilenBildirimler.clear();
      });
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(ids.length.toString()+' bildirim silindi.')));
    }catch(_){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Bildirimler silinemedi. Tekrar dene.')));
    }
  }

"""
if helpers not in main:
    if anchor not in main: raise SystemExit('activity helper anchor missing')
    main=main.replace(anchor,helpers+anchor,1)

# Audio activity icon / color.
main=rep(
    main,
    "IconData _ikon(String tur){switch(tur){case 'live':return Icons.live_tv_rounded;",
    "IconData _ikon(String tur){switch(tur){case 'audio_live':return Icons.graphic_eq_rounded;case 'live':return Icons.live_tv_rounded;",
    'audio activity icon',
)
main=rep(
    main,
    "Color _renk(String tur){switch(tur){case 'live':return const Color(0xFFFF1744);",
    "Color _renk(String tur){switch(tur){case 'audio_live':return mor;case 'live':return const Color(0xFFFF1744);",
    'audio activity color',
)

# Audio activity click.
audio_anchor="    final canliHedefi=tur=='live'||hedefTuru=='live'||olay=='live_started'||olay=='live_share';\n\n"
audio_insert="""    final canliHedefi=tur=='live'||hedefTuru=='live'||olay=='live_started'||olay=='live_share';
    final sesliHedefi=tur=='audio_live'||hedefTuru=='audio_room'||olay=='audio_room_started';

    if(sesliHedefi&&kaynak.isNotEmpty){
      await ngelxSesliOdayaKatil(context,kaynak);
      return;
    }

"""
main=rep(main,audio_anchor,audio_insert,'audio activity open')

# Rebuild activity AppBar to support long-press multi-select + direct delete.
class_start=main.index("class _AktivitePageState")
build_start=main.index("  @override\n  Widget build(BuildContext context) {",class_start)
app_start=main.index("      appBar: AppBar(",build_start)
body_start=main.index("      body: StreamBuilder",app_start)
new_appbar="""      appBar: AppBar(
        title:Text(_secimModu?(_secilenBildirimler.length.toString()+' seçildi'):t('activity'),style:const TextStyle(fontWeight:FontWeight.w900)),
        actions:_secimModu
          ?[
              IconButton(tooltip:'Sil',onPressed:_secilenBildirimleriSil,icon:const Icon(Icons.delete_forever_rounded,color:Colors.red)),
              IconButton(tooltip:'Seçimi kapat',onPressed:()=>setState(()=>_secilenBildirimler.clear()),icon:const Icon(Icons.close_rounded,color:Colors.black54)),
            ]
          :[
              IconButton(tooltip:lt('Yenile','Refresh'),onPressed:_aktiviteYenileniyor?null:()=>_aktiviteyiYenile(),icon:_aktiviteYenileniyor?const SizedBox(width:19,height:19,child:CircularProgressIndicator(strokeWidth:2,color:mor)):const Icon(Icons.refresh_rounded,color:mor)),
              IconButton(tooltip:t('markAllRead'),onPressed:()async{
                if(uid==null)return;
                try{
                  final q=await FirebaseFirestore.instance.collection('notifications').where('toUid',isEqualTo:uid).limit(200).get().timeout(const Duration(seconds:10));
                  final b=FirebaseFirestore.instance.batch();
                  for(final d in q.docs){b.set(d.reference,{'read':true},SetOptions(merge:true));}
                  await b.commit().timeout(const Duration(seconds:10));
                  if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Tüm aktiviteler okundu olarak işaretlendi.')));
                }catch(_){
                  if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Aktiviteler güncellenemedi. Tekrar dene.')));
                }
              },icon:const Icon(Icons.done_all_rounded,color:Color(0xFF20B86A))),
            ],
      ),
"""
main=main[:app_start]+new_appbar+main[body_start:]

# Activity rows: selection visuals and behavior.
old_pending="""            final bekliyor = (v['type'] == 'follow_request' || v['type'] == 'friend_request') && v['status'] == 'pending';
            return Container("""
new_pending="""            final bekliyor = (v['type'] == 'follow_request' || v['type'] == 'friend_request') && v['status'] == 'pending';
            final secili=_secilenBildirimler.contains(d.id);
            return Container("""
main=rep(main,old_pending,new_pending,'activity selected variable')

old_leading="""              leading: Stack(children:[CircleAvatar(radius:26,backgroundColor:renk.withValues(alpha:.13),backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?Icon(ikon,color:renk):null),if(!okundu)Positioned(right:0,top:0,child:CircleAvatar(radius:5,backgroundColor:grup?ngelxGroupGreen:const Color(0xFF7C3AED)))]),"""
new_leading="""              leading:secili
                ?const CircleAvatar(radius:26,backgroundColor:mor,child:Icon(Icons.check_rounded,color:Colors.white))
                :Stack(children:[CircleAvatar(radius:26,backgroundColor:renk.withValues(alpha:.13),backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?Icon(ikon,color:renk):null),if(!okundu)Positioned(right:0,top:0,child:CircleAvatar(radius:5,backgroundColor:grup?ngelxGroupGreen:const Color(0xFF7C3AED)))]),"""
main=rep(main,old_leading,new_leading,'activity selected leading')

main=rep(
    main,
    "              onTap: () => _aktiviteAc(context,d),",
    "              onLongPress:()=>_bildirimSec(d.id),\n              onTap:()=>_secimModu?_bildirimSec(d.id):_aktiviteAc(context,d),",
    'activity long press selection',
)

# Private chat: audio room share becomes tappable.
main=rep(
    main,
    "    final canliPaylasimi=v['liveShare']==true||tur=='live_share'||(v['liveId']??'').toString().trim().isNotEmpty;\n",
    "    final canliPaylasimi=v['liveShare']==true||tur=='live_share'||(v['liveId']??'').toString().trim().isNotEmpty;\n    final sesliOdaPaylasimi=tur=='audio_room_share'||(v['audioRoomId']??'').toString().trim().isNotEmpty;\n",
    'private audio share flag',
)
main=rep(
    main,
    "        onTap:canliPaylasimi\n          ? ()=>canliPaylasimMesajiniAc(v)",
    "        onTap:sesliOdaPaylasimi\n          ? ()=>ngelxSesliPaylasimMesajiniAc(context,v)\n          : canliPaylasimi\n          ? ()=>canliPaylasimMesajiniAc(v)",
    'private audio share tap',
)

# Group chat: audio room share becomes tappable.
group_flag_old="""    final metin=(v['text']??v['message']??v['content']??'').toString(),tur=(v['type']??'text').toString();
    final media=ngelxMesajMedyaUrl(v,video:tur=='video'),"""
group_flag_new="""    final metin=(v['text']??v['message']??v['content']??'').toString(),tur=(v['type']??'text').toString();
    final sesliOdaPaylasimi=tur=='audio_room_share'||(v['audioRoomId']??'').toString().trim().isNotEmpty;
    final media=ngelxMesajMedyaUrl(v,video:tur=='video'),"""
main=rep(main,group_flag_old,group_flag_new,'group audio share flag')

main=rep(
    main,
    "            onTap:(tur=='photo'||tur=='gif')&&media.isNotEmpty\n              ? ()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>TamEkranMedyaPage(url:media)))",
    "            onTap:sesliOdaPaylasimi\n              ? ()=>ngelxSesliPaylasimMesajiniAc(context,v)\n              : (tur=='photo'||tur=='gif')&&media.isNotEmpty\n              ? ()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>TamEkranMedyaPage(url:media)))",
    'group audio share tap',
)

main_path.write_text(main,encoding='utf-8')
pub_path.write_text(pub,encoding='utf-8')
print('Build 346 main patch applied')
