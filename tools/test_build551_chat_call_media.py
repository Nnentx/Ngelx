import os
import unittest
from pathlib import Path
from apply_build551_chat_call_media import main_source

class Regression551(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base=Path(os.environ.get('BUILD551_BASELINE','app/lib/main.dart')).read_text()
        cls.result=main_source(cls.base)
    def test_idempotent(self):
        self.assertEqual(main_source(self.result),self.result)
    def test_remote_photo_decode_and_upload_fallbacks_preserved(self):
        a=self.result.index('Future<String> _ngelxFotografYayininiDogrula(')
        b=self.result.index('bool _ngelxFotoKind(',a)
        aa=self.base.index('Future<String> _ngelxFotografYayininiDogrula(')
        bb=self.base.index('bool _ngelxFotoKind(',aa)
        self.assertEqual(self.result[a:b],self.base[aa:bb])
        for marker in ['_ngelxDirectR2BytesYukle(', '_ngelxStandartBytesYukle(', '_ngelxKucukMedyaYukleAndroid(']:
            self.assertEqual(self.result.count(marker),self.base.count(marker))
    def test_group_send_still_waits_for_authoritative_commit_and_preserves_retry(self):
        for marker in ['await ngelxBatchCommitDogrula(',"_grup463FotoDosya=x.path;",'_grup463FotoUrl=url;',"label:'Tekrar dene'"]:
            self.assertEqual(self.result.count(marker),self.base.count(marker))
    def test_no_new_backend_or_call_lifecycle_change(self):
        for start,end in [('  Future<void> aktifGrupAramasinaKatil(', '  Future<void>',),('  Future<void> bitir({bool geriDon=true})async{','  @override void dispose()')]:
            a=self.base.index(start);b=self.base.index(end,a+len(start))
            self.assertIn(self.base[a:b],self.result)
    def test_fail_closed_on_wrong_generation(self):
        with self.assertRaises((RuntimeError,ValueError)):main_source('wrong version')

if __name__=='__main__':unittest.main()
