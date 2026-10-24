"""Generate the Visual Studio style icon pack and its theme mappings.

Writes one SVG per icon into ``src/main/resources/icons/vs/`` and a mapping of
platform icon path -> plugin icon path into ``build/icon-map.json``, which
``tools/build_theme.py`` merges into the ``icons`` section of the theme.

Every platform path is validated against the icon inventory of the installed
Rider (``ref/icon-paths.txt``).  Paths that do not exist in this build are
skipped -- a theme may only patch icons that the IDE actually loads.
"""
from __future__ import annotations

import json
from pathlib import Path

import icons_files  # noqa: F401  (registers the node/file/type specs)
import icons_ui
from icons_ui import SPEC

ROOT = Path(__file__).resolve().parent.parent
ICON_DIR = ROOT / "src" / "main" / "resources" / "icons" / "vs"
INVENTORY = ROOT / "ref" / "icon-paths.txt"
OUT_MAP = ROOT / "build" / "icon-map.json"


def load_inventory() -> set[str]:
    if not INVENTORY.exists():
        raise SystemExit(
            f"{INVENTORY} is missing -- run tools/scan_platform.py --dump-icons ref/icon-paths.txt"
        )
    return {line.strip() for line in INVENTORY.read_text(encoding="utf-8").splitlines() if line.strip()}


def main() -> None:
    inventory = load_inventory()
    ICON_DIR.mkdir(parents=True, exist_ok=True)

    mappings: dict[str, str] = {}
    used: dict[str, int] = {}
    missing: dict[str, list[str]] = {}

    for name, (markup, targets) in sorted(SPEC.items()):
        resource = f"/icons/vs/{name}.svg"
        (ICON_DIR / f"{name}.svg").write_text(markup + "\n", encoding="utf-8")
        for target in targets:
            platform_path = target.lstrip("/")
            if platform_path in inventory:
                mappings[f"/{platform_path}"] = resource
                used[name] = used.get(name, 0) + 1
            else:
                missing.setdefault(name, []).append(target)

    OUT_MAP.parent.mkdir(parents=True, exist_ok=True)
    OUT_MAP.write_text(
        json.dumps({"paths": dict(sorted(mappings.items()))}, indent=2) + "\n",
        encoding="utf-8",
    )

    multi = [name for name, count in used.items() if count > 1]
    print(f"icons generated        : {len(SPEC)}")
    print(f"platform paths patched : {len(mappings)}")
    print(f"icons never patched    : {sorted(set(SPEC) - set(used))}")
    print(f"icons patching >1 path : {len(multi)}")
    if missing:
        print("\nskipped paths (not in this build):")
        for name, targets in sorted(missing.items()):
            print(f"  {name:16s} {', '.join(targets)}")
    print(f"\nwrote {ICON_DIR} and {OUT_MAP}")


if __name__ == "__main__":
    main()
