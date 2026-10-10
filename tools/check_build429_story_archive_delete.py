#!/usr/bin/env python3
"""Build429 regression contract for Build428-preserved story flows."""
from pathlib import Path

main=Path('app/lib/main.dart').read_text(encoding='utf-8')
story=Path('app/lib/story_v66.dart').read_text(encoding='utf-8')
owner=main[main.index('class _ProfilPageState extends State<ProfilPage>'):main.index('class _ProfilEtkilesimRozeti')]
checks={
  'Profile bell opens dedicated Activity page': "const AktivitePage()" in owner and "const MesajPage(initialFilter:'Bildirimler')" not in owner,
  'Profile bell badge uses deduplicated Firebase unread count': 'ngelxOkunmamisAktiviteSayisi(' in owner and 'Badge(label:Text(sayi>99?' in owner,
  'Build428 story reply still reaches private chat': "'type':'story_reply'" in story and "'storyOwnerId':hedef" in story,
  'Story reply preview card still opens story': '_hikayeYanitKartiAc(v)' in main,
  'Story series timeout remains bounded': 'initialize().timeout(const Duration(seconds:12))' in story,
  'Story archive keeps only explicitly archived/highlighted, non-deleted owner stories': "v['archivedAt'] is Timestamp||v['highlighted']==true" in main and "v['deleted']!=true&&v['isDeleted']!=true" in main and '!hidden.contains(uid)' in main,
  'Story archive shows loading and recoverable error states': 'if(s.connectionState==ConnectionState.waiting)' in main and 'Hikâye arşivi yüklenemedi.' in main and 'Tekrar dene' in main,
  'Archive remains owner scoped': "where('ownerId',isEqualTo:uid)" in main and "where('type',isEqualTo:'story')" in main,
  'Permanent story deletion validates signed-in owner': "veri['ownerId']" in story and 'Yalnızca kendi hikâyeni silebilirsin.' in story,
  'Firebase Storage media deletion checks owner path': "dosya.fullPath.startsWith('stories/'+uid+'/')" in story and 'await dosya.delete()' in story,
  'Story cleanup uses authenticated R2 key and rejects cross-user paths': "api+'/object'" in story and "'Bearer '+token" in story and "keyPath.startsWith('stories/'+uid+'/')" in story and "raw.startsWith('stories/'+uid+'/')" in story,
  'Story deletion cleans comments, reactions and nested likes': 'ref.collection(\'comments\')' in story and 'comment.reference.collection(\'likes\')' in story and 'ref.collection(\'likes\')' in story,
  'Firestore story record deleted only after media cleanup': story.index('await dosya.delete()') < story.index('await ref.delete()'),
  'Firebase Storage dependency and import': "import 'package:firebase_storage/firebase_storage.dart';" in main and 'firebase_storage: ^13.6.0' in Path('app/pubspec.yaml').read_text(encoding='utf-8'),
  'Build429 version': "defaultValue: '429'" in main and "defaultValue: '1.0.204'" in main and 'version: 1.0.204+429' in Path('app/pubspec.yaml').read_text(encoding='utf-8'),
}
failed=[name for name,ok in checks.items() if not ok]
for name,ok in checks.items(): print(('PASS' if ok else 'FAIL')+' '+name)
if failed: raise SystemExit('Build429 regression failures: '+', '.join(failed))
