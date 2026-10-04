from pathlib import Path
p=Path("app/lib/main.dart")
s=p.read_text(encoding="utf-8")
needle="\\{"
# Avoid embedding a Dart interpolation token literally in this helper source.
bad="\\"+chr(36)+"{"
good=chr(36)+"{"
count=s.count(bad)
if count!=2:
    raise SystemExit(f"expected 2 escaped Dart interpolations, found {count}")
s=s.replace(bad,good)
p.write_text(s,encoding="utf-8")
print("Fixed escaped Dart interpolation in interaction detail subtitle.")
