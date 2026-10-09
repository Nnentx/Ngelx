#!/usr/bin/env python3
"""Build422: private follow request Reply -> accept/reject in visitor profile."""
from pathlib import Path
p=Path('app/lib/main.dart')
s=p.read_text(encoding='utf-8')
a=s.index('class _KullaniciProfilPageState extends State<KullaniciProfilPage>')
b=s.index('\nclass NgelXVideoKapakOnizleme',a)
v=s[a:b]
anchor="final etiket=takipte?'Takip ediyorsun':(bekliyor?'Takip isteği bekliyor':(gizli?'Takip isteği gönder':t('follow')));"
if v.count(anchor)!=1:raise SystemExit('Build422 follow label drift')
start=v.index('return OutlinedButton.icon(',v.index(anchor))
end=v.index('\n                        },',start)
old=v[start:end]
for key in ["onPressed:()async{", "if(me==null)return;", "Text(etiket,maxLines:1)"]:
    if key not in old:raise SystemExit('Build422 follow action missing '+key)
old=old.replace("if(me==null)return;",
"""if(me==null)return;
                              if(gelenTakipBekliyor&&!takipte){
                                final secim=await showModalBottomSheet<bool>(
                                  context:context,backgroundColor:Colors.white,
                                  showDragHandle:true,builder:(c)=>SafeArea(
                                    child:Column(mainAxisSize:MainAxisSize.min,children:[
                                      const ListTile(title:Text('Takip isteğini yanıtla',
                                        style:TextStyle(fontWeight:FontWeight.w900))),
                                      ListTile(leading:const Icon(Icons.check_circle,color:mor),
                                        title:const Text('Kabul et'),
                                        onTap:()=>Navigator.pop(c,true)),
                                      ListTile(leading:const Icon(Icons.close_rounded),
                                        title:const Text('Reddet'),
                                        onTap:()=>Navigator.pop(c,false)),
                                    ])));
                                if(secim!=null){
                                  try{
                                    await ngelxGelenSosyalIstekCevapla(
                                      gonderenUid:uid,tur:'follow_request',kabul:secim);
                                    if(context.mounted)ScaffoldMessenger.of(context)
                                      .showSnackBar(SnackBar(content:Text(
                                        secim?'Takip isteği kabul edildi.':'Takip isteği reddedildi.')));
                                  }catch(e){
                                    if(context.mounted)ScaffoldMessenger.of(context)
                                      .showSnackBar(SnackBar(content:Text(
                                        e is StateError?e.message.toString():'Takip isteği işlenemedi.')));
                                  }
                                }
                                return;
                              }""",1)
old=old.replace('Text(etiket,maxLines:1)',"Text(gelenTakipBekliyor&&!takipte?'Yanıtla':etiket,maxLines:1)",1)
old=old.replace("takipte?Icons.person_remove_outlined:(bekliyor?Icons.schedule_rounded:Icons.person_add_alt_1)",
                "takipte?Icons.person_remove_outlined:(gelenTakipBekliyor?Icons.mark_email_unread_rounded:(bekliyor?Icons.schedule_rounded:Icons.person_add_alt_1))",1)
wrapped="""return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
                            stream:me==null?null:sosyalIstekRef(uid,me,'follow_request').snapshots(),
                            builder:(_,gelenSnap){
                              if(me!=null&&!gelenSnap.hasData){
                                return const SizedBox(height:48,child:Center(
                                  child:CircularProgressIndicator(strokeWidth:2,color:mor)));
                              }
                              final gelenTakipBekliyor=gelenSnap.data?.data()?['status']=='pending';
                              """+old+"""
                            },
                          );"""
v=v[:start]+wrapped+v[end:]
s=s[:a]+v+s[b:]
p.write_text(s,encoding='utf-8')
print('Build422: incoming private follow request Reply -> Accept/Reject on profile.')
