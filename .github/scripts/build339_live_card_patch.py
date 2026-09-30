from pathlib import Path

main_path=Path('app/lib/main.dart')
pubspec_path=Path('app/pubspec.yaml')
s=main_path.read_text(encoding='utf-8')

helper_marker="  Widget ozelMesajKarti(QueryDocumentSnapshot<Map<String,dynamic>> d,{double fontSize=16,bool goruldu=false,String quickReaction='❤️'}){"
helper="""  Future<void> canliPaylasimMesajiniAc(Map<String,dynamic> v)async{
    var canliId=(v['liveId']??v['sourceId']??v['belgeId']??'').toString().trim();
    if(canliId.isEmpty){
      final ham=(v['text']??v['message']??v['content']??'').toString();
      final eslesme=RegExp(r'ngelx://live/([A-Za-z0-9_-]+)').firstMatch(ham);
      canliId=eslesme?.group(1)??'';
    }
    if(canliId.isEmpty){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
        content:Text('Canlı yayın bağlantısı bulunamadı.',style:TextStyle(fontWeight:FontWeight.w800)),
        behavior:SnackBarBehavior.floating,
      ));
      return;
    }
    try{
      final canli=await FirebaseFirestore.instance.collection('live_streams').doc(canliId)
          .get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:8));
      final veri=canli.data()??<String,dynamic>{};
      if(!canli.exists||!ngelxCanliKaydiTaze(veri)){
        if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content:const Text('Bu canlı yayın bitti.',style:TextStyle(fontWeight:FontWeight.w800)),
          behavior:SnackBarBehavior.floating,
          width:230,
          duration:const Duration(milliseconds:1400),
          shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(14)),
        ));
        return;
      }
      if(mounted)await ngelxCanliYayinaKatil(context,canliId);
    }on TimeoutException{
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
        content:Text('Canlı yayın kontrolü zaman aşımına uğradı. Tekrar dene.',style:TextStyle(fontWeight:FontWeight.w700)),
        behavior:SnackBarBehavior.floating,
      ));
    }catch(_){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
        content:Text('Canlı yayın açılamadı. Bağlantını kontrol edip tekrar dene.',style:TextStyle(fontWeight:FontWeight.w700)),
        behavior:SnackBarBehavior.floating,
      ));
    }
  }

"""
if 'Future<void> canliPaylasimMesajiniAc(' not in s:
    if helper_marker not in s:
        raise SystemExit('ozelMesajKarti helper marker bulunamadi')
    s=s.replace(helper_marker,helper+helper_marker,1)

vars_old="""    final v=d.data(),ben=v['senderId']==uid,tur=(v['type']??'text').toString();
    final photo=tur=='photo',video=tur=='video',shared=tur=='shared_content',audio=tur=='audio',file=tur=='file',location=tur=='location',call=tur=='call',storyReply=tur=='story_reply';"""
vars_new="""    final v=d.data(),ben=v['senderId']==uid,tur=(v['type']??'text').toString();
    final canliPaylasimi=v['liveShare']==true||tur=='live_share'||(v['liveId']??'').toString().trim().isNotEmpty;
    final canliBaslik=(v['liveTitle']??'Canlı yayın').toString().trim();
    final canliKullanici=(v['liveUsername']??'').toString().trim();
    final photo=tur=='photo',video=tur=='video',shared=tur=='shared_content',audio=tur=='audio',file=tur=='file',location=tur=='location',call=tur=='call',storyReply=tur=='story_reply';"""
if "final canliPaylasimi=v['liveShare']==true" not in s:
    if vars_old not in s:
        raise SystemExit('live card vars marker bulunamadi')
    s=s.replace(vars_old,vars_new,1)

tap_old="""        onTap:photo
          ? ()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>TamEkranMedyaPage(url:medyaUrl)))"""
tap_new="""        onTap:canliPaylasimi
          ? ()=>canliPaylasimMesajiniAc(v)
          : photo
          ? ()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>TamEkranMedyaPage(url:medyaUrl)))"""
if 'onTap:canliPaylasimi' not in s:
    if tap_old not in s:
        raise SystemExit('live card tap marker bulunamadi')
    s=s.replace(tap_old,tap_new,1)

render_old="""            else if(storyReply)
              Row(crossAxisAlignment:CrossAxisAlignment.center,children:["""
render_new="""            else if(canliPaylasimi)
              Column(crossAxisAlignment:CrossAxisAlignment.stretch,children:[
                Row(children:[
                  Container(
                    width:34,height:34,
                    decoration:const BoxDecoration(color:Color(0xFFFF1744),shape:BoxShape.circle),
                    child:const Icon(Icons.live_tv_rounded,color:Colors.white,size:19),
                  ),
                  const SizedBox(width:10),
                  Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                    Text('CANLI',style:TextStyle(color:ben?Colors.white70:const Color(0xFFFF1744),fontSize:10.5,fontWeight:FontWeight.w900,letterSpacing:.4)),
                    const SizedBox(height:2),
                    Text(canliBaslik.isEmpty?'Canlı yayın':canliBaslik,maxLines:2,overflow:TextOverflow.ellipsis,style:TextStyle(color:ben?Colors.white:Colors.black87,fontSize:fontSize,fontWeight:FontWeight.w900)),
                    if(canliKullanici.isNotEmpty)Text('@'+canliKullanici,maxLines:1,overflow:TextOverflow.ellipsis,style:TextStyle(color:ben?Colors.white70:Colors.black54,fontSize:11.5,fontWeight:FontWeight.w700)),
                  ])),
                ]),
                const SizedBox(height:9),
                Row(children:[
                  Icon(Icons.touch_app_rounded,color:ben?Colors.white70:ngelxPrivateBlue,size:16),
                  const SizedBox(width:5),
                  Expanded(child:Text('Yayına gitmek için dokun',style:TextStyle(color:ben?Colors.white70:ngelxPrivateBlue,fontSize:11.5,fontWeight:FontWeight.w800))),
                ]),
              ])
            else if(storyReply)
              Row(crossAxisAlignment:CrossAxisAlignment.center,children:["""
if "Text('Yayına gitmek için dokun'" not in s:
    if render_old not in s:
        raise SystemExit('live card render marker bulunamadi')
    s=s.replace(render_old,render_new,1)

activity_marker="""  bool _canliAktivitesi(Map<String,dynamic> v){
    final tur=(v['type']??'').toString();
    final hedef=(v['targetKind']??'').toString();
    final olay=(v['eventKind']??'').toString();
    return tur=='live'||hedef=='live'||olay=='live_started'||olay=='live_share'||olay=='live_pk_request'||olay=='live_pk_accept';
  }

"""
activity_helper="""  String _aktiviteTekilAnahtar(QueryDocumentSnapshot<Map<String,dynamic>> d){
    final v=d.data();
    final tur=(v['type']??'').toString();
    final olay=(v['eventKind']??'').toString();
    final kaynak=(v['sourceId']??v['belgeId']??'').toString();
    final from=(v['fromUid']??v['senderId']??v['senderUid']??'').toString();
    final genelCanli=olay=='live_started'||olay=='live_share'||(tur=='live'&&!olay.startsWith('live_pk_'));
    if(genelCanli&&kaynak.isNotEmpty)return 'live|'+kaynak+'|'+from;
    return 'doc|'+d.id;
  }

"""
if 'String _aktiviteTekilAnahtar(' not in s:
    if activity_marker not in s:
        raise SystemExit('activity helper marker bulunamadi')
    s=s.replace(activity_marker,activity_marker+activity_helper,1)

dedupe_old="""          final tumDocs = (s.data?.docs ?? []).toList()
            ..sort((a, b) {
              final at = a.data()['createdAt'];
              final bt = b.data()['createdAt'];
              final ad = at is Timestamp ? at.toDate() : DateTime.fromMillisecondsSinceEpoch(0);
              final bd = bt is Timestamp ? bt.toDate() : DateTime.fromMillisecondsSinceEpoch(0);
              return bd.compareTo(ad);
            });"""
dedupe_new="""          final gelenDocs=(s.data?.docs??[]).toList();
          int bildirimZamani(QueryDocumentSnapshot<Map<String,dynamic>> d){
            final ham=d.data()['createdAt'];
            return ham is Timestamp?ham.millisecondsSinceEpoch:0;
          }
          final tekil=<String,QueryDocumentSnapshot<Map<String,dynamic>>>{};
          for(final d in gelenDocs){
            final anahtar=_aktiviteTekilAnahtar(d);
            final onceki=tekil[anahtar];
            if(onceki==null){
              tekil[anahtar]=d;
              continue;
            }
            final yeniZaman=bildirimZamani(d),eskiZaman=bildirimZamani(onceki);
            if(yeniZaman>eskiZaman||(yeniZaman==eskiZaman&&onceki.data()['read']==true&&d.data()['read']!=true)){
              tekil[anahtar]=d;
            }
          }
          final tumDocs=tekil.values.toList()
            ..sort((a,b)=>bildirimZamani(b).compareTo(bildirimZamani(a)));"""
if 'final gelenDocs=(s.data?.docs??[]).toList();' not in s:
    if dedupe_old not in s:
        raise SystemExit('activity dedupe marker bulunamadi')
    s=s.replace(dedupe_old,dedupe_new,1)

if "defaultValue: '1.0.119'" in s:
    s=s.replace("defaultValue: '1.0.119'","defaultValue: '1.0.120'",1)
if "defaultValue: '338'" in s:
    s=s.replace("defaultValue: '338'","defaultValue: '339'",1)
if "defaultValue: '1.0.120'" not in s or "defaultValue: '339'" not in s:
    raise SystemExit('main.dart version patch basarisiz')

main_path.write_text(s,encoding='utf-8')

pub=pubspec_path.read_text(encoding='utf-8')
if 'version: 1.0.119+338' in pub:
    pub=pub.replace('version: 1.0.119+338','version: 1.0.120+339',1)
if 'version: 1.0.120+339' not in pub:
    raise SystemExit('pubspec version patch basarisiz')
pubspec_path.write_text(pub,encoding='utf-8')

print('Build 339 patch applied successfully')
