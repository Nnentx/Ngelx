import 'dart:typed_data';
void ngelx570CachePut(Map<String,Uint8List> cache,String key,Uint8List bytes,{int maxBytes=24*1024*1024,int maxEntries=96}){
 cache.remove(key);if(bytes.length>maxBytes)return;
 var total=bytes.length+cache.values.fold<int>(0,(n,b)=>n+b.length);
 while(cache.isNotEmpty&&(cache.length>=maxEntries||total>maxBytes)){final first=cache.keys.first;total-=cache.remove(first)!.length;}
 cache[key]=bytes;
}
