from pathlib import Path
import re

# Patch Web mobile Remote to use the strict in-memory auth session first.
remote = Path('rev346-build/app/src/main/assets/www/mobile-remote.js')
s = remote.read_text(encoding='utf-8')
old = """  function auth(){\n    const c=getJson(CREDS_KEY),s=getJson(STATE_KEY);\n    if(!c||!s||!c.email||!c.token||!s.sessionToken)return null;\n    return {email:c.email,token:c.token,licenseId:s.licenseId||s.license||'',sessionToken:s.sessionToken};\n  }"""
new = """  function auth(){\n    // REV349: strict fresh-start mode keeps Email/Token/session in memory only.\n    const mem=window.__TF_MOBILE_AUTH_V349||null;\n    if(mem&&mem.email&&mem.token&&mem.sessionToken){\n      return {email:mem.email,token:mem.token,licenseId:mem.licenseId||'',sessionToken:mem.sessionToken};\n    }\n    const c=getJson(CREDS_KEY),s=getJson(STATE_KEY);\n    if(!c||!s||!c.email||!c.token||!s.sessionToken)return null;\n    return {email:c.email,token:c.token,licenseId:s.licenseId||s.license||'',sessionToken:s.sessionToken};\n  }"""
if old not in s:
    raise SystemExit('REV349 mobile-remote auth block not found')
s = s.replace(old, new, 1)
s = s.replace("mobileVersion:'1.0.101',remoteRevision:'REV332'", "mobileVersion:'1.0.106',remoteRevision:'REV349'")
remote.write_text(s, encoding='utf-8')

# Native Android fresh-start hardening: purge WebView browser storage/cache on every Activity creation.
main = Path('rev346-build/app/src/main/java/com/skillfusion/tfmultianalystmobil3/MainActivity.java')
m = main.read_text(encoding='utf-8')
if 'import android.webkit.WebStorage;' not in m:
    m = m.replace('import android.webkit.WebSettings;\n', 'import android.webkit.WebSettings;\nimport android.webkit.WebStorage;\nimport android.webkit.CookieManager;\n')

m = m.replace('settings.setTextZoom(100);', '''settings.setTextZoom(100);\n        settings.setCacheMode(WebSettings.LOAD_NO_CACHE);\n        try { settings.setSaveFormData(false); } catch (Exception ignored) {}''')

marker = '        webView.loadUrl("file:///android_asset/www/index.html");'
fresh = '''        // REV349: every true Android app launch starts fresh. No prior WebView user/session/import\n        // data may bypass the token gate or repopulate the dashboard.\n        try { WebStorage.getInstance().deleteAllData(); } catch (Exception ignored) {}\n        try {\n            CookieManager cm = CookieManager.getInstance();\n            cm.removeAllCookies(null);\n            cm.flush();\n        } catch (Exception ignored) {}\n        try {\n            webView.clearCache(true);\n            webView.clearHistory();\n            webView.clearFormData();\n        } catch (Exception ignored) {}\n\n        webView.loadUrl("file:///android_asset/www/index.html");'''
if marker not in m:
    raise SystemExit('MainActivity loadUrl marker not found')
m = m.replace(marker, fresh, 1)
m = m.replace('return "v1.16.64";', 'return "v1.16.65";')
main.write_text(m, encoding='utf-8')

# Bump Web runtime revision references.
idx = Path('rev346-build/app/src/main/assets/www/index.html')
i = idx.read_text(encoding='utf-8')
i = re.sub(r'\?rev=(?:344|345|346|347|348)', '?rev=349', i)
idx.write_text(i, encoding='utf-8')

sw = Path('rev346-build/app/src/main/assets/www/service-worker.js')
if sw.exists():
    t = sw.read_text(encoding='utf-8')
    t = re.sub(r"const CACHE='[^']+';", "const CACHE='tf-analyzer-analyst-mobile-v145-rev349-strict-live-license-fresh-start';", t, count=1)
    t = re.sub(r'\?rev=(?:344|345|346|347|348)', '?rev=349', t)
    t += '\n// REV349: strict token gate + live license revocation + fresh-start user data policy.\n'
    sw.write_text(t, encoding='utf-8')
