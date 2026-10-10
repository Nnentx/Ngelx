from pathlib import Path
s=Path('app/lib/main.dart').read_text()
story=Path('app/lib/story_v66.dart').read_text()
checks={
 'Both final profile bells use the notification-only badge widget':s.count('const NgelXProfilBildirimZili()')==2,
 'Profile bell opens independent Activity page':"builder:(_)=>const AktivitePage()" in s,
 'No final profile bell opens inbox':"_profilKapakIkon(Icons.notifications_none_rounded,()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>const MesajPage" not in s,
 'Presence honors privacy before timestamps':"if(v['showActivityStatus']==false)return false;" in s,
 'Search stream is retained during typing':'stream:_paylasimAkisi,' in s,
 'Story reply uses video decoder for video story':"(v['storyMediaType']=='video')?NgelXVideoKapakOnizleme" in s,
 'Seen rows mark backend read without creating deleted notifications':"widget.bildirim.reference.update({'read':true})" in s,
 'Offscreen and inactive route rows stay unread':'top>=height||top+box.size.height<=0' in s and 'ModalRoute.of(context)?.isCurrent!=true' in s,
 'Both notification lists use seen-row wrapper':s.count('NgelXGorulenBildirim(bildirim:d,child:')==2,
 'Concurrent request creation rereads request inside transaction':"final latest=await tx.get(istekRef);" in s and "latest.data()?['status']=='pending'" in s,
 'Permanent post deletion waits for media cleanup':'for(final url in urls){await ngelxMedyaSil(url);}' in s,
 'Delete rejects unauthorized paths and buckets':"ref.bucket!=storage.ref().bucket" in s and 'parts[1]!=uid' in s,
 'Story replies still send to DM':"'type':'story_reply'" in story,
 'Story retries still available':"label:const Text('Tekrar dene')" in story,
 'Existing chat message renderer preserved':'class SohbetPage' in s and 'class MesajPage' in s,
 'Release version':'version: 1.0.205+430' in Path('app/pubspec.yaml').read_text(),
}
for label,passed in checks.items():print(('PASS ' if passed else 'FAIL ')+label)
if not all(checks.values()):raise SystemExit('Build430 source validation failed')
