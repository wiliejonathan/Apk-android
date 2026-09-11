# TF Analyzer Analyst Android REV372

## Remote Dashboard Home Routing Fix

Build ini memperbaiki tombol **Remote > Buka Dashboard** agar kembali ke halaman depan aplikasi Android (Table 1), bukan membuka Dashboard milik Plugin PC.

### Perbaikan
- Dashboard di halaman Remote sekarang merupakan navigasi lokal Android.
- Command `open_dashboard` tidak lagi dikirim ke PC ketika tombol Dashboard ditekan.
- Remote page ditutup terlebih dahulu lalu aplikasi kembali ke halaman depan Mobile.
- Update, Submit, Refresh/Reset, Scan From iSignal, dan command Remote lain tidak diubah.

### Penting — Fresh Install Test
APK pada prerelease ini ditandatangani dengan **test signing certificate**, karena production Android keystore yang menandatangani REV330–REV352 tidak tersedia pada repository/session ini.

Akibatnya APK ini **tidak dapat meng-update APK production existing** tanpa uninstall terlebih dahulu. Karena itu release ini sengaja ditandai **Prerelease**, sehingga endpoint GitHub `/releases/latest` milik updater production tetap menunjuk ke v1.16.68/REV352 dan customer tidak dipaksa memasang signature yang berbeda.

Untuk production update yang kompatibel, build REV372 yang sama harus ditandatangani dengan production/update keystore lama.

**Tag:** v1.16.69-rev372-test

**Asset:** `TF.Analyzer.Analyst.V1.16.69_REV372_REMOTE_DASHBOARD_HOME_FIX_FRESH_INSTALL_TEST.apk`
