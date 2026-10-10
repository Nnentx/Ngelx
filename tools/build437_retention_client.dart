final ngelx437ImageCache=CacheManager(Config('ngelx_images437',stalePeriod:const Duration(days:7),maxNrOfCacheObjects:200));
bool ngelx437ReceiptVisible({required bool foreground,required bool currentRoute,required bool listReady,required bool atBottom,required bool searching})=>foreground&&currentRoute&&listReady&&atBottom&&!searching;
bool ngelx437MediaInList(dynamic stamp,DateTime now)=>stamp is Timestamp&&stamp.toDate().isAfter(now.subtract(const Duration(hours:48)));
bool ngelx437MessageExpired(dynamic stamp,DateTime now)=>stamp is Timestamp&&!stamp.toDate().isAfter(now.subtract(const Duration(days:14)));
String ngelx437SharedEmoji(Map<String,dynamic> chat){final selected=chat['quickEmoji'];return selected is String&&selected.trim().isNotEmpty?selected:'👍';}

// Only application-owned downloaded attachment copies are eligible. Camera
// originals, pending uploads, drafts and unrelated temporary files are untouched.
Future<void> ngelx437TrimDownloads()async{
  try{
    final root=await getTemporaryDirectory();
    final managed=Directory('${root.path}/ngelx_message435');
    if(!await managed.exists())return;
    final files=<({File file,FileStat stat})>[];
    await for(final entry in managed.list(recursive:true,followLinks:false)){
      if(entry is File){final stat=await entry.stat();if(stat.type==FileSystemEntityType.file)files.add((file:entry,stat:stat));}
    }
    files.sort((a,b)=>a.stat.modified.compareTo(b.stat.modified));
    var bytes=files.fold<int>(0,(total,item)=>total+item.stat.size);
    final cutoff=DateTime.now().subtract(const Duration(days:7));
    for(final item in files){
      if(item.stat.modified.isAfter(cutoff)&&bytes<=256*1024*1024)continue;
      // A file being replaced/downloaded during this pass is retained.
      final fresh=await item.file.stat();
      if(fresh.modified!=item.stat.modified||fresh.size!=item.stat.size)continue;
      await item.file.delete();bytes-=item.stat.size;
    }
  }catch(_){/* Cache housekeeping never prevents sign-in or sending. */}
}
final _ngelx437SeenLocks=<String>{};
Future<void> ngelx437MarkGroupMessagesSeen({required String chatId,required List<QueryDocumentSnapshot<Map<String,dynamic>>> docs,required String uid,required bool shareReadReceipt})async{
  final key='$chatId/$uid';if(!_ngelx437SeenLocks.add(key))return;
  try{await ngelxMarkGroupMessagesSeen(chatId:chatId,docs:docs,uid:uid,shareReadReceipt:shareReadReceipt).timeout(const Duration(seconds:15));}
  catch(_){/* The thread receipt remains available; a later snapshot retries individual markers. */}
  finally{_ngelx437SeenLocks.remove(key);}
}
