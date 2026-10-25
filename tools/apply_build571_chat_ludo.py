"""Add Ludo entry to existing private/group chat attach menus; preserve every other action."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
p = root / 'app/lib/main.dart'
s = p.read_text(encoding='utf-8')

# Existing group message composer + menu uses a grid of attachments.
needle = """              Expanded(child:_ekSecenek(c,Icons.location_on_rounded,'Konum','location')),

            ]),"""
replacement = """              Expanded(child:_ekSecenek(c,Icons.location_on_rounded,'Konum','location')),

            ]),
            const SizedBox(height:10),
            Row(children:[Expanded(child:_ekSecenek(c,Icons.casino_rounded,'Ludo','ludo'))]),"""
assert s.count(needle) == 1, 'Group attachments layout changed; inspect before patching'
s = s.replace(needle, replacement, 1)
needle = """    else if(secim=='location')await grupKonumGonder();
    else if(secim=='sticker')await stickerGonder();"""
replacement = """    else if(secim=='location')await grupKonumGonder();
    else if(secim=='ludo')await Navigator.push(context,MaterialPageRoute(builder:(_)=>const Ngelx565LudoLobby()));
    else if(secim=='sticker')await stickerGonder();"""
assert s.count(needle) == 1, 'Group attach action changed; inspect before patching'
s = s.replace(needle, replacement, 1)

# Existing private message composer + list includes Oyun; Ludo deserves its own choice.
needle = """                                    ListTile(leading:const Icon(Icons.sports_esports_rounded,color:ngelxPrivateBlue),title:const Text('Oyun',style:TextStyle(color:Colors.black87)),onTap:()=>Navigator.pop(sheetContext,'game')),"""
replacement = needle + """
                                    ListTile(leading:const Icon(Icons.casino_rounded,color:ngelxPrivateBlue),title:const Text('Ludo oyna',style:TextStyle(color:Colors.black87)),subtitle:const Text('Arkadaşına oyun daveti gönder',style:TextStyle(color:Colors.black54)),onTap:()=>Navigator.pop(sheetContext,'ludo')),"""
assert s.count(needle) == 1, 'Private attachments menu changed; inspect before patching'
s = s.replace(needle, replacement, 1)
needle = """                          else if(secim=='game')await Navigator.push(context,MaterialPageRoute(builder:(_)=>const NgelXMiniOyunPage()));"""
replacement = needle + """
                          else if(secim=='ludo')await Navigator.push(context,MaterialPageRoute(builder:(_)=>const Ngelx565LudoLobby()));"""
assert s.count(needle) == 1, 'Private attachment action changed; inspect before patching'
s = s.replace(needle, replacement, 1)
p.write_text(s, encoding='utf-8')

p = root / 'app/pubspec.yaml'
s = p.read_text(encoding='utf-8')
assert 'version: 1.0.340+570' in s, 'Unexpected baseline version; do not overwrite'
p.write_text(s.replace('version: 1.0.340+570', 'version: 1.0.341+571', 1), encoding='utf-8')
print('Build571: both chat plus menus expose Ludo; existing invite picker sends draft to private/group chats')
