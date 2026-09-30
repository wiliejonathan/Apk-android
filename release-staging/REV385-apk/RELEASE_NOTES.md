# TF Analyzer Analyst Android v1.16.98 — REV385

## Holding Period — Table 3 Source-of-Truth Fix

Build Android ini memakai source iOS/browser REV385 v1.16.98 yang sama.

- Holding = Table 3 Closed At − Table 3 Created At.
- Label tanggal WIB yang tampil di Table 3 menjadi source of truth.
- Numeric sort keys hanya fallback kompatibilitas.
- Max dan Avg memakai exact final trade rows Table 3 setelah filter Nama Analis/Pair, Time Range, Time Range per Month, dan Filter Tanggal.
- Withdraw tidak dihitung.
- Alignment REV384 dan Table 3 performance fix tetap dipertahankan.

### Signing
APK release ini adalah fresh-install/QA build karena private production/update key lama tidak tersimpan di repository. Paket production-signing-ready juga dipublish untuk build dengan key production yang benar.
