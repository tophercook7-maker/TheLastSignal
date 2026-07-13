# Answering the Dark — Store Submission Runbook

> **STATUS (2026-07-12): submission is already IN FLIGHT — this is not a from-scratch guide.**
> - **Apple:** app record created, build 1.0.0 uploaded, **submitted 07-11**, came back
>   "info needed", **replied 07-12 with a demo video → back in review.** Nothing to do but wait.
> - **Google Play:** store listing done; build in Internal testing; **app-content forms are
>   ~1 of 13 done** (privacy → content rating → target audience → data safety → etc.) + set price.
>   That's the real remaining work.
> - **Privacy URL already used in both filings:** `https://answering-the-dark-relay.fly.dev/privacy`
>   (the GitHub Pages one below is a redundant spare.)
>
> The steps below are the full reference; skip what's already done above.

Everything is built and staged. The remaining steps split into **things already
prepped** (below) and **account-gated clicks only you can do** (need your Apple /
Google logins).

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

## ✅ Both gaps now closed
1. **Privacy policy URL** — hosted via GitHub Pages from `docs/`:
   **https://tophercook7-maker.github.io/TheLastSignal/privacy.html**
   Paste this into both stores' privacy-policy field. (Give Pages a couple minutes to
   build after the first push.)
2. **Google phone screenshots** — regenerated at **1080×1920** (9:16, within Google's 2:1
   max) from the real game screens: `dist/play-assets/phone-1-lobby.png`,
   `phone-2-mission.png`, `phone-3-ending.png`. Upload these three.

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
- [x] Privacy policy hosted → https://tophercook7-maker.github.io/TheLastSignal/privacy.html
- [x] Google phone screenshots at 1080×1920 (`dist/play-assets/phone-*.png`)
- [ ] Apple: create record → upload build → submit  ← your login
- [ ] Google: create app → upload .aab → submit  ← your login
