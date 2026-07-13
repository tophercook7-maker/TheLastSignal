# Answering the Dark — Store Submission Runbook

Everything is built and staged. The remaining steps split into **things I already
prepped** (below) and **account-gated clicks only you can do** (need your Apple /
Google logins). Follow this top to bottom.

App: **Answering the Dark** · bundle `com.tophercook.answeringthedark` · v1.0.0 · Paid **$2.99**

---

## ✅ Ready in `dist/` (nothing to rebuild)
| File | Store |
|---|---|
| `AnsweringTheDark-1.0.0.ipa` | Apple App Store |
| `AnsweringTheDark-1.0.0.aab` | Google Play (upload this) |
| `AnsweringTheDark-1.0.0.apk` | sideload/testing only |
| `AnsweringTheDark-1.0.0.dmg` | Mac (optional / direct) |

Screenshots ready:
- iPhone 6.7" (1284×2778): `dist/apple-screens/` — 3 shots
- iPad 12.9" (2048×2732): `dist/ipad-screens/` — 3 shots
- Google feature graphic `dist/play-assets/feature-1024x500.png` + icon `icon-512.png`

Metadata (copy-paste ready): `STORE_LISTING.md`

---

## ⚠️ Two gaps to close before/at submit
1. **Privacy policy URL** — both stores require a *public* URL. `PRIVACY.md` is written
   but not hosted. Fastest: enable GitHub Pages on this repo and link the rendered file,
   or drop it on one of your sites. (Say the word and I'll wire GitHub Pages.)
2. **Google phone screenshots are low-res** (756×469). They pass Google's 320px minimum
   but look weak. Better to regenerate at 1080×1920 from the running app — I can script
   that with headless Chrome when you want.

---

## A. Apple — App Store Connect  🔑 (your login)
1. appstoreconnect.apple.com → **My Apps → +  → New App**
   - Platform iOS · Name **Answering the Dark** · Primary language English (U.S.)
   - Bundle ID `com.tophercook.answeringthedark` (already registered) · SKU `answeringthedark`
2. **Pricing** → Paid → **$2.99** tier.
3. **App Information** → Category **Games/Adventure** · Age rating **9+** (answer the
   questionnaire: no violence/gore/profanity → mild/infrequent sci-fi peril only).
4. Version page → paste **subtitle, description, keywords, promo** from `STORE_LISTING.md`;
   upload the 6.7" + iPad 12.9" screenshots; set the **privacy policy URL** (gap #1).
5. **Upload the build** (I prepped this — build record must exist first):
   ```bash
   cd ~/Games/TheLastSignal
   ASC_KEY_ID=<your key id> ASC_ISSUER_ID=<your issuer id> tools/upload_ios.sh
   ```
   (Key id + issuer are in `SHIPPING.md`; the `.p8` is in `~/Downloads/`.)
6. After it finishes processing (~few min), on the version page select the build →
   **Add for Review → Submit**.

## B. Google — Play Console  🔑 (your login)
1. play.google.com/console → **Create app** → Answering the Dark · Game · Paid.
2. Set **price $2.99** (Monetization → set up).
3. **Store listing**: paste short/full description from `STORE_LISTING.md`; upload
   `dist/play-assets/feature-1024x500.png`, `icon-512.png`, and phone screenshots (gap #2).
4. **Content rating** questionnaire (no violence/language → Everyone), **Data safety**
   (no data collected; relay only fans out room-coded game messages), **privacy URL** (gap #1).
5. **Production → Create release** → upload `dist/AnsweringTheDark-1.0.0.aab` → review → **roll out**.

## C. Multiplayer relay — already LIVE ✅
`wss://answering-the-dark-relay.fly.dev` (Fly.io, verified). Solo play works fully offline;
share-code co-op uses this relay. Nothing to do unless it needs redeploy:
`cd server && fly deploy`.

---

## Quick status
- [x] Three-act game built · Tauri shell · icons
- [x] Signed artifacts (ipa/aab/apk/dmg)
- [x] Apple + iPad screenshots · Google feature graphic + icon
- [x] Listing copy · privacy policy text · upload script
- [x] Relay live
- [ ] Privacy policy hosted at a public URL  ← gap #1
- [ ] Google phone screenshots at 1080×1920  ← gap #2 (optional polish)
- [ ] Apple: create record → upload build → submit  ← your login
- [ ] Google: create app → upload .aab → submit  ← your login
