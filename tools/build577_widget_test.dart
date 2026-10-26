import 'dart:async';
import 'dart:io';
import 'dart:typed_data';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import '../lib/main.dart';
import '../lib/build567_room_controller.dart';

Map<String,dynamic> room577({int revision=1,String status='playing',bool oneMove=false})=>{
 'id':'859819','owner':'a','capacity':2,'status':status,'revision':revision,
 'mode':'power','team':false,'botGame':true,'chips':5000,'gems':0,
 'players':[{'uid':'a','seat':0,'name':'Sen','level':1},{'uid':'bot','seat':2,'name':'Makine 1','bot':true}],
 'tokens':[oneMove?[-1,10,-1,-1]:[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1]],
 'power':List.generate(4,(_)=>{'control':2,'double':1,'shield':1}),
 'turn':0,'dice':oneMove?1:null,'deadline':DateTime.now().millisecondsSinceEpoch+10000,
 'shields':<String,dynamic>{},'autoSeats':<String,dynamic>{},'chat':[],'winner':null,
};
Future<void> settle577(WidgetTester tester)async{
 // The live room has a clock and periodic polling; do not wait for every animation to stop.
 await tester.pump(const Duration(milliseconds:350));await tester.pump();
}
Future<void> savePreview(WidgetTester tester,String name)async{
 final boundary=tester.renderObject<RenderRepaintBoundary>(find.byKey(const ValueKey('preview577')));
 await tester.runAsync(()async{
  final frame=await boundary.toImage(pixelRatio:2);
  final bytes=await frame.toByteData(format:ui.ImageByteFormat.png);
  Directory('build577-previews').createSync();
  File('build577-previews/$name.png').writeAsBytesSync(bytes!.buffer.asUint8List());frame.dispose();
 });
}
void main(){
 test('578 feet stay on socket/cell center while heads extend upward',(){
  for(final cell in [20.0,26.0,45.0])for(final position in [-1,0,30]){
   final size=ngelx578PawnSize(cell,position,1),foot=ngelx578FootY(100,cell,position),top=ngelx578PawnTop(foot,size);
   expect(top+size*.89,closeTo(position<0?100:100+cell*.28,.000001));
   if(position>=0){expect(top,lessThan(100-cell*.5));expect(foot,lessThan(100+cell*.5));}
   expect(size,greaterThan(cell));
   expect(ngelx578PawnLeft(cell*.5,size)+size*.5,closeTo(cell*.5,.000001));
  }
  expect(ngelx578PawnTop(10,45),lessThan(0));
  expect(ngelx578PawnSize(30,4,2),lessThan(30));
 });

 TestWidgetsFlutterBinding.ensureInitialized();
 setUpAll(()async{
  final text=File('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf');
  if(text.existsSync())await (FontLoader('Roboto')..addFont(Future.value(ByteData.view(text.readAsBytesSync().buffer)))).load();
  final root=Platform.environment['FLUTTER_ROOT']??Platform.resolvedExecutable.split('/bin/cache/dart-sdk/').first;
  final icons=File('$root/bin/cache/artifacts/material_fonts/MaterialIcons-Regular.otf');
  if(icons.existsSync())await (FontLoader('MaterialIcons')..addFont(Future.value(ByteData.view(icons.readAsBytesSync().buffer)))).load();
 });
 test('leave survives repeated real revision conflicts and retains one idempotency key',()async{
  final calls=<Map<String,dynamic>>[];var leaves=0,revision=1;
  final controller=Ngelx567RoomController(id:'859819',uid:'a',initial:room577(),request:(body)async{
   calls.add(Map.of(body));
   if(body['action']=='leave'){
    leaves++;if(leaves<3){revision++;throw const Ngelx567Failure('state_changed','stale');}
    return room577(revision:revision+1,status:'closed');
   }
   return room577(revision:revision);
  });
  expect(await controller.leave(),true);
  expect(leaves,3);expect(controller.detached,true);
  expect(calls.where((b)=>b['action']=='leave').map((b)=>b['requestId']).toSet().length,1);
  expect(controller.error,isEmpty);controller.dispose();
 });
 testWidgets('production 3D sprite painter at gameplay sizes',(tester)async{
  final atlas=await tester.runAsync(()=>ngelx570PawnSprite());
  expect(atlas,isNotNull);expect(atlas!.width,1254);expect(atlas.height,1254);
  final bytes=await tester.runAsync(()=>atlas.toByteData(format:ui.ImageByteFormat.rawRgba));
  expect(bytes!.getUint8(3),0); // real alpha rather than a baked black/white background
  tester.view.physicalSize=const Size(393,240);tester.view.devicePixelRatio=1;
  addTearDown(tester.view.resetPhysicalSize);addTearDown(tester.view.resetDevicePixelRatio);
  await tester.pumpWidget(MaterialApp(home:Scaffold(body:RepaintBoundary(key:const ValueKey('preview577'),child:Container(
   color:const Color(0xFF163D62),padding:const EdgeInsets.all(16),child:Column(mainAxisSize:MainAxisSize.min,children:[
    for(final size in [28.0,44.0,80.0])Row(mainAxisAlignment:MainAxisAlignment.spaceEvenly,children:[
     for(var seat=0;seat<4;seat++)SizedBox(width:size,height:size,child:CustomPaint(painter:Ngelx570SpritePainter(seat,false,atlas))),
    ]),
   ]),
  )))));
  await settle577(tester);expect(tester.takeException(),isNull);await savePreview(tester,'actual-sprites-28-44-80px');
  await tester.pumpWidget(const SizedBox());
 });
 test('leave conflict exhaustion remains an error and never fabricates detachment',()async{
  var attempts=0;
  final controller=Ngelx567RoomController(id:'859819',uid:'a',initial:room577(),request:(body)async{
   if(body['action']=='leave'){attempts++;throw const Ngelx567Failure('state_changed','conflict');}
   return room577(revision:attempts+1);
  });
  expect(await controller.leave(),false);expect(attempts,4);expect(controller.detached,false);
  expect(controller.error,'conflict');controller.dispose();
 });
}
