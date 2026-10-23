String ngelx556Search(String value)=>value.toLowerCase().replaceAll('ı','i').replaceAll('İ','i').replaceAll('ş','s').replaceAll('ğ','g').replaceAll('ü','u').replaceAll('ö','o').replaceAll('ç','c');
bool ngelx556HighlightVisible(Map<String,dynamic> story,String owner,Map<String,dynamic> profile,Map<String,dynamic> viewer,String? uid){
  if(story['type']!='story'||story['highlighted']!=true||story['deleted']==true)return false;
  if(uid==owner)return true;
  if(uid!=null&&List<String>.from(story['hiddenFor']??const[]).contains(uid))return false;
  final friends=uid!=null&&(List<String>.from(profile['friends']??const[]).contains(uid)||List<String>.from(viewer['friends']??const[]).contains(owner));
  final privacy=(story['privacy']??'Herkes').toString();
  if(privacy=='Yalnızca ben')return false;
  if(privacy=='Arkadaşlar')return friends;
  if(privacy=='Yakın arkadaşlar')return uid!=null&&List<String>.from(story['visibleTo']??const[]).contains(uid);
  return true;
}
