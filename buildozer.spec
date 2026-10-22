[app]
title = My Kivy Application
package.name = mykivyapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 1
android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.ndk_api = 21
android.archs = arm64-v8a, armeabi-v7a
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
p4a.branch = release-2022.12.20
