"""Apply narrowly scoped Build457 community runtime fixes AFTER Build456.

Build456 is a large generated patch. Changing its inputs invalidates patch
hunks and can silently discard later changes. Run these transformations on
fully generated Dart source and refuse unknown source layouts.
No Firebase or customer data changes are performed.
"""
from pathlib import Path

COMMUNITY=Path('app/lib/community450.dart')
COUNTS=Path('app/lib/build455_widgets.dart')

OLD_FOUNDER="""bool _communityAdmin450(Map<String, dynamic> v) =>
    List<String>.from(v['admins'] ?? []).contains(_communityUid450);"""
NEW_FOUNDER="""bool _communityAdmin450(Map<String, dynamic> v) =>
    _communityUid450.isNotEmpty &&
    (v['founderId'] == _communityUid450 ||
        List<String>.from(v['admins'] ?? []).contains(_communityUid450));"""

LOAD_START="  Future<Map<String, int>> load() async {"
LOAD_END="  @override\n  void didUpdateWidget(covariant Ngelx455PostCounts old) {"
LIVE_FIRST="widget.liveCounts[item.$1] ?? s.data?[item.$1]"
SERVER_FIRST="s.data?[item.$1] ?? widget.liveCounts[item.$1]"

# Reaction and comment counters must never use permanently stale counts456.
# Keep the server-side aggregate reads bounded to two collections per card.
# Views/shares can use provided summary counters to limit Firestore reads.
NEW_LOAD="""  Future<Map<String, int>> load() async {
    const keys = ['likes', 'comments', 'shares', 'views'];
    final values = await Future.wait(keys.map((key) async {
      final cached = widget.liveCounts[key];
      if ((key == 'shares' || key == 'views') && cached is num) {
        return cached.toInt();
      }
      final result = await widget.ref.collection(key).count().get();
      return result.count ?? 0;
    }));
    return {
      for (var i = 0; i < keys.length; i++) keys[i]: values[i],
    };
  }

"""

def community_fix(src:str)->str:
    if NEW_FOUNDER in src:
        return src
    if src.count(OLD_FOUNDER)!=1:
        raise ValueError('Build457 founder permission widget anchor changed')
    return src.replace(OLD_FOUNDER,NEW_FOUNDER,1)

def counts_fix(src:str)->str:
    if NEW_LOAD in src and SERVER_FIRST in src and LIVE_FIRST not in src:
        return src
    if src.count(LOAD_START)!=1 or src.count(LOAD_END)!=1:
        raise ValueError('Build456 comment-count widget structure changed')
    left=src.index(LOAD_START)
    right=src.index(LOAD_END,left)
    old=src[left:right]
    if "widget.liveCounts.containsKey" not in old or "collection(k).count().get()" not in old:
        raise ValueError('Build456 count logic differs: refuse an unsafe replacement')
    if src.count(LIVE_FIRST)!=1:
        raise ValueError('Unexpected comment count display precedence')
    result=src[:left]+NEW_LOAD+src[right:]
    return result.replace(LIVE_FIRST,SERVER_FIRST,1)

def main()->None:
    cs=COMMUNITY.read_text(encoding='utf-8')
    cc=COUNTS.read_text(encoding='utf-8')
    fixed_community=community_fix(cs)
    fixed_counts=counts_fix(cc)
    if cs!=fixed_community:
        COMMUNITY.write_text(fixed_community,encoding='utf-8')
    if cc!=fixed_counts:
        COUNTS.write_text(fixed_counts,encoding='utf-8')
    print('Build457: legacy founders recognized; post comments/reactions use live aggregate counts.')

if __name__=='__main__':
    main()
