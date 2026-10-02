#!/usr/bin/env bash
set -euo pipefail

PUB_CACHE_DIR="${PUB_CACHE:-$HOME/.pub-cache}"
BANUBA_GRADLE="$(find "$PUB_CACHE_DIR" -type f -path '*/banuba_sdk-*/android/build.gradle' | sort | tail -n 1)"

if [[ -z "$BANUBA_GRADLE" || ! -f "$BANUBA_GRADLE" ]]; then
  echo "banuba_sdk android/build.gradle bulunamadi." >&2
  exit 1
fi

echo "Banuba Gradle dosyasi: $BANUBA_GRADLE"

python3 - "$BANUBA_GRADLE" <<'PY'
from pathlib import Path
import re
import sys

path = Path(sys.argv[1])
text = path.read_text()
patched, count = re.subn(r'compileSdkVersion\s+31\b', 'compileSdkVersion 36', text)
if count == 0 and 'compileSdkVersion 36' not in text:
    raise SystemExit('Banuba compileSdkVersion 31 kalibi bulunamadi.')
path.write_text(patched)
PY

grep -q 'compileSdkVersion 36' "$BANUBA_GRADLE"
echo "banuba_sdk compileSdkVersion 36 olarak yamalandi."
