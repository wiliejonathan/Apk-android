from pathlib import Path
p = Path('rev346-build/app/src/main/assets/www/mobile-license-gate.js')
s = p.read_text(encoding='utf-8')

s = s.replace("const LICENSE_WATCH_MS = 5000;", "const LICENSE_WATCH_MS = 5000;\n  const AUTH_KEY = 'tfMobileRememberedLicenseV351';")
s = s.replace("'mobile-chrome-shim.js?rev=349'", "'mobile-chrome-shim.js?rev=351'")
s = s.replace("'assets/dashboard-mobile.js?rev=349'", "'assets/dashboard-mobile.js?rev=351'")
s = s.replace("'mobile-data-bridge.js?rev=349'", "'mobile-data-bridge.js?rev=351'")
s = s.replace("'mobile-app-shell.js?rev=349'", "'mobile-app-shell.js?rev=351'")
s = s.replace("'mobile-remote.js?rev=349'", "'mobile-remote.js?rev=351'")
s = s.replace("mobileVersion: '1.0.106'", "mobileVersion: '1.0.108'")
s = s.replace("remoteRevision: 'REV349'", "remoteRevision: 'REV351'")
s = s.replace("token-gate-rev349", "token-gate-rev351")

old = "for (const k of keys) if (isTfStorageKey(k)) localStorage.removeItem(k);"
new = "for (const k of keys) if (isTfStorageKey(k) && k !== AUTH_KEY && k !== 'tf_android_required_update_v1' && k !== 'tf_android_update_last_check_v1') localStorage.removeItem(k);"
if old not in s:
    raise SystemExit('localStorage purge marker not found')
s = s.replace(old, new)

marker = "\n  function createGate() {"
helpers = r'''

  function readRememberedCredentials() {
    try {
      const raw = localStorage.getItem(AUTH_KEY);
      if (!raw) return null;
      const data = JSON.parse(raw);
      const email = cleanEmail(data && data.email);
      const token = normalizeToken(data && data.token);
      return email && token ? { email, token } : null;
    } catch (_) { return null; }
  }

  function rememberCredentials(email, token) {
    try {
      email = cleanEmail(email); token = normalizeToken(token);
      if (email && token) localStorage.setItem(AUTH_KEY, JSON.stringify({ email, token, savedAt: Date.now() }));
    } catch (_) {}
  }

  function forgetCredentials() {
    try { localStorage.removeItem(AUTH_KEY); } catch (_) {}
  }
'''
if marker not in s:
    raise SystemExit('createGate marker not found')
s = s.replace(marker, helpers + marker, 1)

s = s.replace(
    'Token selalu diperiksa ke server <b>sebelum dashboard dibuka</b>. Demi keamanan, login dan data aplikasi tidak disimpan untuk pemakaian berikutnya.',
    'Token selalu diperiksa ke server <b>sebelum dashboard dibuka</b>. Setelah aktivasi pertama berhasil, Email + Token diingat agar pemeriksaan berikutnya berjalan otomatis tanpa input ulang.'
)

old = "if (!(result && result.valid === true && result.sessionValid === true && result.sessionToken)) {"
new = "if (!(result && result.valid === true && result.sessionValid !== false)) {"
if old not in s:
    raise SystemExit('login validity marker not found')
s = s.replace(old, new, 1)

old = "setStatus(`[${code}] ${message}`, 'error'); return false;"
new = "forgetCredentials(); setStatus(`[${code}] ${message}`, 'error'); return false;"
if old in s:
    s = s.replace(old, new, 1)
else:
    old2 = "setStatus(`[${code}] ${message}`, 'error');\n        return false;"
    new2 = "forgetCredentials();\n        setStatus(`[${code}] ${message}`, 'error');\n        return false;"
    if old2 not in s:
        raise SystemExit('login failure marker not found')
    s = s.replace(old2, new2, 1)

old = "activeCredentials = { email, token };\n      activeState = { ...result, valid: true, checkedAt: Date.now() };"
new = "activeCredentials = { email, token };\n      activeState = { ...result, valid: true, checkedAt: Date.now() };\n      rememberCredentials(email, token);"
if old not in s:
    raise SystemExit('login success marker not found')
s = s.replace(old, new, 1)

if "activeCredentials = null; activeState = null; exposeEphemeralAuth();\n    await clearPersistentAppData();" in s:
    s = s.replace("activeCredentials = null; activeState = null; exposeEphemeralAuth();\n    await clearPersistentAppData();", "forgetCredentials(); activeCredentials = null; activeState = null; exposeEphemeralAuth();\n    await clearPersistentAppData();", 1)
else:
    s = s.replace("activeCredentials = null;\n    activeState = null;\n    exposeEphemeralAuth();\n    await clearPersistentAppData();", "forgetCredentials();\n    activeCredentials = null;\n    activeState = null;\n    exposeEphemeralAuth();\n    await clearPersistentAppData();", 1)

logout_marker = "async function logout({ ask = true } = {}) {"
idx = s.find(logout_marker)
if idx < 0:
    raise SystemExit('logout marker not found')
tail = s[idx:]
if "activeCredentials = null; activeState = null; exposeEphemeralAuth();\n    await clearPersistentAppData();" in tail:
    tail = tail.replace("activeCredentials = null; activeState = null; exposeEphemeralAuth();\n    await clearPersistentAppData();", "forgetCredentials(); activeCredentials = null; activeState = null; exposeEphemeralAuth();\n    await clearPersistentAppData();", 1)
elif "activeCredentials = null;\n    activeState = null;\n    exposeEphemeralAuth();\n    await clearPersistentAppData();" in tail:
    tail = tail.replace("activeCredentials = null;\n    activeState = null;\n    exposeEphemeralAuth();\n    await clearPersistentAppData();", "forgetCredentials();\n    activeCredentials = null;\n    activeState = null;\n    exposeEphemeralAuth();\n    await clearPersistentAppData();", 1)
else:
    raise SystemExit('logout clear marker not found')
s = s[:idx] + tail

start = s.find("  async function boot() {")
end = s.find("\n  window.addEventListener('pagehide'", start)
if start < 0 or end < 0:
    raise SystemExit('boot block not found')
boot = r'''  async function boot() {
    const remembered = readRememberedCredentials();
    await clearPersistentAppData();
    activeCredentials = null; activeState = null; exposeEphemeralAuth();
    createGate(); bindUi();

    if (remembered && remembered.email && remembered.token) {
      const emailInput = document.getElementById('tf-license-email');
      const tokenInput = document.getElementById('tf-license-token');
      if (emailInput) emailInput.value = remembered.email;
      if (tokenInput) tokenInput.value = remembered.token;
      setStatus('Memeriksa lisensi tersimpan ke server…');
      await login(remembered.email, remembered.token);
      return;
    }

    setStatus('Aktivasi pertama: masukkan Email dan Token lisensi.');
  }
'''
s = s[:start] + boot + s[end:]

checks = [
    "AUTH_KEY = 'tfMobileRememberedLicenseV351'",
    "rememberCredentials(email, token)",
    "Memeriksa lisensi tersimpan ke server",
    "result.valid === true && result.sessionValid !== false",
    "forgetCredentials();",
    "remoteRevision: 'REV351'"
]
for c in checks:
    if c not in s:
        raise SystemExit('REV351 patch missing: ' + c)

p.write_text(s, encoding='utf-8')
print('REV351 gate patched:', p)
