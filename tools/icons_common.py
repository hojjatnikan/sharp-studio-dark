"""Drawing helpers for the Visual Studio style icon pack.

Visual Studio's icon language, as observed in a real VS 2022 window:

* monochrome outline glyphs, 1.2px strokes, light grey ``#C8C8C8``;
* a handful of accent colours with fixed meaning -- blue for save/build,
  green for run/add, gold for folders, purple for C# and solution items;
* documents are grey sheets carrying a small coloured badge with a white glyph;
* language/member symbols are letter tiles, coloured by the editor syntax
  palette (types teal, methods yellow, constants light blue, ...).
"""
from __future__ import annotations

GRAY = "#C8C8C8"
GRAY_DIM = "#9A9A9A"
BLUE = "#4CA3E0"
ACCENT = "#51B3FF"
GREEN = "#6BB700"
GOLD = "#E8C46A"
PURPLE = "#B180D7"
RED = "#E5534B"
YELLOW = "#DCDCAA"
TEAL = "#4EC9B0"
LIGHTBLUE = "#4FC1FF"
ORANGE = "#E8A06A"
DARK = "#1E1E1E"
WHITE = "#FFFFFF"

# --------------------------------------------------------------------------
# a minimal stroke font, enough for the letter tiles (unit box 6 x 8)
# --------------------------------------------------------------------------
LETTERS: dict[str, str] = {
    "C": "M5.5 2.3A2.6 2.6 0 1 0 5.5 5.7",
    "I": "M3 0.9v6.2M1.7 0.9h2.6M1.7 7.1h2.6",
    "S": "M5.2 2.2C4.6 1 1.4 1 1.4 2.9c0 1.6 4 1 4 3.1 0 1.9-3.6 1.7-4.2.4",
    "E": "M5.2 1v6M5.2 1H1.3M5.2 4H1.6M5.2 7H1.3",
    "M": "M1 7V1l2.5 3.4L6 1v6",
    "P": "M1.2 7V1h2.5c2.3 0 2.3 3.3 0 3.3H1.2",
    "F": "M1.2 7V1h3.9M1.2 3.9h3.1",
    "N": "M1.2 7V1l3.6 5.6V1",
    "K": "M1.2 1v6M4.9 1L1.4 4.1l3.5 2.9",
    "V": "M1 1l2 6 2-6",
    "D": "M1.2 1v6h1.5c3 0 3-6 0-6z",
    "T": "M3 1v6M1 1h4",
    "G": "M5.5 2.3A2.6 2.6 0 1 0 5.6 5.7H3.6",
    "L": "M1.4 1v6h3.9",
    "X": "M1.1 1l3.8 6M4.9 1l-3.8 6",
    "R": "M1.2 7V1h2.3c2 0 2 3 0 3H1.2M3.5 4l2.1 3",
    "A": "M1 7l2-6 2 6M1.7 4.7h2.6",
    "B": "M1.3 1v6h2.2c2 0 2-3 0-3H1.3M1.3 4.1h2.4c2 0 2-3.1 0-3.1H1.3",
    "H": "M1.2 1v6M5 1v6M1.2 4H5",
    "O": "M3 1a2.6 2.6 0 1 0 0 6 2.6 2.6 0 0 0 0-6z",
    "J": "M4.7 1v5.1c0 1.5-1.8 1.7-2.7.5",
    "U": "M1.2 1v4.2a1.8 1.8 0 0 0 3.6 0V1",
    "W": "M.6 1l1.3 6L3 2.6 4.4 7 5.7 1",
    "?": "M1.4 2.4a2.2 2.2 0 1 1 3.3 2c-.7.4-1 .8-1 1.5v.3M3.3 7.4a.55.55 0 1 0 1.1 0 .55.55 0 1 0-1.1 0",
    "#": "M1.9 1.4l-.9 5.6M4.7 1.4l-.9 5.6M.9 3.2h4.4M.6 5.1h4.4",
    "@": "M4.3 1.5a2.3 2.3 0 1 0 1.2 4.2c.2.9-.5 1.4-1.2 1M5.7 1.9v3.4",
}


# --------------------------------------------------------------------------
# primitives
# --------------------------------------------------------------------------
def svg(*parts: str) -> str:
    return (
        '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" '
        'xmlns="http://www.w3.org/2000/svg">' + "".join(parts) + "</svg>"
    )


def path(d: str, color: str = GRAY, width: float = 1.2, fill: str = "none") -> str:
    return (
        f'<path d="{d}" stroke="{color}" stroke-width="{width}" fill="{fill}" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
    )


def text_letter(char: str, color: str, x: float, y: float, scale: float = 1.0,
                width: float = 1.0) -> str:
    """Draw one letter of the built-in stroke font."""
    d = LETTERS[char]
    return (
        f'<g transform="translate({x} {y}) scale({scale})">'
        f'<path d="{d}" stroke="{color}" stroke-width="{width / scale}" fill="none" '
        'stroke-linecap="round" stroke-linejoin="round"/></g>'
    )


def letter_centered(char: str, color: str, cx: float, cy: float, size: float = 0.62,
                    width: float = 0.9) -> str:
    """Letter centred on (cx, cy); ``size`` is the height of the glyph box (8 units)."""
    scale = size / 8.0
    return text_letter(char, color, cx - 3.0 * scale, cy - 4.0 * scale, scale, width)


def sheet(color: str = GRAY, x: float = 2.6, y: float = 1.4, w: float = 8.6,
          h: float = 13.2, fold: float = 2.6) -> str:
    """A document sheet with a folded top-right corner (Visual Studio style)."""
    body = (
        f"M{x} {y}h{w - fold}l{fold} {fold}v{h - fold}h-{w}v-{h}z"
    )
    corner = f"M{x + w - fold} {y}v{fold}h{fold}"
    return path(body, color) + path(corner, color)


def badge_outline(color: str, x: float, y: float, size: float = 6.6, r: float = 1.4,
                  fill: str = "none", width: float = 1.1) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{r}" '
        f'fill="{fill}" stroke="{color}" stroke-width="{width}"/>'
    )


def badge_filled(color: str, x: float, y: float, size: float = 6.6, r: float = 1.4) -> str:
    return badge_outline(color, x, y, size, r, fill=color, width=0)


def symbol_tile(char: str, color: str, fill_badge: bool = False) -> str:
    """A member/language symbol: rounded letter tile (Visual Studio IntelliSense look)."""
    size = 9.4
    x = y = (16 - size) / 2
    base = badge_filled(color, x, y, size, 2.0) if fill_badge else badge_outline(color, x, y, size, 2.0)
    letter_color = DARK if fill_badge else color
    return base + letter_centered(char, letter_color, 8, 8.1, 5.4, 1.0)


def file_tile(badge_color: str, glyph: str, sheet_color: str = GRAY) -> str:
    """A document sheet with a coloured badge holding a white glyph."""
    bx, by, bs = 7.2, 8.0, 7.6
    return (
        sheet(sheet_color)
        + badge_filled(badge_color, bx, by, bs, 1.6)
        + f'<g transform="translate({bx} {by}) scale({bs / 8.0})">'
        + f'<path d="{glyph}" stroke="{WHITE}" stroke-width="1.05" fill="none" '
          'stroke-linecap="round" stroke-linejoin="round"/></g>'
    )


# glyphs used inside file badges, drawn in an 8x8 box
GLYPHS: dict[str, str] = {
    "braces": "M3.2 0.7c-1.4 0-1.4 2.6-2.4 3.3 1 .7 1 2.6 2.4 2.6M4.8 0.7c1.4 0 1.4 2.6 2.4 3.3-1 .7-1 2.6-2.4 2.6",
    "angles": "M2.6 0.9L0.8 3.3l1.8 2.4M5.4 0.9l1.8 2.4-1.8 2.4",
    "lines": "M0.9 1.4h6.2M0.9 3.3h6.2M0.9 5.2h4",
    "db": "M0.9 1.6c0-1 6.2-1 6.2 0v4.4c0 1-6.2 1-6.2 0zM0.9 1.6c0 1 6.2 1 6.2 0M0.9 3.9c0 1 6.2 1 6.2 0",
    "gear": "M3.9 1.1l.5 1 .9-.2.6.6-.1.9.9.6-.9.6.1.9-.6.6-.9-.2-.5 1-.5-1-.9.2-.6-.6.1-.9-.9-.6.9-.6-.1-.9.6-.6.9.2z",
    "hash": "M2.2 0.8L1.4 5.8M4.6 0.8L3.8 5.8M0.8 2.2h6.2M0.6 4.4h6.2",
    "csharp": "M4.6 1.2A2.5 2.5 0 1 0 4.6 5.4M6.3 2.3l-2.3.5M6.6 3.9l-2.3.5",
    "at": "M4.4 1.6a2.1 2.1 0 1 0 1.1 3.8c.2.8-.5 1.2-1.1.9M5.6 1.9v3",
    "md": "M1 4.9V1.2l1.9 2.3L4.8 1.2v3.7M6.3 1.2v3.7M5 3.4h2.6",
    "arrow": "M0.9 3.4h6.2M4.6 1.1l2.5 2.3-2.5 2.3",
    "prompt": "M1 1.8l1.8 1.6L1 5M3.6 5.6h3.2",
    "globe": "M4 0.8a3.2 3.2 0 1 0 0 6.4 3.2 3.2 0 0 0 0-6.4zM0.8 4h6.4M4 0.8c1.6 1.6 1.6 4.8 0 6.4M4 0.8C2.4 2.4 2.4 5.6 4 7.2",
    "grid": "M0.8 0.8h6.4v6.4H0.8zM0.8 3.2h6.4M0.8 4.8h6.4M3.2 0.8v6.4",
    "mtn": "M0.8 6.2l1.9-3 1.4 2.2 1-1.4 1.3 2.2zM0.8 0.8h6.4v5.4H0.8z",
    "box": "M1 2.2L4 0.8l3 1.4v2.9L4 6.6 1 5.1zM1 2.2L4 3.6l3-1.4M4 3.6v3",
    "dots": "M1.6 2.2a.7.7 0 1 0 1.4 0 .7.7 0 1 0-1.4 0zM1.6 4.4a.7.7 0 1 0 1.4 0 .7.7 0 1 0-1.4 0zM1.6 6.6a.7.7 0 1 0 1.4 0 .7.7 0 1 0-1.4 0zM4 2.2h3.2M4 4.4h3.2M4 6.6h3.2",
    "sum": "M1 1h6M1 1l3 2.6L1 6.4h6",
    "chain": "M2.6 2.4h3.2v3.2H2.6z",
    "property": "M1 4h4.6M5.6 2.5l1.6 1.5-1.6 1.5",
    "equals": "M1 2.4h6M1 4.8h6",
    "fish": "M1 3.4c1.6-2.4 5-2.4 6.2 0-1.2 2.4-4.6 2.4-6.2 0z",
    "star": "M4 1l.9 1.9 2 .3-1.5 1.4.4 2L4 5.7 2.2 6.6l.4-2L1.1 3.2l2-.3z",
    "lock": "M2.2 3.4V2.2a1.8 1.8 0 0 1 3.6 0v1.2M1.5 3.4h5v3.2h-5z",
    "git": "M3 1.4a1.3 1.3 0 1 0 0 2.6 1.3 1.3 0 0 0 0-2.6zM3 3.8v2.4a1.4 1.4 0 0 0 1.4 1.4h1.2"
           "M6 5.8a1.2 1.2 0 1 0 0 2.4 1.2 1.2 0 0 0 0-2.4zM1.6 1.6h4.2",
    "wrench": "M1.4 6.6l2.4-2.4M4.7 1a2 2 0 0 0 2.3 2.3L4.7 1zM5.4 2.6l1.8 1.8",
}
