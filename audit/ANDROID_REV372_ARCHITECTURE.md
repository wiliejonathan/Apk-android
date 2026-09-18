# Production APK architecture audit

## Assets
      689  1981-01-01 01:01   assets/www/README_REV336.txt
      559  1981-01-01 01:01   assets/www/README_REV338.txt
      389  1981-01-01 01:01   assets/www/README_REV339.txt
      369  1981-01-01 01:01   assets/www/README_REV340.txt
      693  1981-01-01 01:01   assets/www/README_REV341.txt
      811  1981-01-01 01:01   assets/www/README_REV342.txt
      462  1981-01-01 01:01   assets/www/README_REV343.txt
      805  1981-01-01 01:01   assets/www/README_REV344.txt
      617  1981-01-01 01:01   assets/www/README_REV345.txt
      423  1981-01-01 01:01   assets/www/README_REV347.txt
      497  1981-01-01 01:01   assets/www/README_REV349.txt
   640568  1981-01-01 01:01   assets/www/assets/dashboard-mobile.js
    57374  1981-01-01 01:01   assets/www/assets/dashboard-original.css
    18997  1981-01-01 01:01   assets/www/icon32.png
    36560  1981-01-01 01:01   assets/www/icons/icon-180.png
    41546  1981-01-01 01:01   assets/www/icons/icon-192.png
   319719  1981-01-01 01:01   assets/www/icons/icon-512.png
     2332  1981-01-01 01:01   assets/www/index.html
      442  1981-01-01 01:01   assets/www/manifest.webmanifest
    70956  1981-01-01 01:01   assets/www/mobile-app-shell.js
     7626  1981-01-01 01:01   assets/www/mobile-chrome-shim.js
    34613  1981-01-01 01:01   assets/www/mobile-data-bridge.js
    10143  1981-01-01 01:01   assets/www/mobile-force-update.js
     6823  1981-01-01 01:01   assets/www/mobile-import-fix-v30.js
    19109  1981-01-01 01:01   assets/www/mobile-license-gate.js
   324283  1981-01-01 01:01   assets/www/mobile-overrides.css
    30600  1981-01-01 01:01   assets/www/mobile-remote.css
   174103  1981-01-01 01:01   assets/www/mobile-remote.js
     2787  1981-01-01 01:01   assets/www/service-worker.js
      711  2026-09-03 14:35   assets/www/README_REV352.txt
      281  2026-09-11 16:54   assets/www/README_REV372.txt

## index.html
<!doctype html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#020617">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="TF Analyzer Analyst">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icons/icon-180.png">
<title>TF Analyzer Analyst</title>
<link rel="stylesheet" href="assets/dashboard-original.css?rev=372">
<link rel="stylesheet" href="mobile-overrides.css?rev=372">
</head>
<body>
<div id="tf-mobile-import-loading" class="tf-mobile-import-loading" role="status" aria-live="polite">
  <div class="tf-mobile-import-loading-card">
    <div class="tf-mobile-import-spinner" aria-hidden="true">
      <span></span><span></span><span></span>
    </div>
    <div class="tf-mobile-import-loading-title">Memuat Data</div>
    <div id="tf-mobile-import-loading-message" class="tf-mobile-import-loading-message">Menyiapkan dashboard…</div>
    <div class="tf-mobile-import-loading-bar" aria-hidden="true"><i></i></div>
    <div id="tf-mobile-import-loading-detail" class="tf-mobile-import-loading-detail">Mohon tunggu. Jangan tutup aplikasi.</div>
    <button id="tf-mobile-import-cancel-rev293" class="tf-rev293-cancel-btn" type="button">Cancel</button>
  </div>
</div>
<script>
(function(){
  try{
    if(sessionStorage.getItem("tf_mobile_import_loading_v8")==="1"){
      document.documentElement.classList.add("tf-mobile-import-busy");
      var el=document.getElementById("tf-mobile-import-loading");
      if(el)el.classList.add("show");
      var detail=sessionStorage.getItem("tf_mobile_import_loading_detail_v8");
      var detailEl=document.getElementById("tf-mobile-import-loading-detail");
      if(detail&&detailEl)detailEl.textContent=detail;
    }
  }catch(e){}
})();
</script>

<script src="mobile-force-update.js?rev=372"></script>
<script src="mobile-license-gate.js?rev=372"></script>
<script src="mobile-import-fix-v30.js?rev=372"></script>
<script>if('serviceWorker' in navigator){window.addEventListener('load',()=>navigator.serviceWorker.register('./service-worker.js').catch(()=>{}));}</script>
</body>
</html>
## mobile-remote.js refs
4:  const API='https://tf-license-device-api.wiliejonathan1999.workers.dev';
865:    q('tf-remote-dashboard').addEventListener('click',()=>openMobileDashboardHome());
921:      ${pairLocked?`<input class="tf-remote-link-input" type="url" inputmode="url" placeholder="https://account.tradersfamily.id/channels/..." value="${esc(currentUrl)}" readonly>`:`<div class="tf-remote-link-line"><input class="tf-remote-link-input" type="url" inputmode="url" placeholder="https://account.tradersfamily.id/channels/..." value="${esc(currentUrl)}"><button type="button" class="tf-remote-link-confirm${linkConfirmed?' is-success':''}" data-confirm-link>CONFIRM</button></div>`}
1641:        if(typeof window.tfMobileApplyRemotePayload==='function')await window.tfMobileApplyRemotePayload(payload,['Remote-PC-Sync.json']);
1971:  function openMobileDashboardHome(){
2016:      if(typeof window.tfMobileApplyRemotePayload==='function')await window.tfMobileApplyRemotePayload(payload,[file.name||'Remote-Import.json']);

## service-worker.js
const CACHE='tf-analyzer-analyst-mobile-v150-rev372-dashboard-home-local';
const ASSETS=[
  './assets/dashboard-mobile.js?rev=372',
  './assets/dashboard-original.css?rev=372',
  './icon32.png',
  './icons/icon-180.png',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './index.html',
  './manifest.webmanifest',
  './mobile-app-shell.js?rev=372',
  './mobile-remote.js?rev=372',
  './mobile-chrome-shim.js?rev=372',
  './mobile-data-bridge.js?rev=372',
  './mobile-force-update.js?rev=372',
  './mobile-license-gate.js?rev=372',
  './mobile-import-fix-v30.js?rev=372',
  './mobile-overrides.css?rev=372'
];
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)).then(()=>self.skipWaiting())));
self.addEventListener('activate',event=>event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));

async function networkFirst(req){
  const cache=await caches.open(CACHE);
  try{
    const res=await fetch(req,{cache:'no-store'});
    if(res&&res.ok)cache.put(req,res.clone()).catch(()=>{});
    return res;
  }catch(_){
    const hit=await caches.match(req);
    if(hit)return hit;
    throw _;
  }
}
async function cacheFirst(req){
  const hit=await caches.match(req);
  if(hit)return hit;
  const res=await fetch(req);
  if(res&&res.ok)caches.open(CACHE).then(c=>c.put(req,res.clone())).catch(()=>{});
  return res;
}
self.addEventListener('fetch',event=>{
  const req=event.request;
  if(req.method!=='GET')return;
  const url=new URL(req.url);
  if(url.origin!==self.location.origin)return;
  const mutable=req.mode==='navigate'||/\.(?:html|js|css|webmanifest)$/i.test(url.pathname);
  event.respondWith(mutable?networkFirst(req):cacheFirst(req));
});

self.addEventListener('notificationclick', event => {
  const action=String(event.action||'');
  event.notification.close();
  if(action!=='stop')return;
  event.waitUntil(self.clients.matchAll({type:'window',includeUncontrolled:true}).then(list=>Promise.all(list.map(c=>c.postMessage({type:'TF_REMOTE_STOP'})))));
});

// REV345: Equity Y-axis uses 5% padding below actual low/start and 5% above actual high.

// REV345: Candle D1 keeps adaptive zoom; visible OHLC viewport also uses 5% edge padding.

// REV347: Touch tooltip is offset from the finger; desktop mouse behavior is unchanged.

// REV349: strict activation on every fresh launch, live license revocation, no persisted TF user/session/import data.

// REV352: remembered activation opens from local confirmed authorization; silent server refresh; timeout-safe boot; activation form only for first activation or explicit revocation.

// REV372: Remote > Buka Dashboard is local Mobile navigation; no open_dashboard command is sent to PC.

## AndroidManifest strings

## signature verification
      >>> Signer
      X.509, CN=TF Analyzer Analyst, OU=TF Analyzer, O=Skill Fusion, L=Pontianak, ST=West Kalimantan, C=ID
      Signature algorithm: SHA384withRSA, 3072-bit key
      [certificate is valid from 8/30/26, 9:23 PM to 1/15/54, 9:23 PM]
      [Invalid certificate chain: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target]

sm     10143 Thu Jan 01 01:01:02 UTC 1981 assets/www/mobile-force-update.js

      >>> Signer
      X.509, CN=TF Analyzer Analyst, OU=TF Analyzer, O=Skill Fusion, L=Pontianak, ST=West Kalimantan, C=ID
      Signature algorithm: SHA384withRSA, 3072-bit key
      [certificate is valid from 8/30/26, 9:23 PM to 1/15/54, 9:23 PM]
      [Invalid certificate chain: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target]

sm      6823 Thu Jan 01 01:01:02 UTC 1981 assets/www/mobile-import-fix-v30.js

      >>> Signer
      X.509, CN=TF Analyzer Analyst, OU=TF Analyzer, O=Skill Fusion, L=Pontianak, ST=West Kalimantan, C=ID
      Signature algorithm: SHA384withRSA, 3072-bit key
      [certificate is valid from 8/30/26, 9:23 PM to 1/15/54, 9:23 PM]
      [Invalid certificate chain: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target]

sm     19109 Thu Jan 01 01:01:02 UTC 1981 assets/www/mobile-license-gate.js

      >>> Signer
      X.509, CN=TF Analyzer Analyst, OU=TF Analyzer, O=Skill Fusion, L=Pontianak, ST=West Kalimantan, C=ID
      Signature algorithm: SHA384withRSA, 3072-bit key
      [certificate is valid from 8/30/26, 9:23 PM to 1/15/54, 9:23 PM]
      [Invalid certificate chain: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target]

sm    324283 Thu Jan 01 01:01:02 UTC 1981 assets/www/mobile-overrides.css

      >>> Signer
      X.509, CN=TF Analyzer Analyst, OU=TF Analyzer, O=Skill Fusion, L=Pontianak, ST=West Kalimantan, C=ID
      Signature algorithm: SHA384withRSA, 3072-bit key
      [certificate is valid from 8/30/26, 9:23 PM to 1/15/54, 9:23 PM]
      [Invalid certificate chain: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target]

sm     30600 Thu Jan 01 01:01:02 UTC 1981 assets/www/mobile-remote.css

      >>> Signer
      X.509, CN=TF Analyzer Analyst, OU=TF Analyzer, O=Skill Fusion, L=Pontianak, ST=West Kalimantan, C=ID
      Signature algorithm: SHA384withRSA, 3072-bit key
      [certificate is valid from 8/30/26, 9:23 PM to 1/15/54, 9:23 PM]
      [Invalid certificate chain: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target]

sm    174103 Thu Jan 01 01:01:02 UTC 1981 assets/www/mobile-remote.js

      >>> Signer
      X.509, CN=TF Analyzer Analyst, OU=TF Analyzer, O=Skill Fusion, L=Pontianak, ST=West Kalimantan, C=ID
      Signature algorithm: SHA384withRSA, 3072-bit key
      [certificate is valid from 8/30/26, 9:23 PM to 1/15/54, 9:23 PM]
      [Invalid certificate chain: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target]

sm      2787 Thu Jan 01 01:01:02 UTC 1981 assets/www/service-worker.js

      >>> Signer
      X.509, CN=TF Analyzer Analyst, OU=TF Analyzer, O=Skill Fusion, L=Pontianak, ST=West Kalimantan, C=ID
      Signature algorithm: SHA384withRSA, 3072-bit key
      [certificate is valid from 8/30/26, 9:23 PM to 1/15/54, 9:23 PM]
      [Invalid certificate chain: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target]

sm      2796 Thu Jan 01 01:01:02 UTC 1981 AndroidManifest.xml

      >>> Signer
      X.509, CN=TF Analyzer Analyst, OU=TF Analyzer, O=Skill Fusion, L=Pontianak, ST=West Kalimantan, C=ID
      Signature algorithm: SHA384withRSA, 3072-bit key
      [certificate is valid from 8/30/26, 9:23 PM to 1/15/54, 9:23 PM]
      [Invalid certificate chain: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target]

sm     41546 Thu Jan 01 01:01:02 UTC 1981 res/aB.png

      >>> Signer
      X.509, CN=TF Analyzer Analyst, OU=TF Analyzer, O=Skill Fusion, L=Pontianak, ST=West Kalimantan, C=ID
      Signature algorithm: SHA384withRSA, 3072-bit key
      [certificate is valid from 8/30/26, 9:23 PM to 1/15/54, 9:23 PM]
      [Invalid certificate chain: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target]

sm       568 Thu Jan 01 01:01:02 UTC 1981 resources.arsc

      >>> Signer
      X.509, CN=TF Analyzer Analyst, OU=TF Analyzer, O=Skill Fusion, L=Pontianak, ST=West Kalimantan, C=ID
      Signature algorithm: SHA384withRSA, 3072-bit key
      [certificate is valid from 8/30/26, 9:23 PM to 1/15/54, 9:23 PM]
      [Invalid certificate chain: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target]

sm       711 Thu Sep 03 14:35:00 UTC 2026 assets/www/README_REV352.txt

      >>> Signer
      X.509, CN=TF Analyzer Analyst, OU=TF Analyzer, O=Skill Fusion, L=Pontianak, ST=West Kalimantan, C=ID
      Signature algorithm: SHA384withRSA, 3072-bit key
      [certificate is valid from 8/30/26, 9:23 PM to 1/15/54, 9:23 PM]
      [Invalid certificate chain: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target]

sm       281 Fri Sep 11 16:54:36 UTC 2026 assets/www/README_REV372.txt

      >>> Signer
      X.509, CN=TF Analyzer Analyst, OU=TF Analyzer, O=Skill Fusion, L=Pontianak, ST=West Kalimantan, C=ID
      Signature algorithm: SHA384withRSA, 3072-bit key
      [certificate is valid from 8/30/26, 9:23 PM to 1/15/54, 9:23 PM]
      [Invalid certificate chain: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target]


  s = signature was verified 
  m = entry is listed in manifest
  k = at least one certificate was found in keystore

- Signed by "CN=TF Analyzer Analyst, OU=TF Analyzer, O=Skill Fusion, L=Pontianak, ST=West Kalimantan, C=ID"
    Digest algorithm: SHA-256
    Signature algorithm: SHA256withRSA, 3072-bit key

jar verified.

Warning: 
This jar contains entries whose certificate chain is invalid. Reason: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target
This jar contains entries whose signer certificate is self-signed.
This jar contains signatures that do not include a timestamp. Without a timestamp, users may not be able to validate this jar after any of the signer certificates expire (as early as 2054-01-15).
POSIX file permission and/or symlink attributes detected. These attributes are ignored when signing and are not protected by the signature.

The signer certificate will expire on 2054-01-15.
