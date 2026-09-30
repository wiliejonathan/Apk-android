# TF Analyzer Analyst Android v1.16.99 — REV386

## Holding Period Final Accuracy

- Holding per trade = **Closed At (`displayDate`) − Created At (`createdDate`)** from Table 3.
- Numeric sort keys are fallback-only.
- Withdraw rows are excluded.
- **Max Holding Period** = longest holding from **all history** for each active Analyst-Pair.
- **Avg Holding Period** = average holding from the active Time Range / Time Range per Month / Filter Tanggal dataset.
- Analyst/Pair ticker filters control which Analyst-Pair rows appear.
- REV384 alignment/performance and import persistence remain intact.

### Signing
Fresh-install/QA APK is provided; production-signing-ready assets are also published for signing with the original production key.
