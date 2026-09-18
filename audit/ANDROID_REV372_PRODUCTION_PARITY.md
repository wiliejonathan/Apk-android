# Android REV372 Production Audit

- APK SHA256: 3f2027a1118591d75535b0f99265f4ae18b2fcab18462c9cd370ca606c03a306
- mobile-data-bridge signed in JAR manifest: True
- dashboard-mobile signed in JAR manifest: False
- force updater signed in JAR manifest: True
- bridge bytes: 34557
- dashboard bytes: 640392

## Bridge behavior
- canonical-history preserve patch present: False
- mobile history normalizer present: True
- old filter path present: False

## Price behavior
- price cache key present: True
- mobile no-live-price comment present: True
- static fallback map present: True

## Force update
~~~js
(function(){
  'use strict';

  var CURRENT_TAG = 'v1.16.69';
  var API_URL = 'https://api.github.com/repos/wiliejonathan/Apk-android/releases/latest';
  var CACHE_KEY = 'tf_android_required_update_v1';
  var CHECK_KEY = 'tf_android_update_last_check_v1';
  var CHECK_EVERY_MS = 5 * 60 * 1000;
  var state = { checking:false, locked:false, latest:null };

  function hasNativeUpdater(){
    try {
      return !!(window.AndroidUpdate && typeof window.AndroidUpdate.downloadAndInstall === 'function');
    } catch (_) { return false; }
  }

  function nums(tag){
    var m=String(tag||'').match(/(\d+)\.(\d+)\.(\d+)/);
    return m ? [Number(m[1]),Number(m[2]),Number(m[3])] : [0,0,0];
  }
  function newer(a,b){
    var A=nums(a), B=nums(b);
    for(var i=0;i<3;i++){
      if(A[i]>B[i]) return true;
      if(A[i]<B[i]) return false;
    }
    return false;
  }
  function apkAsset(release){
    var list = release && Array.isArray(release.assets) ? release.assets : [];
    var apks = list.filter(function(x){
      return x && /\.apk$/i.test(String(x.name||'')) && x.browser_download_url;
    });
    apks.sort(function(a,b){
      return new Date(b.updated_at||b.created_at||0) - new Date(a.updated_at||a.created_at||0);
    });
    return apks[0] || null;
  }

  async function fetchLatestApkInfo(){
    var res=await fetch(API_URL+'?t='+Date.now(),{
      cache:'no-store',
      headers:{
        'Accept':'application/vnd.github+json',
        'Cache-Control':'no-cache'
      }
    });
    if(!res.ok) throw new Error('GitHub API HTTP '+res.status);
    var release=await res.json();
    var tag=String(release.tag_name||'').trim();
    var asset=apkAsset(release);
    if(!tag) throw new Error('Tag release terbaru tidak ditemukan.');
    if(!asset) throw new Error('Asset APK tidak ditemukan pada release '+tag+'.');
    return {
      tag:tag,
      url:String(asset.browser_download_url||''),
      name:String(asset.name||'TF.Analyzer.Analyst.update.apk'),
      releaseUrl:String(release.html_url||'')
    };
  }

  function saveRequired(info){ try{ localStorage.setItem(CACHE_KEY, JSON.stringify(info)); }catch(_){ } }
  function loadRequired(){
    try{ var raw=localStorage.getItem(CACHE_KEY); return raw ? JSON.parse(raw) : null; }
    catch(_){ return null; }
  }
  function clearRequired(){ try{ localStorage.removeItem(CACHE_KEY); }catch(_){ } }

  function setStatus(text){ var e=document.getElementById('tf-force-update-status'); if(e) e.textContent=String(text||''); }
  function setButton(enabled,label){
    var b=document.getElementById('tf-force-update-btn');
    if(!b) return;
    b.disabled=!enabled;
    if(label) b.textContent=label;
  }

  function overlay(){
    var el=document.getElementById('tf-force-update-overlay');
    if(el) return el;
    el=document.createElement('div');
    el.id='tf-force-update-overlay';
    el.innerHTML=''
      +'<div class="tf-force-update-card">'
      +'<div class="tf-force-update-icon">↻</div>'
      +'<div class="tf-force-update-title">Update Wajib Tersedia</div>'
      +'<div class="tf-force-update-copy">Versi aplikasi ini sudah tidak dapat digunakan karena versi terbaru TF Analyzer Analyst sudah tersedia.</div>'
      +'<div class="tf-force-update-version"><span>Versi sekarang</span><b id="tf-force-current">'+CURRENT_TAG+'</b></div>'
      +'<div class="tf-force-update-version"><span>Versi terbaru</span><b id="tf-force-latest">-</b></div>'
      +'<button type="button" id="tf-force-update-btn">DOWNLOAD & INSTALL UPDATE</button>'
      +'<div id="tf-force-update-status">Tekan tombol di atas untuk memperbarui aplikasi.</div>'
      +'<div class="tf-force-update-note">Tombol akan membaca release terbaru langsung dari GitHub, mengunduh asset .apk terbaru, lalu membuka Android Installer otomatis setelah download selesai.</div>'
      +'</div>';
    document.documentElement.appendChild(el);
    var style=document.createElement('style');
    style.id='tf-force-update-style';
    style.textContent=''
      +'#tf-force-update-overlay{position:fixed;inset:0;z-index:2147483647;background:rgba(2,6,23,.98);display:none;align-items:center;justify-content:center;padding:22px;font-family:Arial,sans-serif;color:#f8fafc;box-sizing:border-box;pointer-events:auto}'
      +'#tf-force-update-overlay.show{display:flex}'
      +'.tf-force-update-card{width:min(430px,100%);background:#0f172a;border:1px solid #334155;border-radius:20px;padding:24px;box-shadow:0 24px 70px rgba(0,0,0,.55);text-align:center}'
      +'.tf-force-update-icon{width:62px;height:62px;border-radius:18px;background:#166534;margin:0 auto 14px;display:grid;place-items:center;font-size:36px;font-weight:700}'
      +'.tf-force-update-title{font-size:22px;font-weight:800;margin-bottom:10px}'
      +'.tf-force-update-copy{font-size:14px;line-height:1.55;color:#cbd5e1;margin-bottom:18px}'
      +'.tf-force-update-version{display:flex;justify-content:space-between;gap:16px;padding:10px 12px;background:#020617;border-radius:11px;margin:8px 0;fo
~~~

## Signature coverage excerpts

### assets/www/mobile-data-bridge.js
~~~text
Name: assets/www/mobile-data-bridge.js
SHA-256-Digest: F1745NpH6BEP1aUNRDYC6BYB96/pCQbXBjcw95ZD6iY=

Name: assets/www/icons/icon-192.png
SHA-256-Digest: QcC5j/dBZKPaoZ0Vv49O28YCC0GhIVhl3yL2DH6fdas=

Name: res/aB.png
SHA-256-Digest: QcC5j/dBZKPaoZ0Vv49O28YCC0GhIVhl3yL2DH6fdas=

Name: assets/www/README_REV341.txt
SHA-256-Digest: 8+1ZIVs/SK3GB4Heem990cdN/38kJVr4ZwtgVkBP3NY=

Name: assets/www/mobile-license-gate.js
SHA-256-Digest: 39cW57Bb/hoxY6yMc0OkucOi9+9HnQalhuYnwg2Zcvg=

Name: assets/www/README
~~~

### assets/www/dashboard-mobile.js
~~~text
NOT LISTED
~~~

### assets/www/mobile-force-update.js
~~~text
Name: assets/www/mobile-force-update.js
SHA-256-Digest: UqnTPgwUsI/rwCSIxavf+0/Vj1C3IAn1SeU1cLK5jTk=

Name: assets/www/mobile-data-bridge.js
SHA-256-Digest: F1745NpH6BEP1aUNRDYC6BYB96/pCQbXBjcw95ZD6iY=

Name: assets/www/icons/icon-192.png
SHA-256-Digest: QcC5j/dBZKPaoZ0Vv49O28YCC0GhIVhl3yL2DH6fdas=

Name: res/aB.png
SHA-256-Digest: QcC5j/dBZKPaoZ0Vv49O28YCC0GhIVhl3yL2DH6fdas=

Name: assets/www/README_REV341.txt
SHA-256-Digest: 8+1ZIVs/SK3GB4Heem990cdN/38kJVr4ZwtgVkBP3NY=

Name: assets/www/mobile
~~~