import 'dart:math' as math;

String? ngelx548PeerUid(Iterable<String> members,String me){
  final others=members.where((id)=>id.isNotEmpty&&id!=me).toSet();
  return others.length==1?others.single:null;
}
({double width,double height}) ngelx548PhotoSize(double iw,double ih,double sw,double sh){
  final mw=math.min(260.0,sw*.68),mh=math.min(330.0,sh*.40);
  if(iw<=0||ih<=0)return (width:mw,height:math.min(mw,mh));
  final scale=math.min(mw/iw,mh/ih);
  return (width:iw*scale,height:ih*scale);
}
bool ngelx548UseGrid(int guests)=>guests>=4;
int ngelx548GridColumns(int count)=>count>=6?3:2;
const ngelx548GiftCatalog=<String,int>{'Gül':1,'Kalp':3,'Yıldız':5,
  'Elmas':15,'Kalp Taşı':15,'Ayıcık':25,'Taç':25,'NgelX Roket':50,'Galaksi':100};
bool ngelx548ValidGift(String name,int points,int quantity)=>
  quantity>=1&&quantity<=10&&ngelx548GiftCatalog[name]==points;
