"""Recover an index-unavailable community feed without unbounded Firestore reads.

This modifies generated app/lib/community450.dart ONLY after build456.patch is applied.
The default indexed 20-post query and existing app architecture stay unchanged.
"""
from pathlib import Path

FEED_OLD = """  Stream<QuerySnapshot<Map<String, dynamic>>> feedStream() => _communities450
      .doc(widget.id)
      .collection('posts')
      .where('status', isEqualTo: 'approved')
      .orderBy('createdAt', descending: true)
      .limit(postLimit)
      .snapshots();"""

FEED_NEW = """  Stream<QuerySnapshot<Map<String, dynamic>>> feedStream() async* {
    final approved = _communities450
        .doc(widget.id)
        .collection('posts')
        .where('status', isEqualTo: 'approved');
    try {
      await for (final snapshot in approved
          .orderBy('createdAt', descending: true)
          .limit(postLimit)
          .snapshots()) {
        yield snapshot;
      }
    } on FirebaseException catch (error) {
      if (error.code != 'failed-precondition') rethrow;
      // An index can be missing in an existing project. Fall back to a
      // bounded approved-only sample, never an unbounded collection listener.
      await for (final snapshot in approved
          .limit((postLimit * 3).clamp(20, 120).toInt())
          .snapshots()) {
        yield snapshot;
      }
    }
  }"""

SORT_OLD = """            }).toList();
            return CustomScrollView("""

SORT_NEW = """            }).toList()
              ..sort((a, b) {
                final aTime = (a.data()['createdAt'] as Timestamp?)
                        ?.millisecondsSinceEpoch ??
                    0;
                final bTime = (b.data()['createdAt'] as Timestamp?)
                        ?.millisecondsSinceEpoch ??
                    0;
                return bTime.compareTo(aTime);
              });
            return CustomScrollView("""

def transform(source: str) -> str:
    if FEED_NEW in source and SORT_NEW in source:
        return source
    if source.count(FEED_OLD) != 1 or source.count(SORT_OLD) != 1:
        raise RuntimeError('Unexpected Build456 community feed source; refusing partial edit')
    return source.replace(FEED_OLD, FEED_NEW, 1).replace(SORT_OLD, SORT_NEW, 1)

def main() -> None:
    path = Path('app/lib/community450.dart')
    before = path.read_text()
    after = transform(before)
    if after != before:
        path.write_text(after)
    print('Build456: indexed chronological feed with bounded missing-index fallback')

if __name__ == '__main__':
    main()
