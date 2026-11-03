# Note App Galaxy Remote Control

Package: `com.notesvault.app.glxcodx`  
Store record: `000009374795`  
Public endpoint: https://raw.githubusercontent.com/metosapps/note-app-galaxy-config/main/config.json

This repository contains public configuration only. Never add credentials, signing material,
purchase receipts, user notes or Android source. Android 1.0.1 (2) embeds this endpoint and the
production AdMob App ID. Advertising and Samsung IAP sales start OFF. Real unit IDs stay blank
until this exact app is live and production enablement is explicitly authorized.

## Change Configuration

1. Edit `config.json`, keeping `schemaVersion`, `packageName`, `store`, and `ads.ids.admobAppId` unchanged.
2. Increment `version` for each edit and run `python3 validate.py`.
3. Commit and push `main`. Check the validation workflow and the public endpoint.
4. Check Settings > Diagnostics on the installed APK for `remote_config_refreshed` with the new version.

The app fetches on startup and while its activity is visible every 60 seconds (requests are
coalesced for 30 seconds). Requests use HTTPS, a minute cache key and a three-second socket timeout.
CDN propagation and connectivity can delay delivery. This is not an instantaneous push service.
Malformed/wrong-app responses preserve the last valid config. If no fresh fetch has succeeded
for six hours, cached ads and sales turn off on the next foreground refresh. Local notes and
owned entitlements are not deleted. Offline changes cannot arrive until connectivity returns.

## Advertising

The APK supports App Open, Interstitial and Native ads. Later, add this app's real IDs under
`ads.ids`, enable `ads.enabled` and the desired `ads.placements`, then set bounded frequencies.
For example: `maxAppOpensPerSession: 1`, `maxInterstitialsPerSession: 2`,
`nativeInListEveryN: 8`. Network remains `admob`.

Release uses production unit IDs; debug/staging always substitute official Google test IDs.
The client rejects other publishers' units and Google demo IDs in release. Consent eligibility,
Local Pro ownership, lock state, safe home state, fullscreen cooldown and the cancellable
"Showing ads..." notice cannot be bypassed by config. Configure AdMob Privacy & messaging,
app readiness, store linking and disclosures before enabling requests. Reserved banner/rewarded
fields do not create placements that are not implemented in the APK.

## Samsung IAP

Register `local_pro` on this exact Galaxy Store package as the lifetime ad-removal item. Keep its
ID stable after the first purchase. The SDK is already in production mode; never switch it remotely.
After seller product registration/approval and purchase/Restore QA, enable all three:
`monetization.premiumEnabled`, `paywallEnabled`, `samsungIapEnabled`. An actual Samsung product
with a store-provided price is required; a config flag or fallback label cannot authorize payment.
Restore remains available with new sales disabled. No purchase is performed by this repository.

## Other Controls

- `legal.*`, `support.*`: HTTPS policy/help links and app-specific email addresses.
- `updates.*`: minimum/latest version, correct Galaxy Store update URL, maintenance notice.
- `messaging.*`: optional home message and HTTPS link.
- `features.pdfExportEnabled`: existing PDF export gate. Other feature fields are reserved;
  they do not implement attachments, drawings, extra importers, AI or cloud sync.

Keep minimum version at 1 until a replacement build is actually live everywhere. Do not use
maintenance/update gates to hide functionality from review. New SDKs, native features, permissions,
manifest App IDs, signer or package changes still require a new reviewed APK.

## Emergency Off

Copy `rollback.json` to `config.json`, increase `version`, validate and push. It disables every ad
placement and new IAP sales without touching notes, legal/support links or owned entitlements.

Sources: [Google AdMob setup](https://developers.google.com/admob/android/quick-start),
[Samsung IAP integration](https://developer.samsung.com/codelab/iap/in-app-purchase.html).
