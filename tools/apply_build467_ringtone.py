#!/usr/bin/env python3
"""Build467 native ringtone channel refresh, preserving incoming-call service."""
from pathlib import Path

SERVICE=Path('app/android/app/src/main/kotlin/com/nnentx/ngelx_app/IncomingCallService.kt')
OLD='const val CHANNEL = "ngelx_incoming_calls465"'
NEW='const val CHANNEL = "ngelx_incoming_calls467"'

def transform(s):
    if NEW in s:return s
    if s.count(OLD)!=1:raise RuntimeError('Build467 ringtone: unknown source channel')
    for guard in ('NotificationManager.IMPORTANCE_HIGH','setSound(ringtone','AudioManager.RINGER_MODE_NORMAL','sound.play()','ringing.remove(room)'):
        if guard not in s:raise RuntimeError('Build467 ringtone missing '+guard)
    return s.replace(OLD,NEW,1)

if __name__=='__main__':
    original=SERVICE.read_text(encoding='utf-8')
    changed=transform(original)
    if changed!=original:SERVICE.write_text(changed,encoding='utf-8')
    print('Build467: fresh incoming call ringtone channel with existing stop/cancel safeguards')
