# Android REV390 — Production Signing Ready

Source Android REV389 + activation backend fallback REV390.

- Worker Apps Script 404 -> direct public lookup fallback.
- Dynamic endpoint pointer + hardcoded current endpoint.
- No SERVER_SHARED_SECRET in client.
- REV389 retry + REV388 Performance Holding retained.

Untuk update-in-place di atas production lama tetap diperlukan signing key production yang sama.
