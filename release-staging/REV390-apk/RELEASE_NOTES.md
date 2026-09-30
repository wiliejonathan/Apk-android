# TF Analyzer Analyst Android v1.17.03 — REV390

## Apps Script 404 Activation Fallback

- Memperbaiki error aktivasi `[APPS_SCRIPT_HTTP_ERROR] Apps Script HTTP 404`.
- Cloudflare Device API tetap menjadi jalur utama.
- Jika Worker gagal karena Apps Script 404/timeout/network/invalid-response, login dan license-check otomatis menggunakan **public Apps Script license lookup** secara langsung.
- Fallback tidak membawa atau mengekspos `SERVER_SHARED_SECRET`.
- URL fallback dibaca dari pointer publik `tf-analyzer-admin/license-endpoint.json`, dengan current endpoint sebagai hardcoded safety fallback.
- Invalid/expired/revoked response tetap authoritative dan tidak diubah menjadi valid.
- REV389 retry reliability serta REV388 Performance Holding placement tetap dipertahankan.

### Signing
Fresh-install APK dan production-signing-ready package dipublish.
