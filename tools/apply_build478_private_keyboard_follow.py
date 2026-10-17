#!/usr/bin/env python3
"""Build478: keep the last private message in view while Android IME resizes.

Do not interfere with reading old messages, typing throttling or media.
Provide readable timestamps outside text balloons over photo backgrounds.
"""
from pathlib import Path

MAIN=Path('app/lib/main.dart')
BEGIN='class _SohbetPageState extends State<SohbetPage>'
END='class NgelXSesliMesaj extends StatefulWidget'
MARK='// Build478: follow keyboard layout only when the user is at chat bottom'
CLOCK='// Build478: improve outside-bubble timestamp contrast on photo backgrounds'

def one(src,old,new,why):
    n=src.count(old)
    if n!=1:raise RuntimeError(f'Build478 {why}: expected 1 anchor, found {n}')
    return src.replace(old,new,1)

def transform(source):
    if MARK in source:
        return source
    a=source.index(BEGIN);b=source.index(END,a)
    chat=source[a:b]
    chat=one(chat,
      'class _SohbetPageState extends State<SohbetPage> with Ngelx437MessageJump<SohbetPage> {',
      'class _SohbetPageState extends State<SohbetPage> with Ngelx437MessageJump<SohbetPage>, WidgetsBindingObserver {',
      'listen for Android inset changes')
    chat=one(chat,
      '''  void _ngelx465StopOpeningBottom(){
    _ngelx465OpeningScrollTimer?.cancel();
    _ngelx465OpeningScrollTimer=null;
  }''',
      '''  void _ngelx465StopOpeningBottom(){
    _ngelx465OpeningScrollTimer?.cancel();
    _ngelx465OpeningScrollTimer=null;
  }

  // Build478: follow keyboard layout only when the user is at chat bottom.
  // Tapping or scrolling old messages disables this behavior immediately.
  bool _ngelx478FollowKeyboard=false;
  bool _ngelx478FrameQueued=false;

  void _ngelx478ComposerFocus(){
    _ngelx465StopOpeningBottom();
    if(jumpActive||!liste.hasClients)return;
    final p=liste.position;
    if(!p.hasContentDimensions)return;
    _ngelx478FollowKeyboard=p.maxScrollExtent-p.pixels<150;
  }

  void _ngelx478HistoryPointer(){
    _ngelx478FollowKeyboard=false;
    _ngelx465StopOpeningBottom();
  }

  @override
  void didChangeMetrics(){
    super.didChangeMetrics();
    if(!_ngelx478FollowKeyboard||!mounted||_ngelx478FrameQueued)return;
    _ngelx478FrameQueued=true;
    WidgetsBinding.instance.addPostFrameCallback((_){
      _ngelx478FrameQueued=false;
      if(!mounted||!_ngelx478FollowKeyboard||jumpActive||!liste.hasClients)return;
      final p=liste.position;
      if(!p.hasContentDimensions)return;
      if(p.maxScrollExtent-p.pixels>1)liste.jumpTo(p.maxScrollExtent);
    });
  }''',
      'keyboard metric tail follow with history protection')
    chat=one(chat,
      '''  void initState(){
    super.initState();
    liste.addListener(_private437Scroll);''',
      '''  void initState(){
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    liste.addListener(_private437Scroll);''',
      'register metric observer')
    chat=one(chat,
      '''  void dispose(){_ngelx465StopOpeningBottom();_ngelx470ComposerTick?.cancel();''',
      '''  void dispose(){WidgetsBinding.instance.removeObserver(this);_ngelx478FollowKeyboard=false;_ngelx465StopOpeningBottom();_ngelx470ComposerTick?.cancel();''',
      'release metric observer')
    chat=one(chat,
      '''                          onTap:_ngelx465StopOpeningBottom,''',
      '''                          onTap:_ngelx478ComposerFocus,''',
      'on-tap pin only when near bottom')
    chat=one(chat,
      '''child:Listener(onPointerDown:(_)=>_ngelx465StopOpeningBottom(),child:ListView.builder(''',
      '''child:Listener(onPointerDown:(_)=>_ngelx478HistoryPointer(),child:ListView.builder(''',
      'release follow lock on manual history touch')
    if CLOCK in chat:raise RuntimeError('Build478 clock already present without main marker')
    start=chat.index('        if(yaziSaatiDisarida&&saat.isNotEmpty)')
    stop=chat.index('        ]),\n      ),\n    );\n  }',start)
    clock=chat[start:stop]
    clock=one(clock,
      '''        if(yaziSaatiDisarida&&saat.isNotEmpty)
          Padding(''',
      '''        // Build478: improve outside-bubble timestamp contrast on photo backgrounds.
        if(yaziSaatiDisarida&&saat.isNotEmpty)
          Padding(''',
      'mark contrast source')
    clock=one(clock,
      '''            child:Row(mainAxisSize:MainAxisSize.min,children:[''',
      '''            child:DecoratedBox(
              decoration:BoxDecoration(
                color:Colors.white.withValues(alpha:.90),
                borderRadius:BorderRadius.circular(10),
              ),
              child:Padding(
                padding:const EdgeInsets.symmetric(horizontal:6,vertical:2),
                child:Row(mainAxisSize:MainAxisSize.min,children:[''',
      'light capsule behind timestamp')
    clock=one(clock,
      '''Text(saat,style:const TextStyle(fontSize:10.5,color:Color(0xFF6B7280)))''',
      '''Text(saat,style:const TextStyle(fontSize:10.5,color:Color(0xFF334155),fontWeight:FontWeight.w600))''',
      'timestamp legibility')
    if not clock.endswith('''            ]),
          ),
'''):
        raise RuntimeError('Build478 timestamp closing layout changed')
    clock=clock[:-len('''            ]),
          ),
''')]+'''                ]),
              ),
            ),
          ),
'''
    chat=chat[:start]+clock+chat[stop:]
    for preserve in ('if(yaziSaatiDisarida&&saat.isNotEmpty)',
          "tooltip:'Galeri'","tooltip:'Kamera'",
          'height:math.max(54.0,MediaQuery.viewPaddingOf(context).bottom)',
          '_ngelx477PhotoPickerActive=false',
          'onChanged:mesajDegisti',
          '_ngelx472Wallpaper(arkaPlan,arkaPlanUrl,arkaPlanOpaklik)',
          'if(!_ngelx474MessagesOpened)'):
        if preserve not in chat:raise RuntimeError('Build478 missing '+preserve)
    return source[:a]+chat+source[b:]

if __name__=='__main__':
    before=MAIN.read_text(encoding='utf-8')
    after=transform(before)
    if before!=after:MAIN.write_text(after,encoding='utf-8')
    print('Build478: keyboard follows visible tail without forcing history; clocks contrast improved')
