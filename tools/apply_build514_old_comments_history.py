#!/usr/bin/env python3
"""Build514 QA: read comments older than the last 100 live events, in pages.

The Build510 panel stays connected to real-time Firestore. History is a separate
read-only overlay queried only when the user taps 'Eski yorumlar'. No new index,
server write, payment, microphone, camera or production changes.
"""
from pathlib import Path

FILE=Path('app/lib/live_broadcast_studio.dart')
MARK='// Build514: cursor-paged read-only comment history'

METHOD=r"""
  // Build514: cursor-paged read-only comment history.
  Future<void> _commentHistory514() async {
    final ref=FirebaseFirestore.instance.collection('live_streams')
      .doc(widget.belgeId).collection('comments');
    QuerySnapshot<Map<String,dynamic>> first;
    try{
      first=await ref.orderBy('createdAt',descending:true).limit(50).get();
    }catch(_){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content:Text('Eski yorumlar yüklenemedi.')));
      return;
    }
    if(!mounted)return;
    final events=<QueryDocumentSnapshot<Map<String,dynamic>>>[...first.docs];
    QueryDocumentSnapshot<Map<String,dynamic>>? last=
      first.docs.isEmpty?null:first.docs.last;
    bool hasMore=first.docs.length==50;
    bool loading=false;
    String? message;
    await showModalBottomSheet<void>(
      context:context,
      isScrollControlled:true,
      backgroundColor:const Color(0xFF191523),
      showDragHandle:true,
      builder:(sheetContext)=>StatefulBuilder(builder:(c,refresh){
        Future<void> loadOlder() async {
          if(loading||!hasMore||last==null)return;
          refresh(()=>loading=true);
          try{
            final page=await ref.orderBy('createdAt',descending:true)
              .startAfterDocument(last!).limit(50).get();
            if(!c.mounted)return;
            refresh((){
              final known=events.map((d)=>d.id).toSet();
              events.addAll(page.docs.where((d)=>!known.contains(d.id)));
              if(page.docs.isNotEmpty)last=page.docs.last;
              hasMore=page.docs.length==50;
              message=null;
            });
          }catch(_){
            if(c.mounted)refresh(()=>message='Eski yorumlar yüklenemedi, tekrar dene.');
          }finally{
            if(c.mounted)refresh(()=>loading=false);
          }
        }
        return SafeArea(child:FractionallySizedBox(
          heightFactor:.76,
          child:Padding(
            padding:const EdgeInsets.fromLTRB(12,4,12,14),
            child:Column(crossAxisAlignment:CrossAxisAlignment.stretch,children:[
              Row(children:[
                const Icon(Icons.forum_outlined,color:Color(0xFFFFD46D)),
                const SizedBox(width:8),
                const Expanded(child:Text('Canlı yorum geçmişi',
                  maxLines:1,overflow:TextOverflow.ellipsis,
                  style:TextStyle(color:Colors.white,fontSize:18,fontWeight:FontWeight.w900))),
                IconButton(tooltip:'Kapat',onPressed:()=>Navigator.pop(sheetContext),
                  icon:const Icon(Icons.close_rounded,color:Colors.white)),
              ]),
              const Text('Yeni mesajlar üstte · Eski mesajlar aşağıda',
                style:TextStyle(color:Colors.white60,fontSize:11)),
              const SizedBox(height:7),
              Expanded(child:events.isEmpty
                ?const Center(child:Text('Henüz yorum bulunamadı.',
                    style:TextStyle(color:Colors.white70)))
                :ListView.builder(
                  itemCount:events.length,
                  itemBuilder:(_,i){
                    final event=events[i].data();
                    final kind=(event['kind']??'comment').toString();
                    final name=(event['username']??'İzleyici').toString();
                    final text=kind=='join'
                      ?'Yayına katıldı 👋'
                      :(event['text']??'').toString();
                    final timestamp=event['createdAt'];
                    final date=timestamp is Timestamp?timestamp.toDate():null;
                    final when=date==null?'Zaman bilinmiyor':
                      date.day.toString().padLeft(2,'0')+'.'+
                      date.month.toString().padLeft(2,'0')+' '+
                      date.hour.toString().padLeft(2,'0')+':'+
                      date.minute.toString().padLeft(2,'0');
                    return Padding(
                      padding:const EdgeInsets.symmetric(vertical:4),
                      child:Container(
                        padding:const EdgeInsets.symmetric(horizontal:10,vertical:7),
                        decoration:BoxDecoration(color:const Color(0xC52C2940),
                          borderRadius:BorderRadius.circular(12)),
                        child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                          Row(children:[
                            Expanded(child:Text(name,maxLines:1,overflow:TextOverflow.ellipsis,
                              style:const TextStyle(color:Colors.white,fontWeight:FontWeight.w800,fontSize:12))),
                            Text(when,style:const TextStyle(color:Colors.white54,fontSize:10)),
                          ]),
                          const SizedBox(height:3),
                          Text(text,maxLines:8,overflow:TextOverflow.ellipsis,
                            style:const TextStyle(color:Colors.white,fontSize:12)),
                          if(kind=='gift')const Text('🎁 Hediye',
                            style:TextStyle(color:Color(0xFFFFD46D),fontSize:10)),
                        ]),
                      ),
                    );
                  },
                )),
              if(message!=null)Text(message!,
                  style:const TextStyle(color:Colors.orangeAccent,fontSize:11)),
              if(hasMore)Padding(padding:const EdgeInsets.only(top:9),
                child:FilledButton.tonalIcon(
                  onPressed:loading?null:loadOlder,
                  icon:loading
                    ?const SizedBox(width:16,height:16,child:CircularProgressIndicator(strokeWidth:2))
                    :const Icon(Icons.history_rounded),
                  label:Text(loading?'Yükleniyor…':'Daha eski yorumları getir'),
                )),
              const SizedBox(height:5),
              const Text('Arşiv salt okunurdur; canlı yorumlar ve yeni mesaj sayacı yayında çalışmaya devam eder.',
                maxLines:2,style:TextStyle(color:Colors.white54,fontSize:10)),
            ]),
          ),
        ));
      }),
    );
  }

"""

def one(source,old,new,label):
    count=source.count(old)
    if count!=1:raise RuntimeError(f'Build514 {label}: expected one anchor, got {count}')
    return source.replace(old,new,1)

def transform(src):
    if MARK in src:return src
    a=src.index('class _CanliYayinPageState extends State<CanliYayinPage> {')
    b=src.index('\nclass _CanliOzetSatiri extends StatelessWidget',a)
    left,live,right=src[:a],src[a:b],src[b:]
    for prior in ('Build510: manual livestream comment scrolling',
                  'Build513: sequential confirmed gift animation queue',
                  'Build512: paged read-only gift history'):
        if prior not in live:raise RuntimeError('Build514 missing required parent: '+prior)
    live=one(live,'  Widget _commentSection490(){',
             METHOD+'  Widget _commentSection490(){',
             'older live comment history helper')
    live=one(live,
        'if(!_commentsHidden490)_newCommentChip510(),',
        """if(!_commentsHidden490)_newCommentChip510(),
        if(!_commentsHidden490)Align(alignment:Alignment.centerRight,
          child:TextButton.icon(
            onPressed:_commentHistory514,
            icon:const Icon(Icons.history_rounded,size:15),
            label:const Text('Eski yorumlar',style:TextStyle(fontSize:11)),
            style:TextButton.styleFrom(
              foregroundColor:Colors.white,
              padding:const EdgeInsets.symmetric(horizontal:6,vertical:0)),
          )),""",
        'history button alongside existing live controls')
    for expected in (
      "startAfterDocument(last!).limit(50).get()",
      "events.addAll(page.docs.where((d)=>!known.contains(d.id)))",
      "onPressed:loading?null:loadOlder",
      "onPressed:_commentHistory514",
      "if(!_commentsHidden490)_newCommentChip510()",
      "_commentScroll510",
      "_giftHistory512()",
      "_giftScreen511()",
      "_showNextGift513()",
      "_guestRail488()",
      "_yorumYonet(d.id,y)",
      "bool.fromEnvironment('NGELX_VIRTUAL_GIFT_STAGING',defaultValue:false)",
    ):
        if expected not in live:
            raise RuntimeError('Build514 missing preserved feature: '+expected)
    result=left+live+right
    if result.count(MARK)!=1:raise RuntimeError('Build514 marker duplicated')
    return result

if __name__=='__main__':
    old=FILE.read_text(encoding='utf-8')
    new=transform(old)
    if new!=old:FILE.write_text(new,encoding='utf-8')
    print('Build514 QA: read-only older comments, cursor paging 50 events/read, live video/comment/gift guards retained')
