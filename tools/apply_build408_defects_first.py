#!/usr/bin/env python3
"""NgelX Build 408: fix remaining confirmed functional defects before redesign.
Run after the verified Build 407 patch. No profile layout redesign, data migration
or Firestore permission loosening. Stop on source drift instead of guessing.
"""
from pathlib import Path

def read(p): return Path(p).read_text(encoding='utf-8')
def write(p,s): Path(p).write_text(s,encoding='utf-8')
def one(s,old,new,label):
    n=s.count(old)
    if n!=1: raise SystemExit(f"{label}: expected exactly one anchor, found {n}")
    return s.replace(old,new,1)
def section(s,begin,end,fn):
    a=s.index(begin); b=s.index(end,a+len(begin))
    return s[:a]+fn(s[a:b])+s[b:]

m=read('app/lib/main.dart')
m=one(m,"defaultValue: '407'","defaultValue: '408'","settings build version")
m=one(m,"defaultValue: '1.0.183'","defaultValue: '1.0.184'","settings semantic version")

# A different user's profile must not rely solely on users.isLive/currentLiveId.
# Listen to the authoritative live_streams document; fail closed on loading,
# missing and stale sessions, without overwriting user/profile documents.
def fix_other_profile(s):
    s=one(s,
      "           final canli=v['isLive']==true&&(v['currentLiveId']??'').toString().isNotEmpty;",
      "           final canliAday=v['isLive']==true&&(v['currentLiveId']??'').toString().isNotEmpty;",
      "remove false live user flag from other profile")
    opening="""           final altGuvenliAlan=36.0;
           return ListView(
"""
    replacement="""           final altGuvenliAlan=36.0;
           return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
             stream:canliAday
               ? FirebaseFirestore.instance.collection('live_streams').doc(canliId).snapshots()
               : null,
             builder:(_,yayınSnap){
               final canli=canliAday
                 && yayınSnap.hasData
                 && yayınSnap.data!.exists
                 && ngelxCanliKaydiTaze(yayınSnap.data!.data()??<String,dynamic>{});
               return ListView(
"""
    s=one(s,opening,replacement,"live stream profile builder")
    closing="""             ],
           );
         },
       ),
     ));
   }

   Widget _profilSayac"""
    new_closing="""             ],
           );
             },
           );
         },
       ),
     ));
   }

   Widget _profilSayac"""
    s=one(s,closing,new_closing,"close live builder before profile future builder")
    return s
m=section(m,"class _KullaniciProfilPageState extends State<KullaniciProfilPage>","class NgelXVideoKapakOnizleme",fix_other_profile)

# Warn once per accepted group + block-list combination, including reopen.
# A change to the group's blocking relationships restores the warning.
# The blocked-message rendering and private-call guard remain untouched.
def fix_repeated_block_dialog(s):
    old="""       if(ortak.isEmpty||_engelUyarisiGosterildi)return;
       _engelUyarisiGosterildi=true;
       WidgetsBinding.instance.addPostFrameCallback((_)async{"""
    new="""       if(ortak.isEmpty||_engelUyarisiGosterildi)return;
       final prefs=await SharedPreferences.getInstance();
       final anahtar='ngelx_group_block_dialog_'+me+'_'+widget.chatId;
       final imza=(ortak.toList()..sort()).join('|');
       if(prefs.getString(anahtar)==imza){
         _engelUyarisiGosterildi=true;
         return;
       }
       _engelUyarisiGosterildi=true;
       WidgetsBinding.instance.addPostFrameCallback((_)async{"""
    s=one(s,old,new,"block-warning repeated on every group reopen")
    s=one(s,
      "         if(!gir&&mounted)Navigator.maybePop(context);",
      """         if(gir)await prefs.setString(anahtar,imza);
         if(!gir&&mounted)Navigator.maybePop(context);""",
      "remember acceptance only, preserve cancel action")
    return s
m=section(m,"class _GrupSohbetPageState extends State<GrupSohbetPage>","class ",fix_repeated_block_dialog)

# Previously generated group join request notification is historical but it
# should stop saying "wants to join" after founder/admin accepts or rejects it.
# Resolve its status from the pending request document, not message text.
def fix_activity(s):
    start="""   Widget _bildirimBasligiDurumlu(Map<String,dynamic> v,bool okundu){
     if(!_canliAktivitesi(v))return _bildirimBasligi(v,okundu);"""
    new="""   Widget _bildirimBasligiDurumlu(Map<String,dynamic> v,bool okundu){
     final tur=(v['type']??v['eventKind']??'').toString();
     if(tur=='group_join_request'||(v['eventKind']??'')=='group_join_request'){
       final chatId=(v['chatId']??v['groupId']??v['sourceId']??'').toString();
       final memberId=(v['fromUid']??v['senderUid']??v['senderId']??'').toString();
       if(chatId.isNotEmpty&&memberId.isNotEmpty){
         return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
           stream:FirebaseFirestore.instance.collection('chats').doc(chatId)
              .collection('joinRequests').doc(memberId).snapshots(),
           builder:(_,snap){
             final durum=(snap.data?.data()?['status']??'pending').toString();
             if(durum!='accepted'&&durum!='rejected'&&durum!='cancelled')
               return _bildirimBasligi(v,okundu);
             final ad=(v['senderName']??v['fromName']??'Bir kullanıcı').toString();
             final grup=(v['groupName']??v['targetTitle']??'').toString();
             final sonuc=durum=='accepted'?'onaylandı':durum=='rejected'?'reddedildi':'iptal edildi';
             return Text(ad+' adlı kullanıcının '+grup+' grubuna katılma isteği '+sonuc+'.',
               style:TextStyle(fontWeight:okundu?FontWeight.w500:FontWeight.w800));
           },
         );
       }
     }
     if(!_canliAktivitesi(v))return _bildirimBasligi(v,okundu);"""
    return one(s,start,new,"resolve accepted/rejected group notifications in Activity")
m=section(m,"class AktivitePage", "class KullaniciProfilPage",fix_activity)

# The inbox uses its own renderer in Tümü and Bildirimler. Ensure it shows
# the same status as the admin's request rather than a frozen old text string.
def fix_inbox(s):
    old="""          return goster(v);
        },
      );
    }"""
    replacement="""          if(tur=='group_join_request'){
            final chatId=(v['chatId']??v['groupId']??'').toString();
            final memberId=(v['fromUid']??v['senderUid']??'').toString();
            if(chatId.isNotEmpty&&memberId.isNotEmpty){
              return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
                stream:FirebaseFirestore.instance.collection('chats').doc(chatId)
                   .collection('joinRequests').doc(memberId).snapshots(),
                builder:(_,istekSnap){
                  final durum=(istekSnap.data?.data()?['status']??'pending').toString();
                  if(durum=='accepted'||durum=='rejected'||durum=='cancelled'){
                    final sonuc=durum=='accepted'?'onaylandı':durum=='rejected'?'reddedildi':'iptal edildi';
                    v['text']=(ad.isEmpty?'Bir kullanıcı':ad)+' adlı kullanıcının '
                       +(v['groupName']??v['targetTitle']??'').toString()
                       +' grubuna katılma isteği '+sonuc+'.';
                  }
                  return goster(v);
                },
              );
            }
          }
          return goster(v);
        },
      );
    }"""
    return one(s,old,replacement,"inbox Tümü/Bildirimler group request status")
m=section(m,"class _GelenKutusuPageState", "class ",fix_inbox) if "class _GelenKutusuPageState" in m else m

write('app/lib/main.dart',m)
p=one(read('app/pubspec.yaml'),"version: 1.0.183+407","version: 1.0.184+408","pubspec version")
write('app/pubspec.yaml',p)
print("Build 408 defects-first patch applied: active live session validation, group warning acknowledgment and join-request notification state.",flush=True)
