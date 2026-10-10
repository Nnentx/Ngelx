// One upstream subscription; every newly opened pane receives the last event.
class NgelxSnapshotCache<T> {
  final Stream<T> Function() source;
  final Duration deadline;
  NgelxSnapshotCache(this.source,{this.deadline=const Duration(seconds:15)});
  final Set<MultiStreamController<T>> _listeners={};
  StreamSubscription<T>? _subscription;
  Timer? _timer;
  T? _value;
  bool _hasValue=false,_disposed=false;
  Object? _error;
  StackTrace? _trace;
  int _generation=0;
  late final Stream<T> stream=Stream<T>.multi((listener){
    if(_disposed){listener.close();return;}
    _listeners.add(listener);
    if(_hasValue)listener.add(_value as T);
    if(_error!=null)listener.addError(_error!,_trace);
    listener.onCancel=()=>_listeners.remove(listener);
    _start();
  },isBroadcast:true);
  void _start(){
    if(_disposed||_subscription!=null)return;
    final generation=_generation;
    _timer=Timer(deadline,(){
      if(!_disposed&&generation==_generation&&!_hasValue){
        _sendError(TimeoutException('Veri yüklenemedi. Tekrar dene.',deadline),StackTrace.current);
      }
    });
    _subscription=source().listen((value){
      if(_disposed||generation!=_generation)return;
      _timer?.cancel();_value=value;_hasValue=true;_error=null;_trace=null;
      for(final listener in _listeners.toList()){listener.add(value);}
    },onError:(Object error,StackTrace trace){
      if(_disposed||generation!=_generation)return;
      _timer?.cancel();_sendError(error,trace);
    },onDone:(){
      if(_disposed||generation!=_generation)return;
      _timer?.cancel();
      if(!_hasValue&&_error==null)_sendError(StateError('Veri akışı sonuç vermedi.'),StackTrace.current);
    });
  }
  void _sendError(Object error,StackTrace trace){
    _error=error;_trace=trace;
    for(final listener in _listeners.toList()){listener.addError(error,trace);}
  }
  void retry(){
    if(_disposed)return;
    _generation++;_timer?.cancel();
    final old=_subscription;_subscription=null;
    if(old!=null)unawaited(old.cancel());
    _error=null;_trace=null;
    _start();
  }
  void dispose(){
    if(_disposed)return;
    _disposed=true;_generation++;_timer?.cancel();
    final old=_subscription;_subscription=null;
    if(old!=null)unawaited(old.cancel());
    for(final listener in _listeners.toList()){listener.close();}
    _listeners.clear();_value=null;_error=null;
  }
}

bool ngelx432IcerikGorunur(String id,Map<String,dynamic> v,String uid){
  if(ngelxSilinenIcerikIdleri.contains(id)||v['deleted']==true||v['isDeleted']==true||v['removed']==true)return false;
  final hidden=v['hiddenFor'];
  return hidden is! Iterable||!hidden.map((e)=>e.toString()).contains(uid);
}
bool ngelx432ArsivGorunur(String id,Map<String,dynamic> v,String uid){
  return v['ownerId']==uid&&v['type']=='story'&&ngelx432IcerikGorunur(id,v,uid)&&
    (v['archivedAt'] is Timestamp||v['highlighted']==true);
}
Widget ngelx432YuklemeHatasi(VoidCallback retry,String message)=>Center(child:Padding(
  padding:const EdgeInsets.all(24),child:Column(mainAxisSize:MainAxisSize.min,children:[
    const Icon(Icons.cloud_off_rounded,color:mor,size:38),const SizedBox(height:12),
    Text(message,textAlign:TextAlign.center),const SizedBox(height:8),
    TextButton.icon(onPressed:retry,icon:const Icon(Icons.refresh),label:const Text('Tekrar dene')),
  ])));
