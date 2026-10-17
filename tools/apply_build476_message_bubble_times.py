#!/usr/bin/env python3
"""Build476: move plain private text-message times below the colored bubbles.

Apply ONLY to _ozelMesajKarti435, after Build467's reaction-overlay patch.
Keep reaction overlays, media, reply cards, delivery state and history intact.
"""
from pathlib import Path

MAIN=Path('app/lib/main.dart')
BEGIN='  Widget _ozelMesajKarti435('
END='  Future<void> _hikayeYanitKartiAc('
MARK='// Build476: plain text timestamps belong below, not inside, message bubbles'

def once(s,old,new,where):
    n=s.count(old)
    if n!=1:
        raise RuntimeError(f'Build476 {where}: expected exactly one anchor, got {n}')
    return s.replace(old,new,1)

def transform(source):
    if MARK in source:
        return source
    start=source.index(BEGIN)
    end=source.index(END,start)
    body=source[start:end]
    body=once(body,
       '    final medyaTepkiKart=photo||video;',
       '''    final medyaTepkiKart=photo||video;
    // Build476: plain text timestamps belong below, not inside, message bubbles.
    // Keep dedicated media/call/invite cards and their layout unchanged.
    final yaziSaatiDisarida=!photo&&!video&&!shared&&!sharedProfile
      &&!audio&&!file&&!location&&!call&&!storyReply
      &&!canliPaylasimi&&!sesliOdaPaylasimi
      &&ngelx456InviteCode(gosterilecekMetin)==null;''',
       'text-only flag')
    body=once(body,
       '            if(saat.isNotEmpty)Padding(padding:const EdgeInsets.only(top:4),child:Row(mainAxisSize:MainAxisSize.min,children:[',
       '            if(saat.isNotEmpty&&!yaziSaatiDisarida)Padding(padding:const EdgeInsets.only(top:4),child:Row(mainAxisSize:MainAxisSize.min,children:[',
       'hide in-bubble clock only for plain text')
    body=once(body,
       '        child:Stack(clipBehavior:Clip.none,children:[\n          Padding(padding:EdgeInsets.only(bottom:!medyaTepkiKart&&sayilar.isNotEmpty?10:0),child:Container(',
       '''        child:Column(
          mainAxisSize:MainAxisSize.min,
          crossAxisAlignment:ben?CrossAxisAlignment.end:CrossAxisAlignment.start,
          children:[
          Stack(clipBehavior:Clip.none,children:[
          Padding(padding:EdgeInsets.only(bottom:!medyaTepkiKart&&sayilar.isNotEmpty?10:0),child:Container(''',
       'wrap reaction stack with bubble clock layout')
    body=once(body,
       '''        if(!medyaTepkiKart&&sayilar.isNotEmpty)Positioned(
          bottom:0,right:ben?7:null,left:ben?null:7,
          child:_ozelMedyaTepkiBalonu(d.reference,sayilar,tepkiler.length),
        ),
        ]),
      ),
    );
  }

''',
       '''        if(!medyaTepkiKart&&sayilar.isNotEmpty)Positioned(
          bottom:0,right:ben?7:null,left:ben?null:7,
          child:_ozelMedyaTepkiBalonu(d.reference,sayilar,tepkiler.length),
        ),
        ]),
        if(yaziSaatiDisarida&&saat.isNotEmpty)
          Padding(
            padding:EdgeInsets.only(top:4,left:ben?0:10,right:ben?10:0,bottom:3),
            child:Row(mainAxisSize:MainAxisSize.min,children:[
              Text(saat,style:const TextStyle(fontSize:10.5,color:Color(0xFF6B7280))),
              if(sureli)...[
                const SizedBox(width:5),
                const Icon(Icons.timer_outlined,size:12,color:ngelxPrivateBlue),
                const SizedBox(width:2),
                const Text('Süreli',style:TextStyle(fontSize:9.5,color:ngelxPrivateBlue)),
              ],
              if(goruldu)...[
                const SizedBox(width:5),
                Text(_ngelx438Ui("Görüldü"),style:const TextStyle(fontSize:10,color:Colors.blueGrey)),
              ],
            ]),
          ),
        ]),
      ),
    );
  }

''',
       'place clock outside text bubble and keep reaction anchor')
    return source[:start]+body+source[end:]

if __name__=='__main__':
    before=MAIN.read_text(encoding='utf-8')
    after=transform(before)
    if before!=after:MAIN.write_text(after,encoding='utf-8')
    print('Build476: ordinary outgoing/incoming timestamps rendered below the bubble')
