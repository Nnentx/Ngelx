import 'dart:typed_data';
import 'package:flutter_test/flutter_test.dart';
import '../lib/build570_perf.dart';
void main(){test('image byte cache respects byte and entry limits while preserving original data',(){final cache=<String,Uint8List>{};for(var n=0;n<20;n++)ngelx570CachePut(cache,'$n',Uint8List.fromList([n,n,n,n]),maxBytes:12,maxEntries:8);expect(cache.keys,['17','18','19']);expect(cache['19'],[19,19,19,19]);ngelx570CachePut(cache,'19',Uint8List(2),maxBytes:12,maxEntries:8);expect(cache.values.fold<int>(0,(n,b)=>n+b.length),10);ngelx570CachePut(cache,'large',Uint8List(13),maxBytes:12,maxEntries:8);expect(cache.containsKey('large'),false);});}
