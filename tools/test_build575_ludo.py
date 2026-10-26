from pathlib import Path
s=Path('app/lib/build565_ludo.dart').read_text(encoding='utf-8')
checks={
 'auto toggle':'class Ngelx575AutoBadge',
 'visible auto button':"ValueKey('ludo-auto-toggle')",
 'can turn Auto off':"unawaited(game.perform('auto',{'enabled':!active}))",
 'server-selected Auto state':"autoSeats[seat.toString()]==true",
 'button in active game':'Ngelx575AutoBadge(enabled:auto',
 'existing legal-piece movement':'Future<void> _autoSingleMove574()',
 'existing prizes':'bonusTiles:room[\'bonusTiles\'] is List?',
 'existing powers':'_tapPower572(item.$1',
 'premium image crop':'w*.87,h*.94',
 'pawn shadow':"Colors.black.withValues(alpha:.34)",
 'nonoverlapping pieces':'widget.stackCount > 1 ? 0.52 : 0.98',
 'wallet':'class Ngelx573WalletBar',
 'existing lobby':'class Ngelx565LudoLobby',
 'existing game board':'class Ngelx565LudoBoard',
}
for name,needle in checks.items():
 assert needle in s,f'Build575 missing: {name}'
assert 'version: 1.0.345+575' in Path('app/pubspec.yaml').read_text()
assert s.count('class Ngelx575AutoBadge')==1
print('Build575 Ludo structure checks passed: Auto, quality and existing NgelX layout preserved')
