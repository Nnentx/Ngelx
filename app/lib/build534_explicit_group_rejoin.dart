part of 'main.dart';

// Build534: ONLY a deliberate on-screen confirmation may call this helper.
// The rule engine independently verifies the Firebase identity, room state,
// exact field delta, and moderation exclusions. Merely receiving a LiveKit
// remote-track / reconnect callback MUST NOT invoke this method.
Future<bool> ngelx534ExplicitRejoinGroupCall(
  DocumentReference<Map<String,dynamic>> ref,
  String roomName,
  String uid, {
  required bool userConfirmed,
  bool Function()? cancelled,
}) async {
  if (!userConfirmed || !roomName.startsWith('group_') || uid.isEmpty ||
      FirebaseAuth.instance.currentUser?.uid != uid ||
      cancelled?.call() == true) return false;
  return FirebaseFirestore.instance.runTransaction<bool>((tx) async {
    if (cancelled?.call() == true) return false;
    final snap=await tx.get(ref);
    final data=snap.data();
    if (data == null || data['isGroup'] != true ||
        data['callRoomName'] != roomName || data['callStatus'] != 'active') {
      return false;
    }
    final members=List<String>.from(data['members']??const <String>[]);
    final participants=List<String>.from(
        data['callParticipants']??const <String>[]);
    final oldExits=List<String>.from(
        data['callExitedUids']??const <String>[]);
    if (!members.contains(uid) ||
        !members.contains((data['callStartedBy']??'').toString()) ||
        participants.isEmpty || participants.contains(uid) ||
        data['callExitedRoomName'] != roomName || !oldExits.contains(uid)) {
      return false;
    }
    final kicked=List<String>.from(
        data['callKickedUids']??const <String>[]);
    final moderationRoom=(data['callModerationRoom']??'').toString();
    if (kicked.contains(uid) &&
        (moderationRoom.isEmpty || moderationRoom == roomName)) return false;
    if (cancelled?.call() == true) return false;
    // Both changes commit together. Fresh server token authorization succeeds
    // only after this member-specific exit marker has been removed.
    // Existing active callers, peer exits, room name and status are unchanged.
    tx.update(ref,<String,dynamic>{
      'callExitedUids':FieldValue.arrayRemove([uid]),
      'callParticipants':FieldValue.arrayUnion([uid]),
    });
    return true;
  });
}

// Intended UI entry point. The dialog is tied to the actual tap handler,
// not to automatic RTC reconnect. Future caller must handle a failed token
// acquisition by reverting this participant-scoped join (or showing retry).
Future<bool> ngelx534ConfirmAndRejoinGroupCall(
  BuildContext context,
  DocumentReference<Map<String,dynamic>> ref,
  String roomName, {
  bool Function()? cancelled,
}) async {
  final uid=FirebaseAuth.instance.currentUser?.uid;
  if (uid==null || !roomName.startsWith('group_') || !context.mounted ||
      cancelled?.call()==true) return false;
  final approved=await showDialog<bool>(
    context:context,
    builder:(dialog)=>AlertDialog(
      title:const Text('Grup görüşmesine yeniden katıl?'),
      content:const Text('Yeniden katılırsan mikrofon ve kamera izinlerin geçerli görüşmeye uygulanabilir.'),
      actions:[
        TextButton(onPressed:()=>Navigator.of(dialog).pop(false),
          child:const Text('Vazgeç')),
        TextButton(onPressed:()=>Navigator.of(dialog).pop(true),
          child:const Text('Yeniden katıl')),
      ],
    ),
  ) ?? false;
  if (!approved || !context.mounted || cancelled?.call()==true) return false;
  return ngelx534ExplicitRejoinGroupCall(
    ref,roomName,uid,userConfirmed:approved,cancelled:cancelled);
}
