"""Keep installation separate from launching the jailbreak application."""
from pathlib import Path
import sys

page = Path(sys.argv[1]) / 'frontend/installer-page/index.html'
text = page.read_text(encoding='utf-8')

def replace(old, new):
    global text
    if new in text:
        return
    if text.count(old) != 1:
        raise SystemExit('Installer patch anchor changed: ' + old[:80])
    text = text.replace(old, new, 1)

replace('var probeOk = false;', 'var probeOk = false;\n      var cacheReady = false;')
replace("        window.location.replace(AUTOLOADER_URL);", """        // Installation must never launch the jailbreak on a failed probe.
        if (completed) return;
        completed = true;
        setFailed();
        detailEl.textContent = 'Installer server unavailable. Close this page and resend the installer ELF. No jailbreak was started.';""")
replace('xhr.timeout = 1000;', 'xhr.timeout = 10000;')
replace('              probeOk = true;\n              setCaching();',
        '              if (completed) return;\n              probeOk = true;\n              setCaching();\n              maybeInstall();')
replace('''          if (!probeOk) {
            clearInterval(waitTimer);
            goToAutoloader();
            return;
          }''', '''          if (!probeOk) return; // Probe is asynchronous; wait for its result.''')
replace('''          if (!window.applicationCache) {
            clearInterval(waitTimer);
            maybeInstall();
            return;
          }''', '''          if (!window.applicationCache) {
            clearInterval(waitTimer);
            completed = true;
            setFailed();
            detailEl.textContent = 'Offline cache is unavailable. The app was not installed.';
            return;
          }''')
replace('''      function maybeInstall() {
        if (completed) {
          return;
        }
        completed = true;
        installApp();
      }''', '''      function maybeInstall() {
        if (completed) return;
        var cache = window.applicationCache;
        // Terminal cache events and server readiness can arrive in either order.
        if (!cache) return;
        if (cache.status === cache.IDLE || cache.status === cache.UPDATEREADY)
          cacheReady = true;
        if (!probeOk || !cacheReady || isDownloading) return;
        completed = true;
        installApp();
      }''')
replace("The PS5 Relapse AutoLoader shortcut is now on your PS5 homescreen. You can close this page.",
        "Cache complete and app installed. Close this page. Open PS5 Relapse AutoLoader from the homescreen when you want to jailbreak.")
page.write_text(text, encoding='utf-8', newline='\n')
print('Installer is cache/install only; probe failures never launch the app')
