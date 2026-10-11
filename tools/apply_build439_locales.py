from pathlib import Path
import csv,json
from apply_build438_screen_locales import localize
rows=list(csv.DictReader(Path('tools/build439_locales.tsv').open(),delimiter='\t'))
assert all(len(r)==12 and all(r.values()) for r in rows)
extra={r['tr']:{k:v for k,v in r.items() if k!='tr'} for r in rows}
p=Path('app/lib/main.dart');s=p.read_text()
marker='// Build439 extra locales'
if marker not in s:
 s=s.replace("  final extra=_ngelx438ScreenTranslations[text]?[language];", "  final newer=_ngelx439Translations[text]?[language];\n  if(newer!=null)return newer;\n  final extra=_ngelx438ScreenTranslations[text]?[language];")
 s=s.replace("girisHatasi='Çok fazla hatalı deneme yapıldı. $saniye saniye sonra tekrar dene.'", "girisHatasi=_ngelx439Format('Çok fazla hatalı deneme yapıldı. {seconds} saniye sonra tekrar dene.',{'seconds':saniye})")
 s=s.replace("mesaj='E-posta veya şifre yanlış. ${5-deneme} deneme hakkın kaldı.'", "mesaj=_ngelx439Format('E-posta veya şifre yanlış. {attempts} deneme hakkın kaldı.',{'attempts':5-deneme})")
 s=s.replace('Text(girisHatasi!,','Text(_ngelx438Ui(girisHatasi!),')
 s=s.replace('Text(baslik,textAlign:TextAlign.center,','Text(_ngelx438Ui(baslik),textAlign:TextAlign.center,')
 s=s.replace('Text(aciklama,textAlign:TextAlign.center,','Text(_ngelx438Ui(aciklama),textAlign:TextAlign.center,')
 # Replace only strings displayed in UI, never account data or database values.
 start=s.index('class NgelXDogrulanmisOturumKapisi')
 head=s[:start];body,_=localize(s[start:],set(extra))
 s=head+body+'\n'+marker+'\nconst _ngelx439Translations = <String, Map<String,String>>'+json.dumps(extra,ensure_ascii=False)+';\n'
 s+='''\nString _ngelx439Format(String template,Map<String,Object> values){
  var text=_ngelx438Ui(template);
  for(final entry in values.entries){text=text.replaceAll('{'+entry.key+'}',entry.value.toString());}
  return text;
}
'''
 p.write_text(s)
 print(f'Added {len(rows)} complete 12-language error messages.')
