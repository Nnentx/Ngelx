#!/usr/bin/env python3
"""Build510 source QA: scrolling, unread counter and moderation are intact."""
import importlib.util
from pathlib import Path

spec=importlib.util.spec_from_file_location("build510","tools/apply_build510_live_comment_scroll.py")
assert spec and spec.loader
patch=importlib.util.module_from_spec(spec)
spec.loader.exec_module(patch)
src=Path("app/lib/live_broadcast_studio.dart").read_text(encoding="utf-8")
assert patch.transform(src)==src, "Build510 must be idempotent"
start=src.index("class _CanliYayinPageState")
end=src.index("class _CanliOzetSatiri",start)
live=src[start:end]
import re
start_panel=live.index("  Widget _yorumPaneli(){")
remaining=live[start_panel+len("  Widget _yorumPaneli(){"):]
boundary=re.search(r"(?m)^  (?:Widget|Future|void|bool|int)\s+[_a-zA-Z]",remaining)
assert boundary is not None,"Comment panel method boundary lost"
stop_panel=start_panel+len("  Widget _yorumPaneli(){")+boundary.start()
comments=live[start_panel:stop_panel]
for token in (
    patch.MARK,
    "final ScrollController _commentScroll510=ScrollController();",
    "_commentScroll510.addListener(_onCommentScroll510)",
    "_commentScroll510.removeListener(_onCommentScroll510)",
    "_commentScroll510.dispose();",
    "if(_commentScroll510.offset>56)",
    "_newestComment510=newest",
    "_newComments510.value=(_newComments510.value+arrived).clamp(0,999).toInt();",
    "_commentScroll510.animateTo(0,",
    "Yeni yorumlar ($count) · En alta dön",
    "Semantics(",
    "_readingOld510.dispose();",
    "_newComments510.dispose();",
    "Offstage(offstage:_commentsHidden490,child:_yorumPaneli())",
):
    assert token in live, f"Build510 missing contract: {token}"
for token in (
    ".orderBy('createdAt',descending:true).limit(100).snapshots()",
    "controller:_commentScroll510,",
    "_observeComments510(yorumlar);",
    "if(kind=='gift')",
    "if(kind=='join')",
    "_yorumYonet(d.id,y)",
    "'pinnedComment'",
):
    assert token in comments, f"Build510 missing history/render/moderation contract: {token}"
assert ".limit(30)" not in comments, "Old limit still restricts scrolling"
assert ".limit(100).snapshots()" in comments, "Bounded 100-event feed expected"
assert "controller:_commentScroll510," in comments
assert "_observeComments510(yorumlar);" in comments
assert live.count("if(!_commentsHidden490)_newCommentChip510(),")==1
assert "_bitir(" not in patch.EXTRA and "setCameraEnabled" not in patch.EXTRA
assert "FirebaseFirestore" not in patch.EXTRA and ".add(" not in patch.EXTRA
print("Build510 PASS: scroll older comments, show unread chip, return latest")
print("Build510 PASS: pinned/moderation/gift rendering preserved; no server write or call changes")
print("Build510 LIMIT: last 100 live events only; older-page pagination and two-Android QA are pending")
