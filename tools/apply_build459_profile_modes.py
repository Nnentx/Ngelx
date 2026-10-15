#!/usr/bin/env python3
"""Build459: restore functional cover/coverless profile modes.

Runs AFTER Build458 transforms, keeping its camera, video and other changes.
No Firestore writes, migrations, deletions or changing saved media URLs.
"""
from pathlib import Path

MAIN=Path("app/lib/main.dart")

def replace_once(s,old,new,label):
    count=s.count(old)
    if count!=1:
        raise ValueError(f"Build459 {label}: expected exactly 1 anchor, got {count}")
    return s.replace(old,new,1)

def patch(s):
    if "// Build459 saved profile mode" in s:
        return s
    a=s.index("class _ProfilPageState extends State<ProfilPage>")
    b=s.index("\nclass _ProfilEtkilesimRozeti",a)
    owner=s[a:b]
    original="if(true) // Build458 owner coverless rendering"
    actual="if(ngelx459KapaksizGorunum(profilGorunumu,kapakUrl)) // Build459 saved profile mode"
    owner=replace_once(owner,original,actual,"owner mode not forced")
    s=s[:a]+owner+s[b:]

    a=s.index("class _NgelXOnayliProfilDuzenlePageState")
    b=s.index("\nclass ProfilPage extends StatefulWidget",a)
    editor=s[a:b]
    top="              SizedBox(height:208,child:Stack(clipBehavior:Clip.none,children:["
    bottom="              TextField(controller:_ad,maxLength:60"
    i=editor.index(top)
    j=editor.index(bottom,i+len(top))
    original_cover=editor[i:j]
    if not original_cover.rstrip().endswith(")),"):
        raise ValueError("Build459: cover header not found intact")
    plain="""              SizedBox(height:182,child:Center(child:Stack(clipBehavior:Clip.none,
                alignment:Alignment.center,children:[
                  Container(padding:const EdgeInsets.all(5),decoration:const BoxDecoration(
                    shape:BoxShape.circle,
                    gradient:LinearGradient(colors:[Color(0xFF1AC5F4),Color(0xFF913EF4)])),
                    child:CircleAvatar(radius:67,backgroundColor:Colors.white,
                      backgroundImage:photo.isEmpty?null:NgelXAgImageProvider(photo),
                      child:photo.isEmpty?const Icon(Icons.person_rounded,
                        color:Color(0xFF8B5CF6),size:52):null)),
                  Positioned(right:0,bottom:10,
                    child:IconButton.filledTonal(
                      onPressed:_kaydediliyor?null:widget.onFoto,
                      tooltip:'Profil fotoğrafını değiştir',
                      icon:const Icon(Icons.camera_alt_rounded),
                      style:IconButton.styleFrom(backgroundColor:Colors.white,
                        foregroundColor:Colors.black87))),
                ]))),
"""
    # The two branches genuinely differ. Keep original covered header, cover
    # upload/removal actions and all lower editor widgets exactly as they were.
    branch=("              if(_gorunum=='cover') ...[\n"
            +original_cover
            +"              ] else ...[\n"
            +plain
            +"              ],\n")
    editor=editor[:i]+branch+editor[j:]
    s=s[:a]+editor+s[b:]
    # A pure, testable rendering decision; no backend writes or media updates.
    helper="""bool ngelx459KapaksizGorunum(String profilGorunumu,String kapakUrl) =>
  profilGorunumu=='coverless'||kapakUrl.isEmpty;

"""
    needle="class _ProfilPageState extends State<ProfilPage>"
    if s.count(needle)!=1:raise ValueError("Build459 pure mode predicate injection anchor")
    s=s.replace(needle,helper+needle,1)
    return s

def main():
    s=MAIN.read_text(encoding="utf-8")
    after=patch(s)
    if after!=s:MAIN.write_text(after,encoding="utf-8")
    print("Build459: cover mode saved/rendered correctly, coverless editor avatar centered. No media deleted.")

if __name__=="__main__":
    main()
