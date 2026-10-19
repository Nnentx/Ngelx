part of 'main.dart';

// Build527: atomically register group LiveKit reconnection or first join.
// An old asynchronous callback may NEVER resurrect an ended, missed,
// replaced, or moderated call. Private calls remain on their old path.
Future<bool> ngelx527RegisterGroupParticipant(
  DocumentReference<Map<String,dynamic>> ref,
  String roomName,
  String uid, {
  required bool activate,
  bool Function()? cancelled,
}) async {
  if (!roomName.startsWith('group_') || uid.isEmpty) return false;
  return FirebaseFirestore.instance.runTransaction<bool>((tx)async{
    if(cancelled?.call()==true)return false;
    final snap=await tx.get(ref);
    final data=snap.data();
    if(data==null||
       data['callRoomName']!=roomName||
       !const {'ringing','active'}.contains(data['callStatus']))return false;
    final members=List<String>.from(data['members']??const <String>[]);
    if(!members.contains(uid))return false;
    final kicks=List<String>.from(data['callKickedUids']??const <String>[]);
    final moderationRoom=(data['callModerationRoom']??'').toString();
    if(kicks.contains(uid)&&(moderationRoom.isEmpty||
        moderationRoom==roomName))return false;
    // Build530: no late join/track callback can re-add an explicitly
    // departed participant to the same room after their leave committed.
    // The next group call is not affected by historical exit markers.
    if(data['callExitedRoomName']==roomName &&
        List<String>.from(data['callExitedUids']??const <String>[])
            .contains(uid))return false;
    // Check cancel again after the asynchronous transaction read.
    // A local leave that wins before commit cannot re-add its own UID.
    if(cancelled?.call()==true)return false;
    final status=data['callStatus']=='active'||activate?'active':'ringing';
    tx.update(ref,<String,dynamic>{
      'callParticipants':FieldValue.arrayUnion([uid]),
      'callStatus':status,
      if(status=='active'&&data['callConnectedAt'] is! Timestamp)
        'callConnectedAt':FieldValue.serverTimestamp(),
    });
    return true;
  });
}

// For the remote-track callback, register only an already-authenticated
// local account. All eligibility checks remain inside the transaction.
Future<void> ngelx527ConfirmGroupRemoteTrack(
  DocumentReference<Map<String,dynamic>> ref,
  String roomName, {
  bool Function()? cancelled,
}) async {
  final uid=FirebaseAuth.instance.currentUser?.uid;
  if(uid==null||cancelled?.call()==true)return;
  try{
    await ngelx527RegisterGroupParticipant(
      ref,roomName,uid,activate:true,cancelled:cancelled);
  }catch(_){
    debugPrint('Build527 group track ack did not alter call state');
  }
}
