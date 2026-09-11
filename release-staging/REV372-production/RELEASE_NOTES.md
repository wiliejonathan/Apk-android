# TF Analyzer Analyst V1.16.69

## REV372 — Mobile Dashboard Routing Fix

Release ini memperbaiki tombol **Remote > Buka Dashboard** pada aplikasi Android.

### Perbaikan utama
- **Buka Dashboard** sekarang membuka **dashboard lokal di ponsel (Table 1)**.
- Tombol tersebut **tidak lagi mengirim command `open_dashboard` ke Plugin PC**.
- Dashboard Plugin PC tidak lagi ikut terbuka ketika tombol ini ditekan dari ponsel.
- Remote page ditutup dan navigasi dikembalikan ke halaman depan aplikasi Mobile.
- Cache mobile dinaikkan ke REV372 agar instalasi lama tidak mempertahankan JavaScript Remote yang lama.

### Android update
- Version: **v1.16.69**
- Runtime: **REV372**
- Version Code: **110**
- Base production: **v1.16.68 / REV352**
- Signing certificate: **sama dengan production/update chain REV330+**
- APK dapat dipasang sebagai **update di atas v1.16.68/REV352** tanpa uninstall terlebih dahulu.

### Komponen lain
Fungsi Remote lain seperti Update, Submit, Refresh/Reset, Scan From iSignal User, Import/Export JSON, Pair/Link confirmation, serta progress/event log tidak diubah oleh hotfix ini.

### QA
- APK ZIP integrity: PASS
- JAR signature verification: PASS
- Production signing certificate match REV352: PASS
- Version Name 1.16.69 / Version Code 110: PASS
- Dashboard button local binding: PASS
- Mandatory updater current tag v1.16.69: PASS
- Service-worker cache REV372: PASS
