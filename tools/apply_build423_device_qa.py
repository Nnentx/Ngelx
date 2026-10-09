#!/usr/bin/env python3
"""Build 423: device QA fixes applied AFTER the Build 422 generated UI."""
from pathlib import Path

p=Path('app/lib/main.dart')
s=p.read_text(encoding='utf-8')
a=s.index('class _MesajPageState extends State<MesajPage>')
b=s.index('\nclass ArsivSohbetlerPage',a)
inbox=s[a:b]

def once(old,new,label):
    global inbox
    n=inbox.count(old)
    if n!=1:
        raise SystemExit('Build423 '+label+' source drift: '+str(n))
    inbox=inbox.replace(old,new,1)

# The requests list must reset scroll offset when switching from another tab.
rs=inbox.index('    Widget isteklerIcerigi(){')
re=inbox.index('    Widget sohbetlerIcerigi(){',rs)
requests=inbox[rs:re]
anchor="          final sosyal=(snap.data?.docs??"
start=requests.index(anchor)
end=requests.index('          return ListView(',start)
original=requests[start:end]
if original.count('}).toList();')!=1:
    raise SystemExit('Build423 request filter changed')
unique=original.replace('final sosyal=','final hamSosyal=',1)+"""          // Legacy notifications can contain repeated pending requests.
          // One sender and type must appear once, newest notification first.
          hamSosyal.sort((a,b){
            final at=a.data()['createdAt'],bt=b.data()['createdAt'];
            final ai=at is Timestamp?at.millisecondsSinceEpoch:0;
            final bi=bt is Timestamp?bt.millisecondsSinceEpoch:0;
            return bi.compareTo(ai);
          });
          final gorulen=<String>{};
          final sosyal=hamSosyal.where((d){
            final v=d.data();
            final from=(v['fromUid']??'').toString();
            final tur=(v['type']??'').toString();
            return from.isNotEmpty && gorulen.add(from+'|'+tur);
          }).toList();
"""
requests=requests[:start]+unique+requests[end:]
if requests.count('          return ListView(')!=1:
    raise SystemExit('Build423 request ListView changed')
requests=requests.replace('          return ListView(','          return ListView(\n            key:ValueKey("ngelx-requests-"+filtre),',1)
requests=requests.replace('padding:EdgeInsets.fromLTRB(14,10,14,ngelxAltGuvenliBosluk','padding:EdgeInsets.fromLTRB(14,0,14,ngelxAltGuvenliBosluk',1)
inbox=inbox[:rs]+requests+inbox[re:]

once("Text(ad,maxLines:1,overflow:TextOverflow.ellipsis,\n                                  style:const TextStyle(fontSize:15,fontWeight:FontWeight.w900))",
     "Text(ad,maxLines:1,overflow:TextOverflow.ellipsis,\n                                  style:const TextStyle(color:Color(0xFF142138),fontSize:15,fontWeight:FontWeight.w900))",
     'sender name legibility')
groupOriginal="subtitle:Text((v['lastMessage']??t('groupCreated')).toString(),maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Color(0xFF7C86A0),fontSize:13)),"
groupNew="""subtitle:Column(mainAxisSize:MainAxisSize.min,crossAxisAlignment:CrossAxisAlignment.start,children:[
                      const Text('Grup',style:TextStyle(color:Color(0xFF138A55),fontSize:10.5,fontWeight:FontWeight.w800)),
                      Text((v['lastMessage']??t('groupCreated')).toString(),maxLines:1,
                        overflow:TextOverflow.ellipsis,style:const TextStyle(color:Color(0xFF7C86A0),fontSize:13)),
                    ]),"""
if inbox.count(groupOriginal)!=2:
    raise SystemExit('Build423 group subtitle drift: '+str(inbox.count(groupOriginal)))
inbox=inbox.replace(groupOriginal,groupNew)

# Notifications emphasize the sender, live broadcast (red), and voice room
# (purple) without recoloring unrelated content or showing double sender names.
helper="""    Widget ngelxRenkliBildirim(Map<String,dynamic> v,String metin,bool okundu){
      final ad=(v['senderName']??v['fromName']??'').toString().trim();
      var kalan=metin;
      final spans=<TextSpan>[];
      if(ad.isNotEmpty && metin.toLowerCase().startsWith(ad.toLowerCase())){
        kalan=metin.substring(ad.length).trimLeft();
        spans.add(TextSpan(text:ad+' ',style:const TextStyle(
          color:Color(0xFF8950DF),fontWeight:FontWeight.w900)));
      }
      final r=RegExp(r'canlı yayın|sesli oda',caseSensitive:false);
      var bas=0;
      final normal=TextStyle(color:const Color(0xFF111827),fontSize:13.5,
        fontWeight:okundu?FontWeight.w600:FontWeight.w800);
      for(final match in r.allMatches(kalan)){
        if(match.start>bas)spans.add(TextSpan(text:kalan.substring(bas,match.start),style:normal));
        final canlı=match.group(0)!.toLowerCase().contains('canlı');
        spans.add(TextSpan(text:kalan.substring(match.start,match.end),
          style:TextStyle(color:canlı?const Color(0xFFDA233B):const Color(0xFF844AED),
            fontSize:13.5,fontWeight:FontWeight.w900)));
        bas=match.end;
      }
      if(bas<kalan.length)spans.add(TextSpan(text:kalan.substring(bas),style:normal));
      return Text.rich(TextSpan(children:spans),maxLines:2,overflow:TextOverflow.ellipsis);
    }

"""
once('    Widget sekme(String ad){',helper+'    Widget sekme(String ad){','notification color helper')
once("title:Text(metin,maxLines:2,overflow:TextOverflow.ellipsis,style:TextStyle(color:const Color(0xFF111827),fontSize:13.5,fontWeight:okundu?FontWeight.w600:FontWeight.w900)),",
     "title:ngelxRenkliBildirim(v,metin,okundu),",
     'notification title')

s=s[:a]+inbox+s[b:]
p.write_text(s,encoding='utf-8')

# New visible Build 423 version: the Build 422 release remains untouched.
p=Path('app/lib/main.dart');s=p.read_text(encoding='utf-8')
for old,new in [("defaultValue: '422'","defaultValue: '423'"),
                ("defaultValue: '1.0.197'","defaultValue: '1.0.198'")]:
    if s.count(old)!=1:raise SystemExit('Build423 version drift: '+old)
    s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
p=Path('app/pubspec.yaml');s=p.read_text(encoding='utf-8')
if s.count('version: 1.0.197+422')!=1:
    raise SystemExit('Build423 pubspec version drift')
p.write_text(s.replace('version: 1.0.197+422','version: 1.0.198+423',1),encoding='utf-8')
print('Build423: unique request rows, tab scroll reset, visible names, group label, notification accents, version 423.')
