from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
main_path=ROOT/'app/lib/main.dart'
pub_path=ROOT/'app/pubspec.yaml'

main=main_path.read_text(encoding='utf-8')
pub=pub_path.read_text(encoding='utf-8')

def rep(text,old,new,label):
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f'{label}: kaynak bulunamadi')
    return text.replace(old,new,1)

main=rep(main,"defaultValue: '1.0.127'","defaultValue: '1.0.128'",'version name')
main=rep(main,"defaultValue: '346'","defaultValue: '347'",'build number')
pub=rep(pub,'version: 1.0.127+346','version: 1.0.128+347','pubspec version')

main_path.write_text(main,encoding='utf-8')
pub_path.write_text(pub,encoding='utf-8')
print('Build 347 version applied')
