HELP_1 = """<b><u>دستورات مدیر:</b></u>

فقط کافیست <b>c</b> را در ابتدای دستورات اضافه کنید تا در کانال استفاده شوند.

/pause : توقف موقت پخش فعلی
/resume : ادامه پخش متوقف شده
/skip : رد کردن آهنگ فعلی و پخش آهنگ بعدی در صف
/end یا /stop : پاک کردن صف و پایان پخش فعلی
/player : دریافت پنل پخش تعاملی
/queue : نمایش لیست آهنگ‌های در صف
"""

HELP_2 = """
<b><u>کاربران مجاز:</b></u>

کاربران مجاز می‌توانند از دسترسی‌های مدیر در ربات استفاده کنند بدون اینکه مدیر گروه باشند.

/auth [نام کاربری/شناسه] : افزودن کاربر به لیست مجاز
/unauth [نام کاربری/شناسه] : حذف کاربر از لیست مجاز
/authusers : نمایش لیست کاربران مجاز در گروه
"""

HELP_3 = """
<u><b>ویژگی پخش همگانی</b></u> [فقط برای توسعه‌دهندگان]:

/broadcast [پیام یا ریپلای روی پیام] : ارسال پیام به تمام گروه‌های ربات

<u>حالت‌های پخش همگانی:</u>
<b>-pin</b> : سنجاق کردن پیام در گروه‌ها
<b>-pinloud</b> : سنجاق کردن پیام و ارسال اعلان به اعضا
<b>-user</b> : ارسال به کاربرانی که ربات را استارت کرده‌اند
<b>-assistant</b> : ارسال پیام از طریق اکانت دستیار
<b>-nobot</b> : عدم ارسال پیام توسط ربات

<b>مثال:</b> <code>/broadcast -user -assistant -pin تست پیام همگانی</code>
"""

HELP_4 = """<u><b>لیست سیاه گروه‌ها:</b></u> [فقط برای توسعه‌دهندگان]

جلوگیری از استفاده گروه‌های نامناسب از ربات.

/blacklistchat [شناسه گروه] : افزودن گروه به لیست سیاه
/whitelistchat [شناسه گروه] : حذف گروه از لیست سیاه 
/blacklistedchat : نمایش لیست گروه‌های در لیست سیاه
"""

HELP_5 = """
<u><b>مسدود کردن کاربران:</b></u> [فقط برای توسعه‌دهندگان]

کاربر مسدود شده نمی‌تواند از دستورات ربات استفاده کند.

/block [نام کاربری یا ریپلای] : مسدود کردن کاربر
/unblock [نام کاربری یا ریپلای] : رفع مسدودیت کاربر
/blockedusers : نمایش لیست کاربران مسدود شده
"""

HELP_6 = """
<u><b>دستورات پخش در کانال:</b></u>

می‌توانید صوت/ویدیو را در کانال پخش کنید.

/cplay : شروع پخش موزیک درخواستی در چت ویدیویی کانال
/cvplay : شروع پخش ویدیو درخواستی در چت ویدیویی کانال
/cplayforce یا /cvplayforce : توقف پخش فعلی و شروع پخش درخواستی

/channelplay [نام کاربری/شناسه کانال] یا [disable] : اتصال کانال به گروه و پخش موزیک با دستورات ارسالی در گروه
"""

HELP_7 = """
<u><b>مسدودیت سراسری</b></u> [فقط برای توسعه‌دهندگان]:

/gban [نام کاربری یا ریپلای] : مسدود کردن کاربر از تمام گروه‌های ربات
/ungban [نام کاربری یا ریپلای] : رفع مسدودیت سراسری کاربر
/gbannedusers : نمایش لیست کاربران مسدود شده سراسری
"""

HELP_8 = """
<b><u>تکرار پخش:</b></u>

<b>شروع تکرار پخش فعلی به صورت حلقه‌ای</b>

/loop [enable/disable] : فعال/غیرفعال کردن تکرار پخش فعلی
/loop [1, 2, 3, ...] : فعال کردن تکرار به تعداد مشخص شده
"""

HELP_9 = """
<u><b>حالت تعمیر و نگهداری</b></u> [فقط برای توسعه‌دهندگان]:

/logs : دریافت لاگ‌های ربات
/logger [enable/disable] : شروع ثبت فعالیت‌های انجام شده
/maintenance [enable/disable] : فعال یا غیرفعال کردن حالت تعمیر و نگهداری ربات
"""

HELP_10 = """
<b><u>پینگ و آمار:</b></u>

/start : راه‌اندازی ربات موزیک
/help : دریافت لیست راهنما با توضیح دستورات
/ping : نمایش پینگ و آمار سیستم ربات
/stats : نمایش آمار کامل ربات
"""

HELP_11 = """
<u><b>دستورات پخش:</b></u>

<b>v:</b> برای پخش ویدیو
<b>force:</b> برای پخش اجباری

/play یا /vplay : شروع پخش درخواستی در چت ویدیویی
/playforce یا /vplayforce : توقف پخش فعلی و شروع پخش درخواستی
"""

HELP_12 = """
<b><u>بر هم زدن صف پخش:</b></u>

/shuffle : بر هم زدن ترتیب آهنگ‌ها در صف
/queue : نمایش صف بر هم زده شده
"""

HELP_13 = """
<b><u>جلو و عقب بردن پخش:</b></u>

/seek [زمان به ثانیه] : جلو بردن پخش به زمان مشخص شده
/seekback [زمان به ثانیه] : عقب بردن پخش به زمان مشخص شده
"""

HELP_14 = """
<b><u>دانلود موزیک</b></u>

/song [نام آهنگ/لینک یوتیوب] : دانلود هر موزیک از یوتیوب به صورت MP3 یا MP4
"""

HELP_15 = """
<b><u>دستورات سرعت:</b></u>

می‌توانید سرعت پخش فعلی را کنترل کنید [فقط برای مدیران]

/speed یا /playback : تنظیم سرعت پخش صدا در گروه
/cspeed یا /cplayback : تنظیم سرعت پخش صدا در کانال
"""
