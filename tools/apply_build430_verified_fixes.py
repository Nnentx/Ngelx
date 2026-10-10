#!/usr/bin/env python3
"""Apply reviewed fixes after the Build429 generation chain."""
from pathlib import Path

def one(s,old,new,label):
    if s.count(old)!=1: raise SystemExit(f'Build430 source drift: {label}: {s.count(old)}')
    return s.replace(old,new,1)

p=Path('app/lib/main.dart')
s=p.read_text()
# Preserve independent Activity screen; both current profile layouts use this route.
old="_profilKapakIkon(Icons.notifications_none_rounded,()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const MesajPage(initialFilter:'Bildirimler'))))"
if s.count(old)!=2: raise SystemExit('Build430 profile bell anchors drift')
s=s.replace(old,'const NgelXProfilBildirimZili()')
s=one(s,"bool ngelxPresenceOnline(Map<String,dynamic> v){","bool ngelxPresenceOnline(Map<String,dynamic> v){\n  if(v['showActivityStatus']==false)return false;",'presence privacy')
s=one(s,"return '${fark.inMinutes} dk önce aktifti';","return '${fark.inMinutes}d';",'minutes')
s=one(s,"return '${fark.inHours} saat önce aktifti';","return '${fark.inHours}s';",'hours')
s=one(s,"return '${fark.inDays} gün önce aktifti';","return '${fark.inDays}g';",'days')
# Cache search stream instead of restarting a query on every keystroke.
s=one(s,"class _ProfilAramaPageState extends State<ProfilAramaPage>{","class _ProfilAramaPageState extends State<ProfilAramaPage>{\n  late final _paylasimAkisi=FirebaseFirestore.instance.collection('videos').where('ownerId',isEqualTo:widget.uid).limit(100).snapshots();",'profile search stream')
a=s.index('class _ProfilAramaPageState');b=s.index('class HikayeArsiviPage',a)
part=s[a:b]
part=one(part,"stream:FirebaseFirestore.instance.collection('videos').where('ownerId',isEqualTo:widget.uid).limit(100).snapshots(),","stream:_paylasimAkisi,",'reuse search stream')
part=one(part,"d.data()['type']!='story'","d.data()['type']!='story'&&d.data()['deleted']!=true&&d.data()['isDeleted']!=true",'hide deleted search posts')
s=s[:a]+part+s[b:]
# A video story URL must never be sent to an image decoder.
old="ClipRRect(borderRadius:BorderRadius.circular(12),child:NgelXAgResmi(imageUrl:(v['storyUrl']??'').toString(),width:62,height:82,fit:BoxFit.cover,errorWidget:(_,__,___)=>const SizedBox(width:62,height:82,child:Icon(Icons.auto_stories))))"
new="ClipRRect(borderRadius:BorderRadius.circular(12),child:SizedBox(width:62,height:82,child:(v['storyMediaType']=='video')?NgelXVideoKapakOnizleme(url:(v['storyUrl']??'').toString()):NgelXAgResmi(imageUrl:(v['storyUrl']??'').toString(),width:62,height:82,fit:BoxFit.cover,errorWidget:(_,__,___)=>const Icon(Icons.auto_stories))))"
s=one(s,old,new,'story reply video preview')
# Same notification snapshot for list, tab counts and summary.
a=s.index('class _MesajPageState');b=s.index('class MesajIstekleriPage',a)
part=s[a:b]
part=one(part,"'notification|'+ben+'|'+limit.toString()","'notification|'+ben",'notification stream identity')
part=one(part,".where('toUid',isEqualTo:ben).limit(limit).snapshots());",".where('toUid',isEqualTo:ben).limit(200).snapshots());",'notification stream window')
part=one(part,"}else if(v['read']!=true){","}else if(v['read']!=true&&ngelxAktiviteBildirimiGosterilir(v)){",'notification eligibility')
part=one(part,'            var bildirimler=0,istekler=0,mesajlar=0,gruplar=0;','            var bildirimler=0,istekler=0,mesajlar=0,gruplar=0;\n            var mesajIstekleri=0;','request count')
part=one(part,"              if(n<=0)continue;\n              final members=", "              final membersList=List<String>.from(v['members']??const[]);\n              final other=membersList.firstWhere((id)=>id!=ben,orElse:()=>ben!);\n              final pending=membersList.length==2&&!arkadaslar.contains(other)&&(v['lastMessage']??'').toString().trim().isNotEmpty&&v['isGroup']!=true&&(v['requestRecipientUid']??'').toString()==ben&&v['requestAccepted_$ben']!=true&&v['requestRejected_$ben']!=true&&!List<String>.from(v['hiddenFor']??const[]).contains(ben);\n              if(pending){mesajIstekleri++;continue;}\n              if(n<=0)continue;\n              final members=",'pending messages separated')
part=one(part,"            return Row(children:[\n              Expanded(child:sekme('Tümü',bildirimler+istekler+mesajlar+gruplar)),","            istekler+=mesajIstekleri;\n            return Row(children:[\n              Expanded(child:sekme('Tümü',bildirimler+istekler+mesajlar+gruplar)),",'total requests')
part=one(part,'              return ListTile(\n                contentPadding:const EdgeInsets.symmetric(horizontal:8,vertical:5),','              return NgelXGorulenBildirim(bildirim:d,child:ListTile(\n                contentPadding:const EdgeInsets.symmetric(horizontal:8,vertical:5),','mark viewed inbox items')
part=one(part,'              );\n              });\n            },\n          );\n        },\n      );\n    }\n\n    Widget isteklerIcerigi()', '              ));\n              });\n            },\n          );\n        },\n      );\n    }\n\n    Widget isteklerIcerigi()', 'close viewed inbox wrapper')
needle='          if(snap.connectionState==ConnectionState.waiting&&docs.isEmpty)return const Center(child:CircularProgressIndicator(color:mor));'
part=one(part,needle,needle+"\n          if(snap.hasError&&docs.isEmpty)return Center(child:TextButton(onPressed:_gelenKutusunuYenile,child:const Text('Bildirimler yüklenemedi • Tekrar dene')));",'notification error state')
s=s[:a]+part+s[b:]
# Purple sender names on dedicated notification screen.
a=s.index('class _AktivitePageState');b=s.index('bool ngelxPresenceOnline',a)
part=s[a:b].replace('const kalin=TextStyle(fontWeight:FontWeight.w900);','const kalin=TextStyle(color:mor,fontWeight:FontWeight.w900);')
part=one(part,'            return Container(decoration:BoxDecoration(color:okundu?Colors.white:', '            return NgelXGorulenBildirim(bildirim:d,child:Container(decoration:BoxDecoration(color:okundu?Colors.white:', 'mark viewed activity items')
part=one(part,'             ));\n              },','             )));\n              },','close viewed activity wrapper')
s=s[:a]+part+s[b:]
# Serialize same sender/recipient/type across devices before creating a notification.
a=s.index('Future<bool> sosyalIstekGonder(');b=s.index('Future<void> sosyalIstekIptalEt',a)
part=s[a:b]
start=part.index('    final batch=firestore.batch();')
end=part.index('    return true;',start)+len('    return true;')
block=part[start:end]
block=block.replace('    final batch=firestore.batch();',"    return await firestore.runTransaction<bool>((tx)async{\n      final latest=await tx.get(istekRef);\n      if(latest.data()?['status']=='pending')return false;")
block=block.replace('batch.set(', 'tx.set(')
block=block.replace('    await batch.commit().timeout(const Duration(seconds:12));\n    return true;', '      return true;\n    }).timeout(const Duration(seconds:12));')
part=part[:start]+block+part[end:]
s=s[:a]+part+s[b:]
# Do not drop failed media cleanup after removing its only database reference.
a=s.index('Future<void> ngelxMedyaSil(');b=s.index('String ngelxMedyaHataMetni',a)
s=s[:a]+Path('tools/build430_media_delete.dart').read_text()+'\n'+s[b:]
a=s.index('Future<void> ngelxPaylasimVeAltKayitlariniSil(');b=s.index('Future<void> kendiPaylasiminiSil(',a)
part=s[a:b]
part=one(part,'  final silinecek=',"  final uid=FirebaseAuth.instance.currentUser?.uid;\n  final actual=await ref.get(const GetOptions(source:Source.server));\n  final data=actual.data();\n  if(data==null)return;\n  if(uid==null||data['ownerId']!=uid)throw StateError('Yalnızca kendi paylaşımını silebilirsin.');\n  final urls=<String>{};\n  for(final key in ['mediaUrl','videoUrl','audioUrl','thumbnailUrl','posterUrl','coverUrl']){\n    final url=(data[key]??'').toString().trim();\n    if(url.isNotEmpty)urls.add(url);\n  }\n  for(final url in urls){await ngelxMedyaSil(url);}\n  final silinecek=",'owner and awaited media cleanup')
part=one(part,'  }\n}\n','  }\n  ngelxIcerikSilindi(ref.id);\n}\n','deleted post invalidation')
s=s[:a]+part+s[b:]
s=one(s,"defaultValue: '429'","defaultValue: '430'",'version code')
s=one(s,"defaultValue: '1.0.204'","defaultValue: '1.0.205'",'version name')
s+='\n'+Path('tools/build430_notification_widgets.dart').read_text()
p.write_text(s)
p=Path('app/pubspec.yaml');p.write_text(one(p.read_text(),'version: 1.0.204+429','version: 1.0.205+430','pubspec version'))
print('Build430 notification routing, viewed read state, counters, presence privacy, search and video preview applied')
