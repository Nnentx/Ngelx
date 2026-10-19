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
  final closure=await FirebaseFirestore.instance.runTransaction<Map<String,dynamic>?>((tx)async{
    final snapshot=await tx.get(ref);
    final data=snapshot.data();
    if(data==null ||
       data['callRoomName']!=roomName ||
       data['callStatus']!='ringing')return null;
    final participants=List<String>.from(
      data['callParticipants']??const <String>[]);
    if(participants.length>1)return null;
    final createdAt=data['callCreatedAt'];
    // An early local timer or clock correction should not mark a group
    // call missed before its full 120-second unanswered window.
    if(createdAt is Timestamp &&
       DateTime.now().difference(createdAt.toDate())<
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
