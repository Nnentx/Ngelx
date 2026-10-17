#!/usr/bin/env python3
"""Build473: explain real community Firestore permission failures without
replacing the earlier community handler or changing any security policy.
The existing handler owns offline/network/validation UI and stays intact.
"""
from pathlib import Path

TARGET=Path('app/lib/community450.dart')
HEADER='void _communityError450(BuildContext c, Object e) {'
MARKER='// Build473: explicit Firestore permission denial, preserve existing error UI'

def patch_community(src: str) -> str:
    if MARKER in src:
        return src
    if src.count(HEADER) != 1 or 'Widget _communityImage450' not in src:
        raise RuntimeError('Build473 community handler not found uniquely')
    section=src[src.index(HEADER):src.index('Widget _communityImage450',src.index(HEADER))]
    if '}' not in section:
        raise RuntimeError('Build473 community handler was malformed')
    # This must run even when Build457 or other generated patches no longer use
    # _ngelxKisaHata: Build472's overly restrictive guard skipped that case.
    guard="""\n  // Build473: explicit Firestore permission denial, preserve existing error UI
  if (e is FirebaseException && e.code == 'permission-denied') {
    if (!c.mounted) return;
    ScaffoldMessenger.of(c).hideCurrentSnackBar();
    ScaffoldMessenger.of(c).showSnackBar(const SnackBar(
      content: Text('Topluluk sunucusu bu işleme izin vermedi. Kurucu/yönetici yetkisi ve canlı Firebase güvenlik kuralları kontrol edilmeli.'),
      duration: Duration(seconds: 6),
    ));
    return;
  }"""
    return src.replace(HEADER, HEADER+guard, 1)

if __name__=='__main__':
    original=TARGET.read_text(encoding='utf-8')
    updated=patch_community(original)
    if updated!=original:
        TARGET.write_text(updated,encoding='utf-8')
    print('Build473: safe permission-denied handler attached; prior community UX preserved')
