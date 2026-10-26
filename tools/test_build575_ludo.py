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
 'rounded pawn head':'radius:w*.235',
 'real media sounds':"assets/ludo575_$kind.wav",
 'server movement sounds':'_observeSound575()',
 'pawn shadow':"Colors.black.withValues(alpha:.34)",
 'nonoverlapping pieces':'widget.stackCount > 1 ? 0.52 : 0.98',
 'wallet':'class Ngelx573WalletBar',
 'sound control':"ValueKey('ludo-sound-toggle')",
 'sound persisted':"p.setBool('ngelx_ludo_sound',next)",
 'read-only profile':"ValueKey('ludo-profile-stats')",
 'daily gift UI':"ValueKey('ludo-daily-gift')",
 'treasure UI':"ValueKey('ludo-timed-chest')",
 'rematch':'Future<void> _rematch575()async',
 'profile reports':"'__report575'",
 'profile blocks':"'__block575'",
 'player tap callback declaration':'ValueChanged<Map<String,dynamic>>? onPlayerTap',
 'player avatar tap hit area':"ValueKey('ludo-player-${p['uid']}')",
 'player card mounted': 'onPlayerTap:widget.watch?null:_playerCard575',
 'spectators never get victory UI':"!widget.watch&&!game.detached&&game.seat>=0&&room['status']=='finished'",
 'victory feedback':"ValueKey('ludo-result-celebration')",
 'report reason picker':"'harassment','Rahatsız etme'",
 'gift blocked disabling':'onTap:alreadyBlocked575?null',
 'gift spending confirmation':"ValueKey('ludo-gift-confirmation')",
 'gift cancelled without spending':'if(!mounted||!confirmed)return;',
 'server price only':"final gift=items[selected];",
 'animated chip balance':'class Ngelx575AnimatedBalance',
 'existing lobby':'class Ngelx565LudoLobby',
 'existing game board':'class Ngelx565LudoBoard',
}
for name,needle in checks.items():
 assert needle in s,f'Build575 missing: {name}'
assert 'version: 1.0.346+576' in Path('app/pubspec.yaml').read_text()
assert s.count('class Ngelx575AutoBadge')==1
assert s.index("ValueKey('ludo-gift-confirmation')") < s.index("final ok=await game.perform('gift'")
assert "'kind':selected,'chips':" not in s
print('Build575 Ludo structure checks passed: Auto, quality and existing NgelX layout preserved')
