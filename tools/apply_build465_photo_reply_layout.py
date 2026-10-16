#!/usr/bin/env python3
"""Build465: preserve full original chat photo aspect and readable reply previews.

Run AFTER generated Flutter source patches. Only modifies chat media widgets;
upload/storage/Firestore payload, media fetching and click handlers stay intact.
Refuses to touch unexpected or changed source structures.
"""
from pathlib import Path
MAIN=Path("app/lib/main.dart")

START="class NgelXSohbetFotoOnizleme extends StatelessWidget{"
END="class NgelXSohbetVideoOnizleme extends StatelessWidget{"
REPLY_START="class NgelXReplyMediaPreview extends StatelessWidget{"
REPLY_END="String _ngelxIlkGecerliMedyaAdresi("

OLD_PHOTO_LAYOUT="""    return ClipRRect(
      borderRadius:BorderRadius.circular(16),
      child:SizedBox(
        width:230,
        height:180,
        child:NgelXAgResmi(
          url:url,
          fit:BoxFit.cover,
          placeholder:const ColoredBox(
            color:Color(0xFFF3F4F6),
            child:Center(child:SizedBox(width:24,height:24,child:CircularProgressIndicator(strokeWidth:2,color:Color(0xFF6B7280)))),
          ),
          error:hata(),
        ),
      ),
    );"""

NEW_PHOTO_LAYOUT="""    // Build465: retain the image's natural width/height ratio in chat.
    // A fixed 230x180 BoxFit.cover cropped tall and wide shared pictures.
    final mediaWidth=math.min(280.0,MediaQuery.sizeOf(context).width*.72);
    final mediaHeight=math.min(390.0,MediaQuery.sizeOf(context).height*.52);
    return ClipRRect(
      borderRadius:BorderRadius.circular(18),
      child:ConstrainedBox(
        constraints:BoxConstraints(maxWidth:mediaWidth,maxHeight:mediaHeight),
        child:NgelXAgResmi(
          url:url,
          width:mediaWidth,
          fit:BoxFit.contain,
          placeholder:SizedBox(
            width:mediaWidth,height:180,
            child:const ColoredBox(
              color:Color(0xFFF3F4F6),
              child:Center(child:SizedBox(width:24,height:24,child:CircularProgressIndicator(strokeWidth:2,color:Color(0xFF6B7280)))),
            ),
          ),
          error:hata(),
        ),
      ),
    );"""

OLD_REPLY="return ClipRRect(borderRadius:BorderRadius.circular(9),child:SizedBox(width:46,height:46,child:child));"
NEW_REPLY="""// Build465: recognisable quoted-photo preview, still lightweight for video.
    return ClipRRect(
      borderRadius:BorderRadius.circular(11),
      child:SizedBox(width:60,height:60,child:child),
    );"""

def once(s,old,new,label):
    count=s.count(old)
    if count!=1: raise RuntimeError(f"Build465 photo reply: {label} found {count}, expected 1")
    return s.replace(old,new,1)

def section(s,start,end,fn):
    a=s.index(start);b=s.index(end,a)
    return s[:a]+fn(s[a:b])+s[b:]

def transform(s):
    if "// Build465: retain the image's natural width/height ratio" in s:return s
    s=section(s,START,END,lambda r:once(r,OLD_PHOTO_LAYOUT,NEW_PHOTO_LAYOUT,"photo layout"))
    s=section(s,REPLY_START,REPLY_END,lambda r:once(r,OLD_REPLY,NEW_REPLY,"reply thumbnail"))
    return s

def main():
    s=MAIN.read_text(encoding="utf-8")
    out=transform(s)
    if s!=out:MAIN.write_text(out,encoding="utf-8")
    print("Build465: unclipped chat photo ratio and rounded 60px reply preview")
if __name__=="__main__":main()
