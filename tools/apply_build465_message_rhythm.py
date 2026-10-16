#!/usr/bin/env python3
"""Build465 Messenger reference: coherent group/DM quote cards and sender spacing.

This is a UI-only generated-source patch. It intentionally does not modify
Firestore reply fields, reactions, media URLs, gesture handlers or group ACLs.
"""
from pathlib import Path
import re

MAIN=Path("app/lib/main.dart")
GROUP_START="  Widget mesajKarti(QueryDocumentSnapshot<Map<String,dynamic>> d,"
PRIVATE_START="  Widget ozelMesajKarti(QueryDocumentSnapshot<Map<String,dynamic>> d,"
PRIVATE_END="class NgelXSesliMesaj"
TAG="// Build465 Messenger quote presentation and tight avatar alignment"

def replace_one(s,old,new,label):
    n=s.count(old)
    if n!=1:raise RuntimeError(f"Build465 Messenger quote {label}: {n} anchors")
    return s.replace(old,new,1)

def transform(src):
    if TAG in src:return src
    start=src.index(GROUP_START)
    end=src.index("class TamEkranMedyaPage",start)
    group=src[start:end]
    # The sender avatar and name should sit closer to their first message.
    group=replace_one(group,
        "padding:const EdgeInsets.only(left:2,bottom:5,right:6,top:2),",
        "padding:const EdgeInsets.only(left:2,bottom:2,right:4,top:1),",
        "group sender margin")
    group=replace_one(group,
        "CircleAvatar(radius:10,backgroundColor:ngelxGroupGreenSoft,",
        "CircleAvatar(radius:12,backgroundColor:ngelxGroupGreenSoft,",
        "group sender avatar")
    group=replace_one(group,
        "const SizedBox(width:6),\n              Flexible(child:Text(isim,",
        "const SizedBox(width:5),\n              Flexible(child:Text(isim,",
        "group name gap")
    # Avoid the duplicated 'replied to X' label outside the actual quote card.
    duplicate=re.compile(
        r"          if\(yanit\.isNotEmpty&&yanitGonderen\.isNotEmpty\)Padding\(\n"
        r".*?Icon\(Icons\.reply_rounded.*?\n"
        r".*?yanitGonderen\+'’a yanıt verdi'.*?\n"
        r"          \),\n",
        re.S,
    )
    group,n=duplicate.subn("",group,count=1)
    if n!=1:raise RuntimeError("Build465 quote: expected one duplicated group reply header")
    group=replace_one(group,
        "border:Border.all(color:const Color(0xFFE5E7EB)),",
        "border:Border.all(color:const Color(0xFFD8E6DE)),",
        "quoted group border")
    group=replace_one(group,
        "Container(width:3,height:30,decoration:BoxDecoration(color:const Color(0xFF9CA3AF),",
        "Container(width:3,height:34,decoration:BoxDecoration(color:ngelxGroupGreen,",
        "quoted group accent")
    group=replace_one(group,
        "Text(yanit,maxLines:1,overflow:TextOverflow.ellipsis,",
        "Text(yanit,maxLines:2,overflow:TextOverflow.ellipsis,",
        "quoted group text")
    src=src[:start]+group+src[end:]

    start=src.index(PRIVATE_START)
    end=src.index(PRIVATE_END,start)
    dm=src[start:end]
    dm=replace_one(dm,
        "margin:const EdgeInsets.symmetric(horizontal:4,vertical:5),\n          padding:sadeMedya?EdgeInsets.zero:",
        "margin:const EdgeInsets.symmetric(horizontal:4,vertical:3),\n          padding:sadeMedya?EdgeInsets.zero:",
        "private message gap, excluding deleted-message notices")
    dm=replace_one(dm,
        "width:double.infinity,\n                margin:const EdgeInsets.only(bottom:8),",
        "width:math.min(264.0,MediaQuery.sizeOf(context).width*.68),\n"
        "                margin:const EdgeInsets.only(bottom:7),",
        "quoted DM width")
    dm=replace_one(dm,
        "color:Colors.white.withValues(alpha:.96),\n                  borderRadius:BorderRadius.circular(12),",
        "color:const Color(0xFFF3F5FA),\n                  borderRadius:BorderRadius.circular(12),",
        "quoted DM soft background")
    dm=replace_one(dm,
        "border:const Border(left:BorderSide(color:ngelxPrivateBlue,width:3)),",
        "border:const Border(left:BorderSide(color:ngelxPrivateBlue,width:3)),",
        "quoted DM left accent")
    src=src[:start]+dm+src[end:]
    return src.replace(GROUP_START,TAG+"\n"+GROUP_START,1)

def main():
    old=MAIN.read_text(encoding="utf-8")
    new=transform(old)
    if new!=old:MAIN.write_text(new,encoding="utf-8")
    print("Build465 Messenger: quoted messages compact and sender avatar closer to bubble")

if __name__=="__main__":main()
