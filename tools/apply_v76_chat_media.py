#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MAIN_PATH = ROOT / "app/lib/main.dart"
PUBSPEC_PATH = ROOT / "app/pubspec.yaml"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Build 295 patch failed: {label}: expected 1 match, got {count}")
    return text.replace(old, new, 1)


def regex_once(text: str, pattern: str, repl: str, label: str, flags: int = 0) -> str:
    new_text, count = re.subn(pattern, repl, text, count=1, flags=flags)
    if count != 1:
        raise SystemExit(f"Build 295 patch failed: {label}: expected 1 match, got {count}")
    return new_text


main = MAIN_PATH.read_text(encoding="utf-8")
if "class NgelXSohbetFotoOnizleme" in main:
    raise SystemExit("Build 295 patch already appears to be applied.")

start = main.find("  Widget ozelMesajKarti(")
end = main.find("  Widget sohbetUstBilgi()", start)
if start < 0 or end < 0:
    raise SystemExit("Build 295 patch failed: private chat message card region not found.")

chat = main[start:end]

chat = regex_once(
    chat,
    r"(\s+final photo=tur=='photo',video=tur=='video',[^\n]*;\n)",
    r"\1    final medyaUrl=ngelxMesajMedyaUrl(v,video:video);\n"
    r"    final videoKapakUrl=video?ngelxMesajVideoKapagi(v):'';\n",
    "private chat media variables",
)

chat = replace_once(
    chat,
    "TamEkranMedyaPage(url:(v['mediaUrl']??'').toString())",
    "TamEkranMedyaPage(url:medyaUrl)",
    "photo full-screen URL",
)
chat = replace_once(
    chat,
    "TamEkranVideoPage(url:(v['videoUrl']??v['mediaUrl']??'').toString())",
    "TamEkranVideoPage(url:medyaUrl)",
    "video full-screen URL",
)
chat = replace_once(
    chat,
    "IgnorePointer(child:ClipRRect(borderRadius:BorderRadius.circular(16),child:CachedNetworkImage(imageUrl:(v['mediaUrl']??'').toString(),width:230,fit:BoxFit.cover)))",
    "IgnorePointer(child:NgelXSohbetFotoOnizleme(url:medyaUrl))",
    "private photo preview",
)
chat = replace_once(
    chat,
    "IgnorePointer(child:ClipRRect(borderRadius:BorderRadius.circular(16),child:NgelXGrupVideoMesaj(url:(v['videoUrl']??v['mediaUrl']??'').toString(),compact:true)))",
    "IgnorePointer(child:NgelXSohbetVideoOnizleme(url:medyaUrl,thumbnailUrl:videoKapakUrl))",
    "private video preview",
)

main = main[:start] + chat + main[end:]

helper_anchor = "class NgelXGrupVideoMesaj extends StatefulWidget{"
if main.count(helper_anchor) != 1:
    raise SystemExit(
        f"Build 295 patch failed: video preview anchor expected once, got {main.count(helper_anchor)}"
    )

helpers = r'''
String _ngelxIlkGecerliMedyaAdresi(Iterable<dynamic> adaylar){
  for(final ham in adaylar){
    final adres=(ham??'').toString().trim();
    if(adres.isEmpty)continue;
    final uri=Uri.tryParse(adres);
    if(uri!=null&&(uri.scheme=='https'||uri.scheme=='http'))return adres;
  }
  return '';
}

String ngelxMesajMedyaUrl(Map<String,dynamic> veri,{bool video=false}){
  return _ngelxIlkGecerliMedyaAdresi(video
    ?<dynamic>[
      veri['videoUrl'],
      veri['mediaUrl'],
      veri['playbackUrl'],
      veri['downloadUrl'],
      veri['url'],
      veri['attachmentUrl'],
    ]
    :<dynamic>[
      veri['mediaUrl'],
      veri['imageUrl'],
      veri['photoUrl'],
      veri['downloadUrl'],
      veri['url'],
      veri['attachmentUrl'],
    ]);
}

String ngelxMesajVideoKapagi(Map<String,dynamic> veri){
  return _ngelxIlkGecerliMedyaAdresi(<dynamic>[
    veri['thumbnailUrl'],
    veri['posterUrl'],
    veri['previewUrl'],
    veri['coverUrl'],
    veri['imageUrl'],
  ]);
}

class NgelXSohbetFotoOnizleme extends StatelessWidget{
  final String url;
  const NgelXSohbetFotoOnizleme({super.key,required this.url});

  @override
  Widget build(BuildContext context){
    Widget hata()=>Container(
      width:230,
      height:180,
      alignment:Alignment.center,
      decoration:BoxDecoration(
        color:const Color(0xFFF3F4F6),
        borderRadius:BorderRadius.circular(16),
      ),
      child:const Column(
        mainAxisSize:MainAxisSize.min,
        children:[
          Icon(Icons.image_not_supported_outlined,color:Color(0xFF6B7280),size:34),
          SizedBox(height:7),
          Text('Fotoğraf yüklenemedi',style:TextStyle(color:Color(0xFF4B5563),fontSize:12,fontWeight:FontWeight.w700)),
        ],
      ),
    );
    if(url.isEmpty)return hata();
    return ClipRRect(
      borderRadius:BorderRadius.circular(16),
      child:SizedBox(
        width:230,
        height:180,
        child:CachedNetworkImage(
          key:ValueKey('chat-photo-$url'),
          imageUrl:url,
          fit:BoxFit.cover,
          memCacheWidth:720,
          fadeInDuration:const Duration(milliseconds:120),
          placeholder:(_,__)=>const ColoredBox(
            color:Color(0xFFF3F4F6),
            child:Center(child:SizedBox(width:24,height:24,child:CircularProgressIndicator(strokeWidth:2,color:Color(0xFF6B7280)))),
          ),
          errorWidget:(_,__,___)=>hata(),
        ),
      ),
    );
  }
}

class NgelXSohbetVideoOnizleme extends StatelessWidget{
  final String url,thumbnailUrl;
  const NgelXSohbetVideoOnizleme({super.key,required this.url,this.thumbnailUrl=''});

  Widget _oynatKatmani()=>Center(
    child:Container(
      width:54,
      height:54,
      decoration:BoxDecoration(
        color:Colors.black.withValues(alpha:.58),
        shape:BoxShape.circle,
        border:Border.all(color:Colors.white54),
      ),
      child:const Icon(Icons.play_arrow_rounded,color:Colors.white,size:36),
    ),
  );

  Widget _videoIlkKaresi(){
    if(url.isEmpty){
      return Container(
        width:246,
        height:178,
        alignment:Alignment.center,
        decoration:BoxDecoration(color:const Color(0xFF20242D),borderRadius:BorderRadius.circular(16)),
        child:const Column(mainAxisSize:MainAxisSize.min,children:[
          Icon(Icons.videocam_off_outlined,color:Colors.white60,size:36),
          SizedBox(height:7),
          Text('Video açılamadı',style:TextStyle(color:Colors.white70,fontSize:12,fontWeight:FontWeight.w700)),
        ]),
      );
    }
    return NgelXGrupVideoMesaj(url:url,compact:true);
  }

  @override
  Widget build(BuildContext context){
    if(thumbnailUrl.isEmpty)return _videoIlkKaresi();
    return ClipRRect(
      borderRadius:BorderRadius.circular(16),
      child:SizedBox(
        width:246,
        height:178,
        child:Stack(
          fit:StackFit.expand,
          children:[
            CachedNetworkImage(
              key:ValueKey('chat-video-thumb-$thumbnailUrl'),
              imageUrl:thumbnailUrl,
              fit:BoxFit.cover,
              memCacheWidth:720,
              placeholder:(_,__)=>const ColoredBox(
                color:Color(0xFF20242D),
                child:Center(child:SizedBox(width:24,height:24,child:CircularProgressIndicator(strokeWidth:2,color:Colors.white70))),
              ),
              errorWidget:(_,__,___)=>_videoIlkKaresi(),
            ),
            IgnorePointer(child:_oynatKatmani()),
          ],
        ),
      ),
    );
  }
}

'''

main = main.replace(helper_anchor, helpers + helper_anchor, 1)

main = replace_once(
    main,
    "defaultValue: '1.0.75'",
    "defaultValue: '1.0.76'",
    "app version name",
)
main = replace_once(
    main,
    "defaultValue: '294'",
    "defaultValue: '295'",
    "app build number",
)
MAIN_PATH.write_text(main, encoding="utf-8")

pubspec = PUBSPEC_PATH.read_text(encoding="utf-8")
pubspec = replace_once(
    pubspec,
    "version: 1.0.75+294",
    "version: 1.0.76+295",
    "pubspec version",
)
PUBSPEC_PATH.write_text(pubspec, encoding="utf-8")

# Keep the cumulative regression verifiers compatible with the new build.
for path in sorted((ROOT / "tools").glob("verify_v*.py")):
    if path.name == "verify_v72_device_fixes.py":
        continue
    text = path.read_text(encoding="utf-8")
    if '"version: 1.0.75+294"))' in text and '"version: 1.0.76+295"' not in text:
        text = text.replace(
            '"version: 1.0.75+294"))',
            '"version: 1.0.75+294", "version: 1.0.76+295"))',
        )
        path.write_text(text, encoding="utf-8")

v72_path = ROOT / "tools/verify_v72_device_fixes.py"
v72 = v72_path.read_text(encoding="utf-8")
v72 = replace_once(
    v72,
    'require("version: 1.0.75+294" in PUBSPEC, "Build 294 sürüm zinciri")',
    'require("version: 1.0.76+295" in PUBSPEC, "Build 295 sürüm zinciri")',
    "V72 pubspec build check",
)
v72 = replace_once(
    v72,
    'require("defaultValue: \'1.0.75\'" in MAIN and "defaultValue: \'294\'" in MAIN,',
    'require("defaultValue: \'1.0.76\'" in MAIN and "defaultValue: \'295\'" in MAIN,',
    "V72 runtime build check",
)
v72_path.write_text(v72, encoding="utf-8")

print("Build 295 chat media patch prepared.")
