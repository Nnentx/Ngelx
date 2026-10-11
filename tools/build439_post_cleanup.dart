// The queue contains only server-read media of the currently authenticated owner.
Future<void> ngelx439RememberPostCleanup(String uid,String id,Set<String> urls)async{
  final prefs=await SharedPreferences.getInstance();
  await prefs.setString('post_cleanup439_${uid}_$id',jsonEncode(urls.toList()));
}
bool _ngelx439CleanupRunning=false;
Future<void> ngelx439RetryPostCleanup(String uid)async{
  if(_ngelx439CleanupRunning||FirebaseAuth.instance.currentUser?.uid!=uid)return;
  _ngelx439CleanupRunning=true;
  try{
    final prefs=await SharedPreferences.getInstance();
    final prefix='post_cleanup439_${uid}_';
    for(final key in prefs.getKeys().where((k)=>k.startsWith(prefix)).toList()){
      if(FirebaseAuth.instance.currentUser?.uid!=uid)return;
      final id=key.substring(prefix.length);
      try{
        // Never remove media while its original post still exists (or while offline).
        final post=await FirebaseFirestore.instance.collection('videos').doc(id)
          .get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:8));
        if(post.exists)continue;
        final urls=List<String>.from(jsonDecode(prefs.getString(key)??'[]'));
        var complete=true;
        for(final url in urls){
          if(FirebaseAuth.instance.currentUser?.uid!=uid)return;
          try{await ngelxMedyaSil(url).timeout(const Duration(seconds:15));}
          catch(_){complete=false;}
        }
        if(complete&&FirebaseAuth.instance.currentUser?.uid==uid)await prefs.remove(key);
      }catch(_){/* Keep durable work for the next signed-in foreground session. */}
    }
  }finally{_ngelx439CleanupRunning=false;}
}
