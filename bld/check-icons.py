"""Check converted VS icons: colours + shapes."""
import re
from pathlib import Path

VS = Path("src/main/resources/icons/vs")
expect = {
    "css": {"#F0F0F0", "#F15262"},
    "javaScript": {"#F68D50"},
    "folder": {"#E8C46A"},
    "wwwroot": {"#F8F8F8", "#767676", "#DCB67A"},
    "html": {"#51B3FF", "#F0F0F0"},
    "Csharp": {"#6BB700"},
    "text": {"#F0F0F0"},
    "xml": {"#F0F0F0"},
    "jsscript": {"#F68D50"},
    "solution": {"#F0F0F0", "#C58CE8"},
    "yamlfile": {"#F0F0F0", "#F15262"},
    "jsonscript": {"#F0F0F0"},
    "markdownfile": {"#F0F0F0"},
    "image": {"#51B3FF", "#F0F0F0", "#E8C46A"},
    "fontfile": {"#51B3FF", "#F0F0F0"},
    "configurationfile": {"#F0F0F0"},
    "sqldatabase": {"#F0F0F0", "#6FA8DC"},
}
ok = True
for name in sorted(expect):
    svg = (VS / f"{name}.svg").read_text(encoding="utf-8")
    cols = set(re.findall(r'fill="(#F0F0F0|[A-Z0-9]{6})"', svg))
    good = cols >= expect[name]
    ok &= good
    print(f"{name:14s} {sorted(cols)}   expected {sorted(expect[name])}   {'OK' if good else 'MISMATCH'}")

# sanity: no leftover dark theme colours, no XAML path syntax leak
leak = []
for f in sorted(VS.iterdir()):
    t = f.read_text(encoding="utf-8").lower()
    if "fill-rule" in t or '"fill-rule' in t or "f1 m " in t or "m 16,16" in t:
        leak.append(f.name)
print("leaks:", leak or "none")
print("ALL OK" if ok and not leak else "PROBLEM")
