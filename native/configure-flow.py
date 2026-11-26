#!/usr/bin/env python3
"""Package the Wobkot PS5 route and the Relapse payload menu."""
from pathlib import Path
import shutil
import sys
import subprocess

source = Path(__file__).resolve().parent.parent
root = Path(sys.argv[1]).resolve()
subprocess.run([sys.executable, str(source / 'native/configure-installer.py'), str(root)], check=True)
app = root / "frontend/autoloader"
shutil.copytree(source / "wobkot", app / "wobkot", dirs_exist_ok=True)
for name in ("payload-ui.js", "payload-ui.css"):
    shutil.copyfile(source / "native" / name, app / name)
shutil.copyfile(source / "payloads.js", app / "payloads.js")
shutil.copytree(source / "ui", app / "ui", dirs_exist_ok=True)
shutil.copytree(source / "payloads", app / "payloads", dirs_exist_ok=True)
shutil.copytree(source / "offsets", app / "offsets", dirs_exist_ok=True)
page = app / "index.html"
text = page.read_text(encoding="utf-8")
if 'src="payload-ui.js"' not in text:
    text = text.replace('<script src="app.js"></script>',
                        '<script src="payloads.js"></script>\n'
                        '<script src="payload-ui.js"></script>\n'
                        '<script src="app.js"></script>')
text = text.replace('<link rel="stylesheet" href="payload-ui.css" />\n', '')
# Keep only the small toggle styled during exploitation. Load the card CSS and
# image assets after readiness, without affecting upstream's progress layout.
if 'id="relapse-toggle-style"' not in text:
    toggle_css = (source / "native/payload-ui.css").read_text(encoding="utf-8").split('#relapse-menu {')[0]
    text = text.replace('</head>', '<style id="relapse-toggle-style">' + toggle_css + '</style>\n</head>')
page.write_text(text, encoding="utf-8")

# Make Wobkot the default PS5 7.00-13.60 route in the native app. Keep the
# existing Relapse route available through ?force=relapse.
app_js = app / "app.js"
text = app_js.read_text(encoding="utf-8")
relapse_url = "  var RELAPSE_URL =\n    'relapse/index.html?autoload=payload.elf';"
wobkot_url = relapse_url + "\n  var WOBKOT_URL = 'wobkot/index.html?autoload=payload.elf';"
if "var WOBKOT_URL" not in text:
    if text.count(relapse_url) != 1:
        raise SystemExit("Upstream RELAPSE_URL changed; refusing an unverified Wobkot patch")
    text = text.replace(relapse_url, wobkot_url, 1)
if "function isWobkotSupported" not in text:
    helper = '''  function isWobkotSupported(str) {
    var match = /^(\\d+)\\.(\\d+)$/.exec(str || '');
    if (!match) return false;
    var major = parseInt(match[1], 10);
    var minor = parseInt(match[2], 16);
    return major >= 7 && (major < 13 || (major === 13 && minor <= 0x60));
  }

'''
    anchor = "  var UMTX2_URL ="
    if text.count(anchor) != 1:
        raise SystemExit("Upstream firmware selector changed; refusing the Wobkot firmware guard patch")
    text = text.replace(anchor, helper + anchor, 1)
text = text.replace("q === 'poops' || q === 'relapse'", "q === 'poops' || q === 'relapse' || q === 'wobkot'")
if "if (isWobkotSupported(fw.str)) return 'wobkot';" not in text:
    anchor = "    if (isUmtx2Supported(fw.num)) return 'umtx2';"
    if text.count(anchor) != 1:
        raise SystemExit("Upstream exploit selection changed; refusing the Wobkot default patch")
    text = text.replace(anchor, anchor + "\n    if (isWobkotSupported(fw.str)) return 'wobkot';", 1)
if "q === 'wobkot'" not in text:
    raise SystemExit("Upstream forced exploit selector changed; refusing the Wobkot override patch")
if ": picked === 'wobkot' ? WOBKOT_URL" not in text:
    exploit_url = "    var exploitUrl = picked === 'umtx2' ? UMTX2_URL\n      : picked === 'poops' ? POOPS_URL\n      : RELAPSE_URL;"
    if text.count(exploit_url) != 1:
        raise SystemExit("Upstream iframe routing changed; refusing the Wobkot route patch")
    text = text.replace(exploit_url,
                        "    var exploitUrl = picked === 'umtx2' ? UMTX2_URL\n"
                        "      : picked === 'poops' ? POOPS_URL\n"
                        "      : picked === 'wobkot' ? WOBKOT_URL\n"
                        "      : RELAPSE_URL;", 1)
if "exploitMode === 'wobkot'" not in text:
    log_anchor = "      if (data.kind === 'log' && exploitMode === 'relapse') {\n        mirrorConsole(exploitMode);\n        return;\n      }"
    if text.count(log_anchor) != 1:
        raise SystemExit("Upstream log handler changed; refusing the Wobkot log patch")
    text = text.replace(log_anchor,
                        "      if (data.kind === 'log' && exploitMode === 'wobkot') {\n"
                        "        var line = data.message || '';\n"
                        "        uiLog('[wobkot] ' + line, /^\\[-\\]/.test(line) ? 'error' : /^\\[\\+\\]/.test(line) ? 'success' : 'info');\n"
                        "        return;\n"
                        "      }\n" + log_anchor, 1)
if "picked !== 'wobkot'" not in text:
    mirror_anchor = "    } else {\n      mirrorTimer = setInterval(function () { mirrorConsole(exploitMode); }, 500);\n    }"
    if text.count(mirror_anchor) != 1:
        raise SystemExit("Upstream console mirror setup changed; refusing the Wobkot logger patch")
    text = text.replace(mirror_anchor,
                        "    } else if (picked !== 'wobkot') {\n"
                        "      mirrorTimer = setInterval(function () { mirrorConsole(exploitMode); }, 500);\n"
                        "    }", 1)
app_js.write_text(text, encoding="utf-8")

# The native AppCache matches exploit iframe URLs including their query.
registry = root / "tools/gen_file_registry.py"
text = registry.read_text(encoding="utf-8")
if "def wobkot_iframe_url" not in text:
    anchor = "def umtx2_iframe_url(app_dir):"
    helper = '''def wobkot_iframe_url(app_dir):
    return app_dir + "/wobkot/index.html?autoload=payload.elf"


'''
    if text.count(anchor) != 1:
        raise SystemExit("Upstream file registry changed; refusing the Wobkot route patch")
    text = text.replace(anchor, helper + anchor, 1)
if 'lines.append(wobkot_iframe_url(app_dir))' not in text:
    anchor = '    lines.append(relapse_iframe_url(app_dir))'
    if text.count(anchor) != 1:
        raise SystemExit("Upstream cache manifest changed; refusing the Wobkot route patch")
    text = text.replace(anchor, anchor + '\n    lines.append(wobkot_iframe_url(app_dir))', 1)
registry.write_text(text, encoding="utf-8")

# The upstream exploit patches were created from LF sources, while checked-out
# exploit files may use CRLF. Ask git-apply to ignore line-ending whitespace so
# all three pinned patches work on Windows and Linux build hosts.
for exploit in ("relapse", "slopkit", "umtx2"):
    patch_script = root / f"tools/apply_{exploit}_patch.sh"
    text = patch_script.read_text(encoding="utf-8")
    old_apply = 'if git apply --check "$PATCH" 2>/dev/null; then\n    git apply "$PATCH"'
    new_apply = ('if git apply --ignore-whitespace --check "$PATCH" 2>/dev/null; then\n'
                 '    git apply --ignore-whitespace "$PATCH"')
    if new_apply not in text:
        if text.count(old_apply) != 1:
            raise SystemExit(f"Upstream {exploit} patch handler changed; refusing the line-ending compatibility patch")
        text = text.replace(old_apply, new_apply, 1)
    old_reverse = 'elif git apply --reverse --check "$PATCH" 2>/dev/null; then'
    new_reverse = 'elif git apply --ignore-whitespace --reverse --check "$PATCH" 2>/dev/null; then'
    if new_reverse not in text:
        if text.count(old_reverse) != 1:
            raise SystemExit(f"Upstream {exploit} reverse-patch handler changed; refusing the line-ending compatibility patch")
        text = text.replace(old_reverse, new_reverse, 1)
    patch_script.write_text(text, encoding="utf-8")

# Keep all kernel/exploit code upstream. Add only a post-success payload sender
# bridge, in the generated frontend copy after upstream applies its own patch.
hook = '''from pathlib import Path
p = Path("frontend/autoloader/relapse/src/main.js")
s = p.read_text(encoding="utf-8")
anchor = 'async function startAutoload(p, chain) {\\n'
bridge = ''' + repr('''  if (window.parent.RelapsePayloadUI) {
    const { loadAutoloadPayload } = await import("./kexp.js");
    window.__relapseSendPayload = (name) => loadAutoloadPayload(
      p, chain, name, AUTOLOAD_BASE, (message) => log(message, "info"));
    window.parent.postMessage({ type: "wkal", kind: "menu-ready" }, "*");
    return;
  }
''') + '''
if "window.__relapseSendPayload" not in s:
    if s.count(anchor) != 1:
        raise SystemExit("Upstream startAutoload changed; refusing an unverified patch")
    p.write_text(s.replace(anchor, anchor + bridge, 1), encoding="utf-8")
'''
hook += '\ns = p.read_text(encoding="utf-8")\nold = ' + repr('''    const why = "Already jailbroken.";
    log(why, "error");
    if (AUTOLOAD) reportAutoload(false, { why: why });
    return;''') + '\nnew = ' + repr('''    log("ELF loader already running; opening payload controls", "info");
    await startAutoload(p, chain);
    return;''') + '''
if new not in s:
    if s.count(old) != 1:
        raise SystemExit("Upstream existing-loader branch changed")
    p.write_text(s.replace(old, new, 1), encoding="utf-8")
'''
(root / "tools/relapse_menu_bridge.py").write_text(hook, encoding="utf-8")
make = root / "Makefile"
text = make.read_text(encoding="utf-8")
anchor = '\t./tools/apply_relapse_patch.sh\n'
if 'tools/relapse_menu_bridge.py' not in text:
    if text.count(anchor) != 1:
        raise SystemExit("Upstream relapse-prepare changed")
    text = text.replace(anchor, anchor + '\t$(PYTHON) tools/relapse_menu_bridge.py\n')
    make.write_text(text, encoding="utf-8")

js = app / "app.js"
text = js.read_text(encoding="utf-8")
anchor = "      if (data.kind === 'autoload') {"
if "data.kind === 'menu-ready'" not in text:
    if text.count(anchor) != 1:
        raise SystemExit("Upstream message handler changed")
    text = text.replace(anchor, """      if (data.kind === 'menu-ready') {
        finished = true;
        if (mirrorTimer) { clearInterval(mirrorTimer); mirrorTimer = 0; }
        updateProgress(100, 'Jailbreak complete. ELF loader ready.');
        window.RelapsePayloadUI.ready(exploitEl.contentWindow.__relapseSendPayload);
        return;
      }
""" + anchor)
    js.write_text(text, encoding="utf-8")
if 'window.__relapseChainStartedAt' not in text:
    text = text.replace('    chainStarted = true;',
                        '    window.__relapseChainStartedAt = Date.now();\n    chainStarted = true;')
    text = text.replace("        updateProgress(100, 'Jailbreak complete. ELF loader ready.');",
                        "        updateProgress(100, 'Jailbreak complete. ELF loader ready in ' + "
                        "((Date.now() - window.__relapseChainStartedAt) / 1000).toFixed(1) + ' seconds.');")
    js.write_text(text, encoding="utf-8")
# Remove the optional stability hook from reused build trees. relapse-prepare
# regenerates the child sources from upstream on the next build.
text = make.read_text(encoding="utf-8")
make.write_text(text.replace('\t$(PYTHON) tools/relapse_stability.py\n', ''), encoding="utf-8")
text = js.read_text(encoding="utf-8")
text = text.replace("if ((data.ok || exploitMode === 'relapse') && mirrorTimer) {",
                    "if (data.ok && mirrorTimer) {")
text = text.replace("      if (data.kind === 'menu-ready') {\n        if (finished) return;\n        mirrorConsole(exploitMode);\n        finished = true;",
                    "      if (data.kind === 'menu-ready') {\n        finished = true;")
js.write_text(text, encoding="utf-8")
print("Relapse post-jailbreak menu staged; upstream retry and failure handling restored")
