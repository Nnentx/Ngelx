from pathlib import Path
import os,subprocess,tempfile
s=Path('app/lib/main.dart').read_text()
a=s.index('String _ngelx438Ui(String text)');b=s.index('// Build438 screen localization end',a)
a2=s.index('// Build439 extra locales')
code="class Language{String value='tr';} final uygulamaDili=Language(); const ceviriler=<String,Map<String,String>>{}; const _ngelx438ScreenTranslations=<String,Map<String,String>>{};\n"+s[a:b]+s[a2:]+'''
void main(){
 assert(_ngelx440Translations.length>60);
 for(final language in ['tr','en','de','ar','ru','ku','zh','hi','fr','es','it','pt']){
  uygulamaDili.value=language;
  for(final row in _ngelx440Translations.entries){
   assert(row.value.length==11);
   assert(row.value.values.every((text)=>text.trim().isNotEmpty));
   assert(_ngelx438Ui(row.key)==(language=='tr'?row.key:row.value[language]));
  }
 }
 print('Build440 presentation catalog: all rows in 12 languages passed.');
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d)/'locales.dart';p.write_text(code)
 subprocess.run([os.environ.get('NGELX_DART','dart'),'--enable-asserts',str(p)],check=True)
# Source integration: the actually rendered labels, not only a populated catalog.
assert 'Text(_ngelx438Ui(ad),maxLines:1' in s
assert 'Text(_ngelx438Ui(yazi),style:TextStyle(color:kategori==' in s
settings=Path('app/lib/build258_settings.dart').read_text()
assert '_ngelx438Ui(e.aciklama)' in settings
studio=Path('app/lib/live_broadcast_studio.dart').read_text()
assert '_ngelx438Ui("Canlı yayın hazırla")' in studio
assert '_ngelx438Ui("Yayın başlığı yaz")' in studio
print('Build440 inbox, Explore, settings and live-studio display integration passed.')

assert s.count('Text(_ngelx438Ui(ad),maxLines:1')==1, 'User names must not be localized'
