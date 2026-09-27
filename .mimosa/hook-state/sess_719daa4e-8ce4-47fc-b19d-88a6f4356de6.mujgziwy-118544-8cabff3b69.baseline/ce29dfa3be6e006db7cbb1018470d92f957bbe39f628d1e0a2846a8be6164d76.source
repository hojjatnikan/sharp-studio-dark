"""Render every generated icon into one HTML sheet (for visual review).

The sheet is a plain HTML file; open it in a browser or screenshot it headless:

    python tools/contact_sheet.py
    msedge --headless=new --screenshot=build/icons.png --window-size=1400,2200 build/icons.html
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ICON_DIR = ROOT / "src" / "main" / "resources" / "icons" / "vs"
OUT = ROOT / "build" / "icons.html"

TEMPLATE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
  body {{ background:#282828; color:#C8C8C8; font:12px "Segoe UI",sans-serif; margin:24px; }}
  h1 {{ font-size:15px; font-weight:600; color:#F0F0F0; margin:0 0 4px; }}
  p.note {{ color:#9A9A9A; margin:0 0 20px; }}
  .grid {{ display:grid; grid-template-columns:repeat(12,1fr); gap:14px 12px; }}
  .cell {{ text-align:center; }}
  .box {{ height:34px; display:flex; align-items:center; justify-content:center;
          background:#1E1E1E; border:1px solid #3F3F46; border-radius:4px; }}
  .box svg {{ width:28px; height:28px; }}
  .name {{ margin-top:4px; font-size:10px; color:#9A9A9A; word-break:break-all; }}
</style></head><body>
<h1>Visual Studio 2022 icon pack &mdash; {count} icons</h1>
<p class="note">rendered at 28px on the Visual Studio editor background (#1E1E1E)</p>
<div class="grid">{cells}</div>
</body></html>
"""


def main() -> None:
    icons = sorted(ICON_DIR.glob("*.svg"))
    cells = []
    for icon in icons:
        svg = icon.read_text(encoding="utf-8")
        # scale the 16px canvas up for review
        svg = svg.replace('width="16" height="16"', 'width="28" height="28"')
        cells.append(
            f'<div class="cell"><div class="box">{svg}</div>'
            f'<div class="name">{icon.stem}</div></div>'
        )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(TEMPLATE.format(count=len(icons), cells="".join(cells)), encoding="utf-8")
    print(f"wrote {OUT} ({len(icons)} icons)")


if __name__ == "__main__":
    main()
