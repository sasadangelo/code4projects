---
layout: post
title: How to speed up Android Virtual Device
post_series_id: android-game-programming
slug: how-to-speed-up-android-virtual-device
thumbnail: assets/img/android_virtual_device-mini.jpeg
excerpt: In this article, I will show you how to speed up Android Virtual Device in order to run your application simulation quickly.
categories: Android
---

![How to speed up Android Virtual Device](assets/img/android_virtual_device-mini.jpeg){:width="216" height="200" }

# How to speed up Android Virtual Device
_Posted on **{{ page.date | date_to_string }}**_

This is the fourth article of the [Android Game Programming](android-game-programming) series. Here I would like to explain, step by step, how to speed up Android Virtual devices to run your video game with acceptable performance on Intel processors.

## The Problem

If you tried to run your application on a virtual device on Windows platform two things may have happened. If you were lucky, the application started but took a huge amount of time or, in the worst case, you got an error message like this:

> This computer does not support Intel Virtualization Technology (VT-x). HAXM cannot be installed. Please refer to the Intel HAXM documentation for more information.

In both cases, the solution is to install a driver called **Intel x86 Emulator Accelerator** as known as **HAXM Installer**. It is a hardware accelerator based on VT-x technology that speeds up the execution of Android applications on emulated devices.

To install these drivers, you must first restart the computer and boot the BIOS. To do that, you have to press a special key (i.e F2, F8, Delete, ESC, etc.) during startup.

## Install Intel x86 Emulator Accelerator (HAXM Installer)

Once entered, depending on the type of BIOS installed, you will need to enable the Intel Virtualization Technology that you can find with names like “VT”, “VT-d” or “Virtualization Technology”, save the configuration and exit.

After restarting Windows and Android Studio, you will need to download the HAXM Installer which will install the hardware acceleration drivers. To do this, select _Tools → Android → SDK Manager_ to start the SDK Manager.

![Android Studio HAXM SDK Manager](assets/img/AndroidStudioHAXMSDKManager.png){:width="400" height="142" }

The SDK Manager panel will start, in which you have to select, on the left, _Appearance & Behavior → System Settings → Android SDK_ and on the right the SDK Tools tab. You must then scroll through the list and select Intel x86 Emulator Accelerator (HAXM Installer) and proceed with the installation.

![Android Studio HAXMhaxm](assets/img/AndroidStudioHAXM.png){:width="400" height="189" }

**Warning**: this procedure does not install the HAXM drivers but only downloads the driver installer.

To install the drivers you will need to proceed as described below. Go to the location: _<Android SDK Location>\\extras\\intel\\Hardware\_Accelerated\_Execution\_Manager_ where <Android SDK Location> is the path where the Android SDK is installed. In this folder you will find two executables:

-   _haxm\_check.exe_, check if HAXM drivers are already installed.
-   _intelhaxm-android.exe_, install HAXM drivers. Launching the second executable will start a Windows installation in which you simply have to confirm the default configuration. Once installed the drivers you will be able to run your application on a virtual device.

**Warning**: sometimes it happens that antivirus software blocks the execution of the emulator. If you have problems try disabling it temporarily. If it is the cause of the blockage, be sure to insert the rule to bypass it.

## What’s next?

Now that you’ve learned how to create your first Android application, it’s time to write your first video game.

To do this, you will start from your first “Hello World” application and with exercises of increasing difficulty you will create a framework to manage the basic functionalities of your video game such as graphics, sounds, inputs, and files.

The framework will be the foundations on top of which we will create Droids, a Tetris clone.