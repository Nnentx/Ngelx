from pathlib import Path
s=Path('app/lib/build565_ludo.dart').read_text()
checks={
 'visible clipped pawn correction':"final size=c*1.24,limit=c*15-size;",
 'stacked tokens':"ngelx572StackOffset(room,color,token)",
 'reference headline':"MAKİNEYE KARŞI",
 'classic heading':"return '$mode •",
 'larger pawn':"width:size,height:size",
 'actual dynamic Power icons':"tiles.containsKey('$i')",
 'Power action feedback':"_tapPower572(item.$1",
 'big die tap':"ValueKey('ludo-main-dice')",
 'preserved spectators':"room['spectatorCount']??0",
 'preserved invite':"class Ngelx565LudoInvitePicker",
}
for title,needle in checks.items():
 assert needle in s,title
p=Path('app/pubspec.yaml').read_text();assert 'version: 1.0.342+572' in p
print('Build572 reference visuals, dynamic pickups, input paths and app identity OK.')
