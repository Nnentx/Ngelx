#!/usr/bin/env python3
"""Build526: atomic unanswered GROUP timeout for both foreground & background.
Runs after the integrated Build525 source generation; private timers untouched.
"""
from pathlib import Path

MAIN=Path('app/lib/main.dart')
MARK="// Build526: protect unanswered group calls against stale timeout reads"

def replace_one(src,before,after,label):
    hits=src.count(before)
    if hits!=1:raise RuntimeError(f'Build526 {label}: expected 1 anchor, found {hits}')
    return src.replace(before,after,1)

def transform(src):
    if MARK in src:return src
    src=replace_one(src,
        "part 'build520_livekit_pip.dart';",
        "part 'build520_livekit_pip.dart';\npart 'build526_atomic_group_timeout.dart';",
        "timeout helper Flutter part")
    old_background="""_ngelxArkaPlanAramaZamanAsimlari[roomName]=Timer(Duration(seconds:kalan),()async{
      try{
        final current=await aramaRef.get();"""
    new_background="""_ngelxArkaPlanAramaZamanAsimlari[roomName]=Timer(Duration(seconds:kalan),()async{
      try{
        // Build526: protect unanswered group calls against stale timeout reads.
        if(roomName.startsWith('group_')){
          await ngelx526ExpireUnansweredGroupCall(aramaRef,roomName);
          return;
        }
        final current=await aramaRef.get();"""
    src=replace_one(src,old_background,new_background,"background group call timer")
    a=src.index('class _NgelXAramaPageState')
    b=src.index('class GrupBilgiPage',a)
    part=src[a:b]
    old_front="""cevapsizZamanlayici=Timer(Duration(seconds:kalan),()async{
      if(bitiyor)return;
      try{
        final d=await widget.aramaRef.get();"""
    new_front="""cevapsizZamanlayici=Timer(Duration(seconds:kalan),()async{
      if(bitiyor)return;
      try{
        // An active remote LiveKit member is never an unanswered call.
        // Firestore transaction re-checks the rest atomically.
        if(grupAramasi){
          if(oda?.remoteParticipants.isNotEmpty==true)return;
          await ngelx526ExpireUnansweredGroupCall(
            widget.aramaRef,widget.roomName);
          return;
        }
        final d=await widget.aramaRef.get();"""
    part=replace_one(part,old_front,new_front,"foreground group call timer")
    src=src[:a]+part+src[b:]
    if src.count(MARK)!=1:raise RuntimeError('Build526 marker missing or duplicated')
    return src

if __name__=='__main__':
    before=MAIN.read_text(encoding='utf-8')
    after=transform(before)
    if before!=after:MAIN.write_text(after,encoding='utf-8')
    print('Build526 QA applied: 2 group missed timers use one guarded Firestore transaction')
