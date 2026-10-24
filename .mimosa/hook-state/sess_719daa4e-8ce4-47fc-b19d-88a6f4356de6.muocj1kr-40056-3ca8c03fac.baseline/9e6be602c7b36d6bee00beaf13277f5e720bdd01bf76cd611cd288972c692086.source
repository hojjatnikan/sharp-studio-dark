"""Visual Studio 2022 (Dark) colour system.

Every value here was taken from a pixel probe of a real Visual Studio 2022
window (`tools/probe_screenshot.py`), so the chrome matches what Visual Studio
users actually see rather than a from-memory approximation.

The strategy for the theme file is:

1. Rider's own ``expUI_dark.theme.json`` ("Dark", the New UI base) is used as
   the *key skeleton* -- all of its 658 UI entries are kept, so every key is
   guaranteed to be valid for this build of the IDE.
2. Its 97 palette variables (``Gray1..14``, ``Blue1..13``, ...) are rewritten
   with Visual Studio ramps (:data:`RAMP`).  Because the skeleton references
   colours through those variable names, the whole IDE is recoloured at once.
3. The handful of surfaces that define the Visual Studio *look* -- title bar,
   chrome, tab strip, panels, status bar, selection, scrollbars -- are then
   pinned to the exact sampled values (:data:`SIGNATURE`).
"""

from __future__ import annotations

# --------------------------------------------------------------------------
# sampled from a real Visual Studio 2022 window
# --------------------------------------------------------------------------
TITLE_BAR = "#1C1C1C"      # window frame + title bar
CHROME = "#262626"         # menu bar, toolbars, editor tab strip, bottom tab row
PANEL = "#282828"          # tool windows (Solution Explorer, Output, ...)
EDITOR = "#1E1E1E"         # editor + console background
FIELD = "#353535"          # input fields, focused tree row
STATUS_BAR = "#141414"     # status bar
SCROLL_TRACK = "#2E2E2E"
SCROLL_THUMB = "#A0A0A0"

FG = "#F0F0F0"             # primary text
FG_SOFT = "#C8C8C8"        # regular text / monochrome icons
FG_MUTED = "#9A9A9A"       # secondary text, inactive tab labels
FG_DISABLED = "#6D6D6D"

ACCENT = "#51B3FF"         # accent line under the active tab
ACCENT_DEEP = "#007ACC"    # classic Visual Studio blue
SELECTION_BAR = "#9184EE"  # left indicator on the focused row

SELECTION_BG = FIELD            # Visual Studio selects with flat grey, not blue
SELECTION_BG_INACTIVE = "#2E2E2E"
SELECTION_FG = "#FFFFFF"

# --------------------------------------------------------------------------
# palette ramps -- index 1 is the darkest, the last entry the lightest
# --------------------------------------------------------------------------
RAMP: dict[str, list[str]] = {
    "Gray": [
        TITLE_BAR,   # Gray1  darkest chrome / borders
        CHROME,      # Gray2  toolbars, tabs, panel background
        "#2B2B2B",   # Gray3
        "#333333",   # Gray4
        "#3C3C3C",   # Gray5
        "#454545",   # Gray6
        "#575757",   # Gray7
        FG_DISABLED, # Gray8
        "#8C8C8C",   # Gray9
        "#A6A6A6",   # Gray10
        FG_SOFT,     # Gray11 regular foreground / icons
        "#DCDCDC",   # Gray12
        FG,          # Gray13
        "#FFFFFF",   # Gray14
    ],
    "Blue": [
        "#12283C", "#1B3A57", "#264F78", "#2A5580", "#2C6A9E", "#1F7AC0",
        ACCENT_DEEP, "#1C97EA", "#3794FF", ACCENT, "#6FB9FF", "#9CDCFE", "#C7E7FF",
    ],
    "Green": [
        "#1B2E1B", "#22391F", "#2C4A28", "#375F31", "#42793B", "#4E9347",
        "#5CAD53", "#6BB700", "#89D185", "#A9E0A0", "#C7EDBF", "#E1F7DB",
    ],
    "Yellow": [
        "#3A2E12", "#4E3D18", "#6B541F", "#8A6C28", "#A98430", "#C79A38",
        "#E0AE3E", "#CCA700", "#D7BA7D", "#E9D9A0", "#F5E8C4",
    ],
    "Red": [
        "#3A1A1A", "#4A2020", "#5E2828", "#7A3333", "#9C3F3F", "#BD4B4B",
        "#E5534B", "#F14C4C", "#F48771", "#F8B4A5", "#FFD6D6", "#FFEDEA",
    ],
    "Orange": [
        "#3A2418", "#4E3020", "#6B4229", "#875432", "#A3663C", "#BF7845",
        "#D68C4E", "#CE9178", "#E0A583", "#F0C4A8", "#FFE3CE",
    ],
    "Purple": [
        "#2A1F35", "#382945", "#4A3559", "#5E4270", "#73508A", "#8A63A5",
        "#B180D7", "#C58CE8", "#D9A7F0", "#E4CEFF", "#EEDDFF", "#F6ECFF",
    ],
    "Teal": [
        "#12332F", "#184540", "#1E5A53", "#247067", "#2A877C", "#319E90",
        "#4EC9B0", "#6FD4C0", "#92E0D0", "#B5EBE1", "#D4F5EE", "#EBFAF7",
    ],
}

# --------------------------------------------------------------------------
# exact colours for the surfaces that carry the Visual Studio identity
# --------------------------------------------------------------------------
SIGNATURE: dict[str, str] = {
    # window / chrome ------------------------------------------------------
    # NOTE: MainToolbar / TitlePane / Window / Button / CheckBox / RadioButton /
    # Component / Label keys are deliberately NOT overridden: Rider's own New UI
    # values are kept there, so the window frame and the message-box buttons stay
    # stock (a theme that touches them renders white, unlabelled buttons).
    "*.background": PANEL,
    "*.foreground": FG,
    "*.borderColor": TITLE_BAR,
    "Borders.color": TITLE_BAR,
    "Borders.ContrastBorderColor": "#3F3F46",
    "Panel.background": PANEL,
    "MenuBar.background": CHROME,
    "MenuBar.borderColor": CHROME,
    "StatusBar.background": STATUS_BAR,
    "StatusBar.borderColor": STATUS_BAR,
    "StatusBar.Widget.foreground": FG_SOFT,
    "StatusBar.Widget.hoverForeground": "#FFFFFF",
    "StatusBar.Breadcrumbs.foreground": FG_SOFT,

    # editor tabs ----------------------------------------------------------
    "EditorTabs.background": CHROME,
    "EditorTabs.underlinedTabBackground": CHROME,
    "EditorTabs.underlineColor": ACCENT,
    "EditorTabs.inactiveUnderlineColor": "#3F3F46",
    "EditorTabs.underlineHeight": 3,
    "EditorTabs.underlineArc": 0,
    "EditorTabs.underTabsBorderColor": "#1C1C1C",
    "EditorTabs.hoverBackground": "#303030",
    "EditorTabs.borderColor": TITLE_BAR,
    "DefaultTabs.background": CHROME,
    "DefaultTabs.underlinedTabBackground": CHROME,
    "DefaultTabs.underlineColor": ACCENT,
    "DefaultTabs.inactiveUnderlineColor": "#3F3F46",
    "DefaultTabs.hoverBackground": "#303030",

    # tool windows ---------------------------------------------------------
    "ToolWindow.Header.background": CHROME,
    "ToolWindow.Header.inactiveBackground": CHROME,
    "ToolWindow.Header.borderColor": "#1C1C1C",
    "ToolWindow.HeaderTab.selectedBackground": PANEL,
    "ToolWindow.HeaderTab.hoverBackground": "#303030",
    "ToolWindow.HeaderTab.hoverInactiveBackground": "#2E2E2E",
    "ToolWindow.Stripe.separatorColor": "#1C1C1C",
    "ToolWindow.Button.selectedBackground": ACCENT_DEEP,
    "Toolwindow.Stripe.background": TITLE_BAR,
    "ToolWindow.background": PANEL,

    # lists / trees --------------------------------------------------------
    "*.selectionBackground": SELECTION_BG,
    "*.selectionForeground": SELECTION_FG,
    "*.selectionInactiveBackground": SELECTION_BG_INACTIVE,
    "*.selectionBackgroundInactive": SELECTION_BG_INACTIVE,
    "*.selectionForegroundInactive": FG_SOFT,
    "*.lightSelectionBackground": SELECTION_BG,
    "*.underlineColor": ACCENT,
    "*.inactiveUnderlineColor": "#3F3F46",
    "Tree.selectionBackground": SELECTION_BG,
    "Tree.selectionForeground": SELECTION_FG,
    "Tree.selectionInactiveBackground": SELECTION_BG_INACTIVE,
    "Tree.selectionBorderColor": SELECTION_BAR,
    "Tree.hoverBackground": "#2E2E2E",
    "Tree.hoverInactiveBackground": "#2E2E2E",
    "List.selectionBackground": SELECTION_BG,
    "List.selectionForeground": SELECTION_FG,
    "List.hoverBackground": "#2E2E2E",
    "List.background": PANEL,
    "List.foreground": FG_SOFT,
    "List.border": "0,0,0,0",
    "Table.selectionBackground": SELECTION_BG,
    "Table.selectionForeground": SELECTION_FG,
    "Table.background": PANEL,
    "Table.foreground": FG_SOFT,
    "Table.gridColor": "#2E2E2E",
    "TableHeader.background": CHROME,
    "TableHeader.foreground": FG_MUTED,
    "TableHeader.separatorColor": "#1C1C1C",
    "TableHeader.bottomSeparatorColor": "#1C1C1C",

    # popups, menus, inputs ------------------------------------------------
    "Popup.background": PANEL,
    "Popup.borderColor": "#3F3F46",
    "Popup.inactiveBorderColor": "#3F3F46",
    "Popup.Header.activeBackground": PANEL,
    "Popup.Header.inactiveBackground": PANEL,
    "PopupMenu.background": PANEL,
    "MenuItem.background": PANEL,
    "MenuItem.foreground": FG_SOFT,
    "MenuItem.selectionBackground": SELECTION_BG,
    "MenuItem.selectionForeground": "#FFFFFF",
    "MenuItem.acceleratorForeground": FG_MUTED,
    "Menu.background": PANEL,
    "Menu.foreground": FG_SOFT,
    "Menu.selectionBackground": SELECTION_BG,
    "Menu.selectionForeground": "#FFFFFF",
    "Menu.separatorColor": "#3F3F46",
    "TextField.background": FIELD,
    "TextField.foreground": FG,
    "TextArea.background": FIELD,
    "TextArea.foreground": FG,
    "ComboBox.background": FIELD,
    "ComboBox.foreground": FG,
    "Editor.SearchField.background": FIELD,
    # (Button / ToggleButton / CheckBox / RadioButton / Component / Label are
    # intentionally left to Rider's own values -- see the note at the top.)
    "HelpTooltip.background": "#1B1B1C",
    "HelpTooltip.foreground": FG,
    "HelpTooltip.borderColor": "#3F3F46",
    "ToolTip.background": "#1B1B1C",
    "ToolTip.foreground": FG,
    "ToolTip.borderColor": "#3F3F46",
    "Notification.background": "#1B1B1C",
    "Notification.borderColor": "#3F3F46",
    "Notification.foreground": FG,
    "Link.activeForeground": ACCENT,
    "Link.hoverForeground": "#7FCAFF",
    "Link.visitedForeground": ACCENT,

    # scrollbars -----------------------------------------------------------
    "ScrollBar.background": SCROLL_TRACK,
    "ScrollBar.trackColor": SCROLL_TRACK,
    "ScrollBar.thumbColor": SCROLL_THUMB,
    "ScrollBar.thumbBorderColor": SCROLL_THUMB,
    "ScrollBar.hoverThumbColor": "#C8C8C8",
    "ScrollBar.hoverThumbBorderColor": "#C8C8C8",
    "ScrollBar.hoverTrackColor": SCROLL_TRACK,
    "ScrollBar.Transparent.trackColor": "#2E2E2E00",
    "ScrollBar.Transparent.thumbColor": f"{SCROLL_THUMB}B0",
    "ScrollBar.Transparent.hoverThumbColor": SCROLL_THUMB,
    "ScrollBar.Transparent.thumbBorderColor": "#00000000",
    "ScrollBar.Transparent.hoverThumbBorderColor": "#00000000",

    # misc chrome ----------------------------------------------------------
    "ProgressBar.progressColor": ACCENT_DEEP,
    "ProgressBar.trackColor": "#333333",
    "ProgressBar.indeterminateStartColor": ACCENT_DEEP,
    "ProgressBar.indeterminateEndColor": ACCENT,
    "Counter.background": ACCENT_DEEP,
    "Counter.foreground": "#FFFFFF",
    "Separator.separatorColor": "#3F3F46",
    "ToolBar.separatorColor": "#3F3F46",
    "Group.separatorColor": "#3F3F46",
    "DragAndDrop.areaBackground": "#51B3FF33",
    "DragAndDrop.areaBorderColor": ACCENT,
    "SearchEverywhere.Header.background": CHROME,
    "SearchEverywhere.Tab.selectedBackground": ACCENT_DEEP,
    "SearchEverywhere.List.settingsBackground": PANEL,
    "SearchMatch.startBackground": "#613214",
    "SearchMatch.endBackground": "#613214",
    "SpeedSearch.background": "#3F3F46",
    "SpeedSearch.foreground": FG,
    "CompletionPopup.foreground": FG_SOFT,
    "CompletionPopup.background": PANEL,
    "CompletionPopup.matchForeground": ACCENT,
    "ParameterInfo.background": PANEL,
    "ParameterInfo.foreground": FG_SOFT,
    "ParameterInfo.borderColor": "#3F3F46",
    "ParameterInfo.currentOverloadBackground": "#3A3A3A",
    "ValidationTooltip.errorBackground": "#3A1A1A",
    "ValidationTooltip.errorBorderColor": "#7A3333",
    "ValidationTooltip.warningBackground": "#3A2E12",
    "ValidationTooltip.warningBorderColor": "#8A6C28",
    "BookmarkIcon.background": "#E8C46A",
    "NavBar.background": CHROME,
    "NavBar.borderColor": "#1C1C1C",
    "Breadcrumbs.foreground": FG_MUTED,
    "Editor.Toolbar.borderColor": "#1C1C1C",
    "EditorGutter.background": EDITOR,
    "Editor.background": EDITOR,
    "Console.background": EDITOR,
    "Console.foreground": FG_SOFT,
}

# --------------------------------------------------------------------------
# named icon palettes -- recolours every platform icon towards Visual Studio
# --------------------------------------------------------------------------
ICON_PALETTE: dict[str, str] = {
    "Actions.Grey": f"{FG_SOFT}FF",
    "Actions.GreyInline": f"{FG_SOFT}FF",
    "Actions.GreyInline.Dark": f"{FG_SOFT}FF",
    "Actions.Red": "#E5534BFF",
    "Actions.Green": "#6BB700FF",
    "Actions.Blue": "#51B3FFFF",
    "Actions.Yellow": "#E8C46AFF",
    "Objects.Grey": f"{FG_SOFT}FF",
    "Objects.Red": "#E5534BFF",
    "Objects.RedStatus": "#E5534BFF",
    "Objects.Yellow": "#CCA700FF",
    "Objects.YellowDark": "#CCA700FF",
    "Objects.Green": "#6BB700FF",
    "Objects.GreenAndroid": "#6BB700FF",
    "Objects.Blue": "#51B3FFFF",
    "Objects.Purple": "#B180D7FF",
    "Objects.Pink": "#E0699CFF",
    "Objects.BlackText": "#1C1C1CFF",
}
