#!/usr/bin/env python3
"""Build535: connect explicit group rejoin confirmation BEFORE LiveKit token fetch.

This transforms the generated Build527+534 Flutter call screen only. The
repository's large app/lib/main.dart is assembled by earlier Build4xx scripts;
no compilation or production deployment is implied by this source QA stage.
"""
from pathlib import Path

MAIN=Path('app/lib/main.dart')
MARK='// Build535: self-rejoin preflight before LiveKit token acquisition'
PART="part 'build534_explicit_group_rejoin.dart';"
CALL_START='class _NgelXAramaPageState'
CALL_END='class GrupBilgiPage'

def once(src, old, new, label):
    if src.count(old)!=1:
        raise RuntimeError(f'Build535 {label}: expected exactly one anchor, got {src.count(old)}')
    return src.replace(old,new,1)

PRE_FLIGHT="""      // Build535: self-rejoin preflight before LiveKit token acquisition.
      // A remote-track callback and automatic RTC retry must never prompt
      // for consent or silently remove the Build530 exit marker.
      if(grupAramasi){
        final current=await widget.aramaRef.get();
        final call=current.data();
        if(call==null||call['callRoomName']!=widget.roomName||
            !const {'ringing','active'}.contains(call['callStatus'])){
          throw StateError('Grup görüşmesi artık kullanılamıyor.');
        }
        final exited=(call['callExitedRoomName']==widget.roomName &&
            List<String>.from(call['callExitedUids']??const <String>[])
                .contains(u.uid));
        if(exited){
          if(yeniden)throw StateError(
            'Ayrıldığın grup görüşmesine otomatik bağlanılamaz.');
          final accepted=await ngelx534ConfirmAndRejoinGroupCall(
            context,widget.aramaRef,widget.roomName,
            cancelled:()=>bitiyor||!_alive444);
          if(!accepted){
            if(mounted)setState((){
              baglaniyor=false;
              yenidenBaglaniyor=false;
              hata='Yeniden katılım iptal edildi veya izin verilmedi.';
            });
            return;
          }
          rejoinApproved535=true;
        }
      }
"""
AFTER_CONNECT="""      rtcConnected535=true;
"""
FAILURE_OPTIONS="""      // Build535: failed token/connect must not silently evict another
      // session of the same account. Offer an explicit voluntary rollback,
      // using the already audited group self-leave transaction only if the
      // local RTC connection was never established.
      if(rejoinApproved535&&!rtcConnected535&&mounted&&!bitiyor){
        final discard=await showDialog<bool>(
          context:context,
          builder:(dialog)=>AlertDialog(
            title:const Text('Grup bağlantısı kurulamadı'),
            content:const Text(
              'Tekrar denemek için katılım kaydını koruyabilirsin. '
              'Ayrılmayı seçersen aynı hesabın diğer cihazdaki '
              'katılımı da etkilenebilir.'),
            actions:[
              TextButton(onPressed:()=>Navigator.of(dialog).pop(false),
                child:const Text('Tekrar deneyeceğim')),
              TextButton(onPressed:()=>Navigator.of(dialog).pop(true),
                child:const Text('Görüşmeden ayrıl')),
            ],
          ),
        ) ?? false;
        if(discard&&!bitiyor){
          try{
            await ngelx517LeaveGroupCall(
              widget.aramaRef,widget.roomName,u.uid,
              video:widget.goruntulu,displayName:u.displayName);
          }catch(error){
            debugPrint('Build535 voluntary recovery exit failed: $error');
          }
        }
      }
"""

def transform(src: str) -> str:
    if MARK in src:
        if src.count(MARK)!=1:
            raise RuntimeError('Build535 preflight duplicated in generated source')
        return src
    if PART not in src or src.count(PART)!=1:
        raise RuntimeError('Build535 needs the fully assembled Build534 part')
    if src.count(CALL_START)!=1 or src.count(CALL_END)!=1:
        raise RuntimeError('Build535 expected one group-capable call screen')
    a=src.index(CALL_START)
    b=src.index(CALL_END,a)
    call=src[a:b]
    if ('ngelx527RegisterGroupParticipant(' not in call or
        '_confirmGroupExit517()' not in call or
        'Future<void> baglan({bool yeniden=false})async{' not in call):
        raise RuntimeError('Build535 requires the Build527 and Build517 call paths')
    start=call.index('  Future<void> baglan({bool yeniden=false})async{')
    end=call.index('  lk.VideoTrack? _katilimciVideosu(',start)
    connect=call[start:end]
    connect=once(connect, '    lk.Room? r;\n    try{',
      '    lk.Room? r;\n    bool rejoinApproved535=false;\n'
      '    bool rtcConnected535=false;\n    try{',
      'per-attempt RTC state flags')
    connect=once(connect, '      await _izinleriIste();',
      PRE_FLIGHT+'      await _izinleriIste();',
      'consent before token acquisition')
    # Connection flag is true only after the LiveKit handshake returns.
    anchor="      oda=r;\n      final yerel=r.localParticipant;"
    connect=once(connect,anchor,AFTER_CONNECT+anchor,
      'LiveKit connected flag')
    connect=once(connect, '      oda=null;\n      if(yeniden&&',
      '      oda=null;\n'+FAILURE_OPTIONS+'      if(yeniden&&',
      'explicit post-failure voluntary exit option')
    if connect.index(MARK)>connect.index('final kaynak='):
        raise RuntimeError('Build535 consent must precede token fetch')
    if connect.index('rtcConnected535=true;') < connect.index('await r.connect('):
        raise RuntimeError('Build535 success flag must follow RTC handshake')
    call=call[:start]+connect+call[end:]
    return src[:a]+call+src[b:]

if __name__=='__main__':
    before=MAIN.read_text(encoding='utf-8')
    after=transform(before)
    if after!=before:MAIN.write_text(after,encoding='utf-8')
    print('Build535 generated call screen: consent before RTC token; no automatic rejoin or forced rollback')
