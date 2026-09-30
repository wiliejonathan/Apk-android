# TF Analyzer Analyst Android v1.16.98 — REV385

## Holding Period Accuracy Fix

Build Android ini memakai source iOS/browser REV385 v1.16.98 final.

- Holding = Table 3 **Closed At − Created At**.
- Sumber utama adalah string tanggal yang benar-benar tampil: `displayDate` dan `createdDate`.
- Numeric sort keys hanya fallback untuk legacy rows.
- **Max Holding Period** memakai seluruh history untuk Analyst-Pair yang aktif.
- **Avg Holding Period** mengikuti Time Range, Time Range per Month, dan Filter Tanggal aktif.
- Withdraw tidak dihitung.
- Alignment REV384, no-inner-scroll, import persistence, dan Table 3 performance fix tetap dipertahankan.

### Signing
APK release ini adalah fresh-install/QA build; paket production-signing-ready juga tersedia untuk signing dengan key production lama.
