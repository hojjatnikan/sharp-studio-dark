"""Scan the locally installed Rider distribution for theme resources.

Reports (and optionally extracts):
  * bundled *.theme.json theme descriptors
  * bundled editor color schemes (colors/*.xml)
  * every icon path (expui/*.svg and legacy actions/*.svg) shipped by the platform
"""
from __future__ import annotations

import argparse
import json
import re
import zipfile
from collections import Counter
from pathlib import Path

RIDER = Path(r"D:\Program Files\JetBrains\Rider2026.1")

THEME_RE = re.compile(r".*\.theme\.json$")
SCHEME_RE = re.compile(r"^(colors|colorSchemes)/[^/]+\.(xml|icls)$")
SVG_RE = re.compile(r"\.svg$")


def scan(jars: list[Path]):
    themes, schemes, icons = [], [], []
    for jar in jars:
        try:
            with zipfile.ZipFile(jar) as zf:
                for name in zf.namelist():
                    if THEME_RE.search(name):
                        themes.append((jar, name))
                    elif SCHEME_RE.match(name):
                        schemes.append((jar, name))
                    elif SVG_RE.search(name):
                        icons.append((jar, name))
        except (zipfile.BadZipFile, OSError) as exc:  # pragma: no cover
            print(f"  !! skipped {jar.name}: {exc}")
    return themes, schemes, icons


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(RIDER))
    ap.add_argument("--extract-themes")
    ap.add_argument("--extract-schemes")
    ap.add_argument("--dump-icons")
    args = ap.parse_args()

    root = Path(args.root)
    jars = sorted(root.glob("lib/*.jar")) + sorted(root.glob("plugins/*/lib/*.jar"))
    print(f"scanning {len(jars)} jars under {root}")

    themes, schemes, icons = scan(jars)

    print(f"\n=== theme descriptors: {len(themes)} ===")
    for jar, name in themes:
        print(f"  {name:55s} <= {jar.name}")

    print(f"\n=== editor color schemes: {len(schemes)} ===")
    for jar, name in schemes[:40]:
        print(f"  {name:55s} <= {jar.name}")

    print(f"\n=== icons: {len(icons)} ===")
    buckets = Counter()
    for _jar, name in icons:
        parts = name.split("/")
        head = parts[0]
        if head == "expui":
            buckets["/".join(parts[:2])] += 1
        else:
            buckets[head] += 1
    for key, count in buckets.most_common(40):
        print(f"  {key:45s} {count}")

    if args.dump_icons:
        out = Path(args.dump_icons)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("\n".join(sorted(n for _j, n in icons)), encoding="utf-8")
        print(f"\nwrote {len(icons)} icon paths -> {out}")

    if args.extract_themes:
        out = Path(args.extract_themes)
        out.mkdir(parents=True, exist_ok=True)
        for jar, name in themes:
            with zipfile.ZipFile(jar) as zf:
                dest = out / Path(name).name
                dest.write_bytes(zf.read(name))
                print(f"extracted {dest}")

    if args.extract_schemes:
        out = Path(args.extract_schemes)
        out.mkdir(parents=True, exist_ok=True)
        for jar, name in schemes:
            with zipfile.ZipFile(jar) as zf:
                dest = out / Path(name).name
                if not dest.exists():
                    dest.write_bytes(zf.read(name))
                    print(f"extracted {dest}")


if __name__ == "__main__":
    main()
