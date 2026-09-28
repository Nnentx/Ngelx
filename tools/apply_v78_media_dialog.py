#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN_PATH=ROOT/"app/lib/main.dart"
PUB_PATH=ROOT/"app/pubspec.yaml"
QA_PATH=ROOT/".github/workflows/v65-consolidated-qa.yml"

def one(text,old,new,label):
    n=text.count(old)
    if n!=1:
        raise SystemExit(f"Build 297 patch failed: {label}: expected 1 match, got {n}")
    return text.replace(old,new,1)

main=MAIN_PATH.read_text(encoding="utf-8")
pub=PUB_PATH.read_text(encoding="utf-8")
if "version: 1.0.78+297" in pub:
    raise SystemExit("Build 297 already applied.")

# 1) Arkadaşlıktan çıkar penceresi: açık renk tema + görünür metin + kompakt düzen.
fn=main.find("  Future<void> _arkadasliktanCikar")
if fn<0: raise SystemExit("Build 297 patch failed: friendship dialog function not found")
a=main.find("    final onay=await showDialog<bool>(",fn)
b=main.find("    if(!onay||!mounted)return;",a)
if a<0 or b<0: raise SystemExit("Build 297 patch failed: friendship dialog body not found")
dialog="""    final onay=await showDialog<bool>(
      context:context,
      builder:(d)=>Theme(
        data:ThemeData.light().copyWith(
          colorScheme:ColorScheme.fromSeed(seedColor:mor,brightness:Brightness.light),
          dialogTheme:const DialogThemeData(backgroundColor:Colors.white,surfaceTintColor:Colors.transparent),
          textTheme:ThemeData.light().textTheme.apply(bodyColor:Colors.black87,displayColor:Colors.black87),
        ),
        child:AlertDialog(
          backgroundColor:Colors.white,
          surfaceTintColor:Colors.transparent,
          insetPadding:const EdgeInsets.symmetric(horizontal:28,vertical:24),
          contentPadding:const EdgeInsets.fromLTRB(24,8,24,8),
          actionsPadding:const EdgeInsets.fromLTRB(18,8,18,18),
          shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(28)),
          icon:Container(
            width:54,height:54,
            decoration:BoxDecoration(color:const Color(0xFFFFECEE),borderRadius:BorderRadius.circular(18)),
            child:const Icon(Icons.person_remove_alt_1_rounded,color:Color(0xFFE53935),size:28),
          ),
          title:const Text(
            'Arkadaşlıktan çıkarılsın mı?',
            textAlign:TextAlign.center,
            style:TextStyle(color:Colors.black87,fontWeight:FontWeight.w900,fontSize:20),
          ),
          content:Column(
            mainAxisSize:MainAxisSize.min,
            children:[
              Text(
                '$gorunenAd ile arkadaşlığını kaldırmak istiyor musun?',
                textAlign:TextAlign.center,
                style:const TextStyle(color:Colors.black87,fontSize:14,height:1.35,fontWeight:FontWeight.w600),
              ),
              const SizedBox(height:8),
              const Text(
                'Bu işlem yalnızca arkadaşlığı kaldırır. İstersen daha sonra tekrar arkadaşlık isteği gönderebilirsin.',
                textAlign:TextAlign.center,
                style:TextStyle(color:Colors.black54,fontSize:12.5,height:1.35),
              ),
            ],
          ),
          actions:[
            TextButton(
              onPressed:()=>Navigator.pop(d,false),
              child:const Text('Vazgeç',style:TextStyle(color:mor,fontWeight:FontWeight.w800)),
            ),
            FilledButton(
              style:FilledButton.styleFrom(
                backgroundColor:const Color(0xFFE53935),
                foregroundColor:Colors.white,
                padding:const EdgeInsets.symmetric(horizontal:22,vertical:12),
                shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(18)),
              ),
              onPressed:()=>Navigator.pop(d,true),
              child:const Text('Arkadaşlıktan çıkar',style:TextStyle(fontWeight:FontWeight.w900)),
            ),
          ],
        ),
      ),
    )??false;
"""
main=main[:a]+dialog+main[b:]

# 2) Grup mesajlarında eski/yeni medya alanlarını ortak çözücü ile oku.
main=one(
    main,
    "    final metin=(v['text']??v['message']??v['content']??'').toString(),tur=(v['type']??'text').toString(),media=(v['mediaUrl']??'').toString(),audio=(v['audioUrl']??'').toString();",
    """    final metin=(v['text']??v['message']??v['content']??'').toString(),tur=(v['type']??'text').toString();
    final media=ngelxMesajMedyaUrl(v,video:tur=='video'),videoKapak=ngelxMesajVideoKapagi(v),audio=(v['audioUrl']??'').toString();""",
    "group media URL resolver",
)

old_render="""                else if((tur=='photo'||tur=='gif')&&media.isNotEmpty)
                  IgnorePointer(child:ClipRRect(borderRadius:BorderRadius.circular(14),child:CachedNetworkImage(
                    imageUrl:media,width:246,fit:BoxFit.cover,
                    errorWidget:(_,__,___)=>const SizedBox(width:246,height:116,child:Center(child:Icon(Icons.broken_image_outlined))),
                  )))
                else if(tur=='video'&&media.isNotEmpty)
                  IgnorePointer(child:NgelXGrupVideoMesaj(url:media))"""
new_render="""                else if(tur=='photo'&&media.isNotEmpty)
                  IgnorePointer(child:NgelXSohbetFotoOnizleme(url:media))
                else if(tur=='gif'&&media.isNotEmpty)
                  IgnorePointer(child:ClipRRect(borderRadius:BorderRadius.circular(14),child:CachedNetworkImage(
                    imageUrl:media,width:246,fit:BoxFit.cover,
                    errorWidget:(_,__,___)=>const SizedBox(width:246,height:116,child:Center(child:Icon(Icons.broken_image_outlined))),
                  )))
                else if(tur=='video'&&media.isNotEmpty)
                  IgnorePointer(child:NgelXSohbetVideoOnizleme(url:media,thumbnailUrl:videoKapak))"""
main=one(main,old_render,new_render,"group message photo/video preview")

# 3) Video kapağı yoksa siyah kutu yerine videonun gerçek ilk karesini göster.
main=one(
    main,
    "    return NgelXGrupVideoMesaj(url:url,compact:true);",
    """    return ClipRRect(
      borderRadius:BorderRadius.circular(16),
      child:SizedBox(
        width:246,height:178,
        child:Stack(
          fit:StackFit.expand,
          children:[
            NgelXVideoKapakOnizleme(url:url),
            IgnorePointer(child:_oynatKatmani()),
          ],
        ),
      ),
    );""",
    "private/group video first-frame fallback",
)

# 4) Yeni grup/özel fotoğraflarında uyumluluk alanlarını birlikte kaydet.
main=one(
    main,
    "      final tamam=await payloadGonder({'type':'photo','mediaUrl':url},'📷 Fotoğraf');",
    "      final tamam=await payloadGonder({'type':'photo','mediaUrl':url,'imageUrl':url,'photoUrl':url},'📷 Fotoğraf');",
    "group photo save aliases",
)
main=one(
    main,
    "      await payloadGonder({'type':'video','mediaUrl':url},'🎥 Video');",
    "      await payloadGonder({'type':'video','mediaUrl':url,'videoUrl':url},'🎥 Video');",
    "group video save aliases",
)
main=one(
    main,
    "        'senderId':ben,'text':'','type':'photo','mediaUrl':url,",
    "        'senderId':ben,'text':'','type':'photo','mediaUrl':url,'imageUrl':url,'photoUrl':url,",
    "private photo save aliases",
)

# 5) Grup medya galerisinde videonun kendi görüntüsünü (thumbnail varsa onu, yoksa ilk kareyi) göster.
main=one(
    main,
    "                  final data=docs[i].data(),url=(data['mediaUrl']??'').toString(),t=(data['type']??'').toString();",
    """                  final data=docs[i].data(),t=(data['type']??'').toString();
                  final url=ngelxMesajMedyaUrl(data,video:t=='video');
                  final thumb=ngelxMesajVideoKapagi(data);""",
    "group media gallery URL resolver",
)
old_gallery="""                        if(t=='video')const ColoredBox(color:Color(0xFF15231A),child:Center(child:Icon(Icons.play_circle_fill_rounded,color:Colors.white,size:42)))
                        else if(url.isNotEmpty)CachedNetworkImage(imageUrl:url,fit:BoxFit.cover,errorWidget:(_,__,___)=>const ColoredBox(color:Color(0xFFF0F5F2),child:Icon(Icons.broken_image_outlined)))
                        else const ColoredBox(color:Color(0xFFF0F5F2),child:Icon(Icons.image_outlined)),
                        if(t=='gif')Positioned(left:7,bottom:7,child:Container(padding:const EdgeInsets.symmetric(horizontal:7,vertical:4),decoration:BoxDecoration(color:Colors.black54,borderRadius:BorderRadius.circular(10)),child:const Text('GIF',style:TextStyle(color:Colors.white,fontSize:9,fontWeight:FontWeight.w900)))),"
"""
# The source has no trailing quote/newline token above; use a safer shorter replacement.
old_gallery_core="""                        if(t=='video')const ColoredBox(color:Color(0xFF15231A),child:Center(child:Icon(Icons.play_circle_fill_rounded,color:Colors.white,size:42)))
                        else if(url.isNotEmpty)CachedNetworkImage(imageUrl:url,fit:BoxFit.cover,errorWidget:(_,__,___)=>const ColoredBox(color:Color(0xFFF0F5F2),child:Icon(Icons.broken_image_outlined)))
                        else const ColoredBox(color:Color(0xFFF0F5F2),child:Icon(Icons.image_outlined)),
                        if(t=='gif')Positioned(left:7,bottom:7,child:Container(padding:const EdgeInsets.symmetric(horizontal:7,vertical:4),decoration:BoxDecoration(color:Colors.black54,borderRadius:BorderRadius.circular(10)),child:const Text('GIF',style:TextStyle(color:Colors.white,fontSize:9,fontWeight:FontWeight.w900)))),"
"""
new_gallery_core="""                        if(t=='video'&&thumb.isNotEmpty)
                          CachedNetworkImage(
                            imageUrl:thumb,fit:BoxFit.cover,
                            errorWidget:(_,__,___)=>url.isEmpty
                              ?const ColoredBox(color:Color(0xFF15231A))
                              :NgelXVideoKapakOnizleme(url:url),
                          )
                        else if(t=='video'&&url.isNotEmpty)NgelXVideoKapakOnizleme(url:url)
                        else if(t=='video')const ColoredBox(color:Color(0xFF15231A))
                        else if(url.isNotEmpty)CachedNetworkImage(imageUrl:url,fit:BoxFit.cover,errorWidget:(_,__,___)=>const ColoredBox(color:Color(0xFFF0F5F2),child:Icon(Icons.broken_image_outlined)))
                        else const ColoredBox(color:Color(0xFFF0F5F2),child:Icon(Icons.image_outlined)),
                        if(t=='video')const Center(child:DecoratedBox(
                          decoration:BoxDecoration(color:Colors.black45,shape:BoxShape.circle),
                          child:Padding(padding:EdgeInsets.all(7),child:Icon(Icons.play_arrow_rounded,color:Colors.white,size:31)),
                        )),
                        if(t=='gif')Positioned(left:7,bottom:7,child:Container(padding:const EdgeInsets.symmetric(horizontal:7,vertical:4),decoration:BoxDecoration(color:Colors.black54,borderRadius:BorderRadius.circular(10)),child:const Text('GIF',style:TextStyle(color:Colors.white,fontSize:9,fontWeight:FontWeight.w900)))),"
"""
# Strip the accidental final quote character from the literal representations above.
old_gallery_core=old_gallery_core[:-2] if old_gallery_core.endswith('",\n') else old_gallery_core
new_gallery_core=new_gallery_core[:-2] if new_gallery_core.endswith('",\n') else new_gallery_core
# Direct exact snippets without synthetic quote artifacts.
old_gallery_core = """                        if(t=='video')const ColoredBox(color:Color(0xFF15231A),child:Center(child:Icon(Icons.play_circle_fill_rounded,color:Colors.white,size:42)))
                        else if(url.isNotEmpty)CachedNetworkImage(imageUrl:url,fit:BoxFit.cover,errorWidget:(_,__,___)=>const ColoredBox(color:Color(0xFFF0F5F2),child:Icon(Icons.broken_image_outlined)))
                        else const ColoredBox(color:Color(0xFFF0F5F2),child:Icon(Icons.image_outlined)),
                        if(t=='gif')Positioned(left:7,bottom:7,child:Container(padding:const EdgeInsets.symmetric(horizontal:7,vertical:4),decoration:BoxDecoration(color:Colors.black54,borderRadius:BorderRadius.circular(10)),child:const Text('GIF',style:TextStyle(color:Colors.white,fontSize:9,fontWeight:FontWeight.w900)))),
"""
new_gallery_core = """                        if(t=='video'&&thumb.isNotEmpty)
                          CachedNetworkImage(
                            imageUrl:thumb,fit:BoxFit.cover,
                            errorWidget:(_,__,___)=>url.isEmpty
                              ?const ColoredBox(color:Color(0xFF15231A))
                              :NgelXVideoKapakOnizleme(url:url),
                          )
                        else if(t=='video'&&url.isNotEmpty)NgelXVideoKapakOnizleme(url:url)
                        else if(t=='video')const ColoredBox(color:Color(0xFF15231A))
                        else if(url.isNotEmpty)CachedNetworkImage(imageUrl:url,fit:BoxFit.cover,errorWidget:(_,__,___)=>const ColoredBox(color:Color(0xFFF0F5F2),child:Icon(Icons.broken_image_outlined)))
                        else const ColoredBox(color:Color(0xFFF0F5F2),child:Icon(Icons.image_outlined)),
                        if(t=='video')const Center(child:DecoratedBox(
                          decoration:BoxDecoration(color:Colors.black45,shape:BoxShape.circle),
                          child:Padding(padding:EdgeInsets.all(7),child:Icon(Icons.play_arrow_rounded,color:Colors.white,size:31)),
                        )),
                        if(t=='gif')Positioned(left:7,bottom:7,child:Container(padding:const EdgeInsets.symmetric(horizontal:7,vertical:4),decoration:BoxDecoration(color:Colors.black54,borderRadius:BorderRadius.circular(10)),child:const Text('GIF',style:TextStyle(color:Colors.white,fontSize:9,fontWeight:FontWeight.w900)))),
"""
main=one(main,old_gallery_core,new_gallery_core,"group media gallery video first frame")

# 6) Sürüm.
main=one(main,"defaultValue: '1.0.77'","defaultValue: '1.0.78'","runtime version")
main=one(main,"defaultValue: '296'","defaultValue: '297'","runtime build")
MAIN_PATH.write_text(main,encoding="utf-8")

pub=one(pub,"version: 1.0.77+296","version: 1.0.78+297","pubspec version")
PUB_PATH.write_text(pub,encoding="utf-8")

# 7) Birikimli testlerin sürüm zincirini güncelle.
for path in [
    ROOT/"tools/verify_v64_app_quality.py",
    ROOT/"tools/verify_v65_media_traffic.py",
    ROOT/"tools/verify_v65_work.py",
    ROOT/"tools/verify_v66_work.py",
    ROOT/"tools/verify_v67_work.py",
    ROOT/"tools/verify_v68_work.py",
]:
    t=path.read_text(encoding="utf-8")
    if '"version: 1.0.78+297"' not in t:
        t=t.replace('"version: 1.0.77+296"))','"version: 1.0.77+296", "version: 1.0.78+297"))')
    path.write_text(t,encoding="utf-8")

v72=ROOT/"tools/verify_v72_device_fixes.py"
t=v72.read_text(encoding="utf-8")
t=t.replace('require("version: 1.0.77+296" in PUBSPEC, "Build 296 sürüm zinciri")','require("version: 1.0.78+297" in PUBSPEC, "Build 297 sürüm zinciri")')
t=t.replace('require("defaultValue: \'1.0.77\'" in MAIN and "defaultValue: \'296\'" in MAIN,','require("defaultValue: \'1.0.78\'" in MAIN and "defaultValue: \'297\'" in MAIN,')
v72.write_text(t,encoding="utf-8")

v76=ROOT/"tools/verify_v76_chat_media.py"
t=v76.read_text(encoding="utf-8")
t=t.replace('require("version: 1.0.77+296" in PUBSPEC, "Build 296 surumu")','require("version: 1.0.78+297" in PUBSPEC, "Build 297 surumu")')
t=t.replace('require("defaultValue: \'1.0.77\'" in MAIN and "defaultValue: \'296\'" in MAIN,','require("defaultValue: \'1.0.78\'" in MAIN and "defaultValue: \'297\'" in MAIN,')
v76.write_text(t,encoding="utf-8")

v77=ROOT/"tools/verify_v77_social_relations.py"
t=v77.read_text(encoding="utf-8")
t=t.replace('require("version: 1.0.77+296" in PUB,"Build 296 surumu")','require("version: 1.0.78+297" in PUB,"Build 297 surumu")')
t=t.replace('require("defaultValue: \'1.0.77\'" in MAIN and "defaultValue: \'296\'" in MAIN,"uygulama ici surum")','require("defaultValue: \'1.0.78\'" in MAIN and "defaultValue: \'297\'" in MAIN,"uygulama ici surum")')
v77.write_text(t,encoding="utf-8")

qa=QA_PATH.read_text(encoding="utf-8")
old="""      - name: Build 296 takip ve arkadaslik isteklerini dogrula
        run: python3 tools/verify_v77_social_relations.py

      - name: R2 Worker JavaScript kontrolu"""
new="""      - name: Build 296 takip ve arkadaslik isteklerini dogrula
        run: python3 tools/verify_v77_social_relations.py

      - name: Build 297 grup-ozel medya ve diyalog duzeltmelerini dogrula
        run: python3 tools/verify_v78_media_dialog.py

      - name: R2 Worker JavaScript kontrolu"""
qa=one(qa,old,new,"QA Build 297 step")
QA_PATH.write_text(qa,encoding="utf-8")

print("Build 297 media/dialog patch prepared.")
