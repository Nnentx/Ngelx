part of 'main.dart';

// Build517: a group member leaves only their own LiveKit call membership.
// The call document is changed atomically, so two concurrent departures
// cannot both decide that they were the last participant from a stale read.
// This function never disconnects a peer, deletes a LiveKit room, or grants
// moderation permission.
Future<void> ngelx517LeaveGroupCall(
  DocumentReference<Map<String,dynamic>> ref,
  String roomName,
  String uid, {
  required bool video,
  String? displayName,
}) async {
  if (!roomName.startsWith('group_') || uid.isEmpty) {
    throw ArgumentError('Expected an authenticated group call member');
  }
  // Firestore clients can observe a concurrent same-document transaction as
  // permission-denied instead of a retriable ABORTED response when security
  // rules validate the post-commit participant list. Retry only if another
  // participant actually changed that list and this caller is still eligible.
  // Never retry a genuine ACL rejection or attempt to revive an ended room.
  List<String>? observedParticipants;
  Future<Map<String,dynamic>> attemptLeave()=>FirebaseFirestore.instance
      .runTransaction<Map<String,dynamic>>((tx) async {
    final snapshot=await tx.get(ref);
    final data=snapshot.data()??<String,dynamic>{};
    if (data['callRoomName']!=roomName ||
        const {'ended','rejected','missed'}.contains(data['callStatus'])) {
      return <String,dynamic>{'kind':'stale'};
    }
    final participants=List<String>.from(data['callParticipants']??const <String>[]);
    observedParticipants=participants;
    // Do not close a room if this device's membership has already been
    // removed by a moderator, another session, or a concurrent operation.
    if (!participants.contains(uid)) {
      return <String,dynamic>{'kind':'stale'};
    }
    final remaining=participants.where((id)=>id!=uid).toSet();
    final isLast=remaining.isEmpty;
    final connected=data['callConnectedAt'] is Timestamp;
    final missed=isLast&&!connected;
    final finalStatus=missed?'missed':'ended';
    // Build530: a voluntary exit must outlive delayed RTC reconnects for
    // this exact call room. A later room has a different name, so historical
    // exits cannot prevent a new call. Transaction retries preserve exits
    // from concurrent participants.
    final previousExitRoom=(data['callExitedRoomName']??'').toString();
    final exits=previousExitRoom==roomName
        ?FieldValue.arrayUnion([uid])
        :<String>[uid];
    tx.update(ref,<String,dynamic>{
      'callParticipants':FieldValue.arrayRemove([uid]),
      'callExitedRoomName':roomName,
      'callExitedUids':exits,
      // Starting the call never implies ownership over the other members'
      // active LiveKit media; even the original caller can safely leave.
      'callStatus':isLast?finalStatus:'active',
      if(isLast)'callEndedAt':FieldValue.serverTimestamp(),
    });
    final started=data['callConnectedAt'];
    final elapsed=started is Timestamp
      ?DateTime.now().difference(started.toDate()).inSeconds.clamp(0,86400)
      :0;
    return <String,dynamic>{
      'kind':isLast?'last':'left',
      'missed':missed,
      'messageId':(data['callMessageId']??'').toString(),
      'seconds':elapsed,
    };
  });
  Map<String,dynamic> result;
  for(var retry=0;;retry++){
    try{
      result=await attemptLeave();
      break;
    }on FirebaseException catch(error){
      if(error.code!='permission-denied'||retry>=4||
         observedParticipants==null)rethrow;
      // Only a demonstrated concurrent participant change warrants a fresh
      // transaction. This read is not a write and never authorizes itself.
      final current=(await ref.get()).data();
      if(current==null||current['callRoomName']!=roomName||
         const {'ended','missed','rejected'}.contains(current['callStatus']))return;
      final nowParticipants=List<String>.from(
        current['callParticipants']??const <String>[]);
      if(!nowParticipants.contains(uid))return;
      if(listEquals(nowParticipants,observedParticipants))rethrow;
      debugPrint('Build533: group member changed during leave; retrying');
    }
  }
  if (result['kind']=='stale') return;
  if (result['kind']=='last') {
    final status=result['missed']==true?'missed':'ended';
    final messageId=result['messageId'] as String;
    if (messageId.isNotEmpty) {
      // The call message belongs to its ORIGINAL sender. If another member
      // leaves last, Firestore may reject that user's edit under message ACLs.
      // The authoritative call record was already closed atomically; do not
      // skip the separately authorized call_end system notice.
      try {
        await ref.collection('messages').doc(messageId).set(<String,dynamic>{
          'callStatus':status,
          'callEndedAt':FieldValue.serverTimestamp(),
          'durationSeconds':result['seconds'],
        },SetOptions(merge:true));
      }catch(_){
        debugPrint('Build517 call receipt update denied or unavailable');
      }
    }
    await ref.collection('messages').doc('call_end_$roomName').set(<String,dynamic>{
      'senderId':uid,
      'type':'system',
      'systemAction':'call_end',
      'actorUid':uid,
      'callVideo':video,
      'text':status=='missed'?'Arama cevaplanmadı.':'Arama sona erdi.',
      'createdAt':FieldValue.serverTimestamp(),
    },SetOptions(merge:true));
    return;
  }
  final name=(displayName??'').trim();
  await ref.collection('messages').doc('call_leave_${roomName}_$uid').set(<String,dynamic>{
    'senderId':uid,
    'type':'system',
    'systemAction':'call_leave',
    'actorUid':uid,
    'callVideo':video,
    'text':(name.isEmpty?'Bir üye':name)+
      (video?' görüntülü aramadan ayrıldı.':' sesli aramadan ayrıldı.'),
    'createdAt':FieldValue.serverTimestamp(),
  },SetOptions(merge:true));
}
