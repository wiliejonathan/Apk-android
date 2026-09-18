# Android REV381 — Production Signing Ready

**Plugin PC tetap REV379 / v1.16.92 dan tidak diubah.**

Paket ini membawa source Mobile REV381 yang sudah lolos QA iOS/browser dan disiapkan untuk wrapper Android.

Perbaikan:
- Canonical `tfHistorySignals` dari PC tidak diubah/filter ulang oleh Mobile.
- Duplicate-history precedence disamakan dengan PC REV379.
- Formula kalkulasi Mobile diverifikasi terhadap PC REV379.
- Cache/source Mobile menggunakan REV381 final.

## Penting
Ini adalah **web-assets signing-ready**, bukan APK production final.

APK update resmi harus dibuild menggunakan wrapper Android lama dan **production/update keystore REV330+ yang sama**. Private key tersebut tidak tersimpan di repository, jadi workflow tidak membuat APK dengan sertifikat baru yang akan memutus update chain.
