#!/usr/bin/env python3
"""Create the native installer icon SVG from the project's PNG asset."""

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
    png = base64.b64encode(png_path.read_bytes()).decode("ascii")
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
  <defs>
    <clipPath id="relapseCircle">
      <circle cx="512" cy="512" r="512" />
    </clipPath>
  </defs>
  <circle cx="512" cy="512" r="512" fill="#0b1220" />
  <image href="data:image/png;base64,{png}" x="0" y="0" width="1024" height="1024"
         preserveAspectRatio="xMidYMid slice" clip-path="url(#relapseCircle)" />
</svg>
'''
    svg_path.write_text(svg, encoding="utf-8")
    print(f"Embedded {png_path.name} into {svg_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
