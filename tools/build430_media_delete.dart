Future<void> ngelxMedyaSil(String rawUrl) async {
  final raw=rawUrl.trim();
  if(raw.isEmpty)return;
  final uid=FirebaseAuth.instance.currentUser?.uid;
  if(uid==null)throw StateError('Medya silmek için oturum gerekli.');
  final api=await ngelxMediaApiAdresi();
  if(raw.startsWith('gs://')||raw.contains('firebasestorage.googleapis.com')){
    final storage=FirebaseStorage.instance;
    final ref=storage.refFromURL(raw);
    final parts=ref.fullPath.split('/');
    if(ref.bucket!=storage.ref().bucket||parts.length<3||parts[1]!=uid||parts.contains('..')){
      throw StateError('Medya sahibi doğrulanamadı.');
    }
    try{await ref.delete().timeout(const Duration(seconds:12));}
    on FirebaseException catch(e){if(e.code!='object-not-found')rethrow;}
  }else{
    final uri=Uri.tryParse(raw),base=Uri.tryParse(api);
    if(uri==null||base==null||uri.origin!=base.origin||!uri.path.startsWith('/media/')){
      throw StateError('Medya sunucusu doğrulanamadı.');
    }
    final key=Uri.decodeComponent(uri.path.substring('/media/'.length));
    final parts=key.split('/');
    if(parts.length<3||parts[1]!=uid||parts.contains('..')||parts.contains('.')){
      throw StateError('Medya sahibi doğrulanamadı.');
    }
    final token=await FirebaseAuth.instance.currentUser?.getIdToken();
    if(token==null||token.isEmpty)throw StateError('Medya silmek için oturum gerekli.');
    try{
      await Dio().delete(api+'/object',queryParameters:{'key':key},options:Options(
        headers:{'Authorization':'Bearer '+token},
        sendTimeout:const Duration(seconds:12),receiveTimeout:const Duration(seconds:12),
      ));
    }on DioException catch(e){if(e.response?.statusCode!=404)rethrow;}
  }
  await ngelxAgResmiOnbelleginiTemizle(raw);
}
