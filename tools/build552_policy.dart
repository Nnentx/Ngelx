import 'package:flutter/widgets.dart';
bool ngelx552Visible(AppLifecycleState state)=>
 state==AppLifecycleState.resumed||state==AppLifecycleState.inactive;
int ngelx552Columns(int count)=>count<=1?1:count<=8?2:count<=9?3:4;
