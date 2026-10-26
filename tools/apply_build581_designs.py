"""Apply approved visual UI and instant Ludo invitation delivery to Build580.
Requires the exact Build580 assembled source; never overwrites the historical app tree.
"""
from pathlib import Path
import hashlib

root=Path(__file__).resolve().parents[1]
lib=root/'app/lib'
ludo=lib/'build565_ludo.dart'
main=lib/'main.dart'
s=ludo.read_text(encoding='utf-8')
m=main.read_text(encoding='utf-8')
if 'class Ngelx581StatsScreen' in s:
    assert 'directInvite581' in m and 'version: 1.0.351+581' in (root/'app/pubspec.yaml').read_text()
    print('Build581 already applied')
    raise SystemExit(0)
assert hashlib.sha256(ludo.read_bytes()).hexdigest()=='bc9033992c0dbc82ecc2b2329a24fdae31afa081db65038c556d150ffc3cbe84', 'Wrong Build580 Ludo input'
assert hashlib.sha256(main.read_bytes()).hexdigest()=='a3876511da8a32d8fbc1f4f86aa819243805f6fede4221e236e11cdfdbf2f499', 'Wrong Build580 main input'

def one(data,old,new):
    count=data.count(old)
    assert count==1,(count,old[:130])
    return data.replace(old,new,1)

# Keep the original room creation, validation, transport, rewards and navigation logic.
start=s.index(' Future<void> _myStats575()async{')
end=s.index(' Future<void> _claim575(String action)async{',start)
s=s[:start]+""" Future<void> _myStats575()async{
  try{
   final stats=await (widget.request??ngelx565LudoRequest)({'action':'wallet'});
   if(!mounted)return;
   await Navigator.push(context,MaterialPageRoute(builder:(_)=>Ngelx581StatsScreen(stats:stats)));
  }catch(e){if(mounted)setState(()=>giftMessage575='İstatistikler alınamadı: $e');}
 }
"""+s[end:]
a=s.index(' Widget option(String title,String sub,bool selected,VoidCallback tap,')
b=s.index(' @override Widget build(BuildContext context)=>Theme(',a)
s=s[:a]+""" Widget option(String title,String sub,bool selected,VoidCallback tap,{IconData? icon})=>Expanded(child:InkWell(
  onTap:busy?null:tap,borderRadius:BorderRadius.circular(18),
  child:AnimatedContainer(duration:const Duration(milliseconds:200),
   padding:const EdgeInsets.symmetric(vertical:14,horizontal:5),
   decoration:BoxDecoration(borderRadius:BorderRadius.circular(18),
    gradient:LinearGradient(begin:Alignment.topCenter,end:Alignment.bottomCenter,
     colors:selected?[const Color(0xFF7EBBFF),const Color(0xFF4561E9)]:[const Color(0xFF6064BD),const Color(0xFF514399)]),
    border:Border.all(color:selected?const Color(0xFFFFD75B):const Color(0xFF8D84D4),width:selected?2.5:1),
    boxShadow:const [BoxShadow(color:Color(0x33000000),blurRadius:8,offset:Offset(0,4))]),
   child:Column(mainAxisAlignment:MainAxisAlignment.center,children:[
    if(icon!=null)Icon(icon,color:selected?const Color(0xFFFFDB62):Colors.white70,size:27),
    const SizedBox(height:5),
    Text(title,maxLines:1,overflow:TextOverflow.ellipsis,textAlign:TextAlign.center,style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w900,fontSize:14)),
    Text(sub,maxLines:2,overflow:TextOverflow.ellipsis,textAlign:TextAlign.center,style:const TextStyle(color:Color(0xFFD7D8FC),fontSize:10)),
    const SizedBox(height:3),Icon(selected?Icons.check_circle_rounded:Icons.radio_button_unchecked_rounded,
      color:selected?const Color(0xFFFFD75B):const Color(0xFF979BDE),size:18),
   ]))));
"""+s[b:]

# Restrict lobby composition changes to the lobby class only.
a=s.index('class _Ngelx565LudoLobbyState')
b=s.index('class Ngelx565LudoRoom extends StatefulWidget',a)
head,tail=s[:a],s[b:]
lobby=s[a:b]
lobby=one(lobby,'body:_LudoBackdrop567(child:Padding(','body:Container(decoration:const BoxDecoration(gradient:LinearGradient(begin:Alignment.topCenter,end:Alignment.bottomCenter,colors:[Color(0xFF081D62),Color(0xFF192C87),Color(0xFF0A2367)])),child:Padding(')
lobby=one(lobby,'padding:const EdgeInsets.fromLTRB(24,14,24,28)','padding:const EdgeInsets.fromLTRB(16,12,16,30)')
a1=lobby.index("  const Center(child:Text('LUDO'")
b1=lobby.index("  const Text('Nasıl oynamak istersin?'",a1)
lobby=lobby[:a1]+"""  const Ngelx581Hero(),const SizedBox(height:14),
  Row(children:[
   Expanded(child:Ngelx581QuickAction(actionKey:const ValueKey('ludo-daily-gift'),label:'Günlük hediye',icon:Icons.card_giftcard_rounded,action:busy||giftBusy575?null:()=>_claim575('daily_reward'))),
   const SizedBox(width:5),
   Expanded(child:Ngelx581QuickAction(actionKey:const ValueKey('ludo-timed-chest'),label:'Ödül sandığı',icon:Icons.inventory_2_rounded,action:busy||giftBusy575?null:()=>_claim575('chest_reward'))),
   const SizedBox(width:5),
   Expanded(child:Ngelx581QuickAction(actionKey:const ValueKey('ludo-profile-stats'),label:'Puanlarım',icon:Icons.bar_chart_rounded,action:busy?null:_myStats575)),
  ]),
  if(giftMessage575.isNotEmpty)Padding(padding:const EdgeInsets.only(top:8),child:Text(giftMessage575,textAlign:TextAlign.center,style:const TextStyle(color:Color(0xFFFFE28D),fontWeight:FontWeight.w700,fontSize:12))),
  const SizedBox(height:20),
"""+lobby[b1:]
lobby=one(lobby,"const Text('Nasıl oynamak istersin?',textAlign:TextAlign.center","const Text('Nasıl oynamak istersin?',textAlign:TextAlign.left")
lobby=one(lobby,"const Text('Oyun modunu seç',textAlign:TextAlign.center","const Text('Oyun modu',textAlign:TextAlign.left")
lobby=one(lobby,"const Text('Oyuncuları seç',textAlign:TextAlign.center","const Text('Oyuncu sayısı',textAlign:TextAlign.left")
# Build580 already contains the corrected early-start explanation.
lobby=one(lobby,"play=='random'?'Rakip bul':'Oda oluştur',gold:true","play=='random'?'Rakip bul':'Devam et',gold:true")
lobby=one(lobby,"colors:[Color(0xFF7B67C2),Color(0xFF63439F)]","colors:[Color(0xFF4240A3),Color(0xFF352A85)]")
lobby=one(lobby,"border:Border.all(color:const Color(0xFFAB98EE),width:1.5)","border:Border.all(color:const Color(0xFF8E74E9),width:1.5)")
s=head+lobby+tail

# Replace the bland sender photo banner on the invite with the approved Ludo art.
a=s.index('     SizedBox(height:158,child:photo.isNotEmpty?')
b=s.index('     Padding(padding:const EdgeInsets.fromLTRB(14,14,14,12)',a)
s=s[:a]+'     const SizedBox(height:158,child:Ngelx581Hero()),\n'+s[b:]
s+='\n'+(root/'tools/build581_visuals.dart').read_text(encoding='utf-8')

# Existing chats have complete send, permission, request, offline-queue and notification
# flows. Reuse them instead of inserting Firestore messages outside the trusted path.
s=one(s,"GrupSohbetPage(chatId:target.id,ad:target.name,foto:target.photo,draft565:draft)","GrupSohbetPage(chatId:target.id,ad:target.name,foto:target.photo,directInvite581:draft)")
s=one(s,"SohbetPage(chatId:target.id,digerUid:target.other,ad:target.name,foto:target.photo,draft565:draft)","SohbetPage(chatId:target.id,digerUid:target.other,ad:target.name,foto:target.photo,directInvite581:draft)")

# Modify only the two intended chat page classes.
start=m.index('class GrupSohbetPage extends StatefulWidget')
middle=m.index('class SohbetPage extends StatefulWidget',start)
before,group,private=m[:start],m[start:middle],m[middle:]
group=one(group,'final String draft565;','final String draft565;final String directInvite581;')
group=one(group,"this.joinOnOpen542=false,this.draft565=''", "this.joinOnOpen542=false,this.draft565='',this.directInvite581=''")
group=one(group,"if(widget.draft565.isNotEmpty){mesaj.text=widget.draft565;mesaj.selection=TextSelection.collapsed(offset:mesaj.text.length);}",
 """if(widget.draft565.isNotEmpty){mesaj.text=widget.draft565;mesaj.selection=TextSelection.collapsed(offset:mesaj.text.length);}
    if(widget.directInvite581.isNotEmpty)WidgetsBinding.instance.addPostFrameCallback((_){
      if(mounted)unawaited(gonder(directInvite581:widget.directInvite581));
    });""")
group=one(group,'Future<void> gonder()async{\n    var t=mesaj.text.trim();','Future<void> gonder({String directInvite581=\'\'})async{\n    var t=directInvite581.isNotEmpty?directInvite581:mesaj.text.trim();')
group=one(group,'mesaj.clear();etiketlenenUidler.clear();','if(directInvite581.isEmpty)mesaj.clear();etiketlenenUidler.clear();')

private=one(private,"final String draft565;final bool aktifAramadanAcildi;","final String draft565,directInvite581;final bool aktifAramadanAcildi;")
private=one(private,"this.aktifAramadanAcildi=false,this.draft565=''", "this.aktifAramadanAcildi=false,this.draft565='',this.directInvite581=''")
private=one(private,"if(widget.draft565.isNotEmpty){mesaj.text=widget.draft565;mesaj.selection=TextSelection.collapsed(offset:mesaj.text.length);}",
 """if(widget.draft565.isNotEmpty){mesaj.text=widget.draft565;mesaj.selection=TextSelection.collapsed(offset:mesaj.text.length);}
    if(widget.directInvite581.isNotEmpty)WidgetsBinding.instance.addPostFrameCallback((_){
      if(mounted)unawaited(gonder(directInvite581:widget.directInvite581));
    });""")
private=one(private,'Future<void> gonder() async {\n    final hamMetin=mesaj.text.trim();','Future<void> gonder({String directInvite581=\'\'}) async {\n    final hamMetin=directInvite581.isNotEmpty?directInvite581:mesaj.text.trim();')
private=one(private,'    mesaj.clear();\n    sonaGit(zorla:true);','    if(directInvite581.isEmpty)mesaj.clear();\n    sonaGit(zorla:true);')
assert private.count('if(mesaj.text.isEmpty){')==2
private=private.replace('if(mesaj.text.isEmpty){','if(directInvite581.isEmpty&&mesaj.text.isEmpty){',2)

m=before+group+private
ludo.write_text(s,encoding='utf-8')
main.write_text(m,encoding='utf-8')
pub=root/'app/pubspec.yaml'
v=pub.read_text(encoding='utf-8')
assert 'version: 1.0.350+580' in v
pub.write_text(v.replace('version: 1.0.350+580','version: 1.0.351+581',1),encoding='utf-8')
print('Build581: lobby, statistics, instant invitations applied')
