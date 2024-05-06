[app]

# عنوان برنامه شما
title = My Kivy/KivyMD App

# نام بسته برنامه
package.name = mykivyapp

# دامنه بسته برنامه
package.domain = org.example

# دایرکتوری حاوی کد منبع
source.dir = .

# فرمت‌های فایلی که باید شامل شوند
source.include_exts = py,png,jpg,kv,atlas

# نسخه برنامه
version = 0.1

# نیازمندی‌های برنامه
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow==10.3.0,requests==2.31.0,sqlalchemy==2.0.30, werkzeug==3.0.3

# جهت نمایش برنامه
orientation = portrait

#
# تنظیمات خاص اندروید
#

# نشانی برنامه به صورت فول‌اسکرین
fullscreen = 1

# مجوزهای اندروید
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE

# API هدف اندروید
android.api = 31

# حداقل API پشتیبانی شده
android.minapi = 21

# نسخه NDK اندروید
android.ndk = 23b

# نسخه SDK اندروید
android.sdk = 30

# آیکون برنامه
#icon.filename = %(source.dir)s/data/icon.png

# پیش‌زمینه اپلیکیشن
#presplash.filename = %(source.dir)s/data/presplash.png

[buildozer]

# سطح ورودی‌های لاگ
log_level = 2

# هشدار در صورت اجرا با دسترسی روت
warn_on_root = 1
