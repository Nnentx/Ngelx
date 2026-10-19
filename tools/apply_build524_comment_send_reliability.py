#!/usr/bin/env python3
"""Build524 QA: keep live comment drafts until the server confirms the write."""
from pathlib import Path
FILE=Path('app/lib/live_broadcast_studio.dart')
MARK='// Build524: preserve draft and transaction retry after uncertain comment send'
METHOD=r"""
  // Build524: preserve draft and transaction retry after uncertain comment send.
  bool _sendingComment524=false;
  String? _pendingCommentSignature524;
  String? _pendingCommentId524;

  Future<void> _yorumGonder() async {
    if(_sendingComment524)return;
    final metin=yorum.text.trim();
    final user=FirebaseAuth.instance.currentUser;
    if(metin.isEmpty||user==null||!mounted)return;
    setState(()=>_sendingComment524=true);
    try{
      final ref=FirebaseFirestore.instance.collection('live_streams')
          .doc(widget.belgeId);
      final canli=await ref.get(const GetOptions(source:Source.server));
      if(!mounted)return;
      final v=canli.data()??<String,dynamic>{};
      if(!canli.exists||v['active']!=true){
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
          content:Text('Canlı yayın sona ermiş. Yorum gönderilmedi.')));
        return;
      }
      if(!widget.yayinSahibi&&v['commentsEnabled']==false){
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
          content:Text('Yayıncı yorumları kapattı.')));
        return;
      }
      if(!widget.yayinSahibi&&
         List<String>.from(v['mutedUsers']??const[]).contains(user.uid)){
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
          content:Text('Bu yayında yorum yapman susturuldu.')));
        return;
      }
      final yavas=(v['slowModeSeconds'] as num?)?.toInt()??0;
      if(!widget.yayinSahibi&&yavas>0&&sonYorumZamani!=null){
        final kalan=yavas-DateTime.now().difference(sonYorumZamani!).inSeconds;
        if(kalan>0){
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            content:Text('Yavaş mod açık. $kalan saniye bekle.')));
          return;
        }
      }
      final signature='${widget.belgeId}|${user.uid}|$metin';
      final comments=ref.collection('comments');
      final previous=_pendingCommentSignature524==signature
          ?_pendingCommentId524:null;
      final event=previous==null?comments.doc():comments.doc(previous);
      _pendingCommentId524=event.id;
      _pendingCommentSignature524=signature;
      String username=user.displayName??'ngelx';
      try{
        final profile=await FirebaseFirestore.instance
            .collection('users').doc(user.uid).get();
        username=(profile.data()?['username']??username).toString();
      }catch(_){}
      await FirebaseFirestore.instance.runTransaction<bool>((tx)async{
        final existing=await tx.get(event);
        if(existing.exists){
          final saved=existing.data()??<String,dynamic>{};
          if(saved['kind']!='comment'||saved['uid']!=user.uid||
             saved['userId']!=user.uid||saved['text']!=metin){
            throw StateError('live_comment_retry_mismatch');
          }
          return true;
        }
        tx.set(event,<String,dynamic>{
          'uid':user.uid,'userId':user.uid,'username':username,
          'text':metin,'kind':'comment',
          'isHost':widget.yayinSahibi,
          'role':widget.yayinSahibi?'host':'viewer',
          'createdAt':FieldValue.serverTimestamp(),
        });
        return false;
      },maxAttempts:4);
      sonYorumZamani=DateTime.now();
      _pendingCommentId524=null;
      _pendingCommentSignature524=null;
      if(yorum.text.trim()==metin)yorum.clear();
    }catch(_){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
        content:Text('Yorum doğrulanamadı. Metin korundu; tekrar deneyebilirsin.')));
    }finally{
      if(mounted)setState(()=>_sendingComment524=false);
    }
  }
"""

def exactly_one(src,old,new,description):
    count=src.count(old)
    if count!=1:raise RuntimeError(f'Build524 {description}: expected 1 anchor, got {count}')
    return src.replace(old,new,1)

def transform(src):
    if MARK in src:return src
    a=src.index('class _CanliYayinPageState extends State<CanliYayinPage> {')
    b=src.index('\nclass _CanliOzetSatiri extends StatelessWidget',a)
    live=src[a:b]
    for expected in (
        'Build510: manual livestream comment scrolling',
        'Build513: sequential confirmed gift animation queue',
        'Build514: cursor-paged read-only comment history',
        "bool.fromEnvironment('NGELX_VIRTUAL_GIFT_STAGING',defaultValue:false)",
        '_commentScroll510','_giftQueue513','_guestRail488()'):
        if expected not in live:raise RuntimeError('Build524 missing parent feature '+expected)
    old_start=live.index('  Future<void> _yorumGonder() async {')
    old_end=live.index('  @override\n  void dispose()',old_start)
    old=live[old_start:old_end]
    if 'yorum.clear();' not in old or "collection('comments').add({" not in old:
        raise RuntimeError('Build524 previous send method changed')
    live=live[:old_start]+METHOD+live[old_end:]
    live=exactly_one(live,'onSubmitted:etkin?(_)=>_yorumGonder():null',
        'onSubmitted:etkin&&!_sendingComment524?(_)=>_yorumGonder():null',
        'disable submit while busy')
    live=exactly_one(live,'onPressed:etkin?_yorumGonder:null',
        'onPressed:etkin&&!_sendingComment524?_yorumGonder:null',
        'disable double tap')
    for token in ('_yorumYonet(d.id,y)','_giftHistory512()',
                  '_newCommentChip510()','_commentHistory514()',
                  'yorum.dispose()','_yorumGirisAlani()'):
        if token not in live:raise RuntimeError('Build524 lost '+token)
    result=src[:a]+live+src[b:]
    if result.count(MARK)!=1:raise RuntimeError('Build524 marker duplicate')
    return result

if __name__=='__main__':
    prev=FILE.read_text(encoding='utf-8')
    new=transform(prev)
    if prev!=new:FILE.write_text(new,encoding='utf-8')
    print('Build524 QA: safe draft, one pending event ID, transaction retry; prod unchanged')
