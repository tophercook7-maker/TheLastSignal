#!/usr/bin/env python3
"""Register com.tophercook.answeringthedark (iOS) + create an iOS App Store
provisioning profile via the App Store Connect API. Saves the profile to
~/Downloads/ and installs it for Xcode.

Usage:
  ASC_KEY_ID=<key id> ASC_ISSUER_ID=<uuid> ASC_KEY_PATH=~/Downloads/AuthKey_XXX.p8 \
    python3 tools/asc_provision_ios.py
Adapted from the Whispering Hollow MAS provisioner.
"""
import base64, json, os, sys, time, urllib.error, urllib.request
import jwt

# Account identifiers come from the environment — never hardcode them in a public repo.
KEY_ID = os.environ.get("ASC_KEY_ID")
ISSUER_ID = os.environ.get("ASC_ISSUER_ID")
KEY_PATH = os.path.expanduser(os.environ.get("ASC_KEY_PATH") or "~/Downloads/AuthKey.p8")
if not KEY_ID or not ISSUER_ID:
    sys.exit("Set ASC_KEY_ID and ASC_ISSUER_ID (and optionally ASC_KEY_PATH) in the environment.")

API = "https://api.appstoreconnect.apple.com"
BUNDLE_ID = "com.tophercook.answeringthedark"
APP_NAME = "Answering the Dark"
PROFILE_OUT = os.path.expanduser("~/Downloads/Answering_the_Dark_iOS.mobileprovision")


def token():
    with open(KEY_PATH) as f:
        key = f.read()
    now = int(time.time())
    return jwt.encode(
        {"iss": ISSUER_ID, "iat": now, "exp": now + 1200, "aud": "appstoreconnect-v1"},
        key, algorithm="ES256", headers={"kid": KEY_ID})


def api(method, path, body=None):
    url = path if path.startswith("http") else API + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token()}")
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{method} {path} -> {e.code}: {e.read().decode()[:600]}") from e


def find_or_register_bundle_id():
    r = api("GET", f"/v1/bundleIds?filter[identifier]={BUNDLE_ID}")
    for item in r.get("data", []):
        if item["attributes"]["identifier"] == BUNDLE_ID:
            print(f"bundle id exists: {item['id']}")
            return item["id"]
    r = api("POST", "/v1/bundleIds", {
        "data": {"type": "bundleIds", "attributes": {
            "identifier": BUNDLE_ID, "name": APP_NAME.replace(" ", ""), "platform": "IOS"}}})
    print(f"bundle id registered (iOS): {r['data']['id']}")
    return r["data"]["id"]


def distribution_cert_ids():
    r = api("GET", "/v1/certificates?filter[certificateType]=IOS_DISTRIBUTION,DISTRIBUTION&limit=50")
    ids = []
    for c in r.get("data", []):
        a = c["attributes"]
        print(f"cert: {a['certificateType']} {a['displayName']} expires {a['expirationDate'][:10]}")
        ids.append(c["id"])
    return ids


def create_profile(bundle_ref, cert_ids):
    name = f"{APP_NAME} AppStore"
    q = name.replace(" ", "%20")
    r = api("GET", f"/v1/profiles?filter[name]={q}&limit=5")
    for p in r.get("data", []):
        api("DELETE", f"/v1/profiles/{p['id']}")
        print(f"deleted old profile {p['id']}")
    r = api("POST", "/v1/profiles", {
        "data": {"type": "profiles",
                 "attributes": {"name": name, "profileType": "IOS_APP_STORE"},
                 "relationships": {
                     "bundleId": {"data": {"type": "bundleIds", "id": bundle_ref}},
                     "certificates": {"data": [{"type": "certificates", "id": i} for i in cert_ids]}}}})
    content = r["data"]["attributes"]["profileContent"]
    with open(PROFILE_OUT, "wb") as f:
        f.write(base64.b64decode(content))
    print(f"profile saved: {PROFILE_OUT} ({r['data']['attributes']['profileState']})")
    # install for Xcode
    dest_dir = os.path.expanduser("~/Library/MobileDevice/Provisioning Profiles")
    os.makedirs(dest_dir, exist_ok=True)
    uuid = r["data"]["attributes"].get("uuid", "answering-the-dark")
    dest = os.path.join(dest_dir, f"{uuid}.mobileprovision")
    with open(dest, "wb") as f:
        f.write(base64.b64decode(content))
    print(f"installed for Xcode: {dest}")


def main():
    bid = find_or_register_bundle_id()
    certs = distribution_cert_ids()
    if not certs:
        sys.exit("No iOS distribution certificates found via API")
    create_profile(bid, certs)


if __name__ == "__main__":
    main()
