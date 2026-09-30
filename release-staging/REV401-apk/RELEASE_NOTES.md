# TF Analyzer Analyst Android v1.17.14 — REV401

## JSON Import Remembered Links Restore

- Memperbaiki Import JSON ketika `tfRememberedAnalystLinks` tersimpan sebagai `[]` sementara `tfAnalystSources` masih berisi analis/link.
- Android otomatis membangun ulang link analis dan mengaktifkan Remember Links.
- Data hasil import tetap persisten setelah aplikasi ditutup/dibuka.
- Semua perbaikan REV400 untuk Holding Period dan warna Nama Analis tetap dipertahankan.
- Bundle Android menggunakan source mobile REV401 / v1.17.14 yang sama dengan iOS/browser.

Fresh-install APK memakai signing key build REV401. Untuk update-in-place dari APK produksi lama tetap gunakan production-signing-ready package dengan signing key produksi asli.
