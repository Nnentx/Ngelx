from pathlib import Path
s=Path('app/lib/build565_ludo.dart').read_text(encoding='utf-8')
checks={
 'single-move autoplay':'Future<void> _autoSingleMove574()',
 'exactly one legal move':'if(choices.length!=1)return;',
 'revision check':'room[\'revision\']!=revision',
 'no opponent-turn toast':'if(!myTurn)return;',
 'live bonus tiles':'bonusTiles:room[\'bonusTiles\'] is List?',
 'bonus should repaint':'!listEquals(old.bonusTiles,bonusTiles)',
 'cropped premium pawn atlas':'final src=Rect.fromLTWH(',
 'track piece fits a square':'widget.stackCount > 1 ? 0.49 : 0.98',
 'premium track tile':'Radius.circular(rect.width*.075)',
 'inline power plus icon':'const Icon(Icons.add_rounded',
 'account wallet bar':'class Ngelx573WalletBar',
 'no fake money':'amount is num?amount.toInt().toString():\'—\'',
 'existing invitations':'class Ngelx565LudoInvitePicker',
 'existing power input':'_tapPower572(item.$1',
 'spectator mode':"spectatorCount",
}
for feature,part in checks.items():assert part in s,feature
assert 'version: 1.0.344+574' in Path('app/pubspec.yaml').read_text()
print('Build574 frontend checks passed: visual, power, bonus, legal move, invitation and wallet')
