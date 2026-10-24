"""Replace matching Rider icon specs with authentic Visual Studio XAML art.

Run after ``tools/gen_icons.py`` and before ``tools/build_theme.py``.  Explicit
aliases cover the file/tree assets whose Visual Studio names differ; the
remaining specs are matched by their own name or a platform icon filename.
"""
from __future__ import annotations

import re
from pathlib import Path

import icons_files  # noqa: F401  (registers the node/file/type specs)
import vs_xaml
from icons_ui import SPEC

ROOT = Path(__file__).resolve().parent.parent
XAML_DIR = ROOT.parent / "xaml"
OUT_DIR = ROOT / "src" / "main" / "resources" / "icons" / "vs"

# Explicit aliases for plugin names that do not match the Visual Studio
# library's XAML stems.
ALIASES: dict[str, str] = {
    "addFile": "addtextfile",
    "breakpoint": "breakpointenabled",
    "breakpointConditional": "breakpointdependent",
    "breakpointException": "breakpointerror",
    "Csharp": "csfilenode",
    "classAbstract": "abstractclass",
    "config": "configurationfile",
    "css": "stylesheet",
    "csLibraryProject": "cslibrary",
    "csProject": "csfilenode",
    "csharpFile": "csfilenode",
    "debug": "debugselection",
    "depFrameworks": "framework",
    "depSourceGenerators": "generatefile",
    "dotnetFolder": "folderclosed",
    "editorConfig": "editorconfigfile",
    "enum": "enumeration",
    "errorIntroduction": "messageerror",
    "excludeRoot": "excludepath",
    "exceptionNode": "exceptioninternal",
    "fold": "collapse",
    "folder": "folderclosed",
    "font": "fontfile",
    "ft_cpp": "cppfile",
    "ft_java": "javasource",
    "function": "userfunction",
    "generatedFolder": "generatefile",
    "gitignore": "git",
    "greenCheckmark": "checkmark",
    "help": "f1help",
    "html": "htmlfile",
    "javaScript": "jsscript",
    "json": "jsonscript",
    "manifest": "manifestfile",
    "markdown": "markdownfile",
    "muteBreakpoints": "disableallbreakpoints",
    "projectStructure": "structure",
    "resourcesRoot": "localresources",
    "regexp": "regularexpression",
    "runError": "ruleerror",
    "runFailed": "runfailedtest",
    "runToCursor": "cursor",
    "sourceRoot": "sourcecontrol",
    "sql": "sqldatabase",
    "testRoot": "testgroup",
    "text": "textfile",
    "twBookmarks": "bookmark",
    "twBuild": "builderrorlist",
    "twCoverage": "codecoverage",
    "twDebug": "debugselection",
    "twDependencies": "dependencymatrix",
    "twDocumentation": "helpapplication",
    "twLearn": "helpapplication",
    "twMessages": "message",
    "twNotifications": "notificationhub",
    "twProblems": "builderrorlist",
    "twProject": "solutionexplorerviews",
    "twRepositories": "gitrepository",
    "twTerminal": "terminalreadwrite",
    "twTodo": "tasklist",
    "twVcs": "gittoolwindow",
    "unfold": "expand",
    "unknown": "unknownmember",
    "variable": "localvariable",
    "vbProject": "vbprojectnode",
    "wwwroot": "webfolderclosed",
    "xml": "xmlfile",
    "razorFile": "csrazorfile",
    "binaryData": "binary",
    "yaml": "yamlfile",
}


def _normalise(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def source_map() -> dict[str, str]:
    """Resolve specs to explicit or name-matched Visual Studio XAML sources."""
    assets = vs_xaml.available_assets(XAML_DIR)
    by_name = {_normalise(asset): asset for asset in assets}
    resolved = dict(ALIASES)

    for name, (_markup, targets) in sorted(SPEC.items()):
        if name in resolved:
            continue
        candidates = [name]
        candidates.extend(
            Path(target).stem.removesuffix("_dark")
            for target in targets
        )
        for candidate in candidates:
            asset = by_name.get(_normalise(candidate))
            if asset is not None:
                resolved[name] = asset
                break
    return resolved


def convert(xaml: str) -> str:
    """Convert Visual Studio XAML using the shared, WPF-aware converter."""
    return vs_xaml.convert(xaml, recolor=True)


def main() -> None:
    if not XAML_DIR.is_dir():
        raise SystemExit(f"{XAML_DIR} not found -- the VS icon library is missing")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    mappings = source_map()
    written, missing, failed = 0, [], []
    for name, asset in sorted(mappings.items()):
        xaml = XAML_DIR / f"{asset}.xaml"
        if not xaml.exists():
            missing.append((name, asset))
            continue
        try:
            svg = vs_xaml.convert_file(xaml, recolor=True)
        except vs_xaml.ConversionError as exc:
            failed.append((name, asset, str(exc)))
            continue
        (OUT_DIR / f"{name}.svg").write_text(svg + "\n", encoding="utf-8")
        written += 1

    print(f"VS icons written   : {written} (of {len(mappings)} mapped)")
    print(f"VS-backed specs    : {len(set(mappings) & set(SPEC))} (of {len(SPEC)})")
    if missing:
        print("missing assets     :")
        for name, asset in missing:
            print(f"  {name:20s} <- {asset}.xaml")
    if failed:
        print("unconvertible      :")
        for name, asset, why in failed:
            print(f"  {name:20s} <- {asset}.xaml ({why})")
    print(f"wrote {OUT_DIR}")


if __name__ == "__main__":
    main()
