# TF Analyzer Analyst Android V1.16.95 — REV382

## JSON Import → Table Fix

Release Android ini berisi **satu file APK saja**.

- Memperbaiki import file JSON resmi dari Plugin PC dengan schema `tf_multi_analyst_export_v1`.
- `tfHistorySignals` dan `tfAnalystSources` tidak lagi menjadi kosong pada pre-normalization manual import.
- Table 1, Performance, Table 2, Equity, Table 3, dan Table 4 sekarang menerima canonical storage hasil import.
- Source Mobile sama dengan iOS/browser REV382 v1.16.95.
- Plugin PC tetap REV379 / v1.16.92 dan tidak diubah.

Catatan instalasi: production/update private keystore REV330+ tidak tersedia di repository. Build ini ditandatangani sebagai fresh-install build; bila Android menolak update di atas APK lama karena signature berbeda, uninstall APK lama terlebih dahulu setelah memastikan data yang perlu disimpan sudah diexport.
