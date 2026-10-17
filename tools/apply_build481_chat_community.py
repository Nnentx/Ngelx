#!/usr/bin/env python3
"""Build481: keep Build480 camera/gallery behavior and protect community roles.

Runs after ALL Build480 generated Dart code and QA transforms. Pure UI patch:
never rewrites posts, media transport, membership, security rules or production data.
"""
from pathlib import Path

MAIN=Path("app/lib/main.dart")
COMMUNITY=Path("app/lib/community450.dart")
PHOTO_MARK="// Build481: consistent large rounded chat photo frame"
COMMUNITY_MARK="// Build481: distinguish legacy founder permission from moderator rights"

OLD_PHOTO="""// Build467: common bounded photo, rounded across private and group routes.
class NgelXSohbetFotoOnizleme extends StatelessWidget{
  final String url;
  const NgelXSohbetFotoOnizleme({super.key,required this.url});
  @override Widget build(BuildContext context)=>ClipRRect(
    borderRadius:BorderRadius.circular(20),
    child:ConstrainedBox(
      constraints:BoxConstraints(
        maxWidth:math.min(280.0,MediaQuery.sizeOf(context).width*.68),
        maxHeight:math.min(390.0,MediaQuery.sizeOf(context).height*.48),
      ),
      child:Ngelx453Photo(url:url),
    ),
  );
}"""

NEW_PHOTO="""// Build481: consistent large rounded chat photo frame.
// The media remains uncropped (BoxFit.contain in Ngelx453Photo). This real
// frame keeps tall gallery images wide enough and anchors reactions to its
// bottom-right edge, just as camera photos/video already do.
class NgelXSohbetFotoOnizleme extends StatelessWidget{
  final String url;
  const NgelXSohbetFotoOnizleme({super.key,required this.url});
  @override Widget build(BuildContext context){
    final frameWidth=math.min(320.0,MediaQuery.sizeOf(context).width*.76);
    final frameHeight=math.min(440.0,MediaQuery.sizeOf(context).height*.52);
    return ClipRRect(
      borderRadius:BorderRadius.circular(22),
      child:ColoredBox(
        color:const Color(0xFF161A22),
        child:ConstrainedBox(
          constraints:BoxConstraints(minWidth:frameWidth,maxWidth:frameWidth,
            maxHeight:frameHeight),
          child:Ngelx453Photo(url:url),
        ),
      ),
    );
  }
}"""

COMMUNITY_ANCHOR="""        final root = _communities450.doc(widget.id);
        return ListView(
          padding: const EdgeInsets.all(16),"""

COMMUNITY_REPLACEMENT="""        final root = _communities450.doc(widget.id);
        // Build481: distinguish legacy founder permission from moderator rights.
        // Do not silently promote anyone or bypass Firestore security rules.
        final legacyFounder481 = v['founderId'] == _communityUid450
          && !List<String>.from(v['admins'] ?? const []).contains(_communityUid450);
        return ListView(
          padding: const EdgeInsets.all(16),"""

COMMUNITY_CHILD_ANCHOR="""        return ListView(
          padding: const EdgeInsets.all(16),
          children: ["""

COMMUNITY_CHILD_NEW="""        return ListView(
          padding: const EdgeInsets.all(16),
          children: [
            if(legacyFounder481)
              Padding(
                padding:const EdgeInsets.only(bottom:12),
                child:Material(
                  color:const Color(0xFFFFF4D6),
                  borderRadius:BorderRadius.circular(12),
                  child:Padding(
                    padding:const EdgeInsets.all(12),
                    child:Text(
                      'Bu topluluğun kurucusu olarak görünüyorsun ancak eski yönetici listesinde hesabın yok. Bazı işlemlerin reddedilmesi sunucudaki topluluk güvenlik kurallarından kaynaklanabilir. Üye veya yönetici yetkilerini otomatik değiştirmiyoruz.',
                      style:const TextStyle(color:Color(0xFF654B11),fontSize:12,fontWeight:FontWeight.w600),
                    ),
                  ),
                ),
              ),"""

def replace_once(src,old,new,label):
    count=src.count(old)
    if count!=1:
        raise RuntimeError(f"Build481 {label}: found {count} anchors, expected 1")
    return src.replace(old,new,1)

def photo(src):
    if PHOTO_MARK in src:
        return src
    src=replace_once(src,OLD_PHOTO,NEW_PHOTO,"shared photo frame")
    # Build467's already-correct reaction badge and Build476-478 timestamps
    # must remain byte-for-byte unchanged.
    for flag in ["// Build467: reaction anchored to the real media edge.",
                 "// Build476: plain text timestamps belong below",
                 "// Build478: improve outside-bubble timestamp contrast"]:
        if flag not in src:
            raise RuntimeError("Build481 previous fix absent: "+flag)
    return src

def community(src):
    if COMMUNITY_MARK in src:
        return src
    start=src.index("class _NgelXCommunityAdmin450State")
    # Only edit the administrator page, not chat groups or public directory.
    section=src[start:]
    section=replace_once(section,COMMUNITY_ANCHOR,COMMUNITY_REPLACEMENT,
                         "administrator role marker")
    section=replace_once(section,COMMUNITY_CHILD_ANCHOR,COMMUNITY_CHILD_NEW,
                         "legacy founder explanation")
    return src[:start]+section

def main():
    raw=MAIN.read_text(encoding="utf-8")
    com=COMMUNITY.read_text(encoding="utf-8")
    new_main=photo(raw)
    new_com=community(com)
    if raw != new_main:
        MAIN.write_text(new_main,encoding="utf-8")
    if com != new_com:
        COMMUNITY.write_text(new_com,encoding="utf-8")
    print("Build481: uncropped rounded photo frame; no permission escalation")

if __name__ == "__main__":
    main()
