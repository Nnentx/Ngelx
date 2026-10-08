#!/usr/bin/env python3
"""Build 412: responsive Profile Edit safe-area bottom buttons and color warning.
Apply after the Build 411 appearance/editor scripts. No storage or auth changes.
"""
from pathlib import Path
p=Path("app/lib/main.dart");s=p.read_text(encoding="utf-8")
start=s.index("class NgelXOnayliProfilDuzenlePage")
stop=s.index("class ProfilPage extends StatefulWidget",start)
part=s[start:stop]
def one(old,new,what):
  global part
  n=part.count(old)
  if n!=1:raise SystemExit(f"Build 412 {what} needs 1 match, found {n}")
  part=part.replace(old,new,1)

one("""  void _hata(String mesaj){
    if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(mesaj)));
  }""",
"""  void _hata(String mesaj,{bool kapakUyarisi=false}){
    if(!mounted)return;
    final messenger=ScaffoldMessenger.of(context);
    messenger.hideCurrentSnackBar();
    messenger.showSnackBar(SnackBar(
      behavior:SnackBarBehavior.floating,
      backgroundColor:kapakUyarisi?const Color(0xFFFFE5AA):const Color(0xFFF3E9FF),
      elevation:5,
      shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(16)),
      margin:EdgeInsets.fromLTRB(16,0,16,MediaQuery.of(context).viewPadding.bottom+16),
      duration:const Duration(seconds:4),
      content:Row(children:[
        Icon(kapakUyarisi?Icons.warning_amber_rounded:Icons.info_outline_rounded,
          color:kapakUyarisi?const Color(0xFF9E4D00):const Color(0xFF6E35CA),size:25),
        const SizedBox(width:10),
        Expanded(child:Text(mesaj,style:const TextStyle(
          color:Color(0xFF322438),fontSize:14,fontWeight:FontWeight.w700,height:1.3))),
      ]),
    ));
  }""","colorful accessible warning")
one("_hata('Kapaklı görünüm için önce bir kapak fotoğrafı ekle.');","_hata('Kapaklı görünüm için önce bir kapak fotoğrafı ekle.',kapakUyarisi:true);","cover-validation-only amber warning")
one("padding:const EdgeInsets.fromLTRB(17,8,17,18),",
    """padding:EdgeInsets.fromLTRB(
              17,8,17,
              50.0+MediaQuery.of(context).viewPadding.bottom+
                MediaQuery.of(context).viewInsets.bottom,
            ),""","bottom editor scroll safe area")
# Extra minimum bottom spacing on the content even for non-overlay system navigation,
# while keeping action buttons inside the scrollable content for short screens.
one("""              const SizedBox(height:12),
            ]),
          );
        },
      ),
    ));
  }
}""","""              const SizedBox(height:24),
            ]),
          );
        },
      ),
    ));
  }
}""","bottom action breathing room")
s=s[:start]+part+s[stop:];p.write_text(s,encoding="utf-8")
print("Build 412 editor: colored and accessible cover warning; safe scroll insets for all Android navigation modes.")
