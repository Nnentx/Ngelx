#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN_PATH=ROOT/'app/lib/main.dart'
PUB_PATH=ROOT/'app/pubspec.yaml'

def one(text,old,new,label):
    n=text.count(old)
    if n!=1:
        raise SystemExit(f'Build 301 patch failed: {label}: expected 1 match, got {n}')
    return text.replace(old,new,1)

main=MAIN_PATH.read_text(encoding='utf-8')
pub=PUB_PATH.read_text(encoding='utf-8')
if 'version: 1.0.82+301' in pub:
    raise SystemExit('Build 301 already applied.')

# Ortak fotoğraf yükleyici: önce stream/dosya yolu, gerekirse bytes+PNG fallback.
anchor='\nFuture<void> ngelxMedyaSil(String rawUrl) async {'
if anchor not in main:
    raise SystemExit('Build 301 patch failed: photo helper anchor missing')
helper=r'''
Future<String> ngelxFotografYukle({
  required XFile dosya,
  required String kind,
  required String legacyPath,
  String? ext,
  void Function(int sent,int total)? onProgress,
}) async {
  final ad=dosya.name.trim();
  final hamExt=(ext??(ad.contains('.')?ad.split('.').last:'jpg')).toLowerCase();
  final temizExt=_ngelxUzantiTemizle(hamExt);
  final dogrudanUygun=const <String>{'jpg','jpeg','png','webp'}.contains(temizExt);
  Object? ilkHata;

  if(dogrudanUygun){
    try{
      return await ngelxMedyaYukleDosya(
        dosya:dosya,
        kind:kind,
        ext:temizExt,
        legacyPath:legacyPath,
        onProgress:onProgress,
      );
    }catch(e){
      ilkHata=e;
    }
  }

  try{
    final bytes=await dosya.readAsBytes();
    return await ngelxMedyaYukleBytes(
      bytes:bytes,
      kind:kind,
      ext:temizExt,
      legacyPath:legacyPath,
      onProgress:onProgress,
    );
  }catch(e){
    final ilk=ilkHata==null?'':(' | dosya: '+_ngelxKisaHata(ilkHata));
    throw Exception('Fotoğraf yüklenemedi'+ilk+' | fallback: '+_ngelxKisaHata(e));
  }
}

'''
main=main.replace(anchor,'\n'+helper+anchor.lstrip('\n'),1)

# Grup sohbet fotoğrafı.
main=one(main,
"""      final url=await ngelxMedyaYukleDosya(
        dosya:x,kind:'groups',ext:uzanti,legacyPath:yol,
        onProgress:(sent,total)=>_medyaIlerlemeGuncelle('Fotoğraf yükleniyor',sent,total),
      ).timeout(const Duration(seconds:75));""",
"""      final url=await ngelxFotografYukle(
        dosya:x,kind:'groups',ext:uzanti,legacyPath:yol,
        onProgress:(sent,total)=>_medyaIlerlemeGuncelle('Fotoğraf yükleniyor',sent,total),
      ).timeout(const Duration(seconds:90));""",
'group chat photo helper')

# Özel sohbet fotoğrafı.
main=one(main,
"""      final url=await ngelxMedyaYukleDosya(
        dosya:x,
        kind:'chats',
        ext:uzanti,
        legacyPath:yol,
      ).timeout(const Duration(seconds:75));""",
"""      final url=await ngelxFotografYukle(
        dosya:x,
        kind:'chats',
        ext:uzanti,
        legacyPath:yol,
      ).timeout(const Duration(seconds:90));""",
'private chat photo helper')

# Üret ekranındaki hikâye fotoğrafı.
main=one(main,
"""      final url=video
        ?await ngelxMedyaYukleDosya(dosya:dosya,kind:'stories',ext:uzanti,legacyPath:yol,onProgress:ilerleme)
        :await ngelxMedyaYukleBytes(bytes:await dosya.readAsBytes(),kind:'stories',ext:uzanti,legacyPath:yol,onProgress:ilerleme);""",
"""      final url=video
        ?await ngelxMedyaYukleDosya(dosya:dosya,kind:'stories',ext:uzanti,legacyPath:yol,onProgress:ilerleme)
        :await ngelxFotografYukle(dosya:dosya,kind:'stories',ext:uzanti,legacyPath:yol,onProgress:ilerleme);""",
'create story photo helper')

# Grup oluştururken seçilen fotoğraf.
main=one(main,
"""          final bytes=await foto!.readAsBytes().timeout(const Duration(seconds:8));
          final yol='groups/${u.uid}/${DateTime.now().millisecondsSinceEpoch}.jpg';
          fotoUrl=await ngelxMedyaYukleBytes(
            bytes: bytes,
            kind: 'groups',
            ext: 'jpg',
            legacyPath: yol,
          ).timeout(const Duration(seconds:75));""",
"""          final secilenFoto=foto!;
          final uzanti=secilenFoto.name.contains('.')?secilenFoto.name.split('.').last.toLowerCase():'jpg';
          final yol='groups/${u.uid}/${DateTime.now().millisecondsSinceEpoch}.$uzanti';
          fotoUrl=await ngelxFotografYukle(
            dosya:secilenFoto,
            kind:'groups',
            ext:uzanti,
            legacyPath:yol,
          ).timeout(const Duration(seconds:90));""",
'group creation photo helper')

# Grup avatarını değiştirme.
main=one(main,
"""      final url=await ngelxMedyaYukleBytes(bytes:await x.readAsBytes(),kind:'groups',ext:uzanti,legacyPath:yol);""",
"""      final url=await ngelxFotografYukle(dosya:x,kind:'groups',ext:uzanti,legacyPath:yol);""",
'group avatar photo helper')

# Grup sohbet arka planı.
main=one(main,
"""      final url=await ngelxMedyaYukleBytes(
        bytes:await x.readAsBytes(),kind:'chat-backgrounds',ext:ext,
        legacyPath:'chat-backgrounds/'+uid+'/'+widget.chatId+'_'+DateTime.now().millisecondsSinceEpoch.toString()+'.'+ext,
      );""",
"""      final url=await ngelxFotografYukle(
        dosya:x,kind:'chat-backgrounds',ext:ext,
        legacyPath:'chat-backgrounds/'+uid+'/'+widget.chatId+'_'+DateTime.now().millisecondsSinceEpoch.toString()+'.'+ext,
      );""",
'group background helper')

# Özel sohbet arka planı.
main=one(main,
"""      final url=await ngelxMedyaYukleBytes(
        bytes: await x.readAsBytes(),
        kind: 'chat-backgrounds',
        ext: 'jpg',
        legacyPath: yol,
      );""",
"""      final url=await ngelxFotografYukle(
        dosya:x,
        kind:'chat-backgrounds',
        ext:'jpg',
        legacyPath:yol,
      );""",
'private background helper')

# Destek ekran görüntüsü.
main=one(main,
"""if(ekran!=null){final yol='support/${u.uid}/${DateTime.now().millisecondsSinceEpoch}.jpg';ekranUrl=await ngelxMedyaYukleBytes(bytes:await ekran!.readAsBytes(),kind:'support',ext:'jpg',legacyPath:yol);}""",
"""if(ekran!=null){final yol='support/${u.uid}/${DateTime.now().millisecondsSinceEpoch}.jpg';ekranUrl=await ngelxFotografYukle(dosya:ekran!,kind:'support',ext:'jpg',legacyPath:yol);}""",
'support screenshot helper')

# Profil fotoğrafı.
main=one(main,
"""      final url = await ngelxMedyaYukleBytes(
        bytes: await dosya.readAsBytes(),
        kind: 'profiles',
        ext: uzanti,
        legacyPath: yol,
      );""",
"""      final url = await ngelxFotografYukle(
        dosya:dosya,
        kind:'profiles',
        ext:uzanti,
        legacyPath:yol,
      );""",
'profile photo helper')

# Profil ekranından hikâye paylaşımı.
main=one(main,
"""      final url=video
        ?await ngelxMedyaYukleDosya(
            dosya:dosya,kind:'stories',ext:uzanti,legacyPath:yol,
            contentType:uzanti=='mov'?'video/quicktime':null,
          )
        :await ngelxMedyaYukleBytes(
            bytes:await dosya.readAsBytes(),kind:'stories',ext:uzanti,legacyPath:yol,
          );""",
"""      final url=video
        ?await ngelxMedyaYukleDosya(
            dosya:dosya,kind:'stories',ext:uzanti,legacyPath:yol,
            contentType:uzanti=='mov'?'video/quicktime':null,
          )
        :await ngelxFotografYukle(
            dosya:dosya,kind:'stories',ext:uzanti,legacyPath:yol,
          );""",
'profile story photo helper')

# Sürüm.
main=one(main,"defaultValue: '1.0.81'","defaultValue: '1.0.82'",'runtime version')
main=one(main,"defaultValue: '300'","defaultValue: '301'",'runtime build')
MAIN_PATH.write_text(main,encoding='utf-8')

pub=one(pub,'version: 1.0.81+300','version: 1.0.82+301','pubspec version')
PUB_PATH.write_text(pub,encoding='utf-8')

# Eski regresyon testlerini yeni sürüme taşı.
for path in (ROOT/'tools').glob('verify_v*.py'):
    if path.name=='verify_v83_unified_photo_pipeline.py':
        continue
    t=path.read_text(encoding='utf-8')
    t=t.replace('version: 1.0.81+300','version: 1.0.82+301')
    t=t.replace("defaultValue: '1.0.81'","defaultValue: '1.0.82'")
    t=t.replace("defaultValue: '300'","defaultValue: '301'")
    t=t.replace('Build 300','Build 301')
    path.write_text(t,encoding='utf-8')

# V79 artık sohbet fotoğraflarında ortak fallback yardımcısını bekler.
v79=ROOT/'tools/verify_v79_photo_upload.py'
t=v79.read_text(encoding='utf-8')
t=t.replace('require("ngelxMedyaYukleDosya(" in group,"grup fotografi dosya/stream yukleme yolu")',
            'require("ngelxFotografYukle(" in group,"grup fotografi ortak fallback yukleme yolu")')
t=t.replace('require("ngelxMedyaYukleDosya(" in private,"ozel sohbet fotografi dosya/stream yukleme yolu")',
            'require("ngelxFotografYukle(" in private,"ozel sohbet fotografi ortak fallback yukleme yolu")')
v79.write_text(t,encoding='utf-8')

# V80 hikâye fotoğrafında ortak file+fallback hattını bekler.
v80=ROOT/'tools/verify_v80_critical_firebase.py'
t=v80.read_text(encoding='utf-8')
t=t.replace('require("ngelxMedyaYukleBytes(" in story,\n        "fotoğraf hikâyesinde güvenli PNG normalizasyonu")',
            'require("ngelxFotografYukle(" in story,\n        "fotoğraf hikâyesinde dosya+PNG fallback hattı")')
v80.write_text(t,encoding='utf-8')

print('Build 301 unified media patch prepared.')
