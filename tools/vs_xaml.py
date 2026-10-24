"""Convert the real Visual Studio icon library (XAML) into SVG.

The workspace ships the authentic Visual Studio icon set next to this
project: ``../xaml/*.xaml`` (the vector sources) and ``../png/*.16.16.png``
(the rendered result of those sources, used as ground truth).

Library layout
--------------

The assets are WPF drawings in a 16x16 space that map one-to-one onto SVG.
The common shape is::

    <Viewbox Width="16" Height="16">
      <Canvas Width="16" Height="16">
        <Path Data="M 5,1 C ..." Fill="#11910D"/>
      </Canvas>
    </Viewbox>

Variants that also occur:

``<GeometryDrawing Brush="..." Geometry="...">``
    A path whose geometry lives in a ``Geometry`` attribute.  402 assets.

``<Rectangle>`` + ``<DrawingBrush>`` + ``<DrawingGroup>``
    65 assets paint into a brush instead of a canvas.  The geometry is
    identical, only the nesting differs, so the rectangle itself is
    dropped and the contained drawings are emitted.

``<LinearGradientBrush>`` + ``<GradientStop>``
    3 assets fill a path with a gradient.

``<Pen>``
    One asset strokes a geometry.  Supported.

``UIElement.Opacity``
    14 assets dim part of the drawing.  The attribute may sit on the
    shape itself or on a container (``Grid``/``Canvas``), in which case it
    applies to everything inside that container.

``{StaticResource name}`` / ``{DynamicResource name}``
    3 assets reference a brush.  ``StaticResource`` resolves against the
    file's own ``FrameworkElement.Resources``; ``DynamicResource`` resolves
    against the Visual Studio shell palette (the values the shipped PNGs
    were rendered with).

Colours
-------

The library ships the *light-theme* palette: the neutral artwork is dark
(``#202020``) because it is drawn on a white page.  A dark theme needs the
opposite, so every colour runs through the tables below.

* :data:`RECOLOR` maps the chromatic colours one by one.  They carry
  meaning -- the C# green, the folder gold, the error red -- and Visual
  Studio keeps them recognisable in the dark theme.
* :data:`NEUTRAL_RAMP` maps the greys.  A neutral is a shade between the
  white page and the near-black outline; in the dark theme the same shade
  sits between the ``#1E1E1E`` background and the light outline, so the
  ramp is reversed.
* :data:`KEEP` lists colours that are already correct for the dark theme.

The policy can be switched off (``recolor=False``), which produces the
library's original light-theme artwork.  That is what the validator in
``tools/validate_vs_icons.py`` compares against the shipped PNGs.

Sizing
------

Most assets are 16x16, but the library also ships 7x16 VCS overlay badges
and a few 11x11 / 12x12 status glyphs.  The canvas size is read from the
XAML and used verbatim, so a badge stays a badge instead of being squashed
into a square.
"""
from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
XAML_DIR = ROOT.parent / "xaml"
PNG_DIR = ROOT.parent / "png"

# --------------------------------------------------------------------------
# colour policy
# --------------------------------------------------------------------------

#: The Visual Studio dark-theme background the icons sit on.
DARK_SURFACE = "#1E1E1E"

#: Colours the Visual Studio dark theme keeps unchanged.
KEEP: frozenset[str] = frozenset({
    "FFFFFF", "F6F6F6", "F4F4F4", "F2F2F2", "F0EFF1", "DFDFDF", "DADADA",
    "CECECE", "C1C1C1", "BFBFBF", "BABABA", "B4B4B4", "B3B3B3", "A7A7A7",
    "A3A3A3", "949494", "8F8F8F", "848484", "818181", "7A7A7A", "767676",
    "6E6E6A", "6A6A6A", "5B5B5B", "555555", "545454", "4F4F4F", "474747",
    "444444", "424242", "343434",
})

#: Light-theme colour -> Visual Studio dark-theme colour.
#:
#: The chromatic colours of the library.  They are mapped by hand because
#: each one is a brand colour with a fixed meaning; the values are the ones
#: Visual Studio uses in its own dark theme.
RECOLOR: dict[str, str] = {
    # -- Visual Studio blue / accent ---------------------------------------
    "006CBF": "51B3FF",
    "0078D4": "4CC2FF",
    "0072C6": "4CB8F0",
    "007ACC": "4CB8F0",
    "00529C": "3E9FD6",
    "005BA1": "3E9FD6",
    "005DBD": "4CB8F0",
    "005DBA": "4CB8F0",
    "00BCF2": "3BC8F5",
    "0BCF2A": "4CD44A",
    # -- C# / .NET green ---------------------------------------------------
    "11910D": "6BB700",
    "207245": "3CC46B",
    # -- folder gold -------------------------------------------------------
    "B27C00": "E8C46A",
    "FCB714": "F5CE55",
    "F2C661": "F5CE55",
    "DCB67A": "E8C46A",
    # -- error / danger red ------------------------------------------------
    "C50F1F": "F15262",
    "F05133": "F5634B",
    # -- JavaScript orange -------------------------------------------------
    "DE590B": "F68D50",
    "F28300": "F68D50",
    # -- solution / C++ purple --------------------------------------------
    "9529C2": "C58CE8",
    "5C2E91": "A87BD6",
    "A33FB1": "C77BDA",
    "8661C5": "B493E4",
    "A67AF4": "C0A0F0",
    "673C81": "9A6BB8",
    "772D3F": "B05266",
    "772D40": "B05266",
    "6B2E8C": "A87BD6",
    # -- teal / azure ------------------------------------------------------
    "159195": "4EC9B0",
    "20AC9D": "43C7B7",
    "258277": "3DAE9F",
    "37C2B1": "4ED4C2",
    "32BEDD": "4CD1EF",
    "32D4F5": "4EDAF9",
    "2FA2C8": "3FB2D8",
    "3487C7": "6FA8DC",
    # -- pink / magenta ----------------------------------------------------
    "E43BA6": "F27EC8",
    "672079": "C160C0",
    "00178F": "3A5BC4",
    # -- other brand colours -----------------------------------------------
    "5856D6": "9184EE",
    "7719AA": "A67AF4",
    "D24726": "F5634B",
    "A4262C": "F15262",
    "0C2340": "4A5E8A",
}

#: Neutral (grey) ramp: light-theme grey -> Visual Studio dark-theme grey.
#:
#: The library draws with a single neutral ramp between the white page and
#: the near-black outline.  The dark theme uses the same ramp between the
#: ``#1E1E1E`` background and the light outline, i.e. reversed.  The
#: anchors are the greys that actually occur in the library.
NEUTRAL_RAMP: tuple[tuple[int, int], ...] = (
    (0x00, 0xFF),   # pure black outline  -> pure white outline
    (0x1B, 0xF6),
    (0x20, 0xF0),   # #202020, the workhorse outline
    (0x30, 0xEC),
    (0x40, 0xDE),
    (0x50, 0xD2),
    (0x60, 0xC6),
    (0x70, 0xB6),
    (0x80, 0xA6),
    (0x90, 0x96),
    (0xA0, 0x86),
    (0xB0, 0x76),
    (0xC0, 0x66),
    (0xD0, 0x5A),
    (0xE0, 0x50),
    (0xF0, 0x42),
    (0xFF, 0x1E),   # white page -> the dark background
)

#: Values the Visual Studio shell supplies for the dynamic resources the
#: library uses.  Taken from the shipped PNGs, which are the shell's own
#: rendering of those resources.
THEME_RESOURCES: dict[str, tuple[str, float]] = {
    "light-lightblue": ("#006CBF", 1.0),
    "light-lightblue-10": ("#006CBF", 0.1),
    "light-blue": ("#006CBF", 1.0),
    "canvas": ("#FFFFFF", 0.0),
}

#: The WPF colour keywords the library actually uses.  WPF resolves these
#: against the standard X11-ish palette rather than the system theme, so
#: they are pinned here.
NAMED_COLOURS: dict[str, str] = {
    "White": "FFFFFF",
    "Black": "000000",
    "Transparent": "000000",
    "Gray": "808080",
    "Grey": "808080",
    "LightGray": "D3D3D3",
    "DarkGray": "A9A9A9",
    "Red": "FF0000",
    "Green": "008000",
    "Blue": "0000FF",
    "Yellow": "FFFF00",
    "Orange": "FFA500",
    "Purple": "800080",
    "Silver": "C0C0C0",
    "Maroon": "800000",
    "Navy": "000080",
    "Teal": "008080",
    "Olive": "808000",
    "Lime": "00FF00",
    "Aqua": "00FFFF",
    "Cyan": "00FFFF",
    "Fuchsia": "FF00FF",
    "Magenta": "FF00FF",
}


class ConversionError(RuntimeError):
    """Raised when an asset cannot be turned into an SVG."""


# --------------------------------------------------------------------------
# small helpers
# --------------------------------------------------------------------------
def _local(name: str) -> str:
    """Strip the XML namespace and any ``Prefix.`` decoration from a name."""
    return name.rsplit("}", 1)[-1].rsplit(".", 1)[-1]


def _attr(elem: ET.Element, name: str) -> str | None:
    """Read an attribute by local name, ignoring the XML namespace."""
    for key, value in elem.attrib.items():
        if key == name or _local(key) == name:
            return value
    return None


def _child(elem: ET.Element, name: str) -> ET.Element | None:
    for child in elem:
        if _local(child.tag) == name:
            return child
    return None


def _ancestor_opacity(elem: ET.Element, parent_of: dict) -> float:
    """The opacity contributed by the containers around ``elem``.

    WPF's ``UIElement.Opacity`` on a container dims everything inside it, so
    a ``<Grid UIElement.Opacity="0.1">`` has to dim its children too.  The
    tree is walked upwards, which is why the parent map has to be available.
    """
    total = 1.0
    parent = parent_of.get(elem)
    while parent is not None:
        total *= _float(_attr(parent, "UIElement.Opacity"), 1.0)
        parent = parent_of.get(parent)
    return total


def _float(value: str | None, default: float = 1.0) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    raw = value.lstrip("#").upper()
    if len(raw) == 8:
        raw = raw[2:]
    if len(raw) != 6:
        raise ConversionError(f"bad colour {value!r}")
    return int(raw[0:2], 16), int(raw[2:4], 16), int(raw[4:6], 16)


def _rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    """Format a colour as bare ``RRGGBB`` hex (no leading ``#``)."""
    return "%02X%02X%02X" % rgb


def _neutral_to_dark(value: int) -> int:
    """Map a neutral grey through :data:`NEUTRAL_RAMP`."""
    ramp = NEUTRAL_RAMP
    if value <= ramp[0][0]:
        return ramp[0][1]
    for (lo, out_lo), (hi, out_hi) in zip(ramp, ramp[1:]):
        if lo <= value <= hi:
            span = hi - lo
            t = (value - lo) / span if span else 0.0
            return round(out_lo + t * (out_hi - out_lo))
    return ramp[-1][1]


def _recolour(hex6: str) -> str:
    """Apply the dark-theme colour policy to a ``#RRGGBB`` colour."""
    key = hex6.upper()
    if key in RECOLOR:
        return RECOLOR[key]
    if key in KEEP:
        return key
    r, g, b = _hex_to_rgb(key)
    if r == g == b:
        return _rgb_to_hex((_neutral_to_dark(r),) * 3)
    return key


def _paint(value: str, recolor: bool) -> tuple[str, float] | None:
    """Resolve a brush reference to ``(paint, opacity)``."""
    value = value.strip()
    if value.startswith("{"):
        return None                     # resource references are resolved earlier
    if not value.startswith("#"):
        named = NAMED_COLOURS.get(value)
        if named is None:
            return None
        if named == "000000" and value == "Transparent":
            return None                 # fully transparent -> nothing to paint
        if recolor:
            named = _recolour(named)
        return "#" + named, 1.0
    raw = value.lstrip("#").upper()
    if len(raw) == 8:
        alpha, body = raw[:2], raw[2:]
    elif len(raw) == 6:
        alpha, body = "FF", raw
    else:
        return None
    if alpha == "00":
        return None                     # fully transparent -> nothing to paint
    opacity = int(alpha, 16) / 255.0
    if recolor:
        body = _recolour(body)
    return "#" + body, opacity


# --------------------------------------------------------------------------
# resources
# --------------------------------------------------------------------------
def _collect_resources(root: ET.Element) -> tuple[dict[str, tuple[str, float]], dict[str, dict]]:
    """Read ``FrameworkElement.Resources`` into brush and gradient tables."""
    brushes: dict[str, tuple[str, float]] = {}
    gradients: dict[str, dict] = {}

    for elem in root.iter():
        tag = _local(elem.tag)
        if tag not in ("SolidColorBrush", "LinearGradientBrush"):
            continue
        key = _attr(elem, "x:Key") or _attr(elem, "Key")
        if not key:
            continue
        if tag == "SolidColorBrush":
            colour = _attr(elem, "Color")
            if not colour:
                continue
            opacity = _float(_attr(elem, "Opacity"), 1.0)
            painted = _paint(colour, False)
            if painted is None:
                brushes[key] = ("#000000", 0.0)
                continue
            brushes[key] = (painted[0], opacity * painted[1])
        else:
            start = _attr(elem, "StartPoint") or "0,0"
            end = _attr(elem, "EndPoint") or "1,1"
            stops = []
            for stop in elem:
                if _local(stop.tag) != "GradientStop":
                    continue
                colour = _attr(stop, "Color") or "#000000"
                offset = _float(_attr(stop, "Offset"), 0.0)
                painted = _paint(colour, False)
                if painted is None:
                    continue
                stops.append((offset, painted[0], painted[1]))
            gradients[key] = {
                "start": start,
                "end": end,
                "stops": stops,
                "absolute": (_attr(elem, "MappingMode") or "") == "Absolute",
            }
    return brushes, gradients


def _resolve(value: str, brushes, gradients, recolor: bool) -> tuple[str, float] | None:
    """Resolve a ``Fill``/``Brush`` attribute to ``(paint, opacity)``."""
    value = value.strip()
    if value.startswith("{"):
        body = value.strip("{}")
        kind, _, name = body.partition(" ")
        name = name.strip()
        if kind == "StaticResource":
            if name in gradients:
                return f"url(#{_grad_id(name)})", 1.0
            if name in brushes:
                paint, opacity = brushes[name]
                if recolor and paint.startswith("#"):
                    paint = _recolour(paint[1:]).join(("#", ""))
                return paint, opacity
            return None
        if kind == "DynamicResource":
            if name in THEME_RESOURCES:
                paint, opacity = THEME_RESOURCES[name]
                if recolor and paint.startswith("#"):
                    paint = _recolour(paint[1:]).join(("#", ""))
                return paint, opacity
            if name in brushes:
                paint, opacity = brushes[name]
                if recolor and paint.startswith("#"):
                    paint = _recolour(paint[1:]).join(("#", ""))
                return paint, opacity
            if name in gradients:
                return f"url(#{_grad_id(name)})", 1.0
        return None
    return _paint(value, recolor)


def _grad_id(key: str) -> str:
    safe = "".join(ch if ch.isalnum() else "_" for ch in key)
    return f"g{abs(hash(key)) % 100000}_{safe}"


# --------------------------------------------------------------------------
# geometry
# --------------------------------------------------------------------------
def _geometry(data: str) -> tuple[str, str]:
    """XAML geometry -> ``(path data, fill-rule)``; the syntax is SVG-ready.

    WPF prefixes the path with ``F0`` (even-odd) or ``F1`` (non-zero) to
    select the fill rule.  Only 435 of the 4090 assets spell the prefix
    out; the rest rely on WPF's default, which is *even-odd* -- the
    opposite of SVG's *non-zero* default.  Anything that is not spelled
    out therefore has to carry ``fill-rule="evenodd"`` explicitly, or
    every shape with a hole in it (a folder with a tab, a letter tile)
    fills in solid.
    """
    data = data.strip()
    rule = ""
    if data[:2] in ("F0", "F1"):
        rule = ' fill-rule="evenodd"' if data[:2] == "F0" else ""
        data = data[3:].strip()
    else:
        rule = ' fill-rule="evenodd"'
    return data, rule


def _canvas_size(root: ET.Element) -> tuple[float, float]:
    """The size of the drawing surface, read from the XAML."""
    width = _attr(root, "Width")
    height = _attr(root, "Height")
    if width and height:
        return _float(width, 16.0), _float(height, 16.0)
    for elem in root.iter():
        if _local(elem.tag) == "Canvas":
            cw = _attr(elem, "Width")
            ch = _attr(elem, "Height")
            if cw and ch:
                return _float(cw, 16.0), _float(ch, 16.0)
    return 16.0, 16.0


def _num(value: float) -> str:
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:g}"


# --------------------------------------------------------------------------
# conversion
# --------------------------------------------------------------------------
def convert(text: str, *, recolor: bool = True) -> str:
    """Convert one Visual Studio XAML asset into an SVG document."""
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        raise ConversionError(f"not valid XML: {exc}") from exc

    brushes, gradients = _collect_resources(root)
    width, height = _canvas_size(root)

    parent_of: dict[ET.Element, ET.Element | None] = {}
    for parent in root.iter():
        for child in parent:
            parent_of[child] = parent

    defs: list[str] = []
    body: list[str] = []
    used_gradients: set[str] = set()

    for elem in root.iter():
        tag = _local(elem.tag)
        if tag == "Path":
            data = _attr(elem, "Data")
            fill = _attr(elem, "Fill")
            opacity = _float(_attr(elem, "UIElement.Opacity"), 1.0)
            stroke, stroke_width = None, None
        elif tag == "GeometryDrawing":
            data = _attr(elem, "Geometry")
            fill = _attr(elem, "Brush")
            opacity = 1.0
            pen = _child(elem, "Pen")
            stroke, stroke_width = None, None
            if pen is not None:
                pen_brush = _attr(pen, "Brush")
                if pen_brush:
                    resolved = _resolve(pen_brush, brushes, gradients, recolor)
                    if resolved is not None:
                        stroke = resolved[0]
                stroke_width = _attr(pen, "Thickness")
        else:
            continue

        # A container's opacity dims every shape inside it.
        opacity *= _ancestor_opacity(elem, parent_of)

        if not data or not data.strip() or not fill:
            continue
        resolved = _resolve(fill, brushes, gradients, recolor)
        if resolved is None:
            continue
        paint, alpha = resolved
        if paint.startswith("url(#"):
            used_gradients.add(paint[5:-1])

        d, rule = _geometry(data)
        if not d:
            continue

        attrs = [f'd="{d}"', f'fill="{paint}"']
        if rule:
            attrs.append(rule.strip())
        if alpha < 0.999:
            attrs.append(f'fill-opacity="{_num(round(alpha, 3))}"')
        if stroke:
            attrs.append(f'stroke="{stroke}"')
            attrs.append(f'stroke-width="{_num(_float(stroke_width, 1.0))}"')
        if opacity < 0.999:
            attrs.append(f'opacity="{_num(round(opacity, 3))}"')
        body.append(f'<path {" ".join(attrs)}/>')

    if not body:
        raise ConversionError("no drawable shapes found")

    for key, gradient in gradients.items():
        gid = _grad_id(key)
        if gid not in used_gradients:
            continue
        x1, y1 = (gradient["start"] + ",").split(",")[:2]
        x2, y2 = (gradient["end"] + ",").split(",")[:2]
        units = ' gradientUnits="userSpaceOnUse"' if gradient["absolute"] else ""
        stops = "".join(
            f'<stop offset="{_num(round(offset, 4))}" stop-color="{colour}"'
            + (f' stop-opacity="{_num(round(alpha, 3))}"' if alpha < 0.999 else "")
            + "/>"
            for offset, colour, alpha in gradient["stops"]
        )
        defs.append(
            f'<linearGradient id="{gid}"{units} x1="{_num(float(x1))}" y1="{_num(float(y1))}"'
            f' x2="{_num(float(x2))}" y2="{_num(float(y2))}">{stops}</linearGradient>'
        )

    head = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{_num(width)}" '
        f'height="{_num(height)}" viewBox="0 0 {_num(width)} {_num(height)}">'
    )
    if defs:
        head += "<defs>" + "".join(defs) + "</defs>"
    return head + "".join(body) + "</svg>"


def convert_file(path: Path, *, recolor: bool = True) -> str:
    """Convert the XAML asset at ``path`` into an SVG document."""
    return convert(path.read_text(encoding="utf-8", errors="ignore"), recolor=recolor)


def available_assets(directory: Path = XAML_DIR) -> list[str]:
    """The stems of every XAML asset in the library, sorted."""
    if not directory.is_dir():
        return []
    return sorted(path.stem for path in directory.glob("*.xaml"))


def main() -> None:
    """Convert a single asset -- handy while checking the library."""
    import argparse

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("asset", help="asset stem, e.g. csfile")
    ap.add_argument("--light", action="store_true",
                    help="keep the library's light-theme colours")
    ap.add_argument("--out", help="write the SVG to this file")
    args = ap.parse_args()

    source = XAML_DIR / f"{args.asset}.xaml"
    if not source.exists():
        raise SystemExit(f"{source} not found")
    svg = convert_file(source, recolor=not args.light)
    if args.out:
        Path(args.out).write_text(svg + "\n", encoding="utf-8")
    else:
        print(svg)


if __name__ == "__main__":
    main()
