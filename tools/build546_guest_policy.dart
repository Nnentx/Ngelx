// Pure admission/intent policy shared by live guest UI and regression tests.
bool ngelx546GuestAuthorized({required String expectedUid,required String? currentUid,
 required String expectedOwner,required String room,required String? currentRoom,
 required bool live,required String? owner,required String? host,required String? guest,
 required String? status})=>expectedUid.isNotEmpty&&expectedUid==currentUid&&live&&
 room.isNotEmpty&&room==currentRoom&&owner==expectedOwner&&host==expectedOwner&&
 guest==expectedUid&&status=='accepted';
bool ngelx546CanReuse({required bool connected,required bool canPublish,
 required List<String> sources,required bool microphone,required bool camera}){
 if(!connected||!canPublish)return false;
 final allowed=sources.map((s)=>s.toLowerCase()).toSet();
 return (!microphone||allowed.isEmpty||allowed.contains('microphone'))&&
 (!camera||allowed.isEmpty||allowed.contains('camera'));
}
bool ngelx546ShouldRetry(int attempts,bool wanted,bool alive)=>alive&&wanted&&attempts<3;
