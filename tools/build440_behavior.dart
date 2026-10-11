import 'dart:async';
import 'package:flutter/widgets.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

DateTime? ngelx440StoryExpiry(Map<String,dynamic> data){
  final expiry=data['expiresAt'],created=data['createdAt']??data['clientCreatedAt'];
  if(expiry is Timestamp)return expiry.toDate();
  if(created is Timestamp)return created.toDate().add(const Duration(hours:24));
  return null;
}
bool ngelx440StoryActive(Map<String,dynamic> data,DateTime now){
  final expiry=ngelx440StoryExpiry(data);
  return data['type']=='story'&&expiry!=null&&expiry.isAfter(now);
}
int ngelx440PinCompare(String a,String b,Set<String> pins,Map<String,int> times,int aTime,int bTime){
  final ap=pins.contains(a),bp=pins.contains(b);
  if(ap!=bp)return ap?-1:1;
  if(ap){final result=(times[b]??0).compareTo(times[a]??0);if(result!=0)return result;}
  final result=bTime.compareTo(aTime);
  return result!=0?result:a.compareTo(b);
}
bool ngelx440CallJoinable(Map<String,dynamic> data,DateTime now){
  if(data['callEndedAt']!=null)return false;
  if(!const {'ringing','active'}.contains(data['callStatus']))return false;
  if((data['callRoomName']??'').toString().isEmpty)return false;
  final stamp=data['callHeartbeatAt']??data['callConnectedAt']??data['callCreatedAt'];
  if(stamp is! Timestamp)return false;
  final age=now.difference(stamp.toDate());
  return !age.isNegative&&age<Duration(minutes:data['callHeartbeatAt']!=null?3:2);
}

/// Rebuild at expiry even when Firestore has no new snapshot.
class NgelXStorySnapshotBuilder extends StatefulWidget{
  final Stream<QuerySnapshot<Map<String,dynamic>>>? stream;
  final AsyncWidgetBuilder<QuerySnapshot<Map<String,dynamic>>> builder;
  final DateTime Function()? now;
  const NgelXStorySnapshotBuilder({super.key,required this.stream,required this.builder,this.now});
  @override State<NgelXStorySnapshotBuilder> createState()=>_StorySnapshotState();
}
class _StorySnapshotState extends State<NgelXStorySnapshotBuilder> with WidgetsBindingObserver{
  Timer? _timer; DateTime? _next;
  @override void initState(){super.initState();WidgetsBinding.instance.addObserver(this);}
  @override void dispose(){_timer?.cancel();WidgetsBinding.instance.removeObserver(this);super.dispose();}
  @override void didChangeAppLifecycleState(AppLifecycleState state){if(state==AppLifecycleState.resumed&&mounted)setState((){});}
  void _schedule(QuerySnapshot<Map<String,dynamic>>? snapshot){
    final now=widget.now?.call()??DateTime.now();
    final times=(snapshot?.docs??[]).map((d)=>ngelx440StoryExpiry(d.data())).whereType<DateTime>().where((t)=>t.isAfter(now)).toList()..sort();
    final next=times.isEmpty?null:times.first;
    if(next==_next)return;
    _next=next;_timer?.cancel();
    if(next!=null)_timer=Timer(next.difference(now)+const Duration(milliseconds:10),(){_next=null;if(mounted)setState((){});});
  }
  @override Widget build(BuildContext context)=>StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(stream:widget.stream,builder:(context,snapshot){_schedule(snapshot.data);return widget.builder(context,snapshot);});
}
