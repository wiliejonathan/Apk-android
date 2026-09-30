# Android REV383 — Production Signing Ready

Paket ini membawa web-assets Mobile REV383 v1.16.96 yang sudah dipakai oleh iOS/browser dan siap dimasukkan ke wrapper Android production.

- Holding Period per Analyst-Pair.
- Holding tables tanpa scrollbar internal.
- Header Max/Avg Holding Period centered.
- Table 3 History bebas cursor-follow glow/observer overhead.
- REV382 canonical JSON import fix tetap dipertahankan.

## Penting
Untuk menghasilkan APK yang benar-benar bisa **update di atas instalasi production lama**, build wrapper Android harus ditandatangani dengan **private production/update keystore REV330+ yang sama**. Key tersebut tidak tersimpan di repository, sehingga workflow ini menyediakan assets signing-ready dan tidak memalsukan kompatibilitas signature.
