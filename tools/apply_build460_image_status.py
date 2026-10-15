#!/usr/bin/env python3
"""Build460: bound image-provider wait and show a finite cover-image fallback.

Only edits client image loading UI; does not delete, migrate or reupload photos.
"""
from pathlib import Path
SOURCE=Path("app/lib/main.dart")

def one(s,old,new,name):
    n=s.count(old)
    if n!=1:raise ValueError(f"Build460 {name}: expected one anchor, found {n}")
    return s.replace(old,new,1)

def patch(s):
    if "// Build460 bounded remote image" in s:return s

    start=s.index("class NgelXAgImageProvider extends")
    end=s.index("\nFuture<void> ngelxAgResmiOnbelleginiTemizle",start)
    fragment=s[start:end]
    fragment=one(fragment,"final bytes=await _ngelxAgResmiBaytlari(key.url);",
                 "// Build460 bounded remote image: no spinner for minutes on a dead host.\n    final bytes=await _ngelxAgResmiBaytlari(key.url).timeout(const Duration(seconds:18));",
                 "bounded image provider")
    s=s[:start]+fragment+s[end:]

    start=s.index("class _NgelXOnayliProfilDuzenlePageState")
    end=s.index("\nclass ProfilPage extends StatefulWidget",start)
    fragment=s[start:end]
    target="child:cover.isNotEmpty?Image(image:NgelXAgImageProvider(cover),fit:BoxFit.cover):"
    replacement="""child:cover.isNotEmpty?NgelXAgResmi(
                    url:cover,fit:BoxFit.cover,
                    placeholder:const ColoredBox(color:Color(0xFFF1EAFE),
                      child:Center(child:Icon(Icons.image_outlined,color:Color(0xFFAC96DA),size:35))),
                    retryErrorBuilder:(ctx,error,retry)=>InkWell(onTap:retry,
                      child:const ColoredBox(color:Color(0xFFF1EAFE),
                        child:Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
                          Icon(Icons.cloud_off_outlined,color:Color(0xFF7C3AED)),
                          SizedBox(height:4),
                          Text('Kapak yüklenemedi - tekrar dene',
                            style:TextStyle(fontSize:12,color:Color(0xFF7C3AED))),
                        ])))),
                  ):"""
    # Recent Build456/457 may already replace this bare image with
    # NgelXAgResmi. Preserve that component and bound its shared provider.
    if fragment.count(target)==1:
        fragment=one(fragment,target,replacement,"cover loader fallback")
    elif "NgelXAgResmi(" in fragment:
        print("Build460: existing cover image widget retained with bounded provider")
    else:
        raise ValueError("Build460: unexpected cover widget; refusing blind replacement")
    s=s[:start]+fragment+s[end:]
    return s

def main():
    original=SOURCE.read_text(encoding="utf-8")
    updated=patch(original)
    if original!=updated:SOURCE.write_text(updated,encoding="utf-8")
    print("Build460: bounded cover image loading, non-destructive retry UI.")

if __name__=="__main__":main()
