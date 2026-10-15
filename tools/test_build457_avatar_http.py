import unittest
from apply_build457_avatar_http import (
    transform, START, END, ANCHOR, OLD_TRANSPORT, NEW_TRANSPORT, NO_CACHE,
)

class AvatarHttpFixTest(unittest.TestCase):
    def setUp(self):
        self.before = (
            ANCHOR + "\n"
            + "Future<Uint8List> _ngelxAgResmiBaytlari(String url) {\n"
            + "  return _ngelx456ImageRequests.putIfAbsent(url, ()=>Future.value(Uint8List(0)));\n}\n"
            + START + "\n"
            + "  Future<Response<List<int>>> indir(Uri uri,{String? token}) {\n"
            + OLD_TRANSPORT + "\n"
            + "      uri,options:Options(headers:<String,String>{\n"
            + NO_CACHE
            + "        if(token!=null)HttpHeaders.authorizationHeader:'Bearer $token',\n"
            + "      }),\n    );\n  }\n}\n" + END
        )

    def test_http_reuse_preserves_existing_dedup_and_token(self):
        after = transform(self.before)
        self.assertIn(NEW_TRANSPORT, after)
        self.assertNotIn(NO_CACHE, after)
        self.assertIn("_ngelx456ImageRequests.putIfAbsent(", after)
        self.assertIn("HttpHeaders.authorizationHeader", after)
        self.assertEqual(after.count("final Dio _ngelx457AvatarHttp"), 1)
        self.assertEqual(transform(after), after)

    def test_unsafe_source_drift_fails_closed(self):
        with self.assertRaises(AssertionError):
            transform(self.before.replace(NO_CACHE, ""))

if __name__ == "__main__":
    unittest.main()
