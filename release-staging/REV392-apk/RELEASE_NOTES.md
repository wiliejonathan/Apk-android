# TF Analyzer Analyst Android V1.17.05 — REV392

## Android Activation + Holding Strict Time Range

- APK menggunakan bundle mobile REV392 yang sama dengan iOS/website.
- Aktivasi Android: bila Worker mengembalikan denial device/session lama, token diverifikasi ulang melalui GitHub Pages relay + public license lookup sebelum dianggap gagal.
- Relay sekarang membawa path /mobile/login atau /license-check sehingga aktivasi awal dan validasi berkala konsisten.
- Holding Period: hanya trade Table 3 yang checked/enabled dan Created At berada di dalam Time Range.
- Carry-over sebelum awal 1M/2M/3M/dst dipaksa unchecked, sehingga 1M tidak lagi dapat menghasilkan Holding 57d dari trade di luar periode.
- Fresh-install APK ini ditandatangani dengan key release workflow fresh-install REV392; paket signing-ready juga disediakan untuk signing menggunakan key produksi/original.

Version: **v1.17.05 / REV392**
