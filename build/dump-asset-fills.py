"""Dump every fill colour of the VS assets we plan to reuse (light->dark mapping)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # rider-vs-theme/
FILL = re.compile(r'Fill="#([0-9A-Fa-f]{6,8})"')

ASSETS = [
    "stylesheet", "jsscript", "csfile", "htmlfile", "folderclosed", "folderopened",
    "webfolderclosed", "webfolderopened", "xmlfile", "textfile", "markdownfile",
    "jsonscript", "image", "fontfile", "solution", "csprojectnode", "yamlfile",
    "asprazorfile", "csrazorfile", "connectedservices", "configurationfile",
    "sqldatabase", "propertiesfolderclosed", "lessstylesheet", "sassstylesheet",
]

for name in ASSETS:
    xaml = ROOT / "xaml" / f"{name}.xaml"
    if not xaml.exists():
        print(f"{name:22s} MISSING")
        continue
    fills = sorted({m.group(1).upper() for m in FILL.finditer(xaml.read_text(encoding='utf-8', errors='ignore'))})
    shapes = xaml.read_text(encoding='utf-8', errors='ignore').count("<Path")
    print(f"{name:22s} paths={shapes:<2d} fills: {' '.join('#' + f for f in fills)}")
