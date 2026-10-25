part of 'main.dart';
class Ngelx570JoinSound {
 final lk.Room room;
 final Ngelx570JoinPolicy policy=Ngelx570JoinPolicy();
 final AudioPlayer player=AudioPlayer(handleAudioSessionActivation:false,handleInterruptions:false);
 bool disposed=false,playing=false;late final VoidCallback changed;
 Ngelx570JoinSound(this.room){
  policy.update(room.remoteParticipants.keys,connected:room.connectionState==lk.ConnectionState.connected);
  changed=(){if(policy.update(room.remoteParticipants.keys,connected:room.connectionState==lk.ConnectionState.connected))unawaited(_play());};
  room.addListener(changed);
 }
 Future<void> _play()async{
  if(disposed||playing)return;playing=true;
  try{await player.setAsset('assets/call_join570.wav');await player.setVolume(.65);if(!disposed)await player.play();}catch(e){debugPrint('Join notification unavailable');}finally{playing=false;}
 }
 Future<void> dispose()async{if(disposed)return;disposed=true;room.removeListener(changed);await player.dispose();}
}
