#!/usr/bin/env python3
"""Replace upstream installer-facing branding with PS5 Relapse branding."""

from __future__ import annotations

from pathlib import Path
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: brand-upstream.py <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    targets = [
        root / "frontend" / "installer-page" / "index.html",
        root / "frontend" / "pointer" / "index.html",
        root / "assets" / "param.json.template",
        *sorted((root / "src").glob("*.c")),
        *sorted((root / "src").glob("*.h")),
    ]
    replacements = (
        ("WebKit Autoloader Installer", "PS5 Relapse Installer"),
        ("WebKit Autoloader App", "PS5 Relapse App"),
        ("WebKit Autoloader", "PS5 Relapse"),
        ("by PLK", "by ManoharPadul"),
        ("github.com/itsPLK/ps5-webkit-autoloader", "github.com/ManoharPadul/ps5-relapse-autoloader"),
    )

    changed = 0
    for path in targets:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        updated = text
        for old, new in replacements:
            updated = updated.replace(old, new)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    print(f"Relapse branding applied to {changed} upstream files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
