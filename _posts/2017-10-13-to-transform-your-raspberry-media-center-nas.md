---
layout: post
title: How to transform your Raspberry Media Center in a NAS
post_series_id: raspberry-media-center
slug: how-to-transform-your-raspberry-media-center-nas
thumbnail: wp-content/uploads/2017/10/Raspberry_Samba.jpg
excerpt: In this article, I would like to show you how to transform your Raspberry Media Center in a Network Attached Server (NAS) and share your media files
categories: Multimedia
---

![How to transform your Raspberry Media Center in a NAS]({{ site.baseurl }}/wp-content/uploads/2017/10/Raspberry_Samba.jpg){:width="200" height="200" .responsive_img}

# How to transform your Raspberry Media Center in a NAS
_Posted on **{{ page.date | date_to_string }}**_

In this article, I would like to show you how to transform your Raspberry Media Center in a Network Attached Server (NAS) and share your media files (movies, tv-series, ebooks, music, documents, etc.) across your home network.

I use this feature to browse media files, hosted on my media center, from my PC (Windows or Mac), Tablet or Phone. This is very useful to organize photos, movies, TV series, and read e-books.

Before you read this article I assume:

1. you already [built your own Kodi Media Center with Raspberry]({{ site.baseurl }}/raspberry-media-center/);
2. you already [configured it]({{ site.baseurl }}/how-to-configure-kodi-media-center/).

## What is a NAS?

According to [Wikipedia, a Network Attached Server](https://en.wikipedia.org/wiki/Network-attached_storage) (NAS) is:

> a file-level computer data storage server connected to a computer network providing data access to a heterogeneous group of clients. NAS is specialized for serving files either by its hardware, software, or configuration. NAS systems are networked appliances which contain one or more storage drives, often arranged into logical, redundant storage containers or RAID.
> 
> Network-attached storage removes the responsibility of file serving from other servers on the network. They typically provide access to files using network file sharing protocols such as NFS, SMB/CIFS, or AFP. From the mid-1990s, NAS devices began gaining popularity as a convenient method of sharing files among multiple computers. Potential benefits of dedicated network-attached storage, compared to general-purpose servers also serving files, include faster data access, easier administration, and simple configuration.

The NAS we are going to build, obviously, has some limitations:

- It contains only one Hard Disk;
- No Redundancy/RAID support exists;
- Only Samba protocol will be supported.

With these limitations, if your Hard Disk will be damaged you lost all your data. The reason we need to set these limitations is that NAS hardware usually has higher performance and cost more than a Raspberry card. Moreover, attach more than one Hard Disk requires more Power than the one provided by commonly used Raspberry Power Supplies.  The only function we want to preserve is the sharing of data across the home network and make them accessible to heterogeneous devices (i.e. PC, Tablet, and Phones).

## Use Samba to share your files across your Home Network

In a Home Network, files can be shared using different protocols (i.e. NFS, Samba, SSH, and so on). Our media center already supports SSH for media files sharing, but it is not suitable to browse them using native programs like Explorer for Windows or Finder for Mac. For this reason, I decided to use Samba for this purpose. Samba is available in the OSMC App Store so the installation is very easy as I’ll show you in the next section.

## How to Install Samba on OSMC

Go on _My OSMC_ and access to the OSMC App Store.

![OSMC Samba Install 1]({{ site.baseurl }}/wp-content/uploads/2017/10/OSMC-Samba-Install-1.png){:width="450" height="253" .responsive_img}

![OSMC Samba Installation - Step 2]({{ site.baseurl }}/wp-content/uploads/2017/10/OSMC-Samba-Install-2.png){:width="450" height="253" .responsive_img}

Select the _Samba (SMB) Server_ service to install it on OSMC.

![OSMC Samba Installation - Step 3]({{ site.baseurl }}/wp-content/uploads/2017/10/OSMC-Samba-Install-3.png){:width="450" height="253" .responsive_img}

A window will be opened with information about Samba. Select the _Install_ button.

![OSMC Samba Installation - Step 4]({{ site.baseurl }}/wp-content/uploads/2017/10/OSMC-Samba-Install-4.png){:width="450" height="253" .responsive_img}

Select _Apply_ and wait until the installation will complete.

![OSMC Samba Installation - Step 5]({{ site.baseurl }}/wp-content/uploads/2017/10/OSMC-Samba-Install-5.png){:width="450" height="253".responsive_img}

Once the message “Operations successfully completed” appear you’ve done and your Samba server is up and running.

![OSMC Samba Installation - Step 6]({{ site.baseurl }}/wp-content/uploads/2017/10/OSMC-Samba-Install-6.png){:width="450" height="253" .responsive_img}

![OSMC Samba Installation - Step 7]({{ site.baseurl }}/wp-content/uploads/2017/10/OSMC-Samba-Install-7.png){:width="450" height="253" .responsive_img}

## How to Configure Samba on OSMC

Our goal now is to share our /media/KODI folder with all our devices in our domestic network because here is where we have all our media files (movies, TV Series, music, photos, ebooks, and so on). To do that you have to add the following lines to the _/etc/samba/smb.conf_ file:

    {% highlight plaintext %}
[kodi]
browsable = yes
read only = no
valid users = osmc
path = /media/KODI
comment = KODI Media
    {% endhighlight %}

To modify the file you can access the media center using ssh protocol as described in the section _Access to your Raspberry via SSH with Putty and Filezilla_ [of this article]({{ site.baseurl }}/how-to-configure-kodi-media-center/)_._

Restart the samba service to make the changes effective using the following command.

    {% highlight shell %}
sudo service samba restart
    {% endhighlight %}

## How to view your files from Windows

You can now access your media files from other devices of your domestic network. If you have a Windows machine open Explorer and type the network address using hostname _\\\\osmc.local\\kodi_ or IP _\\\\<your ip>\\kodi_. As you can notice, in the samba configuration file, you added a new section called **_kodi_** and this is the name you have to use to access the shared folder.

When the system asks for credentials, insert the one for _the osmc_ user.

![Samba Share Windows]({{ site.baseurl }}/wp-content/uploads/2017/10/Samba_Share_Windows.png){:width="450" height="219" .responsive_img}

## How to view your files from Mac

To access the shared folder on Mac open Finder and click on Go->Connect to Server:

![Samba Share on Mac - Connect to Server]({{ site.baseurl }}/wp-content/uploads/2017/10/Samba-Share-on-Mac-1.jpg){:width="450" height="373" .responsive_img}

Insert the address \\\\osmc.local or \\\\<your IP number> and click on Connect:

![Samba Share on Mac - Insert IP]({{ site.baseurl }}/wp-content/uploads/2017/10/Samba-Share-on-Mac-2.jpg){:width="450" height="218" .responsive_img}

Then click on Continue and select the KODI shared name:

![Samba Share on Mac - Select Shared Folder]({{ site.baseurl }}/wp-content/uploads/2017/10/Samba-Share-on-Mac-3.jpg){:width="450" height="381" .responsive_img}

You’ll see your KODI Media Files on Mac:

![Samba Share on Mac - Media Files]({{ site.baseurl }}/wp-content/uploads/2017/10/Samba-Share-on-Mac-4.jpg){:width="450" height="258" .responsive_img}

## How to view your files from Android devices

To browse files hosted on my KODI Media Center from my Android devices, I use the [File Manager](https://play.google.com/store/apps/details?id=com.asus.filemanager&hl=it) app. To access to remote files you can go to Menu -> Network Storage -> Network Resource and click on your OSMC system. From there you can browse your files as shown in the following photo.

![Samba File Manager]({{ site.baseurl }}/wp-content/uploads/2017/10/Samba_File_Manager.png){:width="450" height="456" .responsive_img}
