from pathlib import Path
from collections import Counter
s=Path('app/lib/build565_ludo.dart').read_text()
checks={
 'board takes wider screen':'aspectRatio:.78,child:frame',
 'track pawn is below 1 cell':'widget.stackCount > 1 ? 0.49 : 0.91',
 'overlap group sizing':'int ngelx573PawnCount(',
 'wallet placeholder avoids fictitious currency':'amount is num?amount.toInt().toString():\'—\'',
 'levels from actual player data':"p['level'] is num?",
 'compact controls':'Sıra sende',
 'premium background':'_LudoBackdropPainter573',
 'real dice callback':"_tapRoll572(myTurn)",
 'power touch callback':"_tapPower572(item.$1",
 'match status':'Ngelx567WaitingPanel',
 'spectators':"spectatorCount",
 'chat':'Ngelx570ChatPanel'
}
for name,needle in checks.items():
 assert needle in s,name
assert 'version: 1.0.343+573' in Path('app/pubspec.yaml').read_text()
assert s.count("class Ngelx573WalletBar")==1
assert s.count("class _LudoBackdropPainter573")==1
print('Build573 reference layout and preserved game behavior markers PASS')
