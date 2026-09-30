# TF Analyzer Analyst Android v1.17.02 — REV389

## Activation Timeout Reliability Fix

- Server activation endpoint was independently probed and is responding normally.
- First activation now allows a longer request window instead of aborting after one short attempt.
- Timeout/network failures automatically retry once with a longer timeout.
- Explicit invalid/expired/revoked license responses are **not** retried and remain authoritative.
- Error text now distinguishes timeout from network failure.
- REV388 Performance Holding placement is retained: TABLE ANALYTICS is under nav Performance, below Performance/Probability Analis.
- Holding = Closed At − Created At; Max and Avg both follow active filters.

### Signing
Fresh-install/QA APK plus production-signing-ready package are published.
