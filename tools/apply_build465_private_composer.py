#!/usr/bin/env python3
"""Build465: match private composer spacing/action access to working group composer.

Keep private blue palette, message send, attachment, voice recording and
quick emoji semantics.  Change UI placement only, never message delivery.
"""
from pathlib import Path

MAIN=Path("app/lib/main.dart")
START="class _SohbetPageState"
END="class NgelXSesliMesaj"

ADD_BUTTON="""                      icon:const Icon(Icons.add_circle,color:ngelxPrivateBlue,size:29),
                    ),"""
DIRECT_BUTTONS="""                      icon:const Icon(Icons.add_circle,color:ngelxPrivateBlue,size:29),
                    ),
                    // Build465: one-tap camera and gallery, as on group chat.
                    IconButton(
                      tooltip:'Kamera',
                      padding:EdgeInsets.zero,
                      visualDensity:VisualDensity.compact,
                      constraints:const BoxConstraints.tightFor(width:36,height:44),
                      onPressed:ekIslemiSuruyor?null:()=>medyaGonder(ImageSource.camera),
                      icon:const Icon(Icons.camera_alt_rounded,color:ngelxPrivateBlue,size:23),
                    ),
                    IconButton(
                      tooltip:'Galeri',
                      padding:EdgeInsets.zero,
                      visualDensity:VisualDensity.compact,
                      constraints:const BoxConstraints.tightFor(width:36,height:44),
                      onPressed:ekIslemiSuruyor?null:()=>medyaGonder(ImageSource.gallery),
                      icon:const Icon(Icons.photo_library_rounded,color:ngelxPrivateBlue,size:23),
                    ),"""
EMOJI_EXTERNAL="""                    IconButton(
                      tooltip:'Emoji seç',
                      onPressed:emojiSec,
                      icon:const Icon(Icons.emoji_emotions,color:ngelxPrivateBlue),
                    ),"""
EMOJI_SUFFIX="""                          decoration:InputDecoration(
                            hintText:'Mesaj',"""
EMOJI_SUFFIX_NEW="""                          decoration:InputDecoration(
                            suffixIcon:IconButton(
                              tooltip:'Emoji seç',
                              onPressed:emojiSec,
                              icon:const Icon(Icons.emoji_emotions_rounded,color:ngelxPrivateBlue,size:22),
                            ),
                            hintText:'Mesaj',"""
DOUBLE_INSET="    bottomNavigationBar:SizedBox(height:MediaQuery.viewPaddingOf(context).bottom),"
SINGLE_INSET="""    // Build465: the composer already has SafeArea(top:false) at the bottom.
    bottomNavigationBar:const SizedBox.shrink(),"""

def exactly_once(source,old,new,what):
    n=source.count(old)
    if n!=1:
        raise RuntimeError(f"Build465 private composer {what}: expected 1 anchor, found {n}")
    return source.replace(old,new,1)

def transform(source):
    if "// Build465: one-tap camera and gallery" in source:return source
    a=source.index(START);b=source.index(END,a)
    target=source[a:b]
    target=exactly_once(target,ADD_BUTTON,DIRECT_BUTTONS,"group-like attachments")
    # Later Build455/457 stages reformat the input decoration, so locate
    # it from the unique composer controller rather than an exact hint label.
    textfield="controller:mesaj,"
    if target.count(textfield)!=1:
        raise RuntimeError("Build465 private composer: expected one composer TextField")
    origin=target.index(textfield)
    decoration="decoration:InputDecoration("
    pos=target.find(decoration,origin)
    if pos<0 or pos-origin>1200:
        raise RuntimeError("Build465 private composer: message input decoration changed")
    target=exactly_once(target,EMOJI_EXTERNAL,"","move emoji into input")
    suffix="""decoration:InputDecoration(
                            suffixIcon:IconButton(
                              tooltip:'Emoji seç',
                              onPressed:emojiSec,
                              icon:const Icon(Icons.emoji_emotions_rounded,color:ngelxPrivateBlue,size:22),
                            ),"""
    target=target[:pos]+suffix+target[pos+len(decoration):]
    target=exactly_once(target,DOUBLE_INSET,SINGLE_INSET,"remove doubled nav inset")
    return source[:a]+target+source[b:]

def main():
    before=MAIN.read_text(encoding="utf-8")
    after=transform(before)
    if after!=before: MAIN.write_text(after,encoding="utf-8")
    print("Build465: private chat bottom bar matches group geometry, no duplicated nav inset")

if __name__=="__main__":main()
