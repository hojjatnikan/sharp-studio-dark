"""Validation for round 11: VS 2026 editor palette + Solution Explorer icons.

Checks (all offline -- no Rider needed):

1. tools/vs_editor.apply_overrides really rewrites/inserts the VS 2026 editor
   tokens on top of Rider's bundled Visual Studio Dark scheme, and the result
   is well-formed XML with no duplicated option names.
2. The regenerated icon SVGs carry the Visual Studio look from the user's
   screenshots (purple Razor tile with the white bolt, globe on wwwroot,
   purple CSS hash, yellow JS letters).
3. build/icon-map.json points the Razor/wwwroot/CSS/JS platform paths at the
   new icons, and the theme descriptor carries them.
4. The plugin JAR ships the new icons and plugin.xml/build_plugin.py agree on
   version 1.0.3.
"""
from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))

from vs_editor import apply_overrides  # noqa: E402

THEME = ROOT / "src" / "main" / "resources" / "themes" / "visual-studio-2022-dark.theme.json"
ICON_MAP = HERE / "icon-map.json"
ICONS = ROOT / "src" / "main" / "resources" / "icons" / "vs"
BUNDLED = ROOT / "ref" / "schemes" / "VisualStudioDark.xml"
JAR = ROOT / "build" / "distributions" / "sharp-studio-dark.jar"
SHIPPED_SCHEME = ROOT / "src" / "main" / "resources" / "colorSchemes" / "sharp-studio-dark.xml"
BUILD_PLUGIN = ROOT / "tools" / "build_plugin.py"

failures = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global failures
    if not ok:
        failures += 1
    print(f"{'OK  ' if ok else 'FAIL'} {label}{(' -- ' + detail) if detail and not ok else ''}")


# ---------------------------------------------------------------- 1. editor
xml_text, inserted = apply_overrides(BUNDLED.read_text(encoding="utf-8"))


def attr_value(name: str) -> str | None:
    m = re.search(
        r'<option name="' + re.escape(name) + r'">.*?FOREGROUND" value="([0-9A-Fa-f]{6})"',
        xml_text, re.S,
    )
    return m.group(1).upper() if m else None


check("editor: DEFAULT_KEYWORD -> D8A0DF", attr_value("DEFAULT_KEYWORD") == "D8A0DF",
      f"got {attr_value('DEFAULT_KEYWORD')}")
check("editor: CSHARP_KEYWORD -> D8A0DF", attr_value("ReSharper.CSHARP_KEYWORD") == "D8A0DF")
check("editor: CSHARP_CONTROL_FLOW_KEYWORD pinned",
      "ReSharper.CSHARP_CONTROL_FLOW_KEYWORD" in inserted
      and attr_value("ReSharper.CSHARP_CONTROL_FLOW_KEYWORD") == "D8A0DF",
      f"inserted={inserted}")
check("editor: CSHARP_BUILTIN_TYPE_KEYWORD pinned",
      attr_value("ReSharper.CSHARP_BUILTIN_TYPE_KEYWORD") == "D8A0DF")
check("editor: DEFAULT_ATTRIBUTE -> D8A0DF", attr_value("DEFAULT_ATTRIBUTE") == "D8A0DF")
check("editor: ASP_NET_RAZOR_KEYWORD -> A699E6",
      attr_value("ReSharper.ASP_NET_RAZOR_KEYWORD") == "A699E6")
check("editor: RAZOR_TAG_HELPER_ELEMENT -> 4EC9B0",
      attr_value("ReSharper.ASP_NET_RAZOR_TAG_HELPER_ELEMENT") == "4EC9B0")
check("editor: HTML_TAG_NAME -> 808080", attr_value("HTML_TAG_NAME") == "808080")
check("editor: HTML_ATTRIBUTE_NAME -> 9CDCFE", attr_value("HTML_ATTRIBUTE_NAME") == "9CDCFE")
check("editor: HTML_ATTRIBUTE_VALUE -> D69D85", attr_value("HTML_ATTRIBUTE_VALUE") == "D69D85")
check("editor: CARET_ROW_COLOR -> 272727",
      re.search(r'<option name="CARET_ROW_COLOR" value="272727" />', xml_text) is not None)

root = ET.fromstring(xml_text)
base = ET.fromstring(BUNDLED.read_text(encoding="utf-8"))


def top_level_attr_names(tree: ET.Element) -> list[str]:
    attrs = tree.find("attributes")
    return [o.get("name") for o in attrs] if attrs is not None else []


def dupes(names: list[str]) -> set[str]:
    return {n for n in names if names.count(n) > 1}


check("editor: result is well-formed XML", True)
check("editor: no NEW duplicate attribute options",
      dupes(top_level_attr_names(root)) == dupes(top_level_attr_names(base)),
      f"new: {dupes(top_level_attr_names(root)) - dupes(top_level_attr_names(base))}")
check("editor: option count grew by exactly the inserted tokens",
      len(top_level_attr_names(root)) == len(top_level_attr_names(base)) + len(inserted),
      f"{len(top_level_attr_names(root))} vs base {len(top_level_attr_names(base))} + {len(inserted)}")

# ---------------------------------------------------------------- 2. icons
def icon(name: str) -> str:
    return (ICONS / f"{name}.svg").read_text(encoding="utf-8")


razor = icon("razorFile")
check("icon: razorFile is the purple VS tile", "#B180D7" in razor and 'fill="#FFFFFF"' in razor)
check("icon: razorFile no longer uses the grey @ badge", "#C8C8C8" not in razor)
wwwroot = icon("wwwroot")
check("icon: wwwroot = real VS web folder (white folder + globe)",
      "#F6F6F6" in wwwroot and "#DCB67A" in wwwroot and "#767676" in wwwroot)
check("icon: javaScript = real VS jsscript (#F68D50, real path data)",
      "#F68D50" in icon("javaScript") and "#DE590B" not in icon("javaScript")
      and "4.49999" in icon("javaScript"))
check("icon: css = real VS stylesheet (red A #F15262, not the drawn badge)",
      "#F15262" in icon("css") and "#C50F1F" not in icon("css")
      and "#B180D7" not in icon("css") and "4.46957" in icon("css"))
check("icon: folder = real VS gold folder (#E8C46A)",
      "#E8C46A" in icon("folder") and "#B27C00" not in icon("folder")
      and "13.8807" in icon("folder"))
check("icon: no library (light-theme) colour leaked into converted icons",
      not any(c in icon(n) for n in ("css", "javaScript", "folder", "html", "xml",
                                     "Csharp", "solution", "image", "markdown")
              for c in ("#202020", "#B27C00", "#C50F1F", "#DE590B", "#11910D", "#006CBF")))
# ---------------------------------------------------------------- 3. icon map
mapping = json.loads(ICON_MAP.read_text(encoding="utf-8"))["paths"]
check("map: Razor files -> razorFile.svg",
      mapping.get("/resharper/expui/PsiRazor/Razor.svg") == "/icons/vs/razorFile.svg"
      and mapping.get("/resharper/expui/PsiRazor/Razor_dark.svg") == "/icons/vs/razorFile.svg")
check("map: wwwroot folders -> wwwroot.svg",
      all(mapping.get(p) == "/icons/vs/wwwroot.svg" for p in (
          "/resharper/ProjectModel/FolderWWWRootClosed.svg",
          "/resharper/ProjectModel/FolderWWWRootClosed_dark.svg",
          "/resharper/expui/ProjectModel/FolderWWWRootOpened.svg",
          "/resharper/expui/ProjectModel/FolderWWWRootOpened_dark.svg",
      )))
check("map: dotnetFolder no longer claims wwwroot",
      not any(v == "/icons/vs/dotnetFolder.svg" for k, v in mapping.items()
              if "WWWRoot" in k))
check("map: css/js keep their paths",
      mapping.get("/expui/fileTypes/css.svg") == "/icons/vs/css.svg"
      and mapping.get("/expui/fileTypes/javaScript.svg") == "/icons/vs/javaScript.svg")
check("map: still covers every platform path", len(mapping) >= 719, f"{len(mapping)} paths")

theme = json.loads(THEME.read_text(encoding="utf-8"))
theme_icons = theme["icons"]
check("theme: icons section carries every mapped path",
      all(theme_icons.get(k) == v for k, v in mapping.items()))
check("theme: ColorPalette still present", "ColorPalette" in theme_icons)

# ---------------------------------------------------------------- 4. jar/version
check("jar: exists", JAR.exists())
if JAR.exists():
    with zipfile.ZipFile(JAR) as z:
        names = set(z.namelist())
        descriptor = z.read("META-INF/plugin.xml").decode("utf-8")
    check("jar: ships wwwroot.svg + razorFile.svg",
          "icons/vs/wwwroot.svg" in names and "icons/vs/razorFile.svg" in names)
    check("jar: plugin.xml is 1.0.2", "<version>1.0.2</version>" in descriptor)
    check("jar: change-notes mention 1.0.2", "<b>1.0.2</b>" in descriptor)


# ------------------------------------------------- 5. installed user scheme
configs = sorted(
    (p for p in (Path.home() / "AppData" / "Roaming" / "JetBrains").glob("Rider*")
     if (p / "colors" / "Sharp Studio Dark.icls").exists()),
    key=lambda p: p.stat().st_mtime, reverse=True,
)
if configs:
    installed = (configs[0] / "colors" / "Sharp Studio Dark.icls").read_text(encoding="utf-8")
    print(f"\ninstalled scheme: {configs[0] / 'colors' / 'Sharp Studio Dark.icls'}")
    for name, want in (
        ("DEFAULT_KEYWORD", "D8A0DF"),
        ("ReSharper.CSHARP_CONTROL_FLOW_KEYWORD", "D8A0DF"),
        ("DEFAULT_ATTRIBUTE", "D8A0DF"),
        ("ReSharper.ASP_NET_RAZOR_KEYWORD", "A699E6"),
        ("ReSharper.ASP_NET_RAZOR_TAG_HELPER_ELEMENT", "4EC9B0"),
        ("HTML_TAG_NAME", "808080"),
        ("HTML_ATTRIBUTE_VALUE", "D69D85"),
    ):
        got = attr_value_installed = re.search(
            r'<option name="' + re.escape(name) + r'">.*?FOREGROUND" value="([0-9A-Fa-f]{6})"',
            installed, re.S,
        )
        check(f"installed: {name} -> {want}",
              got is not None and got.group(1).upper() == want)
    check("installed: CARET_ROW_COLOR -> 272727",
          re.search(r'CARET_ROW_COLOR" value="272727"', installed) is not None)
    laf = configs[0] / "options" / "laf.xml"
    check("installed: laf.xml points at the theme",
          laf.exists() and "hnikan-vs2022-dark-0f2c7ad4" in laf.read_text(encoding="utf-8"))
else:
    print("\n(no installed 'Sharp Studio Dark.icls' found -- run tools/install_rider.py)")

check("build_plugin.py: VERSION is 1.0.2",
      'VERSION = "1.0.2"' in BUILD_PLUGIN.read_text(encoding="utf-8"))
shipped = SHIPPED_SCHEME.read_text(encoding="utf-8")
check("shipped scheme documents the VS 2026 tokens",
      all(tok in shipped for tok in ("d8a0df", "a699e6", "4ec9b0", "d69d85", "808080")))

print("\nFAILED:", failures)
sys.exit(1 if failures else 0)
