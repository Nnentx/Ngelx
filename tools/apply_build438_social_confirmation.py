"""Apply after the Build438 phone and pending-request patches."""
from pathlib import Path

p = Path('app/lib/main.dart')
s = p.read_text()
if 'final commit438=' not in s:
    start = s.index('Future<bool> sosyalIstekGonder({')
    end = s.index('\nFuture', start + 1)
    part = s[start:end]
    old = 'return await firestore.runTransaction<bool>((tx)async{'
    assert part.count(old) == 1
    part = part.replace(old, 'final commit438=firestore.runTransaction<bool>((tx)async{')
    old = '    }).timeout(const Duration(seconds:12));'
    assert part.count(old) == 1
    part = part.replace(old, """    });
    return await ngelx438AwaitRequest(commit438,()async{
      final confirmed438=await istekRef.get(const GetOptions(source:Source.server))
        .timeout(const Duration(seconds:6));
      final data438=confirmed438.data();
      return data438?['status']=='pending'
        && data438?['requestGeneration']==istekNesli
        && data438?['notificationId']==bildirimRef.id;
    });""")
    s = s[:start] + part + s[end:]
    helper = Path('tools/build438_request_confirmation.dart').read_text()
    s += '\n' + helper.replace("import 'dart:async';\n", '')
    s = s.replace('Takip isteği zaman aşımına uğradı. Tekrar dene.', 'Takip isteğinin sonucu henüz doğrulanamadı. Bağlantını kontrol edip istek durumuna tekrar bak.')
    s = s.replace('Arkadaşlık isteği zaman aşımına uğradı. Tekrar dene.', 'Arkadaşlık isteğinin sonucu henüz doğrulanamadı. Bağlantını kontrol edip istek durumuna tekrar bak.')
    s = s.replace('Takip isteği için güncel Firestore kuralları gerekli.', 'Takip isteği için işlem izni reddedildi (permission-denied).')
    s = s.replace('Arkadaşlık isteği için güncel Firestore kuralları gerekli.', 'Arkadaşlık isteği için işlem izni reddedildi (permission-denied).')
    p.write_text(s)
