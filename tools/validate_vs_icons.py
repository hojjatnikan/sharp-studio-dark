"""Prove the XAML -> SVG conversion against the shipped Visual Studio PNGs.

The library ships both the vector sources (``../xaml``) and the rendered
result (``../png``).  That makes it possible to *measure* the converter
instead of trusting it: convert every asset, rasterise the SVG, and compare
it with the PNG Visual Studio shipped.

    python tools/validate_vs_icons.py            # summary
    python tools/validate_vs_icons.py --show 30  # the worst offenders
    python tools/validate_vs_icons.py --asset csfile --dump

How it works
------------

Rasterising 4090 SVGs one browser launch at a time would take hours, so the
assets are laid out into a single HTML grid per icon size and screenshotted
once.  Each cell is exactly one icon wide, so the screenshot pixels line up
one-to-one with the shipped PNG pixels and can be compared directly.

The comparison runs with ``recolor=False`` (the library's own light-theme
colours) because the PNGs are the light-theme rendering.  The dark-theme
recolour is a separate, hand-verified step.

Rasterisation uses headless Edge, the same Skia renderer the IDE uses, so
the result reflects what the plugin will really show.
"""
from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageChops

import vs_xaml

EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
XAML_DIR = vs_xaml.XAML_DIR
PNG_DIR = vs_xaml.PNG_DIR
OUT_DIR = vs_xaml.ROOT / "build" / "validate"

#: Mean per-channel difference above which an asset counts as a mismatch.
#: The browser and Visual Studio anti-alias slightly differently, so a
#: handful of edge pixels will never line up exactly; the shape and the
#: colours still have to.
MEAN_TOLERANCE = 6.0

#: A single channel may differ by this much before it is noticed at all.
PEAK_TOLERANCE = 90

_COLUMNS = 32


def _svg_size(svg: str) -> tuple[int, int]:
    """The canvas size the converter produced for an asset."""
    head = svg[: svg.index(">")]
    width = int(head.split('width="', 1)[1].split('"', 1)[0])
    height = int(head.split('height="', 1)[1].split('"', 1)[0])
    return width, height


def _png_for(stem: str, canvas: tuple[int, int]) -> Path | None:
    """The shipped PNG that renders an asset at its native canvas size.

    The library ships several renderings of the same icon (10, 12, 16, 32
    pixels, ...).  Comparing an SVG against the wrong size would flag a
    perfectly good asset as broken, so the twin matching the XAML canvas is
    preferred and the closest remaining size is used as a fallback.
    """
    matches = sorted(PNG_DIR.glob(f"{stem}.*.png"))
    if not matches:
        return None
    exact = PNG_DIR / f"{stem}.{canvas[0]}.{canvas[1]}.png"
    if exact.exists():
        return exact
    def distance(path: Path) -> tuple[int, int, str]:
        with Image.open(path) as handle:
            size = handle.size
        return abs(size[0] - canvas[0]) + abs(size[1] - canvas[1]), size[0], path.name
    return min(matches, key=distance)


def _html(cells: list[tuple[str, str, tuple[int, int]]], size: tuple[int, int]) -> str:
    """An HTML grid holding one inline SVG per cell.

    Each cell is rendered at the size of the shipped PNG but keeps the
    viewBox of the XAML canvas, so a 12x12 canvas shipped as a 16x16 PNG is
    scaled up exactly the way Visual Studio scaled it up.
    """
    width, height = size
    body = "".join(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {canvas[0]} {canvas[1]}">{markup}</svg>'
        for _stem, markup, canvas in cells
    )
    return (
        "<!doctype html><meta charset=utf-8>"
        "<style>html,body{margin:0;padding:0;background:transparent;}"
        f"div{{display:grid;grid-template-columns:repeat({_COLUMNS},{width}px);"
        f"width:max-content;line-height:0}}svg{{display:block}}</style>"
        f"<div>{body}</div>"
    )


def _shoot(html: str, width: int, height: int) -> Image.Image:
    """Screenshot an HTML page with headless Edge."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        source = tmp_path / "grid.html"
        source.write_text(html, encoding="utf-8")
        target = tmp_path / "grid.png"
        subprocess.run(
            [str(EDGE), "--headless=new", "--disable-gpu", "--hide-scrollbars",
             "--force-device-scale-factor=1", "--default-background-color=00000000",
             f"--screenshot={target}", f"--window-size={width},{height}",
             source.as_uri()],
            capture_output=True, timeout=300,
        )
        if not target.exists():
            raise RuntimeError("Edge did not produce a screenshot")
        return Image.open(target).convert("RGBA")


def _compare(expected: Image.Image, actual: Image.Image) -> tuple[float, int]:
    """Return ``(mean difference, peak difference)`` for two renderings.

    Both images are straight-alpha RGBA, so they are compared in
    premultiplied space: a pixel that is transparent in one image and opaque
    in the other is a real difference and must count.
    """
    if expected.size != actual.size:
        actual = actual.resize(expected.size, Image.LANCZOS)

    def premultiplied(image: Image.Image) -> Image.Image:
        bands = image.convert("RGBA").split()
        red, green, blue, alpha = bands
        return Image.merge("RGB", [
            ImageChops.multiply(channel, alpha)
            for channel in (red, green, blue)
        ])

    diff = ImageChops.difference(
        premultiplied(expected), premultiplied(actual)
    )
    bands = diff.split()
    peak = max(band.getextrema()[1] for band in bands)
    total = sum(sum(band.getdata()) for band in bands)
    mean = total / (expected.width * expected.height * 3)
    return mean, peak


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--asset", help="check a single asset")
    ap.add_argument("--show", type=int, default=30, help="how many bad assets to list")
    ap.add_argument("--limit", type=int, default=0, help="stop after N assets")
    ap.add_argument("--dump", action="store_true",
                    help="write side-by-side comparison images into build/validate")
    args = ap.parse_args()

    if not EDGE.exists():
        raise SystemExit(f"{EDGE} not found -- cannot rasterise")

    stems = [args.asset] if args.asset else vs_xaml.available_assets()
    if args.limit:
        stems = stems[: args.limit]

    # Convert first: the XAML canvas decides which shipped PNG is the
    # correct ground truth for the comparison.
    groups: dict[tuple[int, int], list[tuple[str, str, tuple[int, int]]]] = {}
    without_png: list[str] = []
    unconvertible: list[str] = []

    for stem in stems:
        try:
            svg = vs_xaml.convert_file(XAML_DIR / f"{stem}.xaml", recolor=False)
        except vs_xaml.ConversionError as exc:
            unconvertible.append(f"{stem}: {exc}")
            continue
        canvas = _svg_size(svg)
        png = _png_for(stem, canvas)
        if png is None:
            without_png.append(stem)
            continue
        with Image.open(png) as handle:
            size = handle.size
        markup = svg[svg.index(">") + 1: svg.rindex("</svg>")]
        groups.setdefault(size, []).append((stem, markup, canvas))

    results: list[tuple[str, float, int, bool]] = []
    failures: list[str] = []

    for size, group in sorted(groups.items()):
        cells = group
        columns = _COLUMNS
        rows = (len(cells) + columns - 1) // columns
        html = _html(cells, size)
        try:
            shot = _shoot(html, columns * size[0], rows * size[1])
        except Exception as exc:                                  # pragma: no cover
            failures.append(f"grid {size}: render failed -- {exc}")
            continue

        for index, (stem, _markup, canvas) in enumerate(cells):
            left = (index % columns) * size[0]
            top = (index // columns) * size[1]
            cell = shot.crop((left, top, left + size[0], top + size[1]))
            png = _png_for(stem, canvas)
            with Image.open(png) as handle:
                expected = handle.convert("RGBA")
            mean, peak = _compare(expected, cell)
            ok = mean <= MEAN_TOLERANCE and peak <= PEAK_TOLERANCE
            results.append((stem, mean, peak, ok))
            if not ok:
                failures.append(
                    f"{stem}: mean {mean:.1f} peak {peak} (size {size[0]}x{size[1]})"
                )
                if args.dump:
                    strip = Image.new("RGBA", (size[0] * 2 + 4, size[1]), (60, 60, 60, 255))
                    strip.paste(expected, (0, 0))
                    strip.paste(cell, (size[0] + 4, 0))
                    OUT_DIR.mkdir(parents=True, exist_ok=True)
                    strip.convert("RGB").save(OUT_DIR / f"{stem}.png")

    ok = [r for r in results if r[3]]
    print(f"assets checked      : {len(results)}")
    print(f"within tolerance    : {len(ok)}")
    print(f"mismatches          : {len(results) - len(ok)}")
    print(f"without a PNG twin  : {len(without_png)}")
    print(f"not convertible     : {len(unconvertible)}")
    if failures:
        print("\nfailures:")
        for line in failures[: args.show]:
            print(f"  {line}")
        if len(failures) > args.show:
            print(f"  ... and {len(failures) - args.show} more")
    if unconvertible:
        print("\nnot convertible:")
        for line in unconvertible[: args.show]:
            print(f"  {line}")
    if args.dump and OUT_DIR.is_dir():
        print(f"\ncomparison images -> {OUT_DIR}")


if __name__ == "__main__":
    main()
