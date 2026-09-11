#!/usr/bin/env python3
from pathlib import Path
import zipfile, sys

if len(sys.argv) != 4:
    raise SystemExit('usage: build_rev372_prod.py BASE_REV352.apk SIGNATURE_DIR OUT.apk')

src = Path(sys.argv[1])
sigdir = Path(sys.argv[2])
out = Path(sys.argv[3])

with zipfile.ZipFile(src, 'r') as zin:
    files = {i.filename: zin.read(i.filename) for i in zin.infolist()}
    infos = {i.filename: i for i in zin.infolist()}

# v1.16.68 / versionCode 109 -> v1.16.69 / versionCode 110.
data = bytearray(files['AndroidManifest.xml'])
old_name = '1.16.68'.encode('utf-16le')
new_name = '1.16.69'.encode('utf-16le')
assert data.count(old_name) == 1
data = data.replace(old_name, new_name, 1)
code109 = bytes([0x08, 0x00, 0x00, 0x10]) + (109).to_bytes(4, 'little')
pos = data.find(code109)
assert pos >= 0 and data.find(code109, pos + 1) < 0
data[pos + 4:pos + 8] = (110).to_bytes(4, 'little')
files['AndroidManifest.xml'] = bytes(data)

# Remote > Buka Dashboard must navigate locally on Mobile and never send open_dashboard to PC.
remote = files['assets/www/mobile-remote.js'].decode('utf-8')
old_bind = "q('tf-remote-dashboard').addEventListener('click',()=>sendCommand('open_dashboard').catch(()=>{}));"
new_bind = "q('tf-remote-dashboard').addEventListener('click',()=>openMobileDashboardHome());"
assert remote.count(old_bind) == 1
assert 'function openMobileDashboardHome()' in remote
remote = remote.replace(old_bind, new_bind, 1)
files['assets/www/mobile-remote.js'] = remote.encode('utf-8')

index = files['assets/www/index.html'].decode('utf-8').replace('?rev=352', '?rev=372')
files['assets/www/index.html'] = index.encode('utf-8')

sw = files['assets/www/service-worker.js'].decode('utf-8')
lines = sw.splitlines()
assert lines and lines[0].startswith('const CACHE=')
lines[0] = "const CACHE='tf-analyzer-analyst-mobile-v150-rev372-dashboard-home-local';"
sw = '\n'.join(lines) + '\n'
sw = sw.replace('?rev=352', '?rev=372')
sw += '\n// REV372: Remote > Buka Dashboard is local Mobile navigation; no open_dashboard command is sent to PC.\n'
files['assets/www/service-worker.js'] = sw.encode('utf-8')

updater = files['assets/www/mobile-force-update.js'].decode('utf-8')
assert updater.count("var CURRENT_TAG = 'v1.16.68';") == 1
updater = updater.replace("var CURRENT_TAG = 'v1.16.68';", "var CURRENT_TAG = 'v1.16.69';", 1)
files['assets/www/mobile-force-update.js'] = updater.encode('utf-8')

files['assets/www/README_REV372.txt'] = (
    'TF Analyzer Analyst Android REV372\n'
    'Version: v1.16.69\n'
    'Version Code: 110\n'
    'Fix: Remote > Buka Dashboard opens the local Mobile dashboard (Table 1) and no longer sends open_dashboard to the PC plugin.\n'
    'Base: production REV352, signed with the same REV330+ production/update certificate.\n'
).encode('utf-8')

signatures = {
    'META-INF/MANIFEST.MF': (sigdir / 'MANIFEST.MF').read_bytes(),
    'META-INF/TFANALYZ.SF': (sigdir / 'TFANALYZ.SF').read_bytes(),
    'META-INF/TFANALYZ.RSA': (sigdir / 'TFANALYZ.RSA').read_bytes(),
}

# Rebuild with public JAR signature blocks produced by the production signer.
# No private signing key is stored in the repository.
with zipfile.ZipFile(out, 'w') as zout:
    for name in ['META-INF/MANIFEST.MF', 'META-INF/TFANALYZ.SF', 'META-INF/TFANALYZ.RSA']:
        zi = zipfile.ZipInfo(name, (2026, 9, 11, 16, 54, 36))
        zi.compress_type = zipfile.ZIP_DEFLATED
        zi.create_system = 0
        zi.external_attr = 0
        zi.internal_attr = 0
        zi.flag_bits = 2056
        zout.writestr(zi, signatures[name])

    for info in infos.values():
        upper = info.filename.upper()
        if upper.startswith('META-INF/') and (upper.endswith('.RSA') or upper.endswith('.SF') or upper.endswith('MANIFEST.MF')):
            continue
        blob = files[info.filename]
        ni = zipfile.ZipInfo(info.filename, info.date_time)
        ni.compress_type = info.compress_type
        ni.external_attr = info.external_attr
        ni.internal_attr = info.internal_attr
        ni.create_system = info.create_system
        ni.extra = info.extra
        ni.comment = info.comment
        ni.flag_bits = info.flag_bits
        zout.writestr(ni, blob)

    name = 'assets/www/README_REV372.txt'
    zi = zipfile.ZipInfo(name, (2026, 9, 11, 16, 54, 36))
    zi.compress_type = zipfile.ZIP_DEFLATED
    zi.create_system = 3
    zi.external_attr = 2175008768
    zi.internal_attr = 0
    zi.flag_bits = 2056
    zout.writestr(zi, files[name])

print(out)
