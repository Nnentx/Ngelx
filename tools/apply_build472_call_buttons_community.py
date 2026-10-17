#!/usr/bin/env python3
"""Build472: native incoming buttons above nav bar and accurate moderator
backend permission denials. No cloud deployment or security bypass.
"""
from pathlib import Path
ACTIVITY=Path('app/android/app/src/main/kotlin/com/nnentx/ngelx_app/IncomingCallActivity470.kt')
COMMUNITY=Path('app/lib/community450.dart')
TAG='// Build472: show a permission-denied backend response truthfully'
def once(s,a,b,why):
    n=s.count(a)
    if n!=1:raise RuntimeError(f'Build472 {why}: expected one anchor, got {n}')
    return s.replace(a,b,1)
def patch_activity(s):
    if 'dp(42))) // Build472: move call actions safely above the system navigation bar' in s:return s
    return once(s,
      'content.addView(View(this), LinearLayout.LayoutParams(1, dp(14)))',
      'content.addView(View(this), LinearLayout.LayoutParams(1, dp(42))) // Build472: move call actions safely above the system navigation bar',
      'call answer/reject vertical alignment')
def patch_community(s):
    if TAG in s:return s
    start=s.index('void _communityError450(BuildContext c, Object e) {')
    stop=s.index('\nWidget _communityImage450',start)
    original=s[start:stop]
    if 'ScaffoldMessenger' not in original or '_ngelxKisaHata' not in original:
        # Prior generated community patches own this handler; do not overwrite
        # their authorization UX on an unrecognized source version.
        print('Build472: existing generated community error handler retained')
        return s
    new="""// Build472: show a permission-denied backend response truthfully.
// Device shows local founder powers, but deployed Firestore rules may lag.
void _communityError450(BuildContext c, Object e) {
  if (!c.mounted) return;
  final permissionDenied=e is FirebaseException && e.code=='permission-denied';
  final message=permissionDenied
      ? 'Topluluk sunucusu bu değişikliğe izin vermedi. Kurucu/yönetici yetkisi ve Firebase kuralları kontrol edilmeli.'
      : 'İşlem tamamlanamadı. ${_ngelxKisaHata(e)}';
  debugPrint('NgelX community operation failed: ${e.runtimeType}'
      + (e is FirebaseException ? ' / ${e.code}' : ''));
  ScaffoldMessenger.of(c).showSnackBar(SnackBar(content:Text(message)));
}"""
    return s[:start]+new+'\n'+s[stop:]
if __name__=='__main__':
    for path,fn in ((ACTIVITY,patch_activity),(COMMUNITY,patch_community)):
      before=path.read_text(encoding='utf-8')
      after=fn(before)
      if before!=after:path.write_text(after,encoding='utf-8')
      print('Build472 scoped:',path)
