import 'package:flutter_test/flutter_test.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:ngelx_app/main.dart';
void main(){
 test('block guards either direction without affecting unrestricted pairs',(){
  expect(ngelx436Blocked({'blocked':['b']},{},'a','b'),isTrue);
  expect(ngelx436Blocked({}, {'blocked':['a']},'a','b'),isTrue);
  expect(ngelx436Blocked({'blocked':['c']},{},'a','b'),isFalse);
 });
 test('permanent permission failures never claim a network retry',(){
  expect(ngelx436Error(FirebaseException(plugin:'cloud_firestore',code:'permission-denied')),contains('izin'));
  expect(ngelx436Error(FirebaseException(plugin:'cloud_firestore',code:'permission-denied')),isNot(contains('Bağlantı')));
  expect(ngelx436Error(FirebaseException(plugin:'cloud_firestore',code:'resource-exhausted')),contains('sınır'));
  expect(ngelx436Error(StateError('Engel varken istek gönderilemez.')),contains('Engel'));
 });
}
