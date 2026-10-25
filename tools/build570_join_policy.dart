class Ngelx570JoinPolicy {
 Set<String>? _last;
 bool update(Iterable<String> identities,{required bool connected}) {
  final current=identities.toSet();
  if(!connected){_last=null;return false;}
  final previous=_last;_last=current;
  return previous!=null&&current.difference(previous).isNotEmpty;
 }
}
