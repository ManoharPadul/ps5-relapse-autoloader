#!/usr/bin/env python3
"""Embed the project PNG into the upstream icon SVG before rsvg-convert runs."""

from __future__ import annotations

import base64
from pathlib import Path
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: embed-icon.py <upstream-root>", file=sys.stderr)
        return 2

    upstream = Path(sys.argv[1]).resolve()
    svg_path = upstream / "assets" / "icon.svg"
    png_path = upstream / "assets" / "relapse-icon.png"
    svg = svg_path.read_text(encoding="utf-8")
    png = base64.b64encode(png_path.read_bytes()).decode("ascii")
    marker = 'href="relapse-icon.png"'
    if marker not in svg:
        raise SystemExit("icon.svg is missing the relapse-icon.png href")
    svg_path.write_text(
        svg.replace(marker, f'href="data:image/png;base64,{png}"'),
        encoding="utf-8",
    )
    print(f"Embedded {png_path.name} into {svg_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
