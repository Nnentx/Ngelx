from pathlib import Path
s=Path('app/lib/main.dart').read_text()
assert "'Okundu bilgisi'" not in s and "'Yazma göstergesi'" not in s
assert "'quickEmoji_$me':emoji" not in s
assert 'with Ngelx437MessageJump<SohbetPage>' in s
assert 'with Ngelx437MessageJump<GrupSohbetPage>' in s
assert "Navigator.pop(context,d.id)" in s
assert 'ngelx437SharedEmoji(veri)' in s and 'ngelx437SharedEmoji(mevcut)' in s
assert 'ngelx437ReceiptVisible(' in s and '_read437Written=stamp' in s
assert "'lastReadAt_$ben':stamp" in s
assert 'ngelx437TrimDownloads()' in s
assert 'initialize().timeout(const Duration(seconds:15))' in s
assert "defaultValue: '1.0.212'" in s and "defaultValue: '437'" in s
assert 'version: 1.0.212+437' in Path('app/pubspec.yaml').read_text()
print('Build437 source contracts passed; device results remain separate')
