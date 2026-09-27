"""Icon specs: toolbar/menu actions, tool windows, run & debug, VCS, gutter.

Each entry is ``name -> (svg_markup, [platform icon paths])``.  Platform paths
are validated against the icon inventory of the local Rider installation by
``tools/gen_icons.py``; paths that do not exist are reported and skipped, so a
wrong guess can never break the theme.
"""
from __future__ import annotations

from icons_common import (
    ACCENT, BLUE, DARK, GOLD, GRAY, GRAY_DIM, GREEN, LIGHTBLUE, ORANGE, PURPLE,
    RED, TEAL, WHITE, YELLOW, GLYPHS, badge_filled, badge_outline, path,
    sheet, svg,
)

SPEC: dict[str, tuple[str, list[str]]] = {}
FOLDER_PATH = (
    "M1.6 4.9c0-.7.5-1.2 1.2-1.2h2.9l1.4 1.5h6.1c.7 0 1.2.5 1.2 1.2v5.5"
    "c0 .7-.5 1.2-1.2 1.2H2.8c-.7 0-1.2-.5-1.2-1.2z"
)


def add(name: str, markup: str, *targets: str, dark: bool = True) -> None:
    """Register an icon; ``dark`` also registers the ``_dark`` variant."""
    paths: list[str] = []
    for target in targets:
        paths.append(target)
        if dark:
            stem, _, ext = target.rpartition(".")
            paths.append(f"{stem}_dark.{ext}")
    SPEC[name] = (svg(markup), paths)


# ==========================================================================
# general / actions
# ==========================================================================
add("save",
    path("M3 3h7.4l2.6 2.6V13H3z", BLUE)
    + path("M5.6 3v3.4h4.8V3", BLUE)
    + path("M4.6 13V9.2h6.8V13", BLUE),
    "/expui/general/save.svg", "/actions/save.svg", "/general/save.svg")

add("saveAll",
    path("M2.4 4.4h5.2l2.4 2.4v5.6H2.4z", BLUE)
    + path("M4.4 2.4h5.4l3 3v7.2", BLUE)
    + path("M3.8 7.6h4.8v4.8H3.8z", BLUE),
    "/actions/menu-saveall.svg", "/expui/general/saveAll.svg")

HAMMER = (
    path("M9.6 2.6l3.8 3.8-6.2 6.2-3.8-3.8z", GRAY)
    + path("M5.8 8.8L2.6 12l1.4 1.4 3.2-3.2", GRAY_DIM, 1.1)
)

add("compile", HAMMER,
    "/expui/build/build.svg", "/actions/compile.svg", "/expui/run/widget/build.svg")

add("rebuild",
    HAMMER + path("M2.6 2.6l10.8 10.8", GRAY_DIM, 1.0),
    "/expui/build/rebuild.svg", "/actions/rebuild.svg")

add("undo",
    path("M3.4 6.2h3.8M7.2 6.2a4 4 0 0 1 4 4v1.2", GRAY)
    + path("M6 3.8L3.2 6.2 6 8.6", GRAY),
    "/expui/general/undo.svg", "/actions/undo.svg", "/general/undo.svg")

add("redo",
    path("M12.6 6.2H8.8M8.8 6.2a4 4 0 0 0-4 4v1.2", GRAY)
    + path("M10 3.8l2.8 2.4L10 8.6", GRAY),
    "/expui/general/redo.svg", "/actions/redo.svg", "/general/redo.svg")

add("copy",
    path("M4.6 4.6h5.2l2.2 2.2v6.2H4.6z", GRAY)
    + path("M2.4 11.2V2.4h5.4l1.6 1.6", GRAY),
    "/expui/general/copy.svg", "/actions/copy.svg", "/general/copy.svg")

add("cut",
    path("M6.2 2.4L10 9.6M9.8 2.4L6 9.6", GRAY)
    + f'<circle cx="5" cy="11.4" r="1.8" stroke="{GRAY}" stroke-width="1.1"/>'
    + f'<circle cx="11" cy="11.4" r="1.8" stroke="{GRAY}" stroke-width="1.1"/>',
    "/expui/general/cut.svg", "/actions/cut.svg", "/general/cut.svg")

add("paste",
    path("M4 3.4h8v10H4z", GRAY)
    + path("M6.2 2.2h3.6v2.4H6.2z", GRAY)
    + path("M6 7.4h4M6 9.8h4M6 12.2h2.4", GRAY_DIM),
    "/expui/general/paste.svg", "/actions/paste.svg", "/general/paste.svg")

add("delete",
    path("M3.4 4.6h9.2M6.2 4.6V3.2h3.6v1.4", GRAY)
    + path("M4.8 4.6l.7 8.2h5l.7-8.2", GRAY)
    + path("M6.8 7v4M9.2 7v4", GRAY_DIM),
    "/expui/general/delete.svg", "/actions/delete.svg", "/general/delete.svg",
    "/expui/general/gc.svg")

add("remove",
    f'<circle cx="8" cy="8" r="5.6" stroke="{GRAY}" stroke-width="1.2"/>'
    + path("M5.6 8h4.8", GRAY),
    "/expui/general/remove.svg", "/actions/remove.svg", "/general/remove.svg")

add("refresh",
    path("M13 8a5 5 0 1 1-1.7-3.7", GRAY)
    + path("M13.2 2.4v3.2h-3.2", GRAY),
    "/expui/general/refresh.svg", "/actions/refresh.svg", "/general/refresh.svg")

add("settings",
    f'<circle cx="8" cy="8" r="2.4" stroke="{GRAY}" stroke-width="1.3"/>'
    + path("M8 2.6v1.7M8 11.7v1.7M2.6 8h1.7M11.7 8h1.7", GRAY, 1.9)
    + path("M4.2 4.2l1.2 1.2M10.6 10.6l1.2 1.2M11.8 4.2l-1.2 1.2M5.4 10.6l-1.2 1.2", GRAY, 1.8),
    "/expui/general/settings.svg", "/actions/settings.svg", "/general/settings.svg")

add("search",
    f'<circle cx="7.2" cy="7.2" r="4.4" stroke="{GRAY}" stroke-width="1.2"/>'
    + path("M10.6 10.6l3.4 3.4", GRAY),
    "/expui/general/search.svg", "/actions/searchEverywhere.svg", "/general/search.svg")

add("close",
    path("M4.4 4.4l7.2 7.2M11.6 4.4l-7.2 7.2", GRAY),
    "/expui/general/close.svg", "/actions/close.svg", "/general/close.svg")

add("closeSmall",
    path("M5.4 5.4l5.2 5.2M10.6 5.4l-5.2 5.2", GRAY_DIM),
    "/expui/general/closeSmall.svg", "/expui/general/closeSmallHovered.svg")

add("chevronRight", path("M6.4 3.8L10.4 8l-4 4.2", GRAY_DIM, 1.3),
    "/expui/general/chevronRight.svg", "/expui/general/chevronRightLarge.svg")
add("chevronDown", path("M3.8 6.4L8 10.4l4.2-4", GRAY_DIM, 1.3),
    "/expui/general/chevronDown.svg", "/expui/general/chevronDownLarge.svg")
add("chevronLeft", path("M9.6 3.8L5.6 8l4 4.2", GRAY_DIM, 1.3),
    "/expui/general/chevronLeft.svg")
add("chevronUp", path("M3.8 9.6L8 5.6l4.2 4", GRAY_DIM, 1.3),
    "/expui/general/chevronUp.svg", "/expui/general/chevronUpLarge.svg")

add("expandAll",
    path("M3.4 5.2h9.2", GRAY) + path("M4.6 7.8L8 11l3.4-3.2", GRAY) + path("M4.6 11.6L8 8.4l3.4 3.2", GRAY_DIM),
    "/expui/general/expandAll.svg", "/actions/expandAll.svg", "/general/expandAll.svg")

add("collapseAll",
    path("M3.4 2.4h9.2", GRAY) + path("M4.6 5.2L8 8.4l3.4-3.2", GRAY_DIM) + path("M4.6 8.6L8 11.4l3.4-2.8", GRAY),
    "/expui/general/collapseAll.svg", "/actions/collapseAll.svg", "/general/collapseAll.svg")

add("addFile",
    sheet(GRAY, 2.4, 1.4, 8.4, 13, 2.5)
    + badge_filled(GREEN, 8.4, 8.4, 6.4, 1.6)
    + path("M11.6 9.9v3.4M9.9 11.6h3.4", WHITE, 1.1),
    "/expui/actions/addFile.svg", "/actions/addFile.svg")

add("newFolder",
    path(FOLDER_PATH, GOLD)
    + path("M10.6 8.6v4M8.6 10.6h4", GREEN, 1.4),
    "/expui/actions/newFolder.svg", "/expui/actions/addDirectory.svg", "/actions/newFolder.svg")

add("edit",
    path("M3 12.8l.6-2.6 6.4-6.4 2 2-6.4 6.4z", GRAY)
    + path("M9.2 4.6l2 2", GRAY),
    "/expui/general/edit.svg", "/actions/edit.svg", "/general/edit.svg")

add("filter",
    path("M2.6 3.4h10.8L9.4 8v4.6l-2.8-1.4V8z", GRAY),
    "/expui/general/filter.svg", "/actions/filter.svg", "/general/filter.svg")

add("pin",
    path("M9.4 2.4l4.2 4.2-1.6 1.6-1.4-.6-2.6 2.6.4 2-1.2 1.2-3-3-3-3 1.2-1.2 2 .4L6.2 4l-.6-1.4z", GRAY),
    "/expui/general/pin.svg", "/actions/pin.svg", "/general/pin.svg")

add("help",
    f'<circle cx="8" cy="8" r="5.6" stroke="{GRAY}" stroke-width="1.2"/>'
    + path("M6.3 6.4a1.8 1.8 0 1 1 2.6 1.6c-.6.3-.9.7-.9 1.3v.3", GRAY)
    + f'<circle cx="8" cy="11.4" r=".75" fill="{GRAY}"/>',
    "/expui/general/help.svg", "/actions/help.svg", "/general/help.svg")

add("moreHorizontal",
    f'<circle cx="3.6" cy="8" r="1.1" fill="{GRAY}"/><circle cx="8" cy="8" r="1.1" fill="{GRAY}"/>'
    f'<circle cx="12.4" cy="8" r="1.1" fill="{GRAY}"/>',
    "/expui/general/moreHorizontal.svg", "/general/moreHorizontal.svg")

add("moreVertical",
    f'<circle cx="8" cy="3.6" r="1.1" fill="{GRAY}"/><circle cx="8" cy="8" r="1.1" fill="{GRAY}"/>'
    f'<circle cx="8" cy="12.4" r="1.1" fill="{GRAY}"/>',
    "/expui/general/moreVertical.svg", "/general/moreVertical.svg")

add("greenCheckmark",
    f'<circle cx="8" cy="8" r="5.8" stroke="{GREEN}" stroke-width="1.3"/>'
    + path("M5.2 8.2l2 2 3.6-4.4", GREEN, 1.5),
    "/expui/general/greenCheckmark.svg", "/general/greenCheckmark.svg")

add("informationDialog",
    f'<circle cx="8" cy="8" r="5.8" stroke="{BLUE}" stroke-width="1.3"/>'
    + path("M8 7.2v4.2", BLUE, 1.4) + f'<circle cx="8" cy="5" r=".8" fill="{BLUE}"/>',
    "/expui/general/informationDialog.svg", "/general/informationDialog.svg")

add("warningDialog",
    path("M8 2.6l6 10.4H2z", YELLOW)
    + path("M8 6.6v3.2", GRAY) + f'<circle cx="8" cy="11.4" r=".75" fill="{GRAY}"/>',
    "/expui/general/warningDialog.svg", "/general/warningDialog.svg")

add("errorDialog",
    f'<circle cx="8" cy="8" r="5.8" stroke="{RED}" stroke-width="1.3"/>'
    + path("M5.8 5.8l4.4 4.4M10.2 5.8l-4.4 4.4", RED, 1.3),
    "/expui/general/errorDialog.svg", "/general/errorDialog.svg")

add("questionDialog",
    f'<circle cx="8" cy="8" r="5.8" stroke="{ACCENT}" stroke-width="1.3"/>'
    + path("M6.3 6.4a1.8 1.8 0 1 1 2.6 1.6c-.6.3-.9.7-.9 1.3v.3", ACCENT)
    + f'<circle cx="8" cy="11.4" r=".75" fill="{ACCENT}"/>',
    "/expui/general/questionDialog.svg", "/general/questionDialog.svg")

add("successDialog",
    f'<circle cx="8" cy="8" r="5.8" stroke="{GREEN}" stroke-width="1.3"/>'
    + path("M5.2 8.2l2 2 3.6-4.4", GREEN, 1.5),
    "/expui/general/successDialog.svg", "/general/successDialog.svg")

add("user",
    f'<circle cx="8" cy="5.6" r="2.6" stroke="{GRAY}" stroke-width="1.2"/>'
    + path("M3 13.4c.6-2.6 2.6-4 5-4s4.4 1.4 5 4", GRAY),
    "/expui/general/user.svg", "/general/user.svg")

add("projectStructure",
    path("M2.4 3.4h4.4v4.4H2.4zM9.2 3.4h4.4v4.4H9.2zM5.8 8.8h4.4v4.4H5.8z", GRAY),
    "/expui/general/projectStructure.svg")

add("print",
    path("M4.4 2.4h7.2v3H4.4zM2.6 5.4h10.8v5H2.6zM4.6 10.4h6.6v3.2H4.6z", GRAY),
    "/expui/general/print.svg", "/general/print.svg")

add("vcsBranch",
    f'<circle cx="5" cy="4.2" r="1.6" stroke="{GRAY}" stroke-width="1.1"/>'
    f'<circle cx="5" cy="12" r="1.6" stroke="{GRAY}" stroke-width="1.1"/>'
    f'<circle cx="11.2" cy="6.6" r="1.6" stroke="{GRAY}" stroke-width="1.1"/>'
    + path("M5 5.8v4.6M10 7.6c-1 1.4-2.3 1.6-3.4 1.6", GRAY),
    "/expui/general/vcs.svg", "/vcs/branch.svg")

# ==========================================================================
# run / debug toolbar
# ==========================================================================
add("run",
    f'<path d="M5 3.4l7.4 4.6L5 12.6z" fill="{GREEN}" stroke="{GREEN}" stroke-width="1" '
    'stroke-linejoin="round"/>',
    "/expui/run/run.svg", "/expui/gutter/run.svg")

add("debug",
    f'<circle cx="8" cy="8.4" r="3.4" stroke="{BLUE}" stroke-width="1.2"/>'
    + path("M4.6 6.2L3 4.6M11.4 6.2L13 4.6M4.6 10.6L3 12.2M11.4 10.6L13 12.2", BLUE, 1.1)
    + path("M6.6 4.6a1.6 1.6 0 0 1 2.8 0", BLUE, 1.1)
    + path("M8 2.8v1.2", BLUE, 1.1),
    "/expui/run/debug.svg", "/expui/general/debug.svg")

add("stop",
    f'<rect x="4" y="4" width="8" height="8" rx="1.2" fill="{RED}"/>',
    "/expui/run/stop.svg")

add("rerun",
    path("M13 8a5 5 0 1 1-1.7-3.7", GREEN)
    + path("M13.2 2.4v3.2h-3.2", GREEN),
    "/expui/run/rerun.svg", "/expui/run/restart.svg")

add("pause",
    path("M6 3.6v8.8M10 3.6v8.8", GRAY, 1.6),
    "/expui/run/pause.svg")

add("stepOver",
    f'<circle cx="4.4" cy="11.6" r="1.5" fill="{GRAY}"/>'
    + path("M4.4 8.6a4 4 0 0 1 7.4-2", GRAY)
    + path("M11 4.2l1.6 2.4-2.8.6", GRAY),
    "/expui/run/stepOver.svg", "/expui/run/forceStepOver.svg")

add("stepInto",
    f'<circle cx="8" cy="12" r="1.5" fill="{GRAY}"/>'
    + path("M8 2.8v6", GRAY) + path("M5.4 6.4L8 9l2.6-2.6", GRAY),
    "/expui/run/stepInto.svg", "/expui/run/forceStepInto.svg", "/expui/run/smartStepInto.svg")

add("stepOut",
    path("M8 9.2V3.4", GRAY) + path("M5.4 6l2.6-2.6L10.6 6", GRAY)
    + f'<circle cx="8" cy="4.4" r="1.5" stroke="{GRAY}" stroke-width="1.1"/>',
    "/expui/run/stepOut.svg")

add("runToCursor",
    path("M3.4 12.6h9.2", GRAY_DIM)
    + path("M4.8 9.6a3.6 3.6 0 0 1 6.4 0", GREEN)
    + f'<circle cx="8" cy="12" r="1.4" fill="{GREEN}"/>',
    "/expui/run/runToCursor.svg", "/expui/run/forceRunToCursor.svg")

add("muteBreakpoints",
    f'<circle cx="8" cy="8" r="4.2" stroke="{GRAY}" stroke-width="1.2"/>'
    + path("M5.4 10.6l5.2-5.2", GRAY_DIM, 1.1),
    "/expui/run/muteBreakpoints.svg", "/expui/run/viewBreakpoints.svg")

add("attachToProcess",
    path("M4.6 6.6h6.8v4.2a3.4 3.4 0 0 1-6.8 0z", GRAY)
    + path("M6.6 6.6V4.8a1.4 1.4 0 0 1 2.8 0v1.8", GRAY)
    + path("M8 2.6v2.2", GRAY),
    "/expui/run/attachToProcess.svg")

# ==========================================================================
# breakpoints (editor gutter -- Visual Studio red circles)
# ==========================================================================
add("breakpoint",
    f'<circle cx="8" cy="8" r="4.6" fill="{RED}"/>',
    "/expui/breakpoints/breakpoint.svg", "/expui/breakpoints/breakpointValid.svg")

add("breakpointDisabled",
    f'<circle cx="8" cy="8" r="4.6" fill="none" stroke="{GRAY_DIM}" stroke-width="1.2"/>',
    "/expui/breakpoints/breakpointDisabled.svg", "/expui/breakpoints/breakpointMuted.svg",
    "/expui/breakpoints/breakpointInvalid.svg")

add("breakpointException",
    f'<circle cx="8" cy="8" r="4.6" fill="{RED}"/>'
    + path("M8 5.4v3.4", WHITE, 1.2) + f'<circle cx="8" cy="10.8" r=".7" fill="{WHITE}"/>',
    "/expui/breakpoints/breakpointException.svg", "/expui/breakpoints/breakpointObsolete.svg")

add("breakpointConditional",
    f'<circle cx="8" cy="8" r="4.6" fill="{RED}"/>'
    + path("M5.6 9.4c1.2-1 1.6-1.4 3-2.6M10.4 9.4c-1.2-1-1.6-1.4-3-2.6", WHITE, 1.1),
    "/expui/breakpoints/conditionalInstrumentation.svg",
    "/expui/breakpoints/loggingInstrumentation.svg")

# ==========================================================================
# gutter
# ==========================================================================
add("fold",
    path("M3.4 8h9.2", GRAY_DIM)
    + path("M5.6 5.4L8 7.8l2.4-2.4", GRAY_DIM, 1.1),
    "/expui/gutter/fold.svg", "/expui/gutter/foldBottom.svg")

add("unfold",
    path("M3.4 8h9.2", GRAY_DIM)
    + path("M5.6 10.4L8 8l2.4 2.4", GRAY_DIM, 1.1),
    "/expui/gutter/unfold.svg")

add("bookmark",
    path("M4.4 2.6h7.2v10.8L8 10.6l-3.6 2.8z", ACCENT),
    "/expui/gutter/bookmark.svg", "/expui/gutter/bookmarkHovered.svg")

add("runSuccess",
    f'<circle cx="8" cy="8" r="5.6" fill="{GREEN}"/>'
    + path("M5.4 8.2l2 2 3.4-4.2", WHITE, 1.4),
    "/expui/gutter/runSuccess.svg")

add("runFailed",
    f'<circle cx="8" cy="8" r="5.6" fill="{RED}"/>'
    + path("M5.8 5.8l4.4 4.4M10.2 5.8l-4.4 4.4", WHITE, 1.3),
    "/expui/gutter/runFailed.svg")

add("runError",
    f'<circle cx="8" cy="8" r="5.6" fill="{ORANGE}"/>'
    + path("M8 5v3.6", WHITE, 1.3) + f'<circle cx="8" cy="10.8" r=".75" fill="{WHITE}"/>',
    "/expui/gutter/runError.svg")

# ==========================================================================
# VCS
# ==========================================================================
add("commit",
    f'<circle cx="8" cy="8" r="5.6" stroke="{GREEN}" stroke-width="1.3"/>'
    + path("M5.4 8.2l2 2 3.4-4.4", GREEN, 1.5),
    "/expui/vcs/commit.svg", "/expui/toolwindows/commit.svg")

add("update",
    f'<circle cx="8" cy="8" r="5.6" stroke="{ACCENT}" stroke-width="1.3"/>'
    + path("M8 4.6v6.2M5.4 8.2L8 10.8l2.6-2.6", ACCENT, 1.5),
    "/expui/vcs/update.svg", "/expui/vcs/fetch.svg")

add("push",
    f'<circle cx="8" cy="8" r="5.6" stroke="{ACCENT}" stroke-width="1.3"/>'
    + path("M8 11v-6.2M5.4 7.4L8 4.8l2.6 2.6", ACCENT, 1.5),
    "/expui/vcs/push.svg")

add("merge",
    path("M8 11.4V6.2M8 6.2L5 3.2M8 6.2l3-3", GRAY)
    + f'<circle cx="5" cy="2.6" r="1.3" fill="{GRAY}"/>'
    + f'<circle cx="11" cy="2.6" r="1.3" fill="{GRAY}"/>'
    + f'<circle cx="8" cy="12.4" r="1.3" fill="{GRAY}"/>',
    "/expui/vcs/merge.svg")

add("diff",
    path("M2.6 3.4h4.6v9.2H2.6zM8.8 3.4h4.6v9.2H8.8z", GRAY)
    + path("M4.4 6.4h1.6M4.4 9h1.6M9.6 6.4h1.6M9.6 9h1.6", GRAY_DIM, 1.1),
    "/expui/vcs/diff.svg", "/expui/vcs/changes.svg", "/expui/toolwindows/changes.svg")

add("revert",
    path("M13 8a5 5 0 1 1-1.7-3.7", ORANGE)
    + path("M13.2 2.4v3.2h-3.2", ORANGE),
    "/expui/vcs/revert.svg")

add("abort",
    path("M4.4 4.4l7.2 7.2M11.6 4.4l-7.2 7.2", RED, 1.3),
    "/expui/vcs/abort.svg", "/expui/vcs/abort_stroke.svg")

add("shelve",
    path("M2.6 6h10.8M2.6 9.4h10.8M2.6 12.6h10.8", GRAY)
    + path("M5.4 3h5.2", GRAY_DIM),
    "/expui/vcs/shelve.svg", "/expui/vcs/unshelve.svg")

# ==========================================================================
# tool windows (16px and 20px stripes)
# ==========================================================================
add("twProject",
    path("M2.6 3.4h5.2v5.2H2.6z", ACCENT)
    + path("M8.2 7.4h5.2v5.2H8.2z", ACCENT)
    + path("M7.8 6l.4 1.4", ACCENT, 1.1),
    "/expui/toolwindows/project.svg", "/expui/toolwindows/project@20x20.svg")

add("twBuild",
    path("M9.6 2.6l3.8 3.8-6.2 6.2-3.8-3.8z", GRAY)
    + path("M5.8 8.8L2.6 12l1.4 1.4 3.2-3.2", GRAY_DIM, 1.1),
    "/expui/toolwindows/build.svg", "/expui/toolwindows/build@20x20.svg")

add("twDebug",
    f'<circle cx="8" cy="8.4" r="3.4" stroke="{BLUE}" stroke-width="1.2"/>'
    + path("M4.6 6.2L3 4.6M11.4 6.2L13 4.6M4.6 10.6L3 12.2M11.4 10.6L13 12.2", BLUE, 1.1)
    + path("M6.6 4.6a1.6 1.6 0 0 1 2.8 0M8 2.8v1.2", BLUE, 1.1),
    "/expui/toolwindows/debug.svg", "/expui/toolwindows/debug@20x20.svg")

add("twRun",
    f'<circle cx="8" cy="8" r="5.6" stroke="{GREEN}" stroke-width="1.2"/>'
    + f'<path d="M6.4 5.4l4.4 2.6-4.4 2.6z" fill="{GREEN}"/>',
    "/expui/toolwindows/run.svg", "/expui/toolwindows/run@20x20.svg")

add("twProblems",
    path("M8 2.4l6.2 10.8H1.8z", YELLOW)
    + path("M8 6.4v3.2", GRAY, 1.1) + f'<circle cx="8" cy="11.4" r=".7" fill="{GRAY}"/>',
    "/expui/toolwindows/problems.svg", "/expui/toolwindows/problems@20x20.svg")

add("twStructure",
    path("M3 3.4h3.4v3H3zM3 9.6h3.4v3H3zM9.6 9.6h3.4v3H9.6z", GRAY)
    + path("M6.4 4.9h3.2v6.2", GRAY_DIM, 1.1),
    "/expui/toolwindows/structure.svg", "/expui/toolwindows/structure@20x20.svg")

add("twServices",
    path("M2.8 3.2h10.4v3.4H2.8zM2.8 9.4h10.4v3.4H2.8z", GRAY)
    + path("M4.6 4.9h2M4.6 11.1h2", GRAY_DIM, 1.1),
    "/expui/toolwindows/services.svg", "/expui/toolwindows/services@20x20.svg")

add("twVcs",
    f'<circle cx="5" cy="4.2" r="1.7" stroke="{GRAY}" stroke-width="1.1"/>'
    f'<circle cx="5" cy="11.8" r="1.7" stroke="{GRAY}" stroke-width="1.1"/>'
    f'<circle cx="11.2" cy="6.4" r="1.7" stroke="{GRAY}" stroke-width="1.1"/>'
    + path("M5 5.9v4.2M10 7.4c-1 1.4-2.4 1.7-3.5 1.7", GRAY),
    "/expui/toolwindows/vcs.svg", "/expui/toolwindows/vcs@20x20.svg")

add("twTerminal",
    path("M2.4 3.2h11.2v9.6H2.4z", GRAY)
    + path("M4.8 6.4l1.8 1.6-1.8 1.6M8.4 9.9h3", GRAY_DIM, 1.1),
    "/icons/expui/toolwindow/terminal.svg", "/expui/toolwindows/terminal.svg")

add("twNotifications",
    path("M8 2.6a3.6 3.6 0 0 1 3.6 3.6c0 2.4.8 3.4 1.4 3.8H3c.6-.4 1.4-1.4 1.4-3.8A3.6 3.6 0 0 1 8 2.6z", GRAY)
    + path("M6.6 12.2a1.5 1.5 0 0 0 2.8 0", GRAY, 1.1),
    "/expui/toolwindows/notifications.svg", "/expui/toolwindows/notifications@20x20.svg")

add("twMessages",
    path("M2.6 4.2h10.8v6.4H7.4l-3 3v-3H2.6z", GRAY),
    "/expui/toolwindows/messages.svg", "/expui/toolwindows/messages@20x20.svg")

add("twBookmarks",
    path("M4.8 2.6h6.4v10.8L8 10.6l-3.2 2.8z", ACCENT),
    "/expui/toolwindows/bookmarks.svg", "/expui/toolwindows/bookmarks@20x20.svg")

add("twTodo",
    path("M2.6 3.4h4.2v4.2H2.6zM2.6 9.6h4.2v4.2H2.6z", GRAY)
    + path("M9.4 4.6h4.2M9.4 6.6h4.2M9.4 10.8h4.2M9.4 12.6h3", GRAY_DIM, 1.1),
    "/expui/toolwindows/todo.svg", "/expui/toolwindows/todo@20x20.svg")

add("twCoverage",
    path("M3 12.6V8.4M8 12.6V3.4M13 12.6V6", GRAY, 1.6),
    "/expui/toolwindows/coverage.svg", "/expui/toolwindows/coverage@20x20.svg")

add("twProfiler",
    path("M2.6 11.4a5.4 5.4 0 1 1 10.8 0", GRAY)
    + path("M8 11.4l3.2-4", ACCENT, 1.3)
    + f'<circle cx="8" cy="11.6" r="1.1" fill="{GRAY_DIM}"/>',
    "/expui/toolwindows/profiler.svg", "/expui/toolwindows/profiler@20x20.svg")

add("twDependencies",
    path("M2.6 4.4h4v4h-4zM9.4 7.6h4v4h-4zM6.6 6.4h2.8", GRAY),
    "/expui/toolwindows/dependencies.svg", "/expui/toolwindows/dependencies@20x20.svg")

add("twDocumentation",
    path("M3 3.2h4a2 2 0 0 1 1 1.8 2 2 0 0 1 1-1.8h4v8.4H9a2 2 0 0 0-1 1 2 2 0 0 0-1-1H3z", GRAY),
    "/expui/toolwindows/documentation.svg", "/expui/toolwindows/documentation@20x20.svg")

add("twHierarchy",
    path("M8 2.6v3M4 8.4V6.6h8v1.8M2.6 10h3v3.4h-3zM6.5 10h3v3.4h-3zM10.4 10h3v3.4h-3z", GRAY),
    "/expui/toolwindows/hierarchy.svg", "/expui/toolwindows/hierarchy@20x20.svg")

add("twFind",
    f'<circle cx="7" cy="7" r="4.2" stroke="{GRAY}" stroke-width="1.2"/>'
    + path("M10 10l3.6 3.6", GRAY),
    "/expui/toolwindows/find.svg", "/expui/toolwindows/find@20x20.svg")

add("twWeb",
    f'<circle cx="8" cy="8" r="5.6" stroke="{GRAY}" stroke-width="1.1"/>'
    + path("M2.6 8h10.8M8 2.4c2 1.8 2 9 0 11.2M8 2.4c-2 1.8-2 9 0 11.2", GRAY, 1.0),
    "/expui/toolwindows/web.svg", "/expui/toolwindows/web@20x20.svg")

add("twTask",
    path("M3.4 3.4h9.2v10.2H3.4z", GRAY)
    + path("M5.8 2.4h4.4v2H5.8z", GRAY, 1.0)
    + path("M5.8 7.6l1.4 1.4 2.8-3", GRAY_DIM, 1.1),
    "/expui/toolwindows/task.svg", "/expui/toolwindows/task@20x20.svg")

add("twPalette",
    path("M8 2.6a5.4 5.4 0 0 0 0 10.8c1 0 1.4-.8 1-1.6-.6-1 .2-2.2 1.4-2.2h1.2a1.8 1.8 0 0 0 1.8-1.8A5.4 5.4 0 0 0 8 2.6z", GRAY)
    + f'<circle cx="5.8" cy="6.4" r=".9" fill="{RED}"/>'
    + f'<circle cx="8.6" cy="5.6" r=".9" fill="{GREEN}"/>'
    + f'<circle cx="5.4" cy="9.2" r=".9" fill="{BLUE}"/>',
    "/expui/toolwindows/palette.svg", "/expui/toolwindows/palette@20x20.svg")

add("twRepositories",
    path("M2.6 3.4h10.8v3.4H2.6zM2.6 9.2h10.8v3.4H2.6z", GRAY)
    + path("M5 5.1h1.6M5 10.9h1.6", GRAY_DIM, 1.1),
    "/expui/toolwindows/repositories.svg", "/expui/toolwindows/repositories@20x20.svg")

add("twLearn",
    path("M2.6 3.6l5.4-1.4 5.4 1.4-5.4 1.4z", GRAY)
    + path("M4.2 5.4v3.2c0 1 1.7 1.8 3.8 1.8s3.8-.8 3.8-1.8V5.4", GRAY, 1.1),
    "/expui/toolwindows/learn.svg", "/expui/toolwindows/learn@20x20.svg")
