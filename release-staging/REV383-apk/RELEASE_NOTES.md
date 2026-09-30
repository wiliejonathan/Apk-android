# TF Analyzer Analyst Android V1.16.96 — REV383

## Holding Analytics + Table 3 Performance Fix

Build Android ini memakai source iOS/browser REV383 v1.16.96 yang sama.

- Holding Period tampil per **Nama Analis - Pair**.
- Tidak ada scrollbar internal pada tabel Holding Period.
- Header **Max - Holding Period** dan **Avg. Holding Period** ditengahkan.
- Efek cursor-follow glow tidak dijalankan pada Table 3 History agar history besar tetap ringan.
- Perbaikan canonical JSON import REV382 tetap dipertahankan.
- Cache mobile dinaikkan ke REV383.

### Signing
Private production/update keystore REV330+ tidak tersedia di repository. Karena itu APK pada release ini adalah **fresh-install/QA APK** yang ditandatangani key build baru dan dipublish sebagai prerelease, sehingga tidak mengganggu channel auto-update production. Jika Android menolak instal di atas APK lama karena signature berbeda, gunakan paket production-signing-ready dan sign dengan keystore production lama.
