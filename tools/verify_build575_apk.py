"""Verify Build578 review APK identity, package content and absence of demo ad IDs.

Read-only local verifier. Does not sign, distribute, upload or update NgelX.
"""
import argparse
import hashlib
from pathlib import Path
import re
import subprocess
import sys
import zipfile

APP_ID = "com.nnentx.ngelx_app"
VERSION = "1.0.348"
BUILD = 578
# Google's published TEST IDs must never be in an APK offered as a review/release.
FORBIDDEN_BYTES = (
    b"ca-app-pub-3940256099942544",
    b"3940256099942544~3347511713",
    b"3940256099942544/5224354917",
)
REQUIRED = ("AndroidManifest.xml", "classes.dex")
ARCH_PREFIX = "lib/arm64-v8a/"


def verify_badging(text):
    """Inspect real Android resource-tool output, not an APK filename."""
    match = re.search(
        r"(?m)^package:\s+name='([^']+)'\s+versionCode='([^']+)'\s+versionName='([^']+)'",
        text,
    )
    if match is None:
        raise ValueError("APK has no readable Android package identity")
    app_id, build, version = match.groups()
    if (app_id, build, version) != (APP_ID, str(BUILD), VERSION):
        raise ValueError(f"Unexpected Android app identity: {app_id}, {version}, {build}")
    return {"package": app_id, "version": version, "build": int(build)}


def verify_archive(apk_path):
    """Stream all decompressed members, including native libraries, for test IDs."""
    path = Path(apk_path)
    if not path.is_file() or path.stat().st_size < 2048:
        raise ValueError("APK missing or implausibly small")
    archive_sha = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            archive_sha.update(chunk)
    try:
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
            if not set(REQUIRED).issubset(names):
                raise ValueError("APK missing mandatory Android manifest or DEX")
            if not any(name.startswith(ARCH_PREFIX) and name.endswith("/libapp.so")
                       for name in names):
                raise ValueError("APK missing ARM64 Flutter application")
            if any(name.startswith("lib/armeabi-v7a/") and name.endswith("/libapp.so")
                   for name in names):
                raise ValueError("Review APK unexpectedly contains 32-bit release target")
            for member in archive.infolist():
                if member.is_dir():
                    continue
                # Blocks patterns that overlap the 64-KiB streaming boundary.
                tail = b""
                with archive.open(member) as reader:
                    while True:
                        part = reader.read(65536)
                        if not part:
                            break
                        sample = tail + part
                        if any(token in sample for token in FORBIDDEN_BYTES):
                            raise ValueError("Google AdMob demo app/ad-unit ID found in review APK")
                        tail = sample[-96:]
            # CRC validation is included when each compressed member is consumed above.
    except zipfile.BadZipFile as exc:
        raise ValueError("Review APK is not a valid ZIP archive") from exc
    return {"size_bytes": path.stat().st_size, "sha256": archive_sha.hexdigest()}


def verify(apk_path, aapt_path):
    result = verify_archive(apk_path)
    completed = subprocess.run(
        [str(aapt_path), "dump", "badging", str(apk_path)],
        text=True, capture_output=True, check=False, timeout=35,
    )
    if completed.returncode != 0:
        raise ValueError("Android build tools could not inspect APK badging")
    result.update(verify_badging(completed.stdout))
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description="Read-only Build578 review APK verifier")
    parser.add_argument("apk", help="Path to locally built Build578 APK")
    parser.add_argument("--aapt", required=True, help="Path to Android build-tools aapt")
    args = parser.parse_args(argv)
    try:
        result = verify(args.apk, args.aapt)
    except (ValueError, OSError, subprocess.TimeoutExpired) as exc:
        print("Build578 APK verification FAILED: " + str(exc), file=sys.stderr)
        return 1
    print("Build578 review APK verification OK")
    for key in ("package", "version", "build", "size_bytes", "sha256"):
        print(f"{key}: {result[key]}")
    print("AdMob demo identifiers: absent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
