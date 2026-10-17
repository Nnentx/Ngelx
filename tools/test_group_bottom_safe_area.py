#!/usr/bin/env python3
"""Source regression checks for issue #104: Android bottom navigation safe areas.

Intentionally validates only two existing UI screens without changing their
membership, moderation, media preview or Firestore behavior.
"""
from pathlib import Path


def section(src: str, start: str, end: str) -> str:
    assert src.count(start) == 1, (start, src.count(start))
    assert src.count(end) == 1, (end, src.count(end))
    start_at = src.index(start)
    end_at = src.index(end, start_at)
    return src[start_at:end_at]


def main() -> None:
    src = Path("app/lib/main.dart").read_text(encoding="utf-8")
    info = section(src, "class _GrupBilgiPageState", "class GrupTakmaAdlarPage")
    members = section(src, "class _GrupUyeleriPageState", "class GrupDavetPage")

    for title, view in (("group info", info), ("group members", members)):
        assert "body:SafeArea(top:false,child:StreamBuilder<" in view, title
        assert "        },\n      )),\n    ),\n  );" in view, title
        assert "stream:ref.snapshots()" in view, title

    # Scaffold owns the app bar. Keep its design, but exclude bottom navigation
    # from the scroll viewport instead of relying only on an added scroll margin.
    assert "padding:const EdgeInsets.fromLTRB(14,16,14,32)" in info
    assert "32+MediaQuery.paddingOf(context).bottom" not in info
    assert "child:GridView.builder(" in info
    assert "GrupMedyaPage(chatId:widget.chatId)" in info

    # Preserve search, member roles, menu actions and scroll padding.
    for marker in ("hintText:'Üye ara'", "padding:const EdgeInsets.fromLTRB(14,4,14,28)",
                   "KURUCU • Yönetici", "_uyeIslemi(", "class _GrupUyeleriPageState"):
        assert marker in members, marker

    print("Issue #104: scoped group info/member SafeArea guards passed.")


if __name__ == "__main__":
    main()
