#!/usr/bin/env python3
"""Build429 regression contract for Build428-preserved story flows."""
from pathlib import Path

main=Path('app/lib/main.dart').read_text(encoding='utf-8')
story=Path('app/lib/story_v66.dart').read_text(encoding='utf-8')
checks={
  'Build428 story reply still reaches private chat': "'type':'story_reply'" in story and "'storyOwnerId':hedef" in story,
  'Story reply preview card still opens story': '_hikayeYanitKartiAc(v)' in main,
  'Story series timeout remains bounded': 'initialize().timeout(const Duration(seconds:12))' in story,
  'Story archive excludes active unsaved stories': "v['archivedAt'] is Timestamp||suresiDolmus||v['highlighted']==true" in main,
  'Archive remains owner scoped': "where('ownerId',isEqualTo:uid)" in main and "where('type',isEqualTo:'story')" in main,
  'Permanent story deletion validates signed-in owner': "veri['ownerId']" in story and 'Yalnızca kendi hikâyeni silebilirsin.' in story,
  'Firebase Storage media deletion checks owner path': 'dosya.fullPath.split(\'/\').contains(uid)' in story and 'await dosya.delete()' in story,
  'Story deletion cleans comments, reactions and nested likes': 'ref.collection(\'comments\')' in story and 'comment.reference.collection(\'likes\')' in story and 'ref.collection(\'likes\')' in story,
  'Firestore story record deleted only after media cleanup': story.index('await dosya.delete()') < story.index('await ref.delete()'),
  'Firebase Storage dependency and import': "import 'package:firebase_storage/firebase_storage.dart';" in main and 'firebase_storage: ^13.6.0' in Path('app/pubspec.yaml').read_text(encoding='utf-8'),
  'Build429 version': "defaultValue: '429'" in main and "defaultValue: '1.0.204'" in main and 'version: 1.0.204+429' in Path('app/pubspec.yaml').read_text(encoding='utf-8'),
}
failed=[name for name,ok in checks.items() if not ok]
for name,ok in checks.items(): print(('PASS' if ok else 'FAIL')+' '+name)
if failed: raise SystemExit('Build429 regression failures: '+', '.join(failed))
