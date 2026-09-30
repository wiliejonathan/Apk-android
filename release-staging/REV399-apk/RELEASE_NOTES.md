# TF Analyzer Analyst Android V1.17.12 — REV399

## JSON Import Fix

APK memakai bundle REV399 yang sama dengan iOS/website:
- official export dan raw canonical storage JSON diterima;
- BOM, padding NUL, dan double-encoded JSON ditangani;
- stale Cancel tidak menggagalkan import berikutnya;
- Combine menormalisasi setiap file sebelum digabung;
- JSON kosong/tidak dikenali ditolak sehingga data lama tidak tertimpa;
- pesan error Import dibuat lebih jelas.

Android activation fallback dan seluruh perbaikan REV392–REV398 tetap dipertahankan.

Version: **v1.17.12 / REV399**
