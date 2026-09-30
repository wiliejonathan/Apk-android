# TF Analyzer Analyst Android v1.17.01 — REV388

## Holding Analytics moved to Performance

- **TABLE ANALYTICS → Holding Period per Analis** sekarang berada di nav **Performance**.
- Posisi tepat **di bawah Performance/Probability Analis**.
- Holding section dipindahkan sebagai DOM yang sama, bukan diduplikasi, sehingga tidak ada duplicate ID / duplicate calculation.
- Holding per trade tetap **Closed At (`displayDate`) − Created At (`createdDate`)**.
- **Max** dan **Avg** sama-sama mengikuti Time Range, Time Range per Month, Filter Tanggal, Nama Analis, dan Pair aktif.
- Layout Android dibuat satu kolom, tanpa inner scrollbar.
- Import persistence, Table 3 performance fix, dan UI REV387 tetap dipertahankan.

### Signing
APK release ini adalah fresh-install/QA signed build. Paket production-signing-ready juga disediakan untuk signing dengan key production asli.
