from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
main_path=ROOT/'app/lib/main.dart'
pub_path=ROOT/'app/pubspec.yaml'

def rep(text,old,new,label):
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f'{label}: kaynak bulunamadi')
    return text.replace(old,new,1)

main=main_path.read_text(encoding='utf-8')
pub=pub_path.read_text(encoding='utf-8')

main=rep(main,"defaultValue: '1.0.125'","defaultValue: '1.0.126'",'version name')
main=rep(main,"defaultValue: '344'","defaultValue: '345'",'build number')
pub=rep(pub,'version: 1.0.125+344','version: 1.0.126+345','pubspec version')

main_path.write_text(main,encoding='utf-8')
pub_path.write_text(pub,encoding='utf-8')
print('Build 345 version applied')
