from pathlib import Path
p=Path('app/lib/main.dart');s=p.read_text();assert '// Build441 child safety report' not in s
start=s.index('Future<void> sikayetEt(');end=s.index('Future<void> kullaniciyiEngelle',start);v=s[start:end]
v=v.replace("'Başkasını taklit ediyor']", "'Başkasını taklit ediyor','Çocuk güvenliği / istismar']")
v=v.replace('title:Text(n,','title:Text(_ngelx438Ui(n),')
v=v.replace("'reason':neden,'status':'pending'", "'reason':neden,'category':neden=='Çocuk güvenliği / istismar'?'child_safety':'general','status':'pending'")
v=v.replace("try{await FirebaseFirestore", "if(FirebaseAuth.instance.currentUser?.uid!=bildiren.uid)return;\n  try{await FirebaseFirestore")
v=v.replace("'createdAt':FieldValue.serverTimestamp()});", "'createdAt':FieldValue.serverTimestamp()}).timeout(const Duration(seconds:12));")
s=s[:start]+v+s[end:];s+='\n// Build441 child safety report\n';p.write_text(s)
p=Path('app/android/app/src/main/AndroidManifest.xml');s=p.read_text()
s=s.replace('android:name="android.hardware.camera" />','android:name="android.hardware.camera" android:required="false" />').replace('android:name="android.hardware.camera.autofocus" />','android:name="android.hardware.camera.autofocus" android:required="false" />');p.write_text(s)
