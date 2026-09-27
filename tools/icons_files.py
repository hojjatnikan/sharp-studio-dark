"""Icon specs: tree nodes, member symbols, file types and .NET specifics.

Visual Studio vocabulary used here:

* **folders** are golden outlines;
* **files** are grey document sheets carrying a small coloured badge;
* **members** (class / method / property / ...) are letter tiles coloured like
  the Visual Studio editor (types teal, methods yellow, constants light blue);
* **C# projects** are the blue ``C#`` tile seen in the Solution Explorer.
"""
from __future__ import annotations

from icons_common import (
    ACCENT, BLUE, DARK, GOLD, GRAY, GRAY_DIM, GREEN, LIGHTBLUE, ORANGE, PURPLE,
    RED, TEAL, WHITE, YELLOW, GLYPHS, LETTERS, badge_filled, badge_outline,
    letter_centered, path, sheet, svg, symbol_tile,
)
from icons_ui import FOLDER_PATH, add

# ==========================================================================
# folders and roots
# ==========================================================================
add("folder", path(FOLDER_PATH, GOLD),
    "/expui/nodes/folder.svg", "/nodes/folder.svg", "/icons/nodes/folder.svg")

add("folderSolution", path(FOLDER_PATH, GOLD),
    "/rider/expui/nodes/FolderSolution.svg")

add("sourceRoot",
    path(FOLDER_PATH, GOLD) + f'<circle cx="11.4" cy="10.6" r="1.3" fill="{ACCENT}"/>',
    "/expui/nodes/sourceRoot.svg", "/expui/nodes/sourceRootFileLayer.svg",
    "/nodes/sourceRoot.svg")

add("testRoot",
    path(FOLDER_PATH, GOLD) + f'<circle cx="11.4" cy="10.6" r="1.3" fill="{GREEN}"/>',
    "/expui/nodes/testRoot.svg", "/expui/nodes/testSourceFolder.svg",
    "/expui/nodes/testResourcesRoot.svg")

add("resourcesRoot",
    path(FOLDER_PATH, GOLD) + f'<circle cx="11.4" cy="10.6" r="1.3" fill="{ORANGE}"/>',
    "/expui/nodes/resourcesRoot.svg")

add("excludeRoot",
    path(FOLDER_PATH, GRAY_DIM) + path("M8.6 10.6l5.6 0", RED, 1.4),
    "/expui/nodes/excludeRoot.svg", "/expui/nodes/excludedGenerated.svg")

add("generatedFolder",
    path(FOLDER_PATH, GOLD)
    + letter_centered("G", GRAY, 11.4, 10.6, 4.4, 0.85),
    "/expui/nodes/annotationFolder.svg", "/actions/generatedFolder.svg")

# ==========================================================================
# member / type symbols (letter tiles in Visual Studio editor colours)
# ==========================================================================
SYMBOL_SPECS = [
    ("class", "C", TEAL, ["/expui/nodes/class.svg", "/nodes/class.svg"]),
    ("classAbstract", "C", TEAL, ["/expui/nodes/classAbstract.svg"]),
    ("interface", "I", TEAL, ["/expui/nodes/interface.svg", "/nodes/interface.svg"]),
    ("enum", "E", TEAL, ["/expui/nodes/enum.svg", "/nodes/enum.svg"]),
    ("record", "R", TEAL, ["/expui/nodes/record.svg"]),
    ("type", "T", TEAL, ["/expui/nodes/type.svg"]),
    ("method", "M", YELLOW, ["/expui/nodes/method.svg", "/nodes/method.svg"]),
    ("methodAbstract", "M", YELLOW, ["/expui/nodes/methodAbstract.svg"]),
    ("function", "F", YELLOW, ["/expui/nodes/function.svg"]),
    ("lambda", "L", YELLOW, ["/expui/nodes/lambda.svg"]),
    ("constructor", "C", TEAL, ["/expui/nodes/constructor.svg"]),
    ("property", "P", GRAY, ["/expui/nodes/property.svg", "/nodes/property.svg"]),
    ("field", "F", GRAY, ["/expui/nodes/field.svg", "/nodes/field.svg"]),
    ("constant", "K", LIGHTBLUE, ["/expui/nodes/constant.svg"]),
    ("parameter", "P", LIGHTBLUE, ["/expui/nodes/parameter.svg"]),
    ("variable", "V", LIGHTBLUE, ["/expui/nodes/variable.svg", "/expui/nodes/gvariable.svg"]),
    ("package", "P", GRAY_DIM, ["/expui/nodes/package.svg"]),
    ("module", "M", ACCENT, ["/expui/nodes/module.svg", "/nodes/module.svg"]),
    ("artifact", "A", ACCENT, ["/expui/nodes/artifact.svg"]),
    ("alias", "A", GRAY_DIM, ["/expui/nodes/alias.svg"]),
    ("attribute", "A", GRAY, ["/expui/nodes/attribute.svg"]),
    ("annotation", "A", GRAY, ["/expui/nodes/annotation.svg"]),
    ("word", "W", GRAY_DIM, ["/expui/nodes/word.svg"]),
    ("unknown", "?", GRAY_DIM, ["/expui/nodes/unknown.svg"]),
]

for _name, _letter, _colour, _targets in SYMBOL_SPECS:
    add(_name, symbol_tile(_letter, _colour), *_targets)

add("library",
    path("M3 4.4h3.2v8H3zM7 4.4h3.2v8H7z", BLUE)
    + path("M11 5.2l1.8 7.2", BLUE, 1.1),
    "/expui/nodes/library.svg", "/nodes/library.svg")

add("moduleGroup",
    path("M3.4 4.6h9.2v7.2H3.4z", ACCENT)
    + path("M5.4 3.2h5.2v1.4H5.4z", ACCENT, 1.1),
    "/expui/nodes/moduleGroup.svg", "/expui/nodes/module8x8.svg")

add("testNode",
    f'<circle cx="8" cy="8" r="5.6" stroke="{GREEN}" stroke-width="1.3"/>'
    + path("M5.4 8.2l2 2 3.4-4.4", GREEN, 1.5),
    "/expui/nodes/test.svg", "/nodes/test.svg")

add("rerunNode",
    f'<circle cx="8" cy="8" r="5.6" stroke="{GRAY}" stroke-width="1.2"/>'
    + path("M8 5.2v5.6M5.4 8.2L8 10.8l2.6-2.6", GRAY, 1.3),
    "/expui/nodes/testIgnored.svg", "/expui/nodes/testGroup.svg")

add("exceptionNode",
    f'<circle cx="8" cy="8" r="5.6" stroke="{ORANGE}" stroke-width="1.3"/>'
    + path("M8 5v3.6", ORANGE, 1.3) + f'<circle cx="8" cy="10.8" r=".75" fill="{ORANGE}"/>',
    "/expui/nodes/exception.svg", "/expui/nodes/abstractException.svg")

add("errorIntroduction",
    f'<circle cx="8" cy="8" r="5" stroke="{RED}" stroke-width="1.2"/>'
    + path("M6.2 6.2l3.6 3.6M9.8 6.2l-3.6 3.6", RED, 1.2),
    "/expui/nodes/errorIntroduction.svg")

add("warningIntroduction",
    path("M8 3.4l5.4 9.2H2.6z", YELLOW)
    + path("M8 6.6v2.8", GRAY, 1.0) + f'<circle cx="8" cy="11" r=".65" fill="{GRAY}"/>',
    "/expui/nodes/warningIntroduction.svg")

add("staticMark", letter_centered("S", GRAY_DIM, 8, 8, 11, 1.6),
    "/expui/nodes/static.svg", "/expui/nodes/staticMark.svg")

add("finalMark", letter_centered("F", GRAY_DIM, 8, 8, 11, 1.6),
    "/expui/nodes/finalMark.svg")

add("sharedMark", letter_centered("H", ACCENT, 8, 8, 11, 1.4),
    "/expui/nodes/shared.svg")

add("lockedMark",
    path("M5.6 7.2V5.6a2.4 2.4 0 0 1 4.8 0v1.6", GRAY_DIM, 1.1)
    + path("M4.6 7.2h6.8v4.4H4.6z", GRAY_DIM, 1.1),
    "/expui/nodes/locked.svg", "/expui/general/locked.svg")

add("resourceBundle",
    path("M3.2 3.2h6.4l3.2 3.2v3.4H3.2z", ACCENT)
    + path("M3.2 9.8h9.6", ACCENT, 1.0),
    "/expui/nodes/resourceBundle.svg", "/expui/nodes/services.svg")

# ==========================================================================
# file types -- grey page with the language glyph drawn *inside* it
# (this is Visual Studio's file-icon language: no corner badge, the coloured
#  glyph sits in the page body, e.g. a green "C#" for a .cs file)
# ==========================================================================
CSHARP_GREEN = "#67B466"     # colour Visual Studio uses for C# in file icons
VS_WINDOW = "#B9BEC6"        # the light grey "application window" tile of VS project icons
VS_PHOTO = "#9AA7B0"
VS_GLOBE = "#2B7FD4"


def cs_glyph(colour: str = CSHARP_GREEN) -> str:
    """The green "C#" of a .cs file in Visual Studio -- C and # kept apart."""
    return letter_centered("C", colour, 4.2, 8.2, 9.6, 1.75) + letter_centered("#", colour, 11.7, 8.2, 9.0, 1.6)


def vs_window(overlay: str = "") -> str:
    """Visual Studio project/solution tile: light grey window with a title bar."""
    return (f'<rect x="4.1" y="2.3" width="9.8" height="11.4" rx="1.7" fill="none" '
            f'stroke="{VS_WINDOW}" stroke-width="1.2"/>'
            + path("M4.1 5.6h9.8", VS_WINDOW, 1.2) + overlay)


def globe_overlay() -> str:
    """The chunky blue globe that Visual Studio overlays on web projects."""
    blue, dark, light = "#4FA8E0", "#2C6E9E", "#BBDDF6"
    return (
        f'<circle cx="4.1" cy="10.4" r="3.5" fill="{blue}"/>'
        + path("M4.1 6.9v7M1.0 9.1c1.9 1 4.3 1 6.2 0M1.0 11.7c1.9-1 4.3-1 6.2 0", dark, 0.9)
        + path("M1.0 10.4h6.2", light, 0.9)
    )


def csharp_overlay() -> str:
    """The purple C# mark Visual Studio overlays on solution / library nodes."""
    purple, dark = "#B47AD8", "#3D2A5A"
    return (
        f'<circle cx="3.1" cy="10.5" r="2.1" fill="{purple}"/>'
        f'<circle cx="5.7" cy="10.5" r="2.1" fill="{purple}"/>'
        f'<circle cx="3.1" cy="10.5" r="0.75" fill="{dark}"/>'
        f'<circle cx="5.7" cy="10.5" r="0.75" fill="{dark}"/>'
    )


def photo_icon() -> str:
    """Visual Studio's image icon: a framed picture with a hill and a sun."""
    return (
        badge_outline(VS_PHOTO, 2.5, 2.9, 11, 2.0)
        + path("M4.3 11.3l3.1-3.5 1.9 2.1 1.5-1.7 2 2.5", VS_PHOTO)
        + f'<circle cx="6.1" cy="6.2" r="1.05" fill="{VS_PHOTO}"/>'
    )


def http_icon() -> str:
    return path("M5.6 4.4h7v9.2h-7z", VS_WINDOW) + path("M5.6 6.7h7", VS_WINDOW, 1.1) + globe_overlay()


def file_badge(colour: str, glyph: str, sheet_colour: str = GRAY) -> str:
    gx, gy, gs = 3.9, 5.1, 7.8          # glyph box inside the page body
    return (
        sheet(sheet_colour)
        + f'<g transform="translate({gx} {gy}) scale({gs / 8.0})">'
        + f'<path d="{glyph}" stroke="{colour}" stroke-width="{1.05 * 8 / gs:.2f}" fill="none" '
          'stroke-linecap="round" stroke-linejoin="round"/></g>'
    )


def file_letters(colour: str, letters: str, sheet_colour: str = GRAY) -> str:
    gx, gy, gs = 3.9, 5.1, 7.8
    step = gs / max(len(letters), 1)
    parts = [sheet(sheet_colour)]
    for index, char in enumerate(letters):
        cx = gx + step * (index + 0.5)
        parts.append(letter_centered(char, colour, cx, gy + gs / 2 + 0.25, gs * 0.74, 1.15))
    return "".join(parts)


FILE_SPECS: list[tuple[str, str, list[str]]] = [
    ("Csharp", cs_glyph(),
     ["/expui/fileTypes/Csharp.svg", "/fileTypes/Csharp.svg"]),
    ("json", file_badge(GRAY, GLYPHS["braces"]),
     ["/expui/fileTypes/json.svg", "/fileTypes/json.svg",
      "/expui/fileTypes/jsonSchema.svg", "/resharper/expui/PsiJavaScript/Json.svg"]),
    ("xml", file_badge("#6E9ED8", GLYPHS["angles"]),
     ["/expui/fileTypes/xml.svg", "/fileTypes/xml.svg", "/rider/expui/fileTypes/xml.svg",
      "/expui/fileTypes/xsd.svg", "/expui/fileTypes/wsdl.svg", "/expui/fileTypes/xhtml.svg",
      "/expui/fileTypes/xsl.svg"]),
    ("config", file_badge(GRAY_DIM, GLYPHS["gear"]),
     ["/expui/fileTypes/config.svg", "/fileTypes/config.svg"]),
    ("editorConfig", file_badge(GRAY_DIM, GLYPHS["gear"]),
     ["/expui/fileTypes/editorConfig.svg", "/nodes/editorconfig.svg"]),
    ("markdown", file_badge(ACCENT, GLYPHS["md"]),
     ["/expui/fileTypes/markdown.svg", "/fileTypes/markdown.svg"]),
    ("text", file_badge(GRAY_DIM, GLYPHS["lines"]),
     ["/expui/fileTypes/text.svg", "/fileTypes/text.svg"]),
    ("sql", file_badge("#D98E8E", GLYPHS["db"]),
     ["/expui/fileTypes/sql.svg", "/fileTypes/sql.svg"]),
    ("javaScript", file_letters("#DCDC6C", "JS"),
     ["/expui/fileTypes/javaScript.svg", "/fileTypes/javaScript.svg"]),
    ("html", file_badge(ORANGE, GLYPHS["angles"]),
     ["/expui/fileTypes/html.svg", "/fileTypes/html.svg", "/expui/fileTypes/jsp.svg",
      "/expui/fileTypes/jspx.svg"]),
    ("css", file_badge("#6E9ED8", GLYPHS["hash"]),
     ["/expui/fileTypes/css.svg", "/fileTypes/css.svg"]),
    ("yaml", file_badge(GRAY_DIM, GLYPHS["dots"]),
     ["/expui/fileTypes/yaml.svg", "/fileTypes/yaml.svg"]),
    ("properties", file_badge(GRAY_DIM, GLYPHS["equals"]),
     ["/expui/fileTypes/properties.svg", "/fileTypes/properties.svg",
      "/expui/fileTypes/toml.svg"]),
    ("shell", file_badge(GRAY, GLYPHS["prompt"]),
     ["/expui/fileTypes/shell.svg"]),
    ("docker", file_badge(BLUE, GLYPHS["box"]),
     ["/expui/fileTypes/docker.svg"]),
    ("gitignore", file_badge(ORANGE, GLYPHS["git"]),
     ["/expui/fileTypes/gitignore.svg"]),
    ("csv", file_badge(GREEN, GLYPHS["grid"]),
     ["/expui/fileTypes/csv.svg"]),
    ("image", photo_icon(),
     ["/expui/fileTypes/image.svg"]),
    ("archive", file_badge(GOLD, GLYPHS["box"]),
     ["/expui/fileTypes/archive.svg"]),
    ("binaryData", file_badge(GRAY_DIM, GLYPHS["dots"]),
     ["/expui/fileTypes/binaryData.svg"]),
    ("font", file_badge(GRAY, "M1 6.8L3 1l2 5.8M1.7 4.9h2.6"),
     ["/expui/fileTypes/font.svg"]),
    ("manifest", file_badge(GRAY_DIM, GLYPHS["lines"]),
     ["/expui/fileTypes/manifest.svg"]),
    ("http", http_icon(),
     ["/expui/fileTypes/http.svg"]),
    ("regexp", file_badge(GRAY_DIM, GLYPHS["star"]),
     ["/expui/fileTypes/regexp.svg"]),
    ("gradle", file_badge(TEAL, GLYPHS["box"]),
     ["/expui/fileTypes/gradle.svg", "/expui/fileTypes/groovy.svg"]),
    ("unknownFile", sheet(GRAY_DIM), ["/expui/fileTypes/unknown.svg"]),
    ("diagram", file_badge(GRAY, GLYPHS["grid"]),
     ["/expui/fileTypes/diagram.svg", "/expui/fileTypes/uml.svg"]),
    ("scratch", file_badge(GRAY_DIM, GLYPHS["lines"]),
     ["/expui/fileTypes/scratch.svg", "/expui/fileTypes/scratches.svg"]),
    ("patch", file_badge(GOLD, GLYPHS["wrench"]),
     ["/expui/fileTypes/patch.svg", "/expui/fileTypes/diff.svg"]),
    ("svgImage", photo_icon(),
     ["/icons/expui/less.svg", "/icons/less.svg", "/icons/expui/sass.svg"]),
    ("i18n", file_badge(GREEN, GLYPHS["globe"]),
     ["/expui/fileTypes/i18n.svg"]),
    ("jupyter", file_badge(ORANGE, GLYPHS["star"]),
     ["/expui/fileTypes/jupyter.svg"]),
    ("terraform", file_badge(PURPLE, GLYPHS["box"]),
     ["/expui/fileTypes/terraform.svg"]),
    ("vue", file_badge(GREEN, GLYPHS["angles"]),
     ["/expui/fileTypes/vue.svg"]),

    # --- .NET / Rider specific -------------------------------------------------
    ("csharpFile",
     cs_glyph(),
     ["/resharper/expui/PsiCSharp/Csharp.svg", "/resharper/PsiCSharp/Csharp.svg"]),
    ("csProject",
     vs_window(globe_overlay()),
     ["/resharper/expui/ProjectModel/CsharpProject.svg",
      "/resharper/ProjectModel/CsharpProject.svg"]),
    ("csLibraryProject",
     vs_window(csharp_overlay()),
     ["/resharper/expui/ProjectModel/CsharpCoreProject.svg",
      "/resharper/expui/ProjectModel/CsharpLegacyProject.svg",
      "/resharper/ProjectModel/CsharpCoreProject.svg",
      "/resharper/ProjectModel/CsharpLegacyProject.svg"]),
    ("csprojFile",
     file_letters(CSHARP_GREEN, "C#"),
     ["/resharper/expui/ProjectModel/CsharpProj.svg", "/resharper/ProjectModel/CsharpProj.svg"]),
    ("vbProject",
     f'<rect x="2.4" y="2.6" width="11.2" height="10.8" rx="1.8" fill="{GREEN}"/>'
     + letter_centered("V", WHITE, 6.4, 8.2, 5.4, 1.15)
     + letter_centered("B", WHITE, 10.2, 8.2, 5.4, 1.15),
     ["/resharper/expui/ProjectModel/VbasicProj.svg",
      "/resharper/ProjectModel/VbasicProj.svg"]),
    ("solutionFile",
     vs_window(csharp_overlay()),
     ["/rider/expui/fileTypes/solution.svg", "/rider/fileTypes/solution.svg",
      "/rider/expui/templates/TemplateSolution.svg"]),
    ("solutionFolder",
     path(FOLDER_PATH, GOLD) + path("M9.6 8.6h3v3h-3z", ACCENT, 1.1),
     ["/rider/expui/nodes/FolderSolution.svg"]),
    ("razorFile",
     file_badge(PURPLE, GLYPHS["at"]),
     ["/resharper/expui/PsiRazor/Razor.svg", "/resharper/PsiRazor/Razor.svg",
      "/resharper/expui/ServicesRazor/ScopeRazor.svg",
      "/rider/expui/templates/TemplateRazor.svg"]),
    ("xamlFile",
     file_badge("#6E9ED8", GLYPHS["angles"]),
     ["/resharper/expui/CommonFeaturesOptions/Xaml.svg",
      "/resharper/ServicesXaml/ScopeXaml.svg", "/resharper/CommonFeaturesOptions/Xaml.svg"]),
    ("resxFile",
     file_badge("#C8A165", GLYPHS["grid"]),
     ["/resharper/expui/LiveTemplatesResx/Resx.svg"]),
    ("androidXml",
     file_badge(GREEN, GLYPHS["angles"]),
     ["/rider/expui/fileTypes/axml.svg", "/rider/fileTypes/axml.svg"]),
    ("publishProfile",
     file_badge(ACCENT, GLYPHS["arrow"]),
     ["/rider/expui/publish/pubxml.svg"]),
    ("cshtml",
     file_letters(PURPLE, "@C"),
     ["/rider/expui/templates/TemplateConsoleApp.svg"]),
]

for _name, _markup, _targets in FILE_SPECS:
    add(_name, _markup, *_targets)

# --------------------------------------------------------------------------
# other languages -- the same sheet + badge language, one letter per language
# --------------------------------------------------------------------------
LANG_SPECS: list[tuple[str, str, str]] = [
    ("c", "C", "#6E9ED8"),
    ("cpp", "C", "#5A8FD0"),
    ("h", "H", "#6E9ED8"),
    ("java", "J", "#E8A06A"),
    ("javaClass", "J", "#D98E8E"),
    ("swiftLang", "S", "#E8A06A"),
    ("perl", "P", "#6E9ED8"),
    ("actionScript", "A", "#D98E8E"),
    ("idl", "I", GRAY_DIM),
    ("bazel", "B", GREEN),
    ("aspectJ", "A", "#A8B8C8"),
    ("rst", "R", GRAY_DIM),
    ("sourceMap", "M", GRAY_DIM),
    ("toml", "T", GRAY_DIM),
    ("modified", "M", "#D7BA7D"),
    ("ignored", "I", GRAY_DIM),
    ("contexts", "C", GRAY_DIM),
    ("contextsModifier", "C", GRAY_DIM),
]

# --------------------------------------------------------------------------
# .NET nodes of Rider's own Solution Explorer (ReSharper icon set)
# --------------------------------------------------------------------------
def _rs(*names: str) -> list[str]:
    return [f"/resharper/ProjectModel/{n}.svg" for n in names] + \
           [f"/resharper/expui/ProjectModel/{n}.svg" for n in names]


add("dotnetFolder", path(FOLDER_PATH, GOLD),
    *_rs("SolutionFolder", "Folder", "FolderWWWRootClosed", "FolderWWWRootOpened", "MissingFolder"))

add("dotnetProject", vs_window(csharp_overlay()),
    *_rs("Project", "Projects", "Directory", "SharedProject", "MauiProject",
         "DotNetCoreProject", "DotNetLegacyProject", "UnloadedProject"))

# --- Dependencies tree nodes (Visual Studio's Solutions Explorer palette) ---
add("depAssemblies",
    path("M2.4 4.6h7.6v7.4H2.4z", GRAY)
    + path("M10.6 9.2h1.6a1.9 1.9 0 0 0 0-3.8h-1.6", VS_GLOBE, 1.1)
    + path("M12.2 10.2h1.5a1.9 1.9 0 0 0 0-3.8h-1.5", VS_GLOBE, 1.1),
    *_rs("Assemblies", "AssemblyReference", "Assembly"))

add("depFrameworks",
    badge_outline(GRAY, 3.6, 4.0, 9.4, 1.8)
    + f'<rect x="1.4" y="5.6" width="2.4" height="2.4" rx="0.6" fill="{VS_GLOBE}"/>'
    + path("M3.8 6.8h2.4M6.2 8.4h6", GRAY, 1.0),
    *_rs("FrameworkFolder", "FrameworkRef", "FrameworkRefIssue", "FrameworkRefLock"))

add("depPackages",
    badge_outline(GRAY, 3.0, 4.2, 9.4, 1.8)
    + f'<circle cx="7.7" cy="8.7" r="1.5" fill="{GRAY}"/>'
    + f'<circle cx="12.8" cy="3.6" r="1.1" fill="{GRAY}"/>',
    *_rs("NuGet"))

add("depProjectsNode",
    path("M2.8 3.6h10.4v9.2H2.8z", GRAY) + path("M2.8 6.4h10.4", GRAY, 1.1),
    *_rs("Projects"))

add("depAnalyzers",
    path("M5.0 3.8h8M5.0 6.3h8M5.0 8.8h5.6", GRAY)
    + f'<circle cx="3.4" cy="10.9" r="2.1" stroke="{VS_GLOBE}" stroke-width="1.1"/>'
    + path("M3.4 10.3v.2M3.4 11.5v1.0", VS_GLOBE, 0.9),
    *_rs("SDKs"))

add("depSourceGenerators",
    path(FOLDER_PATH, GOLD)
    + path("M11.8 6.2l.5 1.4 1.4.5-1.4.5-.5 1.4-.5-1.4-1.4-.5 1.4-.5z", ACCENT, 1.1),
    *_rs("SourceGenerator"))

for _name, _letter, _colour in LANG_SPECS:
    add(f"ft_{_name}", file_letters(_colour, _letter), f"/expui/fileTypes/{_name}.svg")

add("ft_changedFile", file_letters("#D7BA7D", "M"),
    "/expui/fileTypes/changedFile.svg", "/expui/fileTypes/changedFiles.svg")
