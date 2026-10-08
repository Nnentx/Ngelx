#!/usr/bin/env python3
"""NgelX Build 407 consolidated fixes, applied AFTER fully checked Build 406.
Priority 0: founder/admin approval is compulsory for ALL join-link requests.
Patches are exact-match and fail closed on source drift; do not delete user data.
"""
from pathlib import Path
import re

def rd(p): return Path(p).read_text(encoding="utf-8")
def wr(p,c): Path(p).write_text(c,encoding="utf-8")
def one(c,a,b,label):
    n=c.count(a)
    if n!=1: raise SystemExit(f"{label}: expected one anchor, found {n}: {a[:120]!r}")
    return c.replace(a,b,1)
def region(c,start,end,cb):
    a=c.index(start);b=c.index(end,a+len(start))
    return c[:a]+cb(c[a:b])+c[b:]

m=rd("app/lib/main.dart")
m=one(m,"defaultValue: '406'","defaultValue: '407'","build code")
m=one(m,"defaultValue: '1.0.182'","defaultValue: '1.0.183'","version")
pub=one(rd("app/pubspec.yaml"),"version: 1.0.182+406","version: 1.0.183+407","pubspec version")
wr("app/pubspec.yaml",pub)

# Founder/admin approval supersedes Build 406 invite autojoin. This also works with
# old Build 406 request documents after their status is reset to pending.
def patch_join(src):
    beginning=src.index("      final req=chat.collection('joinRequests').doc(me);")
    ending=src.index("    }on FirebaseException catch(e){",beginning)
    old=src[beginning:ending]
    if "'status':'autojoin'" not in old or "await chat.update({" not in old:
        raise SystemExit("group join code no longer matches Build 406 behavior")
    replacement="""      final req=chat.collection('joinRequests').doc(me);
      final once=await req.get().timeout(const Duration(seconds:8));
      if(once.exists&&(once.data()?['status']??'')=='pending'){
        if(mounted)ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content:Text('Katılma isteğin zaten kurucu/yönetici onayını bekliyor.')));
        return;
      }
      await req.set({
        'uid':me,
        'status':'pending',
        'inviteCode':invite,
        'createdAt':FieldValue.serverTimestamp(),
        'updatedAt':FieldValue.serverTimestamp(),
      },SetOptions(merge:true));
      // Pending requests are also visible to founder/admin from the joinRequests
      // collection. Notification delivery is best-effort, never a membership grant.
      try{
        final admins=List<String>.from(iv['admins']??const <String>[]);
        final profil=await FirebaseFirestore.instance.collection('users').doc(me).get()
          .timeout(const Duration(seconds:5));
        final pv=profil.data()??<String,dynamic>{};
        final senderName=(pv['displayName']??pv['username']??'Kullanıcı').toString();
        final photo=(pv['photoUrl']??'').toString();
        for(final adminId in admins.toSet().where((e)=>e.isNotEmpty&&e!=me).take(12)){
          await FirebaseFirestore.instance.collection('notifications').add({
            'type':'group_join_request','toUid':adminId,'fromUid':me,
            'chatId':chatId,'groupId':chatId,'groupName':ad,
            'senderName':senderName,'photoUrl':photo,
            'text':'$senderName $ad grubuna katılmak istiyor',
            'status':'pending','read':false,
            'createdAt':FieldValue.serverTimestamp(),
          });
        }
      }catch(_){/* join request is saved; admins can read their pending queue */}
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content:Text('Katılma isteğin kurucu veya yönetici onayına gönderildi.')));
"""
    src=src[:beginning]+replacement+src[ending:]
    return one(src,
       "'Geçerli davet bağlantısı veya kodu ile yönetici onayı beklemeden katılabilirsin. Üyelik sınırı ve grup güvenliği kuralları geçerlidir.'",
       "'Geçerli davet bağlantısıyla isteğin kurucu veya yöneticinin onayına gönderilir. Onaylanana kadar gruba katılamazsın.'",
       "group invite message")
m=region(m,"class _GrubaKatilPageState extends State<GrubaKatilPage>","\nclass ",patch_join)

# User-approved Akış header names. Backend tab keys and recommendation feed are unchanged.
m=one(m,"'followingTab': {'tr':'Takip'","'followingTab': {'tr':'Çevrem'","feed follows tab")
m=one(m,"'forYou': {'tr':'Sana Özel'","'forYou': {'tr':'Radar'","feed Radar tab")

# Seeking: do NOT submit one remote seek for each onPointerMove gesture.
# Retain immediate scrub thumb update; perform the seek once, on release.
needle=r"(?m)^[ \t]*unawaited\(kontrol\.seekTo\(Duration\(milliseconds:hedef\)\)\);\n(?=[ \t]*if\(mounted\)setState\(\(\)\{\}\);)"
m,count=re.subn(needle,"",m)
if count!=1:raise SystemExit(f"fast seek gesture anchor: {count}")

# Reduce multiple sticky snackbars without changing success payload or navigation.
needle="""      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content:Text(lt('Paylaşım yayınlandı ✅ Akışta ve profilinde görünecek.','Post published ✅ It will appear in your feed and profile.')),"""
replacement="""      ScaffoldMessenger.of(context).hideCurrentSnackBar();
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        duration:const Duration(seconds:3),
        behavior:SnackBarBehavior.floating,
        content:Text(lt('Paylaşım yayınlandı ✅','Post published ✅')),"""
m=one(m,needle,replacement,"Create snackbar lifetime")


# Keep existing Üret layout; make long labels scale without splitting mid-word.
m=one(m,
    "Text(baslik,style:const TextStyle(color:Colors.white,fontSize:17,fontWeight:FontWeight.w900))",
    "FittedBox(fit:BoxFit.scaleDown,alignment:Alignment.centerLeft,child:Text(baslik,maxLines:1,softWrap:false,style:const TextStyle(color:Colors.white,fontSize:17,fontWeight:FontWeight.w900)))",
    "Create card title fits one line")
m=one(m,
    "Text(alt,style:const TextStyle(color:Colors.white70,fontSize:11.5,height:1.2))",
    "FittedBox(fit:BoxFit.scaleDown,alignment:Alignment.centerLeft,child:Text(alt,maxLines:2,style:const TextStyle(color:Colors.white70,fontSize:11.5,height:1.2)))",
    "Create subtitle stays readable")
m=one(m,
    "Flexible(child:Text(yazi,maxLines:1,overflow:TextOverflow.ellipsis,style:TextStyle(color:secili?Colors.white:Colors.black,fontWeight:FontWeight.w800,fontSize:11)))",
    "Flexible(child:FittedBox(fit:BoxFit.scaleDown,child:Text(yazi,maxLines:1,softWrap:false,style:TextStyle(color:secili?Colors.white:Colors.black,fontWeight:FontWeight.w800,fontSize:11))))",
    "Create tabs no ellipsis")

# Search full multiword names (including Turkish characters) across video title,
# description, tags and uploader; de-duplicate the same Firestore post ID only.
old="bool eslesir(String metin) => metin.toLowerCase().split(RegExp(r'[^a-z0-9ığüşöç]+')).any((kelime) => kelime.startsWith(sorgu));"
new="""bool eslesir(String metin){
                   final kelimeler=metin.toLowerCase().split(RegExp(r'[^a-z0-9ığüşöç]+')).where((e)=>e.isNotEmpty).toList();
                   final aranan=sorgu.toLowerCase().split(RegExp(r'[^a-z0-9ığüşöç]+')).where((e)=>e.isNotEmpty).toList();
                   return aranan.isNotEmpty&&aranan.every((q)=>kelimeler.any((k)=>k.startsWith(q)));
                 }"""
m=one(m,old,new,"multiword search")
old="final icerikler = snap.data![1].docs.where((d) { final v=d.data(); return !engellenenler.contains((v['ownerId']??'').toString())&&v['type'] != 'story' && '${v['description'] ?? ''} ${v['username'] ?? ''}'.toLowerCase().contains(sorgu); }).toList();"
new="""final icerikler = snap.data![1].docs.where((d){
                   final v=d.data();
                   final gizlilik=(v['visibility']??v['privacy']??'public').toString().toLowerCase();
                   if(v['deleted']==true||v['isDeleted']==true||v['type']=='story'||gizlilik=='private')return false;
                   if(engellenenler.contains((v['ownerId']??'').toString()))return false;
                   return eslesir('${v['title']??''} ${v['description']??''} ${v['hashtags']??''} ${v['username']??''}');
                 }).toList()..sort((a,b){
                   int puan(Map<String,dynamic> v){
                     final q=sorgu.toLowerCase();
                     final ad=(v['title']??'').toString().toLowerCase();
                     final aciklama=(v['description']??'').toString().toLowerCase();
                     final etiket=(v['hashtags']??'').toString().toLowerCase();
                     return (ad.contains(q)?100:0)+(aciklama.contains(q)?50:0)+(etiket.contains(q)?20:0);
                   }
                   return puan(b.data()).compareTo(puan(a.data()));
                 });"""
m=one(m,old,new,"rank video search for the multiword topic")


# Fix BOTH inbox filters. Build 406 resolved only the separate Activity page;
# the in-box Tümü/Bildirimler lists rendered raw text and lost sender identity.
def repair_inbox(src):
 anchor="    Widget bildirimlerIcerigi(){"
 helper="""    Widget bildirimGonderenIle(Map<String,dynamic> ham,
      Widget Function(Map<String,dynamic>) goster){
      final from=(ham['fromUid']??ham['senderUid']??ham['senderId']??ham['actorUid']??'').toString();
      return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
        stream:from.isEmpty?null:FirebaseFirestore.instance.collection('users').doc(from).snapshots(),
        builder:(_,snap){
          final profil=snap.data?.data()??<String,dynamic>{};
          final v=<String,dynamic>{...ham};
          final tur=(v['type']??'').toString();
          final istek=tur=='follow_request'||tur=='friend_request'||tur=='friend';
          final ad=(profil['displayName']??profil['username']??v['senderName']??v['fromName']??'').toString().trim();
          final foto=(profil['photoUrl']??v['photoUrl']??v['senderPhotoUrl']??'').toString().trim();
          if(foto.isNotEmpty)v['photoUrl']=foto;
          if(ad.isNotEmpty)v['senderName']=ad;
          if(istek){
            final metin=(ham['text']??ham['message']??ham['content']??'').toString().trim();
            if(ad.isEmpty){
              v['text']=snap.connectionState==ConnectionState.waiting
                ?'Gönderen yükleniyor • $metin'
                :'Gönderen hesabı kullanılamıyor • $metin';
            }else{
              v['text']=metin.toLowerCase().startsWith(ad.toLowerCase())?metin:'$ad $metin';
            }
          }
          return goster(v);
        },
      );
    }

"""
 if src.count(anchor)!=1:raise SystemExit("inbox helper insertion anchor count drift")
 src=src.replace(anchor,helper+anchor,1)
 def notif_widget(s):
  s=one(s,
    "final d=docs[i],v=d.data(),okundu=v['read']==true;",
    "final d=docs[i];\n              return bildirimGonderenIle(d.data(),(v){\n               final okundu=v['read']==true;",
    "inbox notifications profile resolution")
  original="""if(context.mounted)await Navigator.push(context,MaterialPageRoute(builder:(_)=>const AktivitePage()));
                },
              );"""
  updated="""if(context.mounted)await Navigator.push(context,MaterialPageRoute(builder:(_)=>const AktivitePage()));
                },
              );
              });"""
  return one(s,original,updated,"inbox notifications builder closure")
 src=region(src,"    Widget bildirimlerIcerigi(){","    Widget isteklerIcerigi(){",notif_widget)
 def all_widget(s):
  s=one(s,
    "final d=item['doc'] as QueryDocumentSnapshot<Map<String,dynamic>>,v=d.data();",
    "final d=item['doc'] as QueryDocumentSnapshot<Map<String,dynamic>>;\n                   return bildirimGonderenIle(d.data(),(v){",
    "inbox all identity resolution")
  branch=s.index("return bildirimGonderenIle(d.data(),(v){")
  branch_end=s.index("final d=item['doc']",branch+len("return bildirimGonderenIle(d.data(),(v){"))
  close=s.rfind(");",branch,branch_end)
  if close<0:raise SystemExit("inbox all ListTile closure not found")
  return s[:close+2]+"\n                   });"+s[close+2:]

 return region(src,"    Widget tumIcerigi(){","    Widget sohbetlerIcerigi(){",all_widget)
m=repair_inbox(m)

# Approved NgelX identity: remove only the oversized feed logo, keep the wordmark.
m=one(m,"const Logo(kucuk:true,koyuZemin:true),",
      "const Text('NgelX',style:TextStyle(color:Colors.white,fontSize:21,fontWeight:FontWeight.w900)),",
      "Akış removes large N logo but retains brand text")

# Feed caption displays one short relative timestamp. Full timestamp remains
# accessible via a TAP tooltip; source createdAt and sorting are unchanged.
def short_time(s):
 old="""            Text(
              tam.isEmpty?zaman:'$zaman • $tam',
              style: const TextStyle(
                color: Colors.white60,
                fontSize: 11,
                fontWeight: FontWeight.w700,
              ),
            ),"""
 new="""            Tooltip(
              message:tam.isEmpty?zaman:tam,
              triggerMode:TooltipTriggerMode.tap,
              child:Text(zaman,
                style:const TextStyle(color:Colors.white60,fontSize:11,fontWeight:FontWeight.w700)),
            ),"""
 return one(s,old,new,"short relative time only")
m=region(m,"class AkisMetaSatiri extends StatelessWidget","class CanliSayacButonu",short_time)

wr("app/lib/main.dart",m)

# Security rules: a link is only a right to REQUEST; it cannot grant membership.
rules=rd("firestore.rules")
rules=one(rules,
    ") || validSelfJoin(chatId) || validPublicSelfJoin() || validFormerHide() || validFounderClose();",
    ") || validPublicSelfJoin() || validFormerHide() || validFounderClose();",
    "remove group invite self join")
beg=rules.index("    function validSelfJoin(chatId) {")
end=rules.index("    function validMemberAddition()",beg)
rules=rules[:beg]+"""    // Invite links must never provide permission to add oneself to members.
    function validSelfJoin(chatId) { return false; }
"""+rules[end:]
rules=one(rules,
    "request.resource.data.get('status', '') in ['pending', 'autojin']",
    "request.resource.data.get('status', '') == 'pending'",
    "spelling-backstop") if "request.resource.data.get('status', '') in ['pending', 'autojin']" in rules else rules
rules=one(rules,
    "request.resource.data.get('status', '') in ['pending', 'autojoin']",
    "request.resource.data.get('status', '') == 'pending'",
    "pending only join request")
target="""        allow update: if isGroupAdmin(chatId) || (
          signedIn()
          && (request.auth.uid == requestUid || resource.data.get('requestedBy', '') == request.auth.uid)
          && onlyChanges(['status', 'updatedAt'])
          && request.resource.data.get('status', '') == 'cancelled'
        ) || (
          signedIn()
          && request.auth.uid == requestUid
          && resource.data.get('uid', '') == request.auth.uid
          && request.resource.data.get('uid', '') == request.auth.uid
          && request.resource.data.get('status', '') == 'autojoin'
          && validInvite(request.resource.data.get('inviteCode', ''), chatId)
          && onlyChanges(['status', 'updatedAt', 'createdAt', 'inviteCode'])
        );"""
safe="""        allow update: if isGroupAdmin(chatId) || (
          signedIn()
          && (request.auth.uid == requestUid || resource.data.get('requestedBy', '') == request.auth.uid)
          && onlyChanges(['status', 'updatedAt'])
          && request.resource.data.get('status', '') == 'cancelled'
        ) || (
          // Let a legacy Build 406 autojoin record be re-submitted for real approval.
          signedIn()
          && request.auth.uid == requestUid
          && resource.data.get('uid', '') == request.auth.uid
          && request.resource.data.get('uid', '') == request.auth.uid
          && resource.data.get('status', '') in ['autojoin', 'cancelled', 'rejected']
          && request.resource.data.get('status', '') == 'pending'
          && validInvite(request.resource.data.get('inviteCode', ''), chatId)
          && onlyChanges(['status', 'updatedAt', 'createdAt', 'inviteCode'])
        );"""
rules=one(rules,target,safe,"replace 406 autojoin status upgrades")
wr("firestore.rules",rules)

# Emulator tests must REJECT link-based self-membership and accept only admin approval.
p="tools/firestore_rules_test.mjs";tests=rd(p)
a=tests.index("  // Geçerli davet kodu ile autojoin talebi oluşturulabilir.")
b=tests.index("  // Normal üye grup yönetim metadatasını değiştiremez.",a)
new="""  // Invite link NEVER self-admits, even in group without joinApproval.
  await assertFails(setDoc(doc(bob, 'chats/group_open/joinRequests/bob'), {
    uid:'bob',status:'autojoin',inviteCode:'CODE123',
    createdAt:serverTimestamp(),updatedAt:serverTimestamp(),
  }));
  await assertSucceeds(setDoc(doc(bob, 'chats/group_open/joinRequests/bob'), {
    uid:'bob',status:'pending',inviteCode:'CODE123',
    createdAt:serverTimestamp(),updatedAt:serverTimestamp(),
  }));
  await assertFails(setDoc(doc(bob, 'chats/group_open/joinRequests/bad'), {
    uid:'bob',status:'pending',inviteCode:'WRONG',
    createdAt:serverTimestamp(),
  }));
  await assertFails(updateDoc(doc(bob, 'chats/group_open'), {
    members:arrayUnion('bob'),formerMembers:arrayRemove('bob'),
    hiddenFor:arrayRemove('bob'),updatedAt:serverTimestamp(),
  }));
  await assertSucceeds(updateDoc(doc(admin, 'chats/group_open'), {
    members:arrayUnion('bob'),formerMembers:arrayRemove('bob'),
    hiddenFor:arrayRemove('bob'),updatedAt:serverTimestamp(),
  }));
  await assertSucceeds(updateDoc(doc(admin, 'chats/group_open/joinRequests/bob'), {
    status:'accepted',decidedBy:'admin',decidedAt:serverTimestamp(),
  }));
  const joined=await assertSucceeds(getDoc(doc(bob, 'chats/group_open')));
  assert.equal(joined.data().members.includes('bob'),true);

"""
tests=tests[:a]+new+tests[b:]
a=tests.index("  // A legacy pending request still cannot add itself without a valid autojoin credential.")
b=tests.index("  // Kurucu tek üyeyse grubu güvenli biçimde kapatabilir.",a)
new="""  // Approval-required group never allows link holder to add itself or upgrade to autojoin.
  await assertSucceeds(setDoc(doc(carol, 'chats/group_approval/joinRequests/carol'), {
    uid:'carol',status:'pending',inviteCode:'CODE999',
    createdAt:serverTimestamp(),updatedAt:serverTimestamp(),
  }));
  await assertFails(updateDoc(doc(carol, 'chats/group_approval/joinRequests/carol'), {
    status:'autojoin',updatedAt:serverTimestamp(),
  }));
  await assertFails(updateDoc(doc(carol, 'chats/group_approval'), {
    members:arrayUnion('carol'),formerMembers:arrayRemove('carol'),
    hiddenFor:arrayRemove('carol'),updatedAt:serverTimestamp(),
  }));
  // Founder/admin explicitly approves the request and adds the member.
  await assertSucceeds(updateDoc(doc(admin, 'chats/group_approval'), {
    members:arrayUnion('carol'),formerMembers:arrayRemove('carol'),
    hiddenFor:arrayRemove('carol'),updatedAt:serverTimestamp(),
  }));
  await assertSucceeds(updateDoc(doc(admin, 'chats/group_approval/joinRequests/carol'), {
    status:'accepted',decidedBy:'admin',decidedAt:serverTimestamp(),
  }));
  const approvedByAdmin=await assertSucceeds(getDoc(doc(carol, 'chats/group_approval')));
  assert.equal(approvedByAdmin.data().members.includes('carol'),true);

"""
tests=tests[:a]+new+tests[b:]
wr(p,tests)
print("Build 407 applied: admin-only link approval, secure Firestore authorization, new Çevrem/Radar, single final video seek, short share toast.",flush=True)
