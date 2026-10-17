#!/usr/bin/env python3
"""Build471: native group/private call visual routing; preserve the Build470
ring, notification channel, answer/reject and full-screen fallback exactly.
"""
from pathlib import Path
SERVICE=Path('app/android/app/src/main/kotlin/com/nnentx/ngelx_app/IncomingCallService.kt')
MAIN=Path('app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt')
FLUTTER=Path('app/lib/build448_incoming_calls.dart')
TAG='// Build471: distinguish group vs private native incoming designs'
def once(s,old,new,why):
    n=s.count(old)
    if n!=1:raise RuntimeError(f'Build471 {why}: expected exactly one anchor got {n}')
    return s.replace(old,new,1)
def service(src):
    if TAG in src:return src
    s=once(src,
      'show(this, chat, room, d["title"] ?: "NgelX araması", d["video"] == "true")',
      'show(this, chat, room, d["title"] ?: "NgelX araması", d["video"] == "true", d["group"] == "true")',
      'FCM native incoming group hint')
    s=once(s,
      '        fun show(context: Context, chat: String, room: String, title: String, video: Boolean) {',
      '        fun show(context: Context, chat: String, room: String, title: String, video: Boolean, group: Boolean = false) {',
      'native show overload')
    s=once(s,
      '                putExtra("callVideo470", video)',
      '''                putExtra("callVideo470", video)
                // Build471: distinguish group vs private native incoming designs.
                // Local account-scoped chat kind covers push relay deployments
                // which still omit the new group hint.
                putExtra("callGroup471", group || isGroupChat471(context, chat))''',
      'native Activity metadata')
    p='''        fun isStillRinging470(room: String): Boolean = room.isNotEmpty() && alerts.containsKey(room)'''
    a='''        private const val GROUP_PREFS471 = "ngelx_call_groups471"
        // Store only a chat/group boolean, scoped to the currently signed-in
        // user UID. No contact names, tokens, call room or message bodies.
        fun rememberChatKind471(context: Context, chat: String, group: Boolean) {
            if(chat.isEmpty() || chat.length > 150)return
            val uid = currentRecipient470(context) ?: return
            val pref = context.getSharedPreferences(GROUP_PREFS471, Context.MODE_PRIVATE)
            pref.edit().putBoolean("$uid|$chat", group).apply()
        }
        private fun isGroupChat471(context: Context, chat: String): Boolean {
            if(chat.isEmpty() || chat.length > 150)return false
            val uid = currentRecipient470(context) ?: return false
            return context.getSharedPreferences(GROUP_PREFS471, Context.MODE_PRIVATE)
                .getBoolean("$uid|$chat", false)
        }
'''
    s=once(s,p,a+p,'account-scoped group cache')
    for guard in ('setFullScreenIntent(fullScreenCall, true)','ring_blocked settings:',
     'fun rememberOwner470(', 'IncomingCallActivity470::class.java',
     'manager.currentInterruptionFilter'):
      if guard not in s:raise RuntimeError('Build470 ringtone contract missing '+guard)
    return s
def main(src):
    if '"noteChatKind471"' in src:return src
    s=once(src,
      '                    "setCallOwner470" -> {',
      '''                    "noteChatKind471" -> {
                        val chat = call.argument<String>("chat").orEmpty()
                        val group = call.argument<Boolean>("group") == true
                        IncomingCallService.rememberChatKind471(this, chat, group)
                        result.success(null)
                    }
                    "setCallOwner470" -> {''',
      'native method channel group metadata')
    s=once(s,
      'call.argument<Boolean>("video") == true); result.success(null)',
      'call.argument<Boolean>("video") == true,call.argument<Boolean>("group") == true); result.success(null)',
      'Flutter-triggered native show group')
    return s
def dart(src):
    if "'noteChatKind471'" in src:return src
    s=once(src,
      '''for(final change in s.docChanges){if(change.type!=DocumentChangeType.removed)unawaited(_pushOutgoing452(change.doc.id,change.doc.data()??<String,dynamic>{},user.uid));}''',
      '''for(final change in s.docChanges){
          if(change.type!=DocumentChangeType.removed){
            final value=change.doc.data()??<String,dynamic>{};
            // Per-change only, no all-chat rebuild on each snapshot.
            unawaited(channel.invokeMethod<void>('noteChatKind471',
              {'chat':change.doc.id,'group':value['isGroup']==true}).catchError((_){ }));
            unawaited(_pushOutgoing452(change.doc.id,value,user.uid));
          }
        }''',
      'existing inbox call watcher')
    s=once(s,
      '''unawaited(_ring(d.id,room,(v['callTitle']??v['groupName']??'NgelX araması').toString(),v['callVideo']==true,caller:v['isGroup']==true?'':(v['callStartedBy']??'').toString()));''',
      '''unawaited(_ring(d.id,room,(v['callTitle']??v['groupName']??'NgelX araması').toString(),v['callVideo']==true,group:v['isGroup']==true,caller:v['isGroup']==true?'':(v['callStartedBy']??'').toString()));''',
      'flutter native group call forwarding')
    s=once(s,
      "Future<void> _ring(String chat,String room,String title,bool video,{String caller=''})async{",
      "Future<void> _ring(String chat,String room,String title,bool video,{String caller='',bool group=false})async{",
      'group argument')
    s=once(s,
      "'title':title,'video':video",
      "'title':title,'video':video,'group':group",
      'show native payload')
    for guard in ("_ringingChat469","setCallOwner470","channel.invokeMapMethod<String,dynamic>('pendingAction')","_pushOutgoing452"):
      if guard not in s:raise RuntimeError('call delivery contract lost '+guard)
    return s
if __name__=='__main__':
    for path,fn in [(SERVICE,service),(MAIN,main),(FLUTTER,dart)]:
      before=path.read_text(encoding='utf-8')
      after=fn(before)
      if before!=after:path.write_text(after,encoding='utf-8')
      print('Build471 group/private routed:',path)
