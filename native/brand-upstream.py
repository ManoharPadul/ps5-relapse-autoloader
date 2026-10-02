#!/usr/bin/env python3
"""Replace upstream installer-facing branding with PS5 Relapse branding."""

from __future__ import annotations

from pathlib import Path
import re
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: brand-upstream.py <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    targets = [
        root / "frontend" / "installer-page" / "index.html",
        root / "frontend" / "pointer" / "index.html",
        root / "frontend" / "autoloader" / "index.html",
        root / "frontend" / "autoloader" / "app.js",
        root / "frontend" / "autoloader" / "style.css",
        root / "assets" / "param.json.template",
        root / "include" / "wkali.h",
        root / "Makefile",
        root / "tools" / "gen_file_registry.py",
        root / "tools" / "gen_icons.py",
        root / "tools" / "gen_version.py",
        *sorted((root / "src").glob("*.c")),
        *sorted((root / "src").glob("*.h")),
    ]
    replacements = (
        ('os.environ.get("BUILD_TYPE", "dev")', 'os.environ.get("BUILD_TYPE", "stable")'),
        ("WebKit Autoloader", "PS5 Relapse AutoLoader"),
        ("PS5 Relapse AutoLoader by PLK", "PS5 Relapse AutoLoader by Manohar Padul"),
        ("by PLK (built", "by Manohar Padul (built"),
        ("github.com/itsPLK/ps5-webkit-autoloader", "github.com/ManoharPadul/ps5-relapse-autoloader"),
        ("#0f172a", "#000000"),
        ("#0b1220", "#000000"),
        (
            '@V=$$($(PYTHON) tools/gen_version.py --print); \\\n',
            '@V=$$(awk -F\'"\' \'/^#define WKAL_FULL_VERSION/{print $$2; exit}\' $(VERSION_HEADER)); \\\n'
            '\ttest -n "$$V"; \\\n',
        ),
        ('every generated asset gets a dark background and ~10% padding added.',
         'every generated asset gets a black background and ~10% padding added.'),
        ('<stop offset="0%" stop-color="#0e182b"/>',
         '<stop offset="0%" stop-color="#000000"/>'),
        ('<stop offset="100%" stop-color="#060a13"/>',
         '<stop offset="100%" stop-color="#000000"/>'),
    )

    changed = 0
    for path in targets:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        updated = text
        for old, new in replacements:
            updated = updated.replace(old, new)
        updated = re.sub(r'(#define\s+WKAL_VERSION\s+)"[^"]+"',
                         r'\1"0.3.0"', updated)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1

    print(f"Relapse branding applied to {changed} upstream files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
