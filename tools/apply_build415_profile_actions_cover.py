#!/usr/bin/env python3
"""Build 415 visual-only changes after verified Build 414 patch stack.

Preserve all original callbacks, Firestore rules, business logic and profile modes.
Abort on unexpected markup rather than risk modifying unrelated UI.
"""
from pathlib import Path
p=Path("app/lib/main.dart")
s=p.read_text(encoding="utf-8")

start=s.index("class _KullaniciProfilPageState extends State<KullaniciProfilPage>")
end=s.index("\nclass NgelXVideoKapakOnizleme",start)
visitor=s[start:end]

def vreplace(old,new,label):
    global visitor
    n=visitor.count(old)
    if n!=1: raise SystemExit(f"Build 415 visitor {label}: expected one anchor, got {n}")
    visitor=visitor.replace(old,new,1)

# Four tightly crammed buttons become two fully tappable rows (52px high).
# Keep the exact existing following, private request, message, friendship,
# removal and mutual-groups callbacks and streams.
vreplace("SizedBox(height:51,child:Row(crossAxisAlignment:CrossAxisAlignment.stretch,children:[",
         "Column(children:[\n"
         "                 SizedBox(height:52,child:Row(crossAxisAlignment:CrossAxisAlignment.stretch,children:[",
         "start first row")
vreplace("Expanded(flex:3,child:StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(",
         "Expanded(child:StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(",
         "follow flex")
vreplace("Expanded(flex:2,child:OutlinedButton.icon(",
         "Expanded(child:OutlinedButton.icon(",
         "message flex")
vreplace("""                   const SizedBox(width:5),
                   Expanded(flex:3,child:StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(""",
"""                 ])),
                 const SizedBox(height:8),
                 SizedBox(height:52,child:Row(crossAxisAlignment:CrossAxisAlignment.stretch,children:[
                   Expanded(child:StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(""",
"second row starts with friendship")
vreplace("Expanded(flex:3,child:OutlinedButton.icon(",
         "Expanded(child:OutlinedButton.icon(",
         "mutual groups flex")
# Close second row and column. Only touch the four-action container's end.
vreplace("""                     label:const FittedBox(fit:BoxFit.scaleDown,child:Text('Ortak gruplar',maxLines:1,
                       style:TextStyle(fontSize:11,fontWeight:FontWeight.w800))),
                   )),
                 ])),""",
"""                     label:const FittedBox(fit:BoxFit.scaleDown,child:Text('Ortak gruplar',maxLines:1,
                       style:TextStyle(fontSize:12,fontWeight:FontWeight.w800))),
                   )),
                 ])),
                 ]),""",
"close mutual groups row and column")
# Readable text, preserve single-line long pending statuses with safe FittedBox.
for old,new,label in [
  ("TextStyle(fontSize:10,fontWeight:FontWeight.w800))),",
   "TextStyle(fontSize:12,fontWeight:FontWeight.w800))),","follow type size"),
  ("TextStyle(fontSize:10.5,fontWeight:FontWeight.w800))),",
   "TextStyle(fontSize:12,fontWeight:FontWeight.w800))),","message type size"),
  ("maxLines:1,style:const TextStyle(fontSize:10,fontWeight:FontWeight.w800)",
   "maxLines:1,style:const TextStyle(fontSize:12,fontWeight:FontWeight.w800)","friend type size"),
]:
    vreplace(old,new,label)
s=s[:start]+visitor+s[end:]

# Long Android AppBar title was clipped next to Kaydet. No crop interaction
# and positioning math changes.
old="AppBar(title:const Text('Kapak fotoğrafını ayarla',style:TextStyle(fontWeight:FontWeight.w900))"
if s.count(old)!=1:
    raise SystemExit(f"Build 415 crop title: expected one anchor, got {s.count(old)}")
s=s.replace(old,"AppBar(title:const Text('Kapağı ayarla',style:TextStyle(fontWeight:FontWeight.w900))",1)

# Owner's editor shows the known cover until live Firestore arrives. On actual
# loaded documents empty URL still means removed cover; do not resurrect it.
start=s.index("class NgelXOnayliProfilDuzenlePage")
end=s.index("class ProfilPage extends StatefulWidget",start)
editor=s[start:end]
old="final cover=(v['coverPhotoUrl']??'').toString();"
new="final cover=snap.hasData?(v['coverPhotoUrl']??'').toString():widget.ilkKapakUrl;"
if editor.count(old)!=1:raise SystemExit("Build 415 owner cover initial preview anchor")
editor=editor.replace(old,new,1)
old="child:cover.isNotEmpty?Image(image:NgelXAgImageProvider(cover),fit:BoxFit.cover):"
new="""child:cover.isNotEmpty?Image(
                     image:NgelXAgImageProvider(cover),fit:BoxFit.cover,
                     gaplessPlayback:true,
                     frameBuilder:(ctx,child,frame,syncLoaded)=>syncLoaded||frame!=null
                       ?child
                       :const ColoredBox(color:Color(0xFFF1EAFE),
                          child:Center(child:CircularProgressIndicator(
                            strokeWidth:2,color:Color(0xFF8B5CF6)))),
                     errorBuilder:(ctx,error,stack)=>const ColoredBox(
                       color:Color(0xFFF1EAFE),
                       child:Center(child:Icon(Icons.broken_image_outlined,
                         color:Color(0xFF8B5CF6),size:35)))):"""
if editor.count(old)!=1:raise SystemExit("Build 415 cover render anchor drift")
editor=editor.replace(old,new,1)
s=s[:start]+editor+s[end:]

# On filtered friend list, do not show "3 friends" while only 1 row is visible.
# Unfiltered list retains accurate total. Avoid inaccurate counts for user docs
# not among the current loaded batch.
old="""? ids.length.toString()+' Arkadaş'+(sorgu.trim().isNotEmpty?' · Arama sonuçları':'')
          : baslik"""
new="""? (sorgu.trim().isNotEmpty?'Arkadaş · Arama sonuçları':ids.length.toString()+' Arkadaş')
          : baslik"""
if s.count(old)!=1:raise SystemExit("Build 415 friends header anchor drift")
s=s.replace(old,new,1)

p.write_text(s,encoding="utf-8")
print("Build 415 two-row actions, cover preview, crop title and friend search header applied.")
