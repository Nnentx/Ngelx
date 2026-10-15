#!/usr/bin/env bash
# Compatibility audit only. No deployment or writes to live Firestore.
# Run inside firebase emulators:exec with the candidate hardened rules loaded.
set -u
failed=0
for script in \
  tools/firestore_rules_test.mjs \
  tools/build450_rules_test.mjs \
  tools/build455_rules_test.mjs \
  tools/build456_rules_test.mjs \
  tools/build457_cover_rules_test.mjs
do
  echo "::group::Legacy Firestore regression: ${script}"
  node "${script}"
  code=$?
  if [ "${code}" -ne 0 ]; then
    echo "::error::Legacy rule regression failed: ${script} (exit ${code})"
    failed=1
  else
    echo "PASS: ${script}"
  fi
  echo "::endgroup::"
done
exit "${failed}"
