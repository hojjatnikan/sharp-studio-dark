"""Install the plugin into a local Rider installation and activate the theme.

* copies the plugin JAR into ``<config>/plugins/<name>/lib/``
* points ``options/laf.xml`` at the Visual Studio 2022 theme (keeping a backup,
  so the previous theme can be restored by copying the file back)
* refuses to rewrite ``laf.xml`` while Rider is running, because the IDE would
  overwrite it with its in-memory value on shutdown

Usage:
    python tools/install_rider.py --list
    python tools/install_rider.py                 # newest Rider config found
    python tools/install_rider.py --config "...\\JetBrains\\Rider2026.1" --restore
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "build" / "distributions"
NAME = "sharp-studio-dark"
THEME_ID = "hnikan-vs2022-dark-0f2c7ad4"
#: Name the user sees in "Settings | Editor | Color Scheme".  The theme itself
#: keeps referencing Rider's bundled "Visual Studio Dark" scheme (a third-party
#: plugin cannot register a bundled scheme -- the bundledColorScheme EP is
#: internal and makes Rider reject the descriptor), while this scheme is installed
#: as a *user* scheme with the same colours under our own name.
EDITOR_SCHEME = "Sharp Studio Dark"
BUNDLED_SCHEME = "Visual Studio Dark"
CONFIG_ROOT = Path.home() / "AppData" / "Roaming" / "JetBrains"
#: Where Rider is installed on this machine (only used as a fallback source for
#: the bundled colour scheme when ref/schemes is missing).
RIDER_INSTALL = Path(r"D:\Program Files\JetBrains\Rider2026.1")

#: Icon-pack plugins replace file/UI icons through their own IconPathPatcher and
#: take priority over theme icon mappings, which makes this theme's icon pack
#: invisible.  They are switched off (reversibly) so the Visual Studio icons win.
ICON_PACK_IDS = (
    "com.jtracker.vscodeicons",            # VSCode Icons
    "com.github.catppuccin.jetbrains_icons",  # Catppuccin Icons
)


def _backup(path: Path) -> Path:
    backup = path.with_name(path.name + ".bak")
    if path.exists() and not backup.exists():
        backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    return backup


def disable_icon_packs(config: Path) -> str:
    target = config / "disabled_plugins.txt"
    backup = _backup(target)
    lines = [line.strip() for line in target.read_text(encoding="utf-8").splitlines() if line.strip()] \
        if target.exists() else []
    added = [plugin_id for plugin_id in ICON_PACK_IDS if plugin_id not in lines]
    if not added:
        return "icon packs already disabled"
    target.write_text("\n".join(lines + added) + "\n", encoding="utf-8")
    return f"disabled icon packs: {', '.join(added)} (backup: {backup.name})"


def enable_main_toolbar(config: Path) -> str:
    """Visual Studio keeps its toolbar visible; Rider's New UI hides it by default."""
    target = config / "options" / "ui.lnf.xml"
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n<application>\n'
            '  <component name="UISettings">\n'
            '    <option name="SHOW_MAIN_TOOLBAR" value="true" />\n'
            '    <option name="SHOW_NEW_MAIN_TOOLBAR" value="true" />\n'
            '  </component>\n</application>\n',
            encoding="utf-8",
        )
        return "created options/ui.lnf.xml with the main toolbar enabled"

    backup = _backup(target)
    text = target.read_text(encoding="utf-8")
    options = (
        '    <option name="SHOW_MAIN_TOOLBAR" value="true" />\n'
        '    <option name="SHOW_NEW_MAIN_TOOLBAR" value="true" />\n'
    )
    if "SHOW_MAIN_TOOLBAR" in text:
        return "main toolbar option already present"
    if "</component>" in text:
        text = text.replace("</component>", options + "  </component>", 1)
    else:
        text = text.replace("</application>", '  <component name="UISettings">\n' + options + "  </component>\n</application>", 1)
    target.write_text(text, encoding="utf-8")
    return f"main toolbar enabled (backup: {backup.name})"


def config_dirs() -> list[Path]:
    if not CONFIG_ROOT.exists():
        return []
    return sorted(
        (p for p in CONFIG_ROOT.iterdir() if p.is_dir() and p.name.lower().startswith("rider")),
        reverse=True,
    )


def rider_running() -> bool:
    try:
        out = subprocess.run(
            ["powershell.exe", "-NoProfile", "-Command",
             "(Get-Process -Name rider64,rider -ErrorAction SilentlyContinue).Count"],
            capture_output=True, text=True, timeout=30,
        ).stdout.strip()
        return out not in ("", "0")
    except Exception:  # pragma: no cover - best effort only
        return False


def install_jar(config: Path) -> Path:
    target = config / "plugins" / NAME / "lib"
    target.mkdir(parents=True, exist_ok=True)
    jar = DIST / f"{NAME}.jar"
    if not jar.exists():
        raise SystemExit(f"{jar} not found -- run tools/build_plugin.py first")
    shutil.copy2(jar, target / jar.name)
    return target / jar.name


def bundled_visual_studio_scheme() -> str:
    """The XML of Rider's bundled "Visual Studio Dark" colour scheme.

    Prefers the copy extracted next to the tools (``ref/schemes``), otherwise
    reads it straight out of the theme pack in the IDE installation.
    """
    local = ROOT / "ref" / "schemes" / "VisualStudioDark.xml"
    if local.exists():
        return local.read_text(encoding="utf-8")
    for jar in RIDER_INSTALL.glob("plugins/*theme-pack*/lib/*.jar") or RIDER_INSTALL.glob("lib/*theme-pack*.jar"):
        with zipfile.ZipFile(jar) as archive:
            for name in archive.namelist():
                if name.endswith("colorSchemes/VisualStudioDark.xml"):
                    return archive.read(name).decode("utf-8")
    raise FileNotFoundError("bundled VisualStudioDark.xml not found")


def install_editor_scheme(config: Path) -> str:
    """Install "Sharp Studio Dark" as a user colour scheme.

    A third-party plugin cannot register a *bundled* colour scheme (the
    bundledColorScheme extension point is internal to JetBrains plugins -- using
    it makes Rider reject the whole descriptor), so the scheme is installed the
    way the IDE itself does it: a file in <config>/colorSchemes/<Name>.icls which
    then shows up by that name in the "Editor color scheme" dropdown.
    """
    try:
        source = bundled_visual_studio_scheme()
    except Exception as exc:  # noqa: BLE001
        return f"editor scheme left as-is ({exc})"

    # User schemes live in <config>/colors (bundled ones sit in colorSchemes/ inside
    # jars) -- that is the folder Rider scans for the "Editor color scheme" list.
    target_dir = config / "colors"
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{EDITOR_SCHEME}.icls"
    text = re.sub(r'(<scheme\s+name=")[^"]*(")', rf"\g<1>{EDITOR_SCHEME}\g<2>", source, count=1)
    target.write_text(text, encoding="utf-8")
    # clean up the copy that an earlier version of this installer wrote to the
    # wrong folder, so it cannot confuse the scheme list
    stale = config / "colorSchemes" / f"{EDITOR_SCHEME}.icls"
    if stale.exists():
        stale.unlink()
    return f"colors/{EDITOR_SCHEME}.icls"


def activate_theme(config: Path) -> str:
    """Point the IDE at the theme *and* at the Visual Studio editor scheme.

    A theme may declare an ``editorScheme``, but the globally selected scheme in
    ``options/colors.scheme.xml`` is restored on top of it at startup, so both
    files have to agree for the editor to really use the Visual Studio palette.
    """
    notes = []

    laf = config / "options" / "laf.xml"
    if not laf.exists():
        laf.parent.mkdir(parents=True, exist_ok=True)
        laf.write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n<application>\n'
            '  <component name="LafManager">\n'
            f'    <laf themeId="{THEME_ID}" />\n'
            '  </component>\n</application>\n',
            encoding="utf-8",
        )
        notes.append("created options/laf.xml")
    else:
        text = laf.read_text(encoding="utf-8")
        backup = laf.with_suffix(".xml.bak")
        if not backup.exists():
            backup.write_text(text, encoding="utf-8")
        # Rider drops the <laf themeId> element when a plugin is (re)installed and
        # the theme it pointed at disappears, so it has to be *inserted* again --
        # replacing only works when the element is still there.
        if re.search(r'<laf themeId="[^"]*"', text):
            updated = re.sub(r'(<laf themeId=")[^"]*(")', rf"\g<1>{THEME_ID}\g<2>", text, count=1)
        elif "</component>" in text:
            updated = text.replace(
                "</component>", f'    <laf themeId="{THEME_ID}" />\n  </component>', 1)
        else:
            updated = text.replace(
                "</application>",
                '  <component name="LafManager">\n'
                f'    <laf themeId="{THEME_ID}" />\n'
                "  </component>\n</application>",
                1,
            )
        laf.write_text(updated, encoding="utf-8")
        notes.append(f"laf.xml -> {THEME_ID} (backup: {backup.name})")

    scheme = config / "options" / "colors.scheme.xml"
    scheme.parent.mkdir(parents=True, exist_ok=True)
    backup = scheme.with_suffix(".xml.bak")
    if scheme.exists() and not backup.exists():
        backup.write_text(scheme.read_text(encoding="utf-8"), encoding="utf-8")

    # Install "Sharp Studio Dark" as a user scheme (same colours as the bundled
    # Visual Studio Dark scheme, but under our own name in the dropdown).
    notes.append(f"scheme: {install_editor_scheme(config)}")

    scheme.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<application>\n'
        '  <component name="EditorColorsManagerImpl">\n'
        f'    <global_color_scheme name="{EDITOR_SCHEME}" />\n'
        '  </component>\n</application>\n',
        encoding="utf-8",
    )
    notes.append(f"editor scheme -> {EDITOR_SCHEME} (backup: {backup.name})")
    return "; ".join(notes)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", help="Rider config directory (defaults to the newest)")
    ap.add_argument("--list", action="store_true", help="only list config directories")
    ap.add_argument("--restore", action="store_true", help="restore laf.xml / colors.scheme.xml / settings from the backups")
    ap.add_argument("--keep-icon-packs", action="store_true",
                    help="do not disable third-party icon packs (they hide this theme's icons)")
    ap.add_argument("--keep-toolbar-hidden", action="store_true",
                    help="do not enable the main toolbar (Visual Studio shows one)")
    args = ap.parse_args()

    dirs = config_dirs()
    if args.list:
        for path in dirs:
            print(path)
        return
    if not dirs:
        raise SystemExit(f"no Rider configuration found under {CONFIG_ROOT}")

    config = Path(args.config) if args.config else dirs[0]
    print(f"config: {config}")

    if args.restore:
        if rider_running():
            raise SystemExit("Rider is running -- close it before restoring settings")
        restored = []
        for rel in ("options/laf.xml", "options/colors.scheme.xml", "options/ui.lnf.xml", "disabled_plugins.txt"):
            backup = config / (rel + ".bak")
            if backup.exists():
                shutil.copy2(backup, config / rel)
                restored.append(rel)
        print("restored: " + (", ".join(restored) if restored else "nothing (no backups found)"))
        return

    jar = install_jar(config)
    print(f"plugin : {jar}")

    if rider_running():
        print("theme  : Rider is running, so options/laf.xml was left untouched.")
        print("         Restart Rider and pick 'Visual Studio 2022 Dark' in")
        print("         Settings | Appearance & Behavior | Appearance | Theme.")
        return

    print(f"theme  : {activate_theme(config)}")
    if not args.keep_icon_packs:
        print(f"icons  : {disable_icon_packs(config)}")
    if not args.keep_toolbar_hidden:
        print(f"layout : {enable_main_toolbar(config)}")
    print("\nRestart Rider for the changes to take effect.")


if __name__ == "__main__":
    sys.exit(main())
