"""Build457: isolate each private chat row by verified participant UID.

Applied only after the existing Build445/Build456 patch pipeline.
No Firestore writes and no change to group or media upload flows.
"""
from pathlib import Path

SOURCE=Path("app/lib/main.dart")

FIELD_OLD="""  final Map<String,Future<DocumentSnapshot<Map<String,dynamic>>>> _kullaniciCache={};"""
FIELD_NEW="""  final Map<String,Future<DocumentSnapshot<Map<String,dynamic>>>> _kullaniciCache={};
  // A stable per-UID listener prevents list-position recycling from showing
  // a previous chat participant after inbox sort/filter or account changes.
  final Map<String,Stream<DocumentSnapshot<Map<String,dynamic>>>> _inbox457Profiles={};
  Stream<DocumentSnapshot<Map<String,dynamic>>> _inbox457Profile(String uid)=>
      _inbox457Profiles.putIfAbsent(uid,()=>FirebaseFirestore.instance.collection('users').doc(uid).snapshots());"""

ROW_OLD="""            final other=members.firstWhere((x)=>x!=ben,orElse:()=>ben??'');
            final benEngelledim=engellenenler.contains(other);
            return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:FirebaseFirestore.instance.collection('users').doc(other).snapshots(),builder:(_,u){
              final p=u.data?.data()??{};"""
ROW_NEW="""            final other=members.firstWhere((x)=>x!=ben&&x.isNotEmpty,orElse:()=>'');
            // Malformed private chats must never fall back to the current user's
            // profile: it would label a conversation as the wrong recipient.
            if(other.isEmpty||other==ben)return const SizedBox.shrink();
            final benEngelledim=engellenenler.contains(other);
            return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
              key:ValueKey<String>('inbox-person-ד' + d.id + '-' + other),
              stream:_inbox457Profile(other),
              builder:(_,u){
              if(u.hasError)return ListTile(
                title:const Text('Kişi bilgisi yüklenemedi'),
                trailing:IconButton(
                  tooltip:'Kişiyi yeniden yükle',
                  icon:const Icon(Icons.refresh),
                  onPressed:()=>setState(()=>_inbox457Profiles.remove(other)),
                ),
              );
              if(!u.hasData)return const ListTile(
                title:Text('Kişi bilgisi yükleniyor…'),
                leading:CircleAvatar(child:Icon(Icons.person_outline)),
              );
              // Do not allow an old listener to show another UID's profile.
              if(u.data!.id!=other)return const SizedBox.shrink();
              final p=u.data!.data()??<String,dynamic>{};"""

# Use stable ASCII key (the source below is never interpolated in Python).
ROW_NEW=ROW_NEW.replace("inbox-person-ד","inbox-person-")

def exactly_once(source: str, old: str, new: str, reason: str) -> str:
    count=source.count(old)
    if count!=1:
        raise ValueError(f"{reason}: expected exactly one anchor, got {count}")
    return source.replace(old,new,1)

def transform(source: str) -> str:
    if "inbox-person-' + d.id" in source:
        return source
    a=source.index("class _MesajPageState extends State<MesajPage> {")
    b=source.index("\nclass ArsivSohbetlerPage",a)
    region=source[a:b]
    region=exactly_once(region,FIELD_OLD,FIELD_NEW,"profile cache")
    region=exactly_once(region,ROW_OLD,ROW_NEW,"private chat row")
    return source[:a]+region+source[b:]

def main():
    before=SOURCE.read_text()
    after=transform(before)
    if after!=before:
        SOURCE.write_text(after)
    print("Build457: UID-keyed private chat rows, no self-recipient fallback")

if __name__=="__main__":
    main()
