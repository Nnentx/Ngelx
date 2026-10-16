"""Fail-closed tests for Build465 stalled-inbox self-recovery."""
import unittest
from apply_build465_inbox_recovery import transform, OLD

def generated():
    return (
        "class _MesajPageState extends State<MesajPage> {\n"
        "  String? get uid=>FirebaseAuth.instance.currentUser?.uid;\n"
        "  final _profiles453={};\n"
        "  Widget build(){return StreamBuilder(stream:_profiles453.putIfAbsent(other,()=>stream),builder:(_,u){\n"
        + OLD +
        "\n final p=u.data?.data()??{}; });}\n"
        "  @override void dispose(){sohbetAra.dispose();super.dispose();}\n"
        "}\nclass ArsivSohbetlerPage {}\n"
    )

class Build465InboxRecoveryTests(unittest.TestCase):
    def test_auto_retry_then_manual_fallback(self):
        updated=transform(generated())
        self.assertIn("Duration(seconds:5*(retry+1))",updated)
        self.assertIn("_ngelx465ProfileRetryCount[target]=retry+1",updated)
        self.assertIn("Kişi bilgisi alınamadı",updated)
        self.assertIn("_ngelx465RetryProfileNow(other)",updated)
        self.assertIn("FirebaseAuth.instance.currentUser?.uid!=account",updated)
        self.assertIn("_profiles453.remove(target)",updated)
        self.assertEqual(updated,transform(updated))
    def test_missing_original_guard_fails_closed(self):
        with self.assertRaises(RuntimeError):
            transform(generated().replace("Kişi bilgisi yükleniyor…","Bekle"))

if __name__=="__main__":unittest.main()
