"""Apply the selected app language consistently before account emails."""
from pathlib import Path
p=Path('app/lib/main.dart');s=p.read_text()
if '// Build438 account email language' not in s:
    replacements={
      "      await widget.user.sendEmailVerification().timeout(const Duration(seconds:12));": "      // Build438 account email language\n      await FirebaseAuth.instance.setLanguageCode(uygulamaDili.value).timeout(const Duration(seconds:6));\n      await widget.user.sendEmailVerification().timeout(const Duration(seconds:12));",
      '      await yeni.sendEmailVerification();': '      await FirebaseAuth.instance.setLanguageCode(uygulamaDili.value).timeout(const Duration(seconds:6));\n      await yeni.sendEmailVerification().timeout(const Duration(seconds:12));',
      '      await FirebaseAuth.instance.sendPasswordResetEmail(email:u!.email!);': '      await FirebaseAuth.instance.setLanguageCode(uygulamaDili.value).timeout(const Duration(seconds:6));\n      await FirebaseAuth.instance.sendPasswordResetEmail(email:u!.email!).timeout(const Duration(seconds:20));',
      '      try{await FirebaseAuth.instance.setLanguageCode(uygulamaDili.value);}catch(_){}': '      await FirebaseAuth.instance.setLanguageCode(uygulamaDili.value).timeout(const Duration(seconds:6));',
    }
    for old,new in replacements.items():
        assert s.count(old)==1,old
        s=s.replace(old,new)
    p.write_text(s)
