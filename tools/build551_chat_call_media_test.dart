import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:image/image.dart' as img;
import '../lib/main.dart' show Ngelx551MediaReaction,Ngelx551CallGrid;
import '../lib/build551_media.dart';

void main(){
  testWidgets('heart follows the right edge of portrait and landscape media after resize',(tester)async{
    var taps=0;
    for(final size in [const Size(140,300),const Size(250,130),const Size(195,220)]){
      await tester.pumpWidget(MaterialApp(home:Scaffold(body:Align(alignment:Alignment.topLeft,
        child:Ngelx551MediaReaction(media:SizedBox(key:const ValueKey('photo'),width:size.width,height:size.height),
          badge:GestureDetector(onTap:()=>taps++,child:const SizedBox(key:ValueKey('badge'),width:42,height:24)))))));
      final photo=tester.getRect(find.byKey(const ValueKey('photo')));
      final badge=tester.getRect(find.byKey(const ValueKey('badge')));
      expect(badge.right,closeTo(photo.right,.01));
      expect(badge.bottom,closeTo(photo.bottom+12,.01));
      await tester.tap(find.byKey(const ValueKey('badge')));
      expect(tester.takeException(),isNull);
    }
    expect(taps,3);
  });
  testWidgets('two voice seats stay compact across narrow wide and short screens',(tester)async{
    for(final size in [const Size(360,650),const Size(320,420),const Size(700,260)]){
      await tester.pumpWidget(MaterialApp(home:Scaffold(body:SizedBox(width:size.width,height:size.height,
        child:Ngelx551CallGrid(count:2,columns:2,voice:true,itemBuilder:(_,i)=>ColoredBox(key:ValueKey('person-$i'),color:Colors.purple))))));
      final first=tester.getRect(find.byKey(const ValueKey('person-0')));
      final second=tester.getRect(find.byKey(const ValueKey('person-1')));
      expect(first.height,lessThanOrEqualTo(320));
      expect(first.height,lessThanOrEqualTo(first.width*1.35+.01));
      expect(first.overlaps(second),isFalse);
      expect(first.top,greaterThanOrEqualTo(0));
      expect(first.bottom,lessThanOrEqualTo(size.height));
      expect(find.byKey(const ValueKey('person-1')),findsOneWidget);
      expect(tester.takeException(),isNull);
    }
  });
  testWidgets('video and larger groups retain full available grid height',(tester)async{
    for(final entry in [(2,false),(4,true)]){
      await tester.pumpWidget(MaterialApp(home:Scaffold(body:SizedBox(width:360,height:600,
        child:Ngelx551CallGrid(count:entry.$1,columns:2,voice:entry.$2,itemBuilder:(_,i)=>ColoredBox(key:ValueKey('person-$i'),color:Colors.purple))))));
      final last=tester.getRect(find.byKey(ValueKey('person-${entry.$1-1}')));
      expect(last.bottom,closeTo(588,.01));
      expect(tester.takeException(),isNull);
    }
  });
  test('chat caps are valid readable bounded JPEG; other media kinds unchanged',(){
    for(final kind in ['groups','chats','chat-images']){expect(ngelx551ChatPhotoKind(kind),isTrue);}
    for(final kind in ['profiles','stories','videos','gifs']){expect(ngelx551ChatPhotoKind(kind),isFalse);}
    final input=img.Image(width:2000,height:1000)..clear(img.ColorRgb8(40,100,180));
    final output=ngelx551ChatJpeg(Uint8List.fromList(img.encodePng(input)));
    final decoded=img.decodeJpg(output)!;
    expect(decoded.width,1600);expect(decoded.height,800);
    final pixel=decoded.getPixel(700,300);
    expect(pixel.r,closeTo(40,5));expect(pixel.g,closeTo(100,5));
    expect(()=>ngelx551ChatJpeg(Uint8List.fromList([0,1,2,3])),throwsFormatException);
  });
}
