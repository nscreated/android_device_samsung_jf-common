# Copyright (C) 2012 The Android Open Source Project
# Copyright (C) 2013 The CyanogenMod Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
#
# This leverages the loki_patch utility created by djrbliss which allows us
# to bypass the bootloader checks on jfltevzw and jflteatt
# See here for more information on loki: https://github.com/djrbliss/loki
#

"""Custom OTA commands for jf devices"""

def FullOTA_CustomAsserts(info):

  info.script.AppendExtra('ifelse(is_substring("I337", getprop("ro.bootloader")), run_program("/sbin/sh", "-c", "busybox cp -R /system/rild/gsm/* /system/ && busybox rm /system/lib/libcnefeatureconfig.so"));')
  info.script.AppendExtra('ifelse(is_substring("I545", getprop("ro.bootloader")), run_program("/sbin/sh", "-c", "busybox cp -R /system/rild/vzw/* /system/"));')
  info.script.AppendExtra('ifelse(is_substring("I545", getprop("ro.bootloader")), run_program("/sbin/sh", "-c", "busybox sed -i \'s/ro.com.google.clientidbase=android-google/ro.com.google.clientidbase=android-verizon/g\' /system/build.prop"));')
  info.script.AppendExtra('ifelse(is_substring("L720", getprop("ro.bootloader")), run_program("/sbin/sh", "-c", "busybox cp -R /system/rild/cdma/* /system/ && busybox rm -rf /system/rild/cdma/lib/libril.so && busybox cp -R /system/rild/gsm/lib/libril.so /system/rild/cdma/lib/"));')
  info.script.AppendExtra('ifelse(is_substring("M919", getprop("ro.bootloader")), run_program("/sbin/sh", "-c", "busybox cp -R /system/rild/gsm/* /system/ && busybox rm /system/lib/libcnefeatureconfig.so"));')
  info.script.AppendExtra('ifelse(is_substring("R970", getprop("ro.bootloader")), run_program("/sbin/sh", "-c", "busybox cp -R /system/rild/usc/* /system/"));')
  info.script.AppendExtra('ifelse(is_substring("S970", getprop("ro.bootloader")), run_program("/sbin/sh", "-c", "busybox cp -R /system/rild/gsm/* /system/ && busybox rm /system/lib/libcnefeatureconfig.so"));')
  info.script.AppendExtra('ifelse(is_substring("S975", getprop("ro.bootloader")), run_program("/sbin/sh", "-c", "busybox cp -R /system/rild/gsm/* /system/ && busybox rm /system/lib/libcnefeatureconfig.so"));')
  info.script.AppendExtra('ifelse(is_substring("I9505", getprop("ro.bootloader")), run_program("/sbin/sh", "-c", "busybox cp -R /system/rild/gsm/* /system/ && busybox rm /system/lib/libcnefeatureconfig.so"));')
  info.script.AppendExtra('ifelse(is_substring("I9507", getprop("ro.bootloader")), run_program("/sbin/sh", "-c", "busybox cp -R /system/rild/gsm/* /system/ && busybox rm /system/lib/libcnefeatureconfig.so"));')
  info.script.AppendExtra('ifelse(is_substring("I9508", getprop("ro.bootloader")), run_program("/sbin/sh", "-c", "busybox cp -R /system/rild/gsm/* /system/ && busybox rm /system/lib/libcnefeatureconfig.so"));')
  info.script.AppendExtra('delete_recursive("/system/rild");')

def FullOTA_InstallEnd(info):
  info.script.Mount("/system")
  info.script.AppendExtra('set_metadata("/system/bin/qcks", "uid", 0, "gid", 2000, "mode", 0755, "capabilities", 0x0, "selabel", "u:object_r:mdm_helper_exec:s0");')
  info.script.AppendExtra('set_metadata("/system/bin/ks", "uid", 0, "gid", 2000, "mode", 0755, "capabilities", 0x0, "selabel", "u:object_r:mdm_helper_exec:s0");')
  info.script.AppendExtra('set_metadata("/system/bin/netmgrd", "uid", 0, "gid", 2000, "mode", 0755, "capabilities", 0x0, "selabel", "u:object_r:netmgrd_exec:s0");')
  info.script.AppendExtra('set_metadata("/system/bin/qmuxd", "uid", 0, "gid", 2000, "mode", 0755, "capabilities", 0x0, "selabel", "u:object_r:qmuxd_exec:s0");')
  info.script.script = [cmd for cmd in info.script.script if not "boot.img" in cmd]
  info.script.script = [cmd for cmd in info.script.script if not "show_progress(0.100000, 0);" in cmd]
  info.script.AppendExtra('package_extract_file("boot.img", "/tmp/boot.img");')
  info.script.AppendExtra('assert(run_program("/sbin/sh", "/system/etc/loki.sh") == 0);')
  info.script.Unmount("/system")
