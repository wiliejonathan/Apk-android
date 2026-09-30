# TF Analyzer Analyst Android v1.17.00 — REV387

## Holding Period Timeframe Parity

- Holding per trade = **Closed At (`displayDate`) − Created At (`createdDate`)**.
- `createdSortKey` / `sortKey` hanya fallback.
- Withdraw tidak dihitung.
- **Max Holding Period dan Avg Holding Period sekarang sama-sama mengikuti Time Range, Time Range per Month, Filter Tanggal, Nama Analis, dan Pair.**
- Alignment/performance REV384, import persistence, custom cursor, dan no-inner-scroll tetap dipertahankan.

### Signing
Fresh-install/QA APK disediakan; paket production-signing-ready juga disediakan untuk signing dengan key production asli.
