#!/usr/bin/env python3
"""Build470: reduce per-key private chat work; preserve last verified inbox profiles.
Maintain account isolation, explicit real loading and same Firestore streams.
"""
from pathlib import Path
MAIN=Path("app/lib/main.dart")
INCOMING=Path("app/lib/build448_incoming_calls.dart")
TAG="// Build470: throttle private composer work off the immediate keystroke"
def one(s,old,new,name):
    if s.count(old)!=1:raise RuntimeError(f"Build470 {name}: expected 1 anchor, found {s.count(old)}")
    return s.replace(old,new,1)
def patch_main(src):
    if TAG in src:return src
    st=src.index('class _SohbetPageState extends State<SohbetPage>')
    end=src.index('class NgelXSesliMesaj extends StatefulWidget',st)
    s=src[st:end]
    s=one(s,
        "  final mesaj=TextEditingController(),liste=ScrollController(keepScrollOffset:false);",
        """  final mesaj=TextEditingController(),liste=ScrollController(keepScrollOffset:false);
  // Build470: throttle private composer work off the immediate keystroke.
  Timer? _ngelx470ComposerTick;
  String _ngelx470QueuedText='';""",
        'private composer state')
    if "  void mesajDegisti(String deger){" not in s:raise RuntimeError("Private composer not found")
    s=one(s,
       "  void mesajDegisti(String deger){\n    PrivateDraftStore.schedule(widget.chatId,deger);\n    mentionZamanlayici?.cancel();",
       """  void mesajDegisti(String deger){
    // Draft persistence is still scheduled for every edit; no keystroke is lost.
    PrivateDraftStore.schedule(widget.chatId,deger);
    // Stop the 2.2-second opening scroll timer when the user starts typing.
    _ngelx465StopOpeningBottom();
    _acilisKaydirmaKalan=0;
    _ilkMesajKaydirma=false;
    _ngelx470QueuedText=deger;
    // Keep all per-key Firestore, mention and timer work outside the
    // synchronous TextField onChanged path. Throttle, not debounce:
    // continuous typing still keeps the remote typing indicator updated.
    _ngelx470ComposerTick ??= Timer(const Duration(milliseconds:120),(){
      _ngelx470ComposerTick=null;
      if(mounted&&mesaj.text==_ngelx470QueuedText){
        _ngelx470ProcessComposer(_ngelx470QueuedText);
      }
    });
  }
  void _ngelx470ProcessComposer(String deger){
    mentionZamanlayici?.cancel();""", 'private typing throttle')
    s=one(s,"  void dispose(){_ngelx465StopOpeningBottom();",
      "  void dispose(){_ngelx465StopOpeningBottom();_ngelx470ComposerTick?.cancel();",
      'composer cleanup')
    for guard in ("PrivateDraftStore.schedule(widget.chatId,deger)",
      "onChanged:mesajDegisti","mentionOnerileri.clear()","typing_$ben",
      "messenger" if False else "void sonaGit({bool zorla=false})"):
      if guard not in s: raise RuntimeError("private chat contract missing: "+guard)
    src=src[:st]+s+src[end:]
    st=src.index('class _MesajPageState extends State<MesajPage>')
    end=src.index('class ArsivSohbetlerPage',st)
    s=src[st:end]
    s=one(s,'  final Map<String,Stream<DocumentSnapshot<Map<String,dynamic>>>> _profiles453={};',
      """  final Map<String,Stream<DocumentSnapshot<Map<String,dynamic>>>> _profiles453={};
  // Build470: a previously verified name remains visible during stream
  // reconnection. Scoped to signed-in account+recipient (not shared across users).
  final Map<String,Map<String,dynamic>> _ngelx470VerifiedProfiles={};""",
      'per account profile cache')
    s=one(s,
      '                    builder:(_,u){\n                      if(u.hasError){',
      """                    builder:(_,u){
                      final profileKey470='$ben|$other';
                      final verified470=_ngelx470VerifiedProfiles[profileKey470];
                      if(u.hasError&&!u.hasData&&verified470==null){""",
      'inbox error state with cached profile')
    s=one(s,'                      if(!u.hasData){\n                        _ngelx465PlanProfileRetry(other);',
      '                      if(!u.hasData&&verified470==null){\n                        _ngelx465PlanProfileRetry(other);',
      'inbox verified fallback for loading')
    s=one(s,'''                      if(u.data!.id!=other)return const SizedBox.shrink();
                      _ngelx465ProfileResolved(other);
                      
                      final p=u.data?.data()??{};''',
      '''                      if(u.hasData&&u.data!.id!=other)return const SizedBox.shrink();
                      if(u.hasData)_ngelx465ProfileResolved(other);
                      final p=u.hasData?(u.data?.data()??<String,dynamic>{})
                        :(verified470??<String,dynamic>{});
                      if(u.hasData&&p.isNotEmpty){
                        if(_ngelx470VerifiedProfiles.length>=240){
                          _ngelx470VerifiedProfiles.remove(_ngelx470VerifiedProfiles.keys.first);
                        }
                        _ngelx470VerifiedProfiles[profileKey470]=p;
                      }''',
       'account scoped stable profiles')
    # Preserve loading and error/retry for never-loaded profiles. Don't fabricate names.
    for guard in ("title:Text('Kişi bilgisi yükleniyor…')",
      "_ngelx465PlanProfileRetry(other)", "_profiles453.putIfAbsent(other",
      "if(u.data!.id!=other)" if False else "_ngelx465ProfileResolved(other)"):
      if guard not in s:raise RuntimeError("Inbox identity or recovery contract missing: "+guard)
    src=src[:st]+s+src[end:]
    return src
def patch_incoming(src):
    if "setCallOwner470" in src:return src
    return one(src, "      final epoch=++_authEpoch454;",
       """      final epoch=++_authEpoch454;
      // Build470: synchronize exact signed-in owner for cold native FCM
      // startup. Cleared on logout; never store a caller or message payload.
      try{await channel.invokeMethod<void>('setCallOwner470',{'uid':user?.uid});}catch(_){}
      if(epoch!=_authEpoch454)return;""",
       "auth owner synchronization")
if __name__=='__main__':
    before=MAIN.read_text(encoding='utf-8')
    after=patch_main(before)
    if after!=before:MAIN.write_text(after,encoding='utf-8')
    before=INCOMING.read_text(encoding='utf-8')
    after=patch_incoming(before)
    if after!=before:INCOMING.write_text(after,encoding='utf-8')
    print("Build470 private typing throttle, verified per-account inbox names and native auth bridge")
