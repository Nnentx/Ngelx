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
    if 'part \'live_feed_card.dart\';' not in src:
        raise RuntimeError('Build516 requires existing searchable Keşfet live_feed_card part')
    if "void _aramaAc(){" not in src or "List<Widget> _canliSliverleri(" not in src:
        raise RuntimeError('Build516 existing Keşfet controls missing')
    old="""              Text(t('explore'),style:const TextStyle(color:Colors.black,fontSize:29,fontWeight:FontWeight.w900)),
              const Spacer(),
              // Build 372: the large search field below is the single search entry point.
              IconButton(tooltip:t('filter'),onPressed:_filtreAc,icon:const Icon(Icons.tune_rounded,color:Colors.black,size:25)),"""
    new="""              Text(t('explore'),style:const TextStyle(color:Colors.black,fontSize:29,fontWeight:FontWeight.w900)),
              const Spacer(),
              // Build516: always-available Keşfet live search.
              IconButton(
                tooltip:'Canlı yayın ara',
                onPressed:()=>ngelxCanliAramaAc(context),
                icon:const Icon(Icons.live_tv_rounded,color:Color(0xFFFF1744),size:24)),
              // Keep the existing general search field and filter untouched.
              IconButton(tooltip:t('filter'),onPressed:_filtreAc,icon:const Icon(Icons.tune_rounded,color:Colors.black,size:25)),"""
    src=once(src,old,new,'always-visible top right live discovery action')
    head="""    SliverToBoxAdapter(child:Padding(
      padding:const EdgeInsets.fromLTRB(16,18,16,10),
      child:Text(trend?'Trend canlı yayınlar':t('liveStreams'),style:const TextStyle(color:Colors.black,fontSize:21,fontWeight:FontWeight.w900)),
    )),"""
    headNext="""    SliverToBoxAdapter(child:Padding(
      padding:const EdgeInsets.fromLTRB(16,18,16,10),
      child:Row(children:[
        Expanded(child:Text(trend?'Trend canlı yayınlar':t('liveStreams'),
          style:const TextStyle(color:Colors.black,fontSize:21,fontWeight:FontWeight.w900))),
        TextButton.icon(
          onPressed:()=>ngelxCanliAramaAc(context),
          icon:const Icon(Icons.search_rounded,size:17),
          label:const Text('Canlı ara'),
          style:TextButton.styleFrom(foregroundColor:const Color(0xFFFF1744)),
        ),
      ]),
    )),"""
    src=once(src,head,headNext,'live section header search (also shown for empty results)')
    # Neutralize the old Keşfet join helper's DevelopmentTokenSource path.
    # Even if another legacy caller reuses it, the authenticated shared join
    # performs the same server-authorized LiveKit token and session checks.
    old_start='  Future<void> _yayinIzle(BuildContext context, Map<String, dynamic> veri, String belgeId) async {'
    start=src.find(old_start)
    end=src.find('  void _aramaAc(){',start)
    if start<0 or end<=start:
        raise RuntimeError('Build516 cannot isolate legacy Keşfet LiveKit join method')
    old_method=src[start:end]
    if old_method.count('lk.DevelopmentTokenSource(')!=1:
        raise RuntimeError('Build516 legacy DevelopmentTokenSource changed; manual security review required')
    src=src[:start]+"""  Future<void> _yayinIzle(BuildContext context, Map<String, dynamic> veri, String belgeId) async {
    await ngelxCanliYayinaKatil(context,belgeId);
  }

"""+src[end:]
    # The existing category grid used _yayinIzle with a DevelopmentTokenSource.
    # This card now reuses the authenticated join helper the video/feed uses.
    src=once(src,
      "onTap:()=>_yayinIzle(context,y,yayinlar[i].id),",
      "onTap:()=>ngelxCanliYayinaKatil(context,yayinlar[i].id),",
      'live list tap uses existing authenticated LiveKit join guard')
    for needed in (
      MARK,
      "tooltip:'Canlı yayın ara'",
      "onPressed:()=>ngelxCanliAramaAc(context)",
      "label:const Text('Canlı ara')",
      "onTap:()=>ngelxCanliYayinaKatil(context,yayinlar[i].id)",
      "onTap:_aramaAc,",
      "onPressed:_filtreAc",
      "_kesfetSekmesi(Icons.live_tv_rounded,t('live'),0)",
      "if(kategori==0)..._canliSliverleri()",
    ):
        if needed not in src:raise RuntimeError('Build516 lost Keşfet/legacy control '+needed)
    if src.count(MARK)!=1:
        raise RuntimeError('Build516 marker should only appear once')
    return src

if __name__=='__main__':
    original=FILE.read_text(encoding='utf-8')
    updated=transform(original)
    if updated!=original:FILE.write_text(updated,encoding='utf-8')
    print('Build516: globally accessible Keşfet live search; reused authenticated LiveKit join (QA only)')
