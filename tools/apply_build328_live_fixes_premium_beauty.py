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
        raise SystemExit("Build 328 patch failed: marker not found: "+label)
    return text.replace(old,new,1)

pub=rep(pub,"version: 1.0.108+327","version: 1.0.109+328","version")
main=main.replace("defaultValue: '1.0.108'","defaultValue: '1.0.109'")
main=main.replace("defaultValue: '327'","defaultValue: '328'")

live=rep(live,
"""double _ngelxCanliDouble(dynamic value,double fallback)=>value is num?value.toDouble():fallback;

_NgelXCanliFiltrePreset ngelxCanliPresetBul(String? ad){""",
"""double _ngelxCanliDouble(dynamic value,double fallback)=>value is num?value.toDouble():fallback;

bool ngelxCanliKaydiTaze(Map<String,dynamic> veri){
  if(veri['active']!=true)return false;
  final simdi=DateTime.now();
  final hb=veri['lastHeartbeatAt'];
  if(hb is Timestamp)return simdi.difference(hb.toDate()).inSeconds<=85;
  final baslangic=veri['startedAt'];
  if(baslangic is Timestamp)return simdi.difference(baslangic.toDate()).inMinutes<=3;
  return false;
}

_NgelXCanliFiltrePreset ngelxCanliPresetBul(String? ad){""","fresh live helper")

live=rep(live,
"""List<double> ngelxCanliRenkMatrisi({
  required _NgelXCanliFiltrePreset preset,
  double parlaklik=0,double kontrast=1,double doygunluk=1,double sicaklik=0,double netlik=0,
  bool otomatikIyilestirme=true,bool dusukIsik=false,
}){""",
"""List<double> ngelxCanliRenkMatrisi({
  required _NgelXCanliFiltrePreset preset,
  double parlaklik=0,double kontrast=1,double doygunluk=1,double sicaklik=0,double netlik=0,
  double ciltTonu=.08,double highlightKoruma=.65,double golgeAcma=.10,double guzellik=.18,
  bool otomatikIyilestirme=true,bool dusukIsik=false,
}){""","matrix params")

live=rep(live,
"""  var w=(preset.sicaklik+sicaklik).clamp(-.55,.55).toDouble();
  final n=(preset.netlik+netlik).clamp(0.0,1.0).toDouble();
  if(otomatikIyilestirme){b-=.005;c*=1.015;s*=1.012;}
  if(dusukIsik){b+=.055;c*=.96;s*=1.025;w+=.02;}
  c=(c*(1+n*.10)).clamp(.75,1.65).toDouble();
  s=(s*(1+n*.04)).clamp(.65,1.75).toDouble();""",
"""  var w=(preset.sicaklik+sicaklik).clamp(-.55,.55).toDouble();
  final n=(preset.netlik+netlik).clamp(0.0,1.0).toDouble();
  final hp=highlightKoruma.clamp(0.0,1.0).toDouble();
  final sh=golgeAcma.clamp(0.0,1.0).toDouble();
  final skin=ciltTonu.clamp(-1.0,1.0).toDouble();
  final beauty=guzellik.clamp(0.0,1.0).toDouble();
  if(otomatikIyilestirme){b-=.010;c*=1.008;s*=1.010;}
  if(dusukIsik){b+=.045;c*=.965;s*=1.020;w+=.018;}
  b-=hp*.022;
  c*=1-(hp*.055);
  b+=sh*.030;
  c*=1-(sh*.018);
  w+=skin*.085;
  s*=1+(skin.abs()*.012);
  c*=1-(beauty*.028);
  s*=1-(beauty*.010);
  b+=beauty*.004;
  c=(c*(1+n*.085)).clamp(.75,1.60).toDouble();
  s=(s*(1+n*.035)).clamp(.65,1.70).toDouble();""","matrix premium logic")

live=rep(live,
"""    netlik:_ngelxCanliDouble(veri['filterClarity'],.12),
    otomatikIyilestirme:veri['autoEnhance']!=false,
    dusukIsik:veri['lowLight']==true,
  );""",
"""    netlik:_ngelxCanliDouble(veri['filterClarity'],.10),
    ciltTonu:_ngelxCanliDouble(veri['skinTone'],.08),
    highlightKoruma:_ngelxCanliDouble(veri['highlightProtect'],.65),
    golgeAcma:_ngelxCanliDouble(veri['shadowLift'],.10),
    guzellik:beauty,
    otomatikIyilestirme:veri['autoEnhance']!=false,
    dusukIsik:veri['lowLight']==true,
  );""","effect premium params")

live=rep(live,
"""      if(beauty>.01)IgnorePointer(child:ColoredBox(color:Colors.white.withOpacity((beauty*.024).clamp(0.0,.030).toDouble()))),""",
"""      if(beauty>.01)IgnorePointer(child:ColoredBox(color:const Color(0xFFFFE7DE).withOpacity((beauty*.012).clamp(0.0,.014).toDouble()))),""","effect beauty tint")

live=rep(live,
"""  double netlik = .10;
  bool otomatikIyilestirme = true;""",
"""  double netlik = .10;
  double ciltTonu = .08;
  double highlightKoruma = .65;
  double golgeAcma = .10;
  bool otomatikIyilestirme = true;""","prepare beauty state")

live=rep(live,
"""      try { await yeni.setFocusMode(FocusMode.auto); } catch (_) {}
      try { await yeni.setExposureMode(ExposureMode.auto); } catch (_) {}
      if (!arkaKamera) flashAcik = false;""",
"""      try { await yeni.setFocusMode(FocusMode.auto); } catch (_) {}
      try { await yeni.setExposureMode(ExposureMode.auto); } catch (_) {}
      try {
        final minExp=await yeni.getMinExposureOffset();
        final maxExp=await yeni.getMaxExposureOffset();
        await yeni.setExposureOffset((-0.35).clamp(minExp,maxExp).toDouble());
      } catch (_) {}
      if (!arkaKamera) flashAcik = false;""","preview exposure guard")

live=rep(live,
"""      preset:filtre,parlaklik:parlaklik,kontrast:kontrast,doygunluk:doygunluk,sicaklik:sicaklik,netlik:netlik,
      otomatikIyilestirme:otomatikIyilestirme,dusukIsik:dusukIsik,
    );""",
"""      preset:filtre,parlaklik:parlaklik,kontrast:kontrast,doygunluk:doygunluk,sicaklik:sicaklik,netlik:netlik,
      ciltTonu:ciltTonu,highlightKoruma:highlightKoruma,golgeAcma:golgeAcma,guzellik:retus,
      otomatikIyilestirme:otomatikIyilestirme,dusukIsik:dusukIsik,
    );""","preview premium params")

live=rep(live,
"""        if(retus>.01)IgnorePointer(child:ColoredBox(color:Colors.white.withOpacity((retus*.024).clamp(0.0,.030).toDouble()))),""",
"""        if(retus>.01)IgnorePointer(child:ColoredBox(color:const Color(0xFFFFE7DE).withOpacity((retus*.012).clamp(0.0,.014).toDouble()))),""","preview beauty tint")

live=rep(live,
"""      final profil = await FirebaseFirestore.instance.collection('users').doc(user.uid).get();
      final ad = (profil.data()?['username'] ?? user.displayName ?? 'ngelx').toString();""",
"""      final profil = await FirebaseFirestore.instance.collection('users').doc(user.uid).get();
      final eskiCanli=(profil.data()?['currentLiveId']??'').toString();
      if(eskiCanli.isNotEmpty){
        try{
          await FirebaseFirestore.instance.collection('live_streams').doc(eskiCanli).set({
            'active':false,'endedAt':FieldValue.serverTimestamp(),'endReason':'replaced_by_new_live',
          },SetOptions(merge:true));
        }catch(_){}
      }
      final ad = (profil.data()?['username'] ?? user.displayName ?? 'ngelx').toString();""","close previous live")

live=rep(live,
"""        'startedAt': FieldValue.serverTimestamp(),
        'cameraPosition': arkaKamera ? 'back' : 'front',""",
"""        'startedAt': FieldValue.serverTimestamp(),
        'lastHeartbeatAt': FieldValue.serverTimestamp(),
        'cameraPosition': arkaKamera ? 'back' : 'front',""","initial heartbeat")

live=rep(live,
"""        'filterClarity': netlik,
        'autoEnhance': otomatikIyilestirme,""",
"""        'filterClarity': netlik,
        'skinTone': ciltTonu,
        'highlightProtect': highlightKoruma,
        'shadowLift': golgeAcma,
        'autoEnhance': otomatikIyilestirme,""","store premium beauty")

live=rep(live,
"""                _proSlider('Netlik',Icons.hd_rounded,netlik,0,.60,(v)=>setState(()=>netlik=v),yuzde:true),
                SwitchListTile(""",
"""                _proSlider('Netlik',Icons.hd_rounded,netlik,0,.60,(v)=>setState(()=>netlik=v),yuzde:true),
                _proSlider('Cilt tonu',Icons.face_rounded,ciltTonu,-.40,.40,(v)=>setState(()=>ciltTonu=v)),
                _proSlider('Parlak alan',Icons.wb_sunny_outlined,highlightKoruma,0,1,(v)=>setState(()=>highlightKoruma=v),yuzde:true),
                _proSlider('Gölgeler',Icons.brightness_4_rounded,golgeAcma,0,1,(v)=>setState(()=>golgeAcma=v),yuzde:true),
                SwitchListTile(""","prepare premium sliders")

live=rep(live,
"""                  title:const Text('Otomatik görüntü iyileştirme',style:TextStyle(fontWeight:FontWeight.w800)),
                  subtitle:const Text('Işık, kontrast ve canlılığı dengeler.'),""",
"""                  title:const Text('Otomatik görüntü iyileştirme',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
                  subtitle:const Text('Işık, kontrast ve canlılığı dengeler.',style:TextStyle(color:Colors.black54)),""","prepare auto text color")

live=rep(live,
"""                  title:const Text('Düşük ışık desteği',style:TextStyle(fontWeight:FontWeight.w800)),
                  subtitle:const Text('Karanlık ortamda yüzü ve gölgeleri daha görünür tutar.'),""",
"""                  title:const Text('Düşük ışık desteği',style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
                  subtitle:const Text('Karanlık ortamda yüzü ve gölgeleri daha görünür tutar.',style:TextStyle(color:Colors.black54)),""","prepare lowlight text color")

live=rep(live,
"""                title: const Text('3-2-1', style: TextStyle(fontWeight: FontWeight.w700)),
                subtitle: const Text('Başlangıç'),""",
"""                title: const Text('3-2-1', style: TextStyle(color:Colors.black87,fontWeight: FontWeight.w700)),
                subtitle: const Text('Başlangıç',style:TextStyle(color:Colors.black54)),""","countdown colors")

live=rep(live,
"""            SwitchListTile(contentPadding: EdgeInsets.zero, value: kamera, onChanged: baglaniyor ? null : _kamerayiAcKapat, secondary: Icon(kamera ? Icons.videocam_rounded : Icons.videocam_off_rounded, color: const Color(0xFFE91E63)), title: const Text('Kamera', style: TextStyle(color: Colors.black87, fontWeight: FontWeight.w700)), subtitle: const Text('Seçimler yayını otomatik başlatmaz.')),""",
"""            SwitchListTile(contentPadding: EdgeInsets.zero, value: kamera, onChanged: baglaniyor ? null : _kamerayiAcKapat, secondary: Icon(kamera ? Icons.videocam_rounded : Icons.videocam_off_rounded, color: const Color(0xFFE91E63)), title: const Text('Kamera', style: TextStyle(color: Colors.black87, fontWeight: FontWeight.w700)), subtitle: const Text('Seçimler yayını otomatik başlatmaz.',style:TextStyle(color:Colors.black54))),""","camera subtitle color")

live=rep(live,
"""            ListTile(contentPadding: EdgeInsets.zero, leading: const Icon(Icons.public_rounded, color: Color(0xFFE91E63)), title: Text(gizlilik, style: const TextStyle(color: Colors.black87, fontWeight: FontWeight.w700)), subtitle: Text('$kategori • ${fps} FPS • $kalite')),""",
"""            ListTile(contentPadding: EdgeInsets.zero, leading: const Icon(Icons.public_rounded, color: Color(0xFFE91E63)), title: Text(gizlilik, style: const TextStyle(color: Colors.black87, fontWeight: FontWeight.w700)), subtitle: Text('$kategori • ${fps} FPS • $kalite',style:const TextStyle(color:Colors.black54))),""","summary subtitle color")

live=rep(live,
"""      SizedBox(width:78,child:Text(etiket,style:const TextStyle(fontWeight:FontWeight.w700,fontSize:12.5))),""",
"""      SizedBox(width:78,child:Text(etiket,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w700,fontSize:12.5))),""","slider label color")

old_select="""  Widget _canliSecimKutusu(String etiket, String deger, List<String> secenekler, FutureOr<void> Function(String) degisti) {
    return InputDecorator(
      decoration: InputDecoration(labelText: etiket, filled: true, fillColor: const Color(0xFFF4F6F8), border: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none)),
      child: DropdownButtonHideUnderline(child: DropdownButton<String>(
        value: deger,
        isDense: true,
        isExpanded: true,
        style: const TextStyle(color: Colors.black87, fontWeight: FontWeight.w700),
        items: secenekler.map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
        onChanged: baglaniyor ? null : (v) { if (v != null) unawaited(Future.sync(() => degisti(v))); },
      )),
    );
  }"""
new_select="""  Widget _canliSecimKutusu(String etiket, String deger, List<String> secenekler, FutureOr<void> Function(String) degisti) {
    return Theme(
      data:ThemeData.light(),
      child:InputDecorator(
        decoration:InputDecoration(
          labelText:etiket,
          labelStyle:const TextStyle(color:Color(0xFF5F6368),fontWeight:FontWeight.w700),
          floatingLabelStyle:const TextStyle(color:Color(0xFF5F6368),fontWeight:FontWeight.w800),
          filled:true,fillColor:const Color(0xFFF2F3F5),
          border:OutlineInputBorder(borderRadius:BorderRadius.circular(16),borderSide:BorderSide.none),
        ),
        child:DropdownButtonHideUnderline(child:DropdownButton<String>(
          value:deger,isDense:true,isExpanded:true,dropdownColor:Colors.white,
          iconEnabledColor:const Color(0xFF5F6368),
          style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w800),
          items:secenekler.map((e)=>DropdownMenuItem<String>(
            value:e,child:Text(e,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w800)),
          )).toList(),
          onChanged:baglaniyor?null:(v){if(v!=null)unawaited(Future.sync(()=>degisti(v)));},
        )),
      ),
    );
  }"""
live=rep(live,old_select,new_select,"readable dropdown")

live=rep(live,"""  Timer? sayac;
  int saniye = 0;""","""  Timer? sayac;
  Timer? heartbeat;
  int saniye = 0;""","heartbeat field")

live=rep(live,
"""    widget.oda.addListener(_yenile);
    if (!widget.yayinSahibi) unawaited(_katildimKaydet());
    sayac = Timer.periodic(const Duration(seconds: 1), (_) {""",
"""    widget.oda.addListener(_yenile);
    if (!widget.yayinSahibi) {
      unawaited(_katildimKaydet());
    } else {
      unawaited(_heartbeatYaz());
      heartbeat=Timer.periodic(const Duration(seconds:12),(_)=>unawaited(_heartbeatYaz()));
    }
    sayac = Timer.periodic(const Duration(seconds: 1), (_) {""","heartbeat init")

live=rep(live,
"""  void _yenile() {
    if (mounted) setState(() {});
  }

  lk.VideoTrack? _goruntu() {""",
"""  void _yenile() {
    if (mounted) setState(() {});
  }

  Future<void> _heartbeatYaz()async{
    if(!widget.yayinSahibi||kapatildi)return;
    try{
      await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).set({
        'active':true,'lastHeartbeatAt':FieldValue.serverTimestamp(),'viewerCount':_aktifIzleyiciler().length,
      },SetOptions(merge:true));
    }catch(_){}
  }

  lk.VideoTrack? _goruntu() {""","heartbeat function")

live=rep(live,
"""  Future<void> _bitir({bool geriDon = true}) async {
    if (kapatildi) return;
    kapatildi = true;""",
"""  Future<void> _bitir({bool geriDon = true}) async {
    if (kapatildi) return;
    kapatildi = true;
    heartbeat?.cancel();
    heartbeat=null;""","heartbeat stop")

live=rep(live,"""  void dispose() {
    sayac?.cancel();
    yorum.dispose();""","""  void dispose() {
    sayac?.cancel();
    heartbeat?.cancel();
    yorum.dispose();""","heartbeat dispose")

live=rep(live,
"""            child:track==null
              ?const Center(child:CircularProgressIndicator())
              :StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(""",
"""            child:track==null
              ?Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
                const CircularProgressIndicator(color:Colors.white),
                const SizedBox(height:12),
                Text(saniye<8?'Yayın görüntüsü hazırlanıyor…':'Yayın görüntüsü alınamadı. Tekrar bağlanmayı deneyebilirsin.',textAlign:TextAlign.center,style:const TextStyle(color:Colors.white70,fontWeight:FontWeight.w700)),
              ]))
              :StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(""","track loading message")

live=rep(live,
"""    var clarity=_ngelxCanliDouble(veri['filterClarity'],.10).clamp(0.0,.60).toDouble();
    var autoEnhance=veri['autoEnhance']!=false;""",
"""    var clarity=_ngelxCanliDouble(veri['filterClarity'],.10).clamp(0.0,.60).toDouble();
    var skinTone=_ngelxCanliDouble(veri['skinTone'],.08).clamp(-.40,.40).toDouble();
    var highlightProtect=_ngelxCanliDouble(veri['highlightProtect'],.65).clamp(0.0,1.0).toDouble();
    var shadowLift=_ngelxCanliDouble(veri['shadowLift'],.10).clamp(0.0,1.0).toDouble();
    var autoEnhance=veri['autoEnhance']!=false;""","live studio premium state")

live=rep(live,
"""            presetAdi='Doğal';beauty=.18;bright=0;contrast=1;saturation=1;warmth=0;clarity=.10;autoEnhance=true;lowLight=false;""",
"""            presetAdi='Doğal';beauty=.18;bright=0;contrast=1;saturation=1;warmth=0;clarity=.10;skinTone=.08;highlightProtect=.65;shadowLift=.10;autoEnhance=true;lowLight=false;""","live studio reset state")

live=rep(live,
"""            'filterBrightness':0.0,'filterContrast':1.0,'filterSaturation':1.0,'filterWarmth':0.0,'filterClarity':.10,
            'autoEnhance':true,'lowLight':false,""",
"""            'filterBrightness':0.0,'filterContrast':1.0,'filterSaturation':1.0,'filterWarmth':0.0,'filterClarity':.10,
            'skinTone':.08,'highlightProtect':.65,'shadowLift':.10,
            'autoEnhance':true,'lowLight':false,""","live studio reset payload")

live=rep(live,
"""            ayarSlider('Netlik',Icons.hd_rounded,clarity,0,.60,(v)=>setSheet(()=>clarity=v),(v)=>unawaited(yaz({'filterClarity':v})),percent:true),
            SwitchListTile(""",
"""            ayarSlider('Netlik',Icons.hd_rounded,clarity,0,.60,(v)=>setSheet(()=>clarity=v),(v)=>unawaited(yaz({'filterClarity':v})),percent:true),
            ayarSlider('Cilt tonu',Icons.face_rounded,skinTone,-.40,.40,(v)=>setSheet(()=>skinTone=v),(v)=>unawaited(yaz({'skinTone':v}))),
            ayarSlider('Parlak alan',Icons.wb_sunny_outlined,highlightProtect,0,1,(v)=>setSheet(()=>highlightProtect=v),(v)=>unawaited(yaz({'highlightProtect':v})),percent:true),
            ayarSlider('Gölgeler',Icons.brightness_4_rounded,shadowLift,0,1,(v)=>setSheet(()=>shadowLift=v),(v)=>unawaited(yaz({'shadowLift':v})),percent:true),
            SwitchListTile(""","live studio premium sliders")

old_send="""  Future<void> _canliKisiyeGonder(User ben,String hedefUid)async{
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
  }"""
new_send="""  Future<void> _canliKisiyeGonder(User ben,String hedefUid)async{
    final ids=<String>[ben.uid,hedefUid]..sort();
    final chatId=ids.join('_');
    final chat=FirebaseFirestore.instance.collection('chats').doc(chatId);
    final metin='🔴 CANLI • ${widget.baslik}\n@${widget.username}\nYayına katıl: ngelx://live/${widget.belgeId}';
    await chat.set({'members':ids,'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
    await chat.collection('messages').add({
      'senderId':ben.uid,'text':metin,'type':'text','liveShare':true,
      'liveId':widget.belgeId,'liveTitle':widget.baslik,'liveOwnerId':widget.ownerId,
      'liveUsername':widget.username,'createdAt':FieldValue.serverTimestamp(),
    });
    try{
      await chat.set({
        'lastMessage':'🔴 ${widget.baslik}','updatedAt':FieldValue.serverTimestamp(),
        'unread_$hedefUid':FieldValue.increment(1),
      },SetOptions(merge:true));
    }catch(_){}
    try{
      await uygulamaBildirimiGonder(
        toUid:hedefUid,fromUid:ben.uid,tur:'message',metin:'Sana bir canlı yayın gönderdi',
        belgeId:widget.belgeId,hedefTuru:'live',hedefBaslik:widget.baslik,
        olayTuru:'live_share',onizleme:widget.baslik,
      );
    }catch(_){}
  }"""
live=rep(live,old_send,new_send,"robust live send")

live=rep(live,
"""          const SizedBox(height:4),
          const Text('Arkadaş veya kullanıcı seç • aynı anda birden fazla kişiye gönderebilirsin.',style:TextStyle(color:Colors.black54,fontSize:12)),
          Padding(
            padding:const EdgeInsets.all(14),
            child:TextField(
              autofocus:false,onChanged:(v)=>setSheet(()=>sorgu=v.trim().toLowerCase()),
              decoration:InputDecoration(hintText:'NgelX’te kişi ara',prefixIcon:const Icon(Icons.search_rounded),filled:true,fillColor:const Color(0xFFF3F4F6),border:OutlineInputBorder(borderRadius:BorderRadius.circular(22),borderSide:BorderSide.none)),
            ),
          ),""",
"""          const SizedBox(height:5),
          const Padding(
            padding:EdgeInsets.symmetric(horizontal:20),
            child:Text('Arkadaş veya kullanıcı seç • aynı anda birden fazla kişiye gönderebilirsin.',textAlign:TextAlign.center,style:TextStyle(color:Colors.black54,fontSize:12.5,height:1.35)),
          ),
          Padding(
            padding:const EdgeInsets.fromLTRB(14,14,14,8),
            child:TextField(
              autofocus:false,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w700),
              onChanged:(v)=>setSheet(()=>sorgu=v.trim().toLowerCase()),
              decoration:InputDecoration(
                hintText:'NgelX’te kişi ara',hintStyle:const TextStyle(color:Colors.black45,fontWeight:FontWeight.w600),
                prefixIcon:const Icon(Icons.search_rounded,color:Colors.black45),
                filled:true,fillColor:const Color(0xFFF3F4F6),
                border:OutlineInputBorder(borderRadius:BorderRadius.circular(22),borderSide:BorderSide.none),
              ),
            ),
          ),
          if(secilen.isNotEmpty)Padding(
            padding:const EdgeInsets.fromLTRB(18,0,18,6),
            child:Align(alignment:Alignment.centerLeft,child:Container(
              padding:const EdgeInsets.symmetric(horizontal:10,vertical:6),
              decoration:BoxDecoration(color:const Color(0xFFF0E9FF),borderRadius:BorderRadius.circular(14)),
              child:Text('${secilen.length} kişi seçildi',style:const TextStyle(color:Color(0xFF6F41D8),fontWeight:FontWeight.w800)),
            )),
          ),""","share search readability")

live=rep(live,
"""              OutlinedButton.icon(
                onPressed:gonderiliyor?null:()async{Navigator.pop(sheetContext);await _baglantiKopyala();},
                icon:const Icon(Icons.link_rounded),label:const Text('Kopyala'),
              ),""",
"""              OutlinedButton.icon(
                style:OutlinedButton.styleFrom(foregroundColor:const Color(0xFF7C4DFF),side:const BorderSide(color:Color(0xFFB9A7F7)),padding:const EdgeInsets.symmetric(horizontal:14,vertical:14)),
                onPressed:gonderiliyor?null:()async{Navigator.pop(sheetContext);await _baglantiKopyala();},
                icon:const Icon(Icons.link_rounded),label:const Text('Kopyala',style:TextStyle(fontWeight:FontWeight.w800)),
              ),""","share copy button")

old_action="""                onPressed:secilen.isEmpty||gonderiliyor?null:()async{
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
                },"""
new_action="""                onPressed:secilen.isEmpty||gonderiliyor?null:()async{
                  setSheet(()=>gonderiliyor=true);
                  var basarili=0;
                  var basarisiz=0;
                  for(final uid in secilen.toList()){
                    try{await _canliKisiyeGonder(ben,uid);basarili++;}catch(_){basarisiz++;}
                  }
                  if(basarili>0){
                    try{await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).set({'shareCount':FieldValue.increment(basarili)},SetOptions(merge:true));}catch(_){}
                    if(sheetContext.mounted)Navigator.pop(sheetContext);
                    if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                      content:Text(basarisiz==0?'Canlı yayın $basarili kişiye gönderildi.':'$basarili kişiye gönderildi • $basarisiz kişiye gönderilemedi.',style:const TextStyle(fontWeight:FontWeight.w700)),
                      behavior:SnackBarBehavior.floating,width:basarisiz==0?285:330,duration:const Duration(milliseconds:1500),
                      shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(14)),
                    ));
                  }else{
                    if(sheetContext.mounted)setSheet(()=>gonderiliyor=false);
                    if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                      content:const Text('Gönderilemedi • tekrar deneyebilirsin.',style:TextStyle(fontWeight:FontWeight.w700)),
                      behavior:SnackBarBehavior.floating,width:285,duration:const Duration(milliseconds:1500),
                      shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(14)),
                    ));
                  }
                },"""
live=rep(live,old_action,new_action,"partial share success")

main=rep(main,
"""          final yayinlar=snap.data?.docs??[];
          if(yayinlar.isEmpty)return _bosKart(t('noLive'),Icons.live_tv_outlined);""",
"""          final yayinlar=(snap.data?.docs??[]).where((d)=>ngelxCanliKaydiTaze(d.data())).toList();
          if(yayinlar.isEmpty)return _bosKart(t('noLive'),Icons.live_tv_outlined);""","explore fresh live filter")

main=rep(main,
"""    final veri=belge.data()??<String,dynamic>{};
    final roomName=(veri['roomName']??'').toString();
    if(veri['active']!=true||roomName.isEmpty){
      if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Bu canlı yayın sona ermiş.')));
      return;
    }""",
"""    final veri=belge.data()??<String,dynamic>{};
    final roomName=(veri['roomName']??'').toString();
    if(!ngelxCanliKaydiTaze(veri)||roomName.isEmpty){
      if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content:const Text('Bu canlı yayın sona ermiş.',style:TextStyle(fontWeight:FontWeight.w700)),
        behavior:SnackBarBehavior.floating,width:235,duration:const Duration(milliseconds:1400),
        shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(14)),
      ));
      return;
    }""","join stale live guard")

main=rep(main,
"""  final canliBildirimi=tur=='live'||olayTuru=='live_started';""",
"""  final canliBildirimi=tur=='live'||olayTuru=='live_started'||olayTuru=='live_share';""","live share notification classification")

LIVE.write_text(live,encoding="utf-8")
MAIN.write_text(main,encoding="utf-8")
PUB.write_text(pub,encoding="utf-8")
print("Build 328 live fixes + premium beauty v2 applied.")
