from pathlib import Path
import re

MAIN = Path("app/lib/main.dart")
PUBSPEC = Path("app/pubspec.yaml")
s = MAIN.read_text(encoding="utf-8")
changes = []

def replace_once(old: str, new: str, label: str, required: bool = True):
    global s
    n = s.count(old)
    if n == 0:
        if required:
            raise SystemExit(f"[V58] target missing: {label}")
        return
    if n != 1 and required:
        raise SystemExit(f"[V58] expected one target for {label}, got {n}")
    s = s.replace(old, new, 1)
    changes.append(label)

# 1) Private nickname crash: avoid disposing a TextEditingController while the
# dialog route/TextField is still being deactivated.
old_alias = """  Future<void> takmaAd(BuildContext context)async{final me=FirebaseAuth.instance.currentUser?.uid;if(me==null)return;final chat=await FirebaseFirestore.instance.collection('chats').doc(chatId).get(),c=TextEditingController(text:(chat.data()?['nicknames']?[me]??'').toString());if(!context.mounted)return;final sonuc=await showDialog<String>(context:context,builder:(x)=>AlertDialog(backgroundColor:Colors.white,title:const Text('Takma ad'),content:TextField(controller:c,maxLength:30,decoration:const InputDecoration(hintText:'Bu sohbette görünecek ad')),actions:[TextButton(onPressed:()=>Navigator.pop(x),child:const Text('Vazgeç')),FilledButton(onPressed:()=>Navigator.pop(x,c.text.trim()),child:const Text('Kaydet'))]));c.dispose();if(sonuc!=null)await FirebaseFirestore.instance.collection('chats').doc(chatId).update({'nicknames.$me':sonuc});}"""
new_alias = """  Future<void> takmaAd(BuildContext context)async{
    final me=FirebaseAuth.instance.currentUser?.uid;
    if(me==null)return;
    final chat=await FirebaseFirestore.instance.collection('chats').doc(chatId).get();
    if(!context.mounted)return;
    var taslak=(chat.data()?['nicknames']?[me]??'').toString();
    final sonuc=await showDialog<String>(
      context:context,
      builder:(x)=>AlertDialog(
        backgroundColor:Colors.white,
        title:const Text('Takma ad'),
        content:TextFormField(
          initialValue:taslak,
          autofocus:true,
          maxLength:30,
          onChanged:(v)=>taslak=v,
          decoration:const InputDecoration(hintText:'Bu sohbette görünecek ad'),
        ),
        actions:[
          TextButton(
            onPressed:(){FocusScope.of(x).unfocus();Navigator.of(x).pop();},
            child:const Text('Vazgeç'),
          ),
          FilledButton(
            onPressed:(){FocusScope.of(x).unfocus();Navigator.of(x).pop(taslak.trim());},
            child:const Text('Kaydet'),
          ),
        ],
      ),
    );
    if(sonuc==null||!context.mounted)return;
    await FirebaseFirestore.instance.collection('chats').doc(chatId).set({
      'nicknames.$me':sonuc.isEmpty?FieldValue.delete():sonuc,
      'updatedAt':FieldValue.serverTimestamp(),
    },SetOptions(merge:true));
  }"""
replace_once(old_alias, new_alias, "private nickname crash")

# 2) Founder counts as a manager everywhere in group info and group posting.
replace_once(
"""          final yoneticiler=List<String>.from(v['admins']??const[]);
          final yonetici=yoneticiler.contains(ben);
          final duzenleyebilir=yonetici||v['onlyAdminsCanEditGroup']!=true;""",
"""          final yoneticiler=List<String>.from(v['admins']??const[]);
          final kurucu=(v['createdBy']??'').toString();
          final yonetici=yoneticiler.contains(ben)||kurucu==ben;
          final duzenleyebilir=yonetici;""",
"group manager/owner gate",
)

replace_once(
"""    final yoneticiler=List<String>.from(v['admins']??const[]);
    if(!uyeler.contains(ben)){""",
"""    final yoneticiler=List<String>.from(v['admins']??const[]);
    final kurucu=(v['createdBy']??'').toString();
    final yonetici=yoneticiler.contains(ben)||kurucu==ben;
    if(!uyeler.contains(ben)){""",
"group sender owner role",
)
replace_once(
"""    if(v['onlyAdminsCanPost']==true&&!yoneticiler.contains(ben)){""",
"""    if(v['onlyAdminsCanPost']==true&&!yonetici){""",
"group sender admin-only permission",
)

# 3) Adding/removing/invite-request management is admin/founder only.
replace_once(
"""    final gv=grup.data()??<String,dynamic>{};
    final yonetici=List<String>.from(gv['admins']??const[]).contains(me);
    if(gv['onlyAdminsCanAddMembers']==true&&!yonetici){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Bu grupta yalnızca yöneticiler üye ekleyebilir.')));
      return;
    }""",
"""    final gv=grup.data()??<String,dynamic>{};
    final yonetici=List<String>.from(gv['admins']??const[]).contains(me)||(gv['createdBy']??'').toString()==me;
    if(!yonetici){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Yalnızca grup kurucusu ve yöneticiler üye ekleyebilir.')));
      return;
    }""",
"group add member authorization",
)

replace_once(
"""                    Expanded(child:_grupKisayol(Icons.person_add_alt_1_rounded,'Ekle',uyeler.length>=60?null:()=>uyeEkle(uyeler))),""",
"""                    Expanded(child:_grupKisayol(Icons.person_add_alt_1_rounded,'Ekle',!yonetici||uyeler.length>=60?null:()=>uyeEkle(uyeler))),""",
"group add button gate",
)

replace_once(
"""                        onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>GrupKatilmaIstekleriPage(chatId:widget.chatId))),""",
"""                        onTap:yonetici?()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>GrupKatilmaIstekleriPage(chatId:widget.chatId))):null,""",
"group invite/request row gate",
)

replace_once(
"""  Future<void> ayarDegistir(String alan,bool deger)async{
    await ref.set({alan:deger,'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));""",
"""  Future<void> ayarDegistir(String alan,bool deger)async{
    if(alan=='onlyAdminsCanAddMembers')deger=true;
    await ref.set({alan:deger,'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));""",
"force add-member admin policy",
)

replace_once(
"""  })async{
    final secim=await showModalBottomSheet<bool>(""",
"""  })async{
    if(alan=='onlyAdminsCanAddMembers'){
      await ayarDegistir(alan,true);
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Üye ekleme yalnızca kurucu ve yöneticilere açıktır.')));
      return;
    }
    final secim=await showModalBottomSheet<bool>(""",
"lock add-member policy picker",
)

# 4) System log must say WHO removed a member.
s = s.replace(
"""        await sistemMesaji('$isim gruptan çıkarıldı.');""",
"""        final yapanAd=await ngelxCurrentDisplayName();
        await sistemMesaji('$yapanAd, $isim adlı üyeyi gruptan çıkardı.',action:'member_removed',targetUids:[id]);""",
)
if "member_removed" in s:
    changes.append("group removal actor log")

s = s.replace(
"""      await _sistemMesaji(isim+' gruptan çıkarıldı.');""",
"""      final yapanAd=await ngelxCurrentDisplayName();
      await _sistemMesaji(yapanAd+', '+isim+' adlı üyeyi gruptan çıkardı.');""",
)
changes.append("member list removal actor log")

# 5) Group background is shared and only founder/admin can change it.
replace_once(
"""  Future<void> grupArkaPlanMenusu()async{
    final me=uid;if(me==null)return;
    final d=await chatRef.get();""",
"""  Future<void> _grupArkaPlanOlayi(String eylem)async{
    final me=uid;if(me==null)return;
    final ad=await ngelxCurrentDisplayName();
    try{
      await chatRef.collection('messages').add({
        'senderId':me,'actorUid':me,'type':'system','systemAction':'background_changed',
        'text':ad+' '+eylem,'createdAt':FieldValue.serverTimestamp(),
      });
      await chatRef.set({'lastMessage':ad+' '+eylem,'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
    }catch(_){}
  }

  Future<void> grupArkaPlanMenusu()async{
    final me=uid;if(me==null)return;
    if(!await ngelxCanManageGroup(widget.chatId,me)){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Grup arka planını yalnızca kurucu ve yöneticiler değiştirebilir.')));
      return;
    }
    final d=await chatRef.get();""",
"group background manager gate",
)

s = s.replace("(v['backgroundUrl_$me']??'').toString()", "(v['backgroundUrl']??v['backgroundUrl_$me']??'').toString()", 1)
s = s.replace("(v['backgroundOpacity_$me'] is num?(v['backgroundOpacity_$me'] as num).toDouble():.35)", "(v['backgroundOpacity'] is num?(v['backgroundOpacity'] as num).toDouble():(v['backgroundOpacity_$me'] is num?(v['backgroundOpacity_$me'] as num).toDouble():.35))", 1)
s = s.replace("await chatRef.set({'backgroundOpacity_$me':oran},SetOptions(merge:true));\n      return;", "await chatRef.set({'backgroundOpacity':oran},SetOptions(merge:true));\n      await _grupArkaPlanOlayi('grup arka plan görünürlüğünü değiştirdi.');\n      return;", 1)
s = s.replace("await chatRef.set({'backgroundUrl_$me':''},SetOptions(merge:true));\n      return;", "await chatRef.set({'backgroundUrl':'','backgroundOpacity':FieldValue.delete()},SetOptions(merge:true));\n      await _grupArkaPlanOlayi('grup arka planını kaldırdı.');\n      return;", 1)
s = s.replace("ImagePicker().pickImage(source:ImageSource.gallery,imageQuality:80,maxWidth:1440)", "ImagePicker().pickImage(source:ImageSource.gallery,imageQuality:68,maxWidth:1080)", 1)
s = s.replace("await chatRef.set({'backgroundUrl_$me':url,'backgroundOpacity_$me':.35},SetOptions(merge:true));", "await chatRef.set({'backgroundUrl':url,'backgroundOpacity':.32},SetOptions(merge:true));\n      await _grupArkaPlanOlayi('grup arka planını değiştirdi.');", 1)
s = s.replace("arkaPlanUrl=(tv['backgroundUrl_$uid']??'').toString(),", "arkaPlanUrl=(tv['backgroundUrl']??tv['backgroundUrl_$uid']??'').toString(),", 1)
s = s.replace("final opaklik=(tv['backgroundOpacity_$uid'] is num?(tv['backgroundOpacity_$uid'] as num).toDouble():.26).clamp(.10,.55).toDouble();", "final opaklik=(tv['backgroundOpacity'] is num?(tv['backgroundOpacity'] as num).toDouble():(tv['backgroundOpacity_$uid'] is num?(tv['backgroundOpacity_$uid'] as num).toDouble():.26)).clamp(.10,.55).toDouble();", 1)
s = s.replace("DecorationImage(image:CachedNetworkImageProvider(arkaPlanUrl),fit:BoxFit.cover,opacity:opaklik)", "DecorationImage(image:ResizeImage(CachedNetworkImageProvider(arkaPlanUrl),width:1080),fit:BoxFit.cover,opacity:opaklik)", 1)
changes.append("shared manager-only group background + lower memory decode")

# Group info customize page: same shared fields and permission.
replace_once(
"""  Future<void> _arkaPlanSec()async{
    final uid=me;if(uid==null||yukleniyor)return;""",
"""  Future<void> _arkaPlanSistemMesaji(String eylem)async{
    final uid=me;if(uid==null)return;
    final ad=await ngelxCurrentDisplayName();
    try{
      await ref.collection('messages').add({
        'senderId':uid,'actorUid':uid,'type':'system','systemAction':'background_changed',
        'text':ad+' '+eylem,'createdAt':FieldValue.serverTimestamp(),
      });
      await ref.set({'lastMessage':ad+' '+eylem,'updatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
    }catch(_){}
  }

  Future<void> _arkaPlanSec()async{
    final uid=me;if(uid==null||yukleniyor)return;
    if(!await ngelxCanManageGroup(widget.chatId,uid)){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Grup arka planını yalnızca kurucu ve yöneticiler değiştirebilir.')));
      return;
    }""",
"group customize permission gate",
)

# These replacements are confined by their exact forms in GrupOzellestirPage.
s = s.replace("ImagePicker().pickImage(source:ImageSource.gallery,imageQuality:82,maxWidth:1440)", "ImagePicker().pickImage(source:ImageSource.gallery,imageQuality:68,maxWidth:1080)", 1)
s = s.replace("final eski=(onceki.data()?['backgroundUrl_'+uid]??'').toString();", "final eski=(onceki.data()?['backgroundUrl']??'').toString();", 1)
s = s.replace("await ref.set({'backgroundUrl_'+uid:url,'backgroundOpacity_'+uid:.35},SetOptions(merge:true));", "await ref.set({'backgroundUrl':url,'backgroundOpacity':.32},SetOptions(merge:true));\n      await _arkaPlanSistemMesaji('grup arka planını değiştirdi.');", 1)
s = s.replace(
"""  Future<void> _arkaPlanKaldir(String eski)async{
    final uid=me;if(uid==null)return;
    await ref.set({'backgroundUrl_'+uid:FieldValue.delete(),'backgroundOpacity_'+uid:FieldValue.delete()},SetOptions(merge:true));""",
"""  Future<void> _arkaPlanKaldir(String eski)async{
    final uid=me;if(uid==null)return;
    if(!await ngelxCanManageGroup(widget.chatId,uid)){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Grup arka planını yalnızca kurucu ve yöneticiler değiştirebilir.')));
      return;
    }
    await ref.set({'backgroundUrl':FieldValue.delete(),'backgroundOpacity':FieldValue.delete()},SetOptions(merge:true));
    await _arkaPlanSistemMesaji('grup arka planını kaldırdı.');""",
    1,
)
s = s.replace("final url=(v['backgroundUrl_'+uid]??'').toString();", "final url=(v['backgroundUrl']??v['backgroundUrl_'+uid]??'').toString();", 1)
s = s.replace("final opacity=(v['backgroundOpacity_'+uid] is num?(v['backgroundOpacity_'+uid] as num).toDouble():.35).clamp(.10,.55).toDouble();", "final opacity=(v['backgroundOpacity'] is num?(v['backgroundOpacity'] as num).toDouble():(v['backgroundOpacity_'+uid] is num?(v['backgroundOpacity_'+uid] as num).toDouble():.35)).clamp(.10,.55).toDouble();", 1)
s = s.replace("const Text('Grup sohbetinde yalnızca sana özel görünecek arka planı seç.'", "const Text('Grup arka planını yalnızca kurucu ve yöneticiler değiştirebilir.'", 1)
s = s.replace("DecorationImage(image:CachedNetworkImageProvider(url),fit:BoxFit.cover,opacity:opacity)", "DecorationImage(image:ResizeImage(CachedNetworkImageProvider(url),width:1080),fit:BoxFit.cover,opacity:opacity)", 1)
changes.append("group customize shared background")

# 6) Pinned-message three-dot menu must actually work.
replace_once(
"""                      const Icon(Icons.more_horiz_rounded,color:Color(0xFFA49BAB)),""",
"""                      PopupMenuButton<String>(
                        tooltip:'Mesaj işlemleri',
                        icon:const Icon(Icons.more_horiz_rounded,color:Color(0xFFA49BAB)),
                        onSelected:(sec)async{
                          if(sec!='unpin')return;
                          final chat=await FirebaseFirestore.instance.collection('chats').doc(chatId).get();
                          final data=chat.data()??<String,dynamic>{};
                          final me=FirebaseAuth.instance.currentUser?.uid;
                          final admins=List<String>.from(data['admins']??const[]);
                          final owner=(data['createdBy']??'').toString();
                          final onlyAdmins=data['onlyAdminsCanPin']!=false;
                          if(me==null||(onlyAdmins&&!admins.contains(me)&&owner!=me)){
                            if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Bu mesajı sabitlemeden kaldırma yetkin yok.')));
                            return;
                          }
                          await d.reference.set({'pinned':false,'pinnedAt':FieldValue.delete(),'pinnedBy':FieldValue.delete()},SetOptions(merge:true));
                        },
                        itemBuilder:(_)=>const [
                          PopupMenuItem<String>(value:'unpin',child:Row(children:[
                            Icon(Icons.push_pin_outlined,size:19),
                            SizedBox(width:9),
                            Text('Sabitlemeyi kaldır'),
                          ])),
                        ],
                      ),""",
"pinned message menu",
)

# 7) Make the sent/read label less cramped against the composer.
s = s.replace(
"padding:const EdgeInsets.only(top:1,right:7,bottom:2),",
"padding:const EdgeInsets.only(top:0,right:7,bottom:7),",
1,
)
changes.append("group sent label spacing")

# 8) Lower background upload size in any remaining group customize upload call.
# (Only targeted chat-backgrounds occurrences; no feed/photo quality changes.)
s = re.sub(
    r"(kind:'chat-backgrounds'[\s\S]{0,450}?)maxWidth:1440",
    lambda m: m.group(1) + "maxWidth:1080",
    s,
)

MAIN.write_text(s, encoding="utf-8")

# Version bump for the new test build.
p = PUBSPEC.read_text(encoding="utf-8")
p2, n = re.subn(r"(?m)^version:\s+\S+\s*$", "version: 1.0.58+277", p, count=1)
if n != 1:
    raise SystemExit("[V58] pubspec version line missing")
PUBSPEC.write_text(p2, encoding="utf-8")

print("[V58] patched:", ", ".join(changes))
print("[V58] version: 1.0.58+277")
