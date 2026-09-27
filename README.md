# Sharp Studio Dark — تم و آیکن به سبک Visual Studio 2026 برای JetBrains Rider

پلاگین تمی که ظاهر Rider را شبیه **Visual Studio 2026 (Dark)** می‌کند: رنگ‌های پوسته، رنگ‌بندی ادیتور و یک بستهٔ آیکن با زبان بصری VS.

رنگ‌ها از روی **اسکرین‌شات واقعی VS خودتان** نمونه‌برداری شده‌اند (نه از حافظه)، و کلیدواژه‌های تم از تم رسمی Rider همین نسخه گرفته شده تا همهٔ کلیدها برای این بیلد معتبر باشند.

- نصب‌شده و فعال روی: **Rider 2026.2.1** (build `262.9437.287`)
- پوشهٔ تنظیمات: `%APPDATA%\JetBrains\Rider2026.2`
- نام پلاگین: **Sharp Studio Dark** (شناسه `com.hnikan.sharpstudiodark`، پوشهٔ `sharp-studio-dark`)
- خروجی بسته: `build/distributions/sharp-studio-dark-1.0.0.zip`

## چه چیزی داخلش است

| بخش | توضیح |
| --- | --- |
| **تم UI** | ۶۵۸ کلید رنگ از تم پایهٔ New UI + ۱۷۷ کلید امضایی که دستی روی پالت VS قفل شده‌اند |
| **اسکیم ادیتور** | اسکیم داخلی «Visual Studio Dark» خود Rider (کلیدواژه `#569CD6`، رشته `#D69D85`، عدد `#B5CEA8`، پس‌زمینهٔ `#1E1E1E`) |
| **بستهٔ آیکن** | ۲۰۱ آیکن SVG که روی **۶۲۷ مسیر آیکن** پلتفرم نگاشت شده‌اند (`expui/...` و `_dark` و مسیرهای قدیمی) |
| **رنگ‌آمیزی سراسری آیکن‌ها** | `ColorPalette` روی ۱۹ نقش رنگی، تا آیکن‌هایی که سفارشی نساخته‌ایم هم به پالت VS نزدیک شوند |

### پالت پوسته (نمونه‌برداری‌شده از VS شما)

| سطح | رنگ |
| --- | --- |
| نوار عنوان | `#1C1C1C` |
| نوار ابزار، منو، نوار تب‌ها | `#262626` |
| پنجره‌های ابزار (Solution Explorer، Output، …) | `#282828` |
| ادیتور و کنسول | `#1E1E1E` |
| فیلدهای ورودی و ردیف انتخاب‌شده | `#353535` |
| نوار وضعیت | `#141414` |
| خط تأکید زیر تب فعال | `#51B3FF` |
| آبی کلاسیک VS | `#007ACC` |
| نوار کنارِ آیتم فعال درخت | `#9184EE` |

نکتهٔ مهم برای حس VS: در VS انتخاب‌ها **خاکستری تخت** هستند نه آبی؛ تم همین را پیاده می‌کند (`#353535` + نشانگر بنفش-آبی کنار ردیف).

### آیکن‌ها

آیکن‌ها با همان دستور زبان VS کشیده شده‌اند: خط‌های تکرنگ خاکستری `#C8C8C8`، پوشه‌های **طلایی** `#E8C46A`، ذخیره/بیلد **آبی**، اجرا/افزودن **سبز**، نماد C# و سولوشن **بنفش**، و کارت‌های فایل به شکل «برگهٔ خاکستری + بِجٔ رنگی».

پوشش اصلی: اکشن‌ها (save/saveAll/undo/redo/cut/copy/paste/delete/refresh/settings/search/close/…)، اجرا و دیباگ (run/debug/stop/rerun/step over-into-out/runToCursor/…)، نقاط توقف (شش حالت)، gutter (fold/unfold/bookmark/run result)، VCS (commit/update/push/merge/diff/revert/…)، ۳۰ پنجرهٔ ابزار (Solution Explorer، Build، Debug، Problems، Terminal، Structure، Tests، …)، نمادهای عضو (class/interface/enum/record/method/property/field/constant/…)، و انواع فایل (C#، json، xml، markdown، sql، csproj، sln، razor، xaml، resx، و ۱۸ زبان دیگر).

## نصب و فعال‌سازی

پلاگین در `%APPDATA%\JetBrains\Rider2026.2\plugins\rider-visual-studio-2022-look\` نصب شده و تم هم فعال است. برای نصب روی هر Rider دیگر:

```bash
python tools/build_plugin.py                      # بسته‌سازی
python tools/install_rider.py --list              # نمایش پوشه‌های تنظیمات Rider
python tools/install_rider.py                     # نصب + فعال‌سازی تم و اسکیم
python tools/install_rider.py --restore           # بازگشت به تنظیمات قبلی
```

معادل دستی: `Settings | Appearance & Behavior | Appearance` → `Theme` = **Visual Studio 2022 Dark** و `Editor color scheme` = **Visual Studio Dark**.

از `laf.xml.bak` و `colors.scheme.xml.bak` در همان پوشهٔ `options` می‌توانید تم و اسکیم قبلی را برگردانید.

## چرا اول شبیه VS نبود (مهم‌ترین نکته)

پک‌های آیکن ثالثی که روی این نصب فعال بودند — **VSCode Icons** (`com.jtracker.vscodeicons`) و **Catppuccin Icons** (`com.github.catppuccin.jetbrains_icons`) — آیکن‌ها را با `IconPathPatcher` خودشان جایگزین می‌کنند و **بر نگاشت آیکن تم اولویت دارند**. نتیجه: رنگ‌ها و چیدمان تم اعمال می‌شد ولی آیکن‌ها همچنان خاکستری/پک‌های دیگر می‌ماندند.

با غیرفعال‌کردن آن دو، آیکن‌های تم در **همان سولوشن PlanDataMiner** ظاهر شدند: پروژه‌ها کاشی آبی `C#`، پوشه‌ها طلایی، `appsettings.json` بِج طلایی `{}`، فایل‌های `.jpg` بِج آبی تصویر، `.cs` بِج بنفش C# و `.txt` بِج متن.

نصب‌کننده الان این کارها را خودکار انجام می‌دهد:

| کار | توضیح |
| --- | --- |
| فعال‌سازی تم و اسکیم ادیتور | `options/laf.xml` و `options/colors.scheme.xml` |
| غیرفعال‌کردن پک‌های آیکن مزاحم | `disabled_plugins.txt` (قابل رد کردن با `--keep-icon-packs`) |
| روشن‌کردن نوار ابزار اصلی | `options/ui.lnf.xml` (قابل رد کردن با `--keep-toolbar-hidden`) |

```bash
python tools/install_rider.py                        # همه‌ی موارد بالا، با بکاپ
python tools/install_rider.py --keep-icon-packs       # اگر پک آیکن خودتان را می‌خواهید
python tools/install_rider.py --restore              # بازگشت کامل (تم، اسکیم، پلاگین‌ها، چیدمان)
```

## مرزهای یک «تم» در Rider

تم فقط رنگ و آیکن را عوض می‌کند، نه چیدمان. این تفاوت‌ها ساختاری‌اند و با تم قابل تغییر نیستند:

- VS یک **نوار ابزار سراسری** با دکمه‌های Save/Undo/Redo/Debug و دراپ‌داون Any CPU دارد. در New UI جت‌برینز نوار ابزار به یک گروه جمع‌وجور در نوار عنوان تبدیل شده؛ گزینه‌اش (`SHOW_MAIN_TOOLBAR`) را روشن کرده‌ام، ولی ردیف کامل VS فقط در حالت **Classic UI** وجود دارد.
- VS پنل‌ها را به‌شکل تب‌های داک‌شده نشان می‌دهد؛ New UI از **نوارهای کناری (stripes)** استفاده می‌کند.
- مینی‌مپ، inlay hint‌ها، منوی همبرگری و پنل دستیار (Junie) اجزای Rider هستند و معادل VS ندارند.

اگر خواستید، می‌توانم تم را برای **Classic UI** هم تنظیم و تست کنم؛ آن حالت از نظر چیدمان به VS نزدیک‌تر است.

## بازتولید و توسعه

```bash
python tools/scan_platform.py --extract-themes ref/themes --extract-schemes ref/schemes --dump-icons ref/icon-paths.txt
python tools/gen_icons.py        # ۲۰۱ آیکن + build/icon-map.json (مسیرها با فهرست آیکن‌های خود IDE اعتبارسنجی می‌شوند)
python tools/build_theme.py      # تم نهایی در src/main/resources/themes
python tools/build_plugin.py     # JAR/ZIP قابل نصب
python tools/contact_sheet.py    # برگهٔ HTML همهٔ آیکن‌ها برای مرور چشمی
```

| فایل | نقش |
| --- | --- |
| `tools/vs_palette.py` | پالت VS (رنگ‌های نمونه‌برداری‌شده) + رَمپ‌های پالت + کلیدهای امضایی + پالت آیکن |
| `tools/build_theme.py` | تم پایهٔ `expUI_dark` را به‌عنوان اسکلت کلیدها برمی‌دارد و با پالت VS بازرنگی می‌کند |
| `tools/icons_common.py` | ابزار ترسیم: برگه، کاشی حرف، بِج فایل، فونت خطی کوچک |
| `tools/icons_ui.py`, `tools/icons_files.py` | مشخصات آیکن‌ها و نگاشت‌ها |
| `tools/gen_icons.py` | تولید SVG + اعتبارسنجی مسیرها بر ضد `ref/icon-paths.txt` |
| `tools/probe_screenshot.py` | نمونه‌برداری رنگ از اسکرین‌شات VS و برش نواحی مرجع |

برای بیلد با ابزار رسمی JetBrains (نیازمند دانلود Rider ≈۲GB): `build.gradle.kts` با IntelliJ Platform Gradle Plugin 2.x آماده است (`./gradlew buildPlugin`). مسیر تست‌شدهٔ فعلی همان اسکریپت‌های پایتون است که بدون دانلود کار می‌کنند.

## نتیجهٔ تست

- لاگ IDE: پلاگین `com.hnikan.rider.visualstudio2022` بارگذاری شد، بدون خطا/هشدار تم یا آیکن.
- `Settings → Appearance` تم **Visual Studio 2022 Dark** را فعال نشان می‌دهد.
- ادیتور: کلیدواژه آبی، نام تایپ‌ها فیروزه‌ای، رشته نارنجی، پس‌زمینهٔ `#1E1E1E`.
- درخت پروژه: کاشی آبی سولوشن، بِج طلایی `{}` برای json، «M↓» آبی برای markdown، نماد بنفش C# برای `Program.cs`.
- رنگ‌های نمونه‌برداری‌شده از پنجرهٔ واقعی Rider: نوار وضعیت `#141414`، popup/منو `#282828`، انتخاب `#353535`، نوارهای کناری `#1C1C1C`.
- تست روی **سولوشن خودتان** (`PlanDataMiner`، ۵۹ پروژه) پس از غیرفعال‌کردن پک‌های آیکن: پوشه‌های طلایی، کاشی آبی `C#` برای پروژه‌ها، بِج `{}` برای json، بِج آبی تصویر برای `.jpg`، بِج بنفش برای `.cs`.

عکس‌های بررسی: `build/rider-project.png`، `build/test-nopacks3-tree.png` (درخت با آیکن‌های تم)، `build/final-with-toolbar.png`، `build/icons.png` (برگهٔ همهٔ آیکن‌ها).

## نکته‌ها

1. برای اینکه نوار ابزار بالای پنجره هم شبیه VS دیده شود (با آیکن‌های همین بسته)، گزینهٔ **Show main toolbar** را در `Settings | Appearance` روشن کنید.
2. پلاگین‌های `vscode-icons-intellij` و `Catppuccin Icons` هم روی این نصب فعال‌اند. در تست‌ها آیکن‌های این تم برای فایل‌های C#/json/markdown برنده شدند، اما اگر جایی آیکن VSCode را دیدید، آن پلاگین را غیرفعال کنید.
3. هنگام اجرای دوم هم‌زمان Rider، پنجرهٔ «Cannot start the IDE — agent library failed Agent_OnLoad: instrument» ظاهر می‌شود. علتش خط `-javaagent:sniarbtej.jar=...` در `bin/rider64.exe.vmoptions` است (ابزار ثالث، بیرون از این پروژه) و به این پلاگین ربطی ندارد. من چیزی در آن فایل تغییر ندادم.
4. تنها تم **Dark** ساخته شده؛ آیکن‌های این بسته برای پس‌زمینهٔ تیره کشیده شده‌اند و در تم روشن کم‌کنتراست می‌شوند.
