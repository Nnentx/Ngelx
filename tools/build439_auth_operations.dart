import 'dart:async';

/// A timeout stops waiting, not the underlying Firebase operation. Keep its
/// future until completion so a late sign-in cannot overwrite a later sign-out.
class NgelXAuthOperations<T> {
  Future<T>? _login;
  Future<void>? _logout;
  Future<T> signIn(Future<T> Function() operation){
    if(_logout!=null)return Future<T>.error(StateError('Sign-out is in progress'));
    final running=_login;
    if(running!=null)return running;
    final future=Future<T>.sync(operation);
    _login=future;
    unawaited(future.then<void>((_){if(identical(_login,future))_login=null;},
      onError:(Object _,StackTrace __){if(identical(_login,future))_login=null;}));
    return future;
  }
  Future<void> signOut(Future<void> Function() operation){
    final running=_logout;
    if(running!=null)return running;
    final pending=_login;
    final future=Future<void>(()async{
      if(pending!=null){try{await pending;}catch(_){}}
      await operation();
    });
    _logout=future;
    unawaited(future.then<void>((_){if(identical(_logout,future))_logout=null;},
      onError:(Object _,StackTrace __){if(identical(_logout,future))_logout=null;}));
    return future;
  }
}
