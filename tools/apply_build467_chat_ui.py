#!/usr/bin/env python3
"""Build467 post-generation layout patch. Preserve transport, ACL, media and calls."""
from pathlib import Path

P=Path('app/lib/main.dart')
def one(s,a,b,label):
    n=s.count(a)
    if n!=1: raise RuntimeError(f'Build467 {label}: {n} anchors')
    return s.replace(a,b,1)
def scoped(s,first,last,fn):
    i=s.index(first);j=s.index(last,i)
    return s[:i]+fn(s[i:j])+s[j:]

def transform(s):
    if '// Build467: common bounded photo' in s:return s
    s=one(s,
      "class NgelXSohbetFotoOnizleme extends StatelessWidget{final String url;const NgelXSohbetFotoOnizleme({super.key,required this.url});@override Widget build(BuildContext context)=>Ngelx453Photo(url:url);}",
      """// Build467: common bounded photo, rounded across private and group routes.
class NgelXSohbetFotoOnizleme extends StatelessWidget{
  final String url;
  const NgelXSohbetFotoOnizleme({super.key,required this.url});
  @override Widget build(BuildContext context)=>ClipRRect(
    borderRadius:BorderRadius.circular(20),
    child:ConstrainedBox(
      constraints:BoxConstraints(
        maxWidth:math.min(280.0,MediaQuery.sizeOf(context).width*.68),
        maxHeight:math.min(390.0,MediaQuery.sizeOf(context).height*.48),
      ),
      child:Ngelx453Photo(url:url),
    ),
  );
}""",'shared rounded image')
    def private_media(r):
        i=r.index('    const sagDokunmaAlani=30.0,altDokunmaAlani=13.0;')
        j=r.index('\n  }',i)
        return r[:i]+"""    // Build467: reaction anchored to the real media edge.
    return Align(widthFactor:1,alignment:Alignment.centerRight,child:Stack(
      clipBehavior:Clip.none,
      children:[
        Padding(padding:const EdgeInsets.only(bottom:10),child:media),
        if(total>0)Positioned(right:5,bottom:0,
          child:_ozelMedyaTepkiBalonu(ref,counts,total)),
      ],
    ));"""+r[j:]
    s=scoped(s,'  Widget _ozelMedyaTepkiAlani(','  Widget ozelMesajKarti(',private_media)
    def bubble(r):
        r=one(r,"""        child:Container(
          constraints:BoxConstraints(maxWidth:math.min(340.0,MediaQuery.sizeOf(context).width*.8)),""",
        """        // Build467: reactions float outside text bubble.
        child:Stack(clipBehavior:Clip.none,children:[
          Padding(padding:EdgeInsets.only(bottom:!medyaTepkiKart&&sayilar.isNotEmpty?10:0),child:Container(
          constraints:BoxConstraints(maxWidth:math.min(340.0,MediaQuery.sizeOf(context).width*.8)),""",'text bubble stack')
        r=one(r,"""            if(!medyaTepkiKart&&sayilar.isNotEmpty)Padding(
              padding:const EdgeInsets.only(top:7),
              child:Wrap(spacing:5,runSpacing:5,children:sayilar.entries.map((e)=>Container(
                padding:const EdgeInsets.symmetric(horizontal:7,vertical:3),
                decoration:BoxDecoration(color:benimMaviBalon?Colors.white.withValues(alpha:.18):const Color(0xFFF3F4F6),borderRadius:BorderRadius.circular(14)),
                child:Text(e.value>1?e.key+' '+e.value.toString():e.key,style:const TextStyle(fontSize:15)),
              )).toList()),
            ),
""",'','inline reaction removal')
        return one(r,"""          ]),
        ),
      ),
    );
  }

""","""          ]),
        )),
        if(!medyaTepkiKart&&sayilar.isNotEmpty)Positioned(
          bottom:0,right:ben?7:null,left:ben?null:7,
          child:_ozelMedyaTepkiBalonu(d.reference,sayilar,tepkiler.length),
        ),
        ]),
      ),
    );
  }

""",'text bubble overlay close')
    s=scoped(s,'  Widget _ozelMesajKarti435(','  Future<void> _hikayeYanitKartiAc(',bubble)
    def composer(r):
        r=one(r,"""                      icon:const Icon(Icons.add_circle,color:ngelxPrivateBlue,size:29),
                    ),
                    // Build465: one-tap camera and gallery,""",
        """                      icon:const Icon(Icons.add_circle,color:ngelxPrivateBlue,size:26),
                      padding:EdgeInsets.zero,
                      constraints:const BoxConstraints.tightFor(width:38,height:44),
                    ),
                    // Build465: one-tap camera and gallery,""",'plus action')
        r=one(r,"""                      icon:const Icon(Icons.mic_rounded,color:ngelxPrivateBlue),
                        );""",
        """                      icon:const Icon(Icons.mic_rounded,color:ngelxPrivateBlue,size:23),
                          padding:EdgeInsets.zero,
                          constraints:const BoxConstraints.tightFor(width:36,height:44),
                        );""",'microphone')
        r=one(r,"""                            icon:Text(hizliEmoji,style:const TextStyle(fontSize:27)),
                          );""",
        """                            icon:Text(hizliEmoji,style:const TextStyle(fontSize:25)),
                            padding:EdgeInsets.zero,
                            constraints:const BoxConstraints.tightFor(width:38,height:44),
                          );""",'quick emoji')
        r=one(r,"""                          icon:gonderiliyor
                            ?const SizedBox(width:20,height:20,child:CircularProgressIndicator(strokeWidth:2))
                            :const Icon(Icons.send,color:ngelxPrivateBlue),
                        );""",
        """                          icon:gonderiliyor
                            ?const SizedBox(width:20,height:20,child:CircularProgressIndicator(strokeWidth:2))
                            :const Icon(Icons.send,color:ngelxPrivateBlue),
                          padding:EdgeInsets.zero,
                          constraints:const BoxConstraints.tightFor(width:38,height:44),
                        );""",'send')
        r=one(r,'        :SafeArea(top:false,child:Container(','        :SafeArea(top:false,minimum:const EdgeInsets.only(bottom:7),child:Container(','navigation safe inset')
        r=one(r,'        padding:const EdgeInsets.fromLTRB(5,8,5,9),','        padding:const EdgeInsets.fromLTRB(4,7,4,8),','composer padding')
        for method in ('camera','gallery'):
            r=one(r,"""                      constraints:const BoxConstraints.tightFor(width:36,height:44),
                      onPressed:ekIslemiSuruyor?null:()=>medyaGonder(ImageSource."""+method+"""),""",
            """                      constraints:const BoxConstraints.tightFor(width:33,height:44),
                      onPressed:ekIslemiSuruyor?null:()=>medyaGonder(ImageSource."""+method+"""),""",'attachment '+method)
        return r
    s=scoped(s,'class _SohbetPageState','class NgelXSesliMesaj',composer)
    old="""    var ticks=0;
    _ngelx465OpeningScrollTimer=Timer.periodic(
      const Duration(milliseconds:140),(timer){
        if(!mounted||++ticks>16){"""
    assert s.count(old)==2,'opening scroll timer drift'
    s=s.replace(old,old.replace('>16','>3'))
    s=scoped(s,'class TamEkranVideoPage','class GrupMedyaPage',
       lambda r:one(r,'    backgroundColor:Colors.black,\n    appBar:AppBar(backgroundColor:Colors.black,foregroundColor:Colors.white,elevation:0),',
          '    backgroundColor:Colors.black,\n    extendBodyBehindAppBar:true,\n    appBar:AppBar(backgroundColor:Colors.transparent,foregroundColor:Colors.white,elevation:0),',
          'centered fullscreen video'))
    return s

if __name__=='__main__':
    before=P.read_text(encoding='utf-8')
    after=transform(before)
    if after!=before:P.write_text(after,encoding='utf-8')
    print('Build467: shared bounded photos, compact composer, anchored reactions, stable scroll, centered video')
