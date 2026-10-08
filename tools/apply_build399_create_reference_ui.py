#!/usr/bin/env python3
from pathlib import Path
p=Path("app/lib/main.dart")
src=p.read_text(encoding="utf-8")
start=src.index("            Container(\n              padding:const EdgeInsets.fromLTRB(18,16,18,15),",src.index("class _YeniYuklePageState"))
end=src.index("            const SizedBox(height:20),",start)+len("            const SizedBox(height:20),")
old=src[start:end]
new=r'''            Row(children:[
              const Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                Text('Üret',style:TextStyle(color:Color(0xFF080E1D),fontSize:31,fontWeight:FontWeight.w900,letterSpacing:-.6)),
                SizedBox(height:2),
                Text('Paylaş, keşfet, ilham ver',style:TextStyle(color:Color(0xFF858B9A),fontSize:14)),
              ])),
              _finalUstUretIkon(Icons.photo_library_outlined,(){_turDegistir('photo');unawaited(medyaSec());}),
              _finalUstUretIkon(Icons.photo_camera_outlined,()=>unawaited(kameraSecimi())),
              _finalUstUretIkon(Icons.text_fields_rounded,()=>_turDegistir('text')),
              _finalUstUretIkon(Icons.auto_awesome_rounded,(){if(tur=='text')_turDegistir('photo');setState(()=>fotoEfekti=fotoEfekti=='Yok'?'Parlak':'Yok');},vurgu:true),
            ]),
            if(taslakVar)Row(mainAxisAlignment:MainAxisAlignment.center,children:[const Icon(Icons.drafts_outlined,size:17,color:mor),const SizedBox(width:6),Text(lt('Taslak otomatik kaydediliyor','Draft is autosaving'),style:const TextStyle(color:Colors.black54,fontSize:12,fontWeight:FontWeight.w700)),TextButton(onPressed:yukleniyor?null:()=>_taslagiSil(),child:Text(lt('Temizle','Clear')))]),
            const SizedBox(height:18),
            Row(children:[
              _finalUretKart(Icons.photo_camera_rounded,'Fotoğraf','Hemen çek\nve paylaş',(){_turDegistir('photo');unawaited(kamerayiAc(video:false));}),
              _finalUretKart(Icons.play_arrow_rounded,'Video','Anını kaydet\nve paylaş',(){_turDegistir('video');unawaited(kamerayiAc(video:true));}),
              _finalUretKart(Icons.text_fields_rounded,'Yazı','Düşüncelerini\npaylaş',()=>_turDegistir('text')),
              _finalUretKart(Icons.emoji_emotions_outlined,'Efektler','Özel efektlerle\npaylaş',(){if(tur=='text')_turDegistir('photo');setState(()=>fotoEfekti=fotoEfekti=='Yok'?'Parlak':'Yok');}),
            ]),
            const SizedBox(height:14),
            Container(
              padding:const EdgeInsets.all(5),
              decoration:BoxDecoration(color:const Color(0xFFF6F7FA),borderRadius:BorderRadius.circular(20)),
              child:Row(children:[
                Expanded(child:_finalUretSekme(Icons.photo_library_outlined,'Gönderi',true,(){})),
                Expanded(child:_finalUretSekme(Icons.auto_stories_outlined,'Hikaye',false,()=>unawaited(hikayeSecimi()))),
                Expanded(child:_finalUretSekme(Icons.movie_creation_outlined,'Reels',false,_reelsSec)),
                Expanded(child:_finalUretSekme(Icons.wifi_tethering_rounded,'Canlı Yayın',false,()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const CanliHazirlikPage())))),
              ]),
            ),
            const SizedBox(height:14),
            Container(
              padding:const EdgeInsets.fromLTRB(12,12,12,10),
              decoration:BoxDecoration(color:Colors.white,borderRadius:BorderRadius.circular(20),border:Border.all(color:const Color(0xFFE8EAF0))),
              child:Column(children:[
                Row(children:[
                  const CircleAvatar(radius:23,backgroundColor:Color(0xFFF1ECFF),child:Icon(Icons.person_rounded,color:mor)),
                  const SizedBox(width:10),
                  Expanded(child:TextField(controller:aciklama,enabled:!yukleniyor,maxLines:3,minLines:1,decoration:const InputDecoration(hintText:'Ne paylaşmak istersin?',filled:true,fillColor:Color(0xFFF8F9FC),border:OutlineInputBorder(borderSide:BorderSide.none,borderRadius:BorderRadius.all(Radius.circular(18)))))),
                  const Icon(Icons.emoji_emotions_outlined,color:Color(0xFF7C8396)),
                ]),
                const SizedBox(height:10),
                Row(children:[
                  _finalUretArac(Icons.photo_rounded,'Fotoğraf',(){_turDegistir('photo');unawaited(medyaSec());}),
                  _finalUretArac(Icons.videocam_rounded,'Video',(){_turDegistir('video');unawaited(medyaSec());}),
                  _finalUretArac(Icons.location_on_rounded,'Konum',()=>FocusScope.of(context).unfocus()),
                  _finalUretArac(Icons.person_add_alt_1_rounded,'Etiketle',()=>FocusScope.of(context).unfocus()),
                  _finalUretArac(Icons.poll_rounded,'Anket',()=>ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Anket aracı hazırlanıyor.')))),
                  _finalUretArac(Icons.music_note_rounded,'Müzik',()=>unawaited(_muzikSec())),
                ]),
              ]),
            ),
            const SizedBox(height:16),'''
src=src[:start]+new+src[end:]

# Replace publish button label/style with approved reference.
src=src.replace("gradient:const LinearGradient(colors:[Color(0xFF22D3EE),Color(0xFF7C3AED)]),","gradient:const LinearGradient(colors:[Color(0xFFA23BFF),Color(0xFF2464FF)]),",1)
src=src.replace("icon:const Icon(Icons.publish_rounded,color:Colors.white),\n                  label:Text(t('publishOnNgelx'),style:const TextStyle(color:Colors.white,fontSize:17,fontWeight:FontWeight.w900)),","icon:const Icon(Icons.send_rounded,color:Colors.white),\n                  label:const Text('Paylaş',style:TextStyle(color:Colors.white,fontSize:19,fontWeight:FontWeight.w900)),",1)

# Helper widgets before existing section helper.
anchor="  Widget _bolumBasligi(String yazi)=>Padding("
helpers=r'''  Widget _finalUstUretIkon(IconData ikon,VoidCallback tikla,{bool vurgu=false})=>Padding(
    padding:const EdgeInsets.only(left:8),
    child:InkWell(
      onTap:yukleniyor?null:tikla,
      borderRadius:BorderRadius.circular(24),
      child:Container(
        width:48,height:48,
        decoration:BoxDecoration(
          gradient:vurgu?const LinearGradient(colors:[Color(0xFF1BB9F2),Color(0xFF913EFF)]):null,
          color:vurgu?null:const Color(0xFFF7F8FB),
          shape:BoxShape.circle,
          border:Border.all(color:const Color(0xFFE7E9F0)),
        ),
        child:Icon(ikon,color:vurgu?Colors.white:Colors.black,size:25),
      ),
    ),
  );

  Widget _finalUretKart(IconData ikon,String baslik,String alt,VoidCallback tikla)=>Expanded(
    child:InkWell(
      onTap:yukleniyor?null:tikla,
      borderRadius:BorderRadius.circular(18),
      child:Container(
        height:170,
        margin:const EdgeInsets.symmetric(horizontal:4),
        padding:const EdgeInsets.all(13),
        decoration:BoxDecoration(
          borderRadius:BorderRadius.circular(18),
          gradient:const LinearGradient(begin:Alignment.topCenter,end:Alignment.bottomCenter,colors:[Color(0xFF616B7A),Color(0xFF202536)]),
        ),
        child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
          const Spacer(),
          CircleAvatar(radius:22,backgroundColor:Colors.white,child:Icon(ikon,color:Colors.black,size:23)),
          const SizedBox(height:10),
          Text(baslik,style:const TextStyle(color:Colors.white,fontSize:17,fontWeight:FontWeight.w900)),
          const SizedBox(height:3),
          Text(alt,style:const TextStyle(color:Colors.white70,fontSize:11.5,height:1.2)),
        ]),
      ),
    ),
  );

  Widget _finalUretSekme(IconData ikon,String yazi,bool secili,VoidCallback tikla)=>InkWell(
    onTap:yukleniyor?null:tikla,
    borderRadius:BorderRadius.circular(15),
    child:Container(
      padding:const EdgeInsets.symmetric(vertical:11,horizontal:4),
      decoration:BoxDecoration(gradient:secili?const LinearGradient(colors:[Color(0xFF9B3EFF),Color(0xFF3064FF)]):null,borderRadius:BorderRadius.circular(15)),
      child:Row(mainAxisAlignment:MainAxisAlignment.center,children:[
        Icon(ikon,size:18,color:secili?Colors.white:Colors.black),
        const SizedBox(width:4),
        Flexible(child:Text(yazi,maxLines:1,overflow:TextOverflow.ellipsis,style:TextStyle(color:secili?Colors.white:Colors.black,fontWeight:FontWeight.w800,fontSize:11))),
      ]),
    ),
  );

  Widget _finalUretArac(IconData ikon,String yazi,VoidCallback tikla)=>Expanded(
    child:InkWell(
      onTap:yukleniyor?null:tikla,
      borderRadius:BorderRadius.circular(15),
      child:Container(
        margin:const EdgeInsets.symmetric(horizontal:3),
        padding:const EdgeInsets.symmetric(vertical:11),
        decoration:BoxDecoration(color:const Color(0xFFF7F5FF),borderRadius:BorderRadius.circular(15)),
        child:Column(children:[Icon(ikon,color:mor,size:22),const SizedBox(height:4),Text(yazi,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Color(0xFF555C70),fontSize:10.5,fontWeight:FontWeight.w700))]),
      ),
    ),
  );

'''
if anchor not in src: raise SystemExit("create helper anchor missing")
src=src.replace(anchor,helpers+anchor,1)

p.write_text(src,encoding="utf-8")
print("Build 399 Create reference structure applied.")
