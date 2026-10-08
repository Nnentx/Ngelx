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
needle="    unawaited(kontrol.seekTo(Duration(milliseconds:hedef)));\n    if(mounted)setState((){});"
m=one(m,needle,"    if(mounted)setState((){});","fast seek gesture without overlapping decoder requests")

# Reduce multiple sticky snackbars without changing success payload or navigation.
needle="""      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content:Text(lt('Paylaşım yayınlandı ✅ Akışta ve profilinde görünecek.','Post published ✅ It will appear in your feed and profile.')),"""
replacement="""      ScaffoldMessenger.of(context).hideCurrentSnackBar();
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        duration:const Duration(seconds:3),
        behavior:SnackBarBehavior.floating,
        content:Text(lt('Paylaşım yayınlandı ✅','Post published ✅')),"""
m=one(m,needle,replacement,"Create snackbar lifetime")

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
