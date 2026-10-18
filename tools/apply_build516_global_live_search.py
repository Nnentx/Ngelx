#!/usr/bin/env python3
"""Build516 QA: reach bounded live search from Keşfet, even with no live cards.

Apply AFTER Build515. The original content-discovery search and category
filter remain unchanged; normal live-card taps use authenticated join helper.
No new backend writes, Firebase indexes, overlay permissions or production
changes.
"""
from pathlib import Path

FILE=Path('app/lib/main.dart')
MARK='// Build516: always-available Keşfet live search'

def once(src,old,new,where):
    count=src.count(old)
    if count!=1:
        raise RuntimeError(f'Build516 {where}: expected one anchor, found {count}')
    return src.replace(old,new,1)

def transform(src):
    if MARK in src:return src
    original=src
    if 'part \'live_feed_card.dart\';' not in src:
        raise RuntimeError('Build516 requires existing searchable Keşfet live_feed_card part')
    if "void _aramaAc(){" not in src or "List<Widget> _canliSliverleri(" not in src:
        raise RuntimeError('Build516 existing Keşfet controls missing')
    # Earlier generated Keşfet layouts vary in whitespace, title widgets
    # and top-row controls. Scope to Keşfet instead of matching a long
    # legacy text fragment that can be rewritten by prior build patches.
    import re
    a=src.index('  void _aramaAc(){')
    b=src.index('  List<Widget> _canliSliverleri(',a)
    keşfet=src[a:b]
    title=re.search(r"(?m)^[ \t]*Text\(t\('explore'\)[^\n]*\),[ \t]*$",keşfet)
    headAction="""              // Build516: always-available Keşfet live search.
              IconButton(
                tooltip:'Canlı yayın ara',
                onPressed:()=>ngelxCanliAramaAc(context),
                icon:const Icon(Icons.live_tv_rounded,color:Color(0xFFFF1744),size:24)),
"""
    if title is not None:
        after=keşfet[title.end():]
        spacer=re.search(r"(?m)^[ \t]*const Spacer\(\),[ \t]*$",after)
        if spacer is not None and spacer.start()<500:
            at=title.end()+spacer.end()
            keşfet=keşfet[:at]+"\n"+headAction.rstrip('\n')+keşfet[at:]
        else:
            title=None
    if title is None:
        # Safe fallback: a standalone sliver in the Keşfet header area. It
        # stays reachable even when the live list has zero cards.
        old="          if(kategori==0)..._canliSliverleri(),"
        extra="""          // Build516: always-available Keşfet live search.
          SliverToBoxAdapter(child:Align(alignment:Alignment.centerRight,
            child:IconButton(
              tooltip:'Canlı yayın ara',
              onPressed:()=>ngelxCanliAramaAc(context),
              icon:const Icon(Icons.live_tv_rounded,color:Color(0xFFFF1744),size:24)))),
"""
        keşfet=once(keşfet,old,extra+old,'fallback Keşfet search action')
    src=src[:a]+keşfet+src[b:]
    # Insert the section action at the beginning of the live sliver list.
    # This avoids assuming its title or row layout survived earlier patches.
    liveHeader='  List<Widget> _canliSliverleri({bool trend=false})=>['
    src=once(src,liveHeader,liveHeader+"""
    SliverToBoxAdapter(child:Align(alignment:Alignment.centerRight,
      child:TextButton.icon(
        onPressed:()=>ngelxCanliAramaAc(context),
        icon:const Icon(Icons.search_rounded,size:17),
        label:const Text('Canlı ara'),
        style:TextButton.styleFrom(foregroundColor:const Color(0xFFFF1744)),
      ))),
""",'live section search before results')
    # Legacy Keşfet versions may already have removed _yayinIzle, or
    # reformatted its signature. Never create an untrusted token path.
    # If present and unsafe, replace only this method with the shared
    # authorized join. If absent, upgrade the visible card's onTap only.
    import re
    match=re.search(r"(?m)^  Future<void>\s+_yayinIzle\s*\([^\n]*\)\s*async\s*\{",src)
    if match:
        after=src[match.end():]
        next_method=re.search(
            r"(?m)^  (?:Future<[^>\n]+>|void|Widget|List<Widget>|bool)\s+[_a-zA-Z]\w*\s*\(",
            after)
        if next_method is None:
            raise RuntimeError('Build516 legacy join method boundary missing')
        start=match.start()
        stop=match.end()+next_method.start()
        old_method=src[start:stop]
        if 'lk.DevelopmentTokenSource(' in old_method:
            src=src[:start]+"""  Future<void> _yayinIzle(BuildContext context, Map<String, dynamic> veri, String belgeId) async {
    await ngelxCanliYayinaKatil(context,belgeId);
  }

"""+src[stop:]
        elif 'ngelxCanliYayinaKatil(context,belgeId)' not in old_method:
            raise RuntimeError('Build516 unexpected existing Keşfet live join; manual review required')
    # The generated category UI can already call the shared join.
    old_tap="onTap:()=>_yayinIzle(context,y,yayinlar[i].id),"
    new_tap="onTap:()=>ngelxCanliYayinaKatil(context,yayinlar[i].id),"
    if old_tap in src:
        src=once(src,old_tap,new_tap,'Keşfet uses authorized shared live join')
    elif new_tap not in src:
        # Some previous UI patches rebuilt the entire section; do not
        # insert a guessed join into an unknown or unrelated card.
        if 'yayinlar[i].id' in src:
            raise RuntimeError('Build516 Keşfet category card join changed; manual QA required')
    # UI generations can remove entire old categories. Verify the new
    # actions are present and any pre-existing navigation controls remain.
    for needed in (
      MARK,
      "tooltip:'Canlı yayın ara'",
      "onPressed:()=>ngelxCanliAramaAc(context)",
      "label:const Text('Canlı ara')",
    ):
        if needed not in src:
            raise RuntimeError('Build516 missing global Keşfet live search '+needed)
    for preserved in (
      "onTap:_aramaAc,",
      "onPressed:_filtreAc",
      "_kesfetSekmesi(Icons.live_tv_rounded,t('live'),0)",
      "if(kategori==0)..._canliSliverleri()",
    ):
        if preserved in original and preserved not in src:
            raise RuntimeError('Build516 changed existing Keşfet action '+preserved)
    # If a generated Keşfet layout still contains its legacy live card,
    # that card must route through the existing authorized join. Other
    # generated layouts may no longer contain this category card at all.
    if old_tap in src:
        raise RuntimeError('Build516 legacy card still points at obsolete join')
    if 'yayinlar[i].id' in src and new_tap not in src:
        raise RuntimeError('Build516 generated live card has no verified secure join')
    if src.count(MARK)!=1:
        raise RuntimeError('Build516 marker should only appear once')
    return src

if __name__=='__main__':
    original=FILE.read_text(encoding='utf-8')
    updated=transform(original)
    if updated!=original:FILE.write_text(updated,encoding='utf-8')
    print('Build516: globally accessible Keşfet live search; reused authenticated LiveKit join (QA only)')
