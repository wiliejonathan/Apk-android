# Android REV381 Fresh-Install QA

This APK contains the same REV381 mobile calculation/data-bridge fixes released for iOS/browser.

- PC remains official REV379 / v1.16.92 and is not modified.
- Official PC export rows are preserved as canonical input on Mobile.
- History duplicate identity/completeness semantics match PC REV379.
- Mobile calculation helper functions were audited against PC REV379.
- Core app assets use REV381 cache revisions.

## Signing note

The connected GitHub repositories, ChatGPT Library and Google Drive do not contain the private production keystore for the current Android certificate.

Therefore this APK is deliberately published as a **prerelease QA / fresh-install build** with a temporary test signer. It cannot update the installed production APK in-place. The stable Android release remains v1.16.69 until the original production private key is available.

Do not promote this prerelease through the production force-updater.
