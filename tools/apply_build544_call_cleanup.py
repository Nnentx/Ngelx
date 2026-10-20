"""Apply after Build543. Preserve unrelated UI and server permissions."""
from pathlib import Path

MARK = '// Build544 account-bound call cleanup'

def once(text, old, new):
    if text.count(old) != 1:
        raise RuntimeError(f'Build544 anchor mismatch: {old[:90]}')
    return text.replace(old, new, 1)

def main(text):
    text = once(text,
        "      final aktif=durum=='ringing'||durum=='active';",
        "      final aktif=(durum=='ringing'||durum=='active')&&sameCall&&ngelx440CallJoinable(callData,DateTime.now());")
    text = once(text,
        '_ngelx439AuthOperations.signIn(()=>FirebaseAuth.instance.signInWithEmailAndPassword(email:email,password:password));',
        '''_ngelx439AuthOperations.signIn(()async{
    // Finish the old identity's server departure before replacing its token.
    // A denied/offline departure keeps this account active for an explicit retry.
    await ngelx544BeforeAccountChange();
    return FirebaseAuth.instance.signInWithEmailAndPassword(email:email,password:password);
  });''')
    text += '''
Future<void> ngelx544BeforeAccountChange()async{
  final uid=FirebaseAuth.instance.currentUser?.uid;
  if(uid==null)return;
  for(final entry in ngelx445CallDetails.entries.toList()){
    if(entry.value.uid==uid)await ngelx445EndBackground(entry.key);
  }
  await ngelx542RetryPendingLeaves().timeout(const Duration(seconds:12));
  final prefs=await SharedPreferences.getInstance();
  final pending=prefs.getKeys().any((key)=>key.startsWith('pending_call_leave_542_${uid}_')&&!key.contains('_receipt_'));
  if(pending)throw StateError('Aramadan ayrılma kaydı tamamlanamadı. Bağlantını kontrol edip tekrar dene.');
}
'''
    return text

def behavior(text):
    return once(text,
        "  if(data['callEndedAt']!=null)return false;",
        """  if(data['callEndedAt']!=null)return false;
  // Empty committed membership cannot advertise an active room. Keep legacy
  // ringing records without the field compatible until their normal expiry.
  final participants=data['callParticipants'];
  if(participants is List&&participants.isEmpty)return false;""")

def pending(text):
    return once(text,
        "  unawaited(_ngelx542AttemptLeave(key,prefs).catchError((Object error){debugPrint('Self-leave queued for retry: $error');}));",
        """  try{
    await _ngelx542AttemptLeave(key,prefs).timeout(const Duration(seconds:10));
  }catch(error){debugPrint('Self-leave queued for retry: $error');}""")

TRANSFORMS={'app/lib/main.dart':main,'app/lib/build440_behavior.dart':behavior,'app/lib/build542_pending_leave.dart':pending}
def transform(text, fn):
    return text if MARK in text else fn(text)+'\n'+MARK+'\n'

if __name__=='__main__':
    changes=[]
    for name,fn in TRANSFORMS.items():
        path=Path(name); value=transform(path.read_text(),fn)
        assert transform(value,fn)==value
        changes.append((path,value))
    for path,value in changes:path.write_text(value)
