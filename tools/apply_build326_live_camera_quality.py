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
        raise SystemExit("Build 326 patch failed: marker not found: "+label)
    return text.replace(old,new,1)

pub=rep(pub,"version: 1.0.106+325","version: 1.0.107+326","version")
main=main.replace("defaultValue: '1.0.106'","defaultValue: '1.0.107'")
main=main.replace("defaultValue: '325'","defaultValue: '326'")

helpers=r"""
class _NgelXCanliFiltrePreset {
  final String ad;
  final double parlaklik, kontrast, doygunluk, sicaklik, netlik;
  const _NgelXCanliFiltrePreset(this.ad,{required this.parlaklik,required this.kontrast,required this.doygunluk,required this.sicaklik,required this.netlik});
}

const List<_NgelXCanliFiltrePreset> ngelxCanliProFiltreleri=[
  _NgelXCanliFiltrePreset('Doğal',parlaklik:.02,kontrast:1.06,doygunluk:1.05,sicaklik:.02,netlik:.10),
  _NgelXCanliFiltrePreset('Canlı',parlaklik:.035,kontrast:1.18,doygunluk:1.20,sicaklik:.04,netlik:.18),
  _NgelXCanliFiltrePreset('Portre Pro',parlaklik:.05,kontrast:1.10,doygunluk:1.08,sicaklik:.08,netlik:.08),
  _NgelXCanliFiltrePreset('Clean HD',parlaklik:.035,kontrast:1.13,doygunluk:1.03,sicaklik:0,netlik:.22),
  _NgelXCanliFiltrePreset('Parlak',parlaklik:.08,kontrast:1.08,doygunluk:1.10,sicaklik:.03,netlik:.08),
  _NgelXCanliFiltrePreset('Sıcak',parlaklik:.03,kontrast:1.10,doygunluk:1.12,sicaklik:.20,netlik:.10),
  _NgelXCanliFiltrePreset('Soğuk',parlaklik:.02,kontrast:1.11,doygunluk:1.08,sicaklik:-.15,netlik:.12),
  _NgelXCanliFiltrePreset('Kontrast+',parlaklik:.01,kontrast:1.28,doygunluk:1.12,sicaklik:.02,netlik:.25),
  _NgelXCanliFiltrePreset('Gece',parlaklik:.12,kontrast:1.08,doygunluk:1.06,sicaklik:.05,netlik:.06),
];

double _ngelxCanliDouble(dynamic value,double fallback)=>value is num?value.toDouble():fallback;

_NgelXCanliFiltrePreset ngelxCanliPresetBul(String? ad){
  final aranan=(ad??'').trim();
  for(final p in ngelxCanliProFiltreleri){if(p.ad==aranan)return p;}
  return ngelxCanliProFiltreleri.first;
}

List<double> ngelxCanliRenkMatrisi({
  required _NgelXCanliFiltrePreset preset,
  double parlaklik=0,double kontrast=1,double doygunluk=1,double sicaklik=0,double netlik=0,
  bool otomatikIyilestirme=true,bool dusukIsik=false,
}){
  var b=(preset.parlaklik+parlaklik).clamp(-.18,.24).toDouble();
  var c=(preset.kontrast*kontrast).clamp(.75,1.55).toDouble();
  var s=(preset.doygunluk*doygunluk).clamp(.65,1.65).toDouble();
  var w=(preset.sicaklik+sicaklik).clamp(-.55,.55).toDouble();
  final n=(preset.netlik+netlik).clamp(0.0,1.0).toDouble();
  if(otomatikIyilestirme){b+=.018;c*=1.035;s*=1.025;}
  if(dusukIsik){b+=.075;c*=.97;s*=1.035;w+=.025;}
  c=(c*(1+n*.10)).clamp(.75,1.65).toDouble();
  s=(s*(1+n*.04)).clamp(.65,1.75).toDouble();
  const lr=.2126,lg=.7152,lb=.0722;
  final inv=1-s;
  final wr=(1+w*.12).clamp(.90,1.10).toDouble();
  final wb=(1-w*.12).clamp(.90,1.10).toDouble();
  final offset=(1-c)*128+b*255;
  return <double>[
    (inv*lr+s)*c*wr,(inv*lg)*c*wr,(inv*lb)*c*wr,0,offset+w*5,
    (inv*lr)*c,(inv*lg+s)*c,(inv*lb)*c,0,offset,
    (inv*lr)*c*wb,(inv*lg)*c*wb,(inv*lb+s)*c*wb,0,offset-w*5,
    0,0,0,1,0,
  ];
}

Widget ngelxCanliEfektKatmani({required Widget child,required Map<String,dynamic> veri}){
  final preset=ngelxCanliPresetBul((veri['filterPro']??veri['filter']??'Doğal').toString());
  final beauty=_ngelxCanliDouble(veri['beauty']??veri['retouch'],.20).clamp(0.0,1.0).toDouble();
  final matris=ngelxCanliRenkMatrisi(
    preset:preset,
    parlaklik:_ngelxCanliDouble(veri['filterBrightness'],0),
    kontrast:_ngelxCanliDouble(veri['filterContrast'],1),
    doygunluk:_ngelxCanliDouble(veri['filterSaturation'],1),
    sicaklik:_ngelxCanliDouble(veri['filterWarmth'],0),
    netlik:_ngelxCanliDouble(veri['filterClarity'],.12),
    otomatikIyilestirme:veri['autoEnhance']!=false,
    dusukIsik:veri['lowLight']==true,
  );
  return ColorFiltered(
    colorFilter:ColorFilter.matrix(matris),
    child:Stack(fit:StackFit.expand,children:[
      child,
      if(beauty>.01)IgnorePointer(child:ColoredBox(color:Colors.white.withOpacity((beauty*.045).clamp(0.0,.055).toDouble()))),
    ]),
  );
}
"""

live=rep(live,"class CanliHazirlikPage extends StatefulWidget {",helpers+"\nclass CanliHazirlikPage extends StatefulWidget {","pro filter helpers")

live=rep(live,
"""  double retus = .18;
  int filtreIndex = 0;""",
"""  double retus = .22;
  double parlaklik = 0;
  double kontrast = 1;
  double doygunluk = 1;
  double sicaklik = 0;
  double netlik = .15;
  bool otomatikIyilestirme = true;
  bool dusukIsik = false;
  int filtreIndex = 0;""","pro filter state")

live=rep(live,
"""  lk.CameraCaptureOptions get _kameraAyarlari => lk.CameraCaptureOptions(
    cameraPosition: arkaKamera ? lk.CameraPosition.back : lk.CameraPosition.front,
    params: _yayinKalitesi,
    maxFrameRate: fps.toDouble(),
    stopCameraCaptureOnMute: true,
  );""",
"""  lk.CameraCaptureOptions get _kameraAyarlari => lk.CameraCaptureOptions(
    cameraPosition: arkaKamera ? lk.CameraPosition.back : lk.CameraPosition.front,
    focusMode: lk.CameraFocusMode.auto,
    exposureMode: lk.CameraExposureMode.auto,
    params: _yayinKalitesi,
    maxFrameRate: fps.toDouble(),
    stopCameraCaptureOnMute: true,
  );""","camera focus exposure")

live=rep(live,
"""      await yeni.initialize();
      if (!arkaKamera) flashAcik = false;""",
"""      await yeni.initialize();
      try { await yeni.setFocusMode(FocusMode.auto); } catch (_) {}
      try { await yeni.setExposureMode(ExposureMode.auto); } catch (_) {}
      if (!arkaKamera) flashAcik = false;""","preview focus exposure")

live=rep(live,
"""    final filtre = ngelxKameraFiltreleri[filtreIndex];
    return ColorFiltered(
      colorFilter: ColorFilter.matrix(filtre.matris),
      child: Stack(fit: StackFit.expand, children: [
        FittedBox(
          fit: BoxFit.cover,
          child: SizedBox(width: c.value.previewSize?.height ?? 720, height: c.value.previewSize?.width ?? 1280, child: CameraPreview(c)),
        ),
        if (retus > .01) IgnorePointer(child: ColoredBox(color: Colors.white.withOpacity(retus * .12))),
      ]),
    );""",
"""    final filtre=ngelxCanliProFiltreleri[filtreIndex];
    final matris=ngelxCanliRenkMatrisi(
      preset:filtre,parlaklik:parlaklik,kontrast:kontrast,doygunluk:doygunluk,sicaklik:sicaklik,netlik:netlik,
      otomatikIyilestirme:otomatikIyilestirme,dusukIsik:dusukIsik,
    );
    return ColorFiltered(
      colorFilter:ColorFilter.matrix(matris),
      child:Stack(fit:StackFit.expand,children:[
        FittedBox(fit:BoxFit.cover,child:SizedBox(width:c.value.previewSize?.height??720,height:c.value.previewSize?.width??1280,child:CameraPreview(c))),
        if(retus>.01)IgnorePointer(child:ColoredBox(color:Colors.white.withOpacity((retus*.045).clamp(0.0,.055).toDouble()))),
        Positioned(left:10,bottom:10,child:Container(
          padding:const EdgeInsets.symmetric(horizontal:9,vertical:5),
          decoration:BoxDecoration(color:Colors.black54,borderRadius:BorderRadius.circular(12)),
          child:Text('${filtre.ad} • PRO',style:const TextStyle(color:Colors.white,fontSize:11,fontWeight:FontWeight.w800)),
        )),
      ]),
    );""","preview pro filter")

live=rep(live,
"""        'filter': ngelxKameraFiltreleri[filtreIndex].ad,
        'retouch': retus,""",
"""        'filter': ngelxCanliProFiltreleri[filtreIndex].ad,
        'filterPro': ngelxCanliProFiltreleri[filtreIndex].ad,
        'retouch': retus,
        'beauty': retus,
        'filterBrightness': parlaklik,
        'filterContrast': kontrast,
        'filterSaturation': doygunluk,
        'filterWarmth': sicaklik,
        'filterClarity': netlik,
        'autoEnhance': otomatikIyilestirme,
        'lowLight': dusukIsik,""","firestore pro settings")

old_ui=r"""            const Text('NgelX filtreleri', style: TextStyle(color: Colors.black87, fontSize: 16, fontWeight: FontWeight.w800)),
            const SizedBox(height: 8),
            SizedBox(height: 42, child: ListView.separated(
              padding: const EdgeInsets.only(right: 22),
              scrollDirection: Axis.horizontal,
              itemCount: ngelxKameraFiltreleri.length,
              separatorBuilder: (_, __) => const SizedBox(width: 7),
              itemBuilder: (_, i) => ChoiceChip(label: Text(ngelxKameraFiltreleri[i].ad), selected: filtreIndex == i, onSelected: baglaniyor ? null : (_) => setState(() => filtreIndex = i)),
            )),
            const SizedBox(height: 12),
            Row(children: [
              const Icon(Icons.auto_fix_high_rounded, color: Color(0xFFE91E63)),
              const SizedBox(width: 9),
              const Text('Doğal rötuş', style: TextStyle(color: Colors.black87, fontWeight: FontWeight.w700)),
              Expanded(child: Slider(value: retus, min: 0, max: 1, divisions: 10, label: '%${(retus * 100).round()}', onChanged: baglaniyor ? null : (v) => setState(() => retus = v))),
              SizedBox(width: 38, child: Text('%${(retus * 100).round()}', style: const TextStyle(color: Colors.black54, fontWeight: FontWeight.w700))),
            ]),"""

new_ui=r"""            Container(
              padding:const EdgeInsets.fromLTRB(14,14,14,10),
              decoration:BoxDecoration(color:const Color(0xFFF7F8FA),borderRadius:BorderRadius.circular(22),border:Border.all(color:const Color(0xFFE8EBEF))),
              child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                Row(children:[
                  const Icon(Icons.auto_awesome_rounded,color:Color(0xFF7C4DFF)),
                  const SizedBox(width:8),
                  const Expanded(child:Text('NgelX Görüntü Stüdyosu',style:TextStyle(color:Colors.black87,fontSize:17,fontWeight:FontWeight.w900))),
                  Container(padding:const EdgeInsets.symmetric(horizontal:8,vertical:4),decoration:BoxDecoration(color:Color(0xFF111111),borderRadius:BorderRadius.all(Radius.circular(10))),child:const Text('PRO',style:TextStyle(color:Colors.white,fontSize:10,fontWeight:FontWeight.w900))),
                ]),
                const SizedBox(height:11),
                Wrap(spacing:7,runSpacing:7,children:[
                  for(var i=0;i<ngelxCanliProFiltreleri.length;i++)ChoiceChip(
                    label:Text(ngelxCanliProFiltreleri[i].ad),selected:filtreIndex==i,
                    onSelected:baglaniyor?null:(_)=>setState(()=>filtreIndex=i),
                  ),
                ]),
                const Divider(height:24),
                _proSlider('Güzellik',Icons.face_retouching_natural_rounded,retus,0,1,(v)=>setState(()=>retus=v),yuzde:true),
                _proSlider('Parlaklık',Icons.light_mode_rounded,parlaklik,-.12,.16,(v)=>setState(()=>parlaklik=v)),
                _proSlider('Kontrast',Icons.contrast_rounded,kontrast,.82,1.30,(v)=>setState(()=>kontrast=v),merkez:1),
                _proSlider('Canlılık',Icons.palette_rounded,doygunluk,.82,1.35,(v)=>setState(()=>doygunluk=v),merkez:1),
                _proSlider('Sıcaklık',Icons.thermostat_rounded,sicaklik,-.35,.35,(v)=>setState(()=>sicaklik=v)),
                _proSlider('Netlik',Icons.hd_rounded,netlik,0,.60,(v)=>setState(()=>netlik=v),yuzde:true),
                SwitchListTile(
                  contentPadding:EdgeInsets.zero,dense:true,value:otomatikIyilestirme,
                  onChanged:baglaniyor?null:(v)=>setState(()=>otomatikIyilestirme=v),
                  secondary:const Icon(Icons.auto_mode_rounded,color:Color(0xFF00A6C8)),
                  title:const Text('Otomatik görüntü iyileştirme',style:TextStyle(fontWeight:FontWeight.w800)),
                  subtitle:const Text('Işık, kontrast ve canlılığı dengeler.'),
                ),
                SwitchListTile(
                  contentPadding:EdgeInsets.zero,dense:true,value:dusukIsik,
                  onChanged:baglaniyor?null:(v)=>setState(()=>dusukIsik=v),
                  secondary:const Icon(Icons.nightlight_round,color:Color(0xFF5D5FEF)),
                  title:const Text('Düşük ışık desteği',style:TextStyle(fontWeight:FontWeight.w800)),
                  subtitle:const Text('Karanlık ortamda yüzü ve gölgeleri daha görünür tutar.'),
                ),
              ]),
            ),"""

live=rep(live,old_ui,new_ui,"prepare pro studio ui")

live=rep(live,
"""  Widget _canliSecimKutusu(String etiket, String deger, List<String> secenekler, FutureOr<void> Function(String) degisti) {""",
r"""  Widget _proSlider(String etiket,IconData ikon,double deger,double min,double max,ValueChanged<double> degisti,{bool yuzde=false,double? merkez}){
    final yazi=yuzde?'%${(deger*100).round()}':(merkez!=null?'${deger.toStringAsFixed(2)}x':(deger>=0?'+${deger.toStringAsFixed(2)}':deger.toStringAsFixed(2)));
    return Row(children:[
      SizedBox(width:31,child:Icon(ikon,size:20,color:const Color(0xFF5F6368))),
      SizedBox(width:78,child:Text(etiket,style:const TextStyle(fontWeight:FontWeight.w700,fontSize:12.5))),
      Expanded(child:Slider(value:deger.clamp(min,max).toDouble(),min:min,max:max,onChanged:baglaniyor?null:degisti)),
      SizedBox(width:50,child:Text(yazi,textAlign:TextAlign.end,style:const TextStyle(color:Colors.black54,fontWeight:FontWeight.w700,fontSize:12))),
    ]);
  }

  Widget _canliSecimKutusu(String etiket, String deger, List<String> secenekler, FutureOr<void> Function(String) degisti) {""","pro slider helper")

live=rep(live,
"""  Future<void> _paylas() async {
    await Clipboard.setData(ClipboardData(text: 'NgelX canlı yayın • ${widget.baslik}\nngelx://live/${widget.belgeId}'));
    if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Canlı yayın bağlantısı kopyalandı.')));
  }""",
r"""  Future<void> _goruntuStudyoPaneli() async {
    if(!widget.yayinSahibi)return;
    final ref=FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId);
    final belge=await ref.get();
    final veri=belge.data()??<String,dynamic>{};
    var presetAdi=(veri['filterPro']??veri['filter']??'Doğal').toString();
    var beauty=_ngelxCanliDouble(veri['beauty']??veri['retouch'],.22).clamp(0.0,1.0).toDouble();
    var bright=_ngelxCanliDouble(veri['filterBrightness'],0).clamp(-.12,.16).toDouble();
    var contrast=_ngelxCanliDouble(veri['filterContrast'],1).clamp(.82,1.30).toDouble();
    var saturation=_ngelxCanliDouble(veri['filterSaturation'],1).clamp(.82,1.35).toDouble();
    var warmth=_ngelxCanliDouble(veri['filterWarmth'],0).clamp(-.35,.35).toDouble();
    var clarity=_ngelxCanliDouble(veri['filterClarity'],.15).clamp(0.0,.60).toDouble();
    var autoEnhance=veri['autoEnhance']!=false;
    var lowLight=veri['lowLight']==true;
    Future<void> yaz(Map<String,dynamic> yama)=>ref.set(yama,SetOptions(merge:true));
    if(!mounted)return;
    await showModalBottomSheet<void>(
      context:context,isScrollControlled:true,backgroundColor:Colors.white,showDragHandle:true,
      builder:(sheetContext)=>StatefulBuilder(builder:(context,setSheet){
        Widget ayarSlider(String ad,IconData ikon,double value,double min,double max,ValueChanged<double> change,ValueChanged<double> save,{bool percent=false}){
          return Row(children:[
            SizedBox(width:34,child:Icon(ikon,color:const Color(0xFF5F6368))),
            SizedBox(width:78,child:Text(ad,style:const TextStyle(fontWeight:FontWeight.w700,fontSize:12.5))),
            Expanded(child:Slider(value:value,min:min,max:max,onChanged:change,onChangeEnd:save)),
            SizedBox(width:46,child:Text(percent?'%${(value*100).round()}':value.toStringAsFixed(2),textAlign:TextAlign.end,style:const TextStyle(fontWeight:FontWeight.w700,color:Colors.black54,fontSize:12))),
          ]);
        }
        return SafeArea(child:Padding(
          padding:EdgeInsets.fromLTRB(16,0,16,18+MediaQuery.of(context).viewInsets.bottom),
          child:SingleChildScrollView(child:Column(mainAxisSize:MainAxisSize.min,crossAxisAlignment:CrossAxisAlignment.start,children:[
            const Text('Görüntü Stüdyosu',style:TextStyle(fontSize:21,fontWeight:FontWeight.w900)),
            const SizedBox(height:4),
            const Text('Değişiklikler yayındaki NgelX görüntüsüne anında uygulanır.',style:TextStyle(color:Colors.black54)),
            const SizedBox(height:12),
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
            SwitchListTile(contentPadding:EdgeInsets.zero,value:autoEnhance,onChanged:(v){setSheet(()=>autoEnhance=v);unawaited(yaz({'autoEnhance':v}));},secondary:const Icon(Icons.auto_mode_rounded,color:Color(0xFF00A6C8)),title:const Text('Otomatik iyileştirme',style:TextStyle(fontWeight:FontWeight.w800))),
            SwitchListTile(contentPadding:EdgeInsets.zero,value:lowLight,onChanged:(v){setSheet(()=>lowLight=v);unawaited(yaz({'lowLight':v}));},secondary:const Icon(Icons.nightlight_round,color:Color(0xFF5D5FEF)),title:const Text('Düşük ışık',style:TextStyle(fontWeight:FontWeight.w800))),
          ])),
        ));
      }),
    );
  }

  Future<void> _paylas() async {
    await Clipboard.setData(ClipboardData(text:'NgelX canlı yayın • ${widget.baslik}\nngelx://live/${widget.belgeId}'));
    if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(
      content:const Text('Bağlantı kopyalandı.',style:TextStyle(fontWeight:FontWeight.w700)),
      behavior:SnackBarBehavior.floating,
      margin:const EdgeInsets.fromLTRB(22,0,22,18),
      duration:const Duration(milliseconds:1400),
      shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(16)),
    ));
  }""","live studio panel")

live=rep(live,
"""          Positioned.fill(child: track == null ? const Center(child: CircularProgressIndicator()) : lk.VideoTrackRenderer(track, fit: lk.VideoViewFit.cover)),""",
r"""          Positioned.fill(
            child:track==null
              ?const Center(child:CircularProgressIndicator())
              :StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
                stream:FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).snapshots(),
                builder:(_,snap){
                  final veri=snap.data?.data()??<String,dynamic>{};
                  return ngelxCanliEfektKatmani(veri:veri,child:lk.VideoTrackRenderer(track,fit:lk.VideoViewFit.cover));
                },
              ),
          ),""","live render effect")

live=rep(live,
"""                  IconButton.filled(onPressed: kameraAcik && !kameraDegisiyor ? _yayinKamerasiniCevir : null, tooltip: 'Ön/arka kamerayı çevir', icon: kameraDegisiyor ? const SizedBox(width: 19, height: 19, child: CircularProgressIndicator(strokeWidth: 2)) : const Icon(Icons.cameraswitch_rounded)),
                  const SizedBox(width: 9),
                  IconButton.filledTonal(onPressed: _paylas, tooltip: 'Yayını paylaş', icon: const Icon(Icons.share_rounded)),""",
"""                  IconButton.filled(onPressed: kameraAcik && !kameraDegisiyor ? _yayinKamerasiniCevir : null, tooltip: 'Ön/arka kamerayı çevir', icon: kameraDegisiyor ? const SizedBox(width: 19, height: 19, child: CircularProgressIndicator(strokeWidth: 2)) : const Icon(Icons.cameraswitch_rounded)),
                  const SizedBox(width: 9),
                  IconButton.filledTonal(onPressed: _goruntuStudyoPaneli, tooltip: 'Görüntü Stüdyosu', icon: const Icon(Icons.tune_rounded)),
                  const SizedBox(width: 9),
                  IconButton.filledTonal(onPressed: _paylas, tooltip: 'Yayını paylaş', icon: const Icon(Icons.share_rounded)),""","live studio button")

LIVE.write_text(live,encoding="utf-8")
MAIN.write_text(main,encoding="utf-8")
PUB.write_text(pub,encoding="utf-8")
print("Build 326 PRO live camera quality package applied.")
