import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
import zipfile

from tools.verify_build575_apk import verify_archive, verify_badging, verify


GOOD_BADGING = (
    "package: name='com.nnentx.ngelx_app' versionCode='577' "
    "versionName='1.0.347' platformBuildVersionName=''\n"
    "sdkVersion:'26'\n"
)


class VerifyBuild575ReviewTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.apk = Path(self.temp.name) / "Build575-REVIEW.apk"

    def make_archive(self, *, arm64=True, dex=True, sample=b"", arm32=False):
        with zipfile.ZipFile(self.apk, "w", compression=zipfile.ZIP_STORED) as out:
            out.writestr("AndroidManifest.xml", b"manifest" + b"x" * 3000)
            if dex:
                out.writestr("classes.dex", b"dex" + b"x" * 100)
            if arm64:
                out.writestr("lib/arm64-v8a/libapp.so", b"flutter64")
            if arm32:
                out.writestr("lib/armeabi-v7a/libapp.so", b"flutter32")
            out.writestr("assets/flutter_assets/asset.bin", sample)

    def test_valid_archive_and_badging(self):
        self.make_archive(sample=b"safe virtual Ludo rewards")
        meta = verify_archive(self.apk)
        self.assertGreater(meta["size_bytes"], 2048)
        self.assertEqual(len(meta["sha256"]), 64)
        self.assertEqual(verify_badging(GOOD_BADGING), {
            "package": "com.nnentx.ngelx_app", "version": "1.0.347", "build": 577
        })

    def test_wrong_package_version_or_build_cannot_pass(self):
        for bad in [
            GOOD_BADGING.replace("com.nnentx.ngelx_app", "com.example.fake"),
            GOOD_BADGING.replace("versionCode='577'", "versionCode='574'"),
            GOOD_BADGING.replace("versionName='1.0.347'", "versionName='1.0.344'"),
            "not an APK",
        ]:
            with self.subTest(value=bad):
                with self.assertRaises(ValueError):
                    verify_badging(bad)

    def test_demo_admob_id_rejected_even_across_chunk_boundary(self):
        test_id = b"ca-app-pub-3940256099942544"
        sample = b"a" * (65536 - 8) + test_id + b"b" * 100
        self.make_archive(sample=sample)
        with self.assertRaisesRegex(ValueError, "demo"):
            verify_archive(self.apk)

    def test_missing_flutter_or_dex_is_rejected(self):
        self.make_archive(arm64=False)
        with self.assertRaisesRegex(ValueError, "ARM64"):
            verify_archive(self.apk)
        self.make_archive(dex=False)
        with self.assertRaisesRegex(ValueError, "manifest or DEX"):
            verify_archive(self.apk)
        self.make_archive(arm32=True)
        with self.assertRaisesRegex(ValueError, "32-bit"):
            verify_archive(self.apk)

    def test_subprocess_error_fails_closed(self):
        self.make_archive()
        with patch("tools.verify_build575_apk.subprocess.run") as run:
            run.return_value.returncode = 1
            with self.assertRaisesRegex(ValueError, "Android build tools"):
                verify(self.apk, "/fake/aapt")

    def test_corrupt_apk_fails_closed(self):
        self.apk.write_bytes(b"no real APK" + b"x" * 4000)
        with self.assertRaisesRegex(ValueError, "ZIP"):
            verify_archive(self.apk)


if __name__ == "__main__":
    unittest.main()
