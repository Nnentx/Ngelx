part of 'main.dart';

// Build526: both background and foreground group missed-call timers must
// re-read the same call inside one Firestore transaction. A user joining
// between a stale snapshot and a blind .set() may NOT end the active call.
//
// This never touches an individual/private call, LiveKit session, or peer.
Future<bool> ngelx526ExpireUnansweredGroupCall(
  DocumentReference<Map<String,dynamic>> ref,
  String roomName,
) async {
  if (!roomName.startsWith('group_')) return false;
  Map<String,dynamic>? closure;
  try{
    closure=await FirebaseFirestore.instance
        .runTransaction<Map<String,dynamic>?>((tx)async{
    final snapshot=await tx.get(ref);
    final data=snapshot.data();
    if(data==null ||
       data['callRoomName']!=roomName ||
       data['callStatus']!='ringing')return null;
    final participants=List<String>.from(
      data['callParticipants']??const <String>[]);
    if(participants.length>1)return null;
    // Build528: fail closed if the call's server-side creation time is
    // missing. Missing metadata must never make a 2-minute timer immediate.
    // A LiveKit acknowledgement can have stamped callConnectedAt while
    // callStatus is still ringing due to a delayed cross-client update.
    if(data['callConnectedAt'] is Timestamp)return null;
    final createdAt=data['callCreatedAt'];
    if(createdAt is! Timestamp)return null;
    // Never expire before 120 seconds according to the recorded timestamp.
    // Client clock skew still needs multi-device acceptance testing.
    if(DateTime.now().toUtc().difference(createdAt.toDate().toUtc())<
        const Duration(seconds:120))return null;
    tx.update(ref,<String,dynamic>{
      'callStatus':'missed',
      'callEndedAt':FieldValue.serverTimestamp(),
      'callAutoEnded':true,
      'callAutoEndedReason':'no_participants_2m',
    });
    return <String,dynamic>{
      'messageId':(data['callMessageId']??'').toString(),
    };
    });
  }on FirebaseException catch(error){
    if(error.code!='permission-denied')rethrow;
    // Another timer or a new participant may have committed before this
    // optimistic update. Inspect the authoritative room and only turn a
    // superseded expiration into a safe no-op; never mask stable ACL errors.
    final current=(await ref.get()).data();
    if(current==null||current['callRoomName']!=roomName||
       current['callStatus']!='ringing'||
       current['callConnectedAt'] is Timestamp||
       List<String>.from(current['callParticipants']??const <String>[]).length>1){
      debugPrint('Build533: obsolete missed-call timeout was ignored');
      return false;
    }
    rethrow;
  }
  if(closure==null)return false;
  // Updating the originating call message can be disallowed when another
  // member is the initiator. The authoritative call document was already
  // closed, so a receipt failure must not retry/end a different call.
  final messageId=closure['messageId'] as String;
  if(messageId.isNotEmpty){
    try{
      await ref.collection('messages').doc(messageId).set(<String,dynamic>{
        'callStatus':'missed',
        'callEndedAt':FieldValue.serverTimestamp(),
        'durationSeconds':0,
        'callAutoEnded':true,
        'callAutoEndedReason':'no_participants_2m',
      },SetOptions(merge:true));
    }catch(_){
      debugPrint('Build526 missed-call receipt unavailable');
    }
  }
  return true;
}
