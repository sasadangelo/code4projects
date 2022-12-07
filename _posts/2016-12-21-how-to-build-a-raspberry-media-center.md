---
layout: post
title: How to build a Raspberry Media Center
post_series_id: raspberry-media-center
slug: raspberry-media-center
thumbnail: assets/img/Hector_TV_Box-min.jpeg
excerpt: In this article, I would like to show you how to build your own Raspberry Media Center using Raspberry, an HDD and an enclosure.
categories: Multimedia
---

![How to build a Raspberry Media Center](assets/img/Hector_TV_Box-min.jpeg){:width="267" height="200" .responsive_img}

# How to build a Raspberry Media Center
_Posted on **{{ page.date | date_to_string }}**_

In this article series, I would like to show you how to build a Raspberry Media Center with an HDD and enclosure. This article will discuss only the hardware I bought and assembled to create it. The name of this Media Center solution is **Hector**.

## The Problem

Classic Raspberry Media Centers use 8GB or 16 GB SD cards. Once you start using them soon you realize that the space available is not enough to store all media files. The first and cheaper option is to buy an HDD to connect to your Raspberry but immediately some issues raise:

1.  How can I power it?
2.  Can I use a single power cable for Raspberry and HDD?
3.  What about the mess of cables next to the TV?
4.  What enclosure can I buy to keep all devices and cables?

I am writing this article because it is not easy to find an answer to these questions on the web. The most difficult part was to find a good enclosure that makes the solution elegant for a living room. Lots of articles on the web focus on Raspberry and KODI without taking into consideration the use of an HDD. Moreover, there are few enclosures available for Raspberry + HDD. The few available have some cons that make them unusable in my specific case. I will list all the possible alternatives at the end of this article with the reason why I discarded them.

## What to buy?

To build your own Raspberry Media Center it’s necessary to buy the right components like:

-   \* Raspberry PI 2 Model B – [Amazon](https://www.amazon.it/Raspberry-Pi-Modello-Quad-Core/dp/B00T2U7R7I/ref=sr_1_3?ie=UTF8&qid=1482318028&sr=8-3&keywords=raspberry+pi+2+model+b)
-   \*\* Kingston Micro SDHC/SDXC Class 10 UHS-I, 16 GB – [Amazon](https://www.amazon.it/gp/product/B0036V9AGU?redirect=true&ref_=oh_aui_detailpage_o01_s00&th=1)
-   Official Raspberry Power Supply 2 A – [Amazon](https://www.amazon.it/gp/product/B00MBH6XNS?psc=1&redirect=true&ref_=oh_aui_detailpage_o01_s00)
-   Western Digital Elements HDD 1Tb + USB cable – [Amazon](https://www.amazon.it/WD-Elements-Hard-Esterno-Portatile/dp/B00CRZ2PRM)
-   \*\*\* ~~WDLabs PiDrive Enclosure Square 6″x6″ – WSDLabs~~
-   2 x Startech.com USB 15 cm Cable Extension –  [Amazon](https://www.amazon.it/gp/product/B000E5CYW8/ref=oh_aui_detailpage_o05_s00?ie=UTF8&psc=1)
-   \*\*\*\* Tontec Dongle USB WI-FI Adapter – [Amazon](https://www.amazon.it/gp/product/B010AKMF3Y?psc=1&redirect=true&ref_=oh_aui_detailpage_o04_s00) (OPTIONAL)

> \* When I started the project Raspberry Pi 3 Model B haven’t released yet. If I started the project today I would opt for Raspberry Pi 3 Model B which already has a WIFI receiver built in and a Bluetooth as well.
> 
> \*\* If you’re interested in best performance for 4K block writes people on OSMC forum recommend the [OSMC card](https://osmc.tv/store/product/osmc-32gb-sd-card/). I haven’t used it but I trust their recommendation because everything I learned on Kodi was thanks to them.
> 
> \*\*\* Western Digital closed its WDLabs and the production of the enclosure is discontinued. There are other options on the web like [this one](https://www.amazon.it/Case-QUATTRO-Raspberry-Tinkerboard-incl/dp/B077S5G7ZT/ref=sr_1_4?adgrpid=101514356357&dchild=1&gclid=CjwKCAjwydP5BRBREiwA-qrCGsn6dVfLxoflQdxnos1xbCOICkxh9xMUKv9-iYjBVERQMqSF9aWyXRoCiCwQAvD_BwE&hvadid=437171236301&hvdev=c&hvlocphy=1008729&hvnetw=g&hvqmt=e&hvrand=15360306011341169533&hvtargid=kwd-296167067660&hydadcr=15885_1838983&keywords=raspberry+pi+3+hdd+case&qid=1597387621&sr=8-4&tag=slhyin-21) that I haven’t tried. If someone find a different solution can notify me with a comment to this article.
> 
> \*\*\*\* For best performance I suggest connecting your Raspberry to an Ethernet cable. If this is not possible, I suggest you buy the WI-FI Adapter listed that works with Raspberry and OSMC.

Hector includes also other components like a DVB-T USB and two Gamepads. I haven’t listed them here because they are out of the scope of this article.

## The Solution: Hector a Raspberry Media Center

![Raspberry Media Center with TV](assets/img/hector-next-tv.jpeg){:width="400" height="300" .responsive_img}

The first issue I needed to solve was the power supply. In the beginning, I used a normal charger for the Samsung phone. Immediately I learned that it does not suit a TV box. The main problem is that it should provide 2A current to power the system. Samsung power supplies usually declare a current from 0.5 A to 2A, but those numbers are not reliable.

![Raspberry Pi Power Supply](assets/img/raspberry-pi-power-supply.jpeg){:width="400" height="315" .responsive_img}

I solved the problem using the official Raspberry Power Supply. Once [OSMC](https://osmc.tv/) installation completes, set the max\_current option to 1 in the /boot/config.txt file. OSMC is a Raspberry Linux distribution for Media Centers with a built-in KODI.

Connect the HDD to a Raspberry USB port. To cut the mess of cable the best solution is to buy a good enclosure (see above).

The first step is to remove the HDD from its enclosure. You can use a small precision screwdriver. You have to remove also the screws it has on the side used to fit it into its enclosure.

![HDD enclosure](assets/img/hdd-enclosure.jpeg){:width="300" height="400" .responsive_img}

![HD out enclosure](assets/img/hd-out-enclosure.jpeg){:width="300" height="400" .responsive_img}

![HDD back](assets/img/hdd-back.jpeg){:width="300" height="400" .responsive_img}

At this point, you can put Raspberry and HDD in the enclosure using few screws available in the enclosure package. With HDD cable connects Raspberry with HDD.

![HDD Raspberry Enclosure Cables DVB](assets/img/hdd-raspberry-enclosure-cables-dvb.jpg){:width="400" height="300" .responsive_img}

As you can see I have also a WI-FI dongle in the enclosure that works fine without any connection issues.

I have a [TV Antenna stick](https://www.amazon.it/TrekStor-59900-Trekstor-DVBT-Stick-Terres/dp/B007Y6GA6Q) that I use to watch TV on KODI. Since it does not fit inside the box I bought two USB extensors. I use them also to attach two gamepads that my kids use to play video games. In this way, without open the box I disconnect the TV stick and connect the Gamepads.

![Raspberry Media Center](assets/img/Hector_TV_Box-min.jpeg){:width="267" height="200" .responsive_img}

The enclosure is easy to open. There are no screws but magnets so you can open it and attach USB cables whenever you want. To be honest I do not like this option and this is the reason I bought the two USB extensors.

## Are there alternatives to this solution?

Yes, there are, but here I will explain why I discarded them. Most articles on the web suggest using two power supply one for Raspberry and another for HDD. I do not like this solution. Would you buy a TV Box if it provides two power supplies? I think no, it doesn’t make sense. Others suggest using a Power HUB that in my opinion is too complicated and add another piece of hardware.

As I said above the most difficult part was to find the right enclosure for the solution. I found a few alternatives with its own power supply solution. Here I want to report them with the reason why I discarded them.

### OSMC Pi Drive:

~~OSMC Pi Drive is a complete solution to build a Media Center with Raspberry. It provides the enclosure, a 384 Gb HDD, and cables. I discarded it because I already had the HDD. Moreover, 384 Gb is too low for a Media Center in my opinion. Today, for example, my media files go over this dimension. I think the best part of this solution is the enclosure but it is exactly the same you can buy on WDLabs. If you do not have an external HDD already and 384 GB are enough for you, then this solution could be right for you.~~

This option is not available anymore because the OSMC team discontinued its production.

### Plusberry:

~~[Plusberry](https://www.indiegogo.com/projects/plusberry-pi-media-box-running-on-raspberry-pi#/) is the best option today available on the web. The solution provides 3A power supply with a Power HUB so you can connect several peripherals. There are two important drawbacks: it is expensive and there are shipping issues. In fact, there are a lot of negative comments on the Comment page. The cost would worth it, but I do not think it is wise to spend 64$ with the risk to not receive the enclosure. I am sure the solution is not a scam and the author will solve soon all the issues, in the meanwhile, I suggest to not buy it.~~

Starting from May 1st Plusberry is not an option anymore. On April 30th the project was definitively shut down, here the announcement of the author:

> We are very sorry to announce that we have come to realize we cannot continue supporting this project. As many of you already experienced, we had major issues supplying the remaining outstanding orders. We have tried hard to supply the remaining units, but as time passes and the amounts decrease, we cannot sustain manufacturing and shipping anymore.

### Media Pi Plus:

[Media Pi Plus](https://www.amazon.com/Limited-Raspberry-MEDIAPI-integrated-Remote/dp/B00SEGYY7C/ref=sr_1_14?s=electronics&ie=UTF8&qid=1483390743&sr=1-14&keywords=raspberry+case+box) is like Plusberry and it works for Raspberry Pi 2 and 3. It is more than a simple enclosure, it has 5 USB ports: 2 in front and 3 at the rear of the case. There is space for HDD and a 5V 3A Power Supply. I think this could be a good solution but maybe too expensive.

### WDLabs WD PiDrive Enclosure:

~~WD PiDrive Enclosure is the first enclosure I bought and I put it immediately into the trash. The reason is that on the top there is no cover so from an aesthetic point of view I do not like to see circuits in my living room. The plastic separator in the box is small and there is the risk that circuits are touching each other. There are no screws. It’s the worst enclosure I saw in my life.~~

Western Digital closed its WDLabs and the production of this enclosure is discontinued. There are other options on the web like [this one](https://www.amazon.it/Case-QUATTRO-Raspberry-Tinkerboard-incl/dp/B077S5G7ZT/ref=sr_1_4?adgrpid=101514356357&dchild=1&gclid=CjwKCAjwydP5BRBREiwA-qrCGsn6dVfLxoflQdxnos1xbCOICkxh9xMUKv9-iYjBVERQMqSF9aWyXRoCiCwQAvD_BwE&hvadid=437171236301&hvdev=c&hvlocphy=1008729&hvnetw=g&hvqmt=e&hvrand=15360306011341169533&hvtargid=kwd-296167067660&hydadcr=15885_1838983&keywords=raspberry+pi+3+hdd+case&qid=1597387621&sr=8-4&tag=slhyin-21) that I haven’t tried. If someone finds a different solution can notify me with a comment on this article. This option is not available anymore

### **OSMC Pi Drive Case:**

~~The OSMC Team recently added the possibility to buy the Pi Drive case alone. There are two versions of the case: standard and bamboo. These cases are produced by Western Digital for OSMC so they are similar to the one I am using.~~

OSMC Pi Drive Case was a resell of the WD PiDrive Enclosure. Since Western Digital discontinued its production the OSMC removed it from its store.

### Raspberry PI B+/2 + HDD 2.5″ case:

The main problem with [this case](https://www.thingiverse.com/thing:702489) is that you need a 3D printer to print it. One of my requirements for the enclosure was that it should be elegant and this enclosure is the opposite. I didn’t like it.

### Tontec Case:

The [Tontect case](https://www.amazon.it/gp/product/B00OFOVZTC?psc=1&redirect=true&ref_=oh_aui_detailpage_o01_s01) is a perfect solution for people that use a Network Attached Server (NAS) instead of an HDD. NAS is the best storage solution but also the more expansive. If you have a NAS then you do not need an HDD and it is sufficient to buy an enclosure like this just to keep the Raspberry board.

It’s possible that there are other alternatives on the web. In this case, feel free to report them in the comments below.

## Conclusions

In my opinion, a good Media Center needs 4 elements to make it great:

-   An elegant enclosure. Because if you have it in the living room you cannot use noises computers or a solution with a mess of cable. The solution proposed in this article solves all these issues and your wife or mother will thank you.
-   Good storage, an HDD with enough space is fundamental. If you have a NAS it is even better.
-   Raspberry, the brain of your system.
-   Good software. In this case, OSMC with KODI is the optimal solution you can find. You can watch TV, Movies and TV Series. Moreover, you can store your photos and share them on social media. Finally, you can listen to your favorite Music, Play Games and much more.

In the [next article](how-to-configure-kodi-media-center), I will show you how to configure your Raspberry Media Center.