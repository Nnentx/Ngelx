"""Build457: fail-closed identity for generated private inbox rows.

Run after Build455/456 source generation. No chat writes or message mutation.
"""
from pathlib import Path

SOURCE=Path("app/lib/main.dart")
LOOKUP="stream:_profiles453.putIfAbsent(other,()=>FirebaseFirestore.instance.collection('users').doc(other).snapshots())"
OTHER="final other=members.firstWhere((x)=>x!=ben,orElse:()=>ben??'');"
BUILDER="builder:(_,u){"
GUARD="""if(u.hasError)return ListTile(
                        title:const Text('Kişi bilgisi yüklenemedi'),
                        trailing:IconButton(
                          onPressed:()=>setState(()=>_profiles453.remove(other)),
                          icon:const Icon(Icons.refresh_rounded),
                        ),
                      );
                      if(!u.hasData)return const ListTile(
                        title:Text('Kişi bilgisi yükleniyor…'),
                        leading:CircleAvatar(child:Icon(Icons.person_outline)),
                      );
                      if(u.data!.id!=other)return const SizedBox.shrink();
                      """

def transform(source):
    if "inbox-uid457-" in source:
        return source
    left=source.index("class _MesajPageState")
    right=source.index("class ArsivSohbetlerPage",left)
    region=source[left:right]
    if region.count(LOOKUP)!=1:
        raise ValueError("Build457: unexpected inbox profile source; refuse an unsafe UID patch")
    at=region.index(LOOKUP)
    prev=region.rfind(OTHER,0,at)
    if prev<0 or at-prev>320:
        raise ValueError("Build457: exact private recipient lookup missing")
    region=region[:prev]+region[prev:].replace(
        OTHER,
        "final other=members.firstWhere((x)=>x!=ben&&x.isNotEmpty,orElse:()=>'');\n"
        "                  if(other.isEmpty||other==ben||!members.contains(ben))return const SizedBox.shrink();",
        1)
    at=region.index(LOOKUP)
    builder=region.index(BUILDER,at)
    if builder-at>380:
        raise ValueError("Build457: unsafe private chat builder drift")
    streamBuilder=region.rfind("return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(",0,at)
    if streamBuilder<0 or at-streamBuilder>220:
        raise ValueError("Build457: expected private chat StreamBuilder not found")
    region=region[:streamBuilder]+region[streamBuilder:].replace(
        "return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(",
        "return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(\n"
        "                    key:ValueKey<String>('inbox-uid457-' + d.id + '-' + other),",
        1)
    at=region.index(LOOKUP)
    builder=region.index(BUILDER,at)
    region=region[:builder]+region[builder:].replace(BUILDER,BUILDER+"\n                      "+GUARD,1)
    return source[:left]+region+source[right:]

def main():
    before=SOURCE.read_text()
    after=transform(before)
    if before!=after:SOURCE.write_text(after)
    print("Build457: private chat is bound to verified recipient UID")

if __name__=="__main__":
    main()
