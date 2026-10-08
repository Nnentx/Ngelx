#!/usr/bin/env python3
"""Build 411: approved cover and coverless profile layouts, preserving all existing actions.
Runs AFTER Build 409 patches. Zero Firestore rules changes, no forced migration.
"""
from pathlib import Path

p=Path("app/lib/main.dart")
src=p.read_text(encoding="utf-8")

def one(s,old,new,label):
    count=s.count(old)
    if count!=1:raise SystemExit(f"{label}: expected one anchor, found {count}")
    return s.replace(old,new,1)

def in_class(s,begin,end,fn):
    a=s.index(begin)
    b=s.index(end,a+len(begin))
    return s[:a]+fn(s[a:b])+s[b:]

def owner(s):
    s=one(s,"  String kapakUrl = '';","  String kapakUrl = '';\n  String profilGorunumu = '';","owner mode field")
    s=one(s,"kapakUrl = (veri['coverPhotoUrl'] ?? '').toString();",
      "kapakUrl = (veri['coverPhotoUrl'] ?? '').toString();\n           profilGorunumu = (veri['profileViewMode'] ?? '').toString();","owner load mode")
    # Retain the old profile editor for compatibility; the prominent Edit action
    # opens the approved full-screen editor and asks the old owner state to reload.
    start="  Future<void> duzenle() async {"
    inject="""  Future<void> _onayliProfilDuzenleAc()async{
    final user=aktifKullanici;
    if(user==null||user.isAnonymous){await duzenle();return;}
    final degisti=await Navigator.push<bool>(context,MaterialPageRoute(builder:(_)=>
      NgelXOnayliProfilDuzenlePage(
        uid:user.uid,
        ilkAd:ad,
        ilkKullanici:kullanici,
        ilkBio:bio,
        ilkKonum:konum=='Konum eklenmedi'?'':konum,
        katilma:katilim,
        onKapak:kapakFotografiDuzenle,
        onFoto:fotografYukle,
        onTanitim:tanitimVideosuYukle,
      ),
    ));
    // Media and cover removal save immediately, even when the editor is closed without form Save.
    if(mounted)await profiliGetir();
  }

"""
    s=one(s,start,inject+start,"owner editor navigation")
    s=one(s,"onPressed:aktifKullanici?.isAnonymous==true?()async{await FirebaseAuth.instance.signOut();if(context.mounted)Navigator.of(context).pushAndRemoveUntil(MaterialPageRoute(builder:(_)=>const KayitPage()),(_)=>false);}:duzenle,",
      "onPressed:aktifKullanici?.isAnonymous==true?()async{await FirebaseAuth.instance.signOut();if(context.mounted)Navigator.of(context).pushAndRemoveUntil(MaterialPageRoute(builder:(_)=>const KayitPage()),(_)=>false);}:_onayliProfilDuzenleAc,",
      "owner edit action")
    # Only replace the top of the owner's profile; all lower widgets keep
    # their existing functionality: stats, shortcut actions, stories and grids.
    import re
    s,count=re.subn(
      r"(?m)^([ \t]*)SizedBox\(\s*\n[ \t]*height:265,\s*\n[ \t]*child:Stack\(clipBehavior:Clip\.none,children:\[",
      lambda m:m.group(1)+"if(profilGorunumu=='coverless'||kapakUrl.isEmpty)\n"+m.group(1)+"  _onayliKapaksizBaslik()\n"+m.group(1)+"else SizedBox(\n"+m.group(1)+"  height:265,\n"+m.group(1)+"  child:Stack(clipBehavior:Clip.none,children:[",
      s
    )
    if count!=1:raise SystemExit(f"owner alternate coverless header: expected one, found {count}")
    # Avoid duplicating real data and media widgets. The coverless avatar stays
    # centered; tapping avatar/story and editing photo use existing callbacks.
    helper="""  Widget _onayliKapaksizBaslik()=>Column(
    mainAxisSize:MainAxisSize.min,
    children:[
      Row(mainAxisAlignment:MainAxisAlignment.end,children:[
        _profilKapakIkon(Icons.search_rounded,()=>aktifKullanici==null?null:Navigator.push(context,MaterialPageRoute(builder:(_)=>ProfilAramaPage(uid:aktifKullanici!.uid)))),
        _profilKapakIkon(Icons.more_horiz_rounded,()=>_profilDahaFazlaAc()),
        _profilKapakIkon(Icons.notifications_none_rounded,()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const AktivitePage()))),
        _profilKapakIkon(Icons.settings_outlined,()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const AyarlarV258Page()))),
      ]),
      const SizedBox(height:12),
      SizedBox(height:174,width:210,child:Stack(alignment:Alignment.center,children:[
        Positioned(left:8,top:50,child:Container(width:58,height:58,decoration:const BoxDecoration(color:Color(0xFFF4E9FF),shape:BoxShape.circle))),
        Positioned(right:7,top:10,child:Container(width:76,height:76,decoration:const BoxDecoration(color:Color(0xFFF4ECFF),shape:BoxShape.circle))),
        const Positioned(left:12,top:14,child:Icon(Icons.auto_awesome_rounded,color:Color(0xFFAD7DFB),size:17)),
        const Positioned(right:0,bottom:38,child:Icon(Icons.auto_awesome_rounded,color:Color(0xFFAD7DFB),size:14)),
        Container(padding:const EdgeInsets.all(4),
          decoration:BoxDecoration(shape:BoxShape.circle,border:Border.all(color:const Color(0xFF8B5CF6),width:2)),
          child:GestureDetector(
            behavior:HitTestBehavior.opaque,
            onTap:hikayeyiAc,onLongPress:fotografYukle,
            child:NgelXHikayeliAvatar(uid:aktifKullanici?.uid??'',fotoUrl:fotoUrl,kullanici:kullanici,radius:70,etkin:false,hikayeYoksaTikla:fotografYukle),
          ),
        ),
        Positioned(right:21,bottom:7,child:InkWell(
          onTap:fotografYukle,
          child:Container(padding:const EdgeInsets.all(9),decoration:const BoxDecoration(color:Colors.white,shape:BoxShape.circle,boxShadow:[BoxShadow(color:Colors.black12,blurRadius:9)]),
            child:const Icon(Icons.photo_camera_rounded,color:Colors.black87,size:21)),
        )),
      ])),
      const SizedBox(height:6),
      Text(ad,textAlign:TextAlign.center,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(fontSize:27,color:Colors.black,fontWeight:FontWeight.w900)),
      const SizedBox(height:4),
      Text(kullanici,textAlign:TextAlign.center,style:const TextStyle(color:Colors.black54,fontSize:15)),
      const SizedBox(height:10),
    ],
  );

"""
    s=one(s,"  Widget _profilKapakIkon(IconData ikon,VoidCallback? tikla)=>",helper+"  Widget _profilKapakIkon(IconData ikon,VoidCallback? tikla)=>","insert owner coverless header helper")
    return s

src=in_class(src,"class _ProfilPageState extends State<ProfilPage>","\nclass _ProfilEtkilesimRozeti",owner)

def other(s):
    s=one(s,"final foto = (v['photoUrl'] ?? '').toString();",
      """           final foto = (v['photoUrl'] ?? '').toString();
           final profilKapak=(v['coverPhotoUrl']??'').toString();
           final gorunum=(v['profileViewMode']??'').toString();
           final kapaksiz=gorunum=='coverless'||profilKapak.isEmpty;
           final kapakKonum=((v['coverPhotoY'] as num?)?.toDouble()??0).clamp(-1.0,1.0);""",
      "other user cover fields")
    s=one(s,"Center(child:Stack(clipBehavior:Clip.none,alignment:Alignment.center,children:[",
      """if(!kapaksiz)...[
                 ClipRRect(
                   borderRadius:BorderRadius.circular(22),
                   child:SizedBox(height:165,width:double.infinity,
                     child:Image(image:NgelXAgImageProvider(profilKapak),fit:BoxFit.cover,alignment:Alignment(0,kapakKonum),gaplessPlayback:true),
                   ),
                 ),
                 const SizedBox(height:10),
               ],
               Center(child:Stack(clipBehavior:Clip.none,alignment:Alignment.center,children:[
                 if(kapaksiz)...[
                   Positioned(left:-18,top:4,child:Container(width:68,height:68,decoration:const BoxDecoration(color:Color(0xFFF2EAFF),shape:BoxShape.circle))),
                   Positioned(right:-19,bottom:14,child:Container(width:48,height:48,decoration:const BoxDecoration(color:Color(0xFFF6F0FF),shape:BoxShape.circle))),
                 ],""",
      "visitor cover/coverless header")
    # Approved order: profile identity, four counters, relationship actions,
    # introduction media, then post sections. Keep the exact original widget
    # with its playback logic; only move its position in the ListView.
    import re
    intro_pat=r"(?m)^[ \t]*if\(\(v\['introVideoUrl'\]\?\?''\)\.toString\(\)\.isNotEmpty\) \.\.\.\[\s*\n[ \t]*const SizedBox\(height:14\),\s*\n[ \t]*ProfilTanitimVideoKarti\(url:\(v\['introVideoUrl'\]\?\?''\)\.toString\(\)\),\s*\n[ \t]*\],\s*\n"
    s,n=re.subn(intro_pat,"",s)
    if n!=1:raise SystemExit(f"move visitor intro from original area: expected 1, found {n}")
    insert_pat=r"(?m)^([ \t]*)const SizedBox\(height: 20\),\s*\n[ \t]*if \(!erisimVar\)"
    def put_intro(m):
        indent=m.group(1)
        return (
           indent+"if((v['introVideoUrl']??'').toString().isNotEmpty) ...[\n"
           +indent+"  const SizedBox(height:14),\n"
           +indent+"  ProfilTanitimVideoKarti(url:(v['introVideoUrl']??'').toString()),\n"
           +indent+"],\n"
           +indent+"const SizedBox(height: 20),\n"
           +indent+"if (!erisimVar)"
        )
    s,n=re.subn(insert_pat,put_intro,s)
    if n!=1:raise SystemExit(f"move visitor intro after actions: expected 1, found {n}")
    return s
src=in_class(src,"class _KullaniciProfilPageState extends State<KullaniciProfilPage>","\nclass NgelXVideoKapakOnizleme",other)

p.write_text(src,encoding="utf-8")
print("Build 411 profile appearance applied: coverless own profile, cover/photo on visitor profile, existing functions and permissions retained.")
