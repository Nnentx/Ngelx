"""Localize presentation literals only; leave stored values and route IDs intact."""
import csv
import json
import re
from pathlib import Path

LANGUAGES = {'tr','en','de','ar','ru','ku','zh','hi','fr','es','it','pt'}
START = '// Build438 screen localization begin'
END = '// Build438 screen localization end'


def tokens(source):
    result = []
    n = len(source)
    def string_end(i, raw=False):
        quote = source[i]
        triple = source.startswith(quote * 3, i)
        delimiter = quote * (3 if triple else 1)
        j = i + len(delimiter)
        while j < n:
            if source.startswith(delimiter, j):
                return j + len(delimiter)
            if not raw and source[j] == '\\':
                j += 2
            elif not raw and source.startswith('${', j):
                depth = 1
                j += 2
                while j < n and depth:
                    if source[j] in "'\"":
                        j = string_end(j)
                    elif source[j] == '{':
                        depth += 1; j += 1
                    elif source[j] == '}':
                        depth -= 1; j += 1
                    else:
                        j += 1
            else:
                j += 1
        raise AssertionError('Unterminated string')
    i = 0
    while i < n:
        if source[i].isspace():
            i += 1; continue
        if source.startswith('//',i):
            e = source.find('\n',i); i = n if e < 0 else e + 1; continue
        if source.startswith('/*',i):
            depth=1; i+=2
            while depth and i<n:
                if source.startswith('/*',i): depth+=1; i+=2
                elif source.startswith('*/',i): depth-=1; i+=2
                else: i+=1
            continue
        raw = source[i]=='r' and i+1<n and source[i+1] in "'\""
        if raw or source[i] in "'\"":
            j=string_end(i+1 if raw else i,raw)
        elif source[i].isalpha() or source[i]=='_':
            j=i+1
            while j<n and (source[j].isalnum() or source[j]=='_'): j+=1
        else:
            j=i+1
        result.append((source[i:j],i,j)); i=j
    return result


def literal(value):
    return json.dumps(value,ensure_ascii=False).replace('$',r'\$')


def localize(source, mapping):
    ts=tokens(source)
    stack=[]; pairs={}
    for i,(token,_,_) in enumerate(ts):
        if token in ('(','[','{'): stack.append(i)
        elif token in (')',']','}'):
            assert stack, f'Unbalanced source near {ts[i][1]}'
            a=stack.pop()
            assert {'(':')','[':']','{':'}'}[ts[a][0]]==token
            pairs[a]=i
    assert not stack
    display=set()
    # Text data, including ternary branches; never touch interpolated user data.
    for i,(token,_,_) in enumerate(ts[:-1]):
        if token=='Text' and ts[i+1][0]=='(':
            j=i+2
            while j<pairs[i+1] and ts[j][0]!=',':
                if ts[j][0] in ('(','[','{'):
                    j=pairs[j]+1; continue
                display.add(j); j+=1
        if token in {'hintText','labelText','tooltip','semanticLabel','yazi'} and ts[i+1][0]==':':
            display.add(i+2)
        # These helper arguments are presentation text, not database values.
        if token in {'_ProfilSekme','_oneCikan'} and ts[i+1][0]=='(':
            j=i+2
            while j<pairs[i+1]:
                if ts[j][0] in ('(','[','{'):
                    j=pairs[j]+1; continue
                display.add(j); j+=1
    replacements=[]
    for i in sorted(display):
        token,a,b=ts[i]
        if len(token)<2 or token[0] not in "'\"" or '$' in token: continue
        value=token[1:-1].replace('\\n','\n').replace("\\'", "'").replace('\\"','"')
        if value in mapping:
            replacements.append((a,b,'_ngelx438Ui('+literal(value)+')'))
    # Remove const only from expressions now containing a runtime translation.
    positions=[a for a,_,_ in replacements]
    for i,(token,a,b) in enumerate(ts):
        if token!='const': continue
        j=i+1
        while j<len(ts) and ts[j][0] not in ('(','[','{',';', '=',',',')',']','}'):
            j+=1
        if j in pairs and any(ts[j][1]<p<ts[pairs[j]][2] for p in positions):
            replacements.append((a,b,''))
    for a,b,value in sorted(replacements,reverse=True): source=source[:a]+value+source[b:]
    return source,len(positions)


def apply():
    rows=list(csv.DictReader(Path('tools/build438_screen_locales.tsv').open(),delimiter='\t'))
    rows=[{k:v.replace(r'\n','\n') for k,v in row.items()} for row in rows]
    assert rows and all(set(row)==LANGUAGES and all(row.values()) for row in rows)
    assert len({row['tr'] for row in rows})==len(rows)
    path=Path('app/lib/main.dart'); source=path.read_text()
    a=source.index('const ceviriler ='); b=source.index('String t(String',a)
    catalog=source[a:b]
    known=set(re.findall(r"'tr'\s*:\s*'((?:\\.|[^'\\])*)'",catalog))
    known={v.replace("\\'", "'").replace('\\n','\n') for v in known}
    mapping=known|{r['tr'] for r in rows}
    aliases={'Şikayet et':'Şikâyet et','Engellemeyi Kaldır':'Engellemeyi kaldır'}
    rows.extend([{**next(r for r in rows if r['tr']==target),'tr':name} for name,target in aliases.items()])
    mapping.update(aliases)
    # Avoid touching catalog definitions and localization helpers themselves.
    body_start=source.index('String tercihBasligi',b)
    head=source[:body_start]; body,count=localize(source[body_start:],mapping)
    # The welcome widget previously stayed const when the language changed.
    body=body.replace('const _NgelXRenkliBaslik()', '_NgelXRenkliBaslik()')
    data={r['tr']:{k:v for k,v in r.items() if k!='tr'} for r in rows}
    extra=START+'\nconst _ngelx438ScreenTranslations = <String, Map<String,String>>'+literal(data)+';\n'+'''String _ngelx438Ui(String text){
  final language=uygulamaDili.value;
  if(language=='tr')return text;
  final extra=_ngelx438ScreenTranslations[text]?[language];
  if(extra!=null)return extra;
  for(final entry in ceviriler.values){
    if(entry['tr']==text)return entry[language]??text;
  }
  return text;
}
'''+END+'\n\n'
    if START in head:
        x=head.index(START); y=head.index(END,x)+len(END)
        head=head[:x]+head[y:].lstrip('\n')
    marker='String lt(String tr,String en,{String? de,String? ar,String? ru}){'
    if '// Build438 extra inline translations' not in head:
        head=head.replace(marker,marker+'''
  // Build438 extra inline translations
  final screen=_ngelx438ScreenTranslations[tr]?[uygulamaDili.value];
  if(screen!=null)return screen;
''',1)
    # Inbox tab IDs continue to control filters; translate their label only.
    x=body.index('    Widget sekme(String ad,int sayi){')
    y=body.index('\n    Widget ',x+20)
    block=body[x:y].replace('Text(ad,maxLines:1,','Text(_ngelx438Ui(ad),maxLines:1,')
    body=body[:x]+block+body[y:]
    path.write_text(head+extra+body)
    for part in Path('app/lib').glob('*.dart'):
        if not part.read_text().startswith("part of 'main.dart';"): continue
        text=part.read_text()
        if part.name=='build258_settings.dart':
            text=text.replace('Text(x,style:', 'Text(_ngelx438Ui(x),style:')
            text=text.replace('Text(e.baslik,style:', 'Text(_ngelx438Ui(e.baslik),style:')
            text=text.replace("aramaSonucu?'${e.bolum} • ${e.aciklama}':e.aciklama,",
                              "aramaSonucu?'${_ngelx438Ui(e.bolum)} • ${_ngelx438Ui(e.aciklama)}':_ngelx438Ui(e.aciklama),")
            text=text.replace("${e.anahtarlar} ${e.bolum}').contains(q)",
                              "${e.anahtarlar} ${e.bolum} ${_ngelx438Ui(e.baslik)} ${_ngelx438Ui(e.aciklama)} ${_ngelx438Ui(e.bolum)}').contains(q)")
            text=text.replace('title:Text(_baslik)', 'title:Text(_ngelx438Ui(_baslik))')
        text,part_count=localize(text,mapping)
        part.write_text(text)
        count+=part_count
    print(f'Localized {count} presentation literals; {len(rows)} additional complete 12-language rows.')


if __name__=='__main__': apply()
