"""Lightweight validation of both chat '+' launch routes and preserved game invites."""
from pathlib import Path
s = Path('app/lib/main.dart').read_text(encoding='utf-8')
assert "_ekSecenek(c,Icons.casino_rounded,'Ludo','ludo')" in s
assert "ListTile(leading:const Icon(Icons.casino_rounded,color:ngelxPrivateBlue),title:const Text('Ludo oyna'" in s
assert s.count("else if(secim=='ludo')await Navigator.push(context,MaterialPageRoute(builder:(_)=>const Ngelx565LudoLobby()));") == 2
ludo = Path('app/lib/build565_ludo.dart').read_text(encoding='utf-8')
assert 'class Ngelx565LudoInvitePicker' in ludo
assert 'GrupSohbetPage(chatId:chat.id' in ludo and 'draft565:draft' in ludo
assert 'SohbetPage(chatId:chat.id' in ludo and 'draft565:draft' in ludo
assert '🎲 Ludo daveti' in ludo
assert Path('app/pubspec.yaml').read_text(encoding='utf-8').count('version: 1.0.341+571') == 1
print('Build571 chat Ludo menus, routing and invite draft paths verified')
