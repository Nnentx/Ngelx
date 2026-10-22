from pathlib import Path
source=Path('app/lib/main.dart').read_text()
a=source.index('String? _media448;');b=source.index('\nbool ngelx444ReserveCall',a)
body=source[a:b]
Path('app/test/build554_media_test.dart').write_text('''import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
class _Call { bool busy=false; }
final ngelxCallSession444=_Call();
int blocked=0;
void ngelxDurumMesaji(BuildContext context,String text,{String tip='bilgi'}){blocked++;}
'''+body+'''
void main(){
  setUp((){_media448=null;_media448Stop=null;_mediaClose554=null;_mediaEpoch554=0;blocked=0;});
  testWidgets('ended live summary releases admission without waiting for route pop',(tester)async{
    late BuildContext context;
    await tester.pumpWidget(MaterialApp(home:Builder(builder:(c){context=c;return const SizedBox();})));
    final route=Completer<void>();
    final old=ngelx448MediaSession(context,'live-host',()=>route.future);
    expect(_media448,'live-host');
    ngelx554ReleaseMedia(_mediaEpoch554);
    var entered=false;
    await ngelx448MediaSession(context,'live:next',()async{entered=true;});
    expect(entered,isTrue);expect(blocked,0);
    route.complete();await old;
  });
  testWidgets('old route completion cannot clear replacement session of same name',(tester)async{
    late BuildContext context;
    await tester.pumpWidget(MaterialApp(home:Builder(builder:(c){context=c;return const SizedBox();})));
    final first=Completer<void>(),second=Completer<void>();
    final old=ngelx448MediaSession(context,'live-host',()=>first.future);
    _mediaClose554=()async{};
    await ngelx554BeforeAccountChange();
    final next=ngelx448MediaSession(context,'live-host',()=>second.future);
    first.complete();await old;
    expect(_media448,'live-host');
    second.complete();await next;expect(_media448,isNull);
  });
  testWidgets('account handoff awaits media shutdown and fails closed on cleanup error',(tester)async{
    late BuildContext context;
    await tester.pumpWidget(MaterialApp(home:Builder(builder:(c){context=c;return const SizedBox();})));
    final route=Completer<void>(),disconnect=Completer<void>();
    final session=ngelx448MediaSession(context,'live-host',()=>route.future);
    _mediaClose554=()=>disconnect.future;
    var finished=false;
    final cleanup=ngelx554BeforeAccountChange().then((_){finished=true;});
    await tester.pump();expect(finished,isFalse);
    disconnect.complete();await cleanup;expect(_media448,isNull);
    route.complete();await session;
    _media448='live:other';_mediaClose554=()async{throw StateError('network');};
    await expectLater(ngelx554BeforeAccountChange(),throwsStateError);
    expect(_media448,'live:other');
  });
}
''')
