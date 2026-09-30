# TF Analyzer Analyst Android V1.17.04 — REV391

## Android Activation + Holding Checkbox Parity

- Android memakai source mobile **REV391 / v1.17.04** yang sama dengan website.
- Aktivasi tetap mencoba Cloudflare Device API lebih dulu.
- Jika jalur Worker/direct Apps Script bermasalah di Android WebView, aplikasi memakai **GitHub Pages activation relay** agar request berasal dari origin website yang sudah berhasil digunakan pada iOS/browser.
- Holding Period hanya menghitung trade Table 3 yang **dicentang/enabled**.
- Carry-over trade yang otomatis unchecked oleh 1M/2M/... atau Time Range per Month tidak lagi ikut Max/Avg.
- Release APK REV391 dipublish sebagai **stable/latest**, bukan prerelease, agar updater Android mengambil APK baru ini dan bukan stable lama v1.16.95.

### Signing
APK ini tetap fresh-install build. Paket production-signing-ready juga dipublish untuk ditandatangani dengan key production asli bila tersedia.
