"""Extend the existing keyed UI catalog to twelve languages, preserving originals."""
import csv
import json
import re
from pathlib import Path

NEW = {'ku': 'Kurdî (Kurmancî)', 'zh': '中文（简体）', 'hi': 'हिन्दी',
       'fr': 'Français', 'es': 'Español', 'it': 'Italiano', 'pt': 'Português'}


def literal(value):
    return json.dumps(value, ensure_ascii=False).replace('$', r'\$')


def apply():
    rows = list(csv.DictReader(Path('tools/build438_locales.tsv').open(), delimiter='\t'))
    translations = {row['key']: row for row in rows}
    assert len(translations) == len(rows), 'Duplicate translation keys'
    assert all(set(row) == {'key', *NEW} and all(row.values()) for row in rows)
    p = Path('app/lib/main.dart')
    source = p.read_text()
    a = source.index('const ceviriler =')
    b = source.index('String t(String', a)
    catalog = source[a:b]
    pattern = r"^(\s*'([^']+)':\s*\{)(.*)(\},\s*)$"
    matches = list(re.finditer(pattern, catalog, re.M))
    assert {m[2] for m in matches} == set(translations), 'Catalog coverage changed'
    def extend(m):
        original = m[3]
        # Remove only our generated entries before reapplying.
        for code in NEW:
            original = re.sub(r',\s*"' + code + r'":\s*"(?:\\.|[^"\\])*"', '', original)
        extra = ''.join(', ' + literal(code) + ':' + literal(translations[m[2]][code]) for code in NEW)
        return m[1] + original + extra + m[4]
    source = source[:a] + re.sub(pattern, extend, catalog, flags=re.M) + source[b:]
    names = {'tr': 'Türkçe', 'en': 'English', 'de': 'Deutsch', 'ar': 'العربية', 'ru': 'Русский', **NEW}
    source = re.sub(r'const dilAdlari = .*?;', 'const dilAdlari = ' +
                    '{' + ','.join(literal(k)+':'+literal(v) for k,v in names.items()) + '};', source, count=1)
    marker = '  switch(uygulamaDili.value){'
    a = source.index('String lt(')
    b = source.index('String tercihBasligi', a)
    block = source[a:b]
    if 'Build438 catalog lookup' not in block:
        block = block.replace(marker, '''  // Build438 catalog lookup for newly supported languages.
  if(const {'ku','zh','hi','fr','es','it','pt'}.contains(uygulamaDili.value)){
    for(final entry in ceviriler.entries){
      if(entry.value['tr']==tr)return entry.value[uygulamaDili.value]??en;
    }
    return en;
  }
''' + marker)
        source = source[:a] + block + source[b:]
    # The animated welcome has its own split title, separate from t('welcome').
    a = source.index('class _NgelXRenkliBaslik')
    b = source.index('    final secili =', a)
    block = source[a:b]
    if "'ku': ['Bi xêr'" not in block:
        block = block.replace("      'ru': ['С', 'возвращением'],", """      'ru': ['С', 'возвращением'],
      'ku': ['Bi xêr', 'hatî dîsa'],
      'zh': ['欢迎', '回来'],
      'hi': ['फिर से', 'स्वागत है'],
      'fr': ['Bon', 'retour'],
      'es': ['Bienvenido', 'de nuevo'],
      'it': ['Bentornato', ''],
      'pt': ['Bem-vindo', 'de volta'],""")
        source = source[:a] + block + source[b:]
    # Firebase's built-in mail templates do not offer Kurmanci. Keep mail usable.
    source = source.replace('setLanguageCode(uygulamaDili.value)',
                            "setLanguageCode(uygulamaDili.value=='ku'?'en':uygulamaDili.value=='zh'?'zh-CN':uygulamaDili.value=='pt'?'pt-BR':uygulamaDili.value)")
    p.write_text(source)
    print(f'Existing catalog extended: {len(rows)} keys × {len(NEW)} new languages; 12 languages total.')


if __name__ == '__main__':
    apply()
