#!/usr/bin/env bash
# Validate + upload the iOS build to App Store Connect using the ASC API key.
# Run this AFTER the app record exists in App Store Connect (see SUBMISSION.md step A2).
#
# Identifiers come from the environment — nothing sensitive is hardcoded:
#   ASC_KEY_ID    App Store Connect API key id (e.g. from the Keys tab)
#   ASC_ISSUER_ID App Store Connect issuer id
#   ASC_KEY_PATH  path to the AuthKey_<id>.p8 file (default: ~/Downloads/AuthKey_<key id>.p8)
#
# Example:
#   ASC_KEY_ID=XXXXXXXXXX ASC_ISSUER_ID=xxxxxxxx-xxxx-... tools/upload_ios.sh
set -euo pipefail

cd "$(dirname "$0")/.."
IPA="dist/AnsweringTheDark-1.0.0.ipa"

: "${ASC_KEY_ID:?Set ASC_KEY_ID (App Store Connect API key id)}"
: "${ASC_ISSUER_ID:?Set ASC_ISSUER_ID (App Store Connect issuer id)}"
ASC_KEY_PATH="${ASC_KEY_PATH:-$HOME/Downloads/AuthKey_${ASC_KEY_ID}.p8}"

[ -f "$IPA" ] || { echo "Missing $IPA — build it first (npx tauri ios build)"; exit 1; }
[ -f "$ASC_KEY_PATH" ] || { echo "Missing API key at $ASC_KEY_PATH — set ASC_KEY_PATH"; exit 1; }

# altool searches ~/.appstoreconnect/private_keys for AuthKey_<id>.p8 — put it there.
KEYDIR="$HOME/.appstoreconnect/private_keys"
mkdir -p "$KEYDIR"
cp -f "$ASC_KEY_PATH" "$KEYDIR/AuthKey_${ASC_KEY_ID}.p8"

echo "==> Validating $IPA ..."
xcrun altool --validate-app -f "$IPA" -t ios \
  --apiKey "$ASC_KEY_ID" --apiIssuer "$ASC_ISSUER_ID"

echo "==> Uploading $IPA to App Store Connect ..."
xcrun altool --upload-app -f "$IPA" -t ios \
  --apiKey "$ASC_KEY_ID" --apiIssuer "$ASC_ISSUER_ID"

echo "==> Done. The build will appear in App Store Connect > TestFlight/Builds"
echo "    after processing (a few minutes). Then attach it to the version and submit."
