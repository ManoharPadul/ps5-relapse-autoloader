#!/usr/bin/env python3
"""Add the optional Relapse menu to the upstream progress interface."""
from pathlib import Path
import shutil
import sys

source = Path(__file__).resolve().parent.parent
root = Path(sys.argv[1]).resolve()
app = root / "frontend/autoloader"
for name in ("payload-ui.js", "payload-ui.css"):
    shutil.copyfile(source / "native" / name, app / name)
shutil.copyfile(source / "payloads.js", app / "payloads.js")
shutil.copytree(source / "ui", app / "ui", dirs_exist_ok=True)
shutil.copytree(source / "payloads", app / "payloads", dirs_exist_ok=True)
page = app / "index.html"
text = page.read_text(encoding="utf-8")
if 'src="payload-ui.js"' not in text:
    text = text.replace('</head>', '<link rel="stylesheet" href="payload-ui.css" />\n</head>')
    text = text.replace('<script src="app.js"></script>',
                        '<script src="payloads.js"></script>\n'
                        '<script src="payload-ui.js"></script>\n'
                        '<script src="app.js"></script>')
    page.write_text(text, encoding="utf-8")

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
print("Relapse menu/autoload choice staged; upstream progress UI retained")
