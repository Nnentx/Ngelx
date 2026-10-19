#!/usr/bin/env python3
"""Apply after the complete Build539 generator; never change RTC or signing."""
from pathlib import Path

MARK = '// Build540: reference live bar and call presentation'

def once(s, old, new):
    if s.count(old) != 1:
        raise RuntimeError('Build540 requires exactly one known anchor: '+old[:100])
    return s.replace(old, new, 1)

def live_transform(s):
    if MARK in s:
        return s
    start = s.index("              Container(key:const ValueKey('live-controls-panel453')")
    end = s.index('\n            ]),\n          )),', start)
    dock = s[start:end].strip().rstrip(',')
    # Retain the working, role-specific controls as an explicit expandable tray.
    # The input is always last, immediately below the most recent comments.
    dock = once(dock, '                _yorumGirisAlani(),\n', '')
    dock = once(dock, '                  if(widget.yayinSahibi)_hostDockHandle490(),\n', '')
    dock = once(dock, 'child:(!widget.yayinSahibi||_hostDockOpen490)', 'child:true')
    methods = r'''
  // Build540: reference live bar and call presentation
  bool _toolsOpen540=false;
  Widget _liveBottom540()=>Column(mainAxisSize:MainAxisSize.min,children:[
    if(_toolsOpen540&&widget.yayinSahibi)_guestControl453(true),
    if(_toolsOpen540) __DOCK__,
    Ngelx540LiveBar(key:const ValueKey('live-bottom540'),
      composer:_yorumGirisAlani(),actions:[
        Ngelx448GuestControls(liveId:widget.belgeId,ownerUid:widget.ownerId,
          host:widget.yayinSahibi,compact:true,
          viewerUids:widget.yayinSahibi?_aktifIzleyiciler().map(_izleyiciUid).where((x)=>x.isNotEmpty).toList():const[]),
        Ngelx540LiveAction(label:'Gül',icon:const Text('🌹',style:TextStyle(fontSize:27)),
          onPressed:widget.yayinSahibi?_giftHistory512:hediyeGonderiliyor?null:_hediyePaneli),
        Ngelx540LiveAction(label:'Hediye',icon:const Text('🎁',style:TextStyle(fontSize:27)),
          onPressed:widget.yayinSahibi?_giftHistory512:hediyeGonderiliyor?null:_hediyePaneli),
        Ngelx540LiveAction(label:'Daha fazla',icon:Icon(_toolsOpen540?Icons.expand_more:Icons.more_horiz,color:Colors.white),
          onPressed:()=>setState(()=>_toolsOpen540=!_toolsOpen540)),
      ]),
  ]);

'''.replace('__DOCK__', dock)
    s = s[:start]+'              _liveBottom540(),'+s[end:]
    # Host guest controls remain in the tray; viewers retain their own request
    # sheet and can never access the host's guest list through this change.
    s = once(s, '              if(widget.yayinSahibi&&MediaQuery.of(context).viewInsets.bottom==0)Align(alignment:Alignment.centerRight,child:_guestControl453(true)),\n', '')
    s = once(s, '  Widget _guestControl453(bool host)', methods+'  Widget _guestControl453(bool host)')
    # Three/four compact rows, without a 224px history block and footer gap.
    s = once(s, 'maxHeight:keyboard?82:224', 'maxHeight:keyboard?76:154')
    a=s.index('  Widget _commentSection490(){'); b=s.index('  Widget _hostDockHandle490()',a)
    section=s[a:b]
    history_start=section.index('        if(!_commentsHidden490)Align(')
    section=section[:history_start]+section[section.index('\n      ]),',history_start):]
    # History is beside the hide toggle, above the message list.
    section=once(section, "        Semantics(button:true,label:_commentsHidden490?", "        Row(children:[Expanded(child:Semantics(button:true,label:_commentsHidden490?")
    section=once(section, '        )),\n        // Offstage', "        ))),IconButton(tooltip:'Eski yorumlar',onPressed:_commentHistory514,\n          color:Colors.white,icon:const Icon(Icons.history_rounded,size:18))]),\n        // Offstage")
    s=s[:a]+section+s[b:]
    s=once(s, '(widget.yayinSahibi?220:172)', '80')
    s=once(s, 'widget.yayinSahibi?270.0:225.0', '190.0')
    # Match the reference's single profile header and compact comment lines.
    a=s.index('              Row(children: [',s.index('  @override\n  Widget build(BuildContext context) {',s.index('  Widget _guestControl453')))
    b=s.index('              const SizedBox(height:8),\n              NgelXCanliPkKatmani',a)
    header=s[a:b]
    view_start=header.index('                InkWell(\n                  onTap:_izleyiciListesiniAc,')
    view_end=header.index('                StreamBuilder<',view_start)
    viewers=header[view_start:view_end]
    new_header="""              Row(children:[Expanded(child:_yayinBasligi()),
                const SizedBox(width:4),
"""+viewers+"""                SizedBox(width:36,child:IconButton(tooltip:'Kapat / Çık',
                  onPressed:()async{if(await _geri()&&mounted)Navigator.pop(context);},
                  padding:EdgeInsets.zero,icon:const Icon(Icons.close_rounded,color:Colors.white))),
              ]),
              const SizedBox(height:5),
              Row(children:[
                const Text('● CANLI',style:TextStyle(color:Color(0xFFFF2851),fontWeight:FontWeight.w800,fontSize:11)),
                const SizedBox(width:8),_baglantiRozeti(),const Spacer(),
                IconButton(tooltip:'Hediye geçmişi',onPressed:_giftHistory512,
                  visualDensity:VisualDensity.compact,icon:const Icon(Icons.card_giftcard_rounded,color:Colors.white,size:19)),
              ]),
"""
    s=s[:a]+new_header+s[b:]
    s=once(s,"              Text('@$username',maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white70,fontSize:12,fontWeight:FontWeight.w600)),\n",'')
    s=once(s,'            if(widget.yayinSahibi)_baglantiRozeti(),\n','')
    s=once(s,'foregroundColor:const Color(0xFF20C5CA),side:const BorderSide(color:Color(0xFF20C5CA)),backgroundColor:Colors.transparent',
      'foregroundColor:Colors.white,backgroundColor:const Color(0xFFFF0060)')
    # Comments retain real profiles, names, moderation and pagination.
    s=once(s,'CircleAvatar(radius:17,backgroundImage:photo.isEmpty?null:NgelXAgImageProvider(photo)',
      'CircleAvatar(radius:13,backgroundImage:photo.isEmpty?null:NgelXAgImageProvider(photo)')
    s=once(s,'padding:const EdgeInsets.symmetric(horizontal:9,vertical:7)',
      'padding:const EdgeInsets.symmetric(horizontal:7,vertical:3)')
    s=once(s,'maxHeight:keyboard?76:154','maxHeight:keyboard?76:148')
    return s

def main_transform(s):
    if MARK in s:
        return s
    s=once(s, "import 'package:flutter/foundation.dart';", "import 'package:flutter/foundation.dart';\nimport 'build540_reference_ui.dart';")
    a=s.index('class _NgelXAramaPageState');b=s.index('class GrupBilgiPage',a)
    body=s[a:b]
    old='  bool _videoCallControlsVisible493=true;'
    new=r'''  // Build540: reference live bar and call presentation
  Timer? _controlsTimer540;
  void _scheduleControls540(){
    _controlsTimer540?.cancel();
    if(!widget.goruntulu||!mounted||kucultuluyor||bitiyor||
        bitisDurumu!=null||hata!=null||MediaQuery.accessibleNavigationOf(context))return;
    _controlsTimer540=Timer(const Duration(seconds:5),(){
      if(!mounted||bitiyor||kucultuluyor||bitisDurumu!=null||hata!=null)return;
      if(baglaniyor||yenidenBaglaniyor){_scheduleControls540();return;}
      setState(()=>_videoCallControlsVisible493=false);
    });
  }
  bool _videoCallControlsVisible493=true;'''
    body=once(body,old,new)
    body=once(body, '      setState(()=>_videoCallControlsVisible493=!_videoCallControlsVisible493);', '      setState(()=>_videoCallControlsVisible493=!_videoCallControlsVisible493);\n      if(_videoCallControlsVisible493){_scheduleControls540();}else{_controlsTimer540?.cancel();}')
    body=once(body,'    super.initState();', '    super.initState();\n    WidgetsBinding.instance.addPostFrameCallback((_){if(mounted)_scheduleControls540();});')
    body=once(body, '  @override void dispose(){', '  @override void dispose(){\n    _controlsTimer540?.cancel();')
    # Every touch grants another five seconds, including menu/control use.
    # Wrap the whole page to observe touches without stealing gesture targets.
    body=once(body, '@override Widget build(BuildContext context)=>PopScope(', '@override Widget build(BuildContext context)=>Listener(\n    onPointerDown:(_){if(_videoCallControlsVisible493)_scheduleControls540();},\n    child:PopScope(')
    tail='    )),\n  );\n\n  Widget ngelxCallMiniButton'
    body=once(body,tail,'    )),\n  ));\n\n  Widget ngelxCallMiniButton')
    return s[:a]+body+s[b:]

def model_transform(s):
    if MARK in s:return s
    a=s.index('class _Ngelx445CallOverlayState');b=s.index('class Ngelx445InboxCallBanner',a)
    body=s[a:b]
    left=body.index('    Offset bounded(Offset p)=>Offset(')
    right=body.index('    final initial=',left)
    body=body[:left]+'''    // Build540: reference live bar and call presentation
    final keyboard=MediaQuery.viewInsetsOf(context).bottom;
    Offset bounded(Offset p)=>ngelx540BoundMini(p,screen,padding,keyboard,width);
'''+body[right:]
    old='      onPanEnd:(end){if(_dragDown448>90||end.velocity.pixelsPerSecond.dy>700)ngelx448HideCallCard(name);},'
    new='''      onPanEnd:(end){
        if(_dragDown448>90||end.velocity.pixelsPerSecond.dy>700){
          ngelx448HideCallCard(name);
        }else{
          _position446.value=ngelx540SnapMini(_position446.value??initial,
            screen,padding,keyboard,width);
        }
      },'''
    body=once(body,old,new)
    return s[:a]+body+s[b:]

def guest_transform(s):
    if MARK in s:return s
    s=once(s, 'final String liveId,ownerUid;final bool host;',
      'final String liveId,ownerUid;final bool host,compact;')
    s=once(s,'required this.host,this.viewerUids=const[]',
      'required this.host,this.compact=false,this.viewerUids=const[]')
    s=once(s,'    if(host)return FilledButton.icon(',
      "    "+MARK+"\n    if(host&&compact)return Ngelx540LiveAction(label:'+Konuk',icon:const Icon(Icons.group_add_outlined,color:Color(0xFFEC8AFF),size:29),onPressed:()=>_panel(context));\n    if(host)return FilledButton.icon(")
    s=once(s,"      if(status=='invited')return IconButton.filledTonal(",
      "      if(compact)return Ngelx540LiveAction(label:status=='pending'?'Bekliyor':status=='accepted'?'Ayrıl':'+Konuk',icon:Icon(status=='invited'?Icons.mark_email_unread_rounded:Icons.group_add_outlined,color:const Color(0xFFEC8AFF),size:29),onPressed:()=>_viewerJoinPanel497(context,uid,status is String?status:null));\n      if(status=='invited')return IconButton.filledTonal(")
    return s

def composer_transform(s):
    if MARK in s:return s
    s=once(s,'class _Ngelx453LiveComposerState extends State<Ngelx453LiveComposer>{',
      MARK+'\nclass _Ngelx453LiveComposerState extends State<Ngelx453LiveComposer>{')
    s=once(s,'style:const TextStyle(color:Colors.black87,fontSize:15)',
      'style:const TextStyle(color:Colors.white,fontSize:13)')
    s=once(s,'fillColor:const Color(0xFFF0F2F5)',
      'hintStyle:const TextStyle(color:Colors.white60),fillColor:const Color(0xB32B2B30)')
    s=once(s,'horizontal:16,vertical:13','horizontal:12,vertical:10')
    a=s.index("suffixIcon:IconButton(tooltip:'Emoji'")
    b=s.index(']);',a)
    s=s[:a]+"""suffixIcon:ValueListenableBuilder<TextEditingValue>(
        valueListenable:widget.controller,builder:(_,value,__){
          final sending=value.text.trim().isNotEmpty;
          return IconButton(tooltip:sending?'Yorumu gönder':'Emoji',
            onPressed:enabled&&!_sending?(sending?_send:_emoji):null,
            icon:_sending?const SizedBox(width:18,height:18,child:CircularProgressIndicator(strokeWidth:2)):
              Icon(sending?Icons.send_rounded:Icons.sentiment_satisfied_alt,color:Colors.white70,size:21));
        })),
    ))"""+s[b:]
    return s

if __name__=='__main__':
    changes=[]
    for p,fn in [('app/lib/main.dart',main_transform),
                 ('app/lib/live_broadcast_studio.dart',live_transform),
                 ('app/lib/build445_inbox_model.dart',model_transform),
                 ('app/lib/build448_live_guests.dart',guest_transform),
                 ('app/lib/build453_widgets.dart',composer_transform)]:
        path=Path(p);old=path.read_text();new=fn(old)
        assert fn(new)==new
        changes.append((path,new))
    for path,new in changes:path.write_text(new)
    print('Build540 reference presentation applied; RTC, package and signing unchanged')
