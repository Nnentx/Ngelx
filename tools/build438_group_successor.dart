// Member arrays preserve insertion order: the first remaining member is the
// oldest recorded member when an explicit joining timestamp is unavailable.
String? ngelx438Successor(List<String> members,List<String> admins,String leaving){
  final remaining=members.where((id)=>id!=leaving&&id.isNotEmpty).toList();
  for(final id in remaining){if(admins.contains(id))return id;}
  return remaining.isEmpty?null:remaining.first;
}
