"""Render the Marketplace page assets (banner, palette strip, icon strip).

Everything is composed in small HTML files and screenshot with headless Edge,
so the assets get real typography and CSS gradients even though the Marketplace
page itself strips styles.  Output PNGs land in build/assets/ and are meant to
be uploaded through the Marketplace page editor; the returned URLs go into
docs/marketplace-page.html.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ICON_DIR = ROOT / "src" / "main" / "resources" / "icons" / "vs"
OUT = ROOT / "build" / "assets"
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

CHROME = ["#1C1C1C", "#262626", "#282828", "#1E1E1E", "#141414"]
ACCENTS = ["#51B3FF", "#67B466", "#E8C46A", "#B47AD8", "#4EC9B0", "#D69D85"]
ICONS = [
    "folder", "Csharp", "csProject", "csLibraryProject", "solutionFile",
    "json", "markdown", "http", "image", "save", "run", "debug", "breakpoint",
]

BASE_CSS = """
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #1E1E1E; font-family: 'Segoe UI', 'Segoe UI Variable', sans-serif; }
"""

BANNER = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>""" + BASE_CSS + """
  body { width: 1200px; height: 300px; overflow: hidden; }
  .wrap { width: 1200px; height: 300px; position: relative;
          background: linear-gradient(135deg, #141414 0%, #1E1E1E 45%, #262626 100%); }
  .edge { position: absolute; left: 0; top: 0; width: 6px; height: 300px;
          background: linear-gradient(#51B3FF, #007ACC); }
  h1 { position: absolute; left: 56px; top: 74px; font-size: 58px; font-weight: 650;
       color: #F0F0F0; letter-spacing: -0.5px; }
  h1 .sharp { color: #67B466; }
  p.sub { position: absolute; left: 58px; top: 152px; font-size: 23px; color: #9A9A9A; }
  p.sub b { color: #C8C8C8; font-weight: 600; }
  .chips { position: absolute; left: 58px; top: 208px; display: flex; gap: 12px; }
  .chip { width: 64px; }
  .chip .c { height: 30px; border-radius: 6px; border: 1px solid #3F3F46; }
  .chip .l { text-align: center; font-size: 9.5px; color: #6F6F6F; margin-top: 3px;
             letter-spacing: 0.3px; }
  .tile { position: absolute; right: 64px; top: 70px; width: 150px; height: 150px;
          border-radius: 18px; background: #1C1C1C; border: 1px solid #3F3F46;
          display: flex; align-items: center; justify-content: center; }
  .tile span { font-size: 64px; font-weight: 700; color: #67B466; letter-spacing: 2px; }
  .tile small { position: absolute; right: 14px; bottom: 10px; width: 26px; height: 26px;
                border-radius: 7px; background: #B47AD8; }
</style></head><body>
  <div class="wrap">
    <div class="edge"></div>
    <h1><span class="sharp">Sharp</span> Studio Dark</h1>
    <p class="sub">The <b>Visual Studio 2026</b> look for JetBrains Rider</p>
    <div class="chips">__CHIPS__</div>
    <div class="tile"><span>C#</span><small></small></div>
  </div>
</body></html>
"""

PALETTE = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>""" + BASE_CSS + """
  body { width: 1200px; height: 170px; overflow: hidden; }
  .wrap { width: 1200px; height: 170px; background: #1E1E1E; padding: 22px 40px; }
  h2 { font-size: 17px; color: #9A9A9A; font-weight: 600; margin-bottom: 16px;
       letter-spacing: 0.3px; }
  .row { display: flex; gap: 18px; }
  .sw { flex: 1; border-radius: 9px; border: 1px solid #333333; overflow: hidden; }
  .sw .c { height: 52px; }
  .sw .l { background: #262626; padding: 7px 10px; }
  .sw .l b { display: block; font-size: 12.5px; color: #DCDCDC; font-weight: 600; }
  .sw .l i { font-style: normal; font-size: 11px; color: #7A7A7A; }
</style></head><body>
  <div class="wrap">
    <h2>Editor palette &mdash; the colours you already read every day</h2>
    <div class="row">__SWATCHES__</div>
  </div>
</body></html>
"""

ICONS_TEMPLATE = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>""" + BASE_CSS + """
  body { width: 1200px; height: 150px; overflow: hidden; }
  .wrap { width: 1200px; height: 150px; background: #1E1E1E; padding: 20px 40px; }
  h2 { font-size: 17px; color: #9A9A9A; font-weight: 600; margin-bottom: 14px; }
  .row { display: flex; gap: 22px; align-items: center; }
  .cell { width: 54px; height: 54px; border-radius: 10px; background: #282828;
          border: 1px solid #3A3A3A; display: flex; align-items: center; justify-content: center; }
  .cell svg, .cell img { width: 36px; height: 36px; }
</style></head><body>
  <div class="wrap">
    <h2>210 icons drawn in the Visual Studio language</h2>
    <div class="row">__CELLS__</div>
  </div>
</body></html>
"""


def chips_html() -> str:
    cells = []
    for colour in CHROME + ACCENTS:
        cells.append(
            f'<div class="chip"><div class="c" style="background:{colour}"></div>'
            f'<div class="l">{colour.upper()}</div></div>'
        )
    return "".join(cells)


def swatches_html() -> str:
    data = [
        ("Keywords", "#569CD6"), ("Strings", "#D69D85"), ("Numbers", "#B5CEA8"),
        ("Types", "#4EC9B0"), ("Methods", "#DCDCAA"), ("Comments", "#57A64A"),
        ("Constants", "#4FC1FF"), ("Editor", "#1E1E1E"), ("Selection", "#264F78"),
    ]
    cells = []
    for label, colour in data:
        cells.append(
            f'<div class="sw"><div class="c" style="background:{colour}"></div>'
            f'<div class="l"><b>{label}</b><i>{colour}</i></div></div>'
        )
    return "".join(cells)


def icon_cells() -> str:
    """Icon cells as <img src="data:..."> -- headless Edge does not reliably lay
    out inline <svg> elements without explicit pixel sizes, but data-URI images
    render exactly like they will on the Marketplace page."""
    import base64

    cells = []
    for name in ICONS:
        path = ICON_DIR / f"{name}.svg"
        if not path.exists():
            continue
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        cells.append(f'<div class="cell"><img src="data:image/svg+xml;base64,{data}"/></div>')
    return "".join(cells)


def shoot(html: str, size: str, name: str) -> None:
    page = OUT / f"{name}.html"
    page.write_text(html, encoding="utf-8")
    target = OUT / f"{name}.png"
    # Edge sometimes exits before the file lands when launched repeatedly in a
    # row from subprocess; retry a few times and check the output exists.
    for attempt in range(4):
        subprocess.run(
            [str(EDGE), "--headless=new", "--disable-gpu", "--hide-scrollbars",
             f"--screenshot={target}", f"--window-size={size}", page.as_uri()],
            capture_output=True, timeout=90,
        )
        if target.exists():
            print(f"  {target}  ({target.stat().st_size / 1024:.0f} KB)")
            return
    raise SystemExit(f"Edge did not write {target}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    print("rendering marketplace assets ->", OUT)
    shoot(BANNER.replace("__CHIPS__", chips_html()), "1200,300", "banner")
    shoot(PALETTE.replace("__SWATCHES__", swatches_html()), "1200,170", "palette")
    shoot(ICONS_TEMPLATE.replace("__CELLS__", icon_cells()), "1200,150", "icons")


if __name__ == "__main__":
    main()
