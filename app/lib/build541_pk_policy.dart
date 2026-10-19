// Pure consent policy shared by the audio PK client and regression tests.
class Ngelx541PkRoom {
  final String id,owner,session,peer;
  final bool publicAndFresh,active;
  final int endsAt;
  const Ngelx541PkRoom({required this.id,required this.owner,required this.publicAndFresh,this.active=false,this.session='',this.peer='',this.endsAt=0});
}
bool ngelx541PkMutual(Ngelx541PkRoom a,Ngelx541PkRoom b,int now)=>
  a.publicAndFresh&&b.publicAndFresh&&a.active&&b.active&&a.id!=b.id&&a.owner!=b.owner&&
  a.owner.isNotEmpty&&b.owner.isNotEmpty&&a.session.isNotEmpty&&a.session==b.session&&
  a.peer==b.id&&b.peer==a.id&&a.endsAt==b.endsAt&&a.endsAt>now&&a.endsAt-now<=190000;
bool ngelx541PkCanAccept({required Ngelx541PkRoom own,required Ngelx541PkRoom other,required String uid,required String inviterUid,required String inviteeUid,required String inviterRoom,required String inviteeRoom,required String status,required int expiresAt,required int now})=>
  uid.isNotEmpty&&uid==own.owner&&uid==inviteeUid&&other.owner==inviterUid&&
  own.id==inviteeRoom&&other.id==inviterRoom&&own.id!=other.id&&own.owner!=other.owner&&
  own.publicAndFresh&&other.publicAndFresh&&!own.active&&!other.active&&
  status=='pending'&&expiresAt>now&&expiresAt-now<=60000;
