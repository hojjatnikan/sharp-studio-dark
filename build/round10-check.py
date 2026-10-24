"""Pixel-style assertion check for the VS 2026 accent round (build artifact)."""
import json
import sys

THEME = "../src/main/resources/themes/visual-studio-2022-dark.theme.json"


def get(ui, *path):
    d = ui
    for p in path:
        d = d[p]
    return d


checks = [
    (("*", "focusColor"), "#9184EE"),
    (("ActionButton", "focusedBorderColor"), "#9184EE"),
    (("Component", "focusedBorderColor"), "#9184EE"),
    (("Link", "focusedBorderColor"), "#9184EE"),
    (("SegmentedButton", "focusedSelectedButtonColor"), "#9184EE"),
    (("TabbedPane", "focusColor"), "#9184EE4D"),
    (("ToolWindow", "Button", "selectedBackground"), "#9184EE4D"),
    (("ToolWindow", "Button", "selectedForeground"), "#FFFFFF"),
    (("ProgressBar", "progressColor"), "#9184EE"),
    (("ProgressBar", "indeterminateStartColor"), "#9184EE"),
    (("ProgressBar", "indeterminateEndColor"), "#D2CCF8"),
    (("Counter", "background"), "#9184EE"),
    (("DragAndDrop", "areaBackground"), "#9184EE33"),
    (("DragAndDrop", "areaBorderColor"), "#9184EE"),
    (("SearchEverywhere", "Tab", "selectedBackground"), "#9184EE4D"),
    (("EditorTabs", "underlineColor"), "#51B3FF"),
    (("Tree", "selectionBorderColor"), "#9184EE"),
    (("List", "selectionBackground"), "#353535"),
]

ui = json.load(open(THEME, encoding="utf-8"))["ui"]
bad = 0
for path, want in checks:
    got = get(ui, *path)
    mark = "OK  " if got == want else "FAIL"
    if got != want:
        bad += 1
    print(mark, ".".join(path), "=", got, "(want %s)" % want)
print("FAILED:", bad)
sys.exit(1 if bad else 0)
