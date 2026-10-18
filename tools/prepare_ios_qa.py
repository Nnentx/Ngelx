#!/usr/bin/env python3
"""Prepare a generated Flutter iOS runner for unsigned NgelX simulator QA only.

Use AFTER: cd app && flutter create --platforms=ios --org com.nnentx --project-name ngelx_app .
No Apple signing, Firebase plist, APNs credentials, or TestFlight upload is performed.
"""
import argparse
import plistlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IOS = ROOT / "app" / "ios"
INFO = IOS / "Runner" / "Info.plist"
PODFILE = IOS / "Podfile"
XCODE = IOS / "Runner.xcodeproj" / "project.pbxproj"

PERMISSIONS = {
    "NSCameraUsageDescription": "NgelX goruntulu arama ve canli yayin icin kameraya erisim ister.",
    "NSMicrophoneUsageDescription": "NgelX sesli arama ve canli yayin icin mikrofona erisim ister.",
    "NSPhotoLibraryUsageDescription": "NgelX sohbet ve paylasimlarda fotograf ve video secmek icin galeri erisimi ister.",
    "NSPhotoLibraryAddUsageDescription": "NgelX secilen medyayi fotograflara kaydetmek icin izin ister.",
    "NSBluetoothAlwaysUsageDescription": "NgelX aramalarda Bluetooth ses cihazlariyla baglanti kurmak icin izin ister.",
}
DEFINITIONS = [
    "PERMISSION_CAMERA=1",
    "PERMISSION_MICROPHONE=1",
    "PERMISSION_PHOTOS=1",
    "PERMISSION_PHOTOS_ADD_ONLY=1",
    "PERMISSION_NOTIFICATIONS=1",
    "PERMISSION_BLUETOOTH=1",
]
MARKER = "# NGELX_IOS_QA_PERMISSION_DEFINITIONS"


def require_generated_runner():
    missing = [str(p.relative_to(ROOT)) for p in (INFO, PODFILE, XCODE) if not p.is_file()]
    if missing:
        raise SystemExit(
            "Missing generated iOS files: " + ", ".join(missing)
            + ". Run flutter create --platforms=ios in app/ on macOS first."
        )


def apply():
    require_generated_runner()
    with INFO.open("rb") as file:
        plist = plistlib.load(file)
    plist.update(PERMISSIONS)
    schemes = plist.setdefault("CFBundleURLTypes", [])
    if not any("ngelx" in entry.get("CFBundleURLSchemes", []) for entry in schemes):
        schemes.append({
            "CFBundleURLName": "com.nnentx.ngelx_app",
            "CFBundleURLSchemes": ["ngelx"],
        })
    with INFO.open("wb") as file:
        plistlib.dump(plist, file, sort_keys=False)

    pod = PODFILE.read_text(encoding="utf-8")
    platform_regex = r"(?m)^#?\s*platform :ios, ['\"][^'\"]+['\"]"
    if not re.search(platform_regex, pod):
        raise SystemExit("Generated Podfile has no recognizable iOS platform line.")
    pod = re.sub(platform_regex, "platform :ios, '15.0'", pod, count=1)
    anchor = "flutter_additional_ios_build_settings(target)"
    if MARKER not in pod:
        if anchor not in pod:
            raise SystemExit("Cannot locate Flutter CocoaPods post_install hook.")
        block = "\n".join([
            anchor,
            "    " + MARKER,
            "    target.build_configurations.each do |config|",
            "      config.build_settings['GCC_PREPROCESSOR_DEFINITIONS'] = [",
            "        '$(inherited)',",
            *["        '" + item + "'," for item in DEFINITIONS],
            "      ]",
            "      config.build_settings['IPHONEOS_DEPLOYMENT_TARGET'] = '15.0'",
            "    end",
        ])
        pod = pod.replace(anchor, block, 1)
    PODFILE.write_text(pod, encoding="utf-8")

    pbx = XCODE.read_text(encoding="utf-8")
    replacement, count = re.subn(
        r"IPHONEOS_DEPLOYMENT_TARGET = [0-9.]+;",
        "IPHONEOS_DEPLOYMENT_TARGET = 15.0;",
        pbx,
    )
    if not count:
        raise SystemExit("Xcode project has no deployment target to adjust.")
    XCODE.write_text(replacement, encoding="utf-8")
    print("NgelX iOS simulator-only QA permissions and minimum iOS 15.0 prepared.")
    check()


def check():
    require_generated_runner()
    with INFO.open("rb") as file:
        plist = plistlib.load(file)
    missing = [key for key in PERMISSIONS if not plist.get(key)]
    schemes = plist.get("CFBundleURLTypes", [])
    if not any("ngelx" in item.get("CFBundleURLSchemes", []) for item in schemes):
        missing.append("CFBundleURLSchemes: ngelx")
    pod = PODFILE.read_text(encoding="utf-8")
    if "platform :ios, '15.0'" not in pod:
        missing.append("Podfile iOS minimum 15.0")
    if MARKER not in pod or any(item not in pod for item in DEFINITIONS):
        missing.append("CocoaPods permission_handler macros")
    pbx = XCODE.read_text(encoding="utf-8")
    if "IPHONEOS_DEPLOYMENT_TARGET = 15.0;" not in pbx:
        missing.append("Xcode deployment target")
    if missing:
        raise SystemExit("iOS preflight incomplete: " + ", ".join(missing))
    print("iOS preflight static configuration PASS (NOT a signed IPA or device test).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--apply", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    apply() if args.apply else check()
