"""Visual Studio 2026 editor (colour scheme) overrides.

Rider's bundled "Visual Studio Dark" scheme is a great base for the chrome, but
it still ships the *classic* Visual Studio 2022 editor palette: C# keywords are
blue ``#569CD6``, Razor directives are the only purple tokens, and HTML
attribute values are plain grey.

Visual Studio 2026 recolours the keyword family: control keywords (``if``,
``foreach``, ``public``, ``private``, ``var``, ``bool``, ...) are drawn in the
purple ``#D8A0DF`` of the 2026 theme, while Razor directives keep their own
``#A699E6`` and Razor components are teal like every other type.  The values
below were taken from Visual Studio 2026's own theme tokens (Roslyn
classification colours) and cross-checked against the user's screenshots, which
show exactly that purple keyword look inside ``@code`` blocks.

``install_rider.py`` applies these on top of the bundled scheme when it writes
the user's "Sharp Studio Dark" scheme, so the numbers below are the single
source of truth for the editor palette.

Two override forms exist:

* :data:`EDITOR_COLORS` -- simple ``<option name="X" value="..."/>`` entries
  inside the scheme's ``<colors>`` section (caret row, ...).
* :data:`EDITOR_OVERRIDES` -- token colours inside ``<attributes>``, each with
  a single ``FOREGROUND`` option.

``apply_overrides`` rewrites an existing entry in place or inserts a new one
before ``</attributes>``, so a token the bundled scheme does not list yet (for
example ``ReSharper.CSHARP_CONTROL_FLOW_KEYWORD``) is added cleanly.
"""

from __future__ import annotations

import re

#: VS 2026 sampled "current line highlight" (fixes the bundled scheme's
#: malformed ``CARET_ROW_COLOR`` value while it is at it).
EDITOR_COLORS: dict[str, str] = {
    "CARET_ROW_COLOR": "272727",
}

#: Token -> VS 2026 foreground.
EDITOR_OVERRIDES: dict[str, str] = {
    # --- C# keywords -----------------------------------------------------
    # Visual Studio 2026 draws the whole keyword family (control keywords and
    # modifiers alike) in the purple #D8A0DF; Rider keys the pieces
    # separately, so every keyword token gets the same value.
    "DEFAULT_KEYWORD": "D8A0DF",
    "ReSharper.CSHARP_KEYWORD": "D8A0DF",
    "ReSharper.CSHARP_CONTROL_FLOW_KEYWORD": "D8A0DF",
    "ReSharper.CSHARP_CONTROL_TRANSFER_KEYWORD": "D8A0DF",
    "ReSharper.CSHARP_BUILTIN_TYPE_KEYWORD": "D8A0DF",
    # C# attributes ([Parameter], [Inject], ...) read as the same purple in
    # the screenshots.
    "DEFAULT_ATTRIBUTE": "D8A0DF",

    # --- Razor ------------------------------------------------------------
    # Directives keep Visual Studio's own #A699E6, components (NativePager,
    # tag helpers) are teal like every other type.
    "ReSharper.ASP_NET_RAZOR_KEYWORD": "A699E6",
    "ReSharper.ASP_NET_BLOCK_TAG": "A699E6",
    "ReSharper.ASP_NET_RAZOR_TAG_HELPER_ELEMENT": "4EC9B0",
    "ReSharper.ASP_NET_RAZOR_TAG_HELPER_ATTRIBUTE": "4EC9B0",

    # --- HTML inside Razor -------------------------------------------------
    # Tags and delimiters grey, attribute names light blue, attribute values
    # string-orange -- all four sampled off the user's screenshots.
    "HTML_TAG": "808080",
    "HTML_TAG_NAME": "808080",
    "HTML_ATTRIBUTE_NAME": "9CDCFE",
    "HTML_ATTRIBUTE_VALUE": "D69D85",
}


def _color_option(name: str, value: str, nl: str) -> str:
    return f'<option name="{name}" value="{value}" />{nl}'


def _attribute_option(name: str, value: str, nl: str) -> str:
    return (
        f'    <option name="{name}">{nl}'
        f'      <value>{nl}'
        f'        <option name="FOREGROUND" value="{value}" />{nl}'
        f'      </value>{nl}'
        f'    </option>{nl}'
    )


def apply_overrides(scheme_xml: str) -> tuple[str, list[str]]:
    """Apply :data:`EDITOR_COLORS` and :data:`EDITOR_OVERRIDES` to a scheme XML.

    Returns ``(new_xml, inserted_names)`` where ``inserted_names`` lists the
    tokens that were not present and had to be added before ``</attributes>``.
    """
    nl = "\r\n" if "\r\n" in scheme_xml else "\n"
    inserted: list[str] = []

    for name, value in EDITOR_COLORS.items():
        pattern = re.compile(
            r'(<option name="' + re.escape(name) + r'")\s+value="[^"]*"(\s*/>)'
        )
        if pattern.search(scheme_xml):
            scheme_xml = pattern.sub(
                lambda m, v=value, n=nl: f'{m.group(1)} value="{v}" />{n}',
                scheme_xml, count=1,
            )
        else:
            inserted.append(name)

    for name, value in EDITOR_OVERRIDES.items():
        pattern = re.compile(
            r'[ \t]*<option name="' + re.escape(name) + r'"[^>]*?'
            r'(?:/>|>.*?</option>)[^\n]*\n',
            re.S,
        )
        replacement = _attribute_option(name, value, nl)
        if pattern.search(scheme_xml):
            scheme_xml = pattern.sub(lambda _m, r=replacement: r, scheme_xml, count=1)
        else:
            inserted.append(name)

    missing_colors = [n for n in inserted if n in EDITOR_COLORS]
    missing_attrs = [n for n in inserted if n in EDITOR_OVERRIDES]
    if missing_attrs:
        block = "".join(_attribute_option(n, EDITOR_OVERRIDES[n], nl) for n in missing_attrs)
        scheme_xml = scheme_xml.replace(
            f"  </attributes>{nl}", block + f"  </attributes>{nl}", 1
        )
    if missing_colors:
        block = "".join(_color_option(n, EDITOR_COLORS[n], nl) for n in missing_colors)
        scheme_xml = scheme_xml.replace(
            f"  </colors>{nl}", block + f"  </colors>{nl}", 1
        )
    return scheme_xml, inserted
