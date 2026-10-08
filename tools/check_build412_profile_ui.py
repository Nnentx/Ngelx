#!/usr/bin/env python3
from pathlib import Path
s=Path('app/lib/main.dart').read_text(encoding='utf-8')
owner=s[s.index('class _ProfilPageState extends State<ProfilPage>'):s.index('class _ProfilEtkilesimRozeti')]
visitor=s[s.index('class _KullaniciProfilPageState extends State<KullaniciProfilPage>'):s.index('class NgelXVideoKapakOnizleme')]
edit=s[s.index('class NgelXOnayliProfilDuzenlePage'):s.index('class ProfilPage extends StatefulWidget')]
checks={
 'owner profile mode still stored':"profileViewMode" in owner,
 'owner original cover editing':"kapakFotografiDuzenle" in owner,
 'visitor uses actual cover field':"v['coverPhotoUrl']" in visitor and 'NgelXAgImageProvider(profilKapak)' in visitor,
 'coverless centered avatar and decor':'if(kapaksiz)...[' in visitor and '_ziyaretciReferansAvatar' in visitor,
 'covered avatar overlapping banner':'Positioned(left:8,top:111' in visitor,
 'live state validation retained':'ngelxCanliKaydiTaze(' in visitor and "const Color(0xFFFF1744)" in visitor,
 'four purple statistics card':'const Color(0xFFF7F2FF)' in visitor and 'Icons.bar_chart_rounded' in visitor,
 'follow original callback':'takipDurumuDegistir(uid' in visitor and 'sosyalIstekGonder' in visitor,
 'message original callback':'profildenMesajAc(' in visitor,
 'friendship original callback':'_arkadasliktanCikar' in visitor and 'friend_request' in visitor,
 'mutual groups original navigation':'OrtakGruplarPage(digerUid:uid)' in visitor,
 'intro playback original widget':'ProfilTanitimVideoKarti(url:' in visitor,
 'privacy and block gating unchanged':'profileViewPermission' in visitor and 'if (!erisimVar)' in visitor and 'kullaniciyiEngelle' in visitor,
 'tagged reels tabs preserved':"_ProfilSekme(t('tagged')" in visitor and "_ProfilSekme(t('reels')" in visitor,
 'editable mode and preview retained':"'profileViewMode':_gorunum" in edit and '_onizlemeAc' in edit,
 'colorful cover-required warning':'kapakUyarisi:true' in edit and 'Color(0xFFFFE5AA)' in edit,
 'bottom nav safe area':"MediaQuery.of(context).viewPadding.bottom" in edit and "MediaQuery.of(context).viewInsets.bottom" in edit,
 'no external Firebase rules changes':'allow' not in edit,
}
for title,ok in checks.items():print(('PASS ' if ok else 'FAIL ')+title,flush=True)
if not all(checks.values()):raise SystemExit('Build 412 regression guard failed')
print('Build 412 profile reference and functionality contract PASSED.')
