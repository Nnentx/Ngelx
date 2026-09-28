#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN_PATH=ROOT/'app/lib/main.dart'
PUB_PATH=ROOT/'app/pubspec.yaml'

def one(text,old,new,label):
    n=text.count(old)
    if n!=1:
        raise SystemExit(f'Build 302 patch failed: {label}: expected 1 match, got {n}')
    return text.replace(old,new,1)

def scoped_replace(text,start_marker,end_marker,old,new,label):
    a=text.index(start_marker)
    b=text.index(end_marker,a)
    section=text[a:b]
    n=section.count(old)
    if n!=1:
        raise SystemExit(f'Build 302 patch failed: {label}: expected 1 scoped match, got {n}')
    section=section.replace(old,new,1)
    return text[:a]+section+text[b:]

def scoped_replace_after(text,anchor_marker,start_marker,end_marker,old,new,label):
    root=text.index(anchor_marker)
    a=text.index(start_marker,root)
    b=text.index(end_marker,a)
    section=text[a:b]
    n=section.count(old)
    if n!=1:
        raise SystemExit(f'Build 302 patch failed: {label}: expected 1 anchored match, got {n}')
    section=section.replace(old,new,1)
    return text[:a]+section+text[b:]

main=MAIN_PATH.read_text(encoding='utf-8')
pub=PUB_PATH.read_text(encoding='utf-8')
if 'version: 1.0.83+302' in pub:
    raise SystemExit('Build 302 already applied.')

notify_start=main.index('Future<void> uygulamaBildirimiGonder({')
helper=r'''Future<void> ngelxBatchCommitDogrula({
  required WriteBatch batch,
  required DocumentReference<Map<String,dynamic>> marker,
  Duration timeout=const Duration(seconds:15),
}) async {
  try{
    await batch.commit().timeout(timeout);
    return;
  }on TimeoutException catch(e){
    try{
      await Future<void>.delayed(const Duration(milliseconds:450));
      final sonuc=await marker.get(const GetOptions(source:Source.server))
          .timeout(const Duration(seconds:6));
      if(sonuc.exists)return;
    }catch(_){}
    throw e;
  }
}

String ngelxBildirimBelgeId(String raw){
  final temiz=raw.trim().replaceAll(RegExp(r'[^a-zA-Z0-9_-]'),'_');
  if(temiz.isEmpty)return '';
  return temiz.length<=300?temiz:temiz.substring(0,300);
}

'''
main=main[:notify_start]+helper+main[notify_start:]

a=main.index('Future<void> uygulamaBildirimiGonder({')
b=main.index('final Set<String> _sosyalIstekIslemleri',a)
new_notify=r'''Future<void> uygulamaBildirimiGonder({
  required String toUid,
  required String fromUid,
  required String tur,
  required String metin,
  String? belgeId,
  String? hedefTuru,
  String? hedefBaslik,
  String? hedefFoto,
  String? olayTuru,
  String? onizleme,
  String? eylem,
  String? dedupeKey,
}) async {
  if(toUid==fromUid)return;
  final hedef=await FirebaseFirestore.instance.collection('users').doc(toUid).get();
  final ayar=hedef.data()??{};
  if(List<String>.from(ayar['restrictedUsers']??const[]).contains(fromUid))return;
  if(ayar['notificationsEnabled']==false)return;
  final grupBildirimi=hedefTuru=='group'||tur=='group'||(olayTuru??'').startsWith('group_');
  final sosyalBildirimi=tur=='friend'||tur=='friend_request'||tur=='follow_request'||tur=='friend_accepted'||tur=='follow_accepted';
  final etkilesimBildirimi=tur=='interaction'||tur=='like'||tur=='comment';
  final aramaBildirimi=tur=='call';
  if(grupBildirimi){
    if(ayar['groupNotifications']==false)return;
  }else if(tur=='message'&&ayar['messageNotifications']==false){
    return;
  }
  if(sosyalBildirimi&&ayar['friendNotifications']==false)return;
  if(etkilesimBildirimi&&ayar['interactionNotifications']==false)return;
  if(aramaBildirimi&&ayar['callNotifications']==false)return;
  final sessizeBagli=tur=='message'||tur=='call'||olayTuru=='group_message'||olayTuru=='group_mention';
  if(sessizeBagli&&belgeId!=null&&List<String>.from(ayar['mutedChats']??const[]).contains(belgeId)){
    final ham=(ayar['mutedChatUntil'] is Map)?(ayar['mutedChatUntil'] as Map)[belgeId]:null;
    final bitis=DateTime.tryParse((ham??'').toString());
    if(bitis==null||bitis.isAfter(DateTime.now().toUtc()))return;
  }

  final gonderen=await FirebaseFirestore.instance.collection('users').doc(fromUid).get();
  final gonderenVeri=gonderen.data()??{};
  final gonderenAdi=(gonderenVeri['displayName']??gonderenVeri['username']??'NgelX kullanıcısı').toString();
  final gonderenFoto=(gonderenVeri['photoUrl']??'').toString();
  final payload=<String,dynamic>{
    'toUid':toUid,'fromUid':fromUid,'type':tur,
    'senderName':gonderenAdi,'photoUrl':gonderenFoto,
    'text':'__D__gonderenAdi __D__metin',
    if(belgeId!=null)'sourceId':belgeId,
    if(hedefTuru!=null&&hedefTuru.isNotEmpty)'targetKind':hedefTuru,
    if(hedefBaslik!=null&&hedefBaslik.isNotEmpty)'targetTitle':hedefBaslik,
    if(hedefFoto!=null&&hedefFoto.isNotEmpty)'targetPhotoUrl':hedefFoto,
    if(olayTuru!=null&&olayTuru.isNotEmpty)'eventKind':olayTuru,
    if(onizleme!=null&&onizleme.isNotEmpty)'preview':onizleme,
    if(eylem!=null&&eylem.isNotEmpty)'eventAction':eylem,
    'read':false,'createdAt':FieldValue.serverTimestamp(),
  };

  final bildirimler=FirebaseFirestore.instance.collection('notifications');
  final anahtar=ngelxBildirimBelgeId(dedupeKey??'');
  if(anahtar.isEmpty){
    await bildirimler.add(payload).timeout(const Duration(seconds:10));
    return;
  }

  final doc=bildirimler.doc(anahtar);
  try{
    final mevcut=await doc.get(const GetOptions(source:Source.server))
        .timeout(const Duration(seconds:6));
    if(mevcut.exists)return;
  }catch(_){}

  try{
    await doc.set(payload).timeout(const Duration(seconds:10));
  }catch(e){
    try{
      final mevcut=await doc.get(const GetOptions(source:Source.server))
          .timeout(const Duration(seconds:6));
      if(mevcut.exists)return;
    }catch(_){}
    rethrow;
  }
}

'''
new_notify=new_notify.replace('__D__','$')
main=main[:a]+new_notify+main[b:]

main=scoped_replace(
    main,
    'Future<bool> payloadGonder(',
    'Future<void> gonder()async',
    '      await batch.commit();',
    """      await ngelxBatchCommitDogrula(
        batch:batch,
        marker:mesajRef,
        timeout:const Duration(seconds:15),
      );""",
    'group message commit verification',
)
main=scoped_replace(
    main,
    'Future<bool> payloadGonder(',
    'Future<void> gonder()async',
    """            eylem:bildirimEylemi,
          ).catchError((_){ }));""",
    """            eylem:bildirimEylemi,
            dedupeKey:'group_msg___D__{widget.chatId}___D__{mesajRef.id}___D__hedef',
          ).catchError((_){ }));""".replace('__D__','$'),
    'group message notification dedupe',
)
main=scoped_replace(
    main,
    'Future<bool> payloadGonder(',
    'Future<void> gonder()async',
    """              olayTuru:'group_mention',
            ).catchError((_){ }));""",
    """              olayTuru:'group_mention',
              dedupeKey:'group_mention___D__{widget.chatId}___D__{mesajRef.id}___D__hedef',
            ).catchError((_){ }));""".replace('__D__','$'),
    'group mention notification dedupe',
)

main=scoped_replace_after(
    main,
    'class _SohbetPageState',
    'Future<void> gonder() async {',
    'Future<void> medyaGonder(ImageSource kaynak) async {',
    '      await batch.commit().timeout(const Duration(seconds:12));',
    """      await ngelxBatchCommitDogrula(
        batch:batch,
        marker:mesajRef,
        timeout:const Duration(seconds:12),
      );""",
    'private text commit verification',
)
main=scoped_replace_after(
    main,
    'class _SohbetPageState',
    'Future<void> gonder() async {',
    'Future<void> medyaGonder(ImageSource kaynak) async {',
    """      unawaited(uygulamaBildirimiGonder(toUid:widget.digerUid,fromUid:ben,tur:'message',metin:'Yeni bir mesajın var',belgeId:widget.chatId).catchError((_){ }));""",
    """      unawaited(uygulamaBildirimiGonder(
        toUid:widget.digerUid,fromUid:ben,tur:'message',metin:'Yeni bir mesajın var',
        belgeId:widget.chatId,
        dedupeKey:'private_msg___D__{widget.chatId}___D__{mesajRef.id}___D__{widget.digerUid}',
      ).catchError((_){ }));""".replace('__D__','$'),
    'private text notification dedupe',
)

main=scoped_replace_after(
    main,
    'class _SohbetPageState',
    'Future<void> medyaGonder(ImageSource kaynak) async {',
    'Future<void> videoGonder(ImageSource kaynak)async{',
    '      await batch.commit().timeout(const Duration(seconds:20));',
    """      await ngelxBatchCommitDogrula(
        batch:batch,
        marker:mesajRef,
        timeout:const Duration(seconds:20),
      );""",
    'private photo commit verification',
)
main=scoped_replace_after(
    main,
    'class _SohbetPageState',
    'Future<void> medyaGonder(ImageSource kaynak) async {',
    'Future<void> videoGonder(ImageSource kaynak)async{',
    """      unawaited(uygulamaBildirimiGonder(toUid:widget.digerUid,fromUid:ben,tur:'message',metin:'Yeni bir fotoğraf mesajın var',belgeId:widget.chatId).catchError((_){ }));""",
    """      unawaited(uygulamaBildirimiGonder(
        toUid:widget.digerUid,fromUid:ben,tur:'message',metin:'Yeni bir fotoğraf mesajın var',
        belgeId:widget.chatId,
        dedupeKey:'private_photo___D__{widget.chatId}___D__{mesajRef.id}___D__{widget.digerUid}',
      ).catchError((_){ }));""".replace('__D__','$'),
    'private photo notification dedupe',
)

main=scoped_replace_after(
    main,
    'class _SohbetPageState',
    'Future<bool> ekMesajGonder(',
    'Future<void> dosyaGonder()async',
    '      await batch.commit().timeout(const Duration(seconds:15));',
    """      await ngelxBatchCommitDogrula(
        batch:batch,
        marker:mesajRef,
        timeout:const Duration(seconds:15),
      );""",
    'private extra commit verification',
)
main=scoped_replace_after(
    main,
    'class _SohbetPageState',
    'Future<bool> ekMesajGonder(',
    'Future<void> dosyaGonder()async',
    """      unawaited(uygulamaBildirimiGonder(toUid:widget.digerUid,fromUid:ben,tur:'message',metin:bildirim,belgeId:widget.chatId).catchError((_){ }));""",
    """      unawaited(uygulamaBildirimiGonder(
        toUid:widget.digerUid,fromUid:ben,tur:'message',metin:bildirim,
        belgeId:widget.chatId,
        dedupeKey:'private_extra___D__{widget.chatId}___D__{mesajRef.id}___D__{widget.digerUid}',
      ).catchError((_){ }));""".replace('__D__','$'),
    'private extra notification dedupe',
)

main=scoped_replace_after(
    main,
    'class _SohbetPageState',
    'Future<void> aramaBaslat(bool goruntulu)async{',
    'void bilgi()=>',
    '      await batch.commit().timeout(const Duration(seconds:10));',
    """      await ngelxBatchCommitDogrula(
        batch:batch,
        marker:mesajRef,
        timeout:const Duration(seconds:10),
      );""",
    'private call commit verification',
)

main=one(main,"defaultValue: '1.0.82'","defaultValue: '1.0.83'",'runtime version')
main=one(main,"defaultValue: '301'","defaultValue: '302'",'runtime build')
MAIN_PATH.write_text(main,encoding='utf-8')

pub=one(pub,'version: 1.0.82+301','version: 1.0.83+302','pubspec version')
PUB_PATH.write_text(pub,encoding='utf-8')

for path in (ROOT/'tools').glob('verify_v*.py'):
    if path.name=='verify_v84_firestore_consistency.py':
        continue
    t=path.read_text(encoding='utf-8')
    t=t.replace('version: 1.0.82+301','version: 1.0.83+302')
    t=t.replace("defaultValue: '1.0.82'","defaultValue: '1.0.83'")
    t=t.replace("defaultValue: '301'","defaultValue: '302'")
    t=t.replace('Build 301','Build 302')
    path.write_text(t,encoding='utf-8')

print('Build 302 Firestore consistency patch prepared.')
# retry Build 302 anchored private chat
