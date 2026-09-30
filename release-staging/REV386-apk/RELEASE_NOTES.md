# TF Analyzer Analyst Android v1.16.99 — REV386

## Holding Period Final Table 3 Accuracy

- Holding dataset = exact final trade rows displayed/exported by Table 3 after active filters.
- Holding per trade = Closed At (`displayDate`) − Created At (`createdDate`).
- Numeric sort keys are fallback-only.
- Withdraw excluded.
- Max and Avg both follow analyst/pair, Time Range, Time Range per Month, and Filter Tanggal because all use the same final Table 3 rows.
- REV384 alignment/performance and import persistence remain intact.

### Signing
Fresh-install/QA APK is provided; production-signing-ready assets are also published for signing with the original production key.
