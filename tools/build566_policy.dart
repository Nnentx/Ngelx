// An empty first snapshot is loading, not evidence that the opponent left.
bool ngelx566PkShouldEnd({required int remaining,required bool opponentLoaded,required bool serverConfirmed,required bool opponentFresh})=>
 remaining<=0||(opponentLoaded&&serverConfirmed&&!opponentFresh);
int ngelx566InboxTime(int messageTime,int openedTime)=>messageTime>openedTime?messageTime:openedTime;
int ngelx566InboxCompare(bool pinnedA,int timeA,bool pinnedB,int timeB)=>pinnedA!=pinnedB?(pinnedA?-1:1):timeB.compareTo(timeA);
final int ngelx566NoticePublished=DateTime.utc(2026,10,25,8,3).millisecondsSinceEpoch;
