import 'dart:async';
import 'dart:io';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import '../lib/build589_gift_sound.dart';
import '../lib/build589_audio_seat.dart';
import '../lib/main.dart';

void main() {
  setUpAll(() async {
    final font=File('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf');
    if(font.existsSync())await (FontLoader('Roboto')..addFont(Future.value(ByteData.view(font.readAsBytesSync().buffer)))).load();
    final root=Platform.environment['FLUTTER_ROOT']??Platform.resolvedExecutable.split('/bin/cache/dart-sdk/').first;
    final icons=File('$root/bin/cache/artifacts/material_fonts/MaterialIcons-Regular.otf');
    if(icons.existsSync())await (FontLoader('MaterialIcons')..addFont(Future.value(ByteData.view(icons.readAsBytesSync().buffer)))).load();
  });
  test('muting while a gift asset is loading prevents any playback',() async {
    var active=true;final loading=Completer<void>();final calls=<String>[];
    final pending=ngelx589PlayGiftSound(allowed:()=>active,
      load:()async{calls.add('load');await loading.future;},
      volume:()async{calls.add('volume');},play:()async{calls.add('play');});
    active=false;loading.complete();await pending;expect(calls,['load']);
  });
  test('muting or disposing during volume setup prevents playback',() async {
    var active=true;final volume=Completer<void>();final calls=<String>[];
    final pending=ngelx589PlayGiftSound(allowed:()=>active,
      load:()async{calls.add('load');},volume:()async{calls.add('volume');await volume.future;},
      play:()async{calls.add('play');});
    await Future<void>.delayed(Duration.zero);active=false;volume.complete();await pending;
    expect(calls,['load','volume']);
  });
  test('enabled playback runs once in load-volume-play order',() async {
    final calls=<String>[];
    await ngelx589PlayGiftSound(allowed:()=>true,load:()async{calls.add('load');},
      volume:()async{calls.add('volume');},play:()async{calls.add('play');});
    expect(calls,['load','volume','play']);
    await ngelx589PlayGiftSound(allowed:()=>false,load:()async{fail('muted load');},
      volume:()async{fail('muted volume');},play:()async{fail('muted play');});
  });
  for(final size in [const Size(360,640),const Size(393,852)]) {
    testWidgets('nine actual audio seats fit ${size.width} with large text',(tester)async {
      tester.view.physicalSize=size;tester.view.devicePixelRatio=1;
      addTearDown(tester.view.resetPhysicalSize);addTearDown(tester.view.resetDevicePixelRatio);
      var requests=0;
      await tester.pumpWidget(MaterialApp(theme:ThemeData.dark(),home:MediaQuery(
        data:MediaQueryData(size:size,textScaler:TextScaler.linear(1.6)),
        child:RepaintBoundary(key:const ValueKey('capture589'),child:Scaffold(backgroundColor:Colors.black,
          appBar:AppBar(backgroundColor:Colors.black,title:const Text('Sesli oda',style:TextStyle(fontSize:18))),
          body:GridView.builder(padding:const EdgeInsets.all(16),
            gridDelegate:const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount:3,crossAxisSpacing:8,mainAxisSpacing:8,childAspectRatio:.88),
            itemCount:9,itemBuilder:(_,i)=>i==8?Ngelx589AudioSeat(key:const ValueKey('empty589'),empty:true,onTap:()=>requests++)
              :Ngelx589AudioSeat(name:i==0?'Yayıncı':i==1?'Uzun kullanıcı adı denemesi':'Katılımcı ${i+1}',
                role:i==0?'Davet sahibi':i==1?'🛡 Moderatör':'',host:i==0,speaking:i==2,micOpen:i==0||i==2))
        )))));
      await tester.pump(const Duration(milliseconds:250));expect(find.byType(Ngelx589AudioSeat),findsNWidgets(9));
      expect(tester.takeException(),isNull);
      for(final element in find.byType(CircleAvatar).evaluate()) {
        final bounds=element.renderObject!.paintBounds.size;
        expect(bounds.width,closeTo(bounds.height,.1));
      }
      await tester.tap(find.byKey(const ValueKey('empty589')));await tester.pump();expect(requests,1);
      final boundary=tester.renderObject<RenderRepaintBoundary>(find.byKey(const ValueKey('capture589')));
      final image=await boundary.toImage(pixelRatio:1);final data=await image.toByteData(format:ui.ImageByteFormat.png);
      final file=File('test/screenshots/build589_audio_${size.width.toInt()}.png');file.parent.createSync(recursive:true);file.writeAsBytesSync(data!.buffer.asUint8List());image.dispose();
      await tester.pumpWidget(const SizedBox());
    });
  }
  testWidgets('gift stream fits small screen with large text',(tester)async {
    tester.view.physicalSize=const Size(320,480);tester.view.devicePixelRatio=1;
    addTearDown(tester.view.resetPhysicalSize);addTearDown(tester.view.resetDevicePixelRatio);
    await tester.pumpWidget(const MaterialApp(home:MediaQuery(data:MediaQueryData(size:Size(320,480),textScaler:TextScaler.linear(1.8)),
      child:Scaffold(body:Ngelx588GiftFlow(emoji:'❤️',name:'Kalp',sender:'Uzun gönderici adı kontrolü',quantity:10)))));
    await tester.pump(const Duration(milliseconds:900));expect(tester.takeException(),isNull);expect(find.text('❤️'),findsNWidgets(36));
    await tester.pumpWidget(const SizedBox());
  });
}
