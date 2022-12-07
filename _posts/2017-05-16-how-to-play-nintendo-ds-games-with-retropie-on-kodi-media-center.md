---
layout: post
title: How to play Nintendo DS games with Retropie on Kodi Media Center
post_series_id: raspberry-media-center
slug: how-to-play-nintendo-ds-games-kodi-media-center
thumbnail: assets/img/nintendo-ds.jpeg
excerpt: In this article, I would like to show you how to play Nintendo DS games with Retropie on your Raspberry Kodi Media Center.
categories: Multimedia
---

![How to play Nintendo DS games with Retropie on Kodi Media Center](assets/img/nintendo-ds.jpeg){:width="200" height="157" .responsive_img}

# How to play Nintendo DS games with Retropie on Kodi Media Center
_Posted on **{{ page.date | date_to_string }}**_

In this article, I would like to show you how to play Nintendo DS games with Retropie on your Raspberry Kodi Media Center.

Before you read this article I assume:

1.  you already [built your own Kodi Media Center with Raspberry](raspberry-media-center);
2.  you already [configured it](how-to-configure-kodi-media-center).
3.  you already [configured your Retro Game platform](how-to-transform-kodi-media-center-retro-game-platform).

## What is DraStic?

[DraStic](http://drastic-ds.com/) is a Nintendo DS closed source emulator written originally for Android and later ported on Raspberry Pi 2/3. [This is the author’s announcement on the Raspberry Pi forum](https://www.raspberrypi.org/forums/viewtopic.php?f=78&t=170820). Immediately the [news arrived on the Retropie forum](https://retropie.org.uk/forum/topic/7435/drastic-nintendo-ds-emulator-out-now-for-pi2-3/13) and in a few days, it was included in the official Retropie installation procedure as an experimental emulator. Unfortunately, after a few days, the feature was rolled back because the author didn’t want a beta release in Retropie. In fact, the emulator is still in beta version but it is quite stable and if you continue to read this article I’ll explain to you how to install it.

Retropie officially supports another Nintendo DS emulator called [lr-desmume](https://github.com/RetroPie/RetroPie-Setup/wiki/Nintendo-DS) and, as reported on official documentation: _“it is very experimental and lags quite a bit even with an overclocked RPI 2/3”_.

Before we start with the installation I suggest you read the official [FAQ](http://drastic-ds.com/viewtopic.php?f=4&t=2) because there you’ll find answers to common questions like this one:

> **Q: Does DraStic support 3DS/2DS games? Will it in the future?**  
> A: No, it does not and never will. 3DS is an entirely different system, a full generation ahead, like N64 to Gamecube. And yes this means 2DS won’t work either, it’s the same thing as 3DS but with a different screen.

## How to install DraStic on Retropie

[Download the following file](https://raw.githubusercontent.com/RetroPie/RetroPie-Setup/master/scriptmodules/emulators/drastic.sh) and copy it under _/home/osmc/Retropie-Setup/scriptmodules/emulators_ using [FileZilla](https://filezilla-project.org/). Start Emulation Station going on Add-ons -> Retrosmc_._

![Retrosmc Launcher](assets/img/Retrosmc-Launcher.png){:width="450" height="253" }

Select _Retropie_ menu item and next _Retropie Setup_.

![Retropie Configuration](assets/img/Retropie_Configuration.png){:width="450" height="253" .responsive_img}

![Retropie Setup](assets/img/Retropie_Setup.png){:width="450" height="253" .responsive_img}

A text menu will appear, select the _Manage packages -> Manage experimental packages -> drastic_. You can exit from Emulation Station going back with button B, then open the menu pressing the button SELECT and selecting the QUIT menu item and confirming the exit selecting YES.

Nintendo DS games are simple “.NDS” file you have to copy under _/home/osmc/Retropie/roms/nds_. You can use [Filezilla](https://filezilla-project.org/) to copy the files from your computer to your Raspberry Media Center. That’s all.

## How to play your Nintendo DS games

Starting from Kodi you can start Retropie again as explained above. You’ll notice that a new _Nintendo DS_ menu item has been added to the Retropie menu. If you select it you’ll see all the games installed.

![NintendoDS Menu](assets/img/NintendoDS_Menu.png){:width="450" height="253" .responsive_img}

![NintendoDS Games](assets/img/NintendoDS_Games.png){:width="450" height="253" .responsive_img}

Here a list of my favorite games that I have already tested with DraStic: [Fifa 2007](https://www.youtube.com/watch?v=-rU_1K0Gdfc), [Mario Kart](https://www.youtube.com/watch?v=F2hltWsF_IE), [Pirates of the Caribbean Pirates](https://www.youtube.com/watch?v=GPkU1wPPb7Q), [Tomb Raider Legend](https://www.youtube.com/watch?v=8gI3dlXWOec), and [Madagascar](https://www.youtube.com/watch?v=7MpaTn0VgVY).