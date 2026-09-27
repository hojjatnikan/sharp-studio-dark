# انتشار «Sharp Studio Dark» در JetBrains Marketplace

هدف: پلاگین در پنل بازار بالا بیاید و برای همه از داخل Rider قابل نصب شود.

---

## ۱) پیش‌نیازها (یک‌بار)

1. حساب JetBrains بسازید/وارد شوید: <https://account.jetbrains.com>
2. پروفایل **Vendor** بسازید: پنل بازار → `Vendors` → نام، ایمیل (`hojjatnikan@gmail.com`) و وب‌سایت/لینک دونیت. توافق‌نامهٔ ناشر (Publisher Agreement) را بپذیرید.
3. لایسنس را انتخاب کنید. پیشنهاد: فایل `LICENSE` با متن MIT در ریشهٔ پروژه و همان گزینه در فرم.
4. مطمئن شوید بستهٔ نهایی هیچ جای‌نگهدار (placeholder) ندارد — `tools/build_plugin.py` خودش اگر `__DONATE_URL__` یا `__VENDOR_EMAIL__` باقی بماند، بیلد را متوقف می‌کند.

---

## ۲) ساخت بستهٔ نهایی

```bash
# لینک دونیت و ایمیل فروشنده پیش‌فرض همین‌ها هستند، پس کافی است:
python tools/build_plugin.py
# خروجی:
#   build/distributions/sharp-studio-dark-1.0.0.zip     <- این را آپلود می‌کنید
#   build/distributions/sharp-studio-dark.jar           <- برای نصب دستی (Install Plugin from Disk)
```

ساختار داخل ZIP درست است (`sharp-studio-dark/lib/sharp-studio-dark.jar` + `pluginIcon.svg`) و همین چیزی است که بازار و IDE انتظار دارند.

---

## ۳) آپلود در پنل بازار (روش ساده، بدون Gradle)

1. وارد پنل شوید: <https://plugins.jetbrains.com/> → `Upload plugin` (یا `Vendors → New Plugin`).
2. **Choose vendor** و `<licence>` را انتخاب کنید، سپس فایل `sharp-studio-dark-1.0.0.zip` را آپلود کنید.
3. اگر فرم پیشنهاد داد فایل را امضا کنید: می‌توانید رد کنید (اجباری نیست) و بعداً امضا اضافه کنید.
4. صفحهٔ تنظیمات پلاگین را پر کنید:
   - **Name**: `Sharp Studio Dark` (از `plugin.xml` می‌آید)
   - **Category**: `Themes`
   - **Tags**: `theme`, `dark`, `visual studio`, `c#`, `csharp`, `rider`
   - **Overview**: از داخل `plugin.xml` پر می‌شود (بخش `description`)؛ همان‌جا در پنل هم قابل ویرایش است.
   - **What's New**: از `change-notes` می‌آید.
   - **Product compatibility**: `since-build 251` و **بدون** `until-build` (بازهٔ باز؛ بازار حدسزدن نسخهٔ آینده را warning میدهد: «Version '2026.9' does not exist»).
   - **Support/Issue tracker + Source code link + Home page**: لینک مخزن گیت‌هاب و لینک دونیت PayPal (`https://www.paypal.com/paypalme/HNDeveloper`).
5. **Screenshots**: ۳ تا ۵ عکس. منابع آماده در پوشهٔ `build/`:
   - `round7-check.png` — تم کامل Rider
   - `round4-tree.png` — درخت پروژه با آیکن‌ها
   - `icons3.png` — برگهٔ کل آیکن‌ها
   برای کیفیت بهتر، از Rider خودتان عکس تازه بگیرید (پیشنهاد ۱۲۸۰×۸۰۰ یا بزرگ‌تر).
6. **Visibility**: اول `Hidden` بگذارید، چند دقیقه صبر کنید تا بررسی خودکار بازار تمام شود، خودتان از داخل IDE تست کنید (Settings → Plugins → Marketplace → جست‌وجوی Sharp Studio Dark)، بعد `Public` کنید تا برای همه در دسترس شود.

> اگر بازار ایراد گرفت، در همان صفحه «Vendor» → `Verification` دلیلش را می‌نویسد؛ رایج‌ترین‌ها: ایمیل نامعتبر، آیکن نداشتن، یا توضیحات کوتاه/مبهم.

---

## ۴) انتشار با Gradle (اختیاری، برای به‌روزرسانی‌های بعدی)

```bash
# توکن را از پنل بازار بگیرید: Profile → My Tokens
set ORG_GRADLE_PROJECT_intellijPlatformPublishingToken=<token>
./gradlew buildPlugin signPlugin publishPlugin
```
(`build.gradle.kts` با پلاگین رسمی IntelliJ Platform Gradle آماده است؛ نیاز به دانلود Rider دارد. برای آپلود دستی، مسیر پایتونی بالا کافی است.)

### نسخه‌های بعدی
1. `VERSION` را در `tools/build_plugin.py` (و `<version>` در `plugin.xml`) بالا ببرید.
2. بخش «What's new» را در `plugin.xml` به‌روز کنید (بالای `change-notes`).
3. `python tools/build_plugin.py` و آپلود بستهٔ جدید در همان صفحهٔ پلاگین → `Update`.

---

## ۵) چک‌لیست قبل از Public کردن

- [ ] ایمیل فروشنده در `plugin.xml` واقعی است (`hojjatnikan@gmail.com`).
- [ ] لینک دونیت PayPal درست است (`__DONATE_URL__` → `https://www.paypal.com/paypalme/HNDeveloper`).
- [ ] `Overview` و `What's new` نام پلاگین و «Visual Studio 2026» را دارند.
- [ ] حداقل یک اسکرین‌شات و آیکن پلاگین موجود است (`META-INF/pluginIcon.svg`).
- [ ] دسته `Themes` و برچسب‌ها پر شده‌اند.
- [ ] روی یک نصب تازهٔ Rider تست شده (نصب از Marketplace → انتخاب تم و اسکیم → ریاستارت).
- [ ] در پلاگین کد اجراشدنی نیست (فقط منابع) — این را در توضیحات هم گفته‌ایم.

---

## ۷) متن آمادهٔ پروفایل فروشنده (Add more details to your vendor profile)

این بخش اختیاری است ولی همان چیزی است که در صفحهٔ فروشندهٔ شما دیده می‌شود. مقادیر پیشنهادی برای کپی:

| فیلد پروفایل | مقدار |
| --- | --- |
| Website | تا وقتی سایت/مخزن ندارید: `https://www.paypal.com/paypalme/HNDeveloper` — بعد از ساخت مخزن، لینک گیت‌هاب را بگذارید و دونیت را در توضیحات پلاگین نگه دارید |
| Support / Issue tracker | `https://github.com/<user>/sharp-studio-dark/issues` (بعد از ساخت مخزن) |
| Source code | `https://github.com/<user>/sharp-studio-dark` |
| Donation / Funding | `https://www.paypal.com/paypalme/HNDeveloper` |
| Social | فقط شبکه‌هایی که واقعاً دارید (مثلاً GitHub یا LinkedIn) — چیزی که ندارید را خالی بگذارید |
| About / Description | متن زیر |

متن آماده برای فیلد توضیحات (انگلیسی، قابل کپی):

```
Independent C# developer building small tools for JetBrains Rider.
Sharp Studio Dark brings the Visual Studio 2026 look — window chrome, editor colour
scheme and a 210-icon pack — to Rider for C# developers who work in both IDEs.
Free to use, optional donations welcome via PayPal.
```

نکته‌ها:

- پروفایل فروشنده **قابل ویرایش** است؛ نیازی نیست همه‌چیز را همین الان کامل کنید. اول فقط Website (لینک PayPal) را بگذارید و بقیه را بعد از ساخت مخزن اضافه کنید.
- **لینک دونیت را در توضیحات پلاگین هم نگه دارید** (همان‌جایی که در `plugin.xml` داریم)؛ کاربر بیشتر همان‌جا کلیک می‌کند نه در پروفایل فروشنده.
- چک‌باکس «show the email address on the Vendor Profile Page» را تیک نزنید؛ به‌جایش Support/Issue tracker را پر کنید تا گزارش‌ها در گیت‌هاب بیاید.
- بعد از ساخت مخزن، همین لینک‌ها را به `plugin.xml` (فیلد `<vendor url>`) و README هم اضافه می‌کنیم تا همه‌جا یکسان باشد.

---

## ۶) نکتهٔ حقوقی/اسم

اسم پلاگین عمداً «Visual Studio» ندارد چون بازار استفادهٔ گمراه‌کننده از نام تجاری مایکروسافت را رد می‌کند؛ در متن توضیحات «look of Visual Studio 2026» مجاز است. همهٔ آیکن‌ها هم بازکشیدهٔ خودمان هستند (هیچ فایل مایکروسافت کپی نشده). اسکیم رنگی، مشتق از پالت JetBrains است؛ برای انتشار عمومی اگر خواستید محافظه‌کارانه‌تر باشید، تم می‌تواند به اسکیم داخلی ارجاع بدهد و کاربر خودش اسکیم را انتخاب کند.

## چیزهایی که فقط شما دارید

لینک مخزن/سایت (برای فیلدهای Support/Source)، انتخاب لایسنس نهایی، و اسکرین‌شات‌های نهایی.
