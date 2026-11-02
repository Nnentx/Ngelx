import 'dart:io';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import '../lib/build590_audio_stage.dart';

void main() {
  setUpAll(() async {
    final font=File('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf');
    if(font.existsSync())await (FontLoader('Roboto')..addFont(Future.value(ByteData.view(font.readAsBytesSync().buffer)))).load();
    final root=Platform.environment['FLUTTER_ROOT']??Platform.resolvedExecutable.split('/bin/cache/dart-sdk/').first;
    final icons=File('$root/bin/cache/artifacts/material_fonts/MaterialIcons-Regular.otf');
    if(icons.existsSync())await (FontLoader('MaterialIcons')..addFont(Future.value(ByteData.view(icons.readAsBytesSync().buffer)))).load();
  });
  for(final config in [(const Size(393,852),1.0,false),(const Size(393,852),1.0,true),
    (const Size(360,640),1.6,false),(const Size(320,568),1.0,false)]) {
    testWidgets('full production composition ${config.$1} scale ${config.$2} solo ${config.$3}',(tester)async{
      final size=config.$1,scale=config.$2,solo=config.$3;
      tester.view.physicalSize=size;tester.view.devicePixelRatio=1;
      addTearDown(tester.view.resetPhysicalSize);addTearDown(tester.view.resetDevicePixelRatio);
      final input=TextEditingController();addTearDown(input.dispose);
      var request=0,close=0,follow=0,send=0,menu=0;
      final photos=List.generate(8,(i)=>MemoryImage(File('test/fixtures590/avatar$i.png').readAsBytesSync()));
      final names=['25.EYL.A.04','49 Mustafa','EZ KURBAN25','Keva','Roje','Ayşe 04','Hülya','DEMİR'];
      await tester.pumpWidget(MaterialApp(theme:ThemeData.dark(),home:MediaQuery(
        data:MediaQueryData(size:size,padding:const EdgeInsets.only(top:24,bottom:24),textScaler:TextScaler.linear(scale)),
        child:RepaintBoundary(key:const ValueKey('capture590'),child:Scaffold(backgroundColor:Colors.black,
          body:Ngelx590AudioStage(
            header:Ngelx590RoomHeader(name:'25.EYL.A.04',title:'Sohbet ve müzik',audience:84,photo:photos.first,
              onFollow:()=>follow++,onClose:()=>close++),
            controls:const Row(children:[
              Expanded(child:Ngelx590RoomChip(child:Text('CANLI 01:24',style:TextStyle(fontSize:12)))),SizedBox(width:6),
              Expanded(child:Ngelx590RoomChip(child:Text('Müzik',style:TextStyle(fontSize:12)))),SizedBox(width:6),
              Expanded(child:Ngelx590RoomChip(child:Text('PK daveti',style:TextStyle(fontSize:12)))),
            ]),
            seatBuilder:(_,i)=>(solo?i>0:i==8)?Ngelx590AudioSeat(empty:true,onTap:()=>request++)
              :Ngelx590AudioSeat(name:names[i],role:i==0?'Davet sahibi':i==2?'Moderatör':'',photo:photos[i],host:i==0,
                speaking:i==2,micOpen:i==0||i==2,onTap:()=>request++),
            chat:Column(children:[Expanded(child:ListView(reverse:true,children:[
              Ngelx590AudioComment(name:'Gamzeli',message:'CANLI yayını beğendi',photo:photos[0]),
              Ngelx590AudioComment(name:'mamoste dedo',message:'@Hülya merhaba',photo:photos[1]),
              Ngelx590AudioComment(name:'Kandemir',message:'odaya katıldı',photo:photos[2]),
              Ngelx590AudioComment(name:'Muazzez',message:'Çok güzel bir sohbet',photo:photos[3]),
            ])),Ngelx590Composer(controller:input,onSend:()=>send++,actions:[
              Ngelx590RoundAction(label:'Mikrofon',icon:Icons.mic,onTap:()=>menu++),
              Ngelx590RoundAction(label:'Tepki',icon:Icons.favorite,color:Colors.pink,onTap:()=>menu++),
              Ngelx590RoundAction(label:'Davet',icon:Icons.reply,onTap:()=>menu++),
              Ngelx590RoundAction(label:'Seçenekler',icon:Icons.more_horiz,onTap:()=>menu++),
            ])]),
          )))));
      await tester.pump(const Duration(milliseconds:250));
      expect(tester.takeException(),isNull);expect(find.byType(Ngelx590AudioSeat),findsNWidgets(9));
      final grid=tester.getRect(find.byKey(const ValueKey('audio590-grid')));
      final composer=tester.getRect(find.byType(Ngelx590Composer));
      expect(grid.bottom,lessThan(composer.top));
      // Every row must be visible without scrolling the old card/list page.
      for(final e in find.byType(Ngelx590AudioSeat).evaluate()) {
        final box=e.renderObject! as RenderBox;final top=box.localToGlobal(Offset.zero).dy;
        expect(top+box.size.height,lessThanOrEqualTo(grid.bottom+.5));
      }
      await tester.tap(find.byTooltip('Odadan ayrıl'));expect(close,1);
      await tester.tap(find.text('+ Takip et'));expect(follow,1);
      await tester.tap(find.byType(Ngelx590AudioSeat).last);expect(request,1);
      await tester.tap(find.byTooltip('Seçenekler'));expect(menu,1);
      await tester.enterText(find.byType(TextField),'Merhaba');
      await tester.testTextInput.receiveAction(TextInputAction.send);expect(send,1);
      await tester.tap(find.byTooltip('Mesajı gönder'));expect(send,2);
      FocusManager.instance.primaryFocus?.unfocus();await tester.pump();
      final boundary=tester.renderObject<RenderRepaintBoundary>(find.byKey(const ValueKey('capture590')));
      await tester.runAsync(()async{
        final image=await boundary.toImage(pixelRatio:1);
        try{final data=await image.toByteData(format:ui.ImageByteFormat.png);
          final file=File('test/screenshots/build590_${size.width.toInt()}_${solo?'solo':'full'}_${scale}.png');
          file.parent.createSync(recursive:true);file.writeAsBytesSync(data!.buffer.asUint8List());
        }finally{image.dispose();}
      });
      await tester.pumpWidget(const SizedBox());
    });
  }
}
