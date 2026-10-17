"""Build473: the permission fix must apply to BOTH old and generated community
handlers, must be idempotent, and must never change other error paths.
"""
import unittest
from pathlib import Path
from apply_build473_community_permission_reporting import patch_community, HEADER, MARKER

TARGET=Path('app/lib/community450.dart')

class CommunityPermission473Tests(unittest.TestCase):
    def test_existing_and_generated_handler_are_supported(self):
        for body in (
            "  if(c.mounted) ScaffoldMessenger.of(c).showSnackBar(SnackBar(content:Text(_ngelxKisaHata(e))));",
            "  if(c.mounted) ngelxDurumMesaji(c, ngelxMedyaHataMetni(e));",
        ):
            src="part of 'main.dart';\n"+HEADER+"\n"+body+"\n}\n\nWidget _communityImage450(String u)=>const SizedBox();\n"
            updated=patch_community(src)
            self.assertIn(MARKER,updated)
            self.assertIn("e.code == 'permission-denied'",updated)
            self.assertIn(body,updated)
            self.assertEqual(patch_community(updated),updated)
            self.assertEqual(updated.count(HEADER),1)
            self.assertEqual(updated.count("Widget _communityImage450"),1)

    def test_real_generated_handler_enriched_without_risk(self):
        src=TARGET.read_text(encoding='utf-8')
        self.assertIn(MARKER,src)
        self.assertIn('Kurucu/yönetici yetkisi ve canlı Firebase güvenlik kuralları',src)
        self.assertIn('return;',src[src.index(MARKER):src.index('Widget _communityImage450',src.index(MARKER))])
        self.assertEqual(patch_community(src),src)
        self.assertEqual(src.count(HEADER),1)

if __name__=='__main__':
    unittest.main()
