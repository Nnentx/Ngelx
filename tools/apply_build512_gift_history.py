#!/usr/bin/env python3
"""Build512: browse older public gift events without altering payment or media."""
from pathlib import Path

FILE=Path('app/lib/live_broadcast_studio.dart')
MARK='// Build512: paged read-only gift history'

METHOD=r"""
  // Build512: paged read-only gift history.
  // Pages the existing public live_streams/{id}/comments timeline without
  // requiring a Firestore composite index or a new collection. Older events
  // are loaded only after a deliberate tap, capped at 50 events per read.
  Future<void> _giftHistory512() async {
    final feed=FirebaseFirestore.instance.collection('live_streams')
        .doc(widget.belgeId).collection('comments');
    QuerySnapshot<Map<String,dynamic>> first;
    try{
      first=await feed.orderBy('createdAt',descending:true).limit(50).get();
    }catch(_){
      if(mounted){
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content:Text('Hediye geçmişi yüklenemedi.')));
      }
      return;
    }
    if(!mounted)return;
    final gifts=<QueryDocumentSnapshot<Map<String,dynamic>>>[
      ...first.docs.where((d)=>d.data()['kind']=='gift'),
    ];
    QueryDocumentSnapshot<Map<String,dynamic>>? last=
      first.docs.isEmpty?null:first.docs.last;
    bool more=first.docs.length==50;
    bool loading=false;
    String? error;

    await showModalBottomSheet<void>(
      context:context,isScrollControlled:true,
      backgroundColor:const Color(0xFF17131F),
      showDragHandle:true,
      builder:(sheetContext)=>StatefulBuilder(builder:(c,refresh){
        Future<void> moreGifts() async {
          if(loading||!more||last==null)return;
          refresh(()=>loading=true);
          try{
            final page=await feed.orderBy('createdAt',descending:true)
              .startAfterDocument(last!).limit(50).get();
            if(!c.mounted)return;
            refresh((){
              gifts.addAll(page.docs.where((d)=>d.data()['kind']=='gift'));
              if(page.docs.isNotEmpty)last=page.docs.last;
              more=page.docs.length==50;
              error=null;
            });
          }catch(_){
            if(c.mounted)refresh(()=>error='Daha eski hediyeler yüklenemedi.');
          }finally{
            if(c.mounted)refresh(()=>loading=false);
          }
        }
        return SafeArea(child:FractionallySizedBox(
          heightFactor:.72,
          child:Padding(
            padding:const EdgeInsets.fromLTRB(16,4,16,16),
            child:Column(crossAxisAlignment:CrossAxisAlignment.stretch,children:[
              Row(children:[
                const Icon(Icons.card_giftcard_rounded,color:Color(0xFFFFD46D)),
                const SizedBox(width:8),
                const Expanded(child:Text('Hediye geçmişi',
                  style:TextStyle(color:Colors.white,fontSize:19,fontWeight:FontWeight.w900))),
                IconButton(onPressed:()=>Navigator.pop(sheetContext),
                  tooltip:'Kapat',icon:const Icon(Icons.close_rounded,color:Colors.white)),
              ]),
              const Text('Gönderen · Hediye · Adet · Zaman',
                style:TextStyle(color:Colors.white60,fontSize:12)),
              const SizedBox(height:10),
              Expanded(child:gifts.isEmpty
                ?Center(child:Text(more?'Bu sayfada hediye yok. Daha eski kayıtları aç.':'Hediye kaydı bulunamadı.',
                  style:const TextStyle(color:Colors.white70),textAlign:TextAlign.center))
                :ListView.separated(
                  itemCount:gifts.length,
                  separatorBuilder:(_,__)=>const Divider(color:Colors.white12,height:1),
                  itemBuilder:(_,i){
                    final d=gifts[i].data();
                    final created=d['createdAt'];
                    final stamp=created is Timestamp?created.toDate():null;
                    final date=stamp==null?'Zaman bilinmiyor':
                      stamp.day.toString().padLeft(2,'0')+'.'+
                      stamp.month.toString().padLeft(2,'0')+'.'+
                      stamp.year.toString()+' '+
                      stamp.hour.toString().padLeft(2,'0')+':'+
                      stamp.minute.toString().padLeft(2,'0');
                    final qty=((d['quantity'] as num?)?.toInt()??1).clamp(1,10);
                    return ListTile(
                      contentPadding:const EdgeInsets.symmetric(horizontal:4),
                      leading:Text((d['giftEmoji']??'🎁').toString(),
                        style:const TextStyle(fontSize:28)),
                      title:Text((d['giftName']??'N-Hediye').toString()+' ×'+qty.toString(),
                        style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w800)),
                      subtitle:Text((d['username']??'ngelx').toString()+' · '+date,
                        maxLines:2,overflow:TextOverflow.ellipsis,
                        style:const TextStyle(color:Colors.white70,fontSize:11)),
                    );
                  },
                )),
              if(error!=null)Text(error!,style:const TextStyle(color:Colors.orangeAccent)),
              if(more)Padding(padding:const EdgeInsets.only(top:10),
                child:FilledButton.tonalIcon(
                  onPressed:loading?null:moreGifts,
                  icon:loading
                    ?const SizedBox(width:16,height:16,child:CircularProgressIndicator(strokeWidth:2))
                    :const Icon(Icons.history_rounded),
                  label:Text(loading?'Yükleniyor…':'Daha eski hediyeleri getir'),
                )),
            ]),
          ),
        ));
      }),
    );
  }

"""
def once(src,old,new,tag):
    n=src.count(old)
    if n!=1:raise RuntimeError(f'Build512 {tag}: expected one anchor, got {n}')
    return src.replace(old,new,1)

def transform(src):
    if MARK in src:return src
    start=src.index('class _CanliYayinPageState extends State<CanliYayinPage> {')
    end=src.index('\nclass _CanliOzetSatiri extends StatelessWidget',start)
    left,view,right=src[:start],src[start:end],src[end:]
    if '// Build511 QA gift event animations' not in view:
        raise RuntimeError('Build512 must follow Build511 generated live gift UI')
    view=once(view,'  Future<void> _hediyePaneli() async {',
              METHOD+'  Future<void> _hediyePaneli() async {','history helper')
    view=once(view,
        "return Text('🎁 $n',style:const TextStyle(color:Colors.white,fontSize:11,fontWeight:FontWeight.w800));",
        """return Semantics(button:true,label:'Toplam hediye $n, geçmişi aç',
                      child:InkWell(
                        onTap:_giftHistory512,
                        borderRadius:BorderRadius.circular(16),
                        child:Padding(padding:const EdgeInsets.symmetric(horizontal:7,vertical:6),
                          child:Text('🎁 $n',style:const TextStyle(
                            color:Colors.white,fontSize:11,fontWeight:FontWeight.w800)))));""",
        'header gift badge opens read-only history')
    for contract in ('_newCommentChip510()','_giftScreen511()',
                     '_guestRail488()','_kalpDegistir()',
                     "'giftCount'","_giftHistory512",
                     'startAfterDocument(last!)',
                     'onPressed:loading?null:moreGifts'):
        if contract not in view:
            raise RuntimeError('Build512 lost existing function: '+contract)
    result=left+view+right
    if result.count(MARK)!=1:
        raise RuntimeError('Build512 marker count not one')
    return result

if __name__=='__main__':
    original=FILE.read_text(encoding='utf-8')
    updated=transform(original)
    if updated!=original:
        FILE.write_text(updated,encoding='utf-8')
    print('Build512 gift history: read-only cursor pagination on public comments')
