"""Compile the real app catalog and exercise all languages without Firebase."""
import os
import subprocess
import tempfile
from pathlib import Path

source = Path('app/lib/main.dart').read_text()
a = source.index('const dilAdlari =')
b = source.index('String tercihBasligi', a)
test = '''
void main(){
  assert(dilAdlari.length==12);
  assert(ceviriler.length==259);
  for(final language in dilAdlari.keys){
    uygulamaDili.value=language;
    for(final entry in ceviriler.entries){
      assert(entry.value[language]!=null && entry.value[language]!.isNotEmpty);
      assert(t(entry.key)==entry.value[language]);
    }
  }
  uygulamaDili.value='zh';assert(t('login')=='登录');
  assert(lt('Giriş Yap','Sign in')=='登录');
  uygulamaDili.value='hi';assert(t('login')=='लॉग इन करें');
  uygulamaDili.value='ku';assert(t('login')=='Têkeve');
  uygulamaDili.value='unknown';assert(t('login')==ceviriler['login']!['tr']);
  assert(t('unknown-key')=='unknown-key');
  print('12 languages: 259 keys each; requested scripts and fallback passed.');
}
'''
with tempfile.TemporaryDirectory() as directory:
    path = Path(directory) / 'catalog.dart'
    path.write_text('class Language {String value="tr";} final uygulamaDili=Language();\n' + source[a:b] + test)
    subprocess.run([os.environ.get('NGELX_DART', 'dart'), '--enable-asserts', str(path)], check=True)
