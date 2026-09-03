package com.skillfusion.tfmultianalystmobil3;

import android.app.Activity;
import android.app.DownloadManager;
import android.content.BroadcastReceiver;
import android.content.ClipData;
import android.content.ContentResolver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.database.Cursor;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.provider.Settings;
import android.util.Base64;
import android.webkit.JavascriptInterface;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

import java.io.File;
import java.io.OutputStream;

public class MainActivity extends Activity {
    private static final int FILE_CHOOSER_REQUEST = 1001;
    private static final int SAVE_FILE_REQUEST = 1002;
    private static final int INSTALL_PERMISSION_REQUEST = 1003;
    private static final String APK_MIME = "application/vnd.android.package-archive";

    private WebView webView;
    private ValueCallback<Uri[]> filePathCallback;
    private byte[] pendingSaveBytes;
    private String pendingSaveName;
    private String pendingSaveMime;

    private DownloadManager downloadManager;
    private long updateDownloadId = -1L;
    private String pendingUpdateUrl;
    private String pendingUpdateName;
    private boolean waitingInstallPermission = false;
    private boolean receiverRegistered = false;

    private final BroadcastReceiver updateDownloadReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            if (!DownloadManager.ACTION_DOWNLOAD_COMPLETE.equals(intent.getAction())) return;
            long id = intent.getLongExtra(DownloadManager.EXTRA_DOWNLOAD_ID, -1L);
            if (id != updateDownloadId || id < 0) return;
            handleUpdateDownloadFinished(id);
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        getWindow().setStatusBarColor(Color.rgb(2, 6, 23));
        getWindow().setNavigationBarColor(Color.rgb(2, 6, 23));
        if (Build.VERSION.SDK_INT >= 23) {
            getWindow().getDecorView().setSystemUiVisibility(0);
        }

        downloadManager = (DownloadManager) getSystemService(DOWNLOAD_SERVICE);
        registerUpdateReceiver();

        webView = new WebView(this);
        webView.setBackgroundColor(Color.rgb(2, 6, 23));
        setContentView(webView);

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);
        settings.setUseWideViewPort(true);
        settings.setLoadWithOverviewMode(true);
        settings.setBuiltInZoomControls(true);
        settings.setDisplayZoomControls(false);
        settings.setMediaPlaybackRequiresUserGesture(false);
        settings.setSupportMultipleWindows(false);
        settings.setTextZoom(100);

        webView.addJavascriptInterface(new AndroidSaveBridge(), "AndroidSave");
        webView.addJavascriptInterface(new AndroidUpdateBridge(), "AndroidUpdate");

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                return openExternalIfNeeded(request != null ? request.getUrl() : null);
            }

            @Override
            @SuppressWarnings("deprecation")
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                return openExternalIfNeeded(url == null ? null : Uri.parse(url));
            }
        });

        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onShowFileChooser(WebView webView, ValueCallback<Uri[]> callback,
                                             FileChooserParams fileChooserParams) {
                if (MainActivity.this.filePathCallback != null) {
                    MainActivity.this.filePathCallback.onReceiveValue(null);
                }
                MainActivity.this.filePathCallback = callback;
                Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
                intent.addCategory(Intent.CATEGORY_OPENABLE);
                intent.setType("*/*");
                intent.putExtra(Intent.EXTRA_MIME_TYPES, new String[]{
                        "application/json", "text/json", "text/plain", "application/octet-stream"
                });
                intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, false);
                try {
                    startActivityForResult(intent, FILE_CHOOSER_REQUEST);
                    return true;
                } catch (Exception e) {
                    MainActivity.this.filePathCallback = null;
                    Toast.makeText(MainActivity.this, "Storage tidak dapat dibuka", Toast.LENGTH_LONG).show();
                    return false;
                }
            }
        });

        webView.loadUrl("file:///android_asset/www/index.html");
    }

    private boolean openExternalIfNeeded(Uri uri) {
        if (uri == null) return false;
        String scheme = uri.getScheme();
        if (scheme == null || "file".equalsIgnoreCase(scheme) || "about".equalsIgnoreCase(scheme)
                || "data".equalsIgnoreCase(scheme) || "javascript".equalsIgnoreCase(scheme)) {
            return false;
        }
        try {
            Intent i = new Intent(Intent.ACTION_VIEW, uri);
            startActivity(i);
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    @Override
    public void onBackPressed() {
        if (webView != null && webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        maybeContinuePendingUpdate();
    }

    @Override
    protected void onDestroy() {
        if (receiverRegistered) {
            try { unregisterReceiver(updateDownloadReceiver); } catch (Exception ignored) {}
            receiverRegistered = false;
        }
        if (webView != null) {
            webView.removeJavascriptInterface("AndroidSave");
            webView.removeJavascriptInterface("AndroidUpdate");
            webView.destroy();
            webView = null;
        }
        super.onDestroy();
    }

    private void registerUpdateReceiver() {
        if (receiverRegistered) return;
        try {
            registerReceiver(updateDownloadReceiver, new IntentFilter(DownloadManager.ACTION_DOWNLOAD_COMPLETE));
            receiverRegistered = true;
        } catch (Exception e) {
            receiverRegistered = false;
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == INSTALL_PERMISSION_REQUEST) {
            maybeContinuePendingUpdate();
            return;
        }

        if (requestCode == FILE_CHOOSER_REQUEST) {
            if (filePathCallback == null) return;
            Uri[] result = null;
            if (resultCode == RESULT_OK && data != null) {
                ClipData clip = data.getClipData();
                if (clip != null && clip.getItemCount() > 0) {
                    result = new Uri[clip.getItemCount()];
                    for (int i = 0; i < clip.getItemCount(); i++) {
                        result[i] = clip.getItemAt(i).getUri();
                    }
                } else if (data.getData() != null) {
                    result = new Uri[]{data.getData()};
                }
            }
            filePathCallback.onReceiveValue(result);
            filePathCallback = null;
            return;
        }

        if (requestCode == SAVE_FILE_REQUEST) {
            if (resultCode == RESULT_OK && data != null && data.getData() != null && pendingSaveBytes != null) {
                Uri uri = data.getData();
                OutputStream out = null;
                try {
                    ContentResolver resolver = getContentResolver();
                    out = resolver.openOutputStream(uri, "w");
                    if (out == null) throw new Exception("Output stream tidak tersedia");
                    out.write(pendingSaveBytes);
                    out.flush();
                    Toast.makeText(this, "File tersimpan: " + pendingSaveName, Toast.LENGTH_SHORT).show();
                    evalJs("window.dispatchEvent(new CustomEvent('tf-native-save-complete'))");
                } catch (Exception e) {
                    Toast.makeText(this, "Gagal menyimpan file: " + e.getMessage(), Toast.LENGTH_LONG).show();
                } finally {
                    if (out != null) try { out.close(); } catch (Exception ignored) {}
                }
            }
            pendingSaveBytes = null;
            pendingSaveName = null;
            pendingSaveMime = null;
        }
    }

    public final class AndroidSaveBridge {
        @JavascriptInterface
        public void saveBase64(final String name, final String mime, final String base64) {
            try {
                final byte[] bytes = Base64.decode(base64 == null ? "" : base64, Base64.DEFAULT);
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        pendingSaveBytes = bytes;
                        pendingSaveName = (name == null || name.trim().isEmpty()) ? "export.bin" : name.trim();
                        pendingSaveMime = (mime == null || mime.trim().isEmpty()) ? "application/octet-stream" : mime.trim();
                        try {
                            Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
                            intent.addCategory(Intent.CATEGORY_OPENABLE);
                            intent.setType(pendingSaveMime);
                            intent.putExtra(Intent.EXTRA_TITLE, pendingSaveName);
                            startActivityForResult(intent, SAVE_FILE_REQUEST);
                        } catch (Exception e) {
                            pendingSaveBytes = null;
                            Toast.makeText(MainActivity.this, "Gagal menyiapkan file: " + e.getMessage(), Toast.LENGTH_LONG).show();
                        }
                    }
                });
            } catch (Exception e) {
                Toast.makeText(MainActivity.this, "Gagal menyiapkan file: " + e.getMessage(), Toast.LENGTH_LONG).show();
            }
        }
    }

    public final class AndroidUpdateBridge {
        @JavascriptInterface
        public String getInstalledVersionTag() {
            return "v1.16.62";
        }

        @JavascriptInterface
        public void downloadAndInstall(final String url, final String fileName) {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    requestUpdateDownload(url, fileName);
                }
            });
        }
    }

    private void requestUpdateDownload(String url, String fileName) {
        String cleanUrl = url == null ? "" : url.trim();
        if (!cleanUrl.startsWith("https://")) {
            dispatchUpdateEvent("tf-native-update-failed", "URL update tidak valid.");
            return;
        }
        String cleanName = safeApkName(fileName);

        if (!canInstallUnknownSources()) {
            pendingUpdateUrl = cleanUrl;
            pendingUpdateName = cleanName;
            waitingInstallPermission = true;
            dispatchUpdateEvent("tf-native-update-needs-permission", "Izinkan instalasi dari TF Analyzer Analyst.");
            try {
                Intent settingsIntent = new Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES,
                        Uri.parse("package:" + getPackageName()));
                startActivityForResult(settingsIntent, INSTALL_PERMISSION_REQUEST);
            } catch (Exception e) {
                dispatchUpdateEvent("tf-native-update-failed", "Pengaturan instalasi tidak dapat dibuka: " + e.getMessage());
            }
            return;
        }

        enqueueUpdateDownload(cleanUrl, cleanName);
    }

    private boolean canInstallUnknownSources() {
        if (Build.VERSION.SDK_INT < 26) return true;
        try {
            return getPackageManager().canRequestPackageInstalls();
        } catch (Exception e) {
            return false;
        }
    }

    private void maybeContinuePendingUpdate() {
        if (!waitingInstallPermission || pendingUpdateUrl == null) return;
        if (!canInstallUnknownSources()) return;
        String url = pendingUpdateUrl;
        String name = pendingUpdateName;
        pendingUpdateUrl = null;
        pendingUpdateName = null;
        waitingInstallPermission = false;
        enqueueUpdateDownload(url, name);
    }

    private String safeApkName(String name) {
        String n = name == null ? "" : name.trim();
        n = n.replaceAll("[^A-Za-z0-9._-]", "_");
        if (n.isEmpty()) n = "TF.Analyzer.Analyst.update.apk";
        if (!n.toLowerCase().endsWith(".apk")) n += ".apk";
        return n;
    }

    private void enqueueUpdateDownload(String url, String fileName) {
        if (downloadManager == null) {
            dispatchUpdateEvent("tf-native-update-failed", "Download Manager Android tidak tersedia.");
            return;
        }
        try {
            File dir = getExternalFilesDir(Environment.DIRECTORY_DOWNLOADS);
            if (dir != null) {
                File old = new File(dir, fileName);
                if (old.exists()) old.delete();
            }

            DownloadManager.Request request = new DownloadManager.Request(Uri.parse(url));
            request.setTitle("TF Analyzer Analyst Update");
            request.setDescription("Mengunduh versi terbaru…");
            request.setMimeType(APK_MIME);
            request.setAllowedOverMetered(true);
            request.setAllowedOverRoaming(true);
            request.setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED);
            request.setDestinationInExternalFilesDir(this, Environment.DIRECTORY_DOWNLOADS, fileName);

            updateDownloadId = downloadManager.enqueue(request);
            dispatchUpdateEvent("tf-native-update-started", "Download update dimulai.");
            Toast.makeText(this, "Mengunduh update TF Analyzer Analyst…", Toast.LENGTH_LONG).show();
        } catch (Exception e) {
            updateDownloadId = -1L;
            dispatchUpdateEvent("tf-native-update-failed", "Download gagal dimulai: " + e.getMessage());
        }
    }

    private void handleUpdateDownloadFinished(long id) {
        Cursor cursor = null;
        try {
            DownloadManager.Query query = new DownloadManager.Query().setFilterById(id);
            cursor = downloadManager.query(query);
            if (cursor == null || !cursor.moveToFirst()) {
                throw new Exception("Status download tidak tersedia.");
            }
            int statusIndex = cursor.getColumnIndex(DownloadManager.COLUMN_STATUS);
            int reasonIndex = cursor.getColumnIndex(DownloadManager.COLUMN_REASON);
            int status = statusIndex >= 0 ? cursor.getInt(statusIndex) : DownloadManager.STATUS_FAILED;
            if (status != DownloadManager.STATUS_SUCCESSFUL) {
                int reason = reasonIndex >= 0 ? cursor.getInt(reasonIndex) : -1;
                throw new Exception("Download gagal (kode " + reason + ").");
            }

            Uri apkUri = downloadManager.getUriForDownloadedFile(id);
            if (apkUri == null) throw new Exception("File APK hasil download tidak ditemukan.");
            openPackageInstaller(apkUri);
        } catch (Exception e) {
            dispatchUpdateEvent("tf-native-update-failed", e.getMessage());
        } finally {
            if (cursor != null) cursor.close();
        }
    }

    private void openPackageInstaller(Uri apkUri) {
        try {
            Intent install = new Intent(Intent.ACTION_VIEW);
            install.setDataAndType(apkUri, APK_MIME);
            install.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_ACTIVITY_NEW_TASK);
            startActivity(install);
            dispatchUpdateEvent("tf-native-update-installer-opened", "Installer Android dibuka.");
        } catch (Exception e) {
            dispatchUpdateEvent("tf-native-update-failed", "Installer tidak dapat dibuka: " + e.getMessage());
        }
    }

    private void dispatchUpdateEvent(final String eventName, final String message) {
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                String safe = jsString(message == null ? "" : message);
                evalJs("window.dispatchEvent(new CustomEvent('" + eventName + "',{detail:{message:'" + safe + "'}}))");
            }
        });
    }

    private String jsString(String s) {
        return s.replace("\\", "\\\\")
                .replace("'", "\\'")
                .replace("\r", "\\r")
                .replace("\n", "\\n")
                .replace("</", "<\\/");
    }

    private void evalJs(String js) {
        if (webView == null) return;
        if (Build.VERSION.SDK_INT >= 19) {
            webView.evaluateJavascript(js, null);
        } else {
            webView.loadUrl("javascript:" + js);
        }
    }
}
