---
layout: post
title: How to turn your Kodi Media Center in a Torrent machine
post_series_id: raspberry-media-center
slug: how-to-turn-your-kodi-media-center-torrent-machine
thumbnail: assets/img/downloading-torrent.jpeg
excerpt: In this article, I would like to show you how to turn your Kodi Media Center in a Torrent machine.
categories: Multimedia
---

![How to turn your Kodi Media Center in a Torrent machine](assets/img/downloading-torrent.jpeg){:width="200" height="133" }

# How to turn your Kodi Media Center in a Torrent machine
_Posted on **{{ page.date | date_to_string }}**_

In this article, I would like to show you how to turn your Kodi Media Center in a Torrent machine. Reading this article you’ll be able to search your torrents on your phone and queue them for download on your Kodi Box. You will not need any more to turn on your computer to manage your torrents.

Before you read this article I assume:

1.  you already [built your own Kodi Media Center](raspberry-media-center);
2.  you already [configured it](how-to-configure-kodi-media-center);
3.  you already [transformed it into a Netflix-like platform](kodi-box-media-library).

## Install Transmission on your Media Center

In order to download torrents from your Kodi Box, you’ll need a software called [Transmission](https://transmissionbt.com/). You won’t need to follow any complicated installation steps, because Transmission is available for installation in the OSMC App Store. In this section, I’ll show you how to install it.

In order to install Transmission on your Kodi Box go on MyOSMC -> App Store.

![OSMC App Store](assets/img//Kodi_App_Store.png){:width="450" height="253" }

Select Transmission Torrent Client and install it. That’s it.

![OSMC Transmission Install](assets/img/Kodi_Transmission_Install.png){:width="450" height="253" }

## Install Torrnado app on your Android phone

My suggestion is to manage your Torrent download using your phone as a client. In this way, you do not have to turn on a computer whenever you need to start a new download or simply check its status.

Install the [Torrnado app](https://play.google.com/store/apps/details?id=com.gabordemko.torrnado&hl=it) on your Android phone. For iOS, there should be something similar. I am not an iPhone user so I cannot give you suggestion on this.

Configure in your Torrnado app the server to connect to. Enter the server IP address and leave the default port 9091.

![Torrnado Configuration](assets/img/Torrnardo-Configuration-270x480.png){:width="270" height="480" }

## Install apps for Torrent Search on your Android phone

Here I suggest installing a [Torrent Search Engine](https://play.google.com/store/apps/details?id=com.paolod.torrentsearch2&hl=it) or [Torrent Search](https://play.google.com/store/apps/details?id=it.nm.torrentsearch&hl=it). Whenever you search something and you find what you are looking for, these apps allow you to download torrent link or magnet link. If possible, choose the magnet link so that Torrnado will open automatically simplifying the download.

## Configure Transmission

When I first tested the download of a torrent, my home network congested completely. In these conditions was impossible to navigate with other devices (ie. phones, tablet, etc.). Initially, I thought I had to limit the download bandwidth for torrents, but I was wrong. To have a torrent client work properly it’s required to limit the upload bandwidth, not the download one. I know it seems counterintuitive but the explanation of this is in how TCP/IP works. In a TCP/IP system when a sender sends a packet an acknowledge packet is sent back from the receiver to the sender, in this way it knows the packet arrived and it can send other packets. If upload bandwidth is congested the whole communication over the network slow down.

In order to know exactly how to configure your Torrent machine to avoid congestions [make a speed test](https://www.speedtest.net/) of your connection and take note of the upload speed.

Convert the upload speed from Mbps to KBS multiplying the value by 1000. In my case, my speed is 0.78 Mbs so I have 780 KBS. Put this value on [this page](http://infinite-source.de/az/az-calc.html) as shown in the following picture.

![Torrent Client Configuration Tool](assets/img/Torrent-Client-Configuration-Tool.png){:width="450" height="264" }

The online tool will provide you the values you have to use in your configuration for the best results. Access to the web interface using this URL in your browser:

**http://<your IP address>:9091/transmission/web/**

![Transmission Web Interface](assets/img/Transmission-Web-Interface.png){:width="450" height="249" }

Click on Settings to configure the Max upload and download speed.

![Transmission Upload Speed](assets/img/Transmission-Upload-Speed.png){:width="200" height="133" }

![Transmission - Configure Download Speed](assets/img/Transmission-Configure-Download-Speed.png){:width="200" height="133" }

Add the Maximum number of connections per torrent and the Maximum number of connections globally in the tab Peers on the field: Max peers per torrent and Max peers globally.

![Transmission Configure Speed](assets/img/Transmission-Configure-Speed.png){:width="450" height="281" }

Then open the file _/home/osmc/.config/transmission-daemon/settings.json_ and set the value “upload-slots-per-torrent” with the value of Max upload slots per torrent.

![Transmission Upload Slots per Torrent](assets/img/Transmission-Upload-Slots-per-Torrent.png){:width="450" height="279" }

To configure _Max simultaneous downloads_ set the following values:

{% highlight json %}
"download-queue-enabled": true,
"download-queue-size": 2,
{% endhighlight %}

![Transmission - Download Queue](assets/img/Transmission-Download-Queue.png){:width="450" height="283" }

Finally, configure the download directory for complete and incomplete files:

{% highlight json %}
"download-dir": "/media/KODI/Movies",
"incomplete-dir": "/home/osmc/Downloads",
{% endhighlight %}

## Torrent files and Legal issues

People usually associate the Torrent name with piracy and sometimes they conclude that the use of Torrents is illegal. Torrent files are only small files used by the BitTorrent protocol to share large files online.

In and of itself torrents and torrenting is not illegal. But, and this is a tremendously important caveat, this changes depending on what you download.

Linux operating systems have been shared completely legally via torrent sites for years. The reason you can download these files is that the copyright holders have agreed to this method of distribution.

If the copyright holder hasn’t agreed, which is the case with pretty much anything you would otherwise have to pay for, then torrenting is seen as stealing.

A quick look at the most popular media downloaded via torrents in 2016 gives you an idea of why people usually associate Torrents with piracy. Game of Thrones headed the list followed by the Walking Dead and Westworld.

As you can imagine these premium titles are not officially made available for you to download for free. The huge production costs involved guarantee that they will only be found on paid services such as NowTV, Amazon Prime Video, iTunes, or Google Play Video.

For more details [read this article](http://www.pcadvisor.co.uk/feature/internet/are-torrents-legal-3653709/).