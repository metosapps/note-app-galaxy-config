"""Validate public configuration before publishing it to Note App."""
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

APP = "com.notesvault.app.glxcodx"
APP_ID = "ca-app-pub-4755121575074602~5178858728"
ROOT = Path(__file__).resolve().parent


def validate(path):
    raw = path.read_bytes()
    assert len(raw) <= 65536
    data = json.loads(raw)
    assert data["schemaVersion"] == 1
    assert data["packageName"] == APP and data["store"] == "galaxy_store"
    assert type(data["version"]) is int and data["version"] >= 1
    ads = data["ads"]
    assert ads["network"] == "admob" and ads["ids"]["admobAppId"] == APP_ID
    for value in ads["ids"].values():
        assert value == APP_ID or not value or re.fullmatch(r"ca-app-pub-4755121575074602/[0-9]{10}", value)
    for group, names in {
        "legal": ["privacyPolicyUrl", "termsUrl"],
        "support": ["websiteUrl", "helpUrl", "galaxyStoreUrl"],
        "updates": ["updateUrl"], "messaging": ["homePromoUrl"],
    }.items():
        for name in names:
            value = data[group][name]
            parsed = urlsplit(value)
            assert not value or (parsed.scheme == "https" and parsed.hostname and not parsed.username), name
    for name in ["supportEmail", "privacyEmail"]:
        assert re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", data["support"][name])
    frequencies = ads["frequency"]
    assert 0 <= frequencies["maxAppOpensPerSession"] <= 2
    assert 0 <= frequencies["maxInterstitialsPerSession"] <= 3
    assert 120 <= frequencies["minFullscreenIntervalSeconds"] <= 3600
    assert 30 <= frequencies["minBackgroundSeconds"] <= 3600
    assert 4 <= frequencies["interstitialEveryNTransitions"] <= 100
    assert 1000 <= frequencies["interstitialNoticeMillis"] <= 3000
    assert frequencies["nativeInListEveryN"] == 0 or frequencies["nativeInListEveryN"] >= 6
    if ads["enabled"]:
        for placement, unit, frequency in [
            ("appOpen", "appOpenUnitId", "maxAppOpensPerSession"),
            ("interstitial", "interstitialUnitId", "maxInterstitialsPerSession"),
            ("nativeInList", "nativeUnitId", "nativeInListEveryN"),
        ]:
            if ads["placements"][placement]:
                assert ads["ids"][unit] and frequencies[frequency] > 0, placement
    assert not any(ads["placements"][key] for key in ["homeBanner", "editorBanner", "backupInterstitial"])
    assert not any(data["features"][key] for key in [
        "attachmentsEnabled", "drawingsEnabled", "importersEnabled", "tasksViewEnabled",
        "analyticsEnabled", "crashReportingEnabled", "aiEnabled",
    ])
    local_pro = data["monetization"]["localPro"]
    assert local_pro["appProductId"] == "local_pro"
    assert re.fullmatch(r"[A-Za-z0-9._-]{1,128}", local_pro["samsungProductId"])
    assert data["updates"]["minSupportedVersionCode"] >= 1
    assert data["updates"]["softUpdateVersionCode"] >= data["updates"]["minSupportedVersionCode"]
    assert data["updates"]["minSupportedVersionCode"] <= 1 or data["updates"]["updateUrl"]
    print(f"PASS {path.name}: {APP}, revision {data['version']}, ads={ads['enabled']}, IAP={data['monetization']['samsungIapEnabled']}")


if __name__ == "__main__":
    for filename in ["config.json", "rollback.json"]:
        validate(ROOT / filename)
