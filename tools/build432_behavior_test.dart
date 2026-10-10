import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:ngelx_app/main.dart';

void main(){
  testWidgets('late keyed pane receives cached snapshot without another backend event',(tester)async{
    var subscriptions=0;
    final source=StreamController<int>.broadcast(onListen:(){subscriptions++;});
    final cache=NgelxSnapshotCache<int>(()=>source.stream);
    Widget pane(String key)=>MaterialApp(home:StreamBuilder<int>(key:ValueKey(key),stream:cache.stream,builder:(_,s)=>Text(s.hasData?'count:${s.data}':'loading')));
    await tester.pumpWidget(pane('counter'));source.add(7);await tester.pump();await tester.pump();
    expect(find.text('count:7'),findsOneWidget);
    await tester.pumpWidget(pane('notifications'));await tester.pump();
    expect(find.text('count:7'),findsOneWidget);expect(subscriptions,1);
    cache.dispose();await tester.pumpWidget(const SizedBox());await source.close();
  });
  testWidgets('request card late subscriber and initial timeout recover',(tester)async{
    final source=StreamController<int>.broadcast();
    final cache=NgelxSnapshotCache<int>(()=>source.stream,deadline:const Duration(seconds:2));
    final events=<int>[],errors=<Object>[];
    final first=cache.stream.listen(events.add,onError:errors.add);
    await tester.pump(const Duration(seconds:3));expect(errors.single,isA<TimeoutException>());
    source.add(0);await tester.pump();expect(events,[0]);
    final late=<int>[];final second=cache.stream.listen(late.add,onError:errors.add);
    await tester.pump();expect(late,[0]);expect(errors.length,1);
    cache.dispose();unawaited(first.cancel());unawaited(second.cancel());unawaited(source.close());await tester.pump();
  });
  testWidgets('upstream error replays and explicit retry reconnects',(tester)async{
    final sources=<StreamController<int>>[];
    final cache=NgelxSnapshotCache<int>(() {final c=StreamController<int>();sources.add(c);return c.stream;});
    final errors=<Object>[],values=<int>[];
    final first=cache.stream.listen(values.add,onError:errors.add);
    sources.first.addError(StateError('offline'));await tester.pump();
    final second=cache.stream.listen(values.add,onError:errors.add);await tester.pump();expect(errors.length,2);
    cache.retry();expect(sources.length,2);sources.last.add(2);await tester.pump();expect(values,[2,2]);
    cache.dispose();unawaited(first.cancel());unawaited(second.cancel());for(final c in sources){unawaited(c.close());}await tester.pump();
  });
  testWidgets('dispose cancels upstream and closes all panes',(tester)async{
    var canceled=0,closed=0;
    final source=StreamController<int>.broadcast(onCancel:(){canceled++;});
    final cache=NgelxSnapshotCache<int>(()=>source.stream);
    cache.stream.listen((_){},onDone:(){closed++;});cache.stream.listen((_){},onDone:(){closed++;});
    cache.dispose();await tester.pump();expect(canceled,1);expect(closed,2);
    var after=false;cache.stream.listen((_){},onDone:(){after=true;});await tester.pump();expect(after,true);
    unawaited(source.close());await tester.pump();
  });
  test('archive excludes other owner, hidden, deleted and unsaved expired story',(){
    final saved=<String,dynamic>{'ownerId':'me','type':'story','archivedAt':Timestamp.now()};
    expect(ngelx432ArsivGorunur('a',saved,'me'),true);
    expect(ngelx432ArsivGorunur('a',saved,'other'),false);
    expect(ngelx432ArsivGorunur('a',{...saved,'hiddenFor':['me']},'me'),false);
    expect(ngelx432ArsivGorunur('a',{...saved,'deleted':true},'me'),false);
    expect(ngelx432ArsivGorunur('a',{'ownerId':'me','type':'story','expiresAt':Timestamp.fromMillisecondsSinceEpoch(1)},'me'),false);
  });
  test('local deletion hides stale query rows before Firestore updates',(){
    final saved=<String,dynamic>{'ownerId':'me','type':'story','highlighted':true};
    expect(ngelx432ArsivGorunur('stale',saved,'me'),true);
    ngelxIcerikSilindi('stale');
    expect(ngelx432ArsivGorunur('stale',saved,'me'),false);
    expect(ngelx432IcerikGorunur('stale',{'type':'video'},'me'),false);
    ngelxSilinenIcerikIdleri.remove('stale');
  });
}
