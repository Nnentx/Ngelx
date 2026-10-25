import 'dart:io';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import '../lib/main.dart';
Map<String,dynamic> table(String mode,int count)=>{'id':'534157','owner':'a','capacity':count,'status':'playing','revision':1,'mode':mode,'team':false,'deadline':DateTime.now().millisecondsSinceEpoch+10000,'spectatorCount':12,'players':[for(var i=0;i<count;i++){'uid':i==0?'a':'p$i','seat':count==2?i*2:i,'name':['Sen','Ahsen','Ali','Hediye'][i]}],'tokens':List.generate(4,(_)=>[-1,-1,-1,-1]),'power':List.generate(4,(_)=>{'control':3,'double':2,'shield':2}),'turn':0,'dice':5,'chat':[]};
void main(){
 setUpAll(()async{
  final text=File('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf');
  if(text.existsSync())await (FontLoader('Roboto')..addFont(Future.value(ByteData.view(text.readAsBytesSync().buffer)))).load();
  final root=Platform.environment['FLUTTER_ROOT']??Platform.resolvedExecutable.split('/bin/cache/dart-sdk/').first;
  final icons=File('$root/bin/cache/artifacts/material_fonts/MaterialIcons-Regular.otf');
  if(icons.existsSync())await (FontLoader('MaterialIcons')..addFont(Future.value(ByteData.view(icons.readAsBytesSync().buffer)))).load();
 });

 for(final mode in ['classic','power']){for(final count in [2,4]){testWidgets('$mode $count player controls and actual sprite artwork render',(t)async{
  t.view.physicalSize=const Size(393,851);t.view.devicePixelRatio=1;addTearDown(t.view.resetPhysicalSize);addTearDown(t.view.resetDevicePixelRatio);
  await t.runAsync(()=>ngelx570PawnSprite());
  final room=table(mode,count);
  await t.pumpWidget(MaterialApp(home:RepaintBoundary(key:const ValueKey('capture570'),child:Ngelx565LudoRoom(id:'534157',userId:'a',initial:room,request:(b)async=>room))));await t.pumpAndSettle();
  expect(find.byType(Ngelx570Power),mode=='power'?findsNWidgets(3):findsNothing);expect(find.text('12'),findsOneWidget);expect(t.takeException(),isNull);
  final painted=t.widgetList<CustomPaint>(find.byType(CustomPaint)).map((w)=>w.painter).whereType<Ngelx570SpritePainter>().toList();expect(painted,isNotEmpty);expect(painted.every((p)=>p.image!=null),true);
  expect(t.getRect(find.text('Sohbet')).bottom,lessThanOrEqualTo(851));
  await t.runAsync(()async{final boundary=t.renderObject<RenderRepaintBoundary>(find.byKey(const ValueKey('capture570'))),image=await boundary.toImage(pixelRatio:2),bytes=await image.toByteData(format:ui.ImageByteFormat.png);Directory('build567-previews').createSync();File('build567-previews/$mode-$count.png').writeAsBytesSync(bytes!.buffer.asUint8List());image.dispose();});
  await t.pumpWidget(const SizedBox());
 });}}
 testWidgets('watcher cannot roll or invoke powers',(t)async{
  final calls=<String>[];final room=table('power',4);
  await t.pumpWidget(MaterialApp(home:Ngelx565LudoRoom(id:'534157',userId:'viewer',watch:true,initial:room,request:(b)async{calls.add(b['action']);return room;})));await t.pumpAndSettle();expect(find.text('Oyunu izliyorsun'),findsOneWidget);expect(find.byType(Ngelx570Power),findsNothing);expect(calls,isEmpty);expect(t.takeException(),isNull);await t.pumpWidget(const SizedBox());
 });
 testWidgets('typing retains focus and draft during live game updates',(t)async{
  t.view.physicalSize=const Size(393,851);t.view.devicePixelRatio=1;addTearDown(t.view.resetPhysicalSize);addTearDown(t.view.resetDevicePixelRatio);
  var room=table('power',2);
  await t.pumpWidget(MaterialApp(home:Ngelx565LudoRoom(id:'534157',userId:'a',initial:room,request:(b)async=>room)));
  await t.tap(find.byTooltip('Emoji ve sohbet'));await t.pumpAndSettle();await t.tap(find.byKey(const ValueKey('ludo-chat-input')));await t.enterText(find.byType(TextField),'Mesajım kaybolmasın');
  final before=t.state<EditableTextState>(find.byType(EditableText));
  room={...room,'revision':2,'chat':[{'uid':'p1','name':'Ahsen','text':'Merhaba','at':DateTime.now().millisecondsSinceEpoch}]};
  await t.pump(const Duration(seconds:4));await t.pump();
  expect(identical(before,t.state<EditableTextState>(find.byType(EditableText))),true);expect(before.widget.controller.text,'Mesajım kaybolmasın');expect(before.widget.focusNode.hasFocus,true);expect(t.takeException(),isNull);await t.pumpWidget(const SizedBox());
 });

}
