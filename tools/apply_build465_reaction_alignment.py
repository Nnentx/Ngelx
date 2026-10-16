#!/usr/bin/env python3
"""Build465: keep image reaction badge attached to image, not chat row edge.

Pure layout patch for existing group and private reaction widgets.  Retain the
existing reactions, double-tap, details and hit-test support.
"""
from pathlib import Path

MAIN=Path("app/lib/main.dart")

def one(src,old,new,what):
    count=src.count(old)
    if count!=1:raise RuntimeError(f"Build465 reaction alignment: {what}: {count} anchors")
    return src.replace(old,new,1)

def section(src,begin,end):
    a=src.index(begin);b=src.index(end,a)
    return a,b,src[a:b]

def transform(src):
    if "// Build465: badge is anchored to media bounds" in src:return src
    a,b,region=section(src,"  Widget _grupMedyaTepkiAlani(","  Widget mesajKarti(")
    region=one(region,"    return Stack(\n", """    // Build465: badge is anchored to media bounds, not chat row width.
    return Align(widthFactor:1.0,alignment:Alignment.centerLeft,child:Stack(
""","group shrink-wrap")
    region=one(region,"          right:8,\n          bottom:2,","          right:18,\n          bottom:2,","group heart offset")
    region=one(region,"    );\n  }\n","    ));\n  }\n","group stack close")
    src=src[:a]+region+src[b:]

    a,b,region=section(src,"  Widget _ozelMedyaTepkiAlani(","  Widget ozelMesajKarti(")
    region=one(region,"    return Stack(clipBehavior:Clip.none,children:[",
               "    return Align(widthFactor:1.0,alignment:Alignment.centerLeft,child:Stack(clipBehavior:Clip.none,children:[",
               "private shrink-wrap")
    region=one(region,"    const sagDokunmaAlani=42.0,altDokunmaAlani=13.0;",
               "    const sagDokunmaAlani=30.0,altDokunmaAlani=13.0;",
               "private reserved touch space")
    region=one(region,"        right:sagDokunmaAlani,\n        bottom:altDokunmaAlani,",
               "        right:sagDokunmaAlani+5,\n        bottom:altDokunmaAlani,",
               "private badge offset")
    region=one(region,"translation:const Offset(.5,.5)",
               "translation:const Offset(.25,.5)",
               "private translation")
    region=one(region,"    ]);\n  }\n","    ]));\n  }\n","private stack close")
    return src[:a]+region+src[b:]

def main():
    original=MAIN.read_text(encoding="utf-8")
    updated=transform(original)
    if original!=updated:MAIN.write_text(updated,encoding="utf-8")
    print("Build465: group and private image hearts follow image width")

if __name__=="__main__":main()
