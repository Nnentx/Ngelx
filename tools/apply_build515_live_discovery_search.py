#!/usr/bin/env python3
"""Build515: bounded live-search sheet in the existing Keşfet live card.

No new Firestore indexes, search services, extra permissions, LiveKit tokens,
camera or server writes. Uses the existing ngelxCanliYayinaKatil join path.
"""
from pathlib import Path

FILE=Path('app/lib/live_feed_card.dart')
MARK='// Build515: bounded active-live search within the Keşfet card'

SEARCH=r"""
// Build515: bounded active-live search within the Keşfet card.
// This first QA version searches at most 60 active livestreams that the
// Firestore query returned. It is NOT an exhaustive full-database search.
Future<void> ngelxCanliAramaAc(BuildContext context) async {
  final selected=await showModalBottomSheet<String>(
    context:context,
    isScrollControlled:true,
    backgroundColor:const Color(0xFF171521),
    showDragHandle:true,
    builder:(_)=>const _NgelxCanliAramaSheet515(),
  );
  if(selected==null||selected.isEmpty||!context.mounted)return;
  // Do not create another LiveKit room/token implementation. Reuse the
  // existing listener/join path, including its session/error guards.
  ngelxCanliYayinaKatil(context,selected);
}

class _NgelxCanliAramaSheet515 extends StatefulWidget{
  const _NgelxCanliAramaSheet515();
  @override State<_NgelxCanliAramaSheet515> createState()=>_NgelxCanliAramaSheet515State();
}

class _NgelxCanliAramaSheet515State extends State<_NgelxCanliAramaSheet515>{
  final TextEditingController _search515=TextEditingController();
  @override void dispose(){
    _search515.dispose();
    super.dispose();
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
            onChanged:(_)=>setState((){}),
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
                onPressed:(){_search515.clear();setState((){});},
              ),
            ),
          ),
          const SizedBox(height:7),
          const Text('İlk 60 aktif yayında arama · sonuçlar gerçek zamanlı güncellenir',
            style:TextStyle(color:Colors.white60,fontSize:11)),
          const SizedBox(height:10),
          Expanded(child:StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
            stream:FirebaseFirestore.instance.collection('live_streams')
              .where('active',isEqualTo:true).limit(60).snapshots(),
            builder:(_,snapshot){
              if(snapshot.hasError){
                return const Center(child:Text(
                  'Canlı yayınlar yüklenemedi. Ağ bağlantını kontrol et.',
                  textAlign:TextAlign.center,
                  style:TextStyle(color:Colors.white70)));
              }
              if(!snapshot.hasData){
                return const Center(child:CircularProgressIndicator(
                  color:Color(0xFFFF607E)));
              }
              final rooms=snapshot.data!.docs.where((d){
                final data=d.data();
                if(!ngelxCanliKaydiTaze(data))return false;
                if(needle.isEmpty)return true;
                final title=(data['title']??'').toString().toLowerCase();
                final username=(data['username']??'').toString().toLowerCase();
                return title.contains(needle)||username.contains(
                  needle.startsWith('@')?needle.substring(1):needle);
              }).toList()
                ..sort((a,b){
                  final one=(a.data()['viewerCount'] as num?)?.toInt()??0;
                  final two=(b.data()['viewerCount'] as num?)?.toInt()??0;
                  return two.compareTo(one);
                });
              if(rooms.isEmpty){
                return Center(child:Text(
                  needle.isEmpty?'Şu anda görüntülenecek aktif yayın yok.':'Eşleşen aktif yayın bulunamadı.',
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

def once(source,old,new,label):
    count=source.count(old)
    if count!=1:raise RuntimeError(f'Build515 {label}: expected one match, found {count}')
    return source.replace(old,new,1)

def transform(source):
    if MARK in source:return source
    if "part of 'main.dart';" not in source or 'class NgelXAkisCanliKarti extends StatelessWidget' not in source:
        raise RuntimeError('Build515: original live feed card is missing')
    source=once(source,'class NgelXAkisCanliKarti extends StatelessWidget{',
                SEARCH+'class NgelXAkisCanliKarti extends StatelessWidget{',
                'live search sheet declaration')
    anchor="""              child:Stack(fit:StackFit.expand,children:[
                const ColoredBox(color:Color(0xFF111116)),"""
    updated="""              child:Stack(fit:StackFit.expand,children:[
                const ColoredBox(color:Color(0xFF111116)),"""
    # The actual tap target is positioned last in the stack so it wins hit
    # testing over the parent live-card GestureDetector without stopping
    # normal full-card tap-to-join behavior.
    source=once(source,
        "                Positioned(\n                  left:22,right:18,bottom:34,",
        """                Positioned(
                  right:12,top:12,
                  child:SafeArea(child:IconButton.filledTonal(
                    tooltip:'Canlı yayın ara',
                    icon:const Icon(Icons.search_rounded),
                    style:IconButton.styleFrom(
                      backgroundColor:const Color(0xDD22212C),
                      foregroundColor:Colors.white),
                    onPressed:()=>ngelxCanliAramaAc(context),
                  )),
                ),
                Positioned(
                  left:22,right:18,bottom:34,""",
        'search action on Keşfet live card')
    for token in (
      "where('active',isEqualTo:true).limit(60).snapshots()",
      "ngelxCanliKaydiTaze(data)",
      "title.contains(needle)",
      "onPressed:()=>ngelxCanliAramaAc(context)",
      "onTap:()=>Navigator.pop(context,d.id)",
      "ngelxCanliYayinaKatil(context,selected)",
      "onTap:canli?()=>ngelxCanliYayinaKatil(context,liveId)",
      'İlk 60 aktif yayında arama',
    ):
        if token not in source:raise RuntimeError('Build515 missing important existing/search control '+token)
    if source.count(MARK)!=1:raise RuntimeError('Build515 duplicate insertion')
    return source

if __name__=='__main__':
    original=FILE.read_text(encoding='utf-8')
    updated=transform(original)
    if updated!=original:FILE.write_text(updated,encoding='utf-8')
    print('Build515: 60 active live discovery cards, search title/username, use existing join; QA-only')
