# Sharp Studio Dark — Visual Studio 2026–Style Theme and Icons for JetBrains Rider

A theme plugin that makes Rider look like **Visual Studio 2026 (Dark)**: shell colors, editor color scheme, and an icon pack in VS’s visual language. 

Colors were sampled from your **actual VS screenshots** (not from memory), and theme keys were taken from Rider’s official theme for this build so all keys remain valid. 

<<<<<<< HEAD
- نصب‌شده و فعال روی: **Rider 2026.2.1** (build `262.9437.287`)
- پوشهٔ تنظیمات: `%APPDATA%\JetBrains\Rider2026.2`
- نام پلاگین: **Sharp Studio Dark** (شناسه `com.hnikan.sharpstudiodark`، پوشهٔ `sharp-studio-dark`)
- خروجی بسته: `build/distributions/sharp-studio-dark-1.0.2.zip`
=======
- Installed and enabled on: **Rider 2026.2.1** (build `262.9437.287`) 
- Settings folder: `%APPDATA%\JetBrains\Rider2026.2` 
- Plugin name: **Sharp Studio Dark** (ID `com.hnikan.sharpstudiodark`, folder `sharp-studio-dark`) 
- Build output: `build/distributions/sharp-studio-dark-1.0.0.zip` 
>>>>>>> 1b9be5f5ba6a6f21d3f1ed6089eb160289cfcaaa

## What’s inside

| Section | Details |
| --- | --- |
<<<<<<< HEAD
| **تم UI** | ۶۵۸ کلید رنگ از تم پایهٔ New UI + ۱۷۷ کلید امضایی که دستی روی پالت VS قفل شده‌اند |
| **اسکیم ادیتور** | اسکیم داخلی «Visual Studio Dark» خود Rider + پالت ویرایشگر VS 2026: کلیدواژه‌ها (کنترلی و اصلاح‌کننده) `#D8A0DF` بنفش، دیسرکتیوهای Razor `#A699E6`، کامپوننت‌های Razor فیروزه‌ای، رشته `#D69D85`، عدد `#B5CEA8`، نوع `#4EC9B0`، پس‌زمینهٔ `#1E1E1E` |
| **بستهٔ آیکن** | ۲۱۰ آیکن SVG که روی **۷۱۹ مسیر آیکن** پلتفرم نگاشت شده‌اند (`expui/...` و `_dark` و مسیرهای قدیمی) |
| **رنگ‌آمیزی سراسری آیکن‌ها** | `ColorPalette` روی ۱۹ نقش رنگی، تا آیکن‌هایی که سفارشی نساخته‌ایم هم به پالت VS نزدیک شوند |
=======
| **UI Theme** | 658 color keys from the New UI base theme + 178 signature keys manually locked to the VS palette  |
| **Editor Scheme** | Rider’s built‑in “Visual Studio Dark” scheme (keyword `#569CD6`, string `#D69D85`, number `#B5CEA8`, background `#1E1E1E`)  |
| **Icon Pack** | 201 SVG icons mapped onto **627 platform icon paths** (`expui/...`, `_dark`, and legacy paths)  |
| **Global Icon Coloring** | A `ColorPalette` over 19 color roles so even icons we didn’t custom‑draw stay close to the VS palette  |
>>>>>>> 1b9be5f5ba6a6f21d3f1ed6089eb160289cfcaaa

### Shell palette (sampled from your VS)

| Surface | Color |
| --- | --- |
<<<<<<< HEAD
| نوار عنوان | `#1C1C1C` |
| نوار ابزار، منو، نوار تب‌ها | `#262626` |
| پنجره‌های ابزار (Solution Explorer، Output، …) | `#282828` |
| ادیتور و کنسول | `#1E1E1E` |
| فیلدهای ورودی و ردیف انتخاب‌شده | `#353535` |
| نوار وضعیت | `#141414` |
| خط تأکید زیر تب فعال | `#51B3FF` |
| آبی کلاسیک VS | `#007ACC` |
| نوار کنارِ آیتم فعال درخت | `#9184EE` |
| اکسنت پوستهٔ VS 2026 (فوکوس، دکمهٔ toggle انتخابی، پیشرفت، شمارنده) | `#9184EE` |
=======
| Title bar | `#1C1C1C`  |
| Toolbars, menus, tab bar | `#262626`  |
| Tool windows (Solution Explorer, Output, …) | `#282828`  |
| Editor and console | `#1E1E1E`  |
| Input fields and selected row | `#353535`  |
| Status bar | `#141414`  |
| Accent line under active tab | `#51B3FF`  |
| Classic VS blue | `#007ACC`  |
| Side bar for active tree item | `#9184EE`  |
>>>>>>> 1b9be5f5ba6a6f21d3f1ed6089eb160289cfcaaa

Key to the VS feel: selections are **flat gray**, not blue; the theme implements exactly that (`#353535` + a purple‑blue indicator beside the row). 

### Icons

<<<<<<< HEAD
آیکن‌ها با همان دستور زبان VS کشیده شده‌اند: خط‌های تکرنگ خاکستری `#C8C8C8`، پوشه‌های **طلایی** `#E8C46A` (و پوشهٔ `wwwroot` با **کرهٔ آبی** مخصوص VS)، ذخیره/بیلد **آبی**، اجرا/افزودن **سبز**، نماد C# و سولوشن **بنفش**، و کارت‌های فایل به شکل «برگهٔ خاکستری + بِجٔ رنگی».

در نسخهٔ **۱.۰.۲**، فایل‌های `.razor` از کارت بنفش `#B180D7` با صاعقهٔ سفید استفاده می‌کنند؛ فایل‌های `.css` نشان VS با `A` قرمز و فایل‌های `.js` حروف نارنجی `JS` را بدون برگه یا باکس نشان می‌دهند. فایل‌های C# هم نشان سبز `C#` را بدون قاب فایل دارند. پوشهٔ `wwwroot` طلایی با کرهٔ آبی است و تگ‌های HTML خاکستری `#808080` با مقدار صفت نارنجی `#D69D85` نمایش داده می‌شوند.

در همین نسخه، ۱۳۶ آیکن از ۲۱۰ آیکن پروژه با طرح‌های اصلی کتابخانهٔ XAML ویژوال استودیو جایگزین شده‌اند؛ این موارد آیکن‌های فایل، اکشن‌ها، پنجره‌ها و درخت پروژه را پوشش می‌دهند. موارد اختصاصی Rider که معادل مستقیمی در منبع VS ندارند، با طراحی VSمانند فعلی باقی مانده‌اند. اکسنت پوستهٔ VS 2026 نیز برای فوکوس، toggleهای انتخاب‌شده، progress bar و شمارنده‌ها روی `#9184EE` تنظیم شده است.
=======
Icons are drawn in VS’s visual language: single‑weight gray strokes `#C8C8C8`, **gold** folders `#E8C46A`, save/build in **blue**, run/add in **green**, C# and solution symbols in **purple**, and file cards as “gray tab + colored badge”. 
>>>>>>> 1b9be5f5ba6a6f21d3f1ed6089eb160289cfcaaa

Main coverage: actions (save/saveAll/undo/redo/cut/copy/paste/delete/refresh/settings/search/close/…), run and debug (run/debug/stop/rerun/step over/into/out/runToCursor/…), breakpoints (six states), gutter (fold/unfold/bookmark/run result), VCS (commit/update/push/merge/diff/revert/…), 30 tool windows (Solution Explorer, Build, Debug, Problems, Terminal, Structure, Tests, …), member symbols (class/interface/enum/record/method/property/field/constant/…), and file types (C#, json, xml, markdown, sql, csproj, sln, razor, xaml, resx, and 18 more languages). 

## Installation and activation

The plugin is installed under `%APPDATA%\JetBrains\Rider2026.2\plugins\rider-visual-studio-2022-look\` and the theme is already active.  To install on any other Rider:

```bash
python tools/build_plugin.py                      # package the plugin
python tools/install_rider.py --list              # list Rider settings folders
python tools/install_rider.py                     # install + enable theme and scheme
python tools/install_rider.py --restore           # revert to previous settings
```

Manually equivalent: `Settings | Appearance & Behavior | Appearance` → set `Theme` to **Visual Studio 2022 Dark** and `Editor color scheme` to **Visual Studio Dark**. 

You can restore the previous theme and scheme from `laf.xml.bak` and `colors.scheme.xml.bak` in the same `options` folder. 

## Why it didn’t look like VS at first (most important point)

Third‑party icon packs active on this install — **VSCode Icons** (`com.jtracker.vscodeicons`) and **Catppuccin Icons** (`com.github.catppuccin.jetbrains_icons`) — override icons via their own `IconPathPatcher` and **take priority over the theme’s icon mapping**.  Result: colors and layout from the theme applied, but icons stayed gray / from other packs. 

After disabling those two, the theme’s icons appeared in **your PlanDataMiner solution**: projects as blue `C#` tiles, folders in gold, `appsettings.json` with a gold `{}` badge, `.jpg` files with a blue image badge, `.cs` with a purple C# badge, and `.txt` with a text badge. 

The installer now does this automatically:

| Task | Details |
| --- | --- |
| Enable theme and editor scheme | `options/laf.xml` and `options/colors.scheme.xml`  |
| Disable conflicting icon packs | `disabled_plugins.txt` (skippable with `--keep-icon-packs`)  |
| Show the main toolbar | `options/ui.lnf.xml` (skippable with `--keep-toolbar-hidden`)  |

```bash
python tools/install_rider.py                        # all of the above, with backups
python tools/install_rider.py --keep-icon-packs       # if you want your own icon pack
python tools/install_rider.py --restore              # full rollback (theme, scheme, plugins, layout)
```

## Limits of a “theme” in Rider

A theme only changes colors and icons, not layout. These differences are structural and cannot be changed by a theme: 

- VS has a **global toolbar** with Save/Undo/Redo/Debug buttons and an “Any CPU” dropdown. In JetBrains’ New UI the toolbar is collapsed into a small group in the title bar; I enabled `SHOW_MAIN_TOOLBAR`, but the full VS‑style row exists only in **Classic UI**. 
- VS shows panels as docked tabs; New UI uses **side stripes**. 
- Minimap, inlay hints, the hamburger menu, and the assistant panel (Junie) are Rider‑specific and have no VS equivalents. 

If you like, I can also configure and test the theme for **Classic UI**; that mode is closer to VS in terms of layout. 

## Reproduction and development

```bash
python tools/scan_platform.py --extract-themes ref/themes --extract-schemes ref/schemes --dump-icons ref/icon-paths.txt
<<<<<<< HEAD
python tools/gen_icons.py        # ۲۰۱ آیکن + build/icon-map.json (مسیرها با فهرست آیکن‌های خود IDE اعتبارسنجی می‌شوند)
python tools/vs_icons.py         # جایگزینی آیکن‌های دارای همتای VS با SVG تبدیل‌شده از xaml/
python tools/build_theme.py      # تم نهایی در src/main/resources/themes
python tools/build_plugin.py     # JAR/ZIP قابل نصب
python tools/contact_sheet.py    # برگهٔ HTML همهٔ آیکن‌ها برای مرور چشمی
=======
python tools/gen_icons.py        # 201 icons + build/icon-map.json (paths validated against the IDE’s own icon list)
python tools/build_theme.py      # final theme in src/main/resources/themes
python tools/build_plugin.py     # installable JAR/ZIP
python tools/contact_sheet.py    # HTML sheet of all icons for visual review
>>>>>>> 1b9be5f5ba6a6f21d3f1ed6089eb160289cfcaaa
```

| File | Role |
| --- | --- |
| `tools/vs_palette.py` | VS palette (sampled colors) + palette ramps + signature keys + icon palette  |
| `tools/build_theme.py` | Takes `expUI_dark` as a skeleton of keys and recolors it with the VS palette  |
| `tools/icons_common.py` | Drawing utilities: file tab, letter tile, file badge, small line font  |
| `tools/icons_ui.py`, `tools/icons_files.py` | Icon specs and mappings  |
| `tools/gen_icons.py` | SVG generation + path validation against `ref/icon-paths.txt`  |
| `tools/probe_screenshot.py` | Sample colors from VS screenshots and crop reference areas  |

For an official JetBrains build (requires downloading Rider ≈ 2 GB): `build.gradle.kts` with IntelliJ Platform Gradle Plugin 2.x is ready (`./gradlew buildPlugin`).  The currently tested path is the Python scripts, which work without downloading anything. 

## Test results

- IDE log: plugin `com.hnikan.rider.visualstudio2022` loaded with no theme or icon errors/warnings. 
- `Settings → Appearance` shows **Visual Studio 2022 Dark** as the active theme. 
- Editor: blue keywords, turquoise type names, orange strings, `#1E1E1E` background. 
- Project tree: blue solution tile, gold `{}` badge for json, blue “M↓” for markdown, purple C# symbol for `Program.cs`. 
- Sampled colors from a real Rider window: status bar `#141414`, popup/menu `#282828`, selection `#353535`, side bars `#1C1C1C`. 
- Tested on **your solution** (`PlanDataMiner`, 59 projects) after disabling icon packs: gold folders, blue `C#` tile for projects, `{}` badge for json, blue image badge for `.jpg`, purple badge for `.cs`. 

Review images: `build/rider-project.png`, `build/test-nopacks3-tree.png` (tree with theme icons), `build/final-with-toolbar.png`, `build/icons.png` (full icon sheet). 

## Notes

1. To make the toolbar at the top of the window look more like VS (using this pack’s icons), enable **Show main toolbar** in `Settings | Appearance`. 
2. The `vscode-icons-intellij` and `Catppuccin Icons` plugins are also active on this install. In tests, this theme’s icons won for C#/json/markdown files, but if you see VSCode icons somewhere, disable that plugin. 
3. When running a second Rider instance simultaneously, the “Cannot start the IDE — agent library failed Agent_OnLoad: instrument” dialog appears. This is caused by the `-javaagent:sniarbtej.jar=...` line in `bin/rider64.exe.vmoptions` (a third‑party tool, outside this project) and is unrelated to this plugin; I did not change that file. 
4. Only the **Dark** theme is built; these icons are drawn for dark backgrounds and become low‑contrast in light themes.
