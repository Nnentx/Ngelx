#!/usr/bin/env python3
"""Build 414: non-destructive UI refinements after Build 413.

No Firestore writes, social callbacks, cover mode settings, or routes are altered.
"""
from pathlib import Path
p=Path('app/lib/main.dart')
s=p.read_text(encoding='utf-8')

def one(old,new,label):
    global s
    n=s.count(old)
    if n!=1:raise SystemExit(f'Build 414 {label}: expected one anchor, got {n}')
    s=s.replace(old,new,1)

# Keep friend tab search itself and the true total count, but make it clear
# that the visible rows are filtered after the query.
one("""        child:Text(toplamArkadas?ids.length.toString()+' Arkadaş':baslik,style:const TextStyle(color:Colors.black87,fontSize:20,fontWeight:FontWeight.w900)),""",
"""        child:Text(toplamArkadas
          ? ids.length.toString()+' Arkadaş'+(sorgu.trim().isNotEmpty?' · Arama sonuçları':'')
          : baslik,style:const TextStyle(color:Colors.black87,fontSize:20,fontWeight:FontWeight.w900)),""",
"friend list search count")

# Full-length friend tabs overflow on compact Android displays. The content of
# the tabs stays the same, only their short visual titles change.
one("Tab(text:'Önerilenler'),","Tab(text:'Öneriler'),","friends recommendation tab")
one("Tab(text:'Ortak noktalar'),","Tab(text:'Ortak'),","friends mutual tab")

# Intro card is only 145x116px on a visitor profile. Big white text over the
# media obscures the thumbnail; keep exactly the same onTap/player logic.
one("""            :const Column(mainAxisSize:MainAxisSize.min,children:[
                Icon(Icons.play_circle_fill_rounded,color:Colors.white,size:54),
                SizedBox(height:7),
                Text('Tanıtım videosunu oynat',style:TextStyle(color:Colors.white,fontWeight:FontWeight.w900)),
              ])),""",
"""            :const Icon(Icons.play_circle_fill_rounded,color:Colors.white,size:45)),""",
"video thumbnail text overlay")

# Edit screen: reduce heavy opaque cover button to a small accessible camera
# icon without changing its original cover callback.
one("""                  FilledButton.icon(onPressed:_kaydediliyor?null:widget.onKapak,
                    style:FilledButton.styleFrom(backgroundColor:Colors.black.withValues(alpha:.7),foregroundColor:Colors.white),
                    icon:const Icon(Icons.camera_alt_rounded,size:16),label:const Text('Kapak fotoğrafını\\ndeğiştir',style:TextStyle(fontWeight:FontWeight.w800,fontSize:10))),""",
"""                  IconButton.filledTonal(
                    tooltip:'Kapak fotoğrafını değiştir',
                    onPressed:_kaydediliyor?null:widget.onKapak,
                    style:IconButton.styleFrom(
                      backgroundColor:Colors.black.withValues(alpha:.72),
                      foregroundColor:Colors.white),
                    icon:const Icon(Icons.camera_alt_rounded,size:20)),""",
"cover edit overlay control")

p.write_text(s,encoding='utf-8')
print('Build 414 visual polish applied with original actions preserved.')
