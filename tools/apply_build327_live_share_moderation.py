#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN=ROOT/"app/lib/main.dart"
LIVE=ROOT/"app/lib/live_broadcast_studio.dart"
PUB=ROOT/"app/pubspec.yaml"

main=MAIN.read_text(encoding="utf-8")
live=LIVE.read_text(encoding="utf-8")
pub=PUB.read_text(encoding="utf-8")

def rep(text,old,new,label):
    if old not in text:
        raise SystemExit("Build 327 patch failed: marker not found: "+label)
    return text.replace(old,new,1)

def rep_between(text,start,end,new,label):
    a=text.find(start)
    if a<0: raise SystemExit("Build 327 patch failed: start marker not found: "+label)
    b=text.find(end,a+len(start))
    if b<0: raise SystemExit("Build 327 patch failed: end marker not found: "+label)
    return text[:a]+new+text[b:]

pub=rep(pub,"version: 1.0.107+326","version: 1.0.108+327","version")
main=main.replace("defaultValue: '1.0.107'","defaultValue: '1.0.108'")
main=main.replace("defaultValue: '326'","defaultValue: '327'")

live=rep(live,
"""const List<_NgelXCanliFiltrePreset> ngelxCanliProFiltreleri=[
  _NgelXCanliFiltrePreset('Doğal',parlaklik:.02,kontrast:1.06,doygunluk:1.05,sicaklik:.02,netlik:.10),
  _NgelXCanliFiltrePreset('Canlı',parlaklik:.035,kontrast:1.18,doygunluk:1.20,sicaklik:.04,netlik:.18),
  _NgelXCanliFiltrePreset('Portre Pro',parlaklik:.05,kontrast:1.10,doygunluk:1.08,sicaklik:.08,netlik:.08),
  _NgelXCanliFiltrePreset('Clean HD',parlaklik:.035,kontrast:1.13,doygunluk:1.03,sicaklik:0,netlik:.22),
  _NgelXCanliFiltrePreset('Parlak',parlaklik:.08,kontrast:1.08,doygunluk:1.10,sicaklik:.03,netlik:.08),
  _NgelXCanliFiltrePreset('Sıcak',parlaklik:.03,kontrast:1.10,doygunluk:1.12,sicaklik:.20,netlik:.10),
  _NgelXCanliFiltrePreset('Soğuk',parlaklik:.02,kontrast:1.11,doygunluk:1.08,sicaklik:-.15,netlik:.12),
  _NgelXCanliFiltrePreset('Kontrast+',parlaklik:.01,kontrast:1.28,doygunluk:1.12,sicaklik:.02,netlik:.25),
  _NgelXCanliFiltrePreset('Gece',parlaklik:.12,kontrast:1.08,doygunluk:1.06,sicaklik:.05,netlik:.06),
];""",
"""const List<_NgelXCanliFiltrePreset> ngelxCanliProFiltreleri=[
  _NgelXCanliFiltrePreset('Doğal',parlaklik:-.015,kontrast:1.03,doygunluk:1.02,sicaklik:.01,netlik:.06),
  _NgelXCanliFiltrePreset('Canlı',parlaklik:0,kontrast:1.12,doygunluk:1.14,sicaklik:.025,netlik:.13),
  _NgelXCanliFiltrePreset('Portre Pro',parlaklik:.005,kontrast:1.05,doygunluk:1.04,sicaklik:.055,netlik:.05),
  _NgelXCanliFiltrePreset('Clean HD',parlaklik:-.01,kontrast:1.08,doygunluk:1.01,sicaklik:0,netlik:.16),
  _NgelXCanliFiltrePreset('Parlak',parlaklik:.035,kontrast:1.04,doygunluk:1.06,sicaklik:.02,netlik:.06),
  _NgelXCanliFiltrePreset('Sıcak',parlaklik:-.005,kontrast:1.06,doygunluk:1.08,sicaklik:.15,netlik:.07),
  _NgelXCanliFiltrePreset('Soğuk',parlaklik:-.01,kontrast:1.07,doygunluk:1.05,sicaklik:-.11,netlik:.08),
  _NgelXCanliFiltrePreset('Kontrast+',parlaklik:-.025,kontrast:1.19,doygunluk:1.08,sicaklik:.01,netlik:.18),
  _NgelXCanliFiltrePreset('Gece',parlaklik:.07,kontrast:1.03,doygunluk:1.04,sicaklik:.035,netlik:.04),
];""","safer camera presets")

live=rep(live,
"""  if(otomatikIyilestirme){b+=.018;c*=1.035;s*=1.025;}
  if(dusukIsik){b+=.075;c*=.97;s*=1.035;w+=.025;}""",
"""  if(otomatikIyilestirme){b-=.005;c*=1.015;s*=1.012;}
  if(dusukIsik){b+=.055;c*=.96;s*=1.025;w+=.02;}""","highlight protection")

live=rep(live,
"""      if(beauty>.01)IgnorePointer(child:ColoredBox(color:Colors.white.withOpacity((beauty*.045).clamp(0.0,.055).toDouble()))),""",
"""      if(beauty>.01)IgnorePointer(child:ColoredBox(color:Colors.white.withOpacity((beauty*.024).clamp(0.0,.030).toDouble()))),""","beauty overlay")

live=rep(live,
"""  double retus = .22;
  double parlaklik = 0;
  double kontrast = 1;
  double doygunluk = 1;
  double sicaklik = 0;
  double netlik = .15;""",
"""  double retus = .18;
  double parlaklik = 0;
  double kontrast = 1;
  double doygunluk = 1;
  double sicaklik = 0;
  double netlik = .10;""","safer prepare defaults")

live=rep(live,
"""        if(retus>.01)IgnorePointer(child:ColoredBox(color:Colors.white.withOpacity((retus*.045).clamp(0.0,.055).toDouble()))),""",
"""        if(retus>.01)IgnorePointer(child:ColoredBox(color:Colors.white.withOpacity((retus*.024).clamp(0.0,.030).toDouble()))),""","preview beauty overlay")

live=rep(live,
"""            TextField(controller: baslik, maxLength: 100, style: const TextStyle(color: Colors.black87, fontWeight: FontWeight.w600), decoration: InputDecoration(prefixIcon: const Icon(Icons.edit_rounded, color: Colors.black54), hintText: 'Yayın başlığı yaz', hintStyle: const TextStyle(color: Colors.black45, fontWeight: FontWeight.w600), filled: true, fillColor: const Color(0xFFF4F6F8), border: OutlineInputBorder(borderRadius: BorderRadius.circular(18), borderSide: BorderSide.none))),""",
"""            TextField(
              controller:baslik,maxLength:100,
              onTapOutside:(_)=>FocusScope.of(context).unfocus(),
              textInputAction:TextInputAction.done,
              onSubmitted:(_)=>FocusScope.of(context).unfocus(),
              style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w600),
              decoration:InputDecoration(prefixIcon:const Icon(Icons.edit_rounded,color:Colors.black54),hintText:'Yayın başlığı yaz',hintStyle:const TextStyle(color:Colors.black45,fontWeight:FontWeight.w600),filled:true,fillColor:const Color(0xFFF4F6F8),border:OutlineInputBorder(borderRadius:BorderRadius.circular(18),borderSide:BorderSide.none)),
            ),""","keyboard dismiss")

live=rep(live,
"""        'giftPoints': 0,
        'pkActive': false,""",
"""        'giftPoints': 0,
        'pkActive': false,
        'commentsEnabled': true,
        'slowModeSeconds': 0,
        'mutedUsers': <String>[],
        'shareCount': 0,""","live moderation defaults")

live=rep(live,
"""  int maxIzleyici = 0;
  int yerelKalpSerisi = 0;""",
"""  int maxIzleyici = 0;
  int yerelKalpSerisi = 0;
  DateTime? sonYorumZamani;""","comment state")

helpers=r"""
  String _izleyiciUid(lk.RemoteParticipant p){
    final kimlik=p.identity;
    if(kimlik==widget.ownerId)return kimlik;
    final parcalar=kimlik.split('-');
    if(parcalar.length>1&&RegExp(r'^\d{10,}$').hasMatch(parcalar.last)){
      return parcalar.sublist(0,parcalar.length-1).join('-');
    }
    return kimlik;
  }

  List<lk.RemoteParticipant> _aktifIzleyiciler()=>widget.oda.remoteParticipants.values
      .where((p)=>_izleyiciUid(p)!=widget.ownerId)
      .toList(growable:false);

  Widget _baglantiRozeti(){
    final durum=widget.oda.connectionState;
    final kalite=widget.oda.localParticipant?.connectionQuality??lk.ConnectionQuality.unknown;
    String yazi='Bağlı';
    Color renk=const Color(0xFF27D17F);
    if(durum==lk.ConnectionState.reconnecting||durum==lk.ConnectionState.connecting){
      yazi='Bağlanıyor';
      renk=const Color(0xFFFFB020);
    }else if(durum==lk.ConnectionState.disconnected){
      yazi='Kesildi';
      renk=const Color(0xFFFF4D5A);
    }else if(kalite==lk.ConnectionQuality.poor){
      yazi='Zayıf';
      renk=const Color(0xFFFFB020);
    }else if(kalite==lk.ConnectionQuality.good){
      yazi='İyi';
    }else if(kalite==lk.ConnectionQuality.excellent){
      yazi='Çok iyi';
    }
    return Container(
      padding:const EdgeInsets.symmetric(horizontal:8,vertical:5),
      decoration:BoxDecoration(color:Colors.black45,borderRadius:BorderRadius.circular(12),border:Border.all(color:renk.withOpacity(.55))),
      child:Row(mainAxisSize:MainAxisSize.min,children:[
        Container(width:7,height:7,decoration:BoxDecoration(color:renk,shape:BoxShape.circle)),
        const SizedBox(width:5),
        Text(yazi,style:const TextStyle(color:Colors.white,fontSize:10.5,fontWeight:FontWeight.w800)),
      ]),
    );
  }

  Future<void> _izleyiciListesiniAc()async{
    final izleyiciler=_aktifIzleyiciler();
    await showModalBottomSheet<void>(
      context:context,backgroundColor:Colors.white,showDragHandle:true,isScrollControlled:true,
      builder:(sheetContext)=>SafeArea(child:SizedBox(
        height:MediaQuery.of(sheetContext).size.height*.62,
        child:Column(children:[
          Padding(
            padding:const EdgeInsets.fromLTRB(18,0,18,12),
            child:Row(children:[
              const Expanded(child:Text('Canlı izleyicileri',style:TextStyle(fontSize:20,fontWeight:FontWeight.w900))),
              Text('${izleyiciler.length}',style:const TextStyle(color:Colors.black54,fontWeight:FontWeight.w800)),
            ]),
          ),
          Expanded(child:izleyiciler.isEmpty
            ?const Center(child:Text('Henüz izleyici yok.',style:TextStyle(color:Colors.black54,fontWeight:FontWeight.w700)))
            :ListView.separated(
              itemCount:izleyiciler.length,
              separatorBuilder:(_,__)=>const Divider(height:1),
              itemBuilder:(_,i){
                final p=izleyiciler[i];
                final uid=_izleyiciUid(p);
                return FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(
                  future:FirebaseFirestore.instance.collection('users').doc(uid).get(),
                  builder:(_,snap){
                    final v=snap.data?.data()??<String,dynamic>{};
                    final foto=(v['photoUrl']??'').toString();
                    final ad=(v['displayName']??v['username']??p.name).toString();
                    return ListTile(
                      leading:CircleAvatar(backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person_rounded):null),
                      title:Text(ad.isEmpty?'NgelX izleyicisi':ad,style:const TextStyle(fontWeight:FontWeight.w800)),
                      subtitle:Text((v['username']??'').toString().isEmpty?'Canlı yayında':'@${v['username']}'),
                      trailing:const Icon(Icons.chevron_right_rounded),
                      onTap:uid.isEmpty?null:(){
                        Navigator.pop(sheetContext);
                        Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:uid)));
                      },
                    );
                  },
                );
              },
            ),
          ),
        ]),
      )),
    );
  }

  Widget _yayinBasligi(){
    final ben=FirebaseAuth.instance.currentUser?.uid??'';
    return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
      stream:FirebaseFirestore.instance.collection('users').doc(widget.ownerId).snapshots(),
      builder:(_,snap){
        final v=snap.data?.data()??<String,dynamic>{};
        final foto=(v['photoUrl']??'').toString();
        final ad=(v['displayName']??v['username']??widget.username).toString();
        final username=(v['username']??widget.username).toString();
        return Container(
          padding:const EdgeInsets.fromLTRB(7,6,8,6),
          decoration:BoxDecoration(color:Colors.black38,borderRadius:BorderRadius.circular(18)),
          child:Row(children:[
            InkWell(
              onTap:widget.ownerId.isEmpty?null:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:widget.ownerId))),
              child:CircleAvatar(radius:18,backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person_rounded,size:19):null),
            ),
            const SizedBox(width:8),
            Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,mainAxisSize:MainAxisSize.min,children:[
              Text(ad,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white,fontSize:12.5,fontWeight:FontWeight.w900)),
              Text('@$username • ${widget.baslik}',maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white70,fontSize:10.5,fontWeight:FontWeight.w600)),
            ])),
            if(ben.isNotEmpty&&ben!=widget.ownerId)StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
              stream:FirebaseFirestore.instance.collection('users').doc(ben).snapshots(),
              builder:(_,benSnap){
                final takipte=List<String>.from(benSnap.data?.data()?['following']??const[]).contains(widget.ownerId);
                return TextButton(
                  style:TextButton.styleFrom(foregroundColor:Colors.white,backgroundColor:takipte?Colors.white12:const Color(0xFFFF1744),padding:const EdgeInsets.symmetric(horizontal:10,vertical:6),minimumSize:Size.zero),
                  onPressed:()=>takipDurumuDegistir(widget.ownerId,takipte),
                  child:Text(takipte?'Takipte':'Takip et',style:const TextStyle(fontSize:10.5,fontWeight:FontWeight.w900)),
                );
              },
            ),
          ]),
        );
      },
    );
  }

  Future<void> _yorumYonet(String yorumId,Map<String,dynamic> y)async{
    if(!widget.yayinSahibi)return;
    final uid=(y['uid']??y['userId']??'').toString();
    final username=(y['username']??'ngelx').toString();
    final metin=(y['text']??'').toString();
    await showModalBottomSheet<void>(
      context:context,backgroundColor:const Color(0xFF15151B),showDragHandle:true,
      builder:(sheetContext)=>SafeArea(child:Column(mainAxisSize:MainAxisSize.min,children:[
        ListTile(
          leading:const Icon(Icons.push_pin_rounded,color:Color(0xFFFFC14D)),
          title:const Text('Yorumu sabitle',style:TextStyle(color:Colors.white,fontWeight:FontWeight.w800)),
          onTap:()async{
            Navigator.pop(sheetContext);
            await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).set({
              'pinnedComment':{'commentId':yorumId,'uid':uid,'username':username,'text':metin},
            },SetOptions(merge:true));
          },
        ),
        if(uid.isNotEmpty&&uid!=widget.ownerId)ListTile(
          leading:const Icon(Icons.volume_off_rounded,color:Color(0xFFFFB020)),
          title:Text('@$username kullanıcısını sustur',style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w800)),
          onTap:()async{
            Navigator.pop(sheetContext);
            await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).set({'mutedUsers':FieldValue.arrayUnion([uid])},SetOptions(merge:true));
          },
        ),
        ListTile(
          leading:const Icon(Icons.delete_outline_rounded,color:Color(0xFFFF5A67)),
          title:const Text('Yorumu sil',style:TextStyle(color:Colors.white,fontWeight:FontWeight.w800)),
          onTap:()async{
            Navigator.pop(sheetContext);
            await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).collection('comments').doc(yorumId).delete();
          },
        ),
      ])),
    );
  }

  Widget _yorumPaneli(){
    final ref=FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId);
    return Container(
      constraints:const BoxConstraints(maxWidth:340,maxHeight:220),
      padding:const EdgeInsets.all(9),
      decoration:BoxDecoration(color:Colors.black38,borderRadius:BorderRadius.circular(18)),
      child:Column(mainAxisSize:MainAxisSize.min,crossAxisAlignment:CrossAxisAlignment.start,children:[
        StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
          stream:ref.snapshots(),
          builder:(_,snap){
            final pinned=snap.data?.data()?['pinnedComment'];
            if(pinned is! Map)return const SizedBox.shrink();
            final p=Map<String,dynamic>.from(pinned);
            if((p['text']??'').toString().isEmpty)return const SizedBox.shrink();
            return Container(
              width:double.infinity,
              margin:const EdgeInsets.only(bottom:6),
              padding:const EdgeInsets.symmetric(horizontal:9,vertical:6),
              decoration:BoxDecoration(color:const Color(0x665D5FEF),borderRadius:BorderRadius.circular(12)),
              child:Row(children:[
                const Icon(Icons.push_pin_rounded,color:Colors.white70,size:15),
                const SizedBox(width:5),
                Expanded(child:Text('@${p['username']??'ngelx'}  ${p['text']??''}',maxLines:2,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white,fontSize:11.5,fontWeight:FontWeight.w800))),
                if(widget.yayinSahibi)IconButton(
                  visualDensity:VisualDensity.compact,
                  onPressed:()=>ref.set({'pinnedComment':FieldValue.delete()},SetOptions(merge:true)),
                  icon:const Icon(Icons.close_rounded,color:Colors.white70,size:16),
                ),
              ]),
            );
          },
        ),
        Flexible(child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
          stream:ref.collection('comments').orderBy('createdAt',descending:true).limit(30).snapshots(),
          builder:(_,snap){
            final yorumlar=snap.data?.docs??[];
            if(yorumlar.isEmpty)return Text(widget.baslik,style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w800));
            return ListView.builder(reverse:true,shrinkWrap:true,itemCount:yorumlar.length,itemBuilder:(_,i){
              final d=yorumlar[i],y=d.data();
              final kind=(y['kind']??'comment').toString();
              if(kind=='join'){
                return Padding(padding:const EdgeInsets.symmetric(vertical:3),child:Text('👋 ${y['username']??'ngelx'} katıldı',style:const TextStyle(color:Colors.white70,fontWeight:FontWeight.w600)));
              }
              if(kind=='gift'){
                return Padding(padding:const EdgeInsets.symmetric(vertical:4),child:Container(
                  padding:const EdgeInsets.symmetric(horizontal:9,vertical:6),
                  decoration:BoxDecoration(color:const Color(0x668D6BFF),borderRadius:BorderRadius.circular(12)),
                  child:Text('${y['giftEmoji']??'🎁'} ${y['username']??'ngelx'} • ${y['giftName']??'N-Hediye'} +${y['points']??0} N',style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w800)),
                ));
              }
              return GestureDetector(
                onLongPress:widget.yayinSahibi?()=>_yorumYonet(d.id,y):null,
                child:Padding(
                  padding:const EdgeInsets.symmetric(vertical:3),
                  child:Text('@${y['username']??'ngelx'}  ${y['text']??''}',style:const TextStyle(color:Colors.white)),
                ),
              );
            });
          },
        )),
      ]),
    );
  }

  Widget _yorumGirisAlani(){
    final uid=FirebaseAuth.instance.currentUser?.uid??'';
    return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
      stream:FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).snapshots(),
      builder:(_,snap){
        final v=snap.data?.data()??<String,dynamic>{};
        final acik=v['commentsEnabled']!=false||widget.yayinSahibi;
        final susturuldu=List<String>.from(v['mutedUsers']??const[]).contains(uid)&&!widget.yayinSahibi;
        final etkin=acik&&!susturuldu;
        final hint=susturuldu?'Yorum yapman susturuldu':acik?'Yorum yaz...':'Yorumlar kapalı';
        return TextField(
          controller:yorum,enabled:etkin,onSubmitted:etkin?(_)=>_yorumGonder():null,
          decoration:InputDecoration(
            hintText:hint,filled:true,fillColor:Colors.black54,
            suffixIcon:IconButton(onPressed:etkin?_yorumGonder:null,icon:const Icon(Icons.send_rounded)),
          ),
        );
      },
    );
  }

"""

live=rep(live,
"""  Future<void> _goruntuStudyoPaneli() async {""",
helpers+"""  Future<void> _goruntuStudyoPaneli() async {""","live helpers")

studio=r"""  Future<void> _goruntuStudyoPaneli() async {
    if(!widget.yayinSahibi)return;
    final ref=FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId);
    final belge=await ref.get();
    final veri=belge.data()??<String,dynamic>{};
    var presetAdi=(veri['filterPro']??veri['filter']??'Doğal').toString();
    var beauty=_ngelxCanliDouble(veri['beauty']??veri['retouch'],.18).clamp(0.0,1.0).toDouble();
    var bright=_ngelxCanliDouble(veri['filterBrightness'],0).clamp(-.12,.16).toDouble();
    var contrast=_ngelxCanliDouble(veri['filterContrast'],1).clamp(.82,1.30).toDouble();
    var saturation=_ngelxCanliDouble(veri['filterSaturation'],1).clamp(.82,1.35).toDouble();
    var warmth=_ngelxCanliDouble(veri['filterWarmth'],0).clamp(-.35,.35).toDouble();
    var clarity=_ngelxCanliDouble(veri['filterClarity'],.10).clamp(0.0,.60).toDouble();
    var autoEnhance=veri['autoEnhance']!=false;
    var lowLight=veri['lowLight']==true;
    var commentsEnabled=veri['commentsEnabled']!=false;
    var slowMode=(veri['slowModeSeconds'] as num?)?.toInt()??0;
    Future<void> yaz(Map<String,dynamic> yama)=>ref.set(yama,SetOptions(merge:true));
    if(!mounted)return;
    await showModalBottomSheet<void>(
      context:context,isScrollControlled:true,backgroundColor:Colors.white,showDragHandle:true,
      builder:(sheetContext)=>StatefulBuilder(builder:(context,setSheet){
        Widget ayarSlider(String ad,IconData ikon,double value,double min,double max,ValueChanged<double> change,ValueChanged<double> save,{bool percent=false}){
          return Row(children:[
            SizedBox(width:34,child:Icon(ikon,color:const Color(0xFF5F6368))),
            SizedBox(width:78,child:Text(ad,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w700,fontSize:12.5))),
            Expanded(child:Slider(value:value,min:min,max:max,onChanged:change,onChangeEnd:save)),
            SizedBox(width:46,child:Text(percent?'%${(value*100).round()}':value.toStringAsFixed(2),textAlign:TextAlign.end,style:const TextStyle(fontWeight:FontWeight.w700,color:Colors.black54,fontSize:12))),
          ]);
        }
        Future<void> sifirla()async{
          setSheet((){
            presetAdi='Doğal';beauty=.18;bright=0;contrast=1;saturation=1;warmth=0;clarity=.10;autoEnhance=true;lowLight=false;
          });
          await yaz({
            'filter':'Doğal','filterPro':'Doğal','beauty':.18,'retouch':.18,
            'filterBrightness':0.0,'filterContrast':1.0,'filterSaturation':1.0,'filterWarmth':0.0,'filterClarity':.10,
            'autoEnhance':true,'lowLight':false,
          });
        }
        return SafeArea(child:Padding(
          padding:EdgeInsets.fromLTRB(16,0,16,18+MediaQuery.of(context).viewInsets.bottom),
          child:SingleChildScrollView(child:Column(mainAxisSize:MainAxisSize.min,crossAxisAlignment:CrossAxisAlignment.start,children:[
            Row(children:[
              const Expanded(child:Text('Canlı yayın araçları',style:TextStyle(color:Colors.black,fontSize:21,fontWeight:FontWeight.w900))),
              TextButton.icon(onPressed:sifirla,icon:const Icon(Icons.restart_alt_rounded),label:const Text('Sıfırla')),
            ]),
            const Text('Görüntü ve yorum ayarlarını yayın kapanmadan değiştirebilirsin.',style:TextStyle(color:Colors.black54)),
            const SizedBox(height:12),
            const Text('Görüntü Stüdyosu',style:TextStyle(color:Colors.black87,fontSize:15,fontWeight:FontWeight.w900)),
            const SizedBox(height:8),
            Wrap(spacing:7,runSpacing:7,children:[
              for(final p in ngelxCanliProFiltreleri)ChoiceChip(
                label:Text(p.ad),selected:p.ad==presetAdi,
                onSelected:(_){setSheet(()=>presetAdi=p.ad);unawaited(yaz({'filter':p.ad,'filterPro':p.ad}));},
              ),
            ]),
            const Divider(height:24),
            ayarSlider('Güzellik',Icons.face_retouching_natural_rounded,beauty,0,1,(v)=>setSheet(()=>beauty=v),(v)=>unawaited(yaz({'beauty':v,'retouch':v})),percent:true),
            ayarSlider('Parlaklık',Icons.light_mode_rounded,bright,-.12,.16,(v)=>setSheet(()=>bright=v),(v)=>unawaited(yaz({'filterBrightness':v}))),
            ayarSlider('Kontrast',Icons.contrast_rounded,contrast,.82,1.30,(v)=>setSheet(()=>contrast=v),(v)=>unawaited(yaz({'filterContrast':v}))),
            ayarSlider('Canlılık',Icons.palette_rounded,saturation,.82,1.35,(v)=>setSheet(()=>saturation=v),(v)=>unawaited(yaz({'filterSaturation':v}))),
            ayarSlider('Sıcaklık',Icons.thermostat_rounded,warmth,-.35,.35,(v)=>setSheet(()=>warmth=v),(v)=>unawaited(yaz({'filterWarmth':v}))),
            ayarSlider('Netlik',Icons.hd_rounded,clarity,0,.60,(v)=>setSheet(()=>clarity=v),(v)=>unawaited(yaz({'filterClarity':v})),percent:true),
            SwitchListTile(
              contentPadding:EdgeInsets.zero,value:autoEnhance,
              onChanged:(v){setSheet(()=>autoEnhance=v);unawaited(yaz({'autoEnhance':v}));},
              secondary:const Icon(Icons.auto_mode_rounded,color:Color(0xFF00A6C8)),
              title:const Text('Otomatik iyileştirme',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
              subtitle:const Text('Parlak bölgeleri koruyup kontrastı dengeler.',style:TextStyle(color:Colors.black54)),
            ),
            SwitchListTile(
              contentPadding:EdgeInsets.zero,value:lowLight,
              onChanged:(v){setSheet(()=>lowLight=v);unawaited(yaz({'lowLight':v}));},
              secondary:const Icon(Icons.nightlight_round,color:Color(0xFF5D5FEF)),
              title:const Text('Düşük ışık',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
            ),
            const Divider(height:28),
            const Text('Yorum ve moderasyon',style:TextStyle(color:Colors.black87,fontSize:15,fontWeight:FontWeight.w900)),
            SwitchListTile(
              contentPadding:EdgeInsets.zero,value:commentsEnabled,
              onChanged:(v){setSheet(()=>commentsEnabled=v);unawaited(yaz({'commentsEnabled':v}));},
              secondary:Icon(commentsEnabled?Icons.mode_comment_rounded:Icons.comments_disabled_rounded,color:const Color(0xFF5D5FEF)),
              title:const Text('Yorumlara izin ver',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
            ),
            const Text('Yavaş mod',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
            const SizedBox(height:7),
            Wrap(spacing:7,children:[
              for(final s in const [0,5,10,30])ChoiceChip(
                label:Text(s==0?'Kapalı':'$s sn'),
                selected:slowMode==s,
                onSelected:(_){setSheet(()=>slowMode=s);unawaited(yaz({'slowModeSeconds':s}));},
              ),
            ]),
            const SizedBox(height:10),
            const Text('İpucu: Bir yoruma uzun basarak sabitleyebilir, silebilir veya kullanıcıyı susturabilirsin.',style:TextStyle(color:Colors.black54,fontSize:12)),
          ])),
        ));
      }),
    );
  }

"""

live=rep_between(live,"  Future<void> _goruntuStudyoPaneli() async {","  Future<void> _paylas() async {",studio,"studio and moderation")

share=r"""  Future<void> _canliKisiyeGonder(User ben,String hedefUid)async{
    final ids=<String>[ben.uid,hedefUid]..sort();
    final chatId=ids.join('_');
    final chat=FirebaseFirestore.instance.collection('chats').doc(chatId);
    final metin='🔴 CANLI • ${widget.baslik}\n@${widget.username}\nNgelX canlı yayınına katıl\nngelx://live/${widget.belgeId}';
    await chat.set({'members':ids,'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
    await chat.collection('messages').add({
      'senderId':ben.uid,
      'text':metin,
      'type':'text',
      'liveShare':true,
      'liveId':widget.belgeId,
      'liveTitle':widget.baslik,
      'liveOwnerId':widget.ownerId,
      'createdAt':FieldValue.serverTimestamp(),
    });
    await chat.set({
      'lastMessage':'🔴 Canlı yayın paylaşıldı',
      'updatedAt':FieldValue.serverTimestamp(),
      'unread_$hedefUid':FieldValue.increment(1),
    },SetOptions(merge:true));
    await uygulamaBildirimiGonder(
      toUid:hedefUid,fromUid:ben.uid,tur:'live',
      metin:'Sana bir canlı yayın gönderdi',
      belgeId:widget.belgeId,
      hedefTuru:'live',
      hedefBaslik:widget.baslik,
      olayTuru:'live_share',
      onizleme:widget.baslik,
      dedupeKey:'live_share_${widget.belgeId}_${ben.uid}_$hedefUid',
    );
  }

  Future<void> _baglantiKopyala()async{
    await Clipboard.setData(ClipboardData(text:'NgelX canlı yayın • ${widget.baslik}\nngelx://live/${widget.belgeId}'));
    if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(
      content:const Text('Bağlantı kopyalandı.',style:TextStyle(fontWeight:FontWeight.w700)),
      behavior:SnackBarBehavior.floating,
      width:230,
      duration:const Duration(milliseconds:1100),
      shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(14)),
    ));
  }

  Future<void> _paylas() async {
    if(await misafirEngeli(context))return;
    final ben=FirebaseAuth.instance.currentUser;
    if(ben==null)return;
    final benim=await FirebaseFirestore.instance.collection('users').doc(ben.uid).get();
    final engellenen=Set<String>.from(List<dynamic>.from(benim.data()?['blocked']??const[]));
    final yakin=<String>{
      ...List<String>.from(benim.data()?['friends']??const[]),
      ...List<String>.from(benim.data()?['following']??const[]),
    };
    if(!mounted)return;
    String sorgu='';
    final secilen=<String>{};
    bool gonderiliyor=false;
    await showModalBottomSheet<void>(
      context:context,isScrollControlled:true,backgroundColor:Colors.white,
      shape:const RoundedRectangleBorder(borderRadius:BorderRadius.vertical(top:Radius.circular(28))),
      builder:(sheetContext)=>StatefulBuilder(builder:(sheetContext,setSheet)=>SafeArea(child:SizedBox(
        height:MediaQuery.of(sheetContext).size.height*.76,
        child:Column(children:[
          Container(width:42,height:4,margin:const EdgeInsets.all(12),decoration:BoxDecoration(color:Colors.black26,borderRadius:BorderRadius.circular(9))),
          const Text('Canlı yayını NgelX’te paylaş',style:TextStyle(color:Colors.black,fontSize:20,fontWeight:FontWeight.w900)),
          const SizedBox(height:4),
          const Text('Arkadaş veya kullanıcı seç • aynı anda birden fazla kişiye gönderebilirsin.',style:TextStyle(color:Colors.black54,fontSize:12)),
          Padding(
            padding:const EdgeInsets.all(14),
            child:TextField(
              autofocus:false,onChanged:(v)=>setSheet(()=>sorgu=v.trim().toLowerCase()),
              decoration:InputDecoration(hintText:'NgelX’te kişi ara',prefixIcon:const Icon(Icons.search_rounded),filled:true,fillColor:const Color(0xFFF3F4F6),border:OutlineInputBorder(borderRadius:BorderRadius.circular(22),borderSide:BorderSide.none)),
            ),
          ),
          Expanded(child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
            stream:FirebaseFirestore.instance.collection('users').limit(100).snapshots(),
            builder:(_,snap){
              if(snap.connectionState==ConnectionState.waiting)return const Center(child:CircularProgressIndicator());
              final docs=(snap.data?.docs??[]).where((d){
                if(d.id==ben.uid||engellenen.contains(d.id))return false;
                final v=d.data();
                if(v['deactivated']==true)return false;
                if(List<String>.from(v['blocked']??const[]).contains(ben.uid))return false;
                final ad='${v['displayName']??''} ${v['username']??''}'.toLowerCase();
                return sorgu.isEmpty||ad.contains(sorgu);
              }).toList()
                ..sort((a,b){
                  final ap=yakin.contains(a.id)?0:1,bp=yakin.contains(b.id)?0:1;
                  if(ap!=bp)return ap.compareTo(bp);
                  final an=(a.data()['displayName']??a.data()['username']??'').toString();
                  final bn=(b.data()['displayName']??b.data()['username']??'').toString();
                  return an.toLowerCase().compareTo(bn.toLowerCase());
                });
              if(docs.isEmpty)return const Center(child:Text('Kullanıcı bulunamadı.',style:TextStyle(color:Colors.black54)));
              return ListView.builder(itemCount:docs.length,itemBuilder:(_,i){
                final d=docs[i],v=d.data();
                final foto=(v['photoUrl']??'').toString();
                final ad=(v['displayName']??v['username']??'NgelX kullanıcısı').toString();
                final secili=secilen.contains(d.id);
                return ListTile(
                  leading:CircleAvatar(backgroundImage:foto.isEmpty?null:NgelXAgImageProvider(foto),child:foto.isEmpty?const Icon(Icons.person_rounded):null),
                  title:Text(ad,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
                  subtitle:Text('@${v['username']??'ngelx'}',style:const TextStyle(color:Colors.black54)),
                  trailing:Checkbox(value:secili,onChanged:gonderiliyor?null:(_)=>setSheet((){secili?secilen.remove(d.id):secilen.add(d.id);})),
                  onTap:gonderiliyor?null:()=>setSheet((){secili?secilen.remove(d.id):secilen.add(d.id);}),
                );
              });
            },
          )),
          Padding(
            padding:const EdgeInsets.fromLTRB(14,8,14,12),
            child:Row(children:[
              OutlinedButton.icon(
                onPressed:gonderiliyor?null:()async{Navigator.pop(sheetContext);await _baglantiKopyala();},
                icon:const Icon(Icons.link_rounded),label:const Text('Kopyala'),
              ),
              const SizedBox(width:10),
              Expanded(child:FilledButton.icon(
                style:FilledButton.styleFrom(minimumSize:const Size.fromHeight(52),backgroundColor:const Color(0xFFFF1744)),
                onPressed:secilen.isEmpty||gonderiliyor?null:()async{
                  setSheet(()=>gonderiliyor=true);
                  try{
                    await Future.wait(secilen.map((uid)=>_canliKisiyeGonder(ben,uid)));
                    await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).set({'shareCount':FieldValue.increment(secilen.length)},SetOptions(merge:true));
                    if(sheetContext.mounted)Navigator.pop(sheetContext);
                    if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                      content:Text('Canlı yayın ${secilen.length} kişiye gönderildi.',style:const TextStyle(fontWeight:FontWeight.w700)),
                      behavior:SnackBarBehavior.floating,width:280,duration:const Duration(milliseconds:1300),
                      shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(14)),
                    ));
                  }catch(_){
                    if(sheetContext.mounted)setSheet(()=>gonderiliyor=false);
                    if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Canlı yayın gönderilemedi.')));
                  }
                },
                icon:gonderiliyor?const SizedBox(width:18,height:18,child:CircularProgressIndicator(strokeWidth:2,color:Colors.white)):const Icon(Icons.send_rounded),
                label:Text(secilen.isEmpty?'Kişi seç':'${secilen.length} kişiye gönder',style:const TextStyle(fontWeight:FontWeight.w900)),
              )),
            ]),
          ),
        ]),
      ))),
    );
  }

"""

live=rep_between(live,"  Future<void> _paylas() async {","  Future<void> _hediyeGonder(",share+"  Future<void> _hediyeGonder(","share flow")

yorum=r"""  Future<void> _yorumGonder() async {
    final metin=yorum.text.trim();
    final user=FirebaseAuth.instance.currentUser;
    if(metin.isEmpty||user==null)return;
    final ref=FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId);
    final canli=await ref.get();
    final v=canli.data()??<String,dynamic>{};
    if(!widget.yayinSahibi&&v['commentsEnabled']==false){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Yayıncı yorumları kapattı.')));
      return;
    }
    if(!widget.yayinSahibi&&List<String>.from(v['mutedUsers']??const[]).contains(user.uid)){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Bu yayında yorum yapman susturuldu.')));
      return;
    }
    final yavas=(v['slowModeSeconds'] as num?)?.toInt()??0;
    if(!widget.yayinSahibi&&yavas>0&&sonYorumZamani!=null){
      final kalan=yavas-DateTime.now().difference(sonYorumZamani!).inSeconds;
      if(kalan>0){
        if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text('Yavaş mod açık. $kalan saniye bekle.')));
        return;
      }
    }
    yorum.clear();
    final profil=await FirebaseFirestore.instance.collection('users').doc(user.uid).get();
    await ref.collection('comments').add({
      'uid':user.uid,'userId':user.uid,
      'username':(profil.data()?['username']??'ngelx').toString(),
      'text':metin,'kind':'comment','createdAt':FieldValue.serverTimestamp(),
    });
    sonYorumZamani=DateTime.now();
  }

"""

live=rep_between(
    live,
    "  Future<void> _yorumGonder() async {",
    """  @override
  void dispose()""",
    yorum+"""  @override
  void dispose()""",
    "comment moderation send",
)

live=rep(live,
"""          Positioned.fill(child: DecoratedBox(decoration: BoxDecoration(gradient: LinearGradient(begin: Alignment.topCenter, end: Alignment.bottomCenter, colors: [Colors.black54, Colors.transparent, Colors.black.withOpacity(.8)])))),""",
"""          Positioned.fill(child:DecoratedBox(decoration:BoxDecoration(gradient:LinearGradient(begin:Alignment.topCenter,end:Alignment.bottomCenter,colors:[Colors.black54,Colors.transparent,Colors.black.withOpacity(.8)])))),
          if(widget.oda.connectionState==lk.ConnectionState.reconnecting)
            Positioned(
              top:74,left:70,right:70,
              child:SafeArea(child:Container(
                padding:const EdgeInsets.symmetric(horizontal:12,vertical:8),
                decoration:BoxDecoration(color:const Color(0xDD1A1A1A),borderRadius:BorderRadius.circular(14)),
                child:const Row(mainAxisAlignment:MainAxisAlignment.center,children:[
                  SizedBox(width:15,height:15,child:CircularProgressIndicator(strokeWidth:2,color:Color(0xFFFFB020))),
                  SizedBox(width:8),
                  Text('Bağlantı yeniden kuruluyor…',style:TextStyle(color:Colors.white,fontSize:11,fontWeight:FontWeight.w800)),
                ]),
              )),
            ),""","reconnect overlay")

live=rep(live,
"""                Container(padding: const EdgeInsets.symmetric(horizontal: 11, vertical: 8), decoration: BoxDecoration(color: Colors.black45, borderRadius: BorderRadius.circular(14)), child: Text('👁 ${widget.oda.remoteParticipants.length}')),
                const Spacer(),""",
"""                InkWell(
                  onTap:_izleyiciListesiniAc,
                  borderRadius:BorderRadius.circular(14),
                  child:Container(padding:const EdgeInsets.symmetric(horizontal:11,vertical:8),decoration:BoxDecoration(color:Colors.black45,borderRadius:BorderRadius.circular(14)),child:Text('👁 ${_aktifIzleyiciler().length}')),
                ),
                const Spacer(),""","viewer count button")

live=rep(live,
"""                IconButton(onPressed: () async { if (await _geri() && mounted) Navigator.pop(context); }, icon: const Icon(Icons.close_rounded, size: 31)),
              ]),
              const Spacer(),""",
"""                IconButton(onPressed:()async{if(await _geri()&&mounted)Navigator.pop(context);},icon:const Icon(Icons.close_rounded,size:31)),
              ]),
              const SizedBox(height:7),
              Row(children:[
                Expanded(child:_yayinBasligi()),
                const SizedBox(width:7),
                _baglantiRozeti(),
              ]),
              const Spacer(),""","owner header and connection")

live=rep_between(live,
"""              Align(alignment: Alignment.centerLeft, child: Container(""",
"""              const SizedBox(height: 10),""",
"""              Align(alignment:Alignment.centerLeft,child:_yorumPaneli()),
""","comment panel")

live=rep(live,
"""                Expanded(child: TextField(controller: yorum, onSubmitted: (_) => _yorumGonder(), decoration: InputDecoration(hintText: 'Yorum yaz...', filled: true, fillColor: Colors.black54, suffixIcon: IconButton(onPressed: _yorumGonder, icon: const Icon(Icons.send_rounded))))),""",
"""                Expanded(child:_yorumGirisAlani()),""","comment input")

LIVE.write_text(live,encoding="utf-8")
MAIN.write_text(main,encoding="utf-8")
PUB.write_text(pub,encoding="utf-8")
print("Build 327 live share, moderation, viewers, profile header and reconnect package applied.")
