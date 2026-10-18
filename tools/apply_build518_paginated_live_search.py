#!/usr/bin/env python3
"""Build518: cursor-scan all active streams on demand, beyond Build515's 60.
Read-only QA implementation. For large scale replace with a server index;
do NOT change production Firestore or deployment here.
"""
from pathlib import Path

FILE=Path('app/lib/live_feed_card.dart')
MARK='// Build518: paginated all-active live search (on demand, read only)'
SEARCH=r"""
// Build518: paginated all-active live search (on demand, read only).
// Do not suggest the first-page listener is a server-side title index.
class _NgelxCanliAramaSheet515State extends State<_NgelxCanliAramaSheet515>{
  final TextEditingController _search515=TextEditingController();
  late final Stream<QuerySnapshot<Map<String,dynamic>>> _activeRooms515=
    FirebaseFirestore.instance.collection('live_streams')
      .where('active',isEqualTo:true).limit(60).snapshots();

  final Map<String,QueryDocumentSnapshot<Map<String,dynamic>>> _pages518={};
  Timer? _scanDelay518;
  bool _scanStarted518=false,_scanRunning518=false,_scanDone518=false;
  String? _scanError518;
  int _pagesRead518=0;

  @override void dispose(){
    _scanDelay518?.cancel();
    _search515.dispose();
    super.dispose();
  }

  void _queryChanged518(String ignored){
    _scanDelay518?.cancel();
    setState((){});
    if(_search515.text.trim().isNotEmpty&&!_scanStarted518){
      // One scan per opened sheet, not another full read on each keystroke.
      _scanDelay518=Timer(const Duration(milliseconds:500),(){
        if(mounted&&_search515.text.trim().isNotEmpty)unawaited(_scanAll518());
      });
    }
  }

  Future<void> _scanAll518()async{
    if(_scanRunning518||_scanStarted518)return;
    setState((){
      _scanStarted518=true;
      _scanRunning518=true;
      _scanDone518=false;
      _scanError518=null;
    });
    DocumentSnapshot<Map<String,dynamic>>? cursor;
    try{
      while(mounted){
        Query<Map<String,dynamic>> query=FirebaseFirestore.instance
          .collection('live_streams').where('active',isEqualTo:true)
          .orderBy(FieldPath.documentId).limit(60);
        if(cursor!=null)query=query.startAfterDocument(cursor);
        final page=await query.get();
        if(!mounted)return;
        final docs=page.docs;
        setState((){
          _pagesRead518++;
          for(final d in docs){_pages518[d.id]=d;}
        });
        if(docs.length<60){
          if(mounted)setState(()=>_scanDone518=true);
          break;
        }
        // startAfterDocument guarantees progress even if the last page has
        // exactly 60 documents. This is a finite paginated read, not limit(60).
        cursor=docs.last;
      }
    }catch(_){
      if(mounted)setState(()=>
        _scanError518='Bütün canlı yayınlar taranamadı. Bağlantını kontrol edip tekrar dene.');
    }finally{
      if(mounted)setState(()=>_scanRunning518=false);
    }
  }

  void _retry518(){
    _scanDelay518?.cancel();
    setState((){
      _scanStarted518=false;
      _scanDone518=false;
      _scanError518=null;
      _pagesRead518=0;
      _pages518.clear();
    });
    unawaited(_scanAll518());
  }

  @override Widget build(BuildContext context){
    final needle=_search515.text.trim().toLowerCase();
    return SafeArea(child:FractionallySizedBox(
      heightFactor:.85,
      child:Padding(
        padding:const EdgeInsets.fromLTRB(14,4,14,14),
        child:Column(crossAxisAlignment:CrossAxisAlignment.stretch,children:[
          Row(children:[
            const Icon(Icons.live_tv_rounded,color:Color(0xFFFF607E)),
            const SizedBox(width:8),
            const Expanded(child:Text('Canlı yayın ara',
              style:TextStyle(color:Colors.white,fontSize:20,fontWeight:FontWeight.w900))),
            IconButton(tooltip:'Aramayı kapat',
              onPressed:()=>Navigator.pop(context),
              icon:const Icon(Icons.close_rounded,color:Colors.white)),
          ]),
          const SizedBox(height:8),
          TextField(
            controller:_search515,
            autofocus:false,
            onChanged:_queryChanged518,
            maxLength:70,
            style:const TextStyle(color:Colors.white),
            textInputAction:TextInputAction.search,
            decoration:InputDecoration(
              prefixIcon:const Icon(Icons.search_rounded,color:Colors.white70),
              hintText:'Yayın başlığı veya @kullanıcı adı',
              hintStyle:const TextStyle(color:Colors.white54),
              counterText:'',
              filled:true,fillColor:const Color(0xFF302B42),
              border:OutlineInputBorder(borderRadius:BorderRadius.circular(16),
                borderSide:BorderSide.none),
              suffixIcon:_search515.text.isEmpty?null:IconButton(
                tooltip:'Aramayı temizle',
                icon:const Icon(Icons.close_rounded,color:Colors.white70),
                onPressed:(){_search515.clear();_queryChanged518('');},
              ),
            ),
          ),
          const SizedBox(height:7),
          Text(needle.isEmpty
              ?'İlk 60 yayını canlı gösterir; arama yapınca diğer aktif yayınlar da taranır.'
              :_scanError518!=null?'Tarama tamamlanamadı'
              :_scanDone518?'Tüm aktif yayın sayfaları tarandı'
              :'Aktif yayınlar taranıyor… $_pagesRead518 sayfa',
            style:const TextStyle(color:Colors.white60,fontSize:11)),
          if(needle.isNotEmpty&&_scanRunning518)
            const LinearProgressIndicator(minHeight:2,color:Color(0xFFFF607E)),
          if(needle.isNotEmpty&&_scanError518!=null)
            TextButton.icon(onPressed:_retry518,icon:const Icon(Icons.refresh),
              label:const Text('Tüm yayınları yeniden tara')),
          const SizedBox(height:10),
          Expanded(child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
            stream:_activeRooms515,
            builder:(_,snapshot){
              if(snapshot.hasError&&needle.isEmpty){
                return const Center(child:Text('Canlı yayınlar yüklenemedi.',
                  style:TextStyle(color:Colors.white70)));
              }
              if(!snapshot.hasData&&needle.isEmpty){
                return const Center(child:CircularProgressIndicator(
                  color:Color(0xFFFF607E)));
              }
              // Prefer fresh first-page listener data. All subsequent pages
              // were read as an on-demand snapshot, not a global live index.
              final merged=<String,QueryDocumentSnapshot<Map<String,dynamic>>>{
                if(needle.isNotEmpty)..._pages518,
                for(final d in snapshot.data?.docs??<QueryDocumentSnapshot<Map<String,dynamic>>>[])
                  d.id:d,
              };
              final rooms=merged.values.where((d){
                final data=d.data();
                if(data['active']!=true||!ngelxCanliKaydiTaze(data))return false;
                if(needle.isEmpty)return true;
                final title=(data['title']??'').toString().toLowerCase();
                final username=(data['username']??'').toString().toLowerCase();
                final term=needle.startsWith('@')?needle.substring(1):needle;
                return title.contains(needle)||username.contains(term);
              }).toList()..sort((a,b){
                final one=(a.data()['viewerCount'] as num?)?.toInt()??0;
                final two=(b.data()['viewerCount'] as num?)?.toInt()??0;
                return two.compareTo(one);
              });
              if(rooms.isEmpty){
                return Center(child:Text(
                  needle.isEmpty?'Şu anda aktif yayın yok.':
                  _scanError518!=null?'Arama tamamlanamadı. Yeniden dene.':
                  !_scanDone518?'Tüm aktif yayınlar taranıyor…':
                    'Eşleşen aktif yayın bulunamadı.',
                  textAlign:TextAlign.center,
                  style:const TextStyle(color:Colors.white70,fontSize:13)));
              }
              return ListView.separated(
                keyboardDismissBehavior:ScrollViewKeyboardDismissBehavior.onDrag,
                itemCount:rooms.length,
                separatorBuilder:(_,__)=>const Divider(color:Colors.white12,height:1),
                itemBuilder:(_,i){
                  final d=rooms[i];
                  final data=d.data();
                  final title=(data['title']??'Canlı yayın').toString();
                  final username=(data['username']??'ngelx').toString();
                  final viewers=(data['viewerCount'] as num?)?.toInt()??0;
                  return Semantics(button:true,label:'$title, $username yayınına katıl',
                    child:ListTile(
                      contentPadding:const EdgeInsets.symmetric(horizontal:2,vertical:4),
                      leading:const CircleAvatar(backgroundColor:Color(0xFFFF1744),
                        child:Icon(Icons.live_tv_rounded,color:Colors.white)),
                      title:Text(title,maxLines:2,overflow:TextOverflow.ellipsis,
                        style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w800)),
                      subtitle:Text('@$username  ·  👁 $viewers',
                        maxLines:1,overflow:TextOverflow.ellipsis,
                        style:const TextStyle(color:Colors.white60,fontSize:11)),
                      trailing:const Icon(Icons.chevron_right_rounded,color:Colors.white70),
                      onTap:()=>Navigator.pop(context,d.id),
                    ),
                  );
                },
              );
            },
          )),
        ]),
      ),
    ));
  }
}

"""

def transform(src):
    if MARK in src:return src
    start=src.index('class _NgelxCanliAramaSheet515State extends State<_NgelxCanliAramaSheet515>{')
    end=src.index('class NgelXAkisCanliKarti extends StatelessWidget{',start)
    original=src[start:end]
    for token in ("where('active',isEqualTo:true).limit(60).snapshots()",
                  'ngelxCanliKaydiTaze(data)',
                  'ngelxCanliYayinaKatil(context,selected)'):
        if token not in src:raise RuntimeError('Build518 search/join invariant lost '+token)
    if 'İlk 60 aktif yayında arama' not in original:
        raise RuntimeError('Build518 expects previous bounded search UI')
    src=src[:start]+SEARCH+src[end:]
    assert src.count(MARK)==1
    return src

if __name__=='__main__':
    old=FILE.read_text(encoding='utf-8')
    new=transform(old)
    if new!=old:FILE.write_text(new,encoding='utf-8')
    print('Build518 on-demand paginated active livestream search, all pages, no deployment')
