"""Apply the device-feedback fixes to the exact assembled Build583 source."""
from pathlib import Path
import hashlib
import sys

root = Path(__file__).resolve().parents[1]
app = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else root / 'app'
lib = app / 'lib'
pub = app / 'pubspec.yaml'
s = (lib / 'build565_ludo.dart').read_text()
if 'Build584: ready dice' in s:
    assert 'version: 1.0.354+584' in pub.read_text()
    print('Build584 already applied')
    raise SystemExit

for name, digest in {
    'build565_ludo.dart': '28365cde600de82df43dfd95ad32fa05cf49f0707c5f1ee78a8a1c3aa68e1265',
    'build583_feedback.dart': 'a82d6627064c927ef5d18b81f5dc15a282a292f2e5df0c3aae011c56c8193c33',
}.items():
    assert hashlib.sha256((lib / name).read_bytes()).hexdigest() == digest, name

def one(text, old, new):
    assert text.count(old) == 1, (text.count(old), old[:100])
    return text.replace(old, new, 1)

# Historical results remain visible to the waiting opponent/spectator. The
# player who can roll sees GO in BOTH controls, including bonus/opening rolls.
s = one(s, 'value:ngelx570ShownDice(room),size:54',
        "value:myTurn&&room['dice']==null?null:ngelx570ShownDice(room),size:54")
s = one(s, "final lastRoll=room['lastRoll'] as Map?;\n    final shownDice=(room['dice'] as num?)?.toInt() ?? (lastRoll!=null && lastRoll['seat']==color ? (lastRoll['value'] as num?)?.toInt() : null);",
        "// Build584: ready dice show GO instead of a stale previous roll.\n    final shownDice=(room['dice'] as num?)?.toInt();")
# Show the actual last server result separately when GO replaces its pips.
s = one(s, "else Expanded(child:Text(widget.watch?'İZLEYİCİ':'KLASİK LUDO',textAlign:TextAlign.center,style:const TextStyle(color:Colors.white70,fontWeight:FontWeight.w800,fontSize:11))),",
        "else Expanded(child:Text(myTurn&&room['dice']==null&&room['lastRoll'] is Map?'Son zar: ${room['lastRoll']['value']}':widget.watch?'İZLEYİCİ':'KLASİK LUDO',textAlign:TextAlign.center,style:const TextStyle(color:Colors.white70,fontWeight:FontWeight.w800,fontSize:11))),")
# Expand vertically by up to ten percent into unused space. Flutter's FittedBox
# applies the same inverse transform to pointer events, preserving pawn targets.
s = one(s, 'final top=math.min(43.0,math.max(0.0,box.maxHeight-side-43));',
        'final boardHeight=math.min(side*1.10,math.max(side,box.maxHeight-86));\n  final top=math.max(43.0,(box.maxHeight-boardHeight)/2);')
s = one(s, 'top:top,width:side,height:side,child:Container(',
        "top:top,width:side,height:boardHeight,child:FittedBox(key:const ValueKey('ludo-expanded-board'),fit:BoxFit.fill,child:SizedBox(width:side,height:side,child:Container(")
s = one(s, 'onToken:onToken))))),', 'onToken:onToken))))))),')
s = one(s, 'top:isTop?top-43:top+side-2', 'top:isTop?top-43:top+boardHeight-2')
s = one(s, 'Ngelx583GiftFlight(room:room,seat:seat,side:side,left:left,top:top)',
        'Ngelx583GiftFlight(room:room,seat:seat,side:side,left:left,top:top,boardHeight:boardHeight)')
g = (lib / 'build583_feedback.dart').read_text()
g = one(g, 'final double side,left,top;', 'final double side,left,top;final double? boardHeight;')
g = one(g, 'required this.side,required this.left,required this.top});',
        'required this.side,required this.left,required this.top,this.boardHeight});')
g = one(g, 'widget.top+widget.side+20', 'widget.top+(widget.boardHeight??widget.side)+20')
(lib / 'build565_ludo.dart').write_text(s)
(lib / 'build583_feedback.dart').write_text(g)
pub.write_text(one(pub.read_text(), 'version: 1.0.353+583', 'version: 1.0.354+584'))
print('Build584 opposite-seat, ready-dice and expanded-board fixes applied')
