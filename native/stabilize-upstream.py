"""Fail closed and reduce embedded log work; do not tune the kernel race."""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')

def patch(relative, old, new):
    path = root / relative
    text = path.read_text(encoding='utf-8')
    if new in text:
        return
    if text.count(old) != 1:
        raise SystemExit('Stability patch anchor changed: ' + relative)
    path.write_text(text.replace(old, new, 1), encoding='utf-8', newline='\n')

base = 'frontend/autoloader/relapse/src/'
patch(base + 'main.js',
      '''    const why = "Already jailbroken.";
    log(why, "error");
    if (AUTOLOAD) reportAutoload(false, { why: why });
    return;''',
      '''    log("ELF loader already running; opening payload controls", "info");
    await startAutoload(p, chain);
    return;''')
patch(base + 'relapse_exploit.js',
      'return { kbase: this.kbase, done: true, payloads: false };',
      'return { kbase: this.kbase, done: false, payloads: false, error: why };')
patch(base + 'main.js',
      'throw new Error("kernel exploit did not finish");',
      'throw new Error((result && result.error) || "kernel exploit did not finish");')
patch(base + 'main.js',
      'log("kernel chain complete: root and sandbox escape are active", "info");',
      'log("ELF loader did not start; payload readiness is not confirmed", "error");')
patch(base + 'site.js',
      '''  output.scrollTop = output.scrollHeight;
  /* A successful chain can finish before the parent's 500 ms poll runs.
     Queue a mirror update for every log write, including rewritten lines. */
  if (window.parent !== window) {
    window.parent.postMessage({ type: "wkal", kind: "log" }, "*");
  }''',
      '''  // Embedded logs are mirrored in batches by the parent's existing poll.
  // Avoid forcing layout in the hidden exploit document for every message.
  if (window.parent === window) output.scrollTop = output.scrollHeight;''')
patch(base + 'site.js',
      'run().catch((error) => writeLog(error instanceof Error ? error.message : String(error), "error"));',
      '''run().catch((error) => {
  const why = error instanceof Error ? error.message : String(error);
  writeLog(why, "error");
  if (window.parent !== window)
    window.parent.postMessage({ type: "wkal", kind: "autoload", ok: false,
      why: why + ". Restart the console before another attempt." }, "*");
});''')
patch(base + 'webkit.js', 'let settleResolve = null',
      'let settleResolve = null\nlet settleReject = null\nconst MAX_SAFE_ATTEMPTS = 5;')
patch(base + 'webkit.js',
      'function retry(reason, safeToRelease) {\n  const nextAttempt',
      '''function retry(reason, safeToRelease) {
  // Do not restart uncertain state or retry indefinitely within one document.
  if (!safeToRelease || attemptNumber >= MAX_SAFE_ATTEMPTS) {
    if (safeToRelease) releaseAttempt();
    settleReject(new Error(reason + "; retry stopped. Restart the console."));
    return;
  }
  const nextAttempt''')
patch(base + 'webkit.js',
      'return new Promise((resolve) => {\n    settleResolve = resolve;',
      'return new Promise((resolve, reject) => {\n    settleReject = reject;\n    settleResolve = resolve;')
patch('frontend/autoloader/app.js', 'if (data.ok && mirrorTimer) {',
      "if ((data.ok || exploitMode === 'relapse') && mirrorTimer) {")
patch('frontend/autoloader/app.js',
      "      if (data.kind === 'menu-ready') {\n        finished = true;",
      "      if (data.kind === 'menu-ready') {\n        if (finished) return;\n        mirrorConsole(exploitMode);\n        finished = true;")
print('Applied terminal-failure reporting, bounded retry and batched logging safeguards')
