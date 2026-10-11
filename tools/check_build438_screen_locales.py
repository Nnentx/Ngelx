"""Compile production localization code and verify display/storage separation."""
import hashlib
import os
import subprocess
import tempfile
from pathlib import Path
from apply_build438_screen_locales import apply, localize

fixture="""const stored = {'audience':'Arkadaşlar', 'action':'Sil'};
final text = const Padding(child: Text('Arkadaşlar'));
final menu = const [Text(enabled ? 'Sil' : 'Kaydet')];
final mixed = Text('${user.name}');
"""
changed,count=localize(fixture,{'Arkadaşlar','Sil','Kaydet'})
assert count==3
assert "const stored = {'audience':'Arkadaşlar', 'action':'Sil'};" in changed
assert "const Padding" not in changed and 'const [' not in changed
assert "Text('${user.name}')" in changed
assert localize(changed,{'Arkadaşlar','Sil','Kaydet'})==(changed,0)
source=Path('app/lib/main.dart').read_text()
before={str(p):hashlib.sha256(p.read_bytes()).digest() for p in Path('app/lib').glob('*.dart')}
apply()
assert {str(p):hashlib.sha256(p.read_bytes()).digest() for p in Path('app/lib').glob('*.dart')}==before
assert 'const _NgelXRenkliBaslik()' not in source
assert "_oneCikan(Icons.add,_ngelx438Ui(\"Yeni\")" in source
assert "_ProfilSekme(_ngelx438Ui(\"Hikayeler\")" in source
assert "Text(_ngelx438Ui(\"Öne çıkan hikâyelerin burada görünecek\")" in source
settings=Path('app/lib/build258_settings.dart').read_text()
assert "bolum:'HESAP',baslik:'Hesap ve profil bilgileri'" in settings
assert "title:Text(_ngelx438Ui(e.baslik)" in settings
assert "${_ngelx438Ui(e.aciklama)} ${_ngelx438Ui(e.bolum)}').contains(q)" in settings
assert "onTap:()=>setState(()=>filtre=ad)" in source
assert "Text(_ngelx438Ui(ad),maxLines:1," in source
start=source.index('const dilAdlari =')
end=source.index('String tercihBasligi',start)
test='''
void main(){
  for(final language in dilAdlari.keys){
    uygulamaDili.value=language;
    for(final entry in _ngelx438ScreenTranslations.entries){
      assert(entry.value.length==11);
      assert(_ngelx438Ui(entry.key)==(language=='tr'?entry.key:entry.value[language]));
    }
    for(final entry in ceviriler.values){
      assert(_ngelx438Ui(entry['tr']!)==(entry.valueOrNull(language)));
    }
  }
  uygulamaDili.value='fr';
  assert(lt('Paylaş','Share')=='Partager');
  assert(lt('Bağlan','Connect')=='Se connecter');
  assert(_ngelx438Ui('Ayarlarda ara')=='Rechercher dans les paramètres');
  assert(_ngelx438Ui('Kapak Fotoğrafını\\nDeğiştir')=='Changer la photo\\nde couverture');
  uygulamaDili.value='ku';
  assert(_ngelx438Ui('Hikayeler')=='Çîrok');
  assert(_ngelx438Ui('Yeni')=='Nû');
  uygulamaDili.value='unknown';
  assert(_ngelx438Ui('Yeni')=='Yeni');
  assert(_ngelx438Ui('user-authored text')=='user-authored text');
  print('Screen strings: all 12 languages, fallback and display/storage isolation passed.');
}
extension CatalogExpected on Map<String,String>{
  String valueOrNull(String language)=>this[language]??this['tr']!;
}
'''
# Extra translations can override an original catalog synonym; compare against
# the exact screen override first, then the unchanged original catalog.
test=test.replace("(entry.valueOrNull(language))", "(_ngelx438ScreenTranslations[entry['tr']]?[language]??entry.valueOrNull(language))")
with tempfile.TemporaryDirectory() as directory:
    path=Path(directory)/'screen_catalog.dart'
    path.write_text('class Language {String value="tr";} final uygulamaDili=Language();\n'+source[start:end]+test)
    subprocess.run([os.environ.get('NGELX_DART','dart'),'--enable-asserts',str(path)],check=True)
