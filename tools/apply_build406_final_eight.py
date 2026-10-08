#!/usr/bin/env python3
"""Build 406: eight user-approved final repairs after the 405 patch."""
from pathlib import Path

def read(p): return Path(p).read_text(encoding="utf-8")
def write(p,x): Path(p).write_text(x,encoding="utf-8")
def one(s,old,new,tag):
 n=s.count(old)
 if n!=1:raise SystemExit(f"{tag}: one anchor needed, found {n}, {old[:90]!r}")
 return s.replace(old,new,1)
def replace_in(s,start_key,end_key,action):
 i=s.index(start_key)
 j=s.index(end_key,i+len(start_key))
 return s[:i]+action(s[i:j])+s[j:]

p="app/lib/main.dart";m=read(p)
m=one(m,"defaultValue: '405'","defaultValue: '406'","build code")
m=one(m,"defaultValue: '1.0.181'","defaultValue: '1.0.182'","build version")
pub=one(read("app/pubspec.yaml"),"version: 1.0.181+405","version: 1.0.182+406","pubspec")
write("app/pubspec.yaml",pub)

# 2. Show authenticated sender identity on *all* activity rows, including legacy follow/friend requests.
# The extra listener is local to a lazily constructed ListView row and uses Firestore's cache.
import re
def notifications(src):
 left=src.index("Widget _bildirimBasligi(Map<String,dynamic>")
 right=src.index("\nclass AktiflikDurumuYazisi",left)
 part=src[left:right]
 pattern=r"itemBuilder:\s*\(_,i\)\s*\{\s*final d\s*=\s*docs\[i\];\s*final v\s*=\s*d\.data\(\);"
 match=re.search(pattern,part)
 if match is None:
  at=part.find("itemBuilder:")
  raise SystemExit("notifications sender row unmatched. Actual snippet: "+repr(part[at:at+450]))
 before=part[match.start():match.end()]
 part=one(part,before,
"""                 itemBuilder:(_,i){final d=docs[i];
            final saved=d.data();
            final fromUid=(saved['fromUid']??saved['senderId']??saved['senderUid']??'').toString();
            return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
              stream:fromUid.isEmpty?null:FirebaseFirestore.instance.collection('users').doc(fromUid).snapshots(),
              builder:(_,sender){
                final v=<String,dynamic>{...saved};
                final person=sender.data?.data();
                if(person!=null){
                  final name=(person['displayName']??person['username']??'').toString().trim();
                  final picture=(person['photoUrl']??'').toString().trim();
                  if(name.isNotEmpty)v['senderName']=name;
                  if(picture.isNotEmpty)v['photoUrl']=picture;
                }
                if((v['senderName']??v['fromName']??'').toString().trim().isEmpty&&
                    (v['type']=='friend_request'||v['type']=='follow_request'||v['type']=='friend')){
                  v['senderName']=fromUid.isEmpty?'Gönderen bilinmiyor':
                    sender.connectionState==ConnectionState.waiting?'Gönderen yükleniyor':'Kullanıcı';
                }""","notifications sender join")
 src=src[:left]+part+src[right:]
 part=src[left:src.index("\nclass AktiflikDurumuYazisi",left)]
 close_re=r"onTap:\s*\(\)=>_secimModu\?_bildirimSec\(d\.id\):_aktiviteAc\(context,d\),\s*\)\);\s*\}\),"
 end_match=re.search(close_re,part)
 if end_match is None:
  p=part.find("onTap:()=>_secimModu")
  raise SystemExit("notification close unmatched: "+repr(part[p:p+380]))
 replacement="""onTap:()=>_secimModu?_bildirimSec(d.id):_aktiviteAc(context,d),
             ));
              },
            );
          }),"""
 part=part[:end_match.start()]+replacement+part[end_match.end():]
 src=src[:left]+part+src[src.index("\nclass AktiflikDurumuYazisi",left):]
 return src
m=notifications(m)

# 3. A valid current admin-issued invitation is itself permission for a direct join.
def join(src):
 src=one(src,"final onayGerekli=iv['joinApproval']==true;","// The current invitation code authorizes direct admission.","invite no approval wait")
 src=one(src,"'status':onayGerekli?'pending':'autojoin',","'status':'autojoin',","join request state")
 start=src.index("if(onayGerekli){")
 end=src.index("await chat.update({",start)
 if "group_join_request" not in src[start:end]:raise SystemExit("invite-approval block unexpectedly changed")
 src=src[:start]+src[end:]
 src=one(src,
"""       final iv=inviteSnap.data()??<String,dynamic>{};
       final chatId=(iv['chatId']??'').toString();""",
"""       final iv=inviteSnap.data()??<String,dynamic>{};
       final expires=iv['expiresAt'];
       if(iv['revoked']==true||iv['active']==false||
           (expires is Timestamp&&expires.toDate().isBefore(DateTime.now()))){
         if(mounted)ScaffoldMessenger.of(context).showSnackBar(
           const SnackBar(content:Text('Bu grup daveti artık geçerli değil.')));
         return;
       }
       final chatId=(iv['chatId']??'').toString();""","invite expiry/revocation")
 src=one(src,
"""'Grup yöneticisi onay istiyorsa önce katılma isteğin gönderilir. Onaylandığında bildirim alırsın.'""",
"""'Geçerli davet bağlantısı veya kodu ile yönetici onayı beklemeden katılabilirsin. Üyelik sınırı ve grup güvenliği kuralları geçerlidir.'""","invite help text")
 return src
m=replace_in(m,"class _GrubaKatilPageState extends State<GrubaKatilPage>","\nclass ",join)

# 4 and 5 and 7: refresh the actual intro player on URL changes, stabilize repeated profile bitmap
# providers, and give the longer Saved label enough width without ugly word splitting.
def owner(src):
 src=one(src,"class _ProfilPageState extends State<ProfilPage> {",
"""class _ProfilPageState extends State<ProfilPage> {
  final Map<String,ImageProvider> _sabitProfilGorselleri=<String,ImageProvider>{};
  ImageProvider _sabitProfilResmi(String url)=>
    _sabitProfilGorselleri.putIfAbsent(url,()=>NgelXAgImageProvider(url));""","profile stable providers")
 photo_count=src.count("NgelXAgImageProvider(fotoUrl)")
 cover_count=src.count("NgelXAgImageProvider(kapakUrl)")
 if photo_count==0 and cover_count==0:raise SystemExit("Profile images provider anchors missing")
 src=src.replace("NgelXAgImageProvider(fotoUrl)","_sabitProfilResmi(fotoUrl)")
 src=src.replace("NgelXAgImageProvider(kapakUrl)","_sabitProfilResmi(kapakUrl)")
 src=one(src,"ProfilTanitimVideoKarti(url:tanitimVideoUrl)",
         "ProfilTanitimVideoKarti(key:ValueKey<String>(tanitimVideoUrl),url:tanitimVideoUrl)",
         "new intro URL must rebuild player and poster")
 src=one(src,"SizedBox(width:55,child:Column(children:[Container(width:48,height:48,",
             "SizedBox(width:67,child:Column(children:[Container(width:48,height:48,",
             "shortcut label has space")
 src=one(src,
"""SizedBox(height:28,child:Center(child:Text(yazi,textAlign:TextAlign.center,maxLines:2,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.black87,fontSize:10,fontWeight:FontWeight.w700))))""",
"""SizedBox(height:28,child:Center(child:FittedBox(fit:BoxFit.scaleDown,child:Text(yazi,
  textAlign:TextAlign.center,maxLines:1,softWrap:false,overflow:TextOverflow.visible,
  style:const TextStyle(color:Colors.black87,fontSize:10,fontWeight:FontWeight.w700)))))""",
"saved label stays on one line")
 return src
m=replace_in(m,"class _ProfilPageState extends State<ProfilPage>","\nclass _ProfilEtkilesimRozeti",owner)

# 8. The two privacy conditions are cumulative; clarify effective visibility without modifying access.
def privacy(src):
 old="""           Padding(padding:const EdgeInsets.fromLTRB(22,14,22,4),child:Text(t('profileViewWho'),style:const TextStyle(fontWeight:FontWeight.w900))),"""
 new="""           Padding(padding:const EdgeInsets.fromLTRB(22,14,22,4),child:Text(t('profileViewWho'),style:const TextStyle(fontWeight:FontWeight.w900))),
           Padding(padding:const EdgeInsets.fromLTRB(22,0,22,8),child:Text(
             hesapGizli
               ?'Gizli hesap açık: yeni takipçiler onay bekler. Profil görünürlüğü seçimi de uygulanır; “Herkes” seçilse bile onaylanmamış kişiler özel alanları göremez.'
               :'Bu seçim profilini kimlerin görebileceğini sınırlar. Gizli hesabı açarsan takip onayı da gerekir.',
             style:const TextStyle(color:Colors.black54,fontSize:12,height:1.35))),
"""
 return one(src,old,new,"profile visibility explanation")
m=replace_in(m,"class _TercihlerPageState extends State<TercihlerPage>","\nclass ",privacy)

# 6. Keep an explanatory poster/loading state in media previews rather than a blank/dark cell;
# do not claim this fixes every decoder/network stall in the full-screen Feed player.
def preview(src):
 old="""       } else if (url.isNotEmpty) {
         kapak = NgelXVideoKapakOnizleme(url: url);"""
 new="""       } else if (url.isNotEmpty) {
         kapak = ColoredBox(color:const Color(0xFFF0EDFA),child:Stack(
           fit:StackFit.expand,
           children:[
             NgelXVideoKapakOnizleme(url:url),
             const Positioned(left:6,bottom:6,child:Text('Video önizlemesi',
               style:TextStyle(fontSize:10,color:Colors.white,fontWeight:FontWeight.w800))),
           ],
         ));"""
 return one(src,old,new,"video cover loading not blank")
m=replace_in(m,"class MedyaOnizleme extends StatelessWidget","\nclass ",preview)
write(p,m)

# 1. Fix inherited white-on-white text in the now-single persistent live summary card.
p="app/lib/live_broadcast_studio.dart";live=read(p)
live=one(live,"Text(etiket,style:const TextStyle(fontWeight:FontWeight.w700))",
         "Text(etiket,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w700))","live summary label")
live=one(live,"Text(deger,style:const TextStyle(fontWeight:FontWeight.w900))",
         "Text(deger,style:const TextStyle(color:Colors.black87,fontWeight:FontWeight.w900))","live summary value")
write(p,live)

# Security: link authority checked by Firestore against active group code. Self-join still
# requires own request, no elevated admin rights, <60 members, non-deleted/non-banned group.
p="firestore.rules";rules=read(p)
rules=one(rules,
"""        && groupDoc(chatId).data.get('inviteCode', '') == code
        && groupDoc(chatId).data.get('groupDeleted', false) != true;""",
"""        && groupDoc(chatId).data.get('inviteCode', '') == code
        && groupDoc(chatId).data.get('groupDeleted', false) != true
        && get(/databases/$(database)/documents/group_invites/$(code)).data.get('revoked', false) != true
        && get(/databases/$(database)/documents/group_invites/$(code)).data.get('active', true) == true
        && (
          get(/databases/$(database)/documents/group_invites/$(code)).data.get('expiresAt', null) == null
          || get(/databases/$(database)/documents/group_invites/$(code)).data.get('expiresAt', null) > request.time
        );""","current active, unexpired group invitation")
i=rules.index("    function validSelfJoin(chatId) {");j=rules.index("    function validMemberAddition()",i)
q=rules[i:j]
q=one(q,"        && resource.data.get('joinApproval', false) != true\n",
"""        && resource.data.get('groupDeleted', false) != true
        && !(request.auth.uid in resource.data.get('bannedUsers', []))
        && !(request.auth.uid in resource.data.get('bannedMembers', []))
        && resource.data.get('members', []).size() < resource.data.get('maxMembers', 60)
""","secure valid link bypasses manual approval")
rules=rules[:i]+q+rules[j:]
# Pending requests from an earlier app build may be converted to authenticated autojoin with
# a still-valid link. Other users cannot modify their status.
needle="""        allow update: if isGroupAdmin(chatId) || (
          signedIn()
          && (request.auth.uid == requestUid || resource.data.get('requestedBy', '') == request.auth.uid)
          && onlyChanges(['status', 'updatedAt'])
          && request.resource.data.get('status', '') == 'cancelled'
        );"""
replace="""        allow update: if isGroupAdmin(chatId) || (
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
rules=one(rules,needle,replace,"existing pending invite upgrades to autojoin")
write(p,rules)

# The older Firebase emulator scenario asserted that joining an approval-enabled group was
# impossible. Update this one scenario: only a verified link holder can self-join.
p="tools/firestore_rules_test.mjs";tests=read(p)
start=tests.index("  // Yönetici onaylı grupta katılma isteği oluşturulabilir ama kullanıcı kendini ekleyemez.")
end=tests.index("  // Kurucu tek üyeyse grubu güvenli biçimde kapatabilir.",start)
new_tests="""  // A legacy pending request still cannot add itself without a valid autojoin credential.
  await assertSucceeds(setDoc(doc(carol, 'chats/group_approval/joinRequests/carol'), {
    uid:'carol', status:'pending', inviteCode:'CODE999',
    createdAt:serverTimestamp(),updatedAt:serverTimestamp(),
  }));
  await assertFails(updateDoc(doc(carol, 'chats/group_approval'), {
    members:arrayUnion('carol'),formerMembers:arrayRemove('carol'),
    hiddenFor:arrayRemove('carol'),updatedAt:serverTimestamp(),
  }));
  // Explicit valid invitation allows direct admission even if joinApproval=true.
  await assertSucceeds(updateDoc(doc(carol, 'chats/group_approval/joinRequests/carol'), {
    status:'autojoin',updatedAt:serverTimestamp(),
  }));
  await assertSucceeds(updateDoc(doc(carol, 'chats/group_approval'), {
    members:arrayUnion('carol'),formerMembers:arrayRemove('carol'),
    hiddenFor:arrayRemove('carol'),updatedAt:serverTimestamp(),
  }));
  const joinedByLink=await assertSucceeds(getDoc(doc(carol, 'chats/group_approval')));
  assert.equal(joinedByLink.exists(),true);
  assert.equal(joinedByLink.data().formerMembers.includes('carol'),false);
  
"""
tests=tests[:start]+new_tests+tests[end:]
write(p,tests)
print("Build 406 applied: live summary text, activity sender, secure direct group invite, intro/cover cache, media preview, saved shortcut and privacy explanation.")
