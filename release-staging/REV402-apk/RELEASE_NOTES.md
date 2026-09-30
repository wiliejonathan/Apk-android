# TF Analyzer Analyst Android v1.17.15 — REV402

## Fast JSON Import / Loading

- Single-flight render setelah Import JSON.
- Bulk IndexedDB write tidak lagi memicu render duplikat.
- Retry render dipangkas menjadi satu pass + fallback singkat.
- Overlay loading ditutup segera setelah data inti siap.
- Boot/storage recovery tidak berjalan bersamaan dengan import.
- REV401 remembered-links restore dan seluruh fix REV400 tetap dipertahankan.

Fresh-install APK memakai signing key build REV402. Untuk update-in-place dari APK produksi lama gunakan production-signing-ready package dengan signing key produksi asli.
