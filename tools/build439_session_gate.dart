import 'dart:async';
import 'package:flutter/widgets.dart';

/// Read the current session on each event, including root-route recreation.
/// Event payloads may describe a session superseded by a newer operation.
class NgelXSessionGate<T> extends StatefulWidget {
  final Stream<T?> changes;
  final T? Function() current;
  final Widget Function(BuildContext, T?) builder;
  const NgelXSessionGate({super.key, required this.changes,
    required this.current, required this.builder});
  @override State<NgelXSessionGate<T>> createState()=>_NgelXSessionGateState<T>();
}
class _NgelXSessionGateState<T> extends State<NgelXSessionGate<T>> {
  StreamSubscription<T?>? _subscription;
  void _listen(){
    _subscription=widget.changes.listen((_) {if(mounted)setState((){});},
      onError:(Object _,StackTrace __){if(mounted)setState((){});});
  }
  @override void initState(){super.initState();_listen();}
  @override void didUpdateWidget(covariant NgelXSessionGate<T> old){
    super.didUpdateWidget(old);
    if(!identical(old.changes,widget.changes)){
      unawaited(_subscription?.cancel());_listen();
    }
  }
  @override void dispose(){unawaited(_subscription?.cancel());super.dispose();}
  @override Widget build(BuildContext context)=>widget.builder(context,widget.current());
}
