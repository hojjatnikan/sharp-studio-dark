"""Sample the exact Visual Studio 2022 dark-theme palette from a screenshot.

Uses the modal (most frequent) colour inside each named rectangle so that text
antialiasing does not skew the reading, and dumps crops of the interesting
regions for visual reference.
"""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from PIL import Image

# name -> (x0, y0, x1, y1) in pixels of a 1908x1037 screenshot
REGIONS = {
    "titlebar":            (880, 8, 1080, 22),
    "menubar_text":        (24, 8, 40, 22),
    "toolbar_row":         (860, 34, 1060, 48),
    "toolbar_row2":        (980, 56, 1180, 70),
    "tabstrip_empty":      (1180, 82, 1380, 98),
    "tab_active":          (620, 82, 700, 98),
    "tab_inactive":        (300, 82, 360, 98),
    "editor_bg":           (600, 380, 900, 440),
    "gutter_bg":           (8, 380, 55, 440),
    "panel_bg":            (1740, 660, 1860, 700),
    "panel_search":        (1560, 130, 1880, 145),
    "panel_header_text":   (1520, 66, 1600, 80),
    "stripe_right":        (1900, 300, 1907, 500),
    "bottom_tabs":         (900, 982, 1000, 995),
    "statusbar":           (600, 1020, 900, 1032),
    "statusbar_left":      (0, 1020, 60, 1032),
    "solution_root":       (1522, 148, 1560, 162),
}


def modal_color(im: Image.Image, box: tuple[int, int, int, int]) -> str:
    crop = im.crop(box).convert("RGB")
    counts = Counter(crop.getdata())
    color, hits = counts.most_common(1)[0]
    total = crop.width * crop.height
    return f"#{color[0]:02X}{color[1]:02X}{color[2]:02X}  ({hits}/{total} px)"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--crops", help="directory to write reference crops into")
    args = ap.parse_args()

    im = Image.open(args.image)
    print(f"image: {im.size[0]}x{im.size[1]}")
    for name, box in REGIONS.items():
        print(f"  {name:20s} {box}  ->  {modal_color(im, box)}")

    if args.crops:
        out = Path(args.crops)
        out.mkdir(parents=True, exist_ok=True)
        crops = {
            "solution_explorer": (1516, 60, 1908, 560),
            "toolbar": (0, 30, 760, 80),
            "titlebar": (0, 0, 1000, 30),
            "tabs_and_statusbar": (540, 78, 1460, 104),
            "bottom_bar": (0, 975, 1250, 1037),
        }
        for name, box in crops.items():
            im.crop(box).resize(((box[2] - box[0]) * 2, (box[3] - box[1]) * 2), Image.LANCZOS).save(
                out / f"{name}.png"
            )
            print(f"  crop -> {out / f'{name}.png'}")


if __name__ == "__main__":
    main()
