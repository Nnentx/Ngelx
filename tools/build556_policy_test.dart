import '../app/lib/build556_policy.dart';
void check(bool condition,String reason){if(!condition)throw StateError(reason);}
void main(){
  check(ngelx556Search('AYAZ ATABEY').contains(ngelx556Search('Ayaz')),'Name mentions match display names');
  check(ngelx556Search('IŞIK ÇAĞRI').contains(ngelx556Search('ışık')),'Turkish casing works');
  final story=<String,dynamic>{'type':'story','highlighted':true,'privacy':'Herkes'};
  final profile=<String,dynamic>{'friends':['friend']};
  check(ngelx556HighlightVisible(story,'owner',profile,{},'visitor'),'Public highlight visible to visitors after expiry');
  check(!ngelx556HighlightVisible({...story,'privacy':'Yalnızca ben'},'owner',profile,{},'visitor'),'Owner-only highlights stay private');
  check(!ngelx556HighlightVisible({...story,'privacy':'Arkadaşlar'},'owner',profile,{},'visitor'),'Stranger cannot see friends-only highlight');
  check(ngelx556HighlightVisible({...story,'privacy':'Arkadaşlar'},'owner',profile,{},'friend'),'Friend sees allowed highlight');
  check(!ngelx556HighlightVisible({...story,'privacy':'Yakın arkadaşlar'},'owner',profile,{},'friend'),'Friendship does not grant close-friend access');
  check(ngelx556HighlightVisible({...story,'privacy':'Yakın arkadaşlar','visibleTo':['friend']},'owner',profile,{},'friend'),'Explicit close-friend audience respected');
  check(!ngelx556HighlightVisible({...story,'hiddenFor':['visitor']},'owner',profile,{},'visitor'),'Hidden audience excluded');
  check(!ngelx556HighlightVisible({...story,'highlighted':false},'owner',profile,{},'visitor'),'Removed highlight disappears');
  check(!ngelx556HighlightVisible({...story,'deleted':true},'owner',profile,{},'visitor'),'Deleted highlight disappears');
  check(!ngelx556HighlightVisible({...story,'type':'video'},'owner',profile,{},'visitor'),'Ordinary video is not a story highlight');
  print('Build556: 12 mention and highlight privacy checks passed');
}
